// Turn what you said out loud into a decision on the current item.
// Uses Claude when ANTHROPIC credentials are present; falls back to keyword matching otherwise.
import Anthropic from "@anthropic-ai/sdk";
import { betaZodOutputFormat } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const MODEL = process.env.CHIEF_MODEL || "claude-opus-5-5";

const Interpretation = z.object({
  action: z.enum(["decide", "defer", "more_info", "repeat", "stop"]),
  option_id: z.string().nullable(),
  note: z.string(),
  confirmed_irreversible: z.boolean(),
  standing_order: z
    .object({ description: z.string(), source: z.string().nullable(), keywords: z.array(z.string()) })
    .nullable(),
  spoken_reply: z.string(),
});

const SYSTEM = `You are a chief of staff on a phone call with your principal, walking through decisions their AI agents need.
Map what they just said to ONE action on the current item:
- decide: they picked an option (option_id must be one of the given ids). "Yes", "go with your recommendation", "sounds good" = the recommended option.
- defer: "later", "skip", "not now".
- more_info: they asked a question about the item. Answer it briefly in spoken_reply from the context given; if the context doesn't cover it, say so.
- repeat: they didn't hear it or asked you to repeat.
- stop: they want to end the call.
If the item is NOT reversible and they chose an option without clearly confirming, set confirmed_irreversible=false and ask for confirmation in spoken_reply.
If they said something like "don't ask me about this kind of thing again" / "just handle these", fill standing_order with a short description and 1-3 keywords.
note: any instruction they attached ("approve but tell them to cut the budget"), otherwise "".
spoken_reply: one short, natural sentence you'll say back. No markdown.`;

let client;
function getClient() {
  if (client !== undefined) return client;
  const hasCreds = process.env.ANTHROPIC_API_KEY || process.env.ANTHROPIC_AUTH_TOKEN;
  client = hasCreds ? new Anthropic() : null;
  return client;
}

export async function interpret(item, utterance) {
  const c = getClient();
  if (!c) return heuristic(item, utterance);

  const payload = {
    item: {
      from: item.source,
      question: item.question,
      context: item.context,
      options: item.options,
      recommended_option_id: item.recommendation,
      reversible: item.reversible,
    },
    they_said: utterance,
  };

  try {
    const res = await c.beta.messages.parse({
      model: MODEL,
      max_tokens: 2000,
      // Voice turn: keep latency low.
      output_config: { effort: "low", format: betaZodOutputFormat(Interpretation) },
      // If the model declines, the API retries on a fallback model in the same call.
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      system: SYSTEM,
      messages: [{ role: "user", content: JSON.stringify(payload) }],
    });
    if (res.stop_reason === "refusal" || !res.parsed_output) return heuristic(item, utterance);
    return validate(item, res.parsed_output);
  } catch (err) {
    console.error("[interpret] Claude call failed, using keyword fallback:", err.message);
    return heuristic(item, utterance);
  }
}

function validate(item, out) {
  if (out.action === "decide" && !item.options.some((o) => o.id === out.option_id)) {
    return { ...out, action: "repeat", spoken_reply: "Sorry, which option was that?" };
  }
  if (out.action === "decide" && !item.reversible && !out.confirmed_irreversible) {
    return { ...out, action: "more_info" };
  }
  return out;
}

/** Keyword fallback so the loop works without an API key (and in tests). */
export function heuristic(item, utterance) {
  const t = ` ${utterance.toLowerCase().replace(/[^a-z0-9 ]/g, " ")} `;
  const base = { option_id: null, note: "", confirmed_irreversible: false, standing_order: null };
  const has = (...words) => words.some((w) => t.includes(` ${w} `));

  if (has("stop", "hang up", "goodbye", "bye", "that s all")) return { ...base, action: "stop", spoken_reply: "Okay, talk later." };
  if (has("repeat", "again", "what")) return { ...base, action: "repeat", spoken_reply: "Sure." };
  if (has("later", "skip", "defer", "not now", "next")) return { ...base, action: "defer", spoken_reply: "Parked it." };

  const confirmed = has("confirm", "confirmed", "definitely", "do it");
  const byLabel = item.options.find((o) => t.includes(` ${o.label.toLowerCase()} `) || t.includes(` ${o.id.replace(/_/g, " ")} `));
  let option = byLabel?.id;
  if (!option && has("yes", "yeah", "yep", "sure", "approve", "go ahead", "sounds good", "recommendation", "do it")) {
    option = item.recommendation || item.options.find((o) => o.id === "yes")?.id;
  }
  if (!option && has("no", "nope", "reject", "decline")) option = item.options.find((o) => o.id === "no")?.id;
  if (!option) return { ...base, action: "repeat", spoken_reply: "Sorry, I didn't catch which option." };

  if (!item.reversible && !confirmed) {
    return { ...base, action: "more_info", option_id: option, spoken_reply: "That one can't be undone. Say confirm to go ahead." };
  }
  const label = item.options.find((o) => o.id === option).label;
  return { ...base, action: "decide", option_id: option, confirmed_irreversible: confirmed, spoken_reply: `Got it, ${label}.` };
}

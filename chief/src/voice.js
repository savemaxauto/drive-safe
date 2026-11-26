// The phone-call brief: Twilio fetches TwiML from us turn by turn.
// Each turn: say something, then <Gather input="speech"> and post the transcript back.
import { composeBrief, introLine, itemLine } from "./brief.js";
import { interpret } from "./interpret.js";
import { autoDecide } from "./rules.js";

const sessions = new Map(); // CallSid -> { itemIds, index }

const esc = (s) => String(s).replace(/[<>&'"]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", "'": "&apos;", '"': "&quot;" })[c]);

const VOICE = process.env.CHIEF_TTS_VOICE || "Polly.Joanna-Neural";
const say = (text) => `<Say voice="${VOICE}">${esc(text)}</Say>`;
const twiml = (inner) => `<?xml version="1.0" encoding="UTF-8"?><Response>${inner}</Response>`;
const gather = (prompt) =>
  `<Gather input="speech" action="/voice/answer" method="POST" speechTimeout="auto" timeout="8">${say(prompt)}</Gather>` +
  // No answer at all: move on rather than hang.
  `<Redirect method="POST">/voice/answer?silence=1</Redirect>`;

export function startCall(store, callSid, { minutes = 5, mode = "normal" } = {}) {
  const brief = composeBrief(store.pending(), { windowSeconds: minutes * 60, mode });
  sessions.set(callSid, { itemIds: brief.items.map((i) => i.id), index: 0, silences: 0 });
  const intro = introLine(brief, minutes);
  if (!brief.items.length) return twiml(say(intro) + "<Hangup/>");
  return twiml(gather(`${intro} ${itemLine(store.getItem(brief.items[0].id), 0)}`));
}

export async function answer(store, callSid, utterance, { silence = false } = {}) {
  const s = sessions.get(callSid);
  if (!s) return twiml(say("Sorry, I lost track of this call. I'll try again later.") + "<Hangup/>");
  const item = store.getItem(s.itemIds[s.index]);

  // Item may have been cancelled or decided elsewhere mid-call.
  if (!item || item.status !== "pending") return next(store, callSid, s, "");

  if (silence || !utterance) {
    s.silences += 1;
    if (s.silences >= 2) {
      sessions.delete(callSid);
      return twiml(say("Sounds like now's not a good time. I'll catch you later.") + "<Hangup/>");
    }
    store.defer(item.id, "no answer on call");
    return next(store, callSid, s, "I'll leave that one for later.");
  }
  s.silences = 0;

  const r = await interpret(item, utterance);
  if (r.standing_order) {
    store.addRule({ description: r.standing_order.description, source: r.standing_order.source || item.source, keywords: r.standing_order.keywords });
  }

  switch (r.action) {
    case "decide":
      store.decide(item.id, { option: r.option_id, note: r.note });
      return next(store, callSid, s, r.spoken_reply);
    case "defer":
      store.defer(item.id, r.note);
      return next(store, callSid, s, r.spoken_reply);
    case "stop":
      sessions.delete(callSid);
      return twiml(say(r.spoken_reply) + "<Hangup/>");
    case "repeat":
      return twiml(gather(`${r.spoken_reply} ${itemLine(item, s.index)}`));
    case "more_info":
    default:
      return twiml(gather(r.spoken_reply));
  }
}

function next(store, callSid, s, ack) {
  s.index += 1;
  // A standing order set during this call may now cover later items.
  while (s.index < s.itemIds.length) {
    const it = store.getItem(s.itemIds[s.index]);
    if (it?.status === "pending" && !autoDecide(store, it)) break;
    s.index += 1;
  }
  if (s.index >= s.itemIds.length) {
    sessions.delete(callSid);
    const left = store.pending().length;
    const tail = left ? `That's it for now. ${left} still open, I'll bring them up later.` : "That's everything. Inbox zero.";
    return twiml(say(`${ack} ${tail}`) + "<Hangup/>");
  }
  return twiml(gather(`${ack} Next. ${itemLine(store.getItem(s.itemIds[s.index]), s.index)}`));
}

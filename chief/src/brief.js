// Turn the pending queue into a brief that fits the time you actually have.

const URGENCY = { now: 100, today: 40, whenever: 10 };
const INTRO_SECONDS = 15;

export function estimateSeconds(item) {
  let s = 25 + 5 * item.options.length;
  if (!item.reversible) s += 20; // spoken confirmation
  if (item.context.length > 300) s += 15;
  return s;
}

export function score(item, now = new Date()) {
  let s = URGENCY[item.urgency] ?? 40;
  if (item.deadline) {
    const hoursLeft = (new Date(item.deadline) - now) / 36e5;
    if (hoursLeft < 1) s += 80;
    else if (hoursLeft < 4) s += 40;
    else if (hoursLeft < 24) s += 15;
  }
  const ageHours = (now - new Date(item.created_at)) / 36e5;
  s += Math.min(ageHours, 48) / 2; // stale asks drift up
  s += 5 * (item.deferrals?.length || 0);
  return s;
}

/**
 * @param items pending items
 * @param opts.windowSeconds how long you have
 * @param opts.mode "normal" | "driving" (driving: simple choices only, nothing visual)
 */
export function composeBrief(items, { windowSeconds = 300, mode = "normal", now = new Date() } = {}) {
  const eligible = items.filter((i) => {
    if (i.status !== "pending") return false;
    if (mode === "driving") return !i.needs_visual && i.options.length <= 3;
    return true;
  });
  const ranked = eligible
    .map((i) => ({ item: i, score: score(i, now), seconds: estimateSeconds(i) }))
    .sort((a, b) => b.score - a.score);

  const picked = [];
  let used = INTRO_SECONDS;
  for (const r of ranked) {
    if (used + r.seconds > windowSeconds) continue;
    picked.push(r);
    used += r.seconds;
  }
  const skipped = items.filter((i) => i.status === "pending").length - picked.length;
  return { items: picked.map((p) => p.item), estimatedSeconds: used, skipped };
}

export function introLine(brief, minutes) {
  const n = brief.items.length;
  if (n === 0) return "Nothing needs you right now.";
  const extra = brief.skipped > 0 ? ` ${brief.skipped} more can wait.` : "";
  return `You've got about ${minutes} minutes. ${n} ${n === 1 ? "thing needs" : "things need"} you.${extra}`;
}

export function itemLine(item, index) {
  const opts = item.options.map((o) => o.label).join(", or ");
  const rec = item.options.find((o) => o.id === item.recommendation);
  const parts = [
    `${index + 1}. From ${item.source}: ${item.question}`,
    item.context ? truncate(item.context, 280) : "",
    `Options: ${opts}.`,
    rec ? `They recommend ${rec.label}.` : "",
    item.reversible ? "" : "Heads up, this one can't be undone.",
  ];
  return parts.filter(Boolean).join(" ");
}

const truncate = (s, n) => (s.length <= n ? s : `${s.slice(0, n).replace(/\s+\S*$/, "")}…`);

// Standing orders: "stop asking me about X". The queue should shrink over time.
// A rule only ever accepts the agent's own recommendation, and never touches
// anything irreversible. Those always reach a human.

export function matchRule(item, rules) {
  if (!item.reversible || !item.recommendation) return null;
  return (
    rules.find((r) => {
      if (r.source && r.source !== "*" && r.source !== item.source) return false;
      if (r.tags?.length && !r.tags.every((t) => item.tags.includes(t))) return false;
      if (r.max_amount != null && (item.amount == null || item.amount > r.max_amount)) return false;
      if (r.keywords?.length) {
        const text = `${item.question} ${item.context}`.toLowerCase();
        if (!r.keywords.some((k) => text.includes(k.toLowerCase()))) return false;
      }
      return true;
    }) || null
  );
}

/** Apply standing orders to a freshly-queued item. Returns the rule used, if any. */
export function autoDecide(store, item) {
  const rule = matchRule(item, store.rules());
  if (!rule) return null;
  store.decide(item.id, {
    option: item.recommendation,
    note: `standing order: ${rule.description}`,
    by: "rule",
  });
  return rule;
}

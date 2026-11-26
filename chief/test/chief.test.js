import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

delete process.env.ANTHROPIC_API_KEY;
delete process.env.ANTHROPIC_AUTH_TOKEN;

const { Store } = await import("../src/store.js");
const { composeBrief } = await import("../src/brief.js");
const { matchRule, autoDecide } = await import("../src/rules.js");
const { parseIcs, findGap } = await import("../src/availability.js");
const { heuristic } = await import("../src/interpret.js");
const { startCall, answer } = await import("../src/voice.js");

const tmpStore = () => new Store(path.join(fs.mkdtempSync(path.join(os.tmpdir(), "chief-")), "db.json"));

test("brief ranks urgent first and fits the window", () => {
  const s = tmpStore();
  s.addItem({ source: "a", question: "low", urgency: "whenever" });
  s.addItem({ source: "b", question: "urgent", urgency: "now" });
  s.addItem({ source: "c", question: "today", urgency: "today" });
  const brief = composeBrief(s.pending(), { windowSeconds: 15 + 35 * 2 });
  assert.deepEqual(brief.items.map((i) => i.question), ["urgent", "today"]);
  assert.equal(brief.skipped, 1);
});

test("driving mode drops visual and many-option items", () => {
  const s = tmpStore();
  s.addItem({ question: "look at diff", needs_visual: true });
  s.addItem({ question: "pick one", options: ["a", "b", "c", "d"] });
  s.addItem({ question: "simple" });
  const brief = composeBrief(s.pending(), { mode: "driving" });
  assert.deepEqual(brief.items.map((i) => i.question), ["simple"]);
});

test("standing orders auto-decide reversible items only, within amount", () => {
  const s = tmpStore();
  s.addRule({ description: "small refunds", keywords: ["refund"], max_amount: 200 });
  const small = s.addItem({ question: "Refund order 1?", amount: 50, recommendation: "yes" });
  const big = s.addItem({ question: "Refund order 2?", amount: 900, recommendation: "yes" });
  const final = s.addItem({ question: "Refund order 3?", amount: 20, recommendation: "yes", reversible: false });
  assert.ok(autoDecide(s, small));
  assert.equal(s.getItem(small.id).status, "auto_decided");
  assert.equal(matchRule(big, s.rules()), null);
  assert.equal(matchRule(final, s.rules()), null);
});

test("ics parsing and gap finding", () => {
  const ics = [
    "BEGIN:VCALENDAR",
    "BEGIN:VEVENT", "DTSTART:20261126T140000", "DTEND:20261126T150000", "END:VEVENT",
    "BEGIN:VEVENT", "DTSTART:20261126T151200", "DTEND:20261126T160000", "END:VEVENT",
    "END:VCALENDAR",
  ].join("\r\n");
  const events = parseIcs(ics);
  assert.equal(events.length, 2);
  const gap = findGap(events, { now: new Date("2026-11-26T14:58:00") });
  assert.equal(gap.minutes, 12); // 15:00 -> 15:12
  assert.equal(findGap(events, { now: new Date("2026-11-26T14:20:00") }), null); // in a meeting
  assert.equal(findGap(events, { now: new Date("2026-11-26T22:00:00") }), null); // after hours
});

test("heuristic interpretation", () => {
  const item = { options: [{ id: "ship", label: "Ship it" }, { id: "hold", label: "Hold" }], recommendation: "ship", reversible: true };
  assert.equal(heuristic(item, "yeah go ahead").option_id, "ship");
  assert.equal(heuristic(item, "hold").option_id, "hold");
  assert.equal(heuristic(item, "later").action, "defer");
  const irreversible = { ...item, reversible: false };
  assert.equal(heuristic(irreversible, "yes").action, "more_info");
  assert.equal(heuristic(irreversible, "yes confirm").action, "decide");
});

test("full voice call walks the queue", async () => {
  const s = tmpStore();
  const a = s.addItem({ source: "billing", question: "Approve the refund?", recommendation: "yes", urgency: "now" });
  const b = s.addItem({ source: "claude-code", question: "Merge the PR?", options: ["Merge", "Hold"], recommendation: "merge" });
  const c = s.addItem({ source: "ops", question: "Delete old backups?", reversible: false, recommendation: "yes" });

  let xml = startCall(s, "CA1", { minutes: 5 });
  assert.match(xml, /Approve the refund/);
  xml = await answer(s, "CA1", "yes");
  assert.equal(s.getItem(a.id).decision.option, "yes");
  assert.match(xml, /Merge the PR/);
  xml = await answer(s, "CA1", "hold");
  assert.equal(s.getItem(b.id).decision.option, "hold");
  assert.match(xml, /can.*t be undone/);
  xml = await answer(s, "CA1", "yes");
  assert.equal(s.getItem(c.id).status, "pending"); // asked to confirm
  xml = await answer(s, "CA1", "yes confirm");
  assert.equal(s.getItem(c.id).decision.option, "yes");
  assert.match(xml, /Inbox zero/);
  assert.match(xml, /<Hangup\/>/);
});

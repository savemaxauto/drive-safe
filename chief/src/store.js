// Decision queue persisted to a single JSON file.
// Both the MCP server (agents asking) and the voice server (you answering) use it,
// so every operation re-reads the file and writes it back atomically.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const DEFAULT_PATH = process.env.CHIEF_DB || path.resolve("data/chief.json");

const empty = () => ({ items: [], rules: [], calls: [] });

export class Store {
  constructor(file = DEFAULT_PATH) {
    this.file = file;
  }

  load() {
    try {
      return { ...empty(), ...JSON.parse(fs.readFileSync(this.file, "utf8")) };
    } catch (err) {
      if (err.code === "ENOENT") return empty();
      throw err;
    }
  }

  save(db) {
    fs.mkdirSync(path.dirname(this.file), { recursive: true });
    const tmp = `${this.file}.${process.pid}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(db, null, 2));
    fs.renameSync(tmp, this.file);
  }

  update(fn) {
    const db = this.load();
    const result = fn(db);
    this.save(db);
    return result;
  }

  addItem(input, now = new Date()) {
    const item = {
      id: crypto.randomUUID().slice(0, 8),
      source: input.source || "unknown-agent",
      question: input.question,
      context: input.context || "",
      options: normalizeOptions(input.options),
      recommendation: input.recommendation ?? null,
      urgency: input.urgency || "today", // now | today | whenever
      reversible: input.reversible ?? true,
      needs_visual: input.needs_visual ?? false,
      deadline: input.deadline || null,
      tags: input.tags || [],
      amount: input.amount ?? null,
      status: "pending",
      decision: null,
      created_at: now.toISOString(),
    };
    if (item.recommendation && !item.options.some((o) => o.id === item.recommendation)) {
      throw new Error(`recommendation "${item.recommendation}" is not one of the option ids`);
    }
    this.update((db) => db.items.push(item));
    return item;
  }

  getItem(id) {
    return this.load().items.find((i) => i.id === id) || null;
  }

  pending() {
    return this.load().items.filter((i) => i.status === "pending");
  }

  decide(id, { option, note = "", by = "human" }, now = new Date()) {
    return this.update((db) => {
      const item = db.items.find((i) => i.id === id);
      if (!item) throw new Error(`no item ${id}`);
      if (item.status !== "pending") return item;
      if (option && !item.options.some((o) => o.id === option)) {
        throw new Error(`option "${option}" not valid for ${id}`);
      }
      item.status = by === "rule" ? "auto_decided" : "decided";
      item.decision = { option, note, by, at: now.toISOString() };
      return item;
    });
  }

  defer(id, note = "") {
    return this.update((db) => {
      const item = db.items.find((i) => i.id === id);
      if (item && item.status === "pending") item.deferrals = [...(item.deferrals || []), note];
      return item;
    });
  }

  cancel(id) {
    return this.update((db) => {
      const item = db.items.find((i) => i.id === id);
      if (item && item.status === "pending") item.status = "cancelled";
      return item;
    });
  }

  addRule(rule) {
    const full = { id: crypto.randomUUID().slice(0, 8), created_at: new Date().toISOString(), ...rule };
    this.update((db) => db.rules.push(full));
    return full;
  }

  rules() {
    return this.load().rules;
  }

  logCall(entry) {
    this.update((db) => db.calls.push({ at: new Date().toISOString(), ...entry }));
  }

  lastCallAt() {
    const calls = this.load().calls;
    return calls.length ? new Date(calls[calls.length - 1].at) : null;
  }
}

function normalizeOptions(options) {
  if (!options || options.length === 0) {
    return [
      { id: "yes", label: "Yes" },
      { id: "no", label: "No" },
    ];
  }
  return options.map((o, i) =>
    typeof o === "string" ? { id: slug(o) || `opt${i + 1}`, label: o } : { id: o.id, label: o.label },
  );
}

const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "").slice(0, 24);

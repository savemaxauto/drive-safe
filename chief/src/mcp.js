#!/usr/bin/env node
// MCP server any agent can use to escalate a decision to you instead of interrupting you.
// Run over stdio:  node src/mcp.js   (add it to Claude Code / Cursor / your agent's MCP config)
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { Store } from "./store.js";
import { autoDecide } from "./rules.js";

const store = new Store();
const server = new McpServer({ name: "chief", version: "0.1.0" });

const json = (obj) => ({ content: [{ type: "text", text: JSON.stringify(obj, null, 2) }] });

const publicView = (item) => ({
  id: item.id,
  status: item.status,
  decision: item.decision,
  question: item.question,
});

server.registerTool(
  "request_decision",
  {
    title: "Escalate a decision to the human",
    description:
      "Queue a decision for your human principal. They are briefed by voice when they have a free moment, " +
      "so do NOT block on this. Keep working on anything that doesn't depend on the answer and poll " +
      "check_decision later. Write the question so it can be understood when heard aloud, " +
      "give 2-4 short options, and say which you recommend.",
    inputSchema: {
      source: z.string().describe("Who is asking, e.g. 'billing-agent' or 'claude-code: drive-safe repo'"),
      question: z.string().describe("One sentence, speakable"),
      context: z.string().optional().describe("The 2-4 sentences they need to decide. No code or tables."),
      options: z.array(z.object({ id: z.string(), label: z.string() })).max(5).optional(),
      recommendation: z.string().optional().describe("id of the option you recommend"),
      urgency: z.enum(["now", "today", "whenever"]).optional(),
      reversible: z.boolean().optional().describe("false if this can't be undone (sending money, deleting, publishing)"),
      needs_visual: z.boolean().optional().describe("true if they must see something (a diff, a design) to decide"),
      deadline: z.string().optional().describe("ISO timestamp after which the decision is moot"),
      tags: z.array(z.string()).optional(),
      amount: z.number().optional().describe("Dollar amount at stake, if any"),
    },
  },
  async (args) => {
    const item = store.addItem(args);
    const rule = autoDecide(store, item);
    const current = store.getItem(item.id);
    return json({
      ...publicView(current),
      note: rule
        ? `Auto-decided by standing order "${rule.description}". Proceed with option ${current.decision.option}.`
        : "Queued. Continue other work and call check_decision later.",
    });
  },
);

server.registerTool(
  "check_decision",
  {
    title: "Check whether the human has decided",
    description: "Returns the status of a queued decision. Optionally waits up to 50s for an answer.",
    inputSchema: {
      id: z.string(),
      wait_seconds: z.number().min(0).max(50).optional(),
    },
  },
  async ({ id, wait_seconds = 0 }) => {
    const deadline = Date.now() + wait_seconds * 1000;
    let item = store.getItem(id);
    while (item && item.status === "pending" && Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 2000));
      item = store.getItem(id);
    }
    if (!item) return json({ error: `no decision with id ${id}` });
    return json(publicView(item));
  },
);

server.registerTool(
  "cancel_decision",
  {
    title: "Withdraw a queued decision",
    description: "Call this if the question became moot so the human isn't asked about it.",
    inputSchema: { id: z.string() },
  },
  async ({ id }) => json(publicView(store.cancel(id) || { id, status: "not_found" })),
);

await server.connect(new StdioServerTransport());

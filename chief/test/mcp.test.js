import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Store } from "../src/store.js";

test("agents can request and check decisions over MCP", async () => {
  const db = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "chief-")), "db.json");
  const transport = new StdioClientTransport({ command: "node", args: ["src/mcp.js"], env: { ...process.env, CHIEF_DB: db } });
  const client = new Client({ name: "test-agent", version: "0" });
  await client.connect(transport);
  try {
    const tools = (await client.listTools()).tools.map((t) => t.name).sort();
    assert.deepEqual(tools, ["cancel_decision", "check_decision", "request_decision"]);

    const res = await client.callTool({ name: "request_decision", arguments: {
      source: "test-agent", question: "Ship v2 today?", recommendation: "yes", urgency: "today" } });
    const queued = JSON.parse(res.content[0].text);
    assert.equal(queued.status, "pending");

    new Store(db).decide(queued.id, { option: "yes" });
    const checked = JSON.parse((await client.callTool({ name: "check_decision", arguments: { id: queued.id } })).content[0].text);
    assert.equal(checked.status, "decided");
    assert.equal(checked.decision.option, "yes");
  } finally {
    await client.close();
  }
});

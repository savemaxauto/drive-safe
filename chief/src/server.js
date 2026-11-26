#!/usr/bin/env node
// HTTP server: Twilio voice webhooks, a tiny JSON API, and the "call me when I'm free" scheduler.
import http from "node:http";
import crypto from "node:crypto";
import { Store } from "./store.js";
import { startCall, answer } from "./voice.js";
import { findGap, loadCalendar } from "./availability.js";

const env = process.env;
const PORT = Number(env.PORT || 8787);
const PUBLIC_URL = env.CHIEF_PUBLIC_URL; // e.g. https://chief.example.com (Twilio must reach it)
const store = new Store();

// ---------- outbound call ----------
export async function placeCall({ minutes = 5, mode = "normal", reason = "manual" } = {}) {
  const { TWILIO_ACCOUNT_SID: sid, TWILIO_AUTH_TOKEN: token, TWILIO_FROM: from, CHIEF_PHONE: to } = env;
  if (!sid || !token || !from || !to || !PUBLIC_URL) throw new Error("Twilio env vars / CHIEF_PUBLIC_URL not set");
  const body = new URLSearchParams({
    To: to,
    From: from,
    Url: `${PUBLIC_URL}/voice/start?minutes=${minutes}&mode=${mode}`,
    MachineDetection: "Enable", // don't brief your voicemail
  });
  const res = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${sid}/Calls.json`, {
    method: "POST",
    headers: { Authorization: `Basic ${Buffer.from(`${sid}:${token}`).toString("base64")}` },
    body,
  });
  if (!res.ok) throw new Error(`Twilio ${res.status}: ${await res.text()}`);
  const call = await res.json();
  store.logCall({ sid: call.sid, minutes, mode, reason });
  return call.sid;
}

// ---------- scheduler ----------
const POLL_MIN = Number(env.CHIEF_POLL_MIN || 5);
const MIN_BETWEEN_CALLS = Number(env.CHIEF_MIN_BETWEEN_CALLS_MIN || 90);

export async function tick(now = new Date()) {
  const pending = store.pending();
  if (!pending.length) return "empty";
  const urgent = pending.some((i) => i.urgency === "now");
  const last = store.lastCallAt();
  const sinceLast = last ? (now - last) / 6e4 : Infinity;
  if (!urgent && sinceLast < MIN_BETWEEN_CALLS) return "too-soon";
  if (urgent && sinceLast < 15) return "too-soon";

  const gap = findGap(await loadCalendar(), { now, minMinutes: urgent ? 2 : 5 });
  if (!gap) return "busy";
  await placeCall({ minutes: gap.minutes, reason: urgent ? "urgent" : "gap" });
  return `called (${gap.minutes} min window)`;
}

// ---------- http ----------
function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (c) => (data += c));
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

function twilioSignatureOk(req, params) {
  if (env.CHIEF_SKIP_TWILIO_SIGNATURE === "1") return true;
  const sig = req.headers["x-twilio-signature"];
  if (!sig || !env.TWILIO_AUTH_TOKEN || !PUBLIC_URL) return false;
  const url = PUBLIC_URL + req.url;
  const payload = url + Object.keys(params).sort().map((k) => k + params[k]).join("");
  const expected = crypto.createHmac("sha1", env.TWILIO_AUTH_TOKEN).update(payload).digest("base64");
  return expected.length === sig.length && crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(sig));
}

function apiAuthOk(req) {
  if (!env.CHIEF_API_TOKEN) return req.socket.remoteAddress === "127.0.0.1" || req.socket.remoteAddress === "::1";
  return req.headers.authorization === `Bearer ${env.CHIEF_API_TOKEN}`;
}

const send = (res, status, body, type = "application/json") => {
  res.writeHead(status, { "Content-Type": type });
  res.end(type === "application/json" ? JSON.stringify(body, null, 2) : body);
};

export const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  try {
    if (url.pathname.startsWith("/voice/")) {
      const params = Object.fromEntries(new URLSearchParams(await readBody(req)));
      if (!twilioSignatureOk(req, params)) return send(res, 403, { error: "bad signature" });
      if (params.AnsweredBy && params.AnsweredBy.startsWith("machine")) {
        return send(res, 200, "<Response><Hangup/></Response>", "text/xml");
      }
      if (url.pathname === "/voice/start") {
        const xml = startCall(store, params.CallSid, {
          minutes: Number(url.searchParams.get("minutes") || 5),
          mode: url.searchParams.get("mode") || "normal",
        });
        return send(res, 200, xml, "text/xml");
      }
      if (url.pathname === "/voice/answer") {
        const xml = await answer(store, params.CallSid, params.SpeechResult, { silence: url.searchParams.has("silence") });
        return send(res, 200, xml, "text/xml");
      }
    }

    if (url.pathname.startsWith("/api/")) {
      if (!apiAuthOk(req)) return send(res, 401, { error: "unauthorized" });
      const body = req.method === "POST" ? JSON.parse((await readBody(req)) || "{}") : {};
      if (req.method === "GET" && url.pathname === "/api/queue") return send(res, 200, store.pending());
      if (req.method === "GET" && url.pathname === "/api/rules") return send(res, 200, store.rules());
      if (req.method === "POST" && url.pathname === "/api/rules") return send(res, 201, store.addRule(body));
      if (req.method === "POST" && url.pathname === "/api/call") return send(res, 200, { sid: await placeCall({ ...body, reason: "manual" }) });
      // Signals from the phone: "I'm driving for 25 min", "AirPods in, free for 10".
      if (req.method === "POST" && url.pathname === "/api/available") {
        if (!store.pending().length) return send(res, 200, { called: false, reason: "nothing pending" });
        return send(res, 200, { called: true, sid: await placeCall({ minutes: body.minutes || 10, mode: body.mode || "normal", reason: body.signal || "signal" }) });
      }
    }
    send(res, 404, { error: "not found" });
  } catch (err) {
    console.error(err);
    send(res, 500, { error: err.message });
  }
});

if (import.meta.url === `file://${process.argv[1]}`) {
  server.listen(PORT, () => console.log(`chief listening on :${PORT}`));
  if (env.CHIEF_SCHEDULER !== "0") {
    setInterval(() => tick().then((r) => console.log(`[tick] ${r}`)).catch((e) => console.error("[tick]", e.message)), POLL_MIN * 6e4);
  }
}

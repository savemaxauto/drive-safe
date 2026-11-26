# chief

A voice chief of staff for your AI agents. Agents put questions in a queue instead of interrupting you. When you have a free moment, chief **calls you**, briefs you on the questions in priority order, takes your spoken answers, and sends each decision back to the agent that asked.

> The inverse of voice dictation: dictation helps you talk *to* the machine; chief helps the machine get *to you*, compressed and on your schedule.

## How it works

```
 agents ──MCP──▶ request_decision ──▶ queue ──▶ standing orders? ──yes──▶ auto-decided
                                         │              no
                                         ▼
           calendar gap / "I'm driving" / urgent item
                                         │
                                         ▼
                 Twilio call ─▶ brief fitted to the time you have
                                         │  you talk
                                         ▼
                 Claude interprets ─▶ decision / defer / follow-up / new standing order
                                         │
 agents ◀──MCP── check_decision ◀────────┘
```

| Piece | File | What it does |
|---|---|---|
| Queue | `src/store.js` | JSON-file store of decision items, standing orders and a call log |
| Agent interface | `src/mcp.js` | MCP tools `request_decision`, `check_decision`, `cancel_decision` |
| Standing orders | `src/rules.js` | "Stop asking me about refunds under $200." Only ever accepts the agent's recommendation, never on anything irreversible |
| Brief composer | `src/brief.js` | Ranks by urgency, deadline and age; fits items into the time window; driving mode skips anything visual or with more than 3 options |
| Availability | `src/availability.js` | ICS calendar gaps inside working hours |
| Voice | `src/voice.js`, `src/server.js` | Twilio TwiML speech loop, outbound calls, scheduler, small JSON API |
| Understanding replies | `src/interpret.js` | Claude maps what you said to an action (structured output, low effort for latency); falls back to keyword matching without an API key |

### Design rules
- **Never blocks agents.** `request_decision` returns immediately; agents keep working and poll.
- **Irreversible means confirm.** Items marked `reversible: false` need a spoken "confirm" and are never auto-decided.
- **The queue should shrink.** Say "don't ask me about these again" on a call and it becomes a standing order.
- **Don't nag.** At most one call per 90 minutes unless something is `urgency: "now"`; two silences end the call; voicemail is detected and hung up on.

## Setup

```bash
npm install
npm test
```

### 1. Point your agents at it (MCP)
Claude Code:
```bash
claude mcp add chief -- node /path/to/chief/src/mcp.js
```
Then tell the agent (for example in `CLAUDE.md`): *"When you need a human decision, use `request_decision` instead of stopping. Keep working on anything else, and check back with `check_decision`."*

### 2. Run the voice server
```bash
export ANTHROPIC_API_KEY=...          # optional; keyword fallback without it
export TWILIO_ACCOUNT_SID=... TWILIO_AUTH_TOKEN=... TWILIO_FROM=+1555...
export CHIEF_PHONE=+1555...           # your phone
export CHIEF_PUBLIC_URL=https://...   # where Twilio can reach this server (e.g. an ngrok URL)
export CHIEF_CALENDAR_ICS=https://... # your calendar's secret ICS URL (optional)
export CHIEF_API_TOKEN=...            # protects /api/*
npm start
```

Other env: `CHIEF_DB` (default `data/chief.json`), `PORT` (8787), `CHIEF_POLL_MIN` (5), `CHIEF_MIN_BETWEEN_CALLS_MIN` (90), `CHIEF_MODEL` (`claude-opus-5-5`), `CHIEF_TTS_VOICE`, `CHIEF_SCHEDULER=0` to disable auto-calls.

### 3. Availability signals
Calendar gaps are checked automatically. To tell chief you're free right now (for example from an iOS Shortcut when CarPlay connects):
```bash
curl -X POST $CHIEF_PUBLIC_URL/api/available -H "Authorization: Bearer $CHIEF_API_TOKEN" \
  -d '{"minutes":25,"mode":"driving","signal":"carplay"}'
```

### API
- `GET /api/queue`: pending items
- `GET|POST /api/rules`: standing orders `{description, source?, keywords?, tags?, max_amount?}`
- `POST /api/call`: call me now `{minutes, mode}`
- `POST /api/available`: availability signal (calls only if something is pending)

## Not built yet
- Real-time speech-to-speech instead of Twilio's turn-based `<Gather>` (lower latency, interruptible)
- "Send it to my phone" handoff for `needs_visual` items
- iOS app: AirPods and motion signals, push-to-brief
- Executing decisions directly (sending the email, merging the PR) instead of handing them back to the agent
- More sources: email, Slack, GitHub review requests

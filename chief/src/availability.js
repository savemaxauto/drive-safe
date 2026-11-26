// When are you free? Calendar gaps plus explicit signals (driving, AirPods in, "call me now").

/** Minimal ICS parser: pulls DTSTART/DTEND pairs out of VEVENTs. Handles UTC and floating times. */
export function parseIcs(text) {
  const events = [];
  const unfolded = text.replace(/\r?\n[ \t]/g, "");
  for (const block of unfolded.split("BEGIN:VEVENT").slice(1)) {
    const start = icsDate(block.match(/^DTSTART[^:]*:(.+)$/m)?.[1]);
    const end = icsDate(block.match(/^DTEND[^:]*:(.+)$/m)?.[1]);
    const transparent = /^TRANSP:TRANSPARENT/m.test(block);
    if (start && end && !transparent) events.push({ start, end });
  }
  return events;
}

function icsDate(v) {
  if (!v) return null;
  const m = v.trim().match(/^(\d{4})(\d{2})(\d{2})(?:T(\d{2})(\d{2})(\d{2})(Z)?)?$/);
  if (!m) return null;
  const [, y, mo, d, h = "00", mi = "00", s = "00", z] = m;
  const iso = `${y}-${mo}-${d}T${h}:${mi}:${s}${z ? "Z" : ""}`;
  return new Date(iso);
}

/**
 * Is there a free window starting now (or within `lookaheadMin`) of at least `minMinutes`?
 * Returns { start, end, minutes } or null.
 */
export function findGap(events, { now = new Date(), minMinutes = 5, lookaheadMin = 10, maxMinutes = 30, workday = [8, 19] } = {}) {
  const hour = now.getHours();
  if (hour < workday[0] || hour >= workday[1]) return null;

  const busy = events
    .filter((e) => e.end > now)
    .sort((a, b) => a.start - b.start);

  let cursor = now;
  for (const e of busy) {
    if (e.start <= cursor) {
      if (e.end > cursor) cursor = e.end;
      continue;
    }
    break;
  }
  if ((cursor - now) / 6e4 > lookaheadMin) return null;

  const next = busy.find((e) => e.start >= cursor);
  const end = next ? next.start : new Date(cursor.getTime() + maxMinutes * 6e4);
  const minutes = Math.min(Math.floor((end - cursor) / 6e4), maxMinutes);
  if (minutes < minMinutes) return null;
  return { start: cursor, end, minutes };
}

export async function loadCalendar(url = process.env.CHIEF_CALENDAR_ICS) {
  if (!url) return [];
  const res = await fetch(url);
  if (!res.ok) throw new Error(`calendar fetch failed: ${res.status}`);
  return parseIcs(await res.text());
}

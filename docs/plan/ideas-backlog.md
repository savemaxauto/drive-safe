# Ideas backlog

Ideas worth revisiting later. Not part of the current plan or forecast.

## Marketing campaign: free freshener for becoming a lead (logged Nov 17, 2026)

**Idea:** Give the freshener away to people who become a lead ("get a quote, we'll send you this").

**Notes from first look:**
- A free kit costs about $14.25 to ship (product $3.75, fulfillment $5.00, postage $5.50).
- Kit contribution by offer: $29 paid = +$13.61; free with $6.95 shipping = −$7.80; fully free = −$14.25.
- Could work as a thank-you to people who already became a lead, or as a hook that lowers cold CPL. If CPL drops from $20.33 to about $12, the kit pays for itself on the first sale.
- Check lead-buyer contracts first: many price incentive-driven leads lower or refuse them.
- Free weakens the core idea that the driver pays to become a lead.
- If tested: show $29 vs $14.99 vs free + $6.95 shipping on the quote thank-you page, judged on refills and renewal leads, not just the first order.

## Lead timing: sell now, upgrade later (logged Nov 17, 2026)

**Question:** Hold opted-in drivers until 3–6 months of driving history before selling them as leads?

**First answer:** No. Sell when they're in market, and use the score to raise the price of later sales.
- App retention is about 2–7% of users after 30 days, and leads 30–90 days old resell for about $1.50–5.
- Waiting six months for a ~$46 premium sale beats selling now at $26.47 only if more than ~57% of drivers are still engaged.
- Ask for renewal month at checkout. Re-ask consent before each later sale ("Your policy renews next month. Want us to find you a better rate?").

## Smart scent: three scents by time of day, and a tag that tracks use (logged Nov 17, 2026)

**Source:** https://nfcwork.com/create-a-fragrance-profile-with-an-nfc-powered-smart-perfume-bottle/ (read from a PDF of the page). It's a sales page from an NFC tag maker in China (RFIDHY). The "high-end perfume brand" is never named. It claims retention up 53%, refill orders up 41% and gift purchases up 28%, with no source, so don't quote those numbers.

**New ideas from the page:**
- Gift mode: a special message shows when the person receiving it taps. For us, a parent gives the freshener to a new driver and the first tap shows their note. Parents of new drivers are also shopping for insurance, since adding a teen raises the bill. The lead is the parent, never the teen; counsel should review anything touching a minor's data.
- Scent by moment: "morning commute → citrus, evening → agarwood, stressful day → lavender." Their example is literally the commute.
- Build notes: glass and metal block NFC, so they move the antenna to the edge (they claim 99% scan success) and use on-metal tags hidden in metal caps. Our wood face is fine. A metal face or trim would need an on-metal tag.
- "Automatic refilling: detects low battery and orders replacements" contradicts their own battery-free cap. Treat it as marketing copy.

**What's interesting:**
- Three scents for different times of day.
- A tag that tracks use. The article's flow: tap the bottle cap, sensors detect usage, the app receives time, location and frequency, then gives recommendations, adjusts the fragrance to mood, and sends refill reminders.

**What works with version 1 (passive tag, no battery):**
- Tap to open the app, and the app logs time and how often. Yes.
- Location of each tap. Yes, but it comes from the phone, and only if the driver turned location on.
- Tap count without our app. Yes: NTAG213 has a built-in tap counter that can be added to the tag's web link, so even a tap that opens a web page counts. The counter is plain text and can be copied, so it isn't proof of a real tap. https://nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf
- Refill reminders. Yes, from the install date and the 30-day scent life. The Home mockup already shows days left.
- Recommendations. Yes, from the app side: which scents drivers keep, rate and reorder.
- Three scents by time of day. Partly. Sell a three-scent refill pack (morning, afternoon, evening) and let the app suggest when to swap.

**What needs the next version (battery and Bluetooth):**
- Sensors in the freshener. A passive NFC tag has no sensors or power. It only answers when a phone is near.
- One freshener holding three scents and switching by time of day. Needs three chambers and a powered pump or valve, which adds cost. Earlier work found the burst version only pays at about $35.
- Adjusting scent to mood. Needs powered dispensing plus a mood signal. Inferring emotion is sensitive data. Asking the driver ("Rough drive?") or using the drive itself (heavy braking, late night) is safer than guessing feelings. Needs counsel before any test.

**Precedents:**
- Paco Rabanne Phantom (2021): an NFC tag in the spray cap, no battery, opens digital content. Same passive approach as our version 1. https://www.engadget.com/paco-rabanne-nfc-fragrance-robot-bottle-140040817.html
- NXP describes beauty brands using secure NFC tags to prove products are genuine. A secure tag in each refill could stop knockoff refills and tell the app which scent is in. https://www.nxp.com/company/about-nxp/smarter-world-blog/BL-BEAUTY-PRODUCTS-SECURE-NFC-TAGS

**Value to us (paths.py, Nov 17):**
- Refill reminders, a day-part trio pack and a scent profile all aim at refill take (30% in the model) and app retention. They cost app work, not hardware.
- Each 5 points of refill take adds about $2.45 per customer over 3 years ($39.05 to $41.50). At Path B's 120K kits in 2029, that's about $290K per year's customers.
- Take of 35% plus a $27 trio pack: $46.34 per customer, up 19%. Test the price before using it.
- Usage tracking adds nothing new for us: our tap already logs the start of a drive, which is worth more than a spray log.

**Open questions:**
- A tag in the body and another in the refill could sit on top of each other. Check whether a phone reads the right one.
- Tap time and location over months show where someone drives. The same opt-in rules apply: off by default, its own switch, trimmed trip ends.

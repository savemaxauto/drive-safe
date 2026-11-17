# Save Max Lives freshener: product development plan

Draft, November 17, 2026. Covers three ways to build the product, what each costs and how long it takes, the standard path from idea to production, and the tests that decide which build to make.

All outside figures came from search summaries of vendor sites, retailer listings, filings and studies. None of the source pages could be opened from this session. Treat every number as a planning range until a supplier quote or a real test replaces it.

## 1. What the product has to do

1. Clip to a car air vent and hold through normal driving.
2. Release a pleasant scent for about 30 days per refill.
3. Turn on Drive Mode when the driver presses their phone to the face (NFC tag, iPhone Shortcut).
4. Ideally, give a noticeable burst of scent at that moment, as a small reward. ("Like a breath of fresh air.")
5. Never leak onto the dash, never damage the vent, and survive a parked car in summer.

### Hard requirements
| Requirement | Target | Why |
|---|---|---|
| Landed cost | Retail price divided by 4 or less ($7.25 at $29, $8.75 at $35) | Standard rule for direct-to-consumer hardware |
| Heat | Passes an 85°C heat soak with no warping, leaking or swelling | Dashboards average 69°C after an hour in sun and have hit 89°C (ASU study, 2018) |
| Leaks | No fragrance reaches the dash, vent or seats in any position | Febreze (2020, 2023), Glade (2016) and Bath & Body Works (2016) faced class actions over leaking car fresheners |
| Materials | Every part that touches fragrance is PP, POM, HDPE or glass | Fragrance oils crack polystyrene, polycarbonate, ABS and acrylic |
| NFC | A phone in a normal case reads the tag through the face, every time | Small tags fail through 5 mm; use a 25 mm tag right behind a thin face |
| Vent load | A press can't break a vent slat | Vent phone mounts are rated around 5 N (about 1 lb); perfume pumps need 10 to 45 N to press |
| Fragrance | Flash point above 60°C (140°F) | Small packages then ship by ground without hazmat rules (49 CFR 173.150) |
| Scent type | Pad or solid core, not a spray, unless testing proves a spray is safe | Pads fall under IFRA category 12; pump sprays fall under 10B, with tighter limits |

## 2. Three ways to build it

| | 1. Basic | 2. Press-to-puff | 3. Powered burst |
|---|---|---|---|
| How it works | Scent pad releases scent all the time. NFC tag turns on Drive Mode. | Same, plus pressing the face pushes a puff of air through the refill (bellows) or a metered spray (pump). No battery. | Same, plus a small battery and fan fire a burst when you press. Later version could fire only once the phone locks. |
| The reward moment | Only the tap and Drive Mode | A puff you can smell, if the mechanism is strong enough | A clear burst every time |
| Unit cost, landed at 10k | $1.55 to $5.30 | $1.90 to $8.30 | $5.50 to $9.65 (lean version) |
| One-time cost, lean path | $25K to $45K | $40K to $115K | $60K to $150K |
| One-time cost, design firm | $70K to $125K | up to about $190K | up to about $290K |
| Time to first production | 4 to 8 months | 6 to 11 months | 7 to 12 months |
| Difficulty | Low | Medium | High |
| Biggest risk | Leaks and heat | The puff is too faint, or a spray is too messy | Lithium battery in a hot car |
| Price it needs | $29 works | Needs about $32 to $35 to pay for itself | Needs $35 or more |

### Build 1: Basic
**Parts list, per unit at 10,000:**
| Part | Cost |
|---|---|
| 3 molded parts in PP or POM (body, back, refill holder) | $0.24 to $0.60 |
| Vent clip | $0.10 to $0.30 |
| Face (wood veneer or fabric) | $0.15 to $0.50 (estimate) |
| Scent pad and 3 to 5 g of oil | $0.18 to $0.45 |
| NFC tag, NTAG213, 25 mm | $0.13 to $0.20 |
| Box | $0.10 to $0.50 |
| Assembly, 1 to 2 minutes | $0.07 to $0.21 |
| **Factory cost** | **$0.97 to $2.76** |
| Factory margin 15 to 25%, duty 31 to 43.5%, freight and brokerage | **$1.55 to $5.30 landed** |

A plain wooden vent diffuser sells for about $1.35 from Chinese factories, so the design and the refill program are what make this worth $29.

### Build 2: Press-to-puff
Two mechanisms, and the research disagrees on which to pick:

- **2A, air bellows.** Pressing the face squeezes a silicone dome that pushes air through the scent pad. No liquid moves. Patents on this idea expired decades ago (US 4,858,831 and others). The problem is strength: a 10 to 20 mL puff of scented air carries roughly 0.1 mg of fragrance, which our math puts right at the edge of what a nose can detect in a car. It may not be noticed.
- **2B, metered pump.** Pressing the face works a perfume-style pump that sprays 50 to 70 µL into the vent airflow. That's about the same as a Glade push-button spray, so it will be noticed. The problems are press force (10 to 45 N against a vent rated for about 5 N, so the design needs a brace foot or a lever), droplets landing on the dash or driver, and seals at 85°C.

**Added parts per unit:** bellows version $0.24 to $1.06; pump version $0.41 to $1.66 (pump $0.07 to $0.45, vial $0.10 to $0.30, extra oil, extra molded parts).

**Decision:** don't pick on paper. Build both as rough prototypes in Feasibility (G1) and test them in real cars. If the bellows puff is noticeable from the driver's seat, use it. It's simpler and has no liquid. If not, make the pump work with a brace and a downward nozzle, or fall back to Build 1.

### Build 3: Powered burst (lean version, no Bluetooth)
**Added parts per unit, about $2 to $2.50:** a very cheap microcontroller (PY32, $0.09), a battery (CR2450 coin cell $0.70, or a 200 mAh rechargeable cell $0.98 plus charger chip and USB-C port), a switch ($0.04), a tiny motor and fan ($0.55), a small circuit board and assembly (about $0.25), two more molded parts and assembly.

**The battery is the hard part.** Rechargeable lithium cells are rated to 60°C, and one maker's spec forbids leaving them in a car above that. Dashboards reach 69 to 89°C. Standard coin cells go to 85°C, and high-temperature ones (Panasonic CR2032A) to 125°C, but coin cells struggle to run a fan and bring Reese's Law rules (locked battery door, warnings, child-resistant packaging). A full version with Bluetooth and a mist atomizer costs $13 to $24 landed, which doesn't work under $39.

**Extra one-time costs:** electronics and firmware $10K to $40K, FCC Part 15B $1K to $5K, battery safety testing (UN 38.3 and IEC 62133) $0 if the cell maker supplies reports, about $13K or more for a custom pack. Adding Bluetooth later is another $23K to $81K.

## 3. The standard path from idea to production

This is the stage-gate process most hardware companies use. Each gate has to pass before money goes into the next stage.

| Gate | What it proves | Time | Cost (Build 1 / Build 2 / Build 3) |
|---|---|---|---|
| G0 Requirements | The table in section 1 is agreed; cost target set; patent and compliance review started | 2 to 4 weeks | $2-5K / $2-5K / $3-8K |
| G1 Feasibility | Scent strength in a real car; the puff or burst is noticeable; NFC reads through the face; press doesn't stress the vent | 2 to 6 weeks | $1-5K / $3-8K / $3-10K |
| G2 Design and prototypes | Looks-like and works-like models; fits 10+ vent types; people like how it looks | 4 to 10 weeks | $5-15K / $8-25K / $10-35K |
| G3 Design freeze | Production-ready CAD; factory signs off on manufacturability; quoted cost meets target | 3 to 8 weeks | $5-20K / $8-25K / $15-60K |
| G4 EVT (engineering validation) | 5 to 40 units built close to final; every function works | 2 to 8 weeks | optional / $2-8K / $5-30K |
| G5 Tooling | Molds cut; first parts measure to drawing | 6 to 12 weeks | $9-48K / $14-80K / $17-92K |
| G6 DVT (design validation) | 50 to 200 tooled units pass heat soak at 85°C, UV, vibration, drop, leak, press cycles, and all compliance | 4 to 8 weeks | $4-17K / $6-27K / $10-50K |
| G7 PVT (production validation) | The factory line holds quality; first article inspection; packaging drop test | 2 to 5 weeks | $1-3K / $1-3K / $2-5K |
| G8 Production | Ramp up; inspection on every shipment | ongoing | $250 to $450 per inspector-day |

## 4. Tests that decide the build (G1, about two weeks)

Run these before any design money is spent:

1. **Smell test.** In three different cars, with the fan on and off, five people rate the burst from the driver's seat: bellows puff, 50 µL pump, 70 µL pump, and a small fan over a pad. Pass: most people notice it within two seconds.
2. **Press force.** Measure how hard people press a phone onto the face, and the load on the vent slat with and without a brace foot. Pass: under about 5 N on the slat.
3. **Droplets.** Witness cards on the dash, screen and steering wheel during 100 pump presses. Pass: nothing lands outside the vent.
4. **Heat.** 85°C for 48 hours with each candidate refill and housing plastic. Pass: no leak, no swelling, no warping.
5. **NFC.** Ten phones, with and without cases, through each face material. Pass: reads on the first tap every time.

Estimated cost: $3K to $8K, mostly prototype parts and a few days of an engineer's time.

## 5. Compliance checklist

| Item | Build 1 | Build 2 | Build 3 | Cost |
|---|---|---|---|---|
| Safety data sheet per scent | Yes | Yes | Yes | $200 to $350 each |
| IFRA certificate (from fragrance supplier) | Yes | Yes | Yes | Supplier provides |
| California Prop 65 screen | Yes | Yes | Yes | $300 to $2K |
| Product liability insurance | Yes | Yes | Yes | About $500 to $1,200 a year |
| FCC Part 15B | No | No | Yes | $1K to $5K |
| Battery reports (UN 38.3, IEC 62133) | No | No | Yes | $0 to $15K |
| Reese's Law (coin cells) | No | No | If coin cell | $450 to $800 |
| RoHS and REACH | No | No | Yes | $300 to $1K |
| Patent review (see below) | Yes | Yes | Yes | Counsel |

**Patents to clear before launch, whichever build:** US 10,951,752 and US 11,601,545 cover a phone holder with a passive NFC tag that puts the phone into a driving mode. That touches the core Drive Mode feature. US 8,988,198 (Nokia) covers an NFC tag carrying scent settings. If we ever add Bluetooth, also check US 9,943,870 and 10,118,190. This needs a proper claims review by counsel.

## 6. Costs to watch

- **Tariffs.** Car air fresheners from China fall under HTS 3307.49: 6% base duty plus Section 301 tariffs, about 31 to 43.5% in total. Confirm with a customs broker before ordering.
- **Freight.** About $480 to $980 per cubic meter by ocean in November 2026, or a few cents a unit.
- **Pricing rule.** Keep landed cost at a quarter of retail or less.

## 7. Recommendation

1. **The 90-day test uses a stock freshener with an NFC sticker** from a US promotional supplier. No development money.
2. **If the test passes, spend $3K to $8K on the two-week feasibility tests** in section 4 before choosing a build.
3. **Choose based on the tests and on price:**
   - If a battery-free burst is noticeable and safe, make **Build 2** and price it around **$35**. That's where the burst pays for itself, and it puts us level with Pura Car.
   - If it isn't, make **Build 1** at $29 and deliver the reward digitally (streaks, refill credits) until a better mechanism exists.
   - Hold **Build 3** until there's proof drivers want a powered version and will pay for it.
4. **During the test, show "tap for a burst of fresh air" at $35 against the basic version at $29** on the thank-you page. That's the cheapest way to learn whether the burst is worth building.

## 8. What each build does to Path B

Same volumes as the plan, one change at a time (docs/plan/cash.py):

| Build | Price | Kit margin | Most cash out | Back to even | Profit 2027 to 2029 |
|---|---|---|---|---|---|
| 1. Basic | $29 | $13.96 | $418K | Oct 2029 | +$339K |
| 2. Press-to-puff | $29 | $12.26 | $543K | Jan 2030 | -$11K |
| 2. Press-to-puff | $35 | $18.08 | $359K | Apr 2029 | +$1.07M |
| 3. Powered, lean | $35 | $15.58 | $515K | Nov 2029 | +$535K |
| 3. Powered, lean | $29 | $9.76 | $881K | Jun 2030 | -$543K |

These assume the same number of buyers at each price, which won't be true. The price test tells us how many fewer people buy at $35.

## Sources
Key sources, all seen only as search summaries:
- Hot car temperatures: https://news.asu.edu/20180516-discoveries-asu-study-hot-cars-can-hit-deadly-temperatures-within-one-hour
- Leaking freshener class actions: https://carcomplaints.com/news/2023/febreze-car-air-freshener-leaking-class-action-lawsuit.shtml
- Bellows patent (expired): https://patents.google.com/patent/US4858831
- Driving-mode NFC patent: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10951752
- Perfume pump doses: https://aptar.com/products/beauty/vp4/
- Pura Car Pro: https://pura.com/pages/tech-specs
- Development costs: https://www.cadcrowd.com/blog/how-much-does-it-cost-to-develop-a-new-physical-product-a-complete-2026-breakdown/
- Stage gates: https://www.openbom.com/blog/evt-vs-dvt-vs-pvt-understanding-the-stages-of-product-development
- FCC costs: https://compliancetesting.com/fcc-certification-faqs/fcc-certification-cost/
- Coin cell ratings: https://energy.panasonic.com/dam/master/pdf/en/datasheet/lithium/CR2032A_Datasheet_EN_240701.pdf
- Tariff ruling: https://www.tarifflens.ai/rulings/N302250
- Ground shipping rule for combustible liquids: https://www.law.cornell.edu/cfr/text/49/173.150

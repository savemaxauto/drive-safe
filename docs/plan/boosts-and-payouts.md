# Boosts, upsells and how prizes reach drivers (Nov 17, 2026)

Numbers come from `rewards.py`. Search-based facts are marked; check them before external use.

## Boosts
**What a boost does:** 2x points on phone-free drives for a set time. It never touches Good Miles. Good Miles are the record insurers see, so they always count real miles. If miles could be bought, the record would be worthless to insurers and could mislead them.

| Boost | Price | We keep (after 15% store fee) | Worst-case points cost | Adds at a regular pace | Worth about |
|---|---|---|---|---|---|
| 2x for 7 days | $0.99 | $0.84 | $0.56 | 58 points | $0.71 |
| 2x for 30 days | $2.99 | $2.54 | $2.40 | 250 points | $3.03 |
| Four 7-day boosts (use within a year) | $2.99 | $2.54 | $2.24 | 233 points | $2.83 |

Rules:
- Every boost covers its own worst case. Worst case means 4 drives a day, every day, with every point spent on gas cards. Even then, what we keep after the store fee pays for the points.
- Before buying, the app shows an honest estimate at the driver's pace, for example "about 250 points, worth about $3 in prizes." Casual drivers see a small number and can skip it.
- Boosts double drive points only, not weekly goals or one-time bonuses. They don't stack.
- Boosted points can't become draw entries, so the draw stays free to enter. Draw entries come from weekly goals and a free way to enter.
- Boosts are digital, so they go through Apple's and Google's in-app purchase (15% under $1M a year, 30% above).
- There's always a free path: drivers earn plenty without buying anything.

What boosts are worth to us: small. If 8% of active drivers buy 2.5 boosts a year, that's about $374 a year per 1,000 active drivers. They're a nice extra, not the business.

## The better upsell: the refill club earns 2x
- Club members earn 2x points on every drive, always. An everyday member gets about 4,800 extra points a year. That costs us about $2.78 expected and $9.60 at worst, against about $41 a year of refill margin.
- It pushes the number that matters most. Each 5 points of refill-club take is worth about $2.45 per customer over three years, about $290K per year's buyers at 120,000 kits.
- Physical goods can use our own checkout, so there's no app store fee.

## Other ways to make money, in order
1. **Refill club with 2x points** (above).
2. **Seasonal scent drops.** Limited scents at $12 a refill instead of $8, sold to club members first.
3. **Wood face swaps.** $15 retail, about $4 landed. Also a top-shelf prize.
4. **A second freshener for another car.** $19. More drivers per household, and more chances for a renewal lead.
5. **New-driver gift kit.** $39 with three scents and a gift note on first tap. The buyer, usually a parent, is the lead, never the teen.
6. **Sponsored challenges.** A partner pays us to run a challenge such as "5 phone-free days, free wash at our stations." This adds to the partner revenue line in `paths.py`.
- Never: selling driving data, ads inside Drive Mode, or points for quotes.

## How prizes actually reach drivers
"10¢ off a gallon" needs a link to gas stations' payment systems, so it's out at launch. Every launch prize uses one of three channels that need no syncing with stations.

| Channel | Used for | How it works | Our cost |
|---|---|---|---|
| Partner codes | Car wash, oil change and auto parts prizes | The partner gives us single-use codes or a code API. We hand one out per redemption. The driver shows it at the counter or enters it online, and the partner reports redemptions each month. | $0. The partner pays the discount to win a customer. |
| Digital gift cards | $5 and $10 gas cards | A rewards API (Tremendous or Tango Card) sends a gas brand's e-gift card by email or in the app, usable at that brand's stations. | Face value. Search says no platform fee for gift cards; fund by bank transfer to avoid about 3% card funding fees. |
| Our own box | Free refill, scent sample, wood face | Added to the driver's next refill box through the store and subscription app. | Our cost of goods, no extra postage. |

### Later, at scale (25,000 to 50,000 active drivers): a Good Miles card
- **What it is:** a virtual prepaid card in Apple Wallet and Google Wallet, issued through a card platform such as Stripe Issuing, Lithic or Marqeta with a sponsor bank.
- **How it's limited:** spending controls hold it to gas, car wash and auto service merchant types. Points convert to dollars on the card at the same cost ceiling. It works at any gas station, with no station integration.
- **Cost:** search says Stripe lists about $0.10 per virtual card (verify US pricing).
- **What it needs:** card program approval, promotional card disclosures, unclaimed property rules and light identity checks.
- **Card-linked offers come with it.** Drivers link the card they already use, and partner-funded cash back triggers when they pay at a participating merchant. Fidel API is one platform; it tracks real-time transactions on linked cards. This is how "10¢ off a gallon" works, and partners fund it.

Recommendation: launch with codes, gift cards and box add-ons. Revisit the card at scale, when the partner list is long enough to fill it.

## Sources (search summaries)
- Stripe Issuing spending controls and per-card pricing: https://docs.stripe.com/issuing/controls/spending-controls , https://stripe.com/issuing
- Card-linked offers: https://docs.fidelapi.com/docs/select/offers/ , https://finledger.com/articles/google-pay-debuts-cash-back-rewards-enabled-by-fidel-api
- Gift card APIs: https://tangocard.com/pricing , https://www.capterra.com/p/197141/Tremendous-Rewards/pricing/

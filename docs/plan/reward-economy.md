# The prize counter: how points work (Nov 17, 2026)

Arcade logic with grown-up rules. Points come in steadily, every prize shows what it's worth, something is always in reach, and a cost ceiling means the counter can't eat the profit. Numbers come from `rewards.py`.

## The rules
1. Every prize shows what it's worth in dollars.
2. Something is always in reach. A driver who turns on Good Miles and takes a first drive has 250 points, enough for a $5 car wash on day one. Regular drivers reach a quick win every 3 weeks or so.
3. Bigger prizes are worth saving for. The biggest (a full tank, money toward tires) live in the monthly draw, which has a fixed budget.
4. Partner prizes stretch points furthest. Gas cards take the most points because they cost us cash.
5. Fair and stable. No price goes up without 30 days' notice. Points don't expire while you keep driving (12 months without a drive).
6. No tricks. Points can't be bought outright or cashed out. A boost only doubles points you earn by driving phone-free (see `boosts-and-payouts.md`). Points never come from asking for quotes or answering profile questions.

## How points come in
| For | Points |
|---|---|
| Phone-free drive with Drive Mode on (5+ min, 2+ miles, up to 4 a day) | 10 |
| Weekly goal: 5 phone-free days (also 1 draw entry) | 50 |
| Four weekly goals in a row | 100 |
| Each refill box | 100 |
| First drive (once) | 50 |
| Good Miles sensors (once): 25 each, plus 100 for all four | 200 |

## The counter
| Shelf | Prize | Points | Worth | Costs us | Delivered by | Weeks, regular driver |
|---|---|---|---|---|---|---|
| Quick wins | $5 off a car wash | 250 | $5 | $0 | partner code | 2.8 |
| Quick wins | New scent sample | 300 | $3 | $0.25 | next refill box | 3.3 |
| Quick wins | $5 off at an auto parts store | 300 | $5 | $0 | partner code | 3.3 |
| Worth saving for | Free car wash | 600 | ~$15 | $0 | partner code | 6.6 |
| Worth saving for | $20 off an oil change | 800 | $20 | $0 | partner code | 8.9 |
| Worth saving for | Free refill | 1,500 | $8 | $1.30 | next refill box | 16.6 |
| Worth saving for | $5 gas gift card | 2,500 | $5 | $5 | gift card API | 27.7 |
| Top shelf | Month of unlimited car washes | 2,500 | ~$34 | $0 | partner code | 27.7 |
| Top shelf | New wood face | 4,000 | $15 | $4 | next refill box | 44.3 |
| Top shelf | $10 gas gift card | 5,000 | $10 | $10 | gift card API | 55.3 |

Draw entries aren't sold for points. They come from weekly goals and a free way to enter, so paid boosts never touch the draw.

## What it costs
| Driver | Share | Points a year | Worth to them | Costs us | Worst case |
|---|---|---|---|---|---|
| Everyday (40 drives a month) | 25% | 8,800 | $85 | $5.10 | $17.60 |
| Regular (25 a month) | 45% | 4,700 | $46 | $2.73 | $9.40 |
| Casual (10 a month) | 30% | 1,500 | $15 | $0.87 | $3.00 |
| Blended | | 4,765 | $46 | $2.76 | $9.53 |

- Each 1,000 points used is worth about $12 to a driver and costs us about 72 cents, assuming 20% of points go unused and half of used points go to partner prizes, a quarter to our products and a quarter to gas cards.
- Worst case means every point spent on gas cards with none left unused. Even then the blended cost, $9.53, is under the $12 a year that `paths.py` budgets. Expected cost is about $9 a year less per opted-in active driver.
- Arcades aim to pay out 25 to 35% of what's played. An active driver brings in about $24 to $36 a year beyond the kit. Our expected cost is about 8 to 11% of that, and the worst case is about 26 to 39%, roughly an arcade's normal payout.
- Unused points: 20% assumed (Dutch Bros reported about 16% in 2021; Bond Brand Loyalty cites about 30%; above 40% usually means rewards aren't compelling).

## Guardrails
- Cost ceiling: no prize costs us more than $1 per 1,000 points for our own products, or $2 for gas cards. This is what caps the worst case.
- Partner prizes go on the counter only at the price their funding covers. If a partner leaves, the prize comes off or is repriced under the ceiling.
- One free refill per box, so free refills don't replace paid ones. One gas card a month.
- Physical prizes ship in the refill box to avoid separate postage.
- Drives count only at 5+ minutes and 2+ miles, up to 4 a day. Passenger rides never count.
- Draw prizes stay under $5,000 each (no bonding in New York and Florida) and always have a free way to enter. Check tax reporting for draw prizes with counsel.

## What has to be true
- Two or three partners: a car wash chain, an oil change chain and an auto parts retailer. Without them the counter is worth about $3 per 1,000 points instead of $12, and it stops feeling worth it. Signing them is part of the test.
- The prize mix is a guess. The test should record what drivers actually pick.
- Counsel: points for turning on sensors (a California financial incentive), sweepstakes rules, and state rules on rewards with no cash value.

## Sources (search summaries; check before external use)
- Arcade payout target 25 to 35%: https://betson.com/?p=43861 ; ticket value tied to real prize cost: https://www.replaymag.com/?p=19879
- Breakage: Dutch Bros 2022 annual report (about 16% of 2021 points expired); Bond Brand Loyalty via https://blog.brandmovers.com/what-is-point-breakage-and-why-should-you-care
- Retail prices and partner funding: `research-rewards.md`

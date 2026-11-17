# The prize counter: how points work (Nov 17, 2026)

Arcade logic with grown-up rules. Points come in steadily, every prize shows what it's worth, something is always in reach, and a cost ceiling means the counter can't eat the profit. Numbers come from `rewards.py`.

## The rules
1. Every prize shows what it's worth in dollars.
2. Something is always in reach. A driver who turns on Good Miles and takes a first drive has 250 points, enough for a $5 car wash on day one. Regular drivers reach a quick win every 1 to 3 weeks.
3. Bigger prizes are worth saving for. The biggest (a full tank, money toward tires) live in the monthly draw, which has a fixed budget.
4. Partner prizes stretch points furthest. Gas cards take the most points because they cost us cash.
5. Fair and stable. No price goes up without 30 days' notice. Points don't expire while you keep driving (12 months without a drive).
6. No tricks. Points can't be bought, have no cash value, and never come from asking for quotes or answering profile questions.

## How points come in
| For | Points |
|---|---|
| Phone-free drive with Drive Mode on (5+ min, 2+ miles, up to 4 a day) | 10 |
| Weekly goal: 5 phone-free days | 50 |
| Four weekly goals in a row | 100 |
| Each refill box | 100 |
| First drive (once) | 50 |
| Good Miles sensors (once): 25 each, plus 100 for all four | 200 |

## The counter
| Shelf | Prize | Points | Worth | Costs us | Who pays | Weeks, regular driver |
|---|---|---|---|---|---|---|
| Quick wins | Extra draw entry | 100 | a chance | $0 | fixed draw pool | 1.1 |
| Quick wins | 10¢ off a gallon for a week | 200 | ~$1.50 | $0 | gas partner | 2.2 |
| Quick wins | $5 off a car wash | 250 | $5 | $0 | car wash partner | 2.8 |
| Worth saving for | Free car wash | 600 | ~$15 | $0 | car wash partner | 6.6 |
| Worth saving for | $20 off an oil change | 800 | $20 | $0 | oil change partner | 8.9 |
| Worth saving for | Free refill in your next box | 1,500 | $8 | $1.30 | us, at cost | 16.6 |
| Worth saving for | $5 gas card | 2,500 | $5 | $5 | us, cash | 27.7 |
| Top shelf | Month of unlimited car washes | 2,500 | ~$34 | $0 | car wash partner | 27.7 |
| Top shelf | New wood face, ships in your box | 4,000 | $15 | $4 | us, at cost | 44.3 |
| Top shelf | $10 gas card | 5,000 | $10 | $10 | us, cash | 55.3 |

## What it costs
| Driver | Share | Points a year | Worth to them | Costs us | Worst case |
|---|---|---|---|---|---|
| Everyday (40 drives a month) | 25% | 8,800 | $70 | $5.09 | $17.60 |
| Regular (25 a month) | 45% | 4,700 | $37 | $2.72 | $9.40 |
| Casual (10 a month) | 30% | 1,500 | $12 | $0.87 | $3.00 |
| Blended | | 4,765 | $38 | $2.76 | $9.53 |

- Each 1,000 points used is worth about $10 to a driver and costs us about 72 cents, assuming 20% of points go unused and the mix of prizes below.
- Worst case means every point spent on gas cards with none left unused. Even then the blended cost, $9.53, is under the $12 a year that `paths.py` budgets. So the plan's rewards line is conservative: expected cost is about $9 a year less per opted-in active driver.
- Arcades aim to pay out 25 to 35% of what's played. An active driver brings in about $24 to $36 a year beyond the kit. Our expected cost is about 8 to 11% of that, and the worst case is about 26 to 39%, roughly an arcade's normal payout.
- Assumed mix of points used: partner prizes 45%, refills 20%, gas cards 25%, wood face 5%, draw entries 5%. Unused points: 20% (Dutch Bros reported about 16% in 2021; Bond Brand Loyalty cites about 30%; above 40% usually means rewards aren't compelling).

## Guardrails
- Cost ceiling: no prize costs us more than $1 per 1,000 points for our own products, or $2 for gas cards. This is what caps the worst case.
- Partner prizes go on the counter only at the price their funding covers. If a partner leaves, the prize comes off or is repriced under the ceiling.
- One free refill per box, so free refills don't replace paid ones. One gas card a month.
- Physical prizes ship in the refill box to avoid separate postage.
- Drives count only at 5+ minutes and 2+ miles, up to 4 a day. Passenger rides never count.
- Draw prizes stay under $5,000 each (no bonding in New York and Florida) and always have a free way to enter. Check tax reporting for draw prizes with counsel.

## What has to be true
- Two or three partners: a car wash chain, an oil change chain and a gas cash back app. Without them the counter is worth about $3 per 1,000 points instead of $10, and it stops feeling worth it. Signing them is part of the test.
- The prize mix is a guess. The test should record what drivers actually pick.
- Counsel: points for turning on sensors (a California financial incentive), sweepstakes rules, and state rules on rewards with no cash value.

## Sources (search summaries; check before external use)
- Arcade payout target 25 to 35%: https://betson.com/?p=43861 ; ticket value tied to real prize cost: https://www.replaymag.com/?p=19879
- Breakage: Dutch Bros 2022 annual report (about 16% of 2021 points expired); Bond Brand Loyalty via https://blog.brandmovers.com/what-is-point-breakage-and-why-should-you-care
- Retail prices and partner funding: `research-rewards.md`

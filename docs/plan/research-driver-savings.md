# What a safe driver could save (Nov 17, 2026)

Behind the savings projection in the app mockups. All figures came from search summaries; none of the source pages could be opened from this session, so check them before external use. "Vendor" marks a company's own claim.

## Premiums
- National average full coverage: $2,357 a year (NerdWallet, Nov 2026). Insurify: about $2,237 (June 2026). MoneyGeek: $2,575. ValuePenguin: about $2,496. https://www.nerdwallet.com/article/insurance/how-much-is-car-insurance
- The projection uses $2,300 a year, or $1,150 per 6-month policy.

## What telematics discounts pay
- Progressive says drivers who earn the Snapshot discount save about $322 to $328 a year (vendor). Older figures: $231 and $156. About 20% see their rate go up. https://www.progressive.com/answers/usage-based-car-insurance/
- Advertised maximums: State Farm Drive Safe & Save 30%, Nationwide SmartRide 40% (10% to sign up), Allstate Drivewise varies by state and can raise rates. https://www.valuepenguin.com/usage-based-auto-insurance-savings-privacy
- Realized discount across all enrollees is much lower: about 7% ($113 a year, J.D. Power 2023, via Policygenius) and about 10% (Consumer Federation of America, via Consumer Reports). https://www.policygenius.com/auto-insurance/news/drivers-opting-into-ubi/
- Maryland 2025 survey of 18 insurers: about 31% of enrolled policies went down, about 45% had no change. https://insurance.maryland.gov/Consumer/Appeals%20and%20Grievances%20Reports/Telematics-Survey-Report-2025.pdf
- Switching: Consumer Reports switchers saved a median $461 a year. Not counted in the projection.

## Can our score lower a price?
- Not on its own. Insurers price on scores they can file. Point-of-quote products exist: LexisNexis Telematics OnDemand (Root was first), Arity Drivesight and ArityIQ, and Arity with Experian letting shoppers share a driving report while quoting (vendor). https://risk.lexisnexis.com/about-us/press-room/press-release/20200724-telematics-ondemand
- Until a filed partner carries our score, the honest path is matching safe drivers to insurers with their own programs.

## What phone telematics collects
- Accelerometer and gyroscope for braking, acceleration, turns and phone motion; GPS for speed and miles; screen state for phone handling; motion and activity for trip detection. Most insurer apps ask for location all the time. CMT and the City of Boston's Safest Driver policy describe this. https://www.boston.gov/node/8921
- Feedback changes behavior: hard braking down about 15% (CMT, vendor); AAA Foundation found up to 13% less speeding and 21% less hard braking.

## Projection used in the mockups
Assumes a driver who keeps a safe score, 6-month policies, 40 phone-free drives a month, and an insurer that prices on the score. Renewal discounts step 10%, 12%, 14%, then 15%.

| With the app | 1 mo | 3 mo | 6 mo | 1 yr | 2 yr | 3 yr |
|---|---|---|---|---|---|---|
| Rate lower by, a year | $0 | $0 | $230 | $276 | $345 | $345 |
| Saved on insurance so far | $0 | $0 | $0 | $115 | $414 | $759 |
| Free refills (1,500 points each) | 0 | 0 | 1 | 3 | 6 | 9 |
| Deals and cash back | $3 | $8 | $15 | $30 | $60 | $90 |
| Back so far | $3 | $8 | $23 | $169 | $522 | $921 |

Refills cost us about $1.30 each plus postage. At about 3 a year that stays near the $12 a year self-funded reward cost in `paths.py`.

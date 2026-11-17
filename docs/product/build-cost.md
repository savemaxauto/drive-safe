# What the app and backend cost to build and run (Nov 17, 2026)

Bottom-up hours by feature, from `docs/plan/build_cost.py`. Rates are blended team rates: about $75 an hour for a nearshore agency (Latin America) and $175 for a US agency. Search shows nearshore React Native rates around $40 to $86 an hour and US agency rates from $80 to over $200, so these are middle-of-range picks. QA adds 25% of build hours and project management 15%.

## The build
| | Phase 1: launch on iPhone | Phase 2: Android and growth | Both |
|---|---|---|---|
| App (React Native with native iPhone and Android parts) | 1,170 h | 570 h | 1,740 h |
| Backend | 940 h | 290 h | 1,230 h |
| Admin console | 320 h | 110 h | 430 h |
| Design | 220 h | 80 h | 300 h |
| QA and project management | 1,005 h | 400 h | 1,405 h |
| **Total** | **3,655 h** | **1,450 h** | **5,105 h** |
| Nearshore agency | **$274K** | **$109K** | **$383K** |
| US agency | $640K | $254K | $893K |
| Time with about 5 people | about 5 months | about 2 months | |

### Phase 1 (launch on iPhone)
- App: account (text code, Apple and Google), pairing and tap to start, Drive Mode with Apple's Screen Time tools, trips and Good Miles in the background, Home, Good Miles, Trips, Savings, prize counter and prize wallet, renewal and quotes, profile and settings, scent and refill box, notifications.
- Backend: drivers and profiles, consent records per insurer, the Good Miles engine with anti-gaming rules, a points ledger and rules engine, the prize catalog with partner codes and a gift card API, lead handoff to our existing lead platform, store hookup, privacy tools (export, delete, retention), cloud and monitoring.
- Admin console, for developers, admins, managers and support, each with their own access:
  - driver lookup and point adjustments, with a reason and an audit log
  - prize catalog, prices, partner codes and stock
  - earn rules, cost ceilings and feature switches
  - a dashboard of active drivers, Good Miles, rewards cost against budget, and the lead funnel

### Phase 2 (Android and growth)
- Android version: pairing, Drive Mode, trips, calls.
- Boosts with in-app purchase, the live drive on the lock screen, gift mode.
- A draw engine with free entry and an audited winner pick.
- Delivering Good Miles to insurers through a filed scoring partner.
- Admin: campaigns, boosts and draws, partner reports.

## Running it each year
| Item | Per year |
|---|---|
| Cloud hosting and database | $24K |
| Sign-in text codes | $5K |
| Analytics, crash reporting, push | $10K |
| Maintenance and small features (about 20% of build) | $75K |
| Security testing | $15K |
| SOC 2 report (insurers will ask before taking data) | $45K |
| **Total** | **$174K** |

If the in-house engineer the plan already pays for from 2028 does maintenance, the extra running cost is about $99K a year. That's close to the plan's $85K to $100K for upkeep and compliance.

## What it does to Path B
| Case | Peak cash | Back to even | 3-year profit |
|---|---|---|---|
| Plan as it stands ($150K app) | $460K | Nov 2029 | $249K |
| Real build, in-house engineer maintains | $702K | Jan 2030 | $2K |
| Same, with rewards at the prize counter's expected cost | $680K | Dec 2029 | $206K |
| Real build, agency maintains, rewards at expected cost | $729K | Jan 2030 | $57K |

**The plan's $150K app line is about half of what this feature set costs, even nearshore.** The honest fix:
- Budget about $275K for the iPhone launch and about $110K for Android the next year.
- Use the in-house engineer for upkeep.
- Use the prize counter's lower reward cost ($4 a year instead of $12).
- With all three, peak cash rises by about $220K, payback moves about a month, and 3-year profit stays close to plan.

## Ways to spend less
- Ship iPhone only until the app proves people keep using it. About 57% of US phones are iPhones, but Android buyers would wait for Drive Mode.
- Outsource the draw to a sweepstakes administrator instead of building it (saves about 60 hours).
- Put off the SOC 2 report until the first insurer asks for it.
- Send quotes through our existing lead form in a web view at first (saves about 150 hours).

## Schedule risks
- Apple must approve the Screen Time (Family Controls) entitlement before Drive Mode can ship. Apply in month one.
- Background location "always" gets close App Store review. The app has to explain it clearly, which the opt-in screen does.
- On Android, app blocking usually relies on the accessibility service, which Google Play reviews closely and requires disclosing.

## Sources (search summaries)
- Developer rates: https://www.revelo.com/blog/how-to-hire-react-native-developers-nearshore-in-2026 , https://www.secondtalent.com/cost-to-hire/react-native-developer/ , https://lemon.io/rate-calculator/react-native/

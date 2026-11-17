"""Save Max Lives: what the app, backend and admin console cost to build and run.

Bottom-up hours by feature, priced at nearshore and US agency rates, then run
through cash.py to show what a realistic app budget does to Path B.

Run: python3 build_cost.py
"""
import copy
import cash as C
import paths as P

RATES = {'Nearshore agency': 75, 'US agency': 175}   # $/hour, blended team rate
QA, PM = 0.25, 0.15                                  # share of build hours

# (phase, area, item, hours). Phase 1 = launch on iPhone. Phase 2 = Android and growth.
ITEMS = [
    (1, 'App', 'Shell, navigation, design system', 80),
    (1, 'App', 'Account: text code, Apple and Google sign-in', 60),
    (1, 'App', 'Freshener pairing and tap to start (iPhone)', 50),
    (1, 'App', 'Drive Mode on iPhone: Screen Time pause, shield screen, end anytime', 180),
    (1, 'App', 'Trips and Good Miles on iPhone: background location and motion, phone handling, hidden trip ends', 240),
    (1, 'App', 'Home, Good Miles, Trips and Savings screens with charts', 120),
    (1, 'App', 'Prize counter, goals, redemptions, prize wallet', 110),
    (1, 'App', 'Renewal check-in, consent, quotes', 90),
    (1, 'App', 'Profile, one question at a time, settings, privacy, delete account', 80),
    (1, 'App', 'Scent and refill box (store checkout inside the app)', 50),
    (1, 'App', 'Notifications, analytics, crash reporting', 40),
    (1, 'App', 'Accessibility, polish, App Store review', 70),
    (1, 'Backend', 'API, sign-in, drivers and profiles', 100),
    (1, 'Backend', 'Consent records per insurer, timestamped and exportable', 50),
    (1, 'Backend', 'Trip intake, Good Miles engine, anti-gaming rules', 180),
    (1, 'Backend', 'Points ledger and rules engine: earn rules, caps, expiry', 150),
    (1, 'Backend', 'Prize catalog, partner codes, gift card API, box add-ons', 120),
    (1, 'Backend', 'Lead and quote handoff to our lead platform', 100),
    (1, 'Backend', 'Store and refill subscription hookup', 50),
    (1, 'Backend', 'Notification service', 30),
    (1, 'Backend', 'Privacy: export, delete, retention, encryption', 70),
    (1, 'Backend', 'Cloud setup, deploys, monitoring, test environment', 90),
    (1, 'Admin', 'Roles (developer, admin, manager, support) and audit log', 50),
    (1, 'Admin', 'Driver lookup, trips, point adjustments with reasons', 80),
    (1, 'Admin', 'Prize catalog, partner codes, stock limits, prices', 70),
    (1, 'Admin', 'Rules and switches: earn rates, cost ceilings, feature flags', 40),
    (1, 'Admin', 'Dashboard: active drivers, Good Miles, rewards cost vs budget, lead funnel', 80),
    (1, 'Design', 'UX and visual design for app and admin', 220),
    (2, 'App', 'Android: pairing, Drive Mode, trips, calls', 420),
    (2, 'App', 'Boosts with in-app purchase (Apple and Google)', 60),
    (2, 'App', 'Lock screen live drive (iPhone) and ongoing notification (Android)', 50),
    (2, 'App', 'Gift mode for new drivers', 40),
    (2, 'Backend', 'Boost receipts and multiplier rules', 50),
    (2, 'Backend', 'Draw engine: entries, free entry, audited winner pick', 60),
    (2, 'Backend', 'Good Miles delivery to insurers through a filed scoring partner', 120),
    (2, 'Backend', 'Android support and scaling', 60),
    (2, 'Admin', 'Push campaigns and content', 40),
    (2, 'Admin', 'Boost and draw admin', 40),
    (2, 'Admin', 'Partner reporting', 30),
    (2, 'Design', 'Android and new features', 80),
]

# Yearly running costs once live (estimates; check vendor pricing).
RUN = [
    ('Cloud hosting and database', 24000),
    ('Sign-in text codes', 5000),
    ('Analytics, crash reporting, push', 10000),
    ('Maintenance and small features (about 20% of build)', 75000),
    ('Security testing', 15000),
    ('SOC 2 report insurers will ask for (tool and auditor)', 45000),
]


def phase_hours(ph):
    rows = [i for i in ITEMS if i[0] == ph]
    build = sum(h for _, a, _, h in rows if a != 'Design')
    design = sum(h for _, a, _, h in rows if a == 'Design')
    by_area = {}
    for _, a, _, h in rows:
        by_area[a] = by_area.get(a, 0) + h
    qa = build * QA
    pm = (build + design) * PM
    return dict(build=build, design=design, qa=qa, pm=pm, total=build + design + qa + pm, by_area=by_area)


def spread_add(f, amount, y, m0, m1):
    months = [k for k in C.MONTHS if k[0] == y and m0 <= k[1] <= m1]
    for k in months:
        f[k] += amount / len(months)


def main():
    totals = {}
    for ph in (1, 2):
        h = phase_hours(ph)
        totals[ph] = h
        areas = ', '.join(f'{a} {v:,}' for a, v in h['by_area'].items())
        print(f'Phase {ph}: {h["total"]:,.0f} hours ({areas}, QA {h["qa"]:,.0f}, PM {h["pm"]:,.0f})')
        for name, r in RATES.items():
            print(f'   {name:17} ${h["total"] * r / 1e3:,.0f}K')
    all_h = totals[1]['total'] + totals[2]['total']
    print(f'Both phases: {all_h:,.0f} hours')
    for name, r in RATES.items():
        print(f'   {name:17} ${all_h * r / 1e3:,.0f}K')
    team_hours = 5 * 140
    print(f'At 5 people (~{team_hours} hours a month): phase 1 about {totals[1]["total"] / team_hours:.1f} months, '
          f'phase 2 about {totals[2]["total"] / team_hours:.1f} months')

    run_total = sum(v for _, v in RUN)
    print(f'\nRunning costs a year: ${run_total / 1e3:,.0f}K')
    for n, v in RUN:
        print(f'   {n:58} ${v / 1e3:,.0f}K')

    # What a realistic budget does to Path B (nearshore build).
    rate = RATES['Nearshore agency']
    p1, p2 = totals[1]['total'] * rate, totals[2]['total'] * rate
    plan_app, plan_upkeep, plan_comp = 150000, {2028: 60000, 2029: 75000}, 25000
    base = C.simulate(P.B, C.kits_b(), C.fixed_b(), 'B')
    f = C.fixed_b()
    spread_add(f, p1 - plan_app, 2027, 4, 9)
    spread_add(f, p2, 2028, 1, 6)
    for y in (2028, 2029, 2030):
        extra_run = run_total - plan_upkeep.get(min(y, 2029)) - plan_comp
        spread_add(f, max(0, extra_run), y, 1, 12)
    allagency = C.simulate(P.B, C.kits_b(), f, 'B')
    # The plan's team line already pays an in-house engineer from 2028, who takes over maintenance.
    g = C.fixed_b()
    spread_add(g, p1 - plan_app, 2027, 4, 9)
    spread_add(g, p2, 2028, 1, 6)
    maint = dict(RUN)['Maintenance and small features (about 20% of build)']
    for y in (2028, 2029, 2030):
        extra_run = run_total - maint - plan_upkeep.get(min(y, 2029)) - plan_comp
        spread_add(g, max(0, extra_run), y, 1, 12)
    inhouse = C.simulate(P.B, C.kits_b(), g, 'B')
    b2 = copy.deepcopy(P.B)
    b2['reward_cost'] = 4.0     # rewards.py expected cost is ~$2.76; $4 leaves room for the club 2x perk
    inhouse_r = C.simulate(b2, C.kits_b(), g, 'B')
    allagency_r = C.simulate(b2, C.kits_b(), f, 'B')

    def line(nm, r):
        prof = sum(v for y, v in r['by_year'].items() if y < 2030)
        print(f'   {nm:52} peak cash ${r["peak"] / 1e3:,.0f}K, back to even {r["back_at"]}, 3-yr profit ${prof / 1e3:,.0f}K')
    print(f'\nPath B with a nearshore build (phase 1 ${p1 / 1e3:,.0f}K in 2027, phase 2 ${p2 / 1e3:,.0f}K in 2028)')
    line('Plan as it stands ($150K app)', base)
    line('Real build, in-house engineer maintains', inhouse)
    line('Real build, in-house maintains, rewards at expected', inhouse_r)
    line('Real build, agency maintains', allagency)
    line('Real build, agency maintains, rewards at expected', allagency_r)


if __name__ == '__main__':
    main()

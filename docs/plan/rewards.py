"""Save Max Lives: the point economy (the prize counter) and boosts.

Arcade logic with grown-up rules: points come in steadily, every prize shows what
it's worth, something is always in reach, and no prize can cost us more than a
set amount per 1,000 points. That ceiling keeps rewards inside the $12 a year
per opted-in active driver that paths.py budgets.

Boosts double points (never Good Miles) for a set time. Each boost is priced so
that, after the app store's cut, it covers the worst-case cost of the points it
can create.

Run: python3 rewards.py
"""

# How points come in. Never for asking for quotes or answering profile questions.
EARN = dict(
    per_drive=10,          # phone-free drive with Drive Mode on, 5+ min and 2+ miles, up to 4 a day
    weekly_goal=50,        # 5 phone-free days in a week (also 1 draw entry)
    streak=100,            # 4 weekly goals in a row
    refill_box=100,        # each refill box shipped
    first_drive=50,        # one time
    sensors=200,           # one time: 25 each for 4 Good Miles sensors + 100 for all four
)
MAX_DRIVES_A_DAY = 4

# Three driver paces (per month, except boxes per year) and their share of active drivers.
PACES = {
    'Everyday': dict(drives=40, goals=4, streaks=1.0, boxes=4, share=0.25),
    'Regular':  dict(drives=25, goals=2, streaks=0.25, boxes=2, share=0.45),
    'Casual':   dict(drives=10, goals=0.5, streaks=0.0, boxes=0, share=0.30),
}

# The prize counter: (shelf, prize, points, worth to driver $, our cash cost $, kind)
# kind: partner = partner funds it (codes), ours = our product at cost, cash = digital gift card at face value.
# Draw entries are not sold for points: they come from weekly goals and a free way to enter.
PRIZES = [
    ('Quick wins', '$5 off a car wash', 250, 5.00, 0.00, 'partner'),
    ('Quick wins', 'New scent sample, in your next box', 300, 3.00, 0.25, 'ours'),
    ('Quick wins', '$5 off at an auto parts store', 300, 5.00, 0.00, 'partner'),
    ('Worth saving for', 'Free car wash', 600, 15.00, 0.00, 'partner'),
    ('Worth saving for', '$20 off an oil change', 800, 20.00, 0.00, 'partner'),
    ('Worth saving for', 'Free refill in your next box', 1500, 8.00, 1.30, 'ours'),
    ('Worth saving for', '$5 gas gift card', 2500, 5.00, 5.00, 'cash'),
    ('Top shelf', 'Month of unlimited car washes', 2500, 34.00, 0.00, 'partner'),
    ('Top shelf', 'New wood face, in your next box', 4000, 15.00, 4.00, 'ours'),
    ('Top shelf', '$10 gas gift card', 5000, 10.00, 10.00, 'cash'),
]

CEILING = {'ours': 1.00, 'cash': 2.00}   # our cash cost per 1,000 points
BREAKAGE = 0.20     # points never used. Dutch Bros reported ~16% (2021); Bond cites ~30%.
MIX = {'partner': 0.50, 'ours': 0.25, 'cash': 0.25}   # share of used points (a guess until the test)
BUDGET = 12.00      # paths.py reward_cost: $ a year per opted-in active driver

# Boosts: 2x points on phone-free drives only. (name, price $, days covered)
BOOSTS = [('2x points for 7 days', 0.99, 7), ('2x points for 30 days', 2.99, 30), ('Four 7-day boosts', 2.99, 28)]
STORE_FEE = 0.15    # Apple and Google small-business rate (30% above $1M a year)
BOOST_BUYERS = 0.08     # share of active drivers who buy any boost in a year (assumption)
BOOSTS_PER_BUYER = 2.5  # purchases a year per buyer (assumption)


def per_1000(points, dollars):
    return dollars / points * 1000


def earn_per_year(p):
    e = EARN
    return (p['drives'] * e['per_drive'] + p['goals'] * e['weekly_goal'] + p['streaks'] * e['streak']) * 12 \
        + p['boxes'] * e['refill_box']


def mix_rates():
    """Average cost and worth per 1,000 used points, weighted by MIX."""
    cost = worth = 0.0
    for k, share in MIX.items():
        rows = [p for p in PRIZES if p[5] == k]
        cost += share * sum(per_1000(p[2], p[4]) for p in rows) / len(rows)
        worth += share * sum(per_1000(p[2], p[3]) for p in rows) / len(rows)
    return cost, worth


def main():
    print('Prize counter (cost and worth per 1,000 points)')
    for shelf, name, pts, worth, cost, k in PRIZES:
        c = per_1000(pts, cost)
        cap = CEILING.get(k)
        flag = '' if cap is None or c <= cap + 1e-9 else '  OVER CEILING'
        print(f'  {shelf:17} {name:36} {pts:6,} pts  worth ${worth:5.2f}  costs us ${cost:5.2f}  (${c:4.2f}/1k){flag}')

    c1k, w1k = mix_rates()
    worst_1k = max(CEILING.values())
    print(f'\nExpected mix: worth ${w1k:.2f} and costs us ${c1k:.2f} per 1,000 used points')

    print('\nPer active driver, per year')
    blend = dict(earn=0.0, worth=0.0, cost=0.0, worst=0.0)
    for name, p in PACES.items():
        earn = earn_per_year(p)
        used = earn * (1 - BREAKAGE)
        worth, cost, worst = used * w1k / 1000, used * c1k / 1000, earn * worst_1k / 1000
        for k, v in (('earn', earn), ('worth', worth), ('cost', cost), ('worst', worst)):
            blend[k] += p['share'] * v
        print(f'  {name:9} earns {earn:6,.0f} ({earn / 52:4.0f} a week)  worth ${worth:5.2f}  costs us ${cost:5.2f}  worst ${worst:5.2f}')
    print(f'  {"Blended":9} earns {blend["earn"]:6,.0f}                worth ${blend["worth"]:5.2f}  costs us ${blend["cost"]:5.2f}  '
          f'worst ${blend["worst"]:5.2f}  (budget ${BUDGET:.2f})')

    print('\nWeeks to earn each prize')
    for shelf, name, pts, *_ in PRIZES:
        w = [pts / (earn_per_year(p) / 52) for p in PACES.values()]
        print(f'  {name:36} ' + '  '.join(f'{n} {x:4.1f}' for n, x in zip(PACES, w)))

    print('\nBoosts (2x points on phone-free drives, never Good Miles)')
    avg_net, avg_cost = 0.0, 0.0
    for name, price, days in BOOSTS:
        net = price * (1 - STORE_FEE)
        worst = MAX_DRIVES_A_DAY * EARN['per_drive'] * days * worst_1k / 1000
        ok = 'covers worst case' if net >= worst - 1e-9 else 'DOES NOT cover worst case'
        print(f'  {name:22} ${price:.2f}  we keep ${net:.2f}  worst-case points cost ${worst:.2f}  ({ok})')
        for pn, p in PACES.items():
            extra = p['drives'] * EARN['per_drive'] * days / 30
            print(f'      {pn:9} adds about {extra:4.0f} points, worth about ${extra * w1k / 1000:4.2f}, '
                  f'expected cost to us ${extra * (1 - BREAKAGE) * c1k / 1000:4.2f}')
        avg_net += net / len(BOOSTS)
        reg = PACES['Regular']['drives'] * EARN['per_drive'] * days / 30
        avg_cost += reg * (1 - BREAKAGE) * c1k / 1000 / len(BOOSTS)
    per_1000_drivers = 1000 * BOOST_BUYERS * BOOSTS_PER_BUYER * (avg_net - avg_cost)
    print(f'  If {BOOST_BUYERS:.0%} of active drivers buy {BOOSTS_PER_BUYER} boosts a year: about '
          f'${per_1000_drivers:,.0f} a year per 1,000 active drivers')

    club = PACES['Everyday']['drives'] * EARN['per_drive'] * 12
    print(f'\nRefill club perk (2x on every drive): an everyday member gets about {club:,} extra points a year, '
          f'expected cost ${club * (1 - BREAKAGE) * c1k / 1000:.2f}, worst ${club * worst_1k / 1000:.2f}, '
          f'against about ${4 * 10.35:.0f} a year of refill margin')

    print(f'\nNew drivers start with {EARN["first_drive"] + EARN["sensors"]} points after the first drive '
          f'with all sensors on: enough for a quick win on day one.')


if __name__ == '__main__':
    main()

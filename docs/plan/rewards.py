"""Save Max Lives: the point economy (the prize counter).

Arcade logic with grown-up rules: points come in steadily, every prize shows what
it's worth, something is always in reach, and no prize can cost us more than a
set amount per 1,000 points. That ceiling is what keeps rewards inside the
$12 a year per opted-in active driver that paths.py budgets.

Run: python3 rewards.py
"""

# How points come in. Never for asking for quotes or answering profile questions.
EARN = dict(
    per_drive=10,          # phone-free drive with Drive Mode on, 5+ min and 2+ miles, up to 4 a day
    weekly_goal=50,        # 5 phone-free days in a week
    streak=100,            # 4 weekly goals in a row
    refill_box=100,        # each refill box shipped
    first_drive=50,        # one time
    sensors=200,           # one time: 25 each for 4 Good Miles sensors + 100 for all four
)

# Three driver paces (per month, except boxes per year) and their share of active drivers.
PACES = {
    'Everyday': dict(drives=40, goals=4, streaks=1.0, boxes=4, share=0.25),
    'Regular':  dict(drives=25, goals=2, streaks=0.25, boxes=2, share=0.45),
    'Casual':   dict(drives=10, goals=0.5, streaks=0.0, boxes=0, share=0.30),
}

# The prize counter: (shelf, prize, points, worth to driver $, our cash cost $, who pays)
PRIZES = [
    ('Quick wins', 'Extra draw entry', 100, 0.00, 0.00, 'draw pool (fixed)'),
    ('Quick wins', '10c off a gallon for a week', 200, 1.50, 0.00, 'gas partner'),
    ('Quick wins', '$5 off a car wash', 250, 5.00, 0.00, 'car wash partner'),
    ('Worth saving for', 'Free car wash', 600, 15.00, 0.00, 'car wash partner'),
    ('Worth saving for', '$20 off an oil change', 800, 20.00, 0.00, 'oil change partner'),
    ('Worth saving for', 'Free refill in your next box', 1500, 8.00, 1.30, 'us, at cost'),
    ('Worth saving for', '$5 gas card', 2500, 5.00, 5.00, 'us, cash'),
    ('Top shelf', 'Month of unlimited car washes', 2500, 34.00, 0.00, 'car wash partner'),
    ('Top shelf', 'New wood face, ships in your box', 4000, 15.00, 4.00, 'us, at cost'),
    ('Top shelf', '$10 gas card', 5000, 10.00, 10.00, 'us, cash'),
]

# Ceilings: our cash cost per 1,000 points. Own products <= $1, gas cards <= $2.
CEILING = {'us, at cost': 1.00, 'us, cash': 2.00}

BREAKAGE = 0.20     # points never used. Dutch Bros reported ~16% (2021); Bond cites ~30%.
# Share of redeemed points by kind (assumption until the test shows real choices).
MIX = {'partner': 0.45, 'refill': 0.20, 'gas': 0.25, 'face': 0.05, 'draw': 0.05}
BUDGET = 12.00      # paths.py reward_cost: $ a year per opted-in active driver


def per_1000(points, dollars):
    return dollars / points * 1000


def earn_per_year(p):
    e = EARN
    return (p['drives'] * e['per_drive'] + p['goals'] * e['weekly_goal'] + p['streaks'] * e['streak']) * 12 \
        + p['boxes'] * e['refill_box']


def kind(name, who):
    if 'partner' in who:
        return 'partner'
    if 'draw' in who:
        return 'draw'
    if 'refill' in name:
        return 'refill'
    if 'gas card' in name:
        return 'gas'
    return 'face'


def mix_rates():
    """Average cost and worth per 1,000 redeemed points for each kind of prize."""
    cost, worth = {}, {}
    for k in MIX:
        rows = [p for p in PRIZES if kind(p[1], p[5]) == k]
        cost[k] = sum(per_1000(p[2], p[4]) for p in rows) / len(rows)
        worth[k] = sum(per_1000(p[2], p[3]) for p in rows) / len(rows)
    c = sum(MIX[k] * cost[k] for k in MIX)
    w = sum(MIX[k] * worth[k] for k in MIX)
    return c, w


def main():
    print('Prize counter (cost and worth per 1,000 points)')
    for shelf, name, pts, worth, cost, who in PRIZES:
        c = per_1000(pts, cost)
        cap = CEILING.get(who)
        flag = '' if cap is None or c <= cap + 1e-9 else '  OVER CEILING'
        print(f'  {shelf:17} {name:34} {pts:6,} pts  worth ${worth:5.2f}  costs us ${cost:5.2f}  '
              f'(${c:4.2f}/1k){flag}')

    c1k, w1k = mix_rates()
    worst_1k = max(CEILING.values())
    print(f'\nExpected mix: worth ${w1k:.2f} and costs us ${c1k:.2f} per 1,000 redeemed points')

    print('\nPer active driver, per year')
    blend = dict(earn=0.0, worth=0.0, cost=0.0, worst=0.0)
    for name, p in PACES.items():
        earn = earn_per_year(p)
        used = earn * (1 - BREAKAGE)
        worth, cost, worst = used * w1k / 1000, used * c1k / 1000, earn * worst_1k / 1000
        for k, v in (('earn', earn), ('worth', worth), ('cost', cost), ('worst', worst)):
            blend[k] += p['share'] * v
        weekly = earn / 52
        print(f'  {name:9} earns {earn:6,.0f}  ({weekly:4.0f} a week)  worth ${worth:5.2f}  '
              f'costs us ${cost:5.2f}  worst case ${worst:5.2f}')
    print(f'  {"Blended":9} earns {blend["earn"]:6,.0f}                 worth ${blend["worth"]:5.2f}  '
          f'costs us ${blend["cost"]:5.2f}  worst case ${blend["worst"]:5.2f}  (budget ${BUDGET:.2f})')

    print('\nWeeks to earn each prize')
    for shelf, name, pts, *_ in PRIZES:
        w = [pts / (earn_per_year(p) / 52) for p in PACES.values()]
        print(f'  {name:34} ' + '  '.join(f'{n} {x:4.1f}' for n, x in zip(PACES, w)))

    print(f'\nNew drivers start with {EARN["first_drive"] + EARN["sensors"]} points after the first drive '
          f'with all sensors on: enough for a quick win on day one.')


if __name__ == '__main__':
    main()

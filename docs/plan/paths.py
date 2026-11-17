"""Save Max Lives: the two paths in the business plan, from one set of assumptions.

Path A, Test first: a stock freshener + NFC sticker sold on our own quote pages.
          No app, no custom design. Grows only on our own traffic.
Path B, Launch with rewards: Path A's test in Q1 2027, then (if it passes) our own
          press-to-puff design, the app with a rewards wallet, partner-funded
          rewards and paid growth.

Run: python3 paths.py
Per-customer values and the yearly view live here. The deck's profit, cash and payback
figures come from cash.py, which runs these same values month by month.
"""
import copy

BASE = dict(
    kit_price=29.00,
    kit_landed=3.75,        # stock diffuser $1.00-2.15, NFC $0.16-0.35, box $0.22-0.40, refill, freight/tariff
    fulfill=5.00,           # 3PL all-in $4.50-7.40 an order
    postage=5.50,
    pay_pct=0.029, pay_fix=0.30,
    refill_take=0.30, refill_price=24.00, refill_cogs=3.90, refill_ship=8.75,   # 3 refills for $24 ($8 each; Drift $11.99, Pura $14.99); finished refill ~$1.30 each
    first_keep=0.73, quarter_keep=0.83,   # 26-28% churn at first renewal; ~6%/mo after
    optin=0.35,             # kit customers who opt in to insurance quotes (TEST #1)
    shop=0.50,              # opted-in customers who shop through us in a year
    reach=0.75,             # share still reachable each later year
    epl=26.47,
    # app / rewards (Path B only)
    app=False,
    active=(0.0, 0.0, 0.0),       # share of kit customers active in the app, by customer-year
    scored=0.0,             # share of opted-in, app-active customers with a safe-driver score
    premium=1.75,           # safe-driver lead price vs EPL
    reward_cost=0.0,        # what WE pay per active driver per year (refills at cost, gift cards)
    partner_rev=(0.0, 0.0, 0.0),  # what partners pay US per active driver, by customer-year
)

def kit_margin(a):
    p = a['kit_price']
    return p - a['kit_landed'] - a['fulfill'] - a['postage'] - (p * a['pay_pct'] + a['pay_fix'])

def refill_margin(a):
    p = a['refill_price']
    return p - a['refill_cogs'] - a['refill_ship'] - (p * a['pay_pct'] + a['pay_fix'])

def refill_ships(a, years=4):
    s = [1.0]
    for i in range(1, 4 * years):
        s.append(s[-1] * (a['first_keep'] if i == 1 else a['quarter_keep']))
    return [sum(s[4 * y:4 * y + 4]) for y in range(years)]

def per_customer(a, t):
    """Value per kit customer in their customer-year t (0 = the year they buy). Excludes the kit."""
    ships = refill_ships(a)
    refill = a['refill_take'] * ships[t] * refill_margin(a)
    leads = a['optin'] * a['shop'] * a['reach'] ** t
    lead = leads * a['epl']
    act = a['active'][t] if a['app'] else 0.0
    prem = leads * a['scored'] * (a['premium'] - 1) * a['epl'] if a['app'] else 0.0
    # Rewards that cost us money go only to drivers who opt in to share (partner-funded offers go to everyone).
    rewards = -act * a['optin'] * a['reward_cost']
    partner = act * a['partner_rev'][t]
    return dict(refill=refill, lead=lead, premium=prem, partner=partner, rewards=rewards)

def three_year_value(a):
    v = kit_margin(a)
    for t in range(3):
        v += sum(per_customer(a, t).values())
    return v

def run(a, kits, cac, fixed):
    """Calendar-year P&L. Customers buy evenly through the year, so their year-t value
    lands half in calendar year c+t and half in c+t+1."""
    years = sorted(kits); out = {}
    for y in years:
        line = dict(kit=0.0, refill=0.0, lead=0.0, premium=0.0, partner=0.0, rewards=0.0)
        rev = dict(kit=0.0, refill=0.0, lead=0.0, premium=0.0, partner=0.0)
        for c in years:
            if c > y: continue
            n = kits[c]; d = y - c
            if d == 0:
                line['kit'] += n * kit_margin(a); rev['kit'] += n * a['kit_price']
            for t, w in ((d, 0.5), (d - 1, 0.5)):
                if t < 0 or t > 3: continue
                v = per_customer(a, t)
                for k in v: line[k] += n * w * v[k]
                rev['refill'] += n * w * a['refill_take'] * refill_ships(a)[t] * a['refill_price']
                rev['lead'] += n * w * v['lead']; rev['premium'] += n * w * v['premium']; rev['partner'] += n * w * v['partner']
        acq = kits[y] * cac[y]; fx = sum(fixed[y].values())
        contrib = sum(line.values())
        out[y] = dict(revenue=sum(rev.values()), rev=rev, line=line, contribution=contrib,
                      acquisition=acq, fixed=fx, profit=contrib - acq - fx)
    return out

# ---------------- Path A: test first, grow on our own traffic ----------------
A_KITS = {2027: 8000, 2028: 10000, 2029: 10000}     # own quote-page traffic only (confirm vs lead volume)
A_CAC = {2027: 5.0, 2028: 5.0, 2029: 5.0}           # page, email, creative; no paid media
A_FIXED = {
    2027: {'90-day test (stock, page, 3PL setup)': 15000, 'Counsel: consent and privacy': 25000, 'Owner (part of one role)': 60000},
    2028: {'Owner (part of one role)': 60000, 'Compliance': 10000},
    2029: {'Owner (part of one role)': 60000, 'Compliance': 10000},
}

# ---------------- Path B: launch with rewards ----------------
B = copy.deepcopy(BASE)
B.update(app=True,
         active=(0.50, 0.35, 0.25),   # app-active share by customer-year (rewards keep people opening it)
         optin=0.40,                  # a reward for sharing nudges opt-in up a little
         scored=0.50,
         premium=1.4,                 # safe-driver lead ~1.4x EPL: bind lift x LTV (Arity IQ, vendor); 1.0x floor, ~2x needs a filed score
         reward_cost=4.0,             # prize counter (rewards.py): ~$2.76 expected per active driver; $4 leaves room for the club 2x perk. Worst case $9.53
         partner_rev=(6.0, 2.5, 2.5)) # Upside referral, car wash bounty (once); affiliate commissions ~$1-3/yr
B_KITS = {2027: 15000, 2028: 50000, 2029: 120000}
B_CAC = {2027: 6.0, 2028: 13.0, 2029: 15.0}       # own traffic first, then partner co-marketing and paid at <= $17
B_FIXED = {
    2027: {'90-day test': 15000, 'Counsel: consent, privacy, sweepstakes': 40000,
           'Product design, molds, prototypes': 70000, 'App, backend, admin console (iPhone launch, build_cost.py)': 274000,
           'Team: owner, engineer (H2), partnerships (H2)': 190000, 'Monthly prize draws (full tank, tires, car washes)': 6000},
    2028: {'Android and growth features (build_cost.py phase 2)': 109000,
           'App running costs: hosting, tools, security testing': 54000, 'SOC 2 and compliance': 45000,
           'Team: owner, engineer (maintains the app), partnerships, support': 450000,
           'Monthly prize draws (full tank, tires, car washes)': 30000, 'Prize draw rules and admin': 10000},
    2029: {'App running costs: hosting, tools, security testing': 54000, 'SOC 2 and compliance': 45000,
           'Team: + carrier partnerships': 560000,
           'Monthly prize draws (full tank, tires, car washes)': 60000, 'Prize draw rules and admin': 10000},
}

def show(name, a, kits, cac, fixed):
    r = run(a, kits, cac, fixed)
    print(f"== {name}: kit margin ${kit_margin(a):.2f}, 3-yr value per customer ${three_year_value(a):.2f}")
    cum = 0
    for y, v in r.items():
        cum += v['profit']
        print(y, f"kits {kits[y]:>7,}  revenue ${v['revenue']/1e6:5.2f}M  contrib ${v['contribution']/1e3:7.0f}K  "
                 f"acq ${v['acquisition']/1e3:6.0f}K  fixed ${v['fixed']/1e3:5.0f}K  profit ${v['profit']/1e3:7.0f}K  cum ${cum/1e3:7.0f}K")
        print('     rev:', {k: round(x/1e3) for k, x in v['rev'].items()}, ' rewards cost', round(v['line']['rewards']/1e3))
    return r

def breakeven_cac(a, kits, cac, fixed):
    lo, hi = 0.0, 100.0
    for _ in range(50):
        m = (lo + hi) / 2
        r = run(a, kits, {y: m for y in kits}, fixed)
        (lo, hi) = (m, hi) if sum(v['profit'] for v in r.values()) > 0 else (lo, m)
    return lo

if __name__ == '__main__':
    ra = show('PATH A  Test first, own traffic', BASE, A_KITS, A_CAC, A_FIXED)
    rb = show('PATH B  Launch with rewards', B, B_KITS, B_CAC, B_FIXED)
    print('break-even flat CAC  A:', round(breakeven_cac(BASE, A_KITS, A_CAC, A_FIXED), 2),
          ' B:', round(breakeven_cac(B, B_KITS, B_CAC, B_FIXED), 2))
    # peak cash: cumulative profit low point plus stock on hand (~2 months of kits at landed cost)
    for nm, r, k in (('A', ra, A_KITS), ('B', rb, B_KITS)):
        cum = 0; low = 0
        for y in sorted(r):
            cum += r[y]['profit']; low = min(low, cum - k[y] / 6 * BASE['kit_landed'])
        print(nm, 'approx peak cash need', round(-low / 1e3), 'K')
    # sensitivities for Path B
    for lab, upd in (('opt-in 25%', dict(optin=0.25)), ('shop 25%', dict(shop=0.25)), ('rewards $20', dict(reward_cost=20.0)),
                     ('no partner revenue', dict(partner_rev=(0, 0, 0))), ('premium 1.0x', dict(premium=1.0))):
        x = copy.deepcopy(B); x.update(upd)
        print('B sens', lab, round(sum(v['profit'] for v in run(x, B_KITS, B_CAC, B_FIXED).values()) / 1e3), 'K')
    for lab, upd in (('shop 25%', dict(shop=0.25)), ('price $25', dict(kit_price=25.0)), ('opt-in 20%', dict(optin=0.20))):
        x = copy.deepcopy(BASE); x.update(upd)
        print('A sens', lab, round(sum(v['profit'] for v in run(x, A_KITS, A_CAC, A_FIXED).values()) / 1e3), 'K')

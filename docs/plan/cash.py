"""Month-by-month cash for Path A and Path B, using the per-customer values in paths.py.

Answers two questions the yearly model can't: how much cash is out at the worst point,
and in which month the cumulative cash turns positive.

Run: python3 cash.py
"""
import copy
import paths as P

MONTHS = [(y, m) for y in (2027, 2028, 2029, 2030) for m in range(1, 13)]   # 2030 only to find the payback month

def spread(total, months):
    return {k: total / len(months) for k in months}

def ramp(total, months):
    """Linear ramp across the months (later months sell more)."""
    w = list(range(1, len(months) + 1)); s = sum(w)
    return {k: total * wi / s for k, wi in zip(months, w)}

def yr(y, a=1, b=12):
    return [(y, m) for m in range(a, b + 1)]

def kits_a():
    k = {}
    k.update(spread(1000, yr(2027, 2, 3)))       # the 90-day test
    k.update(spread(7000, yr(2027, 4, 12)))
    k.update(spread(10000, yr(2028)))
    k.update(spread(10000, yr(2029)))
    k.update(spread(10000, yr(2030)))            # 2030 held flat
    return k

def kits_b():
    k = {}
    k.update(spread(1000, yr(2027, 2, 3)))       # the 90-day test
    k.update(spread(4200, yr(2027, 4, 9)))       # stock freshener keeps selling while we build
    k.update(spread(9800, yr(2027, 10, 12)))     # app and rewards live in October
    k.update(ramp(50000, yr(2028)))
    k.update(ramp(120000, yr(2029)))
    k.update(spread(120000, yr(2030)))           # 2030 held flat at the 2029 total
    return k

def fixed_a():
    f = {k: 0.0 for k in MONTHS}
    for k, v in spread(15000, yr(2027, 1, 1)).items(): f[k] += v           # stock, page, 3PL setup
    for k, v in spread(25000, yr(2027, 1, 3)).items(): f[k] += v           # counsel
    for k, v in spread(45000, yr(2027, 4, 12)).items(): f[k] += v          # owner time after the test
    for y in (2028, 2029, 2030):
        for k, v in spread(70000, yr(y)).items(): f[k] += v
    return f

def fixed_b():
    f = {k: 0.0 for k in MONTHS}
    for k, v in spread(15000, yr(2027, 1, 1)).items(): f[k] += v           # test
    for k, v in spread(40000, yr(2027, 1, 6)).items(): f[k] += v           # counsel
    for k, v in spread(70000, yr(2027, 4, 9)).items(): f[k] += v           # design, molds, prototypes
    for k, v in spread(150000, yr(2027, 4, 9)).items(): f[k] += v          # app, rewards wallet, SDK
    for k, v in spread(190000, yr(2027, 4, 12)).items(): f[k] += v         # team from April
    for k, v in spread(6000, yr(2027, 10, 12)).items(): f[k] += v          # prize draws
    for k, v in spread(3000, yr(2027, 9, 9)).items(): f[k] += v            # prize draw rules
    for y in (2028, 2029, 2030):
        for k, v in spread(sum(P.B_FIXED[min(y, 2029)].values()), yr(y)).items(): f[k] += v
    return f

def cac_for(path, k):
    return (P.A_CAC if path == 'A' else P.B_CAC)[min(k[0], 2029)]

def simulate(a, kits, fixed, path, app_from=(2027, 10), stock_months=2):
    idx = {k: i for i, k in enumerate(MONTHS)}
    cash = {k: 0.0 for k in MONTHS}
    rev = {k: 0.0 for k in MONTHS}
    for k, n in kits.items():
        i = idx[k]
        cash[k] += n * (P.kit_margin(a) - cac_for(path, k))
        rev[k] += n * a['kit_price']
        live = a['app'] and idx[k] >= idx.get(app_from, 0)
        for t in range(3):
            aa = copy.deepcopy(a)
            if not live: aa['app'] = False
            pc = P.per_customer(aa, t)
            v = sum(pc.values()) / 12
            r = (aa['refill_take'] * P.refill_ships(aa)[t] * aa['refill_price'] + pc['lead'] + pc['premium'] + pc['partner']) / 12
            for j in range(12):
                mi = i + 12 * t + j
                if mi < len(MONTHS): cash[MONTHS[mi]] += n * v; rev[MONTHS[mi]] += n * r
    for k in MONTHS: cash[k] -= fixed[k]
    # stock bought ahead: carry `stock_months` of upcoming kits at landed cost
    def stock(i): return sum(kits.get(MONTHS[j], 0) for j in range(i + 1, min(i + 1 + stock_months, len(MONTHS)))) * a['kit_landed']
    run, low, low_at, back_at, prev_stock = 0.0, 0.0, None, None, 0.0
    by_year = {}; rev_year = {}
    for i, k in enumerate(MONTHS):
        s = stock(i)
        run += cash[k] - (s - prev_stock); prev_stock = s
        by_year[k[0]] = by_year.get(k[0], 0) + cash[k]
        rev_year[k[0]] = rev_year.get(k[0], 0) + rev[k]
        if run < low: low, low_at = run, k
        if back_at is None and low < 0 and run >= 0 and low_at is not None: back_at = k
    return dict(peak=-low, peak_at=low_at, back_at=back_at, end=run, by_year=by_year, rev_year=rev_year)

if __name__ == '__main__':
    ra = simulate(P.BASE, kits_a(), fixed_a(), 'A')
    rb = simulate(P.B, kits_b(), fixed_b(), 'B')
    for nm, r in (('A', ra), ('B', rb)):
        print(nm, f"peak cash out ${r['peak']/1e3:.0f}K at {r['peak_at']}, back to even {r['back_at']}, "
                  f"profit by year", {y: round(v/1e3) for y, v in r['by_year'].items()},
                  'revenue by year', {y: round(v/1e6, 2) for y, v in r['rev_year'].items()},
                  '3-yr profit', round(sum(v for y, v in r['by_year'].items() if y < 2030)/1e3),
                  '3-yr revenue', round(sum(v for y, v in r['rev_year'].items() if y < 2030)/1e6, 2))
    # Path B ranges: a cautious and a good case, several levers at once
    for nm, upd, cac_shift in (('cautious', dict(optin=0.35, refill_take=0.27, shop=0.45), 2.0),
                               ('good', dict(optin=0.45, refill_take=0.33, shop=0.55), -2.0)):
        b = copy.deepcopy(P.B); b.update(upd)
        saved = dict(P.B_CAC)
        for y in (2028, 2029): P.B_CAC[y] = saved[y] + cac_shift
        r = simulate(b, kits_b(), fixed_b(), 'B')
        yearly = P.run(b, P.B_KITS, P.B_CAC, P.B_FIXED)
        P.B_CAC.update(saved)
        print('B', nm, f"3-yr profit ${sum(v for y, v in r['by_year'].items() if y < 2030)/1e3:.0f}K, 2029 ${r['by_year'][2029]/1e3:.0f}K, "
                       f"peak cash ${r['peak']/1e3:.0f}K, back to even {r['back_at']}")

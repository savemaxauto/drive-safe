# SUPERSEDED by paths.py (the deck's numbers come from paths.py). Kept for history.
import copy, forecast as F
from model import A, kit_contrib, per_buyer

def lean(price=29.0, kits=None, cac=None, fixed=None, **over):
    a = copy.deepcopy(A); a['kit_price'] = price; a.update(over)
    F.KITS = kits or {2027: 10000, 2028: 30000, 2029: 75000}
    F.CAC = cac or {2027: 5.0, 2028: 10.0, 2029: 14.0}
    F.FIXED = fixed or {
     2027: {'launch': 40000, 'app': 90000, 'compliance': 25000, 'team': 60000},
     2028: {'custom housing': 80000, 'app ops': 45000, 'team': 200000, 'compliance': 20000},
     2029: {'app ops': 60000, 'team': 300000, 'compliance': 20000}}
    r = F.run(a, F.KITS, F.CAC); g = F.gross_revenue(a, F.KITS)
    return a, r, g

for name, kw in [('lean base $29', {}), ('lean upside', dict(optin=0.5, premium_mult=2.8, scored=0.5)),
                 ('lean, price 25', dict(price=25.0))]:
    a, r, g = lean(**kw)
    print('==', name, 'kit contrib', round(kit_contrib(a),2), '3yr/buyer', round(sum(sum(per_buyer(i, True, a).values()) for i in range(3)),2))
    for y in r: print(y, 'gross', g[y], 'sumgross', sum(g[y].values()), '| contrib', r[y]['contribution'], 'acq', r[y]['acquisition'], 'fixed', r[y]['fixed'], 'profit', r[y]['profit'])
    print('cum', sum(v['profit'] for v in r.values()))
    # drivers with consented score history by end of each year
    tot=0
    for y in sorted(F.KITS):
        tot += F.KITS[y]
        print(' cum kits', y, tot, 'opted-in', round(tot*a['optin']), 'scored opted-in (app live)', round(tot*a['optin']*a['scored']) if y>=2028 else 0)

# SUPERSEDED by paths.py (the deck's numbers come from paths.py). Kept for history.
from model import A, per_buyer
import copy, json

KITS = {2027: 12000, 2028: 50000, 2029: 120000}
CAC  = {2027: 12.0, 2028: 18.0, 2029: 20.0}      # blended: owned lead traffic ~$3, paid social/TikTok $17-45
APP_LIVE_FROM = 2028
FIXED = {  # one-time build + operating costs
 2027: {'Validate + launch (samples, site, first 5k units setup)': 45000, 'App MVP build (React Native + telematics SDK)': 90000,
        'Compliance counsel (consent, TCPA, privacy)': 25000, 'Team (product/ops lead)': 110000},
 2028: {'Custom housing: design, DFM, tooling': 80000, 'App maintenance + SDK + data': 45000,
        'Team (+ engineer)': 260000, 'Compliance + data broker registration': 20000},
 2029: {'App maintenance + SDK + data': 70000, 'Team (+ carrier partnerships)': 400000, 'Compliance': 20000},
}

def run(a=A, kits=KITS, cac=CAC):
    years = sorted(kits); out = {}
    for y in years:
        rev = dict(kit=0, refill=0, lead=0, premium=0)
        for cy in years:
            if cy > y: continue
            n = kits[cy]; idx = y - cy
            v = per_buyer(idx, y >= APP_LIVE_FROM, a)
            w = 0.5 if idx == 0 else 1.0   # mid-year launch of each cohort's recurring revenue
            rev['kit'] += n * v['kit']
            for k in ('refill', 'lead', 'premium'):
                rev[k] += n * v[k] * (w if idx == 0 else 1)
                if idx == 1: rev[k] += kits[cy] * per_buyer(0, y>=APP_LIVE_FROM, a)[k] * 0.5  # carry the other half of year-1 value
        acq = kits[y] * cac[y]; fixed = sum(FIXED[y].values())
        contrib = sum(rev.values())
        out[y] = dict(rev={k: round(v) for k, v in rev.items()}, contribution=round(contrib), acquisition=round(acq),
                      fixed=fixed, profit=round(contrib - acq - fixed))
    return out

def gross_revenue(a=A, kits=KITS):
    # top-line revenue (not contribution) for display
    from model import refill_ships_by_year
    years = sorted(kits); res = {}
    for y in years:
        kit = kits[y]*a['kit_price']; refill = lead = prem = 0
        for cy in years:
            if cy > y: continue
            idx = y-cy
            ships = refill_ships_by_year(a, 4)
            s = ships[idx]*(0.5 if idx == 0 else 1) + (ships[0]*0.5 if idx == 1 else 0)
            refill += kits[cy]*a['refill_take']*s*a['refill_price']
            v = per_buyer(idx, y >= APP_LIVE_FROM, a); v0 = per_buyer(0, y >= APP_LIVE_FROM, a)
            lw = (0.5 if idx == 0 else 1)
            lead += kits[cy]*(v['lead']*lw + (v0['lead']*0.5 if idx == 1 else 0))
            prem += kits[cy]*(v['premium']*lw + (v0['premium']*0.5 if idx == 1 else 0))
        res[y] = dict(kit=round(kit), refill=round(refill), lead=round(lead), premium=round(prem))
    return res

if __name__ == '__main__':
    base = run()
    up = copy.deepcopy(A); up.update(optin=0.50, premium_mult=2.8, scored=0.5)
    print('BASE'); [print(y, v) for y, v in base.items()]
    print('cum profit', sum(v['profit'] for v in base.values()))
    print('GROSS', gross_revenue())
    print('UPSIDE'); u = run(up); [print(y, v) for y, v in u.items()]
    print('cum', sum(v['profit'] for v in u.values()))

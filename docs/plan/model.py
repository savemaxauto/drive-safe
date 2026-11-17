"""SUPERSEDED by paths.py (the deck's numbers come from paths.py). Kept for history.
Save Max Lives: unit economics and 3-year forecast.
Every input is listed in ASSUMPTIONS with its basis. Run: python3 model.py"""
A = dict(
    # Kit (phase 1+): stock diffuser + NFC tag, $25
    kit_price=25.00,
    kit_landed=3.75,        # diffuser $1.00-1.40, NFC $0.16-0.25, carton $0.22-0.40, 2 refills ~$1, freight+tariff
    fulfill=5.00,           # 3PL all-in $4.50-7.40/order
    postage=5.50,           # USPS Ground Advantage <1 lb, est.
    pay_fee_pct=0.029, pay_fee_fix=0.30,
    # Refill club: 3 refills every quarter
    refill_take=0.30, refill_price=18.00, refill_cogs=2.40, refill_ship=8.75,
    first_renewal_keep=0.73,  # 26-28% first-renewal churn (Recharge)
    quarterly_keep=0.83,      # 6%/mo churn (4-8% benchmark)
    # Leads
    optin=0.35,               # share of buyers who opt in to quotes at checkout (assumption to test)
    shop_rate=0.50,           # share of opted-in drivers sold as a lead per year (53% shop yearly, J.D. Power)
    reach_decay=0.75,         # share still reachable each later year
    epl=26.47,                # October blended auto EPL
    # Safe-driver tier (app live from 2028)
    scored=0.40,              # share of opted-in drivers with 90+ days of driving history
    safe=0.50,                # share of scored drivers in the safe tier
    premium_mult=1.75,        # 1.5-2x a normal lead (preferred-lead price sheets)
)

def kit_contrib(a=A):
    p=a['kit_price']; return p-a['kit_landed']-a['fulfill']-a['postage']-(p*a['pay_fee_pct']+a['pay_fee_fix'])

def refill_ship_margin(a=A):
    p=a['refill_price']; return p-a['refill_cogs']-a['refill_ship']-(p*a['pay_fee_pct']+a['pay_fee_fix'])

def refill_ships_by_year(a=A, years=3):
    # shipments at months 2,5,8,11,14,... survival: 1, first_keep, then *quarterly_keep
    surv=[1.0]; 
    for i in range(1,4*years): surv.append(surv[-1]*(a['first_renewal_keep'] if i==1 else a['quarterly_keep']))
    return [sum(surv[4*y:4*y+4]) for y in range(years)]

def per_buyer(year_index, app_live, a=A):
    """Value per kit buyer in their Nth year (0 = year bought)."""
    kit = kit_contrib(a) if year_index==0 else 0
    refill = a['refill_take']*refill_ships_by_year(a,4)[year_index]*refill_ship_margin(a)
    reach = a['reach_decay']**year_index
    leads = a['optin']*a['shop_rate']*reach
    std = leads*a['epl']
    prem = leads*(a['scored']*a['safe'])*(a['premium_mult']-1)*a['epl'] if app_live else 0
    return dict(kit=kit, refill=refill, lead=std, premium=prem)

if __name__=='__main__':
    print('kit contribution', round(kit_contrib(),2))
    print('refill margin/shipment', round(refill_ship_margin(),2), 'ships/yr', [round(x,2) for x in refill_ships_by_year()])
    for live in (False, True):
        tot=0
        for y in range(3):
            v=per_buyer(y, live); s=sum(v.values()); tot+=s
            print('app' if live else 'no-app', 'yr',y+1, {k:round(x,2) for k,x in v.items()}, 'total',round(s,2))
        print('  3-yr value per buyer', round(tot,2))

import requests
import json
import cmc_api

def pp(data):
    return json.dumps(data, indent=3)

def mil(market_cap):
    return f"{(float(market_cap)/10**6):.0f}M"
    

######################################################################################
# j = fetch_data(fetch_from_network=True)
# exit(0)

tokens = cmc_api.fetch_data()
cmc_tokens = { t['symbol']: float(t['quote']['USD']['market_cap'] or 0) for t in tokens }
cmc_platforms = { t['symbol']: t['platform']['name'] for t in tokens }

r = requests.get("https://dex.binance.org/api/v1/tokens").json()

sum_market_cap, on_binance, highest = 0.0, [], None
for t in r:
    sym = t['original_symbol']
    on_binance.append(sym)
    if sym in cmc_tokens:
        if highest is None or cmc_tokens[sym] > cmc_tokens[highest]:
            highest = sym
        sum_market_cap += cmc_tokens[sym]
        print(f"{sym}:\t{mil(cmc_tokens[sym])}\t{cmc_platforms[sym]}")
    else:
        print(f"{sym}:\t--")

print(f"\n\ntotal market cap of {len(on_binance)} tokens on Binance DEX: {mil(sum_market_cap)}")
print(f"the highest market cap token on Binance DEX is {highest} ({mil(cmc_tokens[highest])})")

not_on_binance = [ s for s in cmc_tokens if s not in on_binance]
not_binance_sum_market_cap = sum([ cmc_tokens[s] for s in not_on_binance ])
print(f"\n\n{len(not_on_binance)} tokens not traded on Binance DEX (market cap = {mil(not_binance_sum_market_cap)})")

top_ten = { k: f"{mil(cmc_tokens[k])}" for k in not_on_binance[:10] }
print(f"\n\namong the highest market cap are: {top_ten}")




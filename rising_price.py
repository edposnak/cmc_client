# from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


import sys
import json
import requests
# import argparse
# import datetime
# import time
# import csv

##############################################################################################
#
# Library functions for exchanges, tokens, and prices
#
# get exchanges

API_BASE_URL = 'https://pro-api.coinmarketcap.com/v1'
API_KEY = '1bcd5ce4-80f1-4b19-8247-f3856f577cfb'
CRYPTOCURRENCY_ENDPOINT = API_BASE_URL + '/cryptocurrency'
EXCHANGE_ENDPOINT = API_BASE_URL + '/exchange'

def pp(data):
    return json.dumps(data, indent=3)

def best_tokens(tokens, window="24h", min_volume=10000000):
    pct_attr = f"percent_change_{window}"
    pct_change_by_token, no_data_tokens = {}, []
    for t in tokens:
        quote = t['quote']['USD']
        vol = 0 if quote['volume_24h'] is None else int(quote['volume_24h'])
        if vol > min_volume:
            if quote[pct_attr] is None:
                no_data_tokens.append(t['symbol'])
            else:
                pct_change_by_token[t['symbol']] = float(quote[pct_attr])

    return sorted(pct_change_by_token.items(),  key=lambda x: -x[1])
    

def fetch_data(fetch_from_network=False):
    json_filename = 'tokens.json'
    
    if fetch_from_network:
        try:
            # https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=1&limit=10&cryptocurrency_type=tokens&convert=USD,BTC
            r = requests.get(CRYPTOCURRENCY_ENDPOINT + '/listings/latest',
                             params={'sort':'market_cap', 'start':'1', 'limit':'5000',
                                     'cryptocurrency_type':'tokens', 'convert':'USD'},
                             headers={'Accept': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY})
            j = r.json()
            print(f"json: \n{pp(j)}")
            with open(json_filename, 'w') as f:
                json.dump(j, f)
        except Exception as e:
            r = e.args[0]
            print(f"exception: {e}")

    else:
        with open(json_filename) as f:
            j = json.load(f)

    return j

######################################################################################
# j = fetch_data(fetch_from_network=True)
j = fetch_data()
tokens = j['data']

min_24h_volume = 5000000

print("Best Performing Tokens Over the Last 24 Hours")
best = best_tokens(tokens, window="24h", min_volume=min_24h_volume)
for t in best[0:20]:
    print(f"{t[0]}: {t[1]}")

print("\nBest Performing Tokens Over the Last 7 Days")
best = best_tokens(tokens, window="7d", min_volume=min_24h_volume)
for t in best[0:20]:
    print(f"{t[0]}: {t[1]}")
    

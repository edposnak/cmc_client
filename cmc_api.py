import sys
import os
import datetime
import json
import requests

##############################################################################################
#
# Library functions for exchanges, tokens, and prices
#
# get exchanges

API_BASE_URL = 'https://pro-api.coinmarketcap.com/v1'
API_KEY = '1bcd5ce4-80f1-4b19-8247-f3856f577cfb'
CRYPTOCURRENCY_ENDPOINT = API_BASE_URL + '/cryptocurrency'
EXCHANGE_ENDPOINT = API_BASE_URL + '/exchange'
LATEST_JSON_FILENAME = 'json/tokens.json'

def fetch_data(fetch_from_network=False):
    if fetch_from_network:
        # https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=1&limit=10&cryptocurrency_type=tokens&convert=USD,BTC
        r = requests.get(CRYPTOCURRENCY_ENDPOINT + '/listings/latest',
                         params={'sort':'market_cap', 'start':'1', 'limit':'5000',
                                 'cryptocurrency_type':'tokens', 'convert':'USD'},
                         headers={'Accept': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY})
        j = r.json()
        d = datetime.datetime.today()
        json_filename = f"json/{d.year}-{d.month:02d}-{d.day:02d}_{d.hour:02d}:{d.minute:02d}:{d.second:02d}-tokens.json"
        print(f"New data fetched from network will be saved to {json_filename}")
        with open(json_filename, 'w') as f:
            json.dump(j, f)
            if os.path.lexists(LATEST_JSON_FILENAME): os.unlink(LATEST_JSON_FILENAME)
            os.symlink(os.path.basename(json_filename),
                       os.path.join(os.getcwd(), LATEST_JSON_FILENAME))

    with open(LATEST_JSON_FILENAME) as f:
        return json.load(f)['data']


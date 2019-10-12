import sys
import cmc_api

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
    


######################################################################################
# tokens = fetch_data(fetch_from_network=True)
tokens = cmc_api.fetch_data()

min_24h_volume = 5000000

print("Best Performing Tokens Over the Last 24 Hours")
best = best_tokens(tokens, window="24h", min_volume=min_24h_volume)
for t in best[0:20]:
    print(f"{t[0]}: {t[1]}")

print("\nBest Performing Tokens Over the Last 7 Days")
best = best_tokens(tokens, window="7d", min_volume=min_24h_volume)
for t in best[0:20]:
    print(f"{t[0]}: {t[1]}")
    

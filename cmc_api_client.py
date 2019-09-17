import cmc_api

def pp(data):
    return json.dumps(data, indent=3)

def print_stats(tokens, split_usdt_market_cap=True):
    """Prints stats for the given set of tokens"""
    
    # token_cap = { t['symbol']:float(t['quote']['USD']['market_cap'] or 0) for t in tokens }
    platform_cap, platform_n = {}, {}
    for t in tokens:
        platform = t['platform']['name']
        if platform not in platform_n:
            platform_n[platform] = 0
            platform_cap[platform] = 0.0
        market_cap = float(t['quote']['USD']['market_cap'] or 0)
        platform_cap[platform] += market_cap
        platform_n[platform] += 1

    # About 1.55B of Tether's market cap is on Ethereum as ERC-20
    # https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7
    # https://wallet.tether.to/transparency
    ERC20_CAP = 1.95 * 10**9
    if split_usdt_market_cap:
        platform_cap['Omni'] -= ERC20_CAP
        platform_cap['Ethereum'] += ERC20_CAP
        platform_n['Ethereum'] += 1
        
    total_cap = sum(platform_cap.values())/10**9
    total_n = sum(platform_n.values())

    s = [(k, platform_cap[k]/10**9) for k in sorted(platform_cap, key=platform_cap.get, reverse=True)]
    print(f"\n\nout of the top {total_n} tokens listed on CMC making up a total market cap of ${total_cap:.3f}B")
    if split_usdt_market_cap:
        print(f"(and accounting for {ERC20_CAP/10**9}B USDT on Ethereum and not Omni)")
    print("\n")
    for p in s:
        print(f"{p[0]} has {platform_n[p[0]]} tokens ({100*platform_n[p[0]]/total_n:.1f}%) with total market cap ${p[1]:.3f}B ({100*p[1]/total_cap:.2f}%)")
    
    return None

######################################################################################
tokens = cmc_api.fetch_data(fetch_from_network=True)
# tokens = cmc_api.fetch_data()

print_stats(tokens)

TOP_N = 500
print(f"\n\nTop {TOP_N} coins ...\n")
print_stats(tokens[0:TOP_N-1]) # minus 1 because ERC-20 Tether will be added


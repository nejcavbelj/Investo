"""
Benjamin Graham stock analysis module
-------------------------------------
Implements Graham-style ratios and logic to produce a BUY/HOLD/SELL verdict.
Uses the same field names as Peter Lynch module for compatibility.
Includes Net-Net (NCAV) calculation and a comment/explanation of its meaning.
"""

import math

def calc_pe(data):
    return data.get("forwardPE") or data.get("trailingPE") or data.get("pe")

def calc_pb(data):
    return data.get("priceToBook")

def calc_eps_growth_10y(data):
    g = data.get("earningsQuarterlyGrowth") or data.get("epsGrowth")
    return g * 100 if g is not None else None

def calc_earnings_stability_10y(data):
    eps = data.get("trailingEps") or data.get("eps")
    g = data.get("earningsQuarterlyGrowth") or data.get("epsGrowth")
    return (eps is not None and eps > 0) and (g is not None and g > 0)

def calc_debt_to_equity(data):
    return data.get("debtToEquity")

def calc_current_ratio(data):
    ca = data.get("totalCurrentAssets") or data.get("currentAssets")
    cl = data.get("totalCurrentLiabilities") or data.get("currentLiabilities")
    if ca and cl and cl > 0:
        return ca / cl
    return data.get("currentRatio")

def calc_dividend_record_years(data):
    dy = data.get("dividendYield")
    return 20 if dy and dy > 0 else 0

def calc_dividend_yield(data):
    y = data.get("dividendYield")
    return y if y else 0

def calc_intrinsic_value(data):
    eps = data.get("trailingEps") or data.get("eps") or 1
    g = calc_eps_growth_10y(data)
    g_val = g if g is not None else 4
    return eps * (8.5 + 2 * g_val)

def calc_margin_of_safety(data):
    price = data.get("price") or data.get("currentPrice")
    iv = calc_intrinsic_value(data)
    if iv and price:
        return 100 * (1 - price / iv)
    return None

def calc_net_net_value(data):
    """
    Net-Net (NCAV) = totalCurrentAssets - totalLiabilities
    Returns None if fields missing, otherwise numeric (may be negative).
    """
    ca = data.get("totalCurrentAssets")
    tl = data.get("totalLiabilities")
    if ca is not None and tl is not None:
        return ca - tl
    return None

def calc_net_net_comment(data):
    """
    Returns a plain English comment for Net-Net value and buy candidate logic.
    """
    ca = data.get("totalCurrentAssets")
    tl = data.get("totalLiabilities")
    mc = data.get("marketCap")
    shares = data.get("sharesOutstanding") or data.get("shares_outstanding")
    netnet = calc_net_net_value(data)
    comment = ""
    if ca is None or tl is None:
        return "Net-Net calculation not possible: missing totalCurrentAssets or totalLiabilities."
    if netnet is None:
        return "Net-Net calculation not possible: missing required fields."
    if shares is not None and shares > 0:
        ncav_per_share = netnet / shares
    else:
        ncav_per_share = None
    if netnet < 0:
        comment += (
            f"NCAV (Net-Net Current Asset Value) is negative (${netnet:,.0f}): liabilities exceed current assets. "
            "No true Graham deep-value investor would buy this stock, as it fails the liquidation-value test. "
            "For large modern companies (e.g. Apple), this is normal due to bond leverage and earnings power pricing."
        )
    else:
        comment += f"NCAV is positive (${netnet:,.0f}). "
        if mc is not None:
            threshold = (2/3) * netnet
            if mc < threshold:
                comment += (
                    f"Market Cap (${mc:,.0f}) < 2/3×NCAV (${threshold:,.0f}). This is a rare deep-value Graham buy candidate."
                )
            else:
                comment += (
                    f"Market Cap (${mc:,.0f}) >= 2/3×NCAV (${threshold:,.0f}). Not a true Graham net-net candidate."
                )
        else:
            comment += "Market Cap unavailable for net-net screen."
    if ncav_per_share is not None:
        comment += f" NCAV per share: ${ncav_per_share:,.2f}."
    return comment

def calc_market_cap(data):
    return data.get("marketCap")

def calc_netnet_buy_candidate(data):
    mc = calc_market_cap(data)
    nnv = calc_net_net_value(data)
    if mc is None or nnv is None:
        return None
    return mc < (2/3 * nnv) if nnv > 0 else False

def calc_graham_combined_test(data):
    pe = calc_pe(data)
    pb = calc_pb(data)
    d2e = calc_debt_to_equity(data)
    div_years = calc_dividend_record_years(data)
    earning_stab = calc_earnings_stability_10y(data)
    tests = [
        pe is not None and pe < 15,
        pb is not None and pb < 1.5,
        pe is not None and pb is not None and pe * pb < 22.5,
        div_years >= 20,
        earning_stab is True,
        d2e is not None and d2e < 0.5,
    ]
    return all(tests)

def calc_expected_return(data):
    div_yield = calc_dividend_yield(data) or 0
    g = calc_eps_growth_10y(data) or 4
    mos = calc_margin_of_safety(data) or 0
    return div_yield + g + (mos/3)

def graham_metrics(data):
    """
    Returns all Graham metrics, including a 'NetNet_Comment' for the Net-Net calculation.
    """
    return {
        "P/E": calc_pe(data),
        "P/B": calc_pb(data),
        "EPS_Growth_10Y_%": calc_eps_growth_10y(data),
        "Earnings_Stability_10Y": calc_earnings_stability_10y(data),
        "Debt/Equity": calc_debt_to_equity(data),
        "Current_Ratio": calc_current_ratio(data),
        "Dividend_Record_Years": calc_dividend_record_years(data),
        "Dividend_Yield_%": calc_dividend_yield(data),
        "Intrinsic_Value": calc_intrinsic_value(data),
        "Margin_of_Safety_%": calc_margin_of_safety(data),
        "Net_Net_Value": calc_net_net_value(data),
        "NetNet_Buy_Candidate": calc_netnet_buy_candidate(data),
        "NetNet_Comment": calc_net_net_comment(data),  # <-- Comment/explanation
        "Graham_Combined_Test": calc_graham_combined_test(data),
        "Expected_Return_%": calc_expected_return(data),
        "sector": data.get("sector"),
        "industry": data.get("industry"),
        "price": data.get("price"),
        "marketCap": calc_market_cap(data),
    }

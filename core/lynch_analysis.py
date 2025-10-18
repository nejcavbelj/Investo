"""
Peter Lynch stock analysis module
---------------------------------
Implements Lynch-style ratios and logic to produce a BUY/HOLD/SELL verdict.
Keeps all existing metrics and adds all core Lynch metrics and explanations.
"""

def calc_pe(data):
    return data.get("forwardPE") or data.get("trailingPE") or data.get("pe")

def calc_eps_growth(data):
    g = data.get("earningsQuarterlyGrowth") or data.get("epsGrowth")
    if g is not None:
        return g * 100
    return None

def calc_peg(pe, growth):
    if pe and growth and growth > 0:
        return pe / growth
    return None

def calc_debt_to_equity(data):
    return data.get("debtToEquity")

def calc_dividend_yield(data):
    y = data.get("dividendYield")
    if y:
        return y
    return 0

def calc_roe(data):
    roe = data.get("returnOnEquity") or data.get("roe")
    return roe if roe is not None else None

def calc_roa(data):
    roa = data.get("returnOnAssets") or data.get("roa")
    return roa if roa is not None else None

def calc_profit_margin(data):
    pm = data.get("profitMargins") or data.get("profitMargin")
    return pm if pm is not None else None

def calc_price_to_book(data):
    return data.get("priceToBook")

def calc_price_to_sales(data):
    return data.get("priceToSales") or data.get("priceToSalesTrailing12Months")

def calc_current_ratio(data):
    ca = data.get("totalCurrentAssets") or data.get("currentAssets")
    cl = data.get("totalCurrentLiabilities") or data.get("currentLiabilities")
    if ca and cl and cl > 0:
        return ca / cl
    return data.get("currentRatio")

def calc_quick_ratio(data):
    ca = data.get("totalCurrentAssets") or data.get("currentAssets")
    inv = data.get("inventory")
    cl = data.get("totalCurrentLiabilities") or data.get("currentLiabilities")
    if ca and inv is not None and cl and cl > 0:
        return (ca - inv) / cl
    return data.get("quickRatio")

def calc_cash_position(data):
    cash = data.get("totalCash")
    assets = data.get("totalAssets")
    if cash and assets and assets > 0:
        return (cash / assets) * 100
    return None

def calc_inventory_growth(data):
    inv_growth = data.get("inventoryGrowth")
    rev_growth = data.get("salesGrowth") or data.get("revenueGrowth")
    if inv_growth and rev_growth and rev_growth != 0:
        return inv_growth / rev_growth * 100
    return None

def calc_insider_ownership(data):
    insiders = data.get("heldPercentInsiders") or data.get("sharesPercentInsiders")
    if insiders:
        return insiders * 100
    return None

def calc_earnings_yield(data):
    pe = calc_pe(data)
    return 100 / pe if pe else None

def calc_fcf_yield(data):
    fcf = data.get("freeCashflow")
    mcap = data.get("marketCap")
    if fcf and mcap:
        return (fcf / mcap) * 100
    return None

# Collect all metrics in a single dict for reporting
def lynch_metrics(data):
    return {
        "P/E": calc_pe(data),
        "EPS_Growth_%": calc_eps_growth(data),
        "PEG": calc_peg(calc_pe(data), calc_eps_growth(data)),
        "Debt/Equity": calc_debt_to_equity(data),
        "Dividend_Yield_%": calc_dividend_yield(data),
        "Cash/Assets_%": calc_cash_position(data),
        "Inventory/Sales_Growth_%": calc_inventory_growth(data),
        "Insider_Ownership_%": calc_insider_ownership(data),
        "ROE_%": calc_roe(data),
        "ROA_%": calc_roa(data),
        "Profit_Margin_%": calc_profit_margin(data),
        "Price/Book": calc_price_to_book(data),
        "Price/Sales": calc_price_to_sales(data),
        "Current_Ratio": calc_current_ratio(data),
        "Quick_Ratio": calc_quick_ratio(data),
        "Earnings_Yield_%": calc_earnings_yield(data),
        "FCF_Yield_%": calc_fcf_yield(data),
        # keep old metrics if needed
        "sector": data.get("sector"),
        "industry": data.get("industry"),
    }

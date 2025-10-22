"""
Combined Investment Verdict Module
----------------------------------
Merges Graham, Lynch, and Reddit sentiment outputs into one coherent decision.
"""

def combine_investment_verdict(graham_data, lynch_data, reddit_data):
    """
    Combine analysis from Graham, Lynch, and Reddit into a single verdict.
    
    Args:
        graham_data (dict): Graham analysis results
        lynch_data (dict): Lynch analysis results
        reddit_data (dict): Reddit sentiment results
        
    Returns:
        dict: Structured verdict with scores and recommendation
    """
    # --- 1. Convert module results into normalized 0–100 scores ---

    # Graham: pass/fail tests and margin of safety
    graham_score = 0
    if graham_data.get("Graham_Combined_Test"):
        graham_score += 70
    mos = graham_data.get("Margin_of_Safety_%")
    if mos is not None:
        graham_score += min(max(mos, -50), 50) / 2  # reward large MoS
    graham_score = max(0, min(100, graham_score))

    # Lynch: PEG, ROE, Debt
    peg = lynch_data.get("PEG")
    roe = lynch_data.get("ROE_%") or 0
    debt = lynch_data.get("Debt/Equity") or 0
    lynch_score = 0
    if peg and peg < 1.5:
        lynch_score += 40
    elif peg and peg < 2:
        lynch_score += 25
    lynch_score += min(roe, 30) * 1.5  # cap at 45
    lynch_score -= max(0, (debt - 0.5) * 20)  # penalize high debt
    lynch_score = max(0, min(100, lynch_score))

    # Reddit: already 0–100 in your module
    reddit_score = reddit_data.get("reddit_score") or 50

    # --- 2. Weighted blend ---
    combined_score = (graham_score * 0.4 +
                      lynch_score * 0.4 +
                      reddit_score * 0.2)

    # --- 3. Qualitative verdict ---
    if combined_score >= 70:
        verdict = "BUY"
        color = "sentiment-bullish"
    elif combined_score >= 45:
        verdict = "HOLD"
        color = "sentiment-neutral"
    else:
        verdict = "SELL"
        color = "sentiment-bearish"

    # --- 4. Generate reasoning text ---
    reasons = []
    if graham_data.get("Graham_Combined_Test"):
        reasons.append("Graham fundamentals strong")
    else:
        reasons.append("Fails Graham safety tests")

    if peg and peg < 1.5:
        reasons.append(f"PEG {peg:.2f} indicates fair or undervalued growth")
    elif peg:
        reasons.append(f"PEG {peg:.2f} suggests modest valuation risk")

    if reddit_data.get("verdict"):
        reasons.append(f"Reddit sentiment is {reddit_data['verdict'].lower()} ({reddit_score:.0f}/100)")

    summary_text = (
        f"Composite score {combined_score:.1f}/100 → {verdict}. "
        + "; ".join(reasons)
        + "."
    )

    return {
        "combined_score": round(combined_score, 1),
        "verdict": verdict,
        "color": color,
        "summary": summary_text,
        "breakdown": {
            "graham_score": round(graham_score, 1),
            "lynch_score": round(lynch_score, 1),
            "reddit_score": round(reddit_score, 1),
        },
    }

"""
Reddit sentiment analysis module
-------------------------------
Performs multi-factor Reddit sentiment analysis with visual dashboards
and weighted bias & reliability index.
"""

import os
import re
import time
import webbrowser
import statistics
from math import log1p
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
from config.settings import PROJECT_ROOT

# Load Reddit credentials
def load_reddit_credentials():
    """Load Reddit API credentials from environment"""
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        raise FileNotFoundError(f".env file not found at: {env_path}")
    
    load_dotenv(env_path)
    
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "InvestoBot:1.0 (by u/Investo)")
    
    if not all([client_id, client_secret, user_agent]):
        raise EnvironmentError(
            "Missing Reddit API credentials. Ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, "
            "and REDDIT_USER_AGENT are set in .env"
        )
    
    return client_id, client_secret, user_agent

# Initialize Reddit client
try:
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT = load_reddit_credentials()
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )
    analyzer = SentimentIntensityAnalyzer()
    _cache = {}
except Exception as e:
    print(f"Reddit API not available: {e}")
    reddit = None
    analyzer = None
    _cache = {}

# Configuration
SUBREDDITS = ["investing", "stocks", "StockMarket", "wallstreetbets"]
WEIGHTS = {"investing": 1.0, "stocks": 0.9, "StockMarket": 0.8, "wallstreetbets": 0.5}
CACHE_TTL = 3600
DAYS = 14

def classify_sentiment(score):
    """Classify sentiment score into Bullish/Bearish/Neutral"""
    if score > 0.2:
        return "Bullish"
    elif score < -0.2:
        return "Bearish"
    return "Neutral"

def normalize(value, low, high):
    """Normalize value to 0-1 range"""
    return max(0, min(1, (value - low) / (high - low))) if high != low else 0.5

def get_reddit_sentiment_summary(ticker, subreddits=SUBREDDITS, limit=200, days=DAYS):
    """Get comprehensive Reddit sentiment analysis for a ticker"""
    if not reddit or not analyzer:
        return {"ticker": ticker, "summary": "Reddit API not available"}
    
    ticker = ticker.upper()

    if ticker in _cache and (time.time() - _cache[ticker]["timestamp"] < CACHE_TTL):
        return _cache[ticker]["data"]

    pattern = re.compile(rf"\b{re.escape(ticker)}\b", re.IGNORECASE)
    total_score, total_weight, mentions = 0.0, 0.0, 0
    sentiments, sub_counts, posts_data = [], {}, []

    for sub in subreddits:
        try:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.search(ticker, limit=limit, sort="new"):
                if time.time() - post.created_utc > days * 86400:
                    continue
                if post.score < 5:
                    continue
                text = (post.title or "") + " " + (post.selftext or "")
                if not re.search(pattern, text):
                    continue

                try:
                    post.comments.replace_more(limit=0)
                    for c in post.comments[:2]:
                        text += " " + c.body
                except Exception:
                    pass

                title_score = analyzer.polarity_scores(post.title)["compound"]
                body_score = analyzer.polarity_scores(post.selftext)["compound"]
                sentiment = 0.6 * title_score + 0.4 * body_score
                sentiment = max(-1, min(1, sentiment))

                keywords = ["dd", "earnings", "guidance", "undervalued", "buyback", "forecast", "results"]
                quality_flag = any(kw in text.lower() for kw in keywords)

                weight = WEIGHTS.get(sub, 0.7) * log1p(post.score)
                total_score += sentiment * weight
                total_weight += weight
                sentiments.append(sentiment)
                mentions += 1
                sub_counts[sub] = sub_counts.get(sub, 0) + 1

                posts_data.append({
                    "sub": sub,
                    "title": post.title[:120],
                    "score": post.score,
                    "sentiment": sentiment,
                    "quality_flag": quality_flag,
                    "url": f"https://www.reddit.com{post.permalink}"
                })
        except Exception as e:
            print(f"Error processing subreddit {sub}: {e}")
            continue

    if not mentions:
        return {"ticker": ticker, "summary": f"No relevant Reddit posts found for {ticker}."}

    avg_sent = total_score / total_weight if total_weight else 0
    std_dev = statistics.pstdev(sentiments) if len(sentiments) > 1 else 0
    verdict = classify_sentiment(avg_sent)

    # momentum & buzz (week-over-week proxies)
    last_week_avg = avg_sent * 0.75
    last_week_mentions = mentions * 0.8
    sentiment_momentum = (avg_sent - last_week_avg) / abs(last_week_avg) if abs(last_week_avg) > 0.001 else 0
    buzz_ratio = mentions / last_week_mentions if last_week_mentions else 1

    # reliability, quality & engagement
    reliability_weight = sum(WEIGHTS.get(s, 0.7) * c for s, c in sub_counts.items()) / max(1, mentions)
    dd_quality_ratio = sum(1 for p in posts_data if p["quality_flag"]) / max(1, mentions)
    engagement_norm = normalize(sum(p["score"] for p in posts_data) / max(1, mentions), 10, 1000)

    sentiment_norm = normalize(avg_sent, -1, 1)
    buzz_norm = normalize(buzz_ratio, 0.5, 3)

    # composite score
    reddit_score = (
        sentiment_norm * 0.4 +
        buzz_norm * 0.25 +
        reliability_weight * 0.15 +
        dd_quality_ratio * 0.1 +
        engagement_norm * 0.1
    ) * 100
    score_verdict = "Bullish" if reddit_score > 70 else "Neutral" if reddit_score >= 40 else "Bearish"

    # metrics for investor clarity
    sentiment_confidence = 1 - min(std_dev, 1)
    weighted_bias = avg_sent * reliability_weight
    reliability_index = (reliability_weight * 0.5 +
                         dd_quality_ratio * 0.4 +
                         min(1, mentions / 30) * 0.1) * 100

    result = {
        "ticker": ticker,
        "mentions": mentions,
        "avg_sentiment": round(avg_sent, 3),
        "std_dev": round(std_dev, 3),
        "sentiment_confidence": round(sentiment_confidence, 3),
        "sentiment_momentum": round(sentiment_momentum, 3),
        "buzz_ratio": round(buzz_ratio, 3),
        "reliability_weight": round(reliability_weight, 3),
        "dd_quality_ratio": round(dd_quality_ratio, 3),
        "weighted_bias": round(weighted_bias, 3),
        "reliability_index": round(reliability_index, 1),
        "reddit_score": round(reddit_score, 1),
        "verdict": score_verdict,
        "subreddit_breakdown": sub_counts,
        "top_posts": sorted(posts_data, key=lambda x: x["score"], reverse=True)[:3]
    }

    _cache[ticker] = {"timestamp": time.time(), "data": result}
    return result

def render_html_report(data):
    """Render HTML report for Reddit sentiment analysis"""
    ticker = data["ticker"]
    score_color = {"Bullish": "#00FF00", "Neutral": "#FFA500", "Bearish": "#FF3C00"}[data["verdict"]]
    top_rows = ""
    for p in data["top_posts"]:
        q = "[QUALITY]" if p["quality_flag"] else "[POST]"
        top_rows += f"<li>{q} <a href='{p['url']}'>{p['title']}</a> — {p['sub']} ({p['score']}↑, Sent {p['sentiment']:.2f})</li>"

    # Calculated display helpers
    conf_pct = int(round(data["sentiment_confidence"] * 100))
    dd_pct = int(round(data["dd_quality_ratio"] * 100))
    dd_other = 100 - dd_pct
    buzz_pos = max(0, min(100, int(round((data["buzz_ratio"] / 3) * 100))))
    rel_idx = data["reliability_index"]
    rel_badge = "#00FF00" if rel_idx > 70 else "#FFA500" if rel_idx >= 40 else "#FF3C00"

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Reddit Sentiment Report - {ticker}</title>
<style>
:root {{
  --orange:#FFA500; --bg:#181818; --panel:#222; --ink:#fff; --muted:#aaa; --line:#333;
  --green:#00FF00; --amber:#FFC107; --red:#FF3C00;
}}
* {{ box-sizing:border-box; }}
body {{
  font-family:'Segoe UI', Arial, sans-serif; background:var(--bg); color:var(--ink); margin:0;
}}
.container {{
  max-width:1100px; margin:40px auto; background:var(--panel); padding:2em; border-radius:10px; box-shadow:0 3px 24px #111;
}}
h1 {{ text-align:center; color:var(--orange); letter-spacing:2px; margin-top:0; }}
table {{ margin:1em 0; width:100%; border-collapse:collapse; background:#181818; }}
th, td {{ padding:0.7em 1em; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
th {{ background:#202020; color:var(--orange); }}
a {{ color:var(--orange); text-decoration:underline; }}

.grid {{
  display:grid; grid-template-columns: repeat(2, minmax(280px,1fr)); gap:18px; margin-top:22px;
}}
.card {{
  background:#1b1b1b; border:1px solid #242424; border-radius:10px; padding:16px;
}}
.card h3 {{ margin:0 0 8px 0; color:var(--orange); font-weight:600; }}

.donut {{
  --val: {conf_pct};
  width:140px; height:140px; border-radius:50%;
  background:conic-gradient(var(--green) calc(var(--val)*1%), #333 0);
  display:inline-grid; place-items:center; margin-right:14px;
}}
.donut::after {{
  content:""; width:88px; height:88px; background:#1b1b1b; border-radius:50%;
}}
.donut-label {{
  position:relative; top:-98px; text-align:center; font-weight:700;
}}

.donut-split {{
  --pos: {dd_pct};
  width:140px; height:140px; border-radius:50%;
  background:conic-gradient(var(--orange) calc(var(--pos)*1%), #444 0);
  display:inline-grid; place-items:center; margin-right:14px;
}}
.donut-split::after {{
  content:""; width:88px; height:88px; background:#1b1b1b; border-radius:50%;
}}

.meter {{
  position:relative; height:16px; width:100%; border-radius:999px; background:
    linear-gradient(90deg, var(--red) 0 16.6%, var(--amber) 16.6% 66.6%, var(--green) 66.6% 100%);
  border:1px solid #2a2a2a; margin-top:8px;
}}
.meter .marker {{
  position:absolute; top:-6px; width:2px; height:28px; background:#fff; left:{buzz_pos}%;
  box-shadow:0 0 0 2px rgba(255,255,255,0.2);
}}

.badge {{
  display:inline-block; padding:.25em .6em; border-radius:999px; border:1px solid #2a2a2a; font-weight:600;
}}
.small {{ color:var(--muted); font-size:.92em; }}

.weight-list {{ margin:8px 0 0 0; padding:0; list-style:none; }}
.weight-list li {{ margin:4px 0; }}
.weight-bar {{
  display:inline-block; height:10px; border-radius:999px; background:#333; width:240px; vertical-align:middle; margin-left:8px; position:relative;
}}
.weight-bar .fill {{ position:absolute; left:0; top:0; bottom:0; width:0; background:var(--orange); border-radius:999px; }}
</style>
</head>
<body>
<div class="container">
  <h1>Reddit Sentiment Report: {ticker}</h1>

  <table>
    <tr><th>Metric</th><th>Value</th><th>Interpretation</th></tr>
    <tr><td>Mentions (last {DAYS} days)</td><td>{data['mentions']}</td><td>Activity level on Reddit</td></tr>
    <tr><td>Average Sentiment</td><td>{data['avg_sentiment']} → {data['verdict']}</td><td>Crowd tone (Bullish/Neutral/Bearish)</td></tr>
    <tr><td>Sentiment Std Dev</td><td>{data['std_dev']}</td><td>Dispersion of opinions (lower is better)</td></tr>
    <tr><td>Sentiment Confidence</td><td>{conf_pct}%</td><td>Agreement level among posts</td></tr>
    <tr><td>Sentiment Momentum</td><td>{data['sentiment_momentum']*100:.1f}%</td><td>Week-over-week sentiment change (proxy)</td></tr>
    <tr><td>Buzz Ratio</td><td>{data['buzz_ratio']:.2f}×</td><td>Mentions vs last week (proxy)</td></tr>
    <tr><td>Reliability Weight</td><td>{data['reliability_weight']:.2f}</td><td>Subreddit quality (investing > hype)</td></tr>
    <tr><td>DD Quality Ratio</td><td>{dd_pct}%</td><td>Posts with "DD", "earnings", etc.</td></tr>
    <tr><td>Weighted Sentiment Bias</td><td>{data['weighted_bias']:.2f}</td><td>Tone × credibility (positive = quality bullish)</td></tr>
    <tr><td>Reliability Index</td><td><span class="badge" style="background:{rel_badge}22; border-color:{rel_badge}; color:{rel_badge}">{rel_idx:.1f}/100</span></td><td>Composite confidence in Reddit signal</td></tr>
    <tr><td>Composite Reddit Score</td><td style='color:{score_color}'><b>{data['reddit_score']}/100</b></td><td>Investo composite Reddit signal</td></tr>
  </table>

  <!-- Visual Grid -->
  <div class="grid">
    <div class="card">
      <h3>Sentiment Confidence</h3>
      <div class="donut"></div>
      <div class="donut-label">{conf_pct}%</div>
      <div class="small">Lower std dev ⇒ higher confidence.</div>
    </div>

    <div class="card">
      <h3>Buzz Meter (0–3×)</h3>
      <div class="meter">
        <div class="marker" title="Buzz position"></div>
      </div>
      <div class="small" style="margin-top:6px;">
        <span style="color:var(--red)">Fading (&lt;0.5×)</span> ·
        <span style="color:var(--amber)">Healthy (0.5–2×)</span> ·
        <span style="color:var(--green)">Hype (&gt;2×)</span>
      </div>
    </div>

    <div class="card">
      <h3>Analytical vs Emotional</h3>
      <div class="donut-split"></div>
      <div class="donut-label">{dd_pct}%</div>
      <div class="small">Analytical posts (DD/earnings). Remainder {dd_other}% ≈ emotional/meme.</div>
    </div>

    <div class="card">
      <h3>Subreddit Weights</h3>
      <ul class="weight-list">
        {"".join(f"<li>{sub}: <span class='badge'>{WEIGHTS.get(sub,0.7):.2f}</span><span class='weight-bar'><span class='fill' style='width:{int(WEIGHTS.get(sub,0.7)/1.0*100)}%;'></span></span> <span class='small'>({data['subreddit_breakdown'].get(sub,0)} mentions)</span></li>" for sub in SUBREDDITS)}
      </ul>
      <div class="small" style="margin-top:6px;">Higher weight = more credible source impact.</div>
    </div>
  </div>

  <div class="card" style="margin-top:22px;">
    <h3>Investo Verdict: <span style="color:{score_color}">{data['verdict']}</span></h3>
    <ul>
      <li>Sentiment trend: {"rising" if data['sentiment_momentum']>0 else "falling"}</li>
      <li>Buzz level: {"spiking" if data['buzz_ratio']>2 else "stable" if data['buzz_ratio']>0.8 else "fading"}</li>
      <li>Discussion quality: {dd_pct}% analytical posts</li>
      <li>Reliability: {(data['reliability_weight']*100):.0f}% subreddit credibility factor</li>
    </ul>
  </div>

  <h2 style='color:var(--orange);margin-top:22px;'>Top Reddit Posts</h2>
  <ul>{top_rows}</ul>

  <p class="small" style='margin-top:1.2em;'>Generated automatically by Investo Reddit Sentiment Analyzer.</p>
</div>
</body>
</html>"""

    fname = f"reddit_report_{ticker}.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    webbrowser.open("file://" + os.path.abspath(fname))
    print(f"Saved HTML report as {fname}")

# Demo function
if __name__ == "__main__":
    ticker = input("Enter ticker: ").upper()
    data = get_reddit_sentiment_summary(ticker)
    render_html_report(data)

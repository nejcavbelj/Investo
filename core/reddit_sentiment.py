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
from pathlib import Path
from config.settings import PROJECT_ROOT

# ---------- Load Reddit credentials ----------
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


# ---------- Initialize Reddit client ----------
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

# ---------- Configuration ----------
SUBREDDITS = ["investing", "stocks", "StockMarket", "wallstreetbets"]
WEIGHTS = {"investing": 1.0, "stocks": 0.9, "StockMarket": 0.8, "wallstreetbets": 0.5}
CACHE_TTL = 3600
DAYS = 14


# ---------- Utility functions ----------
def classify_sentiment(score):
    if score > 0.2:
        return "Bullish"
    elif score < -0.2:
        return "Bearish"
    return "Neutral"


def normalize(value, low, high):
    """Normalize value to 0–1 range"""
    return max(0, min(1, (value - low) / (high - low))) if high != low else 0.5


# ---------- Main sentiment summary ----------
def get_reddit_sentiment_summary(ticker, subreddits=SUBREDDITS, limit=200, days=DAYS):
    """Perform comprehensive Reddit sentiment analysis for a ticker"""
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

    # Week-over-week proxies
    last_week_avg = avg_sent * 0.75
    last_week_mentions = mentions * 0.8
    sentiment_momentum = (avg_sent - last_week_avg) / abs(last_week_avg) if abs(last_week_avg) > 0.001 else 0
    buzz_ratio = mentions / last_week_mentions if last_week_mentions else 1

    # Reliability, quality, engagement
    reliability_weight = sum(WEIGHTS.get(s, 0.7) * c for s, c in sub_counts.items()) / max(1, mentions)
    dd_quality_ratio = sum(1 for p in posts_data if p["quality_flag"]) / max(1, mentions)
    engagement_norm = normalize(sum(p["score"] for p in posts_data) / max(1, mentions), 10, 1000)

    sentiment_norm = normalize(avg_sent, -1, 1)
    buzz_norm = normalize(buzz_ratio, 0.5, 3)

    reddit_score = (
        sentiment_norm * 0.4 +
        buzz_norm * 0.25 +
        reliability_weight * 0.15 +
        dd_quality_ratio * 0.1 +
        engagement_norm * 0.1
    ) * 100

    score_verdict = "Bullish" if reddit_score > 70 else "Neutral" if reddit_score >= 40 else "Bearish"

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


# ---------- HTML report generator (REMOVED) ----------
# Individual Reddit reports are no longer generated
# Only combined reports are created in reports/generated folder


# ---------- Demo runner (REMOVED) ----------
# Individual Reddit report generation removed
# Use main.py or combined_report_generator.py for full analysis

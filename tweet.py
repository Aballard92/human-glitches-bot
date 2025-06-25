import csv, datetime, os, pathlib
import tweepy

# ----------------- OAuth 2.0 (user context) -----------------
client = tweepy.Client(
    bearer_token=os.environ["BEARER_TOKEN"],
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_SECRET"],
    wait_on_rate_limit=True,
)

# ----------------- pick today's quote -----------------
root = pathlib.Path(__file__).parent
with open(root / "quotes.csv", newline="", encoding="utf-8") as f:
    quotes = [row[0] for row in csv.reader(f) if row]

start = datetime.date(2025, 1, 1)
idx = (datetime.date.today() - start).days % len(quotes)
quote = quotes[idx]

# ----------------- post -----------------
client.create_tweet(text=quote)
print("Tweeted:", quote)

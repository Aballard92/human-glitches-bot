import csv, datetime, os, pathlib
import tweepy

# --- Auth setup ---
auth = tweepy.OAuth1UserHandler(
    os.environ["API_KEY"],
    os.environ["API_SECRET"],
    os.environ["ACCESS_TOKEN"],
    os.environ["ACCESS_SECRET"],
)
api = tweepy.API(auth)

# --- Load the quotes ---
root = pathlib.Path(__file__).parent
with open(root / "quotes.csv", newline="", encoding="utf-8") as f:
    quotes = [row[0] for row in csv.reader(f) if row]

# --- Pick quote of the day ---
start = datetime.date(2025, 1, 1)
today = datetime.date.today()
idx = (today - start).days % len(quotes)
quote = quotes[idx]

# --- Post to X ---
api.update_status(status=quote)
print("Tweeted:", quote)

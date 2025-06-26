"""
tweet.py
Posts TWO brain-glitch tweets per run (AM & PM), skips duplicates,
auto-adds one hashtag every 3rd tweet, and never exceeds 280 chars.

GitHub secrets required:
  API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN
"""

import csv, datetime, os, pathlib, random, textwrap, tweepy, time

# ── 1. AUTH ────────────────────────────────────────────────────────────────────
client = tweepy.Client(
    bearer_token=os.environ["BEARER_TOKEN"],
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_SECRET"],
    wait_on_rate_limit=True,
)

# ── 2. CONFIG ─────────────────────────────────────────────────────────────────
CSV_PATH   = "quotes.csv"      # 730-row data file (see Section 2)
START_DATE = datetime.date(2025, 6, 25)     # day 1 of the bot
HASHTAGS   = ["#HumanNature", "#CognitiveBias", "#BrainFacts",
              "#MindHacks", "#Psychology"]

# ── 3. LOAD GLITCHES ──────────────────────────────────────────────────────────
root = pathlib.Path(__file__).parent
with open(root / CSV_PATH, newline="", encoding="utf-8") as f:
    glitches = [row[0].strip() for row in csv.reader(f) if row]

# ── 4. PICK TODAY’S TWO TWEETS ────────────────────────────────────────────────
days_since   = (datetime.date.today() - START_DATE).days
base_idx     = days_since * 2                # two tweets per calendar day
todays_texts = [
    glitches[ base_idx        % len(glitches) ],
    glitches[(base_idx + 1)   % len(glitches)]
]

# ── 5. POST, SKIPPING DUPLICATES & ADDING TAGS ────────────────────────────────
posted = 0
for text in todays_texts:
    # add a rotating hashtag every 3rd overall tweet
    overall_count = base_idx + posted + 1    # 1-based counter
    if overall_count % 3 == 0:
        tag  = HASHTAGS[ overall_count % len(HASHTAGS) ]
        room = 280 - len(text) - 1           # 1 for space
        if room >= len(tag):
            text = f"{text} {tag}"

    # ensure 280-char max
    text = textwrap.shorten(text, width=280, placeholder="…")

    try:
        client.create_tweet(text=text)
        print("Tweeted:", text)
        posted += 1
        time.sleep(3)        # polite spacing
    except tweepy.errors.Forbidden as e:
        if "duplicate" in str(e).lower():
            print("Duplicate – skipped:", text)
            continue
        raise

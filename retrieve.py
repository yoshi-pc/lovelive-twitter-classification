import tweepy
import re
import unicodedata
import joblib
from pytz import timezone
import os
from dotenv import load_dotenv
load_dotenv()

BEARER = os.environ.get("twitter_bearer")
if BEARER is None:
    raise ValueError("set the baerer token in your environment variable.")

saved_path = "./tweet_contents.jblb"
if os.path.isfile(saved_path):
    tweet_contents = joblib.load(saved_path)
else:
    tweet_contents = dict(
        mus = [],
        aqours = [],
        nijigaku = [],
        liella = [],
        others = [],
        latest_id = ""
    )

auth = tweepy.OAuth2BearerHandler(BEARER)
api = tweepy.API(auth, wait_on_rate_limit = True)
user_timeline_args = {
    "screen_name": "LoveLive_staff",
    "trim_user": True,
    "tweet_mode": "extended",
    "include_rts": False
}

if tweet_contents["latest_id"] == "":
    user_timeline_args["count"] = 50
else:
    user_timeline_args["since_id"] = tweet_contents["latest_id"]
tweets = api.user_timeline(**user_timeline_args)

search_pat = dict(
    mus = r"(μ\'s|音ノ木坂)",
    aqours = r"(Aqours|サンシャイン|浦の星|浦女)",
    nijigaku = r"(ニジガク|虹ヶ咲|同好会|虹)",
    liella = r"(Liella|結ヶ丘|結女|スーパースター)"
)

if len(tweets) == 0:
    pass
else:
    tweet_contents["latest_id"] = tweets[0].id_str

for item in list(reversed(tweets)):
    text = unicodedata.normalize("NFKC", item.full_text)
    hit = 0
    for k, v in search_pat.items():
        try:
            img_urls = [single["media_url_https"] for single in item.extended_entities["media"]]
        except AttributeError as e:
            img_urls = []
        if re.search(v, text) is not None:
            tweet_contents[k].insert(0, dict(
                id = item.id_str,
                text = item.full_text,
                images = img_urls,
                time = item.created_at.astimezone(timezone('Asia/Tokyo')).strftime(r"%Y/%m/%d %H:%M:%S")
            ))
            hit += 1
    if hit == 0:
        tweet_contents["others"].insert(0, dict(
            id = item.id_str,
            text = item.full_text,
            images = img_urls,
            time = item.created_at.astimezone(timezone('Asia/Tokyo')).strftime(r"%Y/%m/%d %H:%M:%S")
        ))

result_contents = {}
for k, v in tweet_contents.items():
    if type(v) is not list:
        result_contents[k] = v
        continue
    result_contents[k] = v[:50]

joblib.dump(result_contents, saved_path, compress = 3)

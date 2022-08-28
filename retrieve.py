import tweepy
import re
import unicodedata
import joblib
from pytz import timezone
import os
from dotenv import load_dotenv
load_dotenv()

BAERER = os.environ.get("twitter_baerer")
if BAERER is None:
    raise ValueError("set the baerer token in your environment variable.")

auth = tweepy.OAuth2BearerHandler(BAERER)
api = tweepy.API(auth, wait_on_rate_limit = True)
tweets = api.user_timeline(screen_name = "LoveLive_staff", count = 30, trim_user = True, tweet_mode = "extended", include_rts = False)

tweet_ids = dict(
    mus = [],
    aqours = [],
    nijigaku = [],
    liella = [],
    others = []
)

tweet_contents = dict(
    mus = [],
    aqours = [],
    nijigaku = [],
    liella = [],
    others = []
)

search_pat = dict(
    mus = r"(μ\'s|音ノ木坂)",
    aqours = r"(Aqours|サンシャイン|浦の星|浦女)",
    nijigaku = r"(ニジガク|虹ヶ咲|同好会)",
    liella = r"(Liella|結ヶ丘|結女|スーパースター)"
)

pass

for item in tweets:
    text = unicodedata.normalize("NFKC", item.full_text)
    hit = 0
    for k, v in search_pat.items():
        try:
            img_urls = [single["media_url_https"] for single in item.extended_entities["media"]]
        except AttributeError as e:
            img_url = []
        if re.search(v, text) is not None:
            tweet_contents[k].append(dict(
                id = item.id_str,
                text = item.full_text,
                images = img_urls,
                time = item.created_at.astimezone(timezone('Asia/Tokyo')).strftime(r"%Y/%m/%d %H:%M:%S")
            ))
            hit += 1
    if hit == 0:
        tweet_contents["others"].append(dict(
            id = item.id_str,
            text = item.full_text,
            images = img_urls,
            time = item.created_at.astimezone(timezone('Asia/Tokyo')).strftime(r"%Y/%m/%d %H:%M:%S")
        ))

joblib.dump(tweet_contents, "./tweet_contents.jblb", compress = 3)
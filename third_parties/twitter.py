import os
import logging
from pytwitter import Api
from datetime import datetime, timezone

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
disable_warnings(category=InsecureRequestWarning)

logger = logging.getLogger("twitter")

api = Api(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_secret=os.environ.get("TWITTER_ACCESS_SECRET"),
)


def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (i.e. not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has 3 fields: "time_posted"(relative to now), "text", and "url"
    """

    tweets = api.get_timelines(user_id=username, max_results=num_tweets)
    tweet_list = []
    for tweet in tweets:
        if "RT @" not in tweet.text.startswith("@"):
            tweet_dict = {}
            tweet_dict["time_posted"] = str(
                datetime.now(timezone.utc) - tweet.created_at
            )
            tweet_dict["text"] = tweet.text
            tweet_dict[
                "url"
            ] = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            tweet_list.append(tweet_dict)

    return tweet_list

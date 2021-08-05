import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_SECRET")

import tweest

def stream(status):
    print(status)
    print("取得")

tweest.set_auth(consumer_key,consumer_secret,access_token,access_secret)
r = tweest.start({'track':'#tbs'},stream)
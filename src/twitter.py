from tweepy import StreamListener
from tweepy.streaming import json


class RedisTwitterListener(StreamListener):
    def __init__(self, redis):
        super().__init__()
        self.redis = redis

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if 'text' in data:
            print(data['text'])
            for tag in data['text'].split():
                if tag.startswith("#"):
                    self.redis.zincrby(name="tweets", value=tag.replace("#", "", 1))
                    print("Tag: %s" % tag)
        return True

    def on_limit(self, track):
        print("Limit %s" % track)
        return

    def on_error(self, status):
        print("Error status %s" % status)

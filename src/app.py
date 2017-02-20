import os
from configparser import RawConfigParser

from flask import Flask
from redis import StrictRedis
from tweepy import OAuthHandler, Stream

from controller import init_rest_api
from twitter import RedisTwitterListener

r = StrictRedis(host='redis')

app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(init_rest_api(r))


def twitter_streaming():
    config = RawConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources', 'config.cfg'))
    consumer_key = config.get('Twitter', 'consumer_key')
    consumer_secret = config.get('Twitter', 'consumer_secret')
    access_token = config.get('Twitter', 'access_token')
    access_token_secret = config.get('Twitter', 'access_token_secret')
    listener = RedisTwitterListener(r)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener=listener)
    print('Twitter stream started!')
    stream.filter(track=['java', 'python', 'javascript', 'scala', 'groovy', 'haskell', 'kotlin'], async=True)


twitter_streaming()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=os.environ["debug"] == "true", threaded=True)

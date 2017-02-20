import json
from datetime import datetime
from time import sleep

from flask import request, abort, jsonify, Blueprint, g, Response, render_template


def init_rest_api(redis):
    rest_api = Blueprint('rest_api', __name__)

    @rest_api.before_request
    def before_request():
        g.timer = datetime.now()
        if request.method == 'POST' and not request.is_json:
            abort(400)

    @rest_api.after_request
    def after_request(response):
        print('Request time: %f' % (datetime.now() - g.timer).seconds)
        return response

    @rest_api.route('/')
    def main_page():
        return render_template('index.html')

    @rest_api.route('/api/hashtag/name/<path:tag>', methods=['GET'])
    def get_hashtag_counter(tag):
        value = redis.zscore(name="tweets", value=tag)
        tweet = {
            'tag': tag,
            'value': 0 if value is None else value
        }
        return jsonify({'tweet': tweet})

    @rest_api.route('/api/stream')
    def stream():
        def event_stream():
            while True:
                yield 'data: %s\n\n' % json.dumps(get_top_hashtags(10))
                sleep(5)

        return Response(event_stream(), mimetype='text/event-stream')

    def get_top_hashtags(length):
        results = redis.zrevrange(name="tweets", start=0, end=length - 1, withscores=True)
        return [{"tweet": {"tag": r[0].decode('utf-8'), "value": r[1]}} for r in results]

    return rest_api

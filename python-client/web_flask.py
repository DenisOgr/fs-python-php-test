from flask import Flask, Response
import json
from worker import Worker
web_flask = Flask(__name__)


@web_flask.route("/")
def index():
    commands = {
        'message': 'Hello I`m mister Missix and I can do :',
    }

    return Response(json.dumps(commands), mimetype=u'application/json')


@web_flask.route("/get_result")
def get_result():
    print(1)
    # worker = Worker()
    # result = worker.process()

    return Response({1}, mimetype=u'application/json')


if __name__ == "__main__":
    web_flask.run(host='0.0.0.0')
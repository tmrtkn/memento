from flask import Flask, request
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth('Memento')

tokens = {
        "Memento1": "john",
        "Memento2": "susan"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.route('/')
@auth.login_required
def index():
    return 'Hello {}!'.format(auth.current_user())

@app.route('/add', methods=['POST'])
@auth.login_required
def add():
    try:
        url = request.form['url']
    except:
        print('No Url given')

    bar = request.args.get('bar')
    if bar is not None:
        print('bar: ' + bar)
    else:
        print('No bar given')

    for p in request.args:
        print(p + ': ' + request.args.get(p))

    return "200 OK"


if __name__ == "main":
    app.run(ssl_context='adhoc')

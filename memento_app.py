from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from datetime import datetime

NEW_URL_FILE = 'newUrl.txt'

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
        appendUrl(url)
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

def appendUrl(url):
    print("Opening " + NEW_URL_FILE)
    f = open(NEW_URL_FILE, "a+")
    f.write(auth.current_user() + ":\t" + str(datetime.today()) + ":\t" + url + '\n')
    print("Writing " + url + " to " + NEW_URL_FILE)
    f.close()

if __name__ == "__main__":
    app.run(ssl_context='adhoc', host='0.0.0.0')

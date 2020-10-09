from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/add', methods=['POST'])
def add():
    url = request.form['url']
    bar = request.args.get('bar')
    print('Url: ' + url)
    print('bar: ' + bar)
    return "200 OK"

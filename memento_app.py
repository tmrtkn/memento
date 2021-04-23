from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import time

# application database files
NEW_URL_FILE = 'newUrl.txt'
PROCESSING_URL_FILE = 'processingUrl.txt'
DONE_URL_FILE = 'doneUrl.txt'

# Flas app and authentication
app = Flask(__name__)
auth = HTTPTokenAuth('Memento')

tokens = {
        "Memento1": "john",
        "Memento2": "susan"
}

# Scheduling
scheduler = BackgroundScheduler({
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '1'
     },
    'apscheduler.job_defaults.max_instances': '1'
})

def process(url):
    print("Processing: '" + url + "'")

def getFirstLine(file):
    first_line = None
    with open(file) as f:
        first_line = f.readline()

    if first_line in (None, '') or not first_line.strip():
        return None

    return first_line.strip()

def remove_first_line(file):
    with open(file, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(file, 'w') as fout:
        fout.writelines(data[1:])

def append_to_file(line, file):
    with open(file, 'a+') as fout:
        fout.write(line + '\n')

def mark_processed(line, file):
    append_to_file(line, file)

def read_file():
    print(str(datetime.today()) + "\tGetting next url from " + NEW_URL_FILE)
    line = getFirstLine(NEW_URL_FILE)

    if line is None:
        return

    # print("Line: " + line)
    # Now we have the first line, and we can be sure that there is some content in the NEW_URL_FILE
    # Next we can process the url
    splitted = line.split()
    process(splitted[3])

    mark_processed(line, PROCESSING_URL_FILE)

    # .. and last, we can remove the first line of the file
    # Next we can delete the first line of the file
    remove_first_line(NEW_URL_FILE)


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

    return "200 OK\n"

def appendUrl(url):
    line = auth.current_user() + ":\t" + str(datetime.today()) + ":\t" + url + '\n'
    append_to_file(line, NEW_URL_FILE)

scheduler.add_job(read_file, 'cron', second='*/5', max_instances=1, id='foo', replace_existing=True)
print("File reading scheduled")
scheduler.start()

if __name__ == "__main__":
    app.run(ssl_context='adhoc', host='0.0.0.0')

#!/bin/bash

export FLASK_ENV=development
export FLASK_APP=memento_app.py

flask run --cert=adhoc

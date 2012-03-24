#!/usr/bin/env python

import flask

def one():
    return "one!"

def two():
    return "two!"

class Three(object):
    __name__ = "Three"
    def __call__(self):
        return "three!"

class Four(object):
    __name__ = "Four"
    def __call__(self):
        return "four!"
    
app = flask.Flask(__name__)
app.route("/one")(one)
app.route("/two")(two)
app.route("/three")(Three())
app.route("/four")(Four())

if __name__ == "__main__":
    app.run()
#!/usr/bin/env python

import flask

def one():
    '''
        View to do nice things and stuff
        
        .. rest_api::

            [response]
            200: asdflkjasdf
            400: asdflaksdf
            
            [params]
            thing: asdflkjlsadf

    '''
    return "one!"

def two():
    '''
        .. rest_api::
            [response]
            200:

    '''
    return "two!"

class Three(object):
    '''
        .. rest_api::
            [response]
            200:

    '''
    __name__ = "Three"
    requires_things = True
    def __call__(self):
        return "three!"

class Four(object):
    '''
        .. rest_api::
            [response]
            200:

    '''
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
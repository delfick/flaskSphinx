import sys
import os
    
def setup_flask_app(app):
    '''Get flask app from example.app.py'''
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../example'))
    import app
    return app.app

def setup(app):
    '''Connect to setup-flask-app event'''
    app.connect("setup-flask-app", setup_flask_app)

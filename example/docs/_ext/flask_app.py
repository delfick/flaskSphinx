import sys
import os
    
def setup_flask_app(app):
    '''Get flask app from example.app.py'''
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../example'))
    import app
    return app.app

def modify_rest_api(app, route, view, config, api):
    '''Modify api if view is Four, for pure contrived example sake'''
    if view.__name__ == 'Four':
        api['special'] = True
    
def setup(app):
    '''Connect to setup-flask-app and modify-rest-api events'''
    app.connect("setup-flask-app", setup_flask_app)
    app.connect("modify-rest-api", modify_rest_api)

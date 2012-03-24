'''
    Plugin to scrape routes from a flask app
    And display a section for each route
    Using the __doc__ properties on the views they route to
'''
from sphinx.ext.autodoc import prepare_docstring
from sphinx.application import ExtensionError
from docutils.core import publish_doctree
from sphinx.util.compat import Directive
from docutils import nodes

class ShowRoutesDirective(Directive):
    """Directive for outputting routes from a flask app"""
    has_content = True
        
    def run(self):
        '''Create nodes to represent the routes'''
        flask_app = self.get_app()
        if not flask_app:
            return []
        
        # Get rules to document
        rules = self.get_rules(flask_app)
        
        # Add nodes for each rule
        result = []
        for route, view in rules.items():
            result.extend(self.nodes_for_route(route, view))
        
        return result

    def nodes_for_route(self, route, view):
        '''Create nodes for a single route'''
        children = []
        title = nodes.title()
        title += nodes.Text(route)
        
        children.append(title)
        children.extend(self.parse_doc(view.__doc__))
        return children
    
    def parse_doc(self, docstring):
        '''Generate nodes from docstring'''
        string = '\n'.join(prepare_docstring(docstring))
        return self.parse_string(string)
    
    def parse_string(self, string):
        '''Generate nodes from restructured text string'''
        return publish_doctree(string, settings=self.state.document.settings).document.children
    
    def get_app(self):
        '''
            Get the flask app to document
            Will only ever do this once
            Before caching the result for future calls
        '''
        env = self.state.document.settings.env
        if not hasattr(env.config, '_flask_app'):
            apps = env.app.emit("setup-flask-app")
            if not apps:
                raise ExtensionError("No event handlerfor 'setup-flask-app' returned an app")
            
            if len(apps) > 1:
                self.state.document.reporter.warning(
                    "Multiple flask apps returned from 'setup-flask-app' handlers"
                )
            
            env.config._flask_app = apps[0]
        
        return env.config._flask_app
    
    def get_rules(self, app):
        '''Get dictionary of {route:view} from routes of provided app'''
        rules = {}
        for rule in app.url_map.iter_rules():
            rules[rule.rule] = app.view_functions[rule.endpoint]
        return rules

def setup(app):   
    """Setup the show_routes directive""" 
    app.add_directive('show_routes', ShowRoutesDirective)
    app.add_event('setup-flask-app')

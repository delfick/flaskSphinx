'''
    Plugin to scrape routes from a flask app
    And display a section for each route
    Using the __doc__ properties on the views they route to
'''

from sphinx.jinja2glue import BuiltinTemplateLoader
from sphinx.ext.autodoc import prepare_docstring
from sphinx.application import ExtensionError
from sphinx.util.compat import Directive

from jinja2.sandbox import SandboxedEnvironment
from docutils.parsers.rst import directives
from docutils.core import publish_doctree
from docutils import nodes
import os

class ShowRoutesDirective(Directive):
    """Directive for outputting routes from a flask app"""
    has_content = True
    option_spec= {'exclude' : directives.unchanged}
    
    def run(self):
        '''Create nodes to represent the routes'''
        flask_app = self.get_app()
        if not flask_app:
            return []
        
        # Get rules to document
        rules = self.get_rules(flask_app)
        
        # Add nodes for each rule
        result = []
        exclusions = self.options.get('exclude', '').split(',')
        for route, view in rules.items():
            if route not in exclusions:
                result.extend(self.nodes_for_route(route, view))
        
        return result

    def nodes_for_route(self, route, view):
        '''Create nodes for a single route'''
        env = self.state.document.settings.env
        doc = '\n'.join(prepare_docstring(view.__doc__))
        
        # Reset values for rest api and rest config
        env.config._rest_api = None
        env.config._rest_config = None
        
        # Get rest api from possible use of .. rest_api::
        self.parse_string(doc)
        config = env.config._rest_config
        context = env.config._rest_api
        if not context:
            context = {}
        
        # Default view, route and doc in context
        context['doc'] = doc
        context['view'] = view
        context['route'] = route
        
        # Use event to add any other context for the template
        env.app.emit('modify-rest-api', route, view, config, context)
        
        # Get template and render restructured text using context
        template_env = self.get_template_env()
        template = template_env.get_template("rest_api/default.rst")
        string = template.render(api=context)
        
        # Return nodes from parsing the restructured text
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
    
    def get_template_env(self):
        '''Create jinja template environment'''
        env = self.state.document.settings.env
        current_dir = os.path.dirname(__file__)
        template_dirs = [os.path.join(current_dir, 'flaskSphinx_templates'), current_dir]
        template_loader = BuiltinTemplateLoader()
        template_loader.init(env.app.builder, dirs=template_dirs)
        return SandboxedEnvironment(loader=template_loader)

def setup(app):   
    """Setup the show_routes directive""" 
    app.add_directive('show_routes', ShowRoutesDirective)
    app.add_event('setup-flask-app')
    app.add_event('modify-rest-api')

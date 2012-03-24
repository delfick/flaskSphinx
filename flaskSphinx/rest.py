'''
    Plugin to format specification of a Restful API
'''

from sphinx.jinja2glue import BuiltinTemplateLoader
from sphinx.util.compat import Directive

from docutils.core import publish_doctree
from docutils import nodes

from jinja2.sandbox import SandboxedEnvironment
import ConfigParser
import cStringIO
import os

class RestApiDirective(Directive):
    """Directive for outputting restful APIs"""
    has_content = True

    def run(self):
        '''Create nodes to represent the rest options'''
        
        # Get REST options from data given to directive
        try:
            config = self.get_config('\n'.join(self.content.data))
        except ConfigParser.ParsingError, e:
            self.state.document.reporter.warning(e)
            return []
        
        # Get options to pass to template
        api = self.get_api(config)
        
        # Get template and render resturctured text using api
        template_env = self.get_template_env()
        template = template_env.get_template("rest_api/default.rst")
        string = template.render(api=api)
        
        # Return nodes from parsing the restructured text
        return publish_doctree(string, settings=self.state.document.settings).document.children
    
    def get_api(self, config):
        return {'sections' : config.sections()}
    
    def get_config(self, data):
        '''Create object to represent all the provided REST options'''
        config = ConfigParser.ConfigParser()
        config.readfp(cStringIO.StringIO(str(data)))
        return config
    
    def get_template_env(self):
        '''Create jinja template environment'''
        env = self.state.document.settings.env
        current_dir = os.path.dirname(__file__)
        template_dirs = [os.path.join(current_dir, 'flaskSphinx_templates'), current_dir]
        template_loader = BuiltinTemplateLoader()
        template_loader.init(env.app.builder, dirs=template_dirs)
        return SandboxedEnvironment(loader=template_loader)
        
def setup(app):
    """Setup the rest_api directive""" 
    app.add_directive('rest_api', RestApiDirective)

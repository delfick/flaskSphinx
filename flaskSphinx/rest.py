'''
    Plugin to gather rest options from a docstring
    Will put options onto env._rest_api
    And output no nodes
'''

from docutils.core import publish_doctree
from sphinx.util.compat import Directive
from docutils import nodes
import ConfigParser
import cStringIO

class RestApiDirective(Directive):
    """Directive for outputting restful APIs"""
    has_content = True

    def run(self):
        '''Create nodes to represent the rest options'''
        env = self.state.document.settings.env
        
        # Get REST options from data given to directive
        try:
            config = self.get_config('\n'.join(self.content.data))
        except ConfigParser.ParsingError, e:
            self.state.document.reporter.warning(e)
            return []
        
        # Get options and put it on env
        # Used by flaskSphinx.routes plugin
        env.config._rest_api = self.get_api(config)
        env.config._rest_config = config
        return []
    
    def get_api(self, config):
        '''Get a dictionary of options from the ini config'''
        return {'sections' : config.sections()}
    
    def get_config(self, data):
        '''Create object to represent all the provided REST options'''
        config = ConfigParser.ConfigParser()
        config.readfp(cStringIO.StringIO(str(data)))
        return config
        
def setup(app):
    """Setup the rest_api directive"""
    app.add_directive('rest_api', RestApiDirective)

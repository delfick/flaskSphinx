'''
    Plugin to format specification of a Restful API
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
        
        # Get REST options from data given to directive
        try:
            config = self.get_config('\n'.join(self.content.data))
        except ConfigParser.ParsingError, e:
            self.state.document.reporter.warning(e)
            return []
        
        # Create restructured text from REST options
        string = self.transform(config)
        
        # Return nodes from parsing the restructured text
        return publish_doctree(string, settings=self.state.document.settings).document.children
    
    def get_config(self, data):
        '''Create object to represent all the provided REST options'''
        config = ConfigParser.ConfigParser()
        config.readfp(cStringIO.StringIO(str(data)))
        return config
    
    def transform(self, config):
        '''Transform REST options into restructured text'''
        return '\n\n'.join('``%s``' % section for section in config.sections())
        
def setup(app):
    """Setup the rest_api directive""" 
    app.add_directive('rest_api', RestApiDirective)

'''
    Plugin to format specification of a Restful API
'''

from sphinx.util.compat import Directive

class RestApiDirective(Directive):
    """Directive for outputting restful APIs"""
    has_content = True

    def run(self):
        return []
        
def setup(app):   
    """Setup the rest_api directive""" 
    app.add_directive('rest_api', RestApiDirective)

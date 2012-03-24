'''
    Plugin to scrape routes from a flask app
    And display a section for each route
    Using the __doc__ properties on the views they route to
'''

from sphinx.util.compat import Directive

class ShowRoutesDirective(Directive):
    """Directive for outputting routes from a flask app"""
    has_content = True

    def run(self):
        return []
        
def setup(app):   
    """Setup the show_routes directive""" 
    app.add_directive('show_routes', ShowRoutesDirective)

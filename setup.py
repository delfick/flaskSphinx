from setuptools import setup

setup(
      name = 'flaskSphinx'
    , version = "0.1"
    , classifiers = [
        'Intended Audience :: Developers'
      , 'Programming Language :: Python'
      , 'Topic :: Software Development :: Documentation'
      ]
                   
    , keywords='flask sphinx directive'
    , author = 'Stephen Moore'
    , author_email = 'stephen@delfick.com'
    , license = 'GPL'
    , url = "https://github.com/delfick/flaskSphinx"

    , description = 'Sphinx plugins to make it easier to generate documentation for a flask project'
    , install_requires = ['sphinx', 'flask']
                          
    , packages = ['flaskSphinx']
)

# -*- coding: utf-8 -*-
#

import sys, os
sys.path.insert(0, os.path.abspath('../..'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest']
templates_path = []
source_suffix = '.rst'
master_doc = 'index'

project = 'fyplot'
copyright = '(C) 2020, Max Planck Gesellschaft'

with open(os.path.join(os.path.dirname(__file__),"..", "..", 'VERSION')) as fd:
    VERSION = fd.readline().strip()
version = VERSION
release = VERSION

exclude_trees = ['build']
pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_theme_options = {}

html_static_path = []
htmlhelp_basename = 'fyplotdoc'

latex_documents = [
  ('index', 'fyplot.tex', ur'Fyplot Documentation',
   ur'Vincent Berenz', 'manual'),
]

def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip

def setup(app):
    app.connect("autodoc-skip-member", skip)

autoclass_content = 'both'

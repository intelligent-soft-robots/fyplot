from setuptools import setup,find_packages
import sys
from os import path

with open(path.join(path.dirname(__file__), 'VERSION')) as v:
        VERSION = v.readline().strip()
        
setup(name = "fyplot",
      packages=find_packages('.'),
      version = VERSION,
      description="minimal interface for dynamic time plotting",
      url="https://github.com/intelligent-soft-robots/fyplot",
      long_description="see https://fyplot.readthedocs.io/en/latest/",
      author="Vincent Berenz",
      author_email="vberenz@tuebingen.mpg.de",
      scripts=['bin/fyplot_demo'],
      install_requires = ["pyqtgraph"]
)


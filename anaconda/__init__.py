"""
A Python3 reference application.
"""


from flask import Flask


__version__ = '0.1.0'


application = Flask(__name__)


import anaconda.views

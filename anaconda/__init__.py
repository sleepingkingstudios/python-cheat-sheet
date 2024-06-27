"""
A Python3 reference application.
"""


from flask import Flask, render_template
from markupsafe import Markup

from .utils.render_utils import render_markdown


__version__ = '0.1.0'


def create_app(injected_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if injected_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(injected_config)

    @app.context_processor
    def markdown_processor():
        return dict(render_markdown=render_markdown)

    @app.context_processor
    def template_processor():
        def unsafe_render_template(template_name, **context):
            return Markup(render_template(template_name, **context))

        return dict(render_template=unsafe_render_template)

    from . import python_doc
    app.register_blueprint(python_doc.blueprint)

    return app

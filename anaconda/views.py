from flask import render_template
from markupsafe import Markup

from anaconda import application
from anaconda.utils.render_utils import render_markdown, render_page


@application.context_processor
def markdown_processor():
    return dict(render_markdown=render_markdown)


@application.context_processor
def template_processor():
    def unsafe_render_template(template_name, **context):
        return Markup(render_template(template_name, **context))

    return dict(render_template=unsafe_render_template)


@application.route('/')
def index():
    return render_page('index.md')

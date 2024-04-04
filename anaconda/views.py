from flask import render_template
from anaconda import application
from anaconda.utils import render_markdown


@application.context_processor
def markdown_processor():
    return dict(render_markdown=render_markdown)


@application.context_processor
def template_processor():
    return dict(render_template=render_template)


@application.route('/')
def index():
    return render_template('index.html')

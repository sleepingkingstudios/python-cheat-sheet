from flask import Blueprint

from .utils.render_utils import render_page


blueprint = Blueprint('python_doc', __name__)


@blueprint.get('/')
def index():
    return render_page('python_doc/overview.md')


@blueprint.get('/functions')
def functions():
    return render_page('python_doc/functions.md')


@blueprint.get('/syntax')
def syntax():
    return render_page('python_doc/syntax.md')

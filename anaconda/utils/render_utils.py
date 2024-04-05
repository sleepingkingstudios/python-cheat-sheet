from typing import Any
from bs4 import BeautifulSoup
from flask import render_template
from markdown import markdown
from markupsafe import Markup

from anaconda.utils.html_utils import add_header_ids


def _post_process_markdown(fragment: BeautifulSoup) -> BeautifulSoup:
    fragment = add_header_ids(fragment)

    return fragment


def parse_markdown(template_name: str, **context: Any) -> BeautifulSoup:
    """
    Renders a Markdown file to intermediate HTML.

    Arguments:
        template_name (str): The name of the template to render.
        context: The variables to make available in the template.

    Returns:
        BeautifulSoup: The intermediate HTML representation.
    """
    raw_text = render_template(template_name, **context)
    rendered = markdown(raw_text)
    fragment = BeautifulSoup(rendered, features="html.parser")
    fragment = _post_process_markdown(fragment)

    return fragment


def render_markdown(template_name: str, **context: Any) -> Markup:
    """
    Renders a Markdown file to HTML with Jinja2 template support.

    Arguments:
        template_name (str): The name of the template to render.
        context: The variables to make available in the template.

    Returns:
        Markup: The generated HTML.
    """
    return Markup(parse_markdown(template_name, **context))

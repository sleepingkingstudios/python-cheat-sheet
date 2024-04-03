from typing import Any
from flask import render_template
from markdown import markdown
from markupsafe import Markup


def render_markdown(template_name: str, **context: Any) -> Markup:
    """
    Renders a Markdown file to HTML with Jinja2 template support.

    Arguments:
        template_name (str): The name of the template to render.
        context: The variables to make available in the template.

    Returns:
        Markup: The generated HTML.
    """
    raw_text = render_template(template_name, **context)
    rendered = markdown(raw_text)

    return Markup(rendered)

from re import split, sub
from typing import Any
from flask import render_template
from markdown import markdown
from markupsafe import Markup
from bs4 import BeautifulSoup


__HEADING_TAGS__ = ['h1', 'h2', 'h3', 'h4', 'h5', 'g6']


def __kebab_case_word__(word: str) -> str:
    normal = sub(r'[^\w]+', '', word)
    chars = (f'-{char.lower()}' if char.isupper() else char for char in normal)

    return sub(r'^-', '', ''.join(chars))


def kebab_case(string: str) -> str:
    """
    Converts a string to kebab-case.

    First, separates the string into words. Then, for each word:

    - Normalizes the word by removing non-letter, non-digit characters.
    - Replaces any uppercase characters with the lowercase letter
      preceded by a dash.
    - Trims a leading dash, if any.

    Finally, joins the words with dash characters.

    Arguments:
        string (str): The input to process.

    Returns:
        str: The input string in kebab-case.
    """
    words = split(r'[ \-_]', string)
    words = (__kebab_case_word__(word) for word in words)

    return '-'.join(words)


def __add_header_ids__(fragment: BeautifulSoup) -> BeautifulSoup:
    """
    Adds auto-generated id attributes to header tags.

    Arguments:
        fragment (BeautifulSoup): The HTML to process.

    Returns:
        BeautifulSoup: The processed HTML.
    """
    for heading_tag in __HEADING_TAGS__:
        for tag in fragment.find_all(heading_tag):
            tag.attrs['id'] = __kebab_case_word__(tag.text)

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
    raw_text = render_template(template_name, **context)
    rendered = markdown(raw_text)
    fragment = BeautifulSoup(rendered, features="html.parser")
    fragment = __add_header_ids__(fragment)

    return Markup(fragment)

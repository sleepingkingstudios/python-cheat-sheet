from re import split, sub, template
from typing import Any
from flask import render_template
from markdown import markdown
from markupsafe import Markup
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

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


def __get_parent_children__(headings: list, heading_level: int) -> list:
    children = headings

    for _ in range(1, heading_level):
        if len(children) == 0:
            return children

        children = children[-1]['children']

    return children


def __parse_heading_tag__(element: PageElement) -> bool:
    if not isinstance(element, Tag):
        return False

    if element.name == 'h1':
        return False

    return element.name in __HEADING_TAGS__


def parse_headings(fragment: BeautifulSoup) -> list:
    headings = []

    for element in fragment.children:
        if not __parse_heading_tag__(element):
            continue

        # Only generate headings for h2-h6 tags.
        heading_level = __HEADING_TAGS__.index(element.name)
        heading = {
            'label': element.text,
            'url': f"#{element.attrs['id']}",
            'children': []
        }
        children = __get_parent_children__(headings, heading_level)
        children.append(heading)

    return headings


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
    fragment = __add_header_ids__(fragment)

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

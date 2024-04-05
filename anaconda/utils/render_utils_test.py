import pytest
from inspect import cleandoc
from bs4 import BeautifulSoup
from jinja2 import TemplateNotFound
from markupsafe import Markup

from anaconda import application
from anaconda.utils.render_utils import parse_markdown, render_markdown


@pytest.fixture
def with_app_context():
    with application.app_context():
        yield


class TestParseMarkdown:
    def test_invalid_template(self, with_app_context):
        with pytest.raises(TemplateNotFound):
            parse_markdown('invalid_template.md')

    def test_empty_template(self, with_app_context):
        fragment = parse_markdown('mocks/empty_template.md')

        assert type(fragment) is BeautifulSoup
        assert str(fragment) == ''

    def test_markdown_template(self, with_app_context):
        fragment = parse_markdown(
            'mocks/markdown_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <p>You have been recruited by the Star League to defend the
            frontier against Xur and the Ko-Dan Armada.</p>
            """
        )

        assert type(fragment) is BeautifulSoup
        assert str(fragment) == expected


class TestRenderMarkdown:
    def test_invalid_template(self, with_app_context):
        with pytest.raises(TemplateNotFound):
            render_markdown('invalid_template.md')

    def test_empty_template(self, with_app_context):
        rendered = render_markdown('mocks/empty_template.md')

        assert type(rendered) is Markup
        assert rendered == ''

    def test_markdown_template(self, with_app_context):
        rendered = render_markdown(
            'mocks/markdown_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <p>You have been recruited by the Star League to defend the
            frontier against Xur and the Ko-Dan Armada.</p>
            """
        )

        assert type(rendered) is Markup
        assert rendered == expected

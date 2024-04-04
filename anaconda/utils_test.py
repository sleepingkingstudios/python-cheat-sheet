import pytest
from inspect import cleandoc
from jinja2 import TemplateNotFound
from markupsafe import Markup
from bs4 import BeautifulSoup

from anaconda import application
from anaconda.utils import kebab_case, parse_headings, render_markdown


@pytest.fixture
def with_app_context():
    with application.app_context():
        yield


class TestKebabCase:
    def test_empty_string(self):
        assert kebab_case('') == ''

    def test_lowercase_string(self):
        assert kebab_case('lowercase') == 'lowercase'

    def test_capitalized_string(self):
        assert kebab_case('Capitalized') == 'capitalized'

    def test_camel_case_string(self):
        assert kebab_case('CamelCase') == 'camel-case'

    def test_kebab_case_string(self):
        assert kebab_case('kebab-case') == 'kebab-case'

    def test_snake_case_string(self):
        assert kebab_case('snake_case') == 'snake-case'

    def test_string_with_punctuation(self):
        assert kebab_case('Greetings, Programs!') == 'greetings-programs'


class TestParseHeadings:
    def test_empty_string(self):
        raw_html = ''
        fragment = BeautifulSoup(raw_html)

        assert parse_headings(fragment) == []

    def test_html_without_headings(self):
        raw_html = cleandoc(
            """
            <p><strong>Fake Heading</strong></p>

            <p>Real paragraph.</p>
            """
        )
        fragment = BeautifulSoup(raw_html, features="html.parser")

        assert parse_headings(fragment) == []

    def test_html_with_flat_headings(self):
        raw_html = cleandoc(
            """
            <h1 id="top-heading">Top Heading</h1>

            <p>Introductory paragraph.</p>

            <h2 id="middle-heading">Middle Heading</h2>

            <p>Middle paragraph.</p>

            <h2 id="final-heading">Final Heading</h2>

            <p>Final paragraph.</p>
            """
        )
        fragment = BeautifulSoup(raw_html, features="html.parser")
        expected = [
            {
                'label': 'Middle Heading',
                'url': '#middle-heading',
                'children': [],
            },
            {
                'label': 'Final Heading',
                'url': '#final-heading',
                'children': [],
            },
        ]

        assert parse_headings(fragment) == expected

    def test_html_with_nested_headings(self):
        raw_html = cleandoc(
            """
            <h1 id="top-heading">Top Heading</h1>

            <p>Introductory paragraph.</p>

            <h2 id="middle-heading">Middle Heading</h2>

            <p>Middle paragraph.</p>

            <h3 id="inner-heading">Inner Heading</h3>

            <p>Inner paragraph.</p>

            <h3 id="another-inner-heading">Another Inner Heading</h3>

            <p>Another inner paragraph.</p>

            <h4 id="nested-heading">Nested Heading</h4>

            <p>Nested paragraph.</p>

            <h2 id="final-heading">Final Heading</h2>

            <p>Final paragraph.</p>
            """
        )
        fragment = BeautifulSoup(raw_html, features="html.parser")
        expected = [
            {
                'label': 'Middle Heading',
                'url': '#middle-heading',
                'children': [
                    {
                        'label': 'Inner Heading',
                        'url': '#inner-heading',
                        'children': [],
                    },
                    {
                        'label': 'Another Inner Heading',
                        'url': '#another-inner-heading',
                        'children': [
                            {
                                'label': 'Nested Heading',
                                'url': '#nested-heading',
                                'children': [],
                            },
                        ],
                    },
                ],
            },
            {
                'label': 'Final Heading',
                'url': '#final-heading',
                'children': [],
            },
        ]

        assert parse_headings(fragment) == expected


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

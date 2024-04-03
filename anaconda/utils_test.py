import pytest
from inspect import cleandoc
from jinja2 import TemplateNotFound
from markupsafe import Markup
from bs4 import BeautifulSoup

from anaconda import application
from anaconda.utils import kebab_case, render_markdown


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

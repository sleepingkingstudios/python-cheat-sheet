import pytest
from inspect import cleandoc
from jinja2 import TemplateNotFound
from markupsafe import Markup

from anaconda import application
from anaconda.utils import render_markdown


@pytest.fixture
def with_app_context():
    with application.app_context():
        yield


class TestRenderMarkdown:
    def test_invalid_template(self, with_app_context):
        with pytest.raises(TemplateNotFound):
            render_markdown('invalid_template.md')

    def test_empty_template(self, with_app_context):
        rendered = render_markdown('mocks/empty_template.md')

        assert type(rendered) == Markup
        assert rendered == ''

    def test_markdown_template(self, with_app_context):
        rendered = render_markdown(
            'mocks/markdown_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1>Greetings, Starfighter!</h1>
            <p>You have been recruited by the Star League to defend the frontier against
            Xur and the Ko-Dan Armada.</p>
            """
        )

        assert type(rendered) == Markup
        assert rendered == expected

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

    def test_code_block_template(self, with_app_context):
        fragment = parse_markdown(
            'mocks/code_block_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <pre><code>recruiter = 'Star League'
            defend = 'the frontier'
            enemies = 'Xur and the Ko-Dan Armada'</code></pre>
            """
        )

        assert type(fragment) is BeautifulSoup
        assert str(fragment) == expected

    def test_highlighted_code_block_template(self, with_app_context):
        fragment = parse_markdown(
            'mocks/highlighted_code_block_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <div class="highlight"><pre><span></span><span class="n">recruiter</span> <span class="o">=</span> <span class="s1">'Star League'</span>
            <span class="n">defend</span> <span class="o">=</span> <span class="s1">'the frontier'</span>
            <span class="n">enemies</span> <span class="o">=</span> <span class="s1">'Xur and the Ko-Dan Armada'</span>
            </pre></div>
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

    def test_code_block_template(self, with_app_context):
        rendered = render_markdown(
            'mocks/code_block_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <pre><code>recruiter = 'Star League'
            defend = 'the frontier'
            enemies = 'Xur and the Ko-Dan Armada'</code></pre>
            """
        )

        assert type(rendered) is Markup
        assert rendered == expected

    def test_highlighted_code_block_template(self, with_app_context):
        rendered = render_markdown(
            'mocks/highlighted_code_block_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <div class="highlight"><pre><span></span><span class="n">recruiter</span> <span class="o">=</span> <span class="s1">'Star League'</span>
            <span class="n">defend</span> <span class="o">=</span> <span class="s1">'the frontier'</span>
            <span class="n">enemies</span> <span class="o">=</span> <span class="s1">'Xur and the Ko-Dan Armada'</span>
            </pre></div>
            """
        )

        assert type(rendered) is Markup
        assert rendered == expected

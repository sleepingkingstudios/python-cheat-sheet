# Flask

Flask is a micro framework for developing web applications.

<dl>
  <dt>Activate The Virtual Environment</dt>
  <dd><code>. .venv/bin/activate</code></dd>

  <dt>Install Dependencies</dt>
  <dd><code>pip install -e .</code></dd>

  <dt>Run The Application</dt>
  <dd><code>flask --app application_name run --port=3000 --debug</code></dd>
</dl>

Note that the default port is 5000, which conflicts with Airdrop services on macOS devices.

## Getting Started

To create a Flask application, start by creating a directory and setting up a [virtual environment]({{url_for('python_doc.index')}}#virtual-environments) and `git` repository.

The application directory should include the following:

- `application_name/`: A Python package containing the application code.
    - `application_name/static/`: A directory for static files, such as assets.
    - `application_name/templates/`: A directory for [templates](#templates).
    - `application_name/__init__.py`: The entry point for the application.
- `tests/`: A directory for test modules.
- `.gitignore`
- `README.md`
- `pyproject.toml`: The configuration file for the application.

In order to install dependencies, the `__init__.py` entry point file must have, at a minimum, a [docstring]({{url_for('python_doc.syntax')}}#docstrings) and a `__version__` constant for the package.

### Configuration File

The [configuration file]({{url_for('python_doc.index')}}#configuration-files) should define the project dependencies and metadata.

```toml
[project]
name = "application_name"
dependencies = [
    "flask >=3.0,<4",
]
dynamic = ["version", "description"]

[project.optional-dependencies]
test = [
    "flake8 >=7,<8",
    "pytest >=8.1,<9",
]

[build-system]
requires = ["flit_core<4"]
build-backend = "flit_core.buildapi"
```

## The Application Factory

The Flask application should be defined in `__init__.py` by defining a `create_app` function that returns an application instance.

```python
from flask import Flask


def create_app(injected_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if injected_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(injected_config)

    # Application views, configuration will be defined here.
    @app.route('/')
    def index():
        return 'Greetings, programs!'

    return app
```

## Blueprints

Blueprints provide a mechanism for organizing a Flask application. Each Blueprint can define its own views, templates, and static files.

```python
# In application_name/authentication.py
from flask import Blueprint

blueprint = Blueprint('authentication', __name__, url_prefix='/session')

# Defines a route at `/session/login`.
@blueprint.route('/login')
def login():
    pass
```

Once the blueprint is defined, it can be included in the application using `register_blueprint`:

```python
# In application_name/__init__.py
def create_app():
    # ...

    from . import authentication
    app.register_blueprint(auth.bp)
```

Blueprints take the following options:

<dl>
  <dt><code>url_prefix</code></dt>
  <dd>
    Sets the URL prefix for views defined in the blueprint.
  </dd>
</dl>

## Views

Flask handles requests using view functions, which can be defined either on a blueprint or directly on the application.

```python
@application.route('/hello')
def hello():
    return 'Greetings, programs!'
```

In the above example, the `route()` decorator is used to register the view (see [#routes](routes), below). When a user navigates to the `/hello` URL, the application calls the `hello()` function, and returns to the browser the value returned by the function.

The name associated with a view is also called the endpoint, and is used by the `url_for()` function to map a name and arguments to an application URL. If the view is defined on a blueprint, the name of the blueprint is prepended to the endpoint. For example, a `/register` route defined on a blueprint with prefix `/authentication` would have an endpoint of `authentication.register`.

### Routes

Functions are associated with URLs using the `route()` decorator. If defined directly on an application, the corresponding function is called when a browser requests the matching value. If defined on a blueprint with a `url_prefix`, the prefix will be prepended to the route. For example, a `/register` route defined on a blueprint with prefix `/authentication` would match requests to `/authentication/register`.

By default, routes will only match `GET` requests. Passing a `tuple` to the `methods` parameter will allow a route to match multiple HTTP methods. The method used for each request can be accessed using `request.method`.

```python
@application.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'GET':
        pass
    else:
        pass
```

Routes with the same URL but different HTTP methods can also be defined using different functions. Flask defines helpers for defining routes for common HTTP methods, such as `get()` and `post()`.

```python
@application.get('/search'):
def get_search():
    pass

@application.post('/search'):
def post_search():
    pass
```

Routes can include wildcards in the url:

```python
@application.get('/widgets/<widget_id>')
def get_widget(widget_id):
    pass
```

Routes can also be combined while referencing the same view function:

```python
@application.get('/greet')
@application.get('/greet/<name>')
def greet(name=None):
    pass
```

### Requests

Request parameters can be accessed using the `flask.request` object:

```python
from flask import request

@application.route('/greet')
def greet():
    name = request.form['name']

    return f"Greetings, {name}"
```

See [flask.Request](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request) for more information.

<!-- ### Sessions -->

<!-- ### The Context Object -->

## Templates

Flask includes the [Jinja2 template engine](https://palletsprojects.com/p/jinja/). To render a template, use the `flask.render_template()` function.

```python
from flask import render_template

@application.get('/overview')
def overview:
    return render_template('overview.html', full_details=True)
```

Any additional parameters are passed to the template engine. The template also has access to the application `config` object, the [request](#requests) object, the `session` object, the `g` context object, and the `url_for` and `get_flashed_messages` functions. Values written to a template are automatically HTML escaped. Use the `markupsafe.Markup` class to avoid escaping a variable.

Templates must be defined in the application's template directory, located at `/application_name/templates`. For example, the `overview` template above should be defined at `/application_name/templates/overview.html`.

### Template Inheritance

Jinja supports template inheritance, which uses `extends` and `block` tags to combine multiple templates. See [the Flask docs](https://flask.palletsprojects.com/en/3.0.x/patterns/templateinheritance/) for more information.

### Static Files

Static files such as CSS and JavaScript assets can be stored in the `/application_name/static` directory in development, and referenced using the special `'static'` endpoint. For example, the `style.css` file should be stored at `/application_name/static/style.css` and can be referenced using `url_for('static', name='style.css')`.

<!-- ## Configuration -->

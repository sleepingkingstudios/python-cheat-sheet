# Overview

## Command Line

<dl>
  <dt>Open A REPL</dt>
  <dd><code>python3</code></dd>
</dl>

<dl>
  <dt>Run A Script</dt>
  <dd><code>python3 some_file.py</code></dd>
</dl>

### Virtual Environments

The
<a href="https://docs.python.org/3/library/venv.html" target="_blank">venv</a>
module provides Python support for lightweight "virtual environments", which allow projects to isolate their dependencies from other projects. Virtual environments must be *activated* to correctly stub the environment. Virtual environments are not portable; if the directory is moved, the virtual environment must be recreated.

<dl>
  <dt>Create A Virtual Environment</dt>
  <dd><code>python3 -m venv .venv</code></dd>

  <dt>Activate A Virtual Environment</dt>
  <dd><code>. .venv/bin/activate</code></dd>

  <dt>Deactivate A Virtual Environment</dt>
  <dd><code>deactivate</code></dd>
</dl>

## Conventions

The generally accepted Python conventions are documented in [PEP 8](https://peps.python.org/pep-0008/).

The `pycodestyle` module can lint a python file from the command line.

<dl>
  <dt>Lint A File</dt>
  <dd>`pycodestyle file_name.py</dd>

  <dt>Lint All Files In A Directory</dt>
  <dd>`pycodestyle path/to/directory</dd>
</dl>

Python prefers 4 spaces per tab, with a maximum line length of 79 (for code) and 72 (for <a href="{{ url_for('python_doc.syntax') }}#docstrings">docstrings</a>).

Surround top-level function and class definitions with two blank lines. Method definitions inside a class are surrounded by a single blank line.

A few specific reminders:

- Inline comments should be preceded by two spaces: `foo = "bar"  # Assigns foo`.
- Do not use whitespace inside brackets: `{eggs: 2}` instead of `{ eggs: 2 }`.
- Do not use spaces around `=` for function parameters or keyword arguments.
- Be consistent with function `return`s. If a function returns a value in one branch, it should return a value in all branches, using `return None`, rather than a bare `return`.

### Naming

Module names (and therefore file names) should be in `snake_case`, e.g. `example_module.py`.

Constant and variable names **must** be a combination of upper-case (`A-Z`) and lower-case (`a-z`) letters, digits (`0-9`), and underscores (`_`), and **must not** start with a digit. Variable names are case-sensitive.

Variables and functions should use `snake_case`.

```python
user_name = 'Alan Bradley'

def full_name(first_name, last_name):
    pass
```

Constants should use `UPPER_SNAKE_CASE`.

```python
DEFAULT_GREETING = 'Greetings, programs!'
```

By convention, private variable, function, and constant names should be wrapped in double underscores.

```python
__private_variable__ = 'secret'

__PRIVATE_CONSTANT__ = '12345'

def __private_function__():
    pass
```

Private module functions may be prefixed by one or two underscores. Class protected variables and methods can be prefixed with one underscore. Private class variables and methods are prefixed with two underscores, and protected via name mangling. Finally, "magic" or "dunder" class methods (such as the constructor method `__init__`) must be wrapped in double underscores.

## Program Structure

Each Python file defines a module and can contain both definitions and statements, such as variables, functions, and classes. Modules can be imported and used in other Python files using the `import` statement.

When the file is run directly (as opposed to being imported by another file), the value of the `__name__` variable is set to `"__main__"`. By convention, executable Python files define a `main()` function, which is executed only `if __name__ == "__main__"`.

```python
def main():
    print('Greetings, programs!')


if __name_ == '__main__':
    main()
```

### Imports

Python code is shared between files using the `import` keyword. Using a bare `import` adds the module to the local scope by name.

```python
import math

math.ceil(0.5)  # returns 1
math.floor(0.5)  # returns 0
```

To import specific definitions from a module, use the `from`...`import` syntax. This adds the definitions to the local scope directly.

```python
from math import ceil, floor

ceil(0.5)  # returns 1
floor(0.5)  # returns 0
```

Long import statements can be broken up using parentheses.

```python
from my_package.my_namespace.my_custom_module import (
    my_method_with_long_name,
    my_variable_with_long_name,
)
```

By default, imports are absolute, i.e. relative to the top-level directory. Python also supports relative imports (using the `from`...`import` syntax) only. A single leading dot indicates a relative import, starting with the current package. Two or more leading dots indicate a relative import to the parent(s) of the current package, one level per dot after the first.

```python
from . import sibling_module
from .sibling_module import sibling_function

from .sibling_module import nibling_module
from .sibling_module.nibling_module import nibling_function

from .. import auncle_module
from ..auncle_module import auncle_function

from ..auncle_module import cousin_module
from ..auncle_module.cousin_module import cousin_function
```

Imports can also be aliased using the `as` keyword.

```python
import random as rand
from random import randint as random_integer, choice as pick
```

### Builtin Modules

Python also defines a set of builtin modules as part of the <a href="https://docs.python.org/3/library/" target="_blank">Python Standard Library</a>. These include:

- <a href="https://docs.python.org/3/library/copy.html" target="_blank">copy</a>: Shallow and deep copy operations.
- <a href="https://docs.python.org/3/library/math.html" target="_blank">math</a>: Mathematical functions.
- <a href="https://docs.python.org/3/library/random.html" target="_blank">random</a>: Generate pseudo-random numbers.
- <a href="https://docs.python.org/3/library/re.html" target="_blank">re</a>: Regular expression operations.

Builtin modules can be imported by name.

```python
import copy
from math import ceil, floor
```

### Packages

Python uses packages to group modules together into a single namespace. Each package is defined by a directory with an `__init__.py` file, which serves as the entry point for the package. (The `__init__.py` file is required for Python to treat the directory as a package, but can be empty.) Packages can also be nested inside one another.

```
magic/
    __init__.py
    mana.py
    schools.py
    potions/
        __init.py
        potion_of_healing.py
    spells/
        __init__.py
        magic_missile.py
```

Packages can be imported by Python files. The dot `.` character is used to import from modules within a package (or a nested package); otherwise, the contents of `__init__.py` for that package are imported.

```python
import magic  # imports from magic/__init__.py

import magic.schools  # imports from magic/schools.py

import magic.potions  # imports from magic/potions/__init__.py

import magic.potions.potion_of_healing  # imports from magic/potions/potion_of_healing.py
```

Packages can also be imported using the `import`...`from` syntax.

```python
# Imports potion_of_healing from magic/potions/__init__.py
from magic.potions import potion_of_healing
```

### Package Managers

Python also has support for external packages from sources such as the <a href="https://pypi.org/" target="_blank">Python Package Index</a>. Python uses `pip` to install packages within a [Virtual Environment](#virtual-environments), or `brew` (on macOS) to install packages globally.

<dl>
  <dt>Install A Package</dt>
  <dd><code>pip install pygments</code></dd>

  <dt>Update A Package</dt>
  <dd><code>python3 -m pip install -U pygments</code></dd>
</dl>

### Configuration Files

Python projects use a `pyproject.toml` configuration file to configure tools such as linters and build tools. See [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).

The `[project]` table defines metadata for the project, including dependencies:

```
[project]
name = "anaconda"
dependencies = [
    "flask >=3.0,<4",
    "beautifulsoup4 >=4.12,<5",
    "markdown >=3.6,<4",
    "pygments >2.17,<3",
]
```

Optional dependencies can be specified using the `[project.optional-dependencies]` table:

```
[project.optional-dependencies]
test = [
    "flake8 >=7,<8",
    "pytest >=8.1,<9",
]
```

For projects with a build tool, the `[build-system]` table specifies and configures the build tool:

```
[build-system]
requires = ["flit_core<4"]
build-backend = "flit_core.buildapi"
```

## Reflection

Python has a number of ways to reflect on a class, module, function, or object.

The `dir` method lists the properties defined for a module. The module must be `import`ed first, or a `NameError` will be raised.

```python
import re
dir(re)
# ['A', 'ASCII', 'DEBUG', 'DOTALL', 'I', 'IGNORECASE', 'L', 'LOCALE', 'M', ...]
```

The `help` method displays the documentation for a module, function or object:

```python
help(1)
# Help on int object:
#
# class int(object)
# ...
```

The documentation can also be accessed in raw form as the `__doc__` property.

The `__name__` property returns the name of a class, module, or function.

```python
def add(a, b):
    return a + b


add.__name__
# add
```

## Debugging

Python has a built-in debugger.

```python
import pdb


def run_debugger():
    value = 'a string'

    pdb.set_trace()

    return value.upper()


print(run_debugger())
```

The debugger will print the location of the `set_trace()` call as well as the *next* line of code (ignoring empty lines) and start a REPL. Any values that are in scope will be available to the debugger:

```
> python3 example_file.py
-> return value.upper()
(pdb) value
'a string'
(pdb) c
A STRING
```

Common PDB commands include:

- `l` or `list`: prints the lines surrounding the `set_trace()` call.
- `n` or `next`: steps to the next line.
- `p` or `print`: same as the built-in `print()` function.
- `c` or `continue`: exits the debugger.


# Python Reference Sheet

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
  <dd><code>python3 -m venv /path/to/new/virtual/environment</code></dd>

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

Python prefers 4 spaces per tab, with a maximum line length of 79 (for code) and 72 (for [docstrings](#docstrings)).

A program is structured as a [module](#modules) with a defined `main()` function. When a Python file is run directly, the special variable `__name__` is set to `"__main__"`. Therefore, it's common to have the boilerplate `if __name__ ==` to call a `main()` function when the module is run directly, but not when the module is imported by some other module.

<pre><code>def main():
    print('Greetings, programs!')


if __name_ == '__main__':
    main()
</code></pre>

A few specific reminders:

- Do not use whitespace inside brackets: `{eggs: 2}` instead of `{ eggs: 2 }`.
- Do not use spaces around `=` for function parameters or keyword arguments.
- Be consistent with function `return`s. If a function returns a value in one branch, it should return a value in all branches, using `return None`, rather than a bare `return`.

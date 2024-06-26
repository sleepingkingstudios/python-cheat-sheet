# Functions

A Python function is defined using the `def` keyword:

```python
def greet(name):
    """
    Prints a greeting.
    """
    print(f"Greetings, {name}!")


greet('programs')
# Greetings, programs!
```

By convention, Python functions use `snake_case`.

Python functions must have a body. To write an empty function, use the `pass` statement.

```python
def empty_function():
    pass
```

Returning a value requires use of the `return` keyword. If the function does not have an explicit return, it returns `None`.

Per [PEP 8](https://peps.python.org/pep-0008/), functions should be consistent about returning a value. If a function returns a value in one branch, it should return a value in all branches, using `return None`, rather than a bare `return`.

## Function Parameters

Python functions can take a mix of required and optional parameters.

```python
def fetch(dictionary, key, default=None):
    value = dictionary.get(value)
    if value:
        return value
    else:
        return default


generations = {'Red': 1, 'Gold': 2, 'Ruby': 3}
fetch(generations, 'Red')
# 1
fetch(generations, 'Blue')
# None
fetch(generations, 'Blue', 0)
# 0
```

### Default Parameters

Functions can set default values for parameters, making that parameter optional when the function is called.

**Important Note:** Python default parameters are evaluated when the function is *defined*, not when the function is *called*. Do not use mutable values such as `list`s or `dicts`. Instead, set the default value to `None` and use a conditional statement.

```python
def add_default_tags(tags=None):
    if not tags:
        tags = []

    tags.append('default')

    return tags
```

### Variadic Parameters

Python supports both variadic positional and variadic keyword parameters.

Variadic positional parameters are denoted with a `*` prefix, and are passed to the function as a `tuple`. A bare `*` does *not* allow for passing arbitrary positional arguments, and is instead used to identify keyword-only parameters (see below).

Variadic keyword parameters are denoted with a `**` prefix, and are passed to the function as a `dict`.

```python
def variadic(*positional, **keywords):
    pass
```

### Positional And Keyword Parameters

Unless otherwise specified, parameter values can be passed as either positional or keyword arguments.

```python
generations = {'Red': 1, 'Gold': 2, 'Ruby': 3}
fetch(key='Ruby', dictionary=generations)
# 3
```

Python also allows for defining positional-only or keyword-only function parameters. To specify parameters as positional only, add a `/` to the parameters list; all parameters before the `/` must be passed as positional arguments. Any parameters listed after a variadic positional parameter (or a bare `*`) must be passed as keyword arguments.

```python
def complex_parameters(pos_only, /, pos_or_keyword, *, keyword_only):
    pass

def variadic_parameters(pos_only, /, pos_or_keyword, *pos_var, keyword_only, **pos_key):
    pass
```

<!-- ## Type Annotations -->

## Function Scope

Functions can read from variables in parent or global scope without issue. However, attempting to write to a global variable, or a variable in a parent scope, actually creates a function-scoped variable with the same name, causing an error:

```python
total = 0


def increment():
    total += 1

    return total


increment()  # Raises an exception.
```

To indicate that the function is intended to reference the global variable, use the `global` keyword.

```python
total = 0


def increment():
    global total

    total += 1

    return total


increment()  # Returns 1.
```

Likewise, to indicate that the function is intended to reference a variable in a parent function, use the `nonlocal` keyword.

```python
def generate_closure():
    count = 0

    def increment():
        nonlocal count

        count += 1

        return count

    return increment


closure = generate_closure()
closure()  # Returns 1
```

## Documenting Functions

The first line of a function can be a [documentation string]({{url_for('syntax')}}/#docstrings) that describes what the function does.

```python
def greet():
    """
    Print a greeting.
    """
    print('Greetings, starfighter!')
```

There are multiple conventions for documenting functions with parameters, return types, etc:

- <a href="https://numpydoc.readthedocs.io/en/latest/format.html" target="_blank">Numpy</a>

## Lambdas

Python allows defining anonymous functions using the `lambda` keyword:

```python
greet = lambda: print('Greetings, programs!')
greet()
# Greetings, programs!
add = lambda a, b: a + b
add(1, 2)
# 3
```

Unlike functions, lambdas cannot be multi-line expressions and always return the value of the expression.

## Generator Functions

Generator functions are a type of [generator]({{url_for('syntax')}}#generators). Generator functions have the following differences from a regular function:

- Instead of using `return`, generator functions use `yield`.
- While a regular function returns once, a generator function can yield multiple times.
- When invoked, a generator function returns a generator, rather than a value.

```python
def upto(max_count):
    count = 0

    while count < max_count:
        yield count

        count += 1


generator = upto(3)
generator
# <generator object upto>
next(generator)
# 0
next(generator)
# 1
next(generator)
# 2
next(generator)
# raises StopIteration

[i for i in upto(5)]
# [0, 1, 2, 3, 4]
```

## Decorators

A decorator is a higher-order function that wraps other functions and modifies their behavior. They can be applied using the `@{decorator}` syntax.

```python
def validate_string(fn):
    def wrapper(value):
        if not isinstance(value, str):
            raise TypeError('value must be a string')

        fn(value)

    return wrapper


@validate_string
def say(value):
    print(value)


say('Hello')
# prints 'Hello'
say(None)
# raises TypeError
```

Decorator functions must accept a function as the first parameter and return a function. By convention, the inner function is named `wrapper`.

Decorators can also be called directly:

```python
def greeting(value):
    return f'Greetings, {value}!'


safe_greeting = validate_string(greeting)
safe_greeting('programs')
# 'Greetings, programs!'
safe_greeting(None)
# raises TypeError
```

### Decorator Parameters

Defining a decorator which takes parameters requires an additional layer of indirection:

```python
def curry(*curried_args, **curried_kwargs):
    def inner(fn):
        def wrapper(*args, **kwargs):
            merged_args = list(curried_args).copy()
            merged_args.extend(args)
            merged_kwargs = dict(curried_kwargs).copy()
            merged_kwargs.update(kwargs)

            return fn(*merged_args, **merged_kwargs)

        return wrapper

    return inner


@curry(rocket='Imp IV')
def launch(rocket, destination=None, launch_site='ksc'):
    return f'Launching {rocket} from {launch_site} bound for {destination}!'


launch(destination='The Mun')
# Launching Imp IV from ksc bound for The Mun!
```

The decorator function (`curry`, above) takes the parameters that are passed to the decorator call (`@curry(rocket='Imp IV')`). The decorator function returns an intermediate function (`inner`, above) that takes the original function as a parameter. Finally, the intermediate function generates and returns the final wrapper function.

### Decorators And Metadata

Because decorators return a new function, preserving the function metadata (such as the name and docstring) requires additional steps. The `@wraps` decorator is useful when defining other decorators.

```python
from functools import wraps


def upcase(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()

    return wrapper


@upcase
def greet():
    """Return a greeting"""
    return 'Greetings, programs!'


greet.__name__
# 'greet'
greet.__doc__
# 'Return a greeting'
```

# Syntax

## Comments

Python comments are delineated by a preceding `#` character.

```python
# This is a comment.
```

Inline comments should be preceded by two spaces:

```python
key = 'value'  # Assigns 'value' to key.
```

## Docstrings

Python uses docstrings to associate documentation with modules, functions, classes, and methods. Docstrings can be accessed via the `__doc__` property or by passing the object to `help()`.

Docstrings are declared using triple single (`'''`) or double (`"""`) quotes just below the class, method, or function declaration.

```python
def do_something:
    """
    This is a one-line summary of what the function does.

    This is an extended description of what the function does. It can be
    multiple lines but should not be wider than 72 characters.
    """
```

Guidelines for writing docstrings:

- The doc string line should begin with a capital letter and end with a period.
- The first line should be a short description.
- If there are more lines in the documentation string, the second line should be blank, visually separating the summary from the rest of the description.
- The following lines should be one or more paragraphs describing the object’s calling conventions, side effects, etc.

## Variables

Variable assignment:

```python
user = 'programs'
user
# 'programs'
type(user)
# <class 'str'>
```

The value of an assignment statement is the assigned value, so you can assign multiple variables:

```python
ultimate = answer = 42
```

Python also supports parallel assignment, including of iterables:

```python
a, b, c = 1, 2, 3

d, e, f = [4, 5, 6]
```

Python supports constants only by convention.

**Important Note:** Do not use the names of built-in types as variable names, e.g. `int` or `str`. This will (silently!) break explicit type casting. See the [List of Reserved Identifiers](#reserved-identifiers)

## Exceptions

```python
raise RuntimeError('Something went wrong')
```

Common error types:

- `AssertionError`: raised when an `assert` statement is passed a falsy expression.
- `AttributeError`: when accessing an undefined attribute on an object.
- `IndexError`: when accessing an invalid index on an indexed object.
- `KeyError`: when accessing an invalid key on a dictionary.
- `NameError`: when trying to access an undefined variable or object.
- `NotImplementedError`: when trying to access a method or function that is abstract or has not been implemented.
- `RuntimeError`: the default error type raised for a generic failure condition.
- `SyntaxError`: returned by the parser for invalid syntax.
- `TypeError`: when an operation or function is applied to an object of inappropriate type.

See <a href="https://docs.python.org/3/library/exceptions.html#exception-hierarchy" target="_blank">Exception Hierarchy</a>.

### Handling Exceptions

Use a `try...except` statement to handle thrown exceptions:

```python
try:
    f = open(filename, 'rb')
    data = f.read()
    f.close()
except IOError as e:
    sys.stderr.write('problem reading:' + filename)
```

The raised exception can also be accessed as `sys.exception()` within the `except` clause.

An `else` clause in a `try...except` statement is evaluated after the `try` clause, and only if no exceptions were raised.

A `finally` clause is evaluated after the `try` clause and any `except` or `else` clauses, whether or not an exception was raised. Any raised exceptions will be re-raised after the `finally` clause unless it includes a `break`, `continue`, or `return` statement.

## Conditionals

Conditional statements can be defined using the `if`, `elif`, and `else` keywords.

```python
if location == 'Oz':
    wear_ruby_slippers()
elif location == 'Narnia':
    enter_wardrobe()
else:
    print('You are on Earth.')
```

Objects that are logically false include `None`, `False`, `0`, and empty iterables.

### Logical Operators

- `and`: Conjunction.
- `or`: Disjunction.
- `not`: Negation.

### Ternary Statements

```python
'Yes' if True else 'No'
```

## Loops

### `for` Loop

Iterates over the items in an iterable object:

```python
for item in iterable_object:
    do_something(item)
```

Examples of iterable objects include `list`s, `range`s, `string`s. The outputs of calling `keys`, `items`, or `values` on a dictionary are also iterable.

Iterate over the keys and values in a dictionary:

```python
for key, value in dictionary:
    do_something(key, value)
```

This can also be used to iterate over nested data structures:

```python
for arabic, roman, ordinal in [[1, 'i', 'first'], [2, 'ii', 'second']]:
    do_something()
```

This will result in a `ValueError` if the inner collection does not have enough items.

```python
for arabic, roman, ordinal in [[]]:
    do_something()
# ValueError: not enough values to unpack (expected 3, got 0)
```

### `while` Loop

Repeats until the given condition evaluates to `False` or a falsy value.

```python
while $conditional:
    do_something()
```

A `while` loop can be negated using the `not` keyword.

```python
while not $conditional:
    do_something()
```

### `break`, `continue`, And `else`

The `break` statement can be used to exit out the innermost enclosing loop.

```python
generations = [('Red', 1), ('Gold', 2), ('Ruby', 3)]

for game, generation in generations:
    if generation == 2:
        print(f'{game} Version is in Generation 2')
        break
else:
    print('There are no Generation 2 games')
```

The `continue` statement continues with the next iteration of the loop.

```python
generations = [('Red', 1), ('Gold', 2), ('Ruby', 3)]

for game, generation in generations:
    if generation == 2:
        print(f'{game} Version is in the best generation')
        continue

    print(f'{game} Version is still fun')
```

The `else` statement in a loop runs when no `break` occurs. In a `for` loop, the `else` clause is executed after the loop reaches its final iteration. In a `while` loop, the `else` clause is executed after the loop's conditional evaluates to false.

### Iterators

An iterator object returns data one item at a time when passed to the `next()` function. Internally, it delegates to the `__next__` method. When the iterator has no remaining items, it raises a `StopIteration` error instead.

```python
class ThereCanOnlyBeOne:
    def __init__(self, limit=None):
        self.count = 0
        self.limit = limit

    def __next__(self):
        if self.limit:
            if self.count == self.limit:
                raise(StopIterationError)

            self.count += 1

        return 1

iterator = ThereCanOnlyBeOne(limit=2)
next(iterator)  # 1
next(iterator)  # 1
next(iterator)  # Raises StopIteration
```

### Iterables

An iterable object can be iterated over, and returns an iterator when passed to the `iter()` function. Internally, it delegates to the `__iter__` method.

```python
class Highlander:
    def __init__(self, limit=None):
        self.limit = limit

    def __iter__(self):
        return ThereCanOnlyBeOne(limit=self.limit)

iterable = Highlander(limit=2)
iterator = iter(iterable)
next(iterator)  # 1
next(iterator)  # 1
next(iterator)  # Raises StopIteration

list(iterable)  # [1, 1]
```

## Generators

Generators are a type of [iterator](#iterators). Generators can be defined either using a
<a href="{{ url_for('functions') }}#generator-functions">generator function</a>
or a generator expression.

A generator expression looks like a list comprehension, but uses parentheses instead of square brackets. It is equivalent to a lazy list comprehension, but without the memory overhead of creating the list. Generator expressions are particularly useful for passing to functions.

```python
generator = (i ** 2 for i in range(0, 5))
# <generator object <genexpr>>
next(generator)
# 0
next(generator)
# 1

max(i ** 2 for i in range(0, 5))
# 16
```

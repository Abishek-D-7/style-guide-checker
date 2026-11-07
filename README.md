# Style Guide Checker

A small command-line tool that checks Python files against three team conventions:

- Function names use `snake_case`.
- Public functions have docstrings.
- File names use `snake_case.py`.

Each violation includes an explanation of why the rule matters. These are our
team's chosen rules; teams should choose conventions that serve their needs.
See [STYLE_GUIDE.md](STYLE_GUIDE.md) for the precise rules and their rationale.
reviewers still decide whether documentation is useful and clear.

## Requirements

Python 3.8 or newer. No external dependencies or installation steps are needed.
The tool uses Python's built-in `ast` module to inspect functions and docstrings,
and `pathlib` to check file names.

## Usage

From the directory containing `style_checker.py`, run:

```sh
python style_checker.py example.py
```

Check multiple files by listing their paths:

```sh
python style_checker.py first_module.py second_module.py
```

The checker inspects regular and async functions, including methods and nested
functions. It checks the files you specify without modifying them or scanning
directories recursively.

## Example

For an `example.py` containing:

```python
def calculateTotal():
    """Calculate the total."""
    return 0


def save_result():
    pass
```

Running the checker prints:

```text
Line 1: Function 'calculateTotal' should use snake_case.
Why: Consistent naming makes code easier to navigate.

Line 6: Public function 'save_result' needs a docstring.
Why: Documentation helps readers understand its purpose.
```

A passing run prints nothing. Exit codes make the tool usable in scripts:

- `0`: all files pass.
- `1`: style violations found.
- `2`: invalid arguments or a file could not be read or parsed.

## Tests

```sh
python -m unittest -v
```

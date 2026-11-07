# Our team's Python style guide

These are our team's chosen conventions, not universal Python requirements.
Teams should choose rules that serve their needs and revisit them as those
needs change. Automated checks make shared expectations easy to apply;
reviewers still judge clarity and documentation quality.

## Function names

Use `snake_case`: lowercase ASCII letters and digits, with single underscores
between words, such as `calculate_total` or `parse_v2`. Names must start with
a letter after any leading underscores. Private prefixes (`_helper`,
`__helper`) and special names (`__init__`) are allowed. Uppercase letters,
repeated internal underscores, and trailing underscores are not allowed.

Consistent naming makes code easier to navigate. The checker inspects regular
and async functions, including methods and nested functions.

## Public function documentation

Every function whose name does not start with `_` must have a docstring as
its first statement. This includes methods and nested functions. Private and
special functions are exempt from this documentation rule.

Documentation helps readers understand a function's purpose. The checker uses
`ast.get_docstring` to check presence only; even an empty string counts as a
docstring. Reviewers decide whether the text explains the function well.

## File names

Use `snake_case.py`, such as `order_utils.py`. The same name rules apply to
the filename stem, allowing private modules and special files like
`__init__.py`. The extension must be lowercase `.py`.

Consistent file names make modules easier to find and import. Directory names
are outside the scope of this checker.

## Usage

Requires Python 3.8 or newer; no external dependencies are needed.

```sh
python style_checker.py example.py
python style_checker.py first_module.py second_module.py
```

Each violation includes its rationale. Function violations include the line
number of the `def` or `async def`. A passing run prints nothing. Exit codes:

- `0`: all files pass.
- `1`: style violations found.
- `2`: a file could not be read or parsed, or command arguments were invalid.

Pass file paths explicitly; the tool does not recursively scan directories or
modify code. When a file cannot be parsed, it reports an error and continues
checking any remaining files.

Run the automated checks with `python -m unittest -v`.

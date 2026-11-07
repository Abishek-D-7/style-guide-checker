"""Check Python files against a small set of team style conventions."""

import argparse
import ast
from pathlib import Path
import re
import sys


SNAKE_CASE = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\Z")


def is_snake_case(name):
    """Accept lowercase words, plus conventional private and special names."""
    if name.startswith("__") and name.endswith("__") and len(name) > 4:
        name = name[2:-2]
    else:
        name = name.lstrip("_")
    return SNAKE_CASE.fullmatch(name) is not None


def check_file(path):
    """Return violations as (line, message, rationale) tuples for one file.

    File violations use None for the line. Read and parse errors are left to
    the caller so they cannot be mistaken for a successful style check.
    """
    violations = []
    if path.suffix != ".py" or not is_snake_case(path.stem):
        violations.append((
            None,
            f"File '{path.name}' should use snake_case.py.",
            "Consistent file names make modules easier to find and import.",
        ))

    # Passing bytes lets ast honor Python source encoding declarations.
    tree = ast.parse(path.read_bytes(), filename=str(path))
    functions = sorted(
        (node for node in ast.walk(tree)
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))),
        key=lambda node: (node.lineno, node.col_offset),
    )
    for node in functions:
        if not is_snake_case(node.name):
            violations.append((
                node.lineno,
                f"Function '{node.name}' should use snake_case.",
                "Consistent naming makes code easier to navigate.",
            ))
        if not node.name.startswith("_") and ast.get_docstring(node) is None:
            violations.append((
                node.lineno,
                f"Public function '{node.name}' needs a docstring.",
                "Documentation helps readers understand its purpose.",
            ))
    return violations


def main(argv=None):
    """Run the checker, returning 0 for success, 1 for style, or 2 for errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="Python files to check")
    args = parser.parse_args(argv)
    has_violations = False
    has_errors = False
    for path in args.files:
        try:
            violations = check_file(path)
        except (OSError, SyntaxError, UnicodeError, ValueError) as error:
            print(f"Error checking {path}: {error}", file=sys.stderr)
            has_errors = True
            continue
        for line, message, rationale in violations:
            location = f"Line {line}" if line is not None else "File"
            if len(args.files) > 1:
                location = f"{path}: {location}"
            print(f"{location}: {message}\nWhy: {rationale}\n")
        has_violations |= bool(violations)
    return 2 if has_errors else 1 if has_violations else 0


if __name__ == "__main__":
    sys.exit(main())

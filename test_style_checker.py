"""Behavior tests for the team's style checker."""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import style_checker


class StyleCheckerTests(unittest.TestCase):
    """Exercise naming, AST inspection, and command-line outcomes."""

    def check_source(self, source, name="example.py"):
        """Check temporary source without leaving files in the repository."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / name
            path.write_text(source, encoding="utf-8")
            return style_checker.check_file(path)

    def test_function_name_and_missing_docstring(self):
        """Both violations point at the function definition."""
        violations = self.check_source("\n\n\ndef calculateTotal():\n    pass\n")
        self.assertEqual([item[0] for item in violations], [4, 4])
        self.assertIn("should use snake_case", violations[0][1])
        self.assertIn("needs a docstring", violations[1][1])

    def test_async_methods_and_nested_functions(self):
        """All supported function locations receive documentation checks."""
        violations = self.check_source(
            "class Example:\n"
            "    async def save_result(self):\n"
            "        def nested():\n"
            "            pass\n"
            "        return nested()\n"
        )
        self.assertEqual([item[0] for item in violations], [2, 3])

    def test_documented_public_and_private_functions_pass(self):
        """Private and special names are exempt from documentation."""
        self.assertEqual(self.check_source(
            'def save_result():\n    """Save a result."""\n'
            'def _helper():\n    pass\n'
            'def __init__():\n    pass\n',
            "__init__.py",
        ), [])

    def test_filename(self):
        """Filename violations do not claim a source line."""
        violations = self.check_source("", "BadName.py")
        self.assertEqual(len(violations), 1)
        self.assertIsNone(violations[0][0])

    def test_name_boundaries(self):
        """Enforce the precise naming convention documented by the team."""
        for name in ("parse_v2", "_helper", "__init__"):
            self.assertTrue(style_checker.is_snake_case(name), name)
        for name in ("BadName", "two__words", "trailing_", "___", "2fast"):
            self.assertFalse(style_checker.is_snake_case(name), name)

    def test_cli_exit_codes_and_error_continuation(self):
        """Read errors take precedence while other files are still checked."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.py"
            path.write_text("", encoding="utf-8")
            self.assertEqual(style_checker.main([str(path)]), 0)
            path.write_text("def save_result(): pass\n", encoding="utf-8")
            output, errors = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                self.assertEqual(style_checker.main([str(path)]), 1)
                self.assertEqual(style_checker.main([str(path / "missing.py"), str(path)]), 2)
            self.assertIn("Why: Documentation", output.getvalue())
            self.assertIn("Error checking", errors.getvalue())
            path.write_text("def broken(\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(style_checker.main([str(path)]), 2)


if __name__ == "__main__":
    unittest.main()

import unittest
from typing import Any
from modules import parse_docstring_params, tool

class TestParseDocstringParams(unittest.TestCase):

    def test_valid_docstring(self):
        docstring = """
        Description of what the tool does.

        Parameters:
            - param1: Description of first parameter
            - param2: Description of second parameter
        """
        expected = {
            'param1': 'Description of first parameter',
            'param2': 'Description of second parameter'
        }
        result = parse_docstring_params(docstring)
        self.assertEqual(result, expected)

    def test_empty_docstring(self):
        self.assertEqual(parse_docstring_params(''), {})

    def test_missing_parameters_section(self):
        docstring = """
        Description of what the tool does.

        Args:
            - param1: Description of first parameter
        """
        with self.assertRaises(ValueError):
            parse_docstring_params(docstring)

    def test_incorrect_param_format(self):
        docstring = """
        Description.

        Parameters:
            - param1 Description without colon
        """
        with self.assertRaises(ValueError):  # this will raise a ValueError due to unpacking fail in split
            parse_docstring_params(docstring)

    def test_extra_whitespace(self):
        docstring = """
        Description.

        Parameters:
            -  param1  :   First
            -  param2  :   Second
        """
        expected = {
            'param1': 'First',
            'param2': 'Second'
        }
        result = parse_docstring_params(docstring)
        self.assertEqual(result, expected)

class TestToolDecorator(unittest.TestCase):

    def test_tool_decorator_basic(self):
        @tool()
        def greet(name: str, loud: bool = False) -> str:
            """
            Greet someone nicely.

            Parameters:
                - name: The name of the person
                - loud: Whether to yell or not
            """
            return f"HELLO {name.upper()}!" if loud else f"Hello, {name}."

        # The decorator should return a Tool instance
        self.assertEqual(greet.name, "greet")
        self.assertEqual(greet.description, "Greet someone nicely.")
        self.assertTrue(callable(greet.func))

        # Check parameters dictionary
        self.assertIn("name", greet.parameters)
        self.assertIn("loud", greet.parameters)

        print(greet.parameters["name"])

        self.assertEqual(greet.parameters["name"]["type"], "str")
        self.assertEqual(greet.parameters["name"]["description"], "The name of the person")

        self.assertEqual(greet.parameters["loud"]["type"], "bool")
        self.assertEqual(greet.parameters["loud"]["description"], "Whether to yell or not")

        # Function should still be callable via .func
        self.assertEqual(greet.func("Bob", False), "Hello, Bob.")
        self.assertEqual(greet.func("Bob", True), "HELLO BOB!")

    def test_tool_custom_name(self):
        @tool(name="custom_tool")
        def do_something(task: str) -> str:
            """Do something important.

            Parameters:
                - task: The task to perform
            """
            return f"Task '{task}' completed."

        self.assertEqual(do_something.name, "custom_tool")
        self.assertEqual(do_something.parameters["task"]["type"], "str")
        self.assertEqual(do_something.parameters["task"]["description"], "The task to perform")


if __name__ == '__main__':
    unittest.main()

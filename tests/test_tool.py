import unittest
import json
from typing import Literal
from toolsmith import forge_tool

class TestTool(unittest.TestCase):

    def test_simple_function(self):
        @forge_tool
        def add(a: int, b: int) -> int:
            """Adds two numbers.
            
            Args:
                a: The first number.
                b: The second number.
            
            Returns:
                The sum of a and b.
            """
            return a + b

        tool = add
        expected_json = {
            "type": "function",
            "function": {
                "name": "add",
                "description": "Adds two numbers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "int", "description": "The first number."},
                        "b": {"type": "int", "description": "The second number."},
                    },
                    "required": ["a", "b"],
                },
            },
        }
        self.assertEqual(tool.json, expected_json)
        self.assertEqual(tool(a=5, b=3), "8")

    def test_function_with_defaults(self):
        @forge_tool
        def greet(name: str, greeting: str = "Hello") -> str:
            """Greets a person.

            Args:
                name: The name of the person.
                greeting: The greeting to use.
            """
            return f"{greeting}, {name}!"

        tool = greet
        expected_json = {
            "type": "function",
            "function": {
                "name": "greet",
                "description": "Greets a person.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "The name of the person."},
                        "greeting": {"type": "string", "description": "The greeting to use."},
                    },
                    "required": ["name"],
                },
            },
        }
        self.assertEqual(tool.json, expected_json)
        self.assertEqual(tool(name="Alice"), "Hello, Alice!")
        self.assertEqual(tool(name="Bob", greeting="Hi"), "Hi, Bob!")

    def test_function_with_no_docstring(self):
        @forge_tool
        def multiply(a: int, b: int) -> int:
            return a * b

        tool = multiply
        expected_json = {
            "type": "function",
            "function": {
                "name": "multiply",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "int"},
                        "b": {"type": "int"},
                    },
                    "required": ["a", "b"],
                },
            },
        }
        self.assertEqual(tool.json, expected_json)
        self.assertEqual(tool(a=2, b=4), "8")
        
    def test_function_with_no_parameters(self):
        @forge_tool
        def get_hello() -> str:
            """Returns the string 'hello'."""
            return "hello"

        tool = get_hello
        expected_json = {
            "type": "function",
            "function": {
                "name": "get_hello",
                "description": "Returns the string 'hello'."
            },
        }
        self.assertEqual(tool.json, expected_json)
        self.assertEqual(tool(), "hello")

    def test_function_with_literal_type(self):
        @forge_tool
        def choose_color(color: Literal["red", "green", "blue"]) -> str:
            """Chooses a color.

            Args:
                color: The color to choose.
            """
            return f"You chose {color}."

        tool = choose_color
        expected_json = {
            "type": "function",
            "function": {
                "name": "choose_color",
                "description": "Chooses a color.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "color": {
                            "type": "string",
                            "description": "The color to choose.",
                            "enum": ["red", "green", "blue"],
                        },
                    },
                    "required": ["color"],
                },
            },
        }
        self.assertEqual(tool.json, expected_json)
        self.assertEqual(tool(color="red"), "You chose red.")

    def test_name_property(self):
        @forge_tool
        def my_function():
            pass
        tool = my_function
        self.assertEqual(tool.name, "my_function")
        
    def test_str_representation(self):
        @forge_tool
        def my_function():
            """This is a test function."""
            pass
        tool = my_function
        expected_str = json.dumps(tool.json, indent=4)
        self.assertEqual(str(tool), expected_str)

if __name__ == "__main__":
    unittest.main()
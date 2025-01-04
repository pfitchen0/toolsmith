import json
import inspect
from typing import Callable
import docstring_parser


class Tool:
    def __init__(self, function: Callable) -> None:
        self.function = function

    @property
    def name(self):
        return self.function.__name__

    @property
    def json(self):
        return self._get_function_json()

    def __str__(self):
        return json.dumps(self._get_function_json(), indent=4)

    def __call__(self, *args, **kwargs):
        # Hack to ensure tool calls always return a string, which is easier to feed into the model.
        return str(self.function(*args, **kwargs))

    def _get_function_json(self) -> str:
        docstring = docstring_parser.parse(self.function.__doc__)
        docstring_args = {
            param.arg_name: param.description for param in docstring.params
        }
        properties = {}
        required = []
        for name, arg in inspect.signature(self.function).parameters.items():
            arg_enums = []
            arg_type = (
                "Any" if arg.annotation == inspect._empty else arg.annotation.__name__
            )
            if arg_type == "Literal":
                arg_enums = [enum for enum in arg.annotation.__args__]
            if arg_type in ["str", "Literal"]:
                arg_type = "string"

            arg_description = {"type": arg_type}
            if arg_enums:
                arg_description["enum"] = arg_enums
            if name in docstring_args:
                arg_description["description"] = docstring_args[name]

            properties[name] = arg_description
            if arg.default == inspect._empty:
                required.append(name)

        function_signature = {
            "type": "function",
            "function": {
                "name": self.function.__name__,
            },
        }
        if docstring.short_description:
            function_signature["function"]["description"] = docstring.short_description
        if properties:
            function_signature["function"]["parameters"] = {
                "type": "object",
                "properties": properties,
            }
            if required:
                function_signature["function"]["parameters"]["required"] = required
        return function_signature


def forge_tool(function: Callable) -> Tool:
    return Tool(function=function)

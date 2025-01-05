# Toolsmith

Toolsmith is a super simple library for converting Python functions into "tools" for LLMs to use. A "Tool" is just a wrapper around the function, but with a method to extract a JSON description from the function and its docstring. The JSON description follows the [OpenAI Function/Tool Calling schema](https://platform.openai.com/docs/guides/function-calling).
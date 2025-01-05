# Toolsmith

Toolsmith is a super simple library for converting Python functions into "tools" for LLMs to use. A "Tool" is just a wrapper around the function, but with a method to extract a JSON description from the function and its docstring. The JSON description follows the [OpenAI Function/Tool Calling schema](https://platform.openai.com/docs/guides/function-calling).

## Prerequisites

(Optional but recommended) Create a virtual environment and activate it.

```
python3 -m venv venv
source venv/bin/activate
# `deactivate` to deactivate the environment
```

Install Python dependencies.

```
pip install -r requirements.txt
```

## Example

See `groq_example.py` for an example of how Toolsmith can be used to easily convert functions into LLM "tools" to create a tool calling agent.
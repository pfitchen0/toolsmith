import json
from dotenv import load_dotenv
import os
import json
from groq import Groq

from toolsmith import forge_tool, Tool

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


class Agent:
    def __init__(
        self,
        client: Groq,
        model: str = MODEL,
        system_prompt: str | None = None,
        tools: list[Tool] | None = None,
    ):
        self.client = client
        self.model = model
        self.messages = []
        self.tools = {tool.name: tool for tool in tools}
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def __call__(self, prompt: str = None) -> str:
        if prompt:
            self.messages.append({"role": "user", "content": prompt})
        response = self._llm()

        while response.tool_calls is not None:
            for tool_call in response.tool_calls:
                if tool_call.function.name not in self.tools.keys():
                    continue
                function_return = self.tools[tool_call.function.name](
                    **json.loads(tool_call.function.arguments)
                )
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_call.function.name,
                        "content": function_return,
                    }
                )
            response = self._llm()

        return response.content

    def _llm(self) -> dict:
        response = (
            self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=False,
                tools=[tool.json for tool in self.tools.values()],
                tool_choice="auto",
                max_tokens=4096,
            )
            .choices[0]
            .message
        )
        self.messages.append(response.to_dict())
        return response

    def __str__(self):
        role_to_color = {
            "system": 33,
            "user": 0,
            "assistant": 36,
            "tool": 31,
        }
        string = ""
        for message in self.messages:
            color = role_to_color.get(message["role"], "red")
            string += f"\n\033[{color}m{str(message)}\033[0m\n"
        return string


if __name__ == "__main__":
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    system_prompt = (
        """You are a helpful math assistant who has access to a calculate function."""
    )

    @forge_tool
    def calculate(expression: str) -> str:
        """Evaluate a mathematical expression"""
        try:
            result = eval(expression)
            return json.dumps({"result": result})
        except:
            return json.dumps({"error": "Invalid expression"})

    agent = Agent(
        client=client,
        system_prompt=system_prompt,
        tools=[calculate],
    )

    print("Enter 'q', 'quit', or 'exit' to end the conversation.")
    while True:
        prompt = input(">>> ")
        if prompt in ["q", "quit", "exit"]:
            break
        response = agent(prompt)
        print(f"\033[36m{response}\033[0m")

    print(agent)  # prints the message history, including hidden tool calls.

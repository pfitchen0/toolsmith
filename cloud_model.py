from dataclasses import dataclass
from dotenv import load_dotenv
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
import os
from typing import Iterable, Literal

load_dotenv()


class BaseUrl(Enum):
    OPENAI = None
    GROQ = "https://api.groq.com/openai/v1"


class ApiKey(Enum):
    OPENAI = "OPENAI_API_KEY"
    GROQ = "GROQ_API_KEY"


Provider = Literal["openai", "groq"]


@dataclass
class CloudModelConfig:
    model: str
    provider: Provider
    base_url: BaseUrl
    api_key: ApiKey


class CloudModelOption(Enum):
    GPT4O_MINI = "openai/gpt-4o-mini"
    GPT4O = "openai/gpt-4o"
    GROQ_LLAMA3_1_8B = "groq/llama-3.1-8b-instant"
    GROQ_LLAMA3_3_70B = "groq/llama-3.3-70b-versatile"


def _build_model_config(option: CloudModelOption) -> CloudModelConfig:
    provider, model = option.value.split("/")
    match provider:
        case "openai":
            return CloudModelConfig(
                model=model,
                provider="openai",
                base_url=BaseUrl.OPENAI,
                api_key=ApiKey.OPENAI,
            )
        case "groq":
            return CloudModelConfig(
                model=model, provider="groq", base_url=BaseUrl.GROQ, api_key=ApiKey.GROQ
            )


class CloudModel:
    def __init__(self, option: CloudModelOption) -> None:
        self.config = _build_model_config(option)
        base_url = self.config.base_url.value
        api_key = self.config.api_key.value
        self.client = OpenAI(api_key=os.environ.get(api_key), base_url=base_url)

    def chat_completion(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        temperature: float | None = None,
        tools: Iterable[ChatCompletionToolParam] | None = None,
    ) -> ChatCompletion:
        return self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=temperature,
            tools=tools,
            stream=False,
            n=1,
        )


if __name__ == "__main__":
    model = CloudModel(CloudModelOption.GPT4O_MINI)
    messages = []
    print("Enter 'q', 'quit', or 'exit' to end the conversation.")
    while True:
        prompt = input(">>> ")
        if prompt in ["q", "quit", "exit"]:
            break
        messages.append(ChatCompletionUserMessageParam(role="user", content=prompt))
        response = model.chat_completion(messages).choices[0].message
        messages.append(response)
        print(f"\033[36m{response.content}\033[0m")

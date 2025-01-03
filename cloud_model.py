from dataclasses import dataclass
from typing import Iterable
from dotenv import load_dotenv
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
import os

load_dotenv()


class BaseUrl(Enum):
    OPENAI = None
    GROQ = "https://api.groq.com/openai/v1"


class ApiKey(Enum):
    OPENAI = "OPENAI_API_KEY"
    GROQ = "GROQ_API_KEY"


@dataclass
class CloudModelConfig:
    model: str
    base_url: BaseUrl
    api_key: ApiKey


class CloudModelOption(Enum):
    GROQ_LLAMA3_1_8B = "groq/llama-3.1-8b-instant"
    GROQ_LLAMA3_3_70B = "groq/llama-3.3-70b-versatile"
    GPT4O_MINI = "openai/gpt-4o-mini"
    GPT4O = "openai/gpt-4o"


def _build_model_config(option: CloudModelOption) -> CloudModelConfig:
    provider, model = option.value.split("/")
    match provider:
        case "openai":
            return CloudModelConfig(
                model=model, base_url=BaseUrl.OPENAI, api_key=ApiKey.OPENAI
            )
        case "groq":
            return CloudModelConfig(
                model=model, base_url=BaseUrl.GROQ, api_key=ApiKey.GROQ
            )


class CloudModel:
    def __init__(self, option: CloudModelOption) -> None:
        model_config = _build_model_config(option)
        base_url = model_config.base_url.value
        api_key = model_config.api_key.value
        self.model = model_config.model
        self.client = OpenAI(api_key=os.environ.get(api_key), base_url=base_url)

    def chat_completion(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        max_completion_tokens: int | None,
        temperature: float | None,
        tools: Iterable[ChatCompletionToolParam] | None,
    ) -> ChatCompletion:
        return self.client.chat.completions.create(
            model = self.model,
            messages=messages,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            tools=tools,
            stream=False,
            n=1,
        )

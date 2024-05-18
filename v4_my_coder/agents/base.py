from llama_cpp import CreateChatCompletionResponse

from utilities import extract_code
from .llama import llm


class BaseAgent:
    system_prompt = ""
    prompt = ""
    response_format = None
    temperature = 0.5
    max_tokens = 2000
    extract_code = False

    def __init__(self, **prompt_kwargs):
        self.prompt_kwargs = prompt_kwargs

    def render_system_prompt(self):
        return self.system_prompt

    def render_prompt(self):
        return self.prompt.format(**self.prompt_kwargs)

    def run(self):
        # print("DEBUG")
        # print("run llm.create_chat_completion")
        # print(self.render_system_prompt())
        # print(self.render_prompt())
        # print(self.response_format)
        # print(self.temperature)
        # print()
        completion: CreateChatCompletionResponse = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": self.render_system_prompt(),
                },
                {"role": "user", "content": self.render_prompt()},
            ],
            response_format=self.response_format,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        result = completion["choices"][0]["message"]["content"]

        if self.extract_code:
            result = extract_code(result)

        return result

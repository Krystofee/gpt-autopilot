import os
from dotenv import load_dotenv
from openai import OpenAI
import openai

load_dotenv()
openai_client = OpenAI()


def get_gpt4_output(prompt: str, system_prompt="You are a helpful assistant with senior knowledge of python designed to output JSON.") -> str:
    # print()
    # print()
    # print(system_prompt)
    # print()
    # print(prompt)
    # print()
    # print()

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


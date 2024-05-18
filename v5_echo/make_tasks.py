import argparse
import json

from model_openai import get_gpt4_output
from print_color import print_colored_text


def make_tasks(prompt_filename):
    with open(prompt_filename, 'r') as file:
        prompt = file.read()

    content = get_gpt4_output(
        prompt,
        system_prompt="""You are a helpful assistant with senior knowledge of python designed to output JSON.
I need you to create a JSON object in this format:

{
    "tasks": [
        {
            "filename": "filename.py",
            "description": "Description of Task 1"
        },
        {
            "filename": "other_filename.py",
            "description": "Description of Task 2"
        }
    ]
}

"""
    )
    print_colored_text("***** gpt-4o output *****", content, "blue")
    return json.loads(content)['tasks']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="Prompt filename")

    args = parser.parse_args()

    # Get the output from GPT-4
    make_tasks(args.prompt)


if __name__ == "__main__":
    main()

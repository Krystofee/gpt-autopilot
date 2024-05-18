import json
import os
from model_openai import get_gpt4_output
from print_color import print_colored_text
from repo_context import repository_context


def write_code(*, repository, filename, prompt, objective):
    repo_context = repository_context(repository)

    response_code = get_gpt4_output(
        f"""
You are just a part of a programmer team to implement the global objective. Here is the objective for you to have more context: {objective}

Here is the context of the whole project: {repo_context}

Now, you need to generate the code for the file {filename} based on the prompt below:
{prompt}
""",
        system_prompt="""
You are a helpful assistant with senior knowledge of python designed to output python code in JSON.

You will receive the context of all the files in the working repository, so you can use that information to generate the code.
Your responses will be used to replace the whole file content, so in case you are editing an existing file, make sure to respond in a way that the whole existing file will be rewritten.

Desired output example:
{
    "filename": "filename.py",
    "code": "print(\"Hello world\")\nprint(\"Goodbye world\")"
}
"""
    )

    response_code_json = json.loads(response_code)

    filename = response_code_json['filename']
    code = response_code_json['code']

    with open(os.path.join(repository, filename), 'w') as file:
        file.write(code)

    # Add to the repository
    os.chdir(repository)
    os.system(f"git add {filename}")
    os.system(f"git commit -m \"Edit {filename}\"")
    os.chdir("..")

    print_colored_text(
        "***** Code written *****",
        f"filename: {filename}\n"
        f"code: {code}",
        "green"
    )

    return filename, code

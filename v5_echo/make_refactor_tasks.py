import json
import os
from model_openai import get_gpt4_output
from print_color import print_colored_text
from repo_context import repository_context


def make_refactor_tasks(repository, objective):
    repo_context = repository_context(repository)

    response_code = get_gpt4_output(
        f"""
Here is the object that these files should implement: {objective}

Here are things to check:
- Is the objective implemented and will work?
- Are there any bugs in the code?
- Are there any unnecessary duplications?
- Is the code written using best practices?
- Is there README.md file with the correct information? Make very simple readme.
- Is the code runnable as required?
- Are there any missing imports?
- is there requirements.txt file with dependencies?

Your task is to determine whether the project is implemented correctly and there are no changes to do. These changes can be related to the code, or the README.md, not the structure or other things, because the tasks are able just to modify the code and not do anything else.

If the project is finished, output empty list of tasks.

Here is the context of the whole project containing all files and their contents: {repo_context}
""",
        system_prompt="""
You are a helpful assistant with senior knowledge of python designed to output python code in JSON.

You will receive the context of all the files in the working repository, so you can use that information to generate the code.

Your responses will be used to replace the whole file content, so in case you are editing an existing file, make sure to respond in a way that the whole existing file will be rewritten.

Desired output example:
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

    tasks = json.loads(response_code)['tasks']

    print_colored_text(
        "***** Refactor tasks generated *****",
        f"tasks: {tasks}",
        "blue"
    )

    return tasks

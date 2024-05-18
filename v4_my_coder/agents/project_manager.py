import json

from utilities import extract_code
from .base import BaseAgent
from .llama import llm


class ProjectManagerAgent(BaseAgent):
    system_prompt = """You are skilled project manager and head of development responsible for creating a detailed checklist of tasks that will guide other AGI agents to complete a given programming objective. Your task is to analyze the provided objective and generate a well-structured checklist, as well as tasks broken down to be very specific, clear, and executable by other agents without the context of other tasks (but don't write the code yet)."""
    prompt = """Here is the programming objective you need to create a checklist for:
{objective}

To generate the checklist, follow these steps:

1. Analyze the objective to identify the high-level requirements and goals of the project. This will help you understand the scope and create a comprehensive checklist.
2. Break down the objective into smaller, highly specific tasks that can be worked on independently in each task.
3. All required dependencies are already available so you don't have to care about installation or environment setup.
4. Provide the current context for each task, which should be sufficient for the agents to understand and execute the task without referring to other tasks in the checklist. This will help agents avoid task duplication.
5. Pay close attention to the objective and make sure the tasks implement all necessary pieces needed to make the program work.
6. Don't create tasks to install dependencies or set up the environment, assume all required dependencies are already available.
7. Don't create tasks to create files or directories, assume they are already created.

Write the checklist in a clear and structured format that is easy to read and follow. Don't write any code yet, just descriptions for other programmers to follow. 

Pay attention to the way files are passed in the tasks, always use full paths. The project root directory is "./project".

Make sure tasks are not duplicated."""

    temperature = 0.7
    max_tokens = 8192

    def render_prompt(self):
        return self.prompt.format(**self.prompt_kwargs)

    def run(self):
        project_description = super().run()

        print("***** Project Description *****")
        print(project_description)
        print()

        json_completion = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": """Your job is to reformat the response of the previous agent to the required JSON format. Fix the pathnames of the files to be relative paths from "./project".

Just include the actionable tasks that require you to write code. 
Don't create any files, assume they are already created. Don't include tasks to install dependencies or set up the environment, assume all required dependencies are already available."""
                },
                {"role": "user", "content": project_description.format(objective=self.prompt_kwargs["objective"])},
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task": {"type": "string"},
                            "file": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["task", "file", "description"],
                    },
                },
            },
            temperature=0.2,
            max_tokens=8192,
        )

        print("***** JSON Completion *****")
        print(json_completion)
        print()

        return json.loads(extract_code(json_completion["choices"][0]["message"]["content"]))



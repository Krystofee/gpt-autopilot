"""
Example usage

python v1_generic.py \
    --prompt "Write a game of tic tac toe. It should be for 2 players and it should accept input in the format 1;2 for example, (x;y where x and y are 1-3). If any player wins, print the result and ask to play again or close the game by input Y or q." \
    --filename tic_tac_toe.py
"""

import argparse
import json
import os

from llama_cpp import Llama, CreateChatCompletionResponse

from utils import extract_python_code

OUTPUT_DIR = "codegen_output"

llm = Llama(
    model_path="./models/Meta-Llama-3-8B-Instruct-Q5_K_M.gguf",
    chat_format="llama-3",
    n_gpu_layers=-1,
    verbose=True,
    n_ctx=8192,
)


def get_completion(system_prompt, prompt, response_format):
    completion: CreateChatCompletionResponse = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": prompt},
        ],
        response_format=response_format,
        temperature=0.4,
    )
    return completion["choices"][0]["message"]["content"]


def generate_tasks(prompt):
    SYSTEM_PROMPT = (
        "You are a helpful python programmer. Your job is to output a set of tasks based on the prompt. "
        "These tasks will be used as more detailed description of the initial prompt by programmers. "
        "The resulting set of tasks should be structured and should provide enough context."
    )

    print()
    print("Generating tasks...")
    print(f"    system_prompt = {SYSTEM_PROMPT}")
    print(f"    prompt = {prompt}")
    print()

    enhanced_prompt = f"""Here is the prompt: {prompt}"""

    completion = get_completion(
        SYSTEM_PROMPT,
        enhanced_prompt,
        {
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "coder_agent_prompt": {"type": "string"},
                            },
                            "required": ["coder_agent_prompt"],
                        },
                    }
                },
                "required": ["tasks"],
            },
        },
    )

    print("Tasks generated:")
    print(completion)

    return json.loads(completion)["tasks"]


def generate_and_save_code(original_prompt, all_tasks, prompt, filename):
    system_prompt = "You are a helpful python senior programmer. Implement the what you are told in python and implement it in structured way. Output working python code."

    print()
    print("Generating completion...")
    print(f"    system_prompt = {system_prompt}")
    print(f"    prompt = {prompt}")
    print()

    # Simulate a function to get completion based on a prompt
    completion = get_completion(
        system_prompt,
        prompt,
        {
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"],
            },
        },
    )

    completion = json.loads(completion)["code"]

    # Strip ```python from the generated code
    completion = extract_python_code(completion)

    print("Completion generated:")
    print(completion)

    full_filename = f"{OUTPUT_DIR}/{filename}"

    # Delete the file if it exists
    if os.path.exists(full_filename):
        print(f"Deleting existing file: {full_filename}")
        os.remove(full_filename)

    # Write the generated code to a file
    with open(full_filename, "w") as f:
        print(f"Writing completion to file: {full_filename}")
        f.write(completion)


def generate_requirements_txt(*filenames):
    """generates requirements.txt from python source files. Reads files and calls get_coompletion base on each file header."""
    print("Generating requirements.txt...", filenames)

    SYSTEM_PROMPT = "You are a helpful python programmer. Your job is to get python dependencies from the python code. You will be provided with python code and you have to extract the dependencies from the code. Don't include versions, just the dependencies."

    requirements = set()
    for filename in filenames:
        filename = f"{OUTPUT_DIR}/{filename}"
        with open(filename, "r") as f:
            prompt = f.readline().strip()
            completion = get_completion(
                SYSTEM_PROMPT,
                prompt,
                {
                    "type": "json_object",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "dependencies": {
                                "type": "array",
                                "items": {"type": "string"},
                            }
                        },
                    },
                },
            )

            print(
                "Dependencies for file:", filename, "are:", completion["dependencies"]
            )

            dependencies = json.loads(completion["dependencies"])
            requirements.update(dependencies)

    # Delete the file if it exists
    if os.path.exists(f"{OUTPUT_DIR}/requirements.txt"):
        print(f"Deleting existing file: {OUTPUT_DIR}/requirements.txt")
        os.remove(f"{OUTPUT_DIR}/requirements.txt")

    with open(f"{OUTPUT_DIR}/requirements.txt", "w") as f:
        for requirement in requirements:
            f.write(requirement + "\n")


def setup_environment():
    """Create new python environment inside OUTPUT_DIR and install requirements.txt"""

    # Create new python environment
    os.system(f"python3 -m venv {OUTPUT_DIR}/env")

    # Install requirements.txt
    os.system(f"{OUTPUT_DIR}/env/bin/pip install -r {OUTPUT_DIR}/requirements.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and optionally execute code based on a prompt."
    )
    parser.add_argument(
        "--prompt", type=str, required=True, help="Prompt to generate the code"
    )
    parser.add_argument(
        "--workdir", type=str, required=True, help="Working directory name"
    )
    args = parser.parse_args()

    OUTPUT_DIR = f"codegen_output/{args.workdir}"

    # Recreate the output directory
    if os.path.exists(OUTPUT_DIR):
        print(f"Deleting existing directory: {OUTPUT_DIR}")
        os.system(f"rm -rf {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR)

    tasks = generate_tasks(args.prompt)

    for task in tasks:
        generate_and_save_code(
            args.prompt, tasks, task["coder_agent_prompt"], "main.py"
        )

    generate_requirements_txt("main.py")
    setup_environment()

    print()
    print("Code generation completed successfully!")
    print(f"Code written to: {OUTPUT_DIR}/main.py")
    print()
    print("To run the generated code, execute:")
    print(f"    python {OUTPUT_DIR}/main.py")
    print()

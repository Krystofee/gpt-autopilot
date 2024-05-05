"""
Example usage

python v1_generic.py \
    --prompt "Write a game of tic tac toe. It should be for 2 players and it should accept input in the format 1;2 for example, (x;y where x and y are 1-3). If any player wins, print the result and ask to play again or close the game by input Y or q." \
    --filename tic_tac_toe.py
"""

import argparse
import os

from llama_cpp import Llama, CreateChatCompletionResponse

from utils import extract_python_code

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
        temperature=0.2,
    )
    return completion['choices'][0]['message']['content']


def generate_and_save_code(prompt, filename):
    system_prompt = "You are a helpful python programmer. Your job is to write a code that you are asked to write. Implement the code in python and implement it in structured way. Output only python code."

    print()
    print("Generating completion...")
    print(f"    system_prompt = {system_prompt}")
    print(f"    prompt = {prompt}")
    print()

    # Simulate a function to get completion based on a prompt
    completion = get_completion(system_prompt, prompt, None)

    # Strip ```python from the generated code
    completion = extract_python_code(completion)

    print("Completion generated:")
    print(completion)

    full_filename = f"codegen_output/{filename}"

    # Delete the file if it exists
    if os.path.exists(full_filename):
        print(f"Deleting existing file: {full_filename}")
        os.remove(full_filename)

    # Write the generated code to a file
    with open(full_filename, "w") as f:
        print(f"Writing completion to file: {full_filename}")
        f.write(completion)

    print()
    print("Code generation completed successfully!")
    print(f"Code written to: {full_filename}")
    print()
    print("To run the generated code, execute:")
    print(f"    python {full_filename}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate and optionally execute code based on a prompt.')
    parser.add_argument('--prompt', type=str, required=True, help='Prompt to generate the code')
    parser.add_argument('--filename', type=str, required=True, help='Filename where the code will be written')
    args = parser.parse_args()

    generate_and_save_code(args.prompt, args.filename)

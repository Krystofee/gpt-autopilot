import json
import os

from llama_cpp import Llama, CreateChatCompletionResponse

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


if __name__ == "__main__":
    system_prompt = "You are a helpful python programmer. Your job is to write a code that you are asked to write. Implement the code in python and implement it in structured way. The output should be runable python code."
    prompt = "Write a game of tic tac toe. It should be for 2 players and it should accept input in the format 1;2 for example, (x;y where x and y are 1-3). If any player wins, print the result and ask to play again or close the game by input Y or q."

    print("Generating completion...")
    completion = get_completion(system_prompt, prompt, None)

    print("Completion generated:")
    print(completion)

    # delete the file if it exists
    os.remove("codegen_output/tic_tac_toe.py") if os.path.exists("codegen_output/tic_tac_toe.py") else None

    with open("codegen_output/tic_tac_toe.py", "w") as f:
        print("Writing completion to file...")
        f.write(completion)

    # run the generated code (oh yeah, and pray that its safe to run it!)
    print("Running the generated code...")
    exec(open("codegen_output/tic_tac_toe.py").read())
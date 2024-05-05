from llama_cpp import Llama

llm = Llama(
    model_path="../models/Meta-Llama-3-8B-Instruct-Q5_K_M.gguf",
    chat_format="llama-3",
    n_gpu_layers=-1,
    verbose=False,
    n_ctx=8192,
)

llm_embedding = Llama(
    model_path="../models/Meta-Llama-3-8B-Instruct-Q5_K_M.gguf",
    chat_format="llama-3",
    n_gpu_layers=-1,
    verbose=False,
    embedding=True,
    n_ctx=8192,
)

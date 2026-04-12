from llama_cpp import Llama

llm = Llama(
    model_path="./models/mistral-7b/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_gpu_layers=1,
    verbose=True,
)
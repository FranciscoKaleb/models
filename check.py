from llama_cpp import Llama

# Check if CUDA backend is available
import llama_cpp
print(dir(llama_cpp))  # look for anything mentioning 'cuda' or 'gpu'

# Load with verbose to see backend info
llm = Llama(
    model_path="./models/mistral-7b/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_gpu_layers=1,   # just 1 layer to test
    verbose=True
)
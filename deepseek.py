from llama_cpp import Llama
from pathlib import Path

MODEL_PATH = "./models/deepseek-coder-v2-lite/DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf"

print("Loading DeepSeek Coder onto RTX 3060...")

llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=20,    # instead of -1, only put 20 layers on GPU
    n_ctx=2048,         # reduce context window too
    n_batch=512,
    verbose=False,
)
print("✅ Model loaded\n")

SYSTEM_PROMPT = "You are an expert programming assistant. Write clean, working code with brief explanations. Default to Python unless specified otherwise."
conversation_history = []

print("=" * 50)
print("  DeepSeek Coder Chat  |  type 'exit' to quit")
print("  type 'clear' to reset conversation history")
print("=" * 50)
print()

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue
    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break
    if user_input.lower() == "clear":
        conversation_history = []
        print("\n--- Conversation history cleared ---\n")
        continue

    conversation_history.append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    print("Assistant: ", end="", flush=True)

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=1024,
        temperature=0.2,      # lower = more precise/deterministic for code
        top_p=0.95,
        repeat_penalty=1.1,
        stream=True,
    )

    full_response = ""
    for chunk in response:
        delta = chunk["choices"][0]["delta"]
        if "content" in delta:
            token = delta["content"]
            print(token, end="", flush=True)
            full_response += token

    print("\n")

    conversation_history.append({"role": "assistant", "content": full_response})

    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]
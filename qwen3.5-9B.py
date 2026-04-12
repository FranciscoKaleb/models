from llama_cpp import Llama
from pathlib import Path

MODEL_PATH = "./models/Qwen3.5-9B-Claude-4.6-Opus-Reasoning-Distilled/Qwen3.5-9B.Q4_K_M.gguf"

print("Loading model onto RTX 3060...")

llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=-1,        # -1 = put ALL layers on GPU (fits entirely in your 12GB VRAM)
    n_ctx=4096,             # context window (how much conversation it remembers)
    n_batch=512,            # batch size for prompt processing
    verbose=False,          # set True if you want to see layer loading details
)

print("✅ Model loaded\n")

# ── Chat state ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = "You are a friendly assistant. Give clear and concise responses."
conversation_history = []  # list of {"role": ..., "content": ...} dicts

print("=" * 50)
print("  Qwen 3.5 9B  |  type 'exit' to quit")
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

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # Build full message list with system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    # Generate response
    print("Assistant: ", end="", flush=True)

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=8192, # prev is 512 for shorter response
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.1,
        stream=True,            # streams tokens as they generate (feels much faster)
    )

    # Stream tokens to console in real time
    full_response = ""
    for chunk in response:
        delta = chunk["choices"][0]["delta"]
        if "content" in delta:
            token = delta["content"]
            print(token, end="", flush=True)
            full_response += token

    print("\n")  # newline after response

    # Add assistant response to history for next turn
    conversation_history.append({
        "role": "assistant",
        "content": full_response
    })

    # Optional: trim history if it gets too long (keeps last 10 exchanges)
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]
from llama_cpp import Llama
from pathlib import Path

def is_hardware_related(user_input):
    check = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are a classifier. Reply ONLY with 'yes' or 'no'. No other text."},
            {"role": "user", "content": f"Is this message asking about computer parts or hardware? Message: '{user_input}'"}
        ],
        max_tokens=5,
        temperature=0.0,  # deterministic
    )
    answer = check["choices"][0]["message"]["content"].strip().lower()
    return "yes" in answer

MODEL_PATH = "./models/qwen2.5-14b/Qwen2.5-14B-Instruct-Q4_K_M.gguf"

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

SYSTEM_PROMPT = """You are a customer support agent for a computer parts shop.
Only answer questions related to computer parts, components, and hardware (CPUs, GPUs, RAM, storage, motherboards, PSUs, cases, cooling, etc.).
If asked anything unrelated to computer parts, respond with: 'Sorry, I can only help with computer parts and hardware questions.'"""

conversation_history = []  # list of {"role": ..., "content": ...} dicts

print("=" * 50)
print("  Mistral 7B Chat  |  type 'exit' to quit")
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

    # ✅ Check if on-topic BEFORE sending to model
    if not is_hardware_related(user_input):
        print("Assistant: Sorry, I can only help with computer parts and hardware questions.\n")
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
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.1,
        stream=True,
    )

    # Stream tokens to console in real time
    full_response = ""
    for chunk in response:
        delta = chunk["choices"][0]["delta"]
        if "content" in delta:
            token = delta["content"]
            print(token, end="", flush=True)
            full_response += token

    print("\n")

    # Add assistant response to history for next turn
    conversation_history.append({
        "role": "assistant",
        "content": full_response
    })

    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]
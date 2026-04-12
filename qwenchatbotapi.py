from llama_cpp import Llama

MODEL_PATH = "./models/qwen2.5-14b/Qwen2.5-14B-Instruct-Q4_K_M.gguf"

SYSTEM_PROMPT = """You are a customer support agent for a computer parts shop.
Only answer questions related to computer parts, components, and hardware (CPUs, GPUs, RAM, storage, motherboards, PSUs, cases, cooling, etc.).
If asked anything unrelated to computer parts, respond with: 'Sorry, I can only help with computer parts and hardware questions.'"""

llm = None

def load_model():
    global llm
    print("Loading Qwen model...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_gpu_layers=-1,
        n_ctx=4096,
        n_batch=512,
        verbose=False,
    )
    print("✅ Model loaded")

ALWAYS_ALLOW = {"hi", "hello", "hey", "yes", "no", "ok", "sure", "thanks"}

def is_hardware_related(user_input, conversation_history=None):
    
    # Greetings always pass through
    if user_input.strip().lower() in ALWAYS_ALLOW:
        return True
    
    # Short follow-ups during active convo always pass
    if conversation_history and len(user_input.split()) <= 4:
        return True
    
    # Build context summary from recent history
    context = ""
    if conversation_history:
        recent = conversation_history[-4:]  # last 4 messages
        context = "Recent conversation:\n"
        for msg in recent:
            context += f"  {msg['role']}: {msg['content']}\n"
        context += "\n"

    check = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a classifier. Reply ONLY with 'yes' or 'no'. No other text."
            },
            {
                "role": "user",
                "content": (
                    f"{context}"
                    f"Given the conversation above, is the latest message part of a discussion "
                    f"about computer parts or hardware (even if it's a short follow-up)?\n"
                    f"Latest message: '{user_input}'"
                )
            }
        ],
        max_tokens=5,
        temperature=0.0,
    )
    answer = check["choices"][0]["message"]["content"].strip().lower()
    return "yes" in answer

def get_response(conversation_history, user_input):
    if not is_hardware_related(user_input):
        return "Sorry, I can only help with computer parts and hardware questions."

    conversation_history.append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.1,
    )

    full_response = response["choices"][0]["message"]["content"]
    conversation_history.append({"role": "assistant", "content": full_response})

    if len(conversation_history) > 20:
        conversation_history[:] = conversation_history[-20:]

    return full_response








# from huggingface_hub import hf_hub_download
# from pathlib import Path

# save_path = Path("./models/mistral-7b")
# save_path.mkdir(parents=True, exist_ok=True)

# print("Downloading Mistral 7B Q4_K_M (~4.1GB)...")

# model_path = hf_hub_download(
#     repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
#     filename="mistral-7b-instruct-v0.2.Q4_K_M.gguf",
#     local_dir=str(save_path),
#     local_dir_use_symlinks=False,
# )

# print(f"✅ Model downloaded to: {model_path}")













# from huggingface_hub import hf_hub_download
# from pathlib import Path

# save_path = Path("./models/qwen2.5-14b")
# save_path.mkdir(parents=True, exist_ok=True)

# print("Downloading Qwen 2.5 14B Q4_K_M (~9GB)...")

# model_path = hf_hub_download(
#     repo_id="bartowski/Qwen2.5-14B-Instruct-GGUF",
#     filename="Qwen2.5-14B-Instruct-Q4_K_M.gguf",
#     local_dir=str(save_path),
# )

# print(f"✅ Model downloaded to: {model_path}")






# from huggingface_hub import hf_hub_download
# from pathlib import Path

# save_path = Path("./models/dolphin-2.6-mistral-7B")
# save_path.mkdir(parents=True, exist_ok=True)

# print("Downloading Dolphin 2.6 Mistral 7B (GGUF)...")


# model_path = hf_hub_download(
#     repo_id="TheBloke/dolphin-2.6-mistral-7B-GGUF",
#     filename="dolphin-2.6-mistral-7b.Q4_K_M.gguf",   # ← corrected filename
#     local_dir=save_path,                             # better to pass Path directly
#     local_dir_use_symlinks=False,                    # recommended for GGUF files
# )

# print(f"✅ Successfully downloaded to:\n{model_path}")




















# from huggingface_hub import hf_hub_download
# from pathlib import Path

# save_path = Path("./models/deepseek-coder-v2-lite")
# save_path.mkdir(parents=True, exist_ok=True)

# print("Downloading DeepSeek-Coder-V2-Lite 16B Q4_K_M (~10GB)...")

# model_path = hf_hub_download(
#     repo_id="bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
#     filename="DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf",
#     local_dir=str(save_path),
# )

# print(f"✅ Downloaded to: {model_path}")



















# from huggingface_hub import hf_hub_download
# from pathlib import Path

# save_path = Path("./models/phi3-mini")
# save_path.mkdir(parents=True, exist_ok=True)

# model_path = hf_hub_download(
#     repo_id="bartowski/Phi-3.1-mini-4k-instruct-GGUF",
#     filename="Phi-3.1-mini-4k-instruct-Q4_K_M.gguf",
#     local_dir=str(save_path),
# )
# print(f"✅ Downloaded to: {model_path}")












# from huggingface_hub import hf_hub_download
# from pathlib import Path

# save_path = Path("./models/seallm-7b")
# save_path.mkdir(parents=True, exist_ok=True)

# model_path = hf_hub_download(
#     repo_id="SeaLLMs/SeaLLM-7B-v2.5-GGUF",
#     filename="seallm-7b-v2.5.Q4_K_M.gguf",
#     local_dir=str(save_path),
# )
# print(f"✅ Downloaded to: {model_path}")











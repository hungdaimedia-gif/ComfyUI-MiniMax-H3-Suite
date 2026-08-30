import os
import sys

# Enable ultra-fast Rust-based hf-transfer
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

from huggingface_hub import hf_hub_download

DOWNLOADS = [
    {
        "repo_id": "molbal/MiniMax-H3-GGUF",
        "filename": "minimax-h3-ref2va-Q4_0.gguf",
        "local_dir": r"G:\ComfyUI\models\unet"
    },
    {
        "repo_id": "joeygambino/MiniMax-H3-encoder-GGUF",
        "filename": "MiniMax-H3-encoder-Q4_K_M.gguf",
        "local_dir": r"G:\ComfyUI\models\text_encoders\MiniMax-H3"
    },
    {
        "repo_id": "joeygambino/MiniMax-H3-encoder-GGUF",
        "filename": "MiniMax-H3-encoder-mmproj-F16.gguf",
        "local_dir": r"G:\ComfyUI\models\text_encoders\MiniMax-H3"
    },
    {
        "repo_id": "Comfy-Org/MiniMax-H3",
        "filename": "vae/minimax_h3_video_vae_fp16.safetensors",
        "local_dir": r"G:\ComfyUI\models\vae"
    },
    {
        "repo_id": "Comfy-Org/MiniMax-H3",
        "filename": "vae/minimax_h3_audio_vae_fp32.safetensors",
        "local_dir": r"G:\ComfyUI\models\vae"
    },
    {
        "repo_id": "lightx2v/Minimax-h3-Turbo",
        "filename": "minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors",
        "local_dir": r"G:\ComfyUI\models\loras\MinimaxH3"
    }
]

print("Starting fast model downloads via Hugging Face Transfer...")
for item in DOWNLOADS:
    repo_id = item["repo_id"]
    filename = item["filename"]
    local_dir = item["local_dir"]
    os.makedirs(local_dir, exist_ok=True)
    print(f"\nDownloading {filename} from {repo_id} -> {local_dir}...")
    try:
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print(f"✓ Successfully downloaded: {path}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Flatten VAE if downloaded into vae/vae/ subdirectory
vae_nested = r"G:\ComfyUI\models\vae\vae"
if os.path.exists(vae_nested):
    for f in os.listdir(vae_nested):
        src = os.path.join(vae_nested, f)
        dst = os.path.join(r"G:\ComfyUI\models\vae", f)
        if not os.path.exists(dst):
            os.replace(src, dst)
            print(f"Moved {f} to G:\\ComfyUI\\models\\vae")
    try:
        os.rmdir(vae_nested)
    except Exception:
        pass

# Also copy/link MiniMax-H3 text encoder to models/clip for compatibility
clip_h3 = r"G:\ComfyUI\models\clip\MiniMax-H3"
os.makedirs(clip_h3, exist_ok=True)
te_dir = r"G:\ComfyUI\models\text_encoders\MiniMax-H3"
if os.path.exists(te_dir):
    for f in os.listdir(te_dir):
        src = os.path.join(te_dir, f)
        dst = os.path.join(clip_h3, f)
        if os.path.isfile(src) and not os.path.exists(dst):
            try:
                import shutil
                shutil.copyfile(src, dst)
                print(f"Copied {f} to clip/MiniMax-H3")
            except Exception as ex:
                print(f"Copy notice: {ex}")

print("\nAll downloads and setup completed!")

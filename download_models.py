import os
import sys
import time
import urllib.request

MODELS = [
    # (Target Dir, Filename, HuggingFace Direct URL)
    (
        r"G:\ComfyUI\models\unet",
        "minimax-h3-ref2va-Q4_0.gguf",
        "https://huggingface.co/molbal/MiniMax-H3-GGUF/resolve/main/minimax-h3-ref2va-Q4_0.gguf"
    ),
    (
        r"G:\ComfyUI\models\text_encoders\MiniMax-H3",
        "MiniMax-H3-encoder-Q4_K_M.gguf",
        "https://huggingface.co/joeygambino/MiniMax-H3-encoder-GGUF/resolve/main/MiniMax-H3-encoder-Q4_K_M.gguf"
    ),
    (
        r"G:\ComfyUI\models\text_encoders\MiniMax-H3",
        "MiniMax-H3-encoder-mmproj-F16.gguf",
        "https://huggingface.co/joeygambino/MiniMax-H3-encoder-GGUF/resolve/main/MiniMax-H3-encoder-mmproj-F16.gguf"
    ),
    (
        r"G:\ComfyUI\models\vae",
        "minimax_h3_video_vae_fp16.safetensors",
        "https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_video_vae_fp16.safetensors"
    ),
    (
        r"G:\ComfyUI\models\vae",
        "minimax_h3_audio_vae_fp32.safetensors",
        "https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors"
    ),
    (
        r"G:\ComfyUI\models\loras\MinimaxH3",
        "minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors",
        "https://huggingface.co/lightx2v/Minimax-h3-Turbo/resolve/main/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors"
    )
]

def download_file(url, out_dir, filename):
    os.makedirs(out_dir, exist_ok=True)
    target_path = os.path.join(out_dir, filename)
    part_path = target_path + ".download"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            total_size = int(resp.headers.get('content-length', 0))
    except Exception as e:
        print(f"Error checking {filename}: {e}")
        return False

    if os.path.exists(target_path) and os.path.getsize(target_path) == total_size and total_size > 0:
        print(f"✓ {filename} already exists ({total_size / (1024*1024):.1f} MB), skipping.")
        return True

    downloaded = 0
    headers = {'User-Agent': 'Mozilla/5.0'}
    if os.path.exists(part_path):
        downloaded = os.path.getsize(part_path)
        if downloaded < total_size:
            headers['Range'] = f'bytes={downloaded}-'
            print(f"Resuming {filename} from {downloaded / (1024*1024):.1f} MB...")
        elif downloaded == total_size:
            os.replace(part_path, target_path)
            print(f"✓ {filename} completed.")
            return True
        else:
            downloaded = 0

    mode = 'ab' if downloaded > 0 else 'wb'
    req = urllib.request.Request(url, headers=headers)
    
    print(f"Downloading {filename} ({total_size / (1024*1024):.1f} MB) -> {target_path}")
    start_time = time.time()
    last_print = start_time
    bytes_since_print = 0

    with urllib.request.urlopen(req) as resp, open(part_path, mode) as f:
        while True:
            chunk = resp.read(1024 * 1024 * 4) # 4MB chunk
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            bytes_since_print += len(chunk)
            now = time.time()
            if now - last_print >= 5.0 or downloaded == total_size:
                speed = (bytes_since_print / (now - last_print)) / (1024 * 1024) if now > last_print else 0
                pct = (downloaded / total_size * 100) if total_size > 0 else 0
                print(f"[{pct:5.1f}%] {filename}: {downloaded/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB ({speed:.1f} MB/s)")
                last_print = now
                bytes_since_print = 0

    os.replace(part_path, target_path)
    print(f"✓ Completed {filename} successfully!\n")
    return True

if __name__ == "__main__":
    print(f"Starting download of {len(MODELS)} models for MiniMax H3 Ref2VA...")
    for out_dir, filename, url in MODELS:
        download_file(url, out_dir, filename)
    print("All models downloaded successfully!")

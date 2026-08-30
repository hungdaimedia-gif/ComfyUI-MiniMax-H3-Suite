# 🎬 MiniMax H3 Ref2VA (4-Step Turbo) ComfyUI Suite

[English](#-english-guide) | [Tiếng Việt](#-hướng-dẫn-tiếng-việt)

---

# 🇬🇧 English Guide

A complete setup suite, automated model download scripts, launcher tools, and original **Workflows** for the **MiniMax H3 Ref2VA (Reference-to-Video/Audio)** multi-modal generation model. 

Specifically optimized to run smoothly on **8GB VRAM GPUs (e.g. RTX 3060 Ti / RTX 4060)** without CUDA Out of Memory (OOM) errors by leveraging **GGUF Q4_0 quantization + 4-Step Turbo LoRA + CPU Text Encoding**.

---

## 📥 1. Model Download Links & Storage Locations

Here are the direct download links from HuggingFace and their exact storage folders inside `ComfyUI/models/`:

| Model Type | File Name | HuggingFace Source Link | Destination Folder in ComfyUI |
| :--- | :--- | :--- | :--- |
| **Diffusion Model (GGUF)** | `minimax-h3-ref2va-Q4_0.gguf` (~10.6 GB) | [molbal/MiniMax-H3-GGUF](https://huggingface.co/molbal/MiniMax-H3-GGUF/resolve/main/minimax-h3-ref2va-Q4_0.gguf) | `ComfyUI/models/unet/` |
| **Text Encoder (GGUF)** | `MiniMax-H3-encoder-Q4_K_M.gguf` (~18.4 GB) | [joeygambino/MiniMax-H3-encoder-GGUF](https://huggingface.co/joeygambino/MiniMax-H3-encoder-GGUF/resolve/main/MiniMax-H3-encoder-Q4_K_M.gguf) | `ComfyUI/models/text_encoders/MiniMax-H3/` *(and `models/clip/MiniMax-H3/`)* |
| **Multimodal Projector** | `MiniMax-H3-encoder-mmproj-F16.gguf` (~1.1 GB) | [joeygambino/MiniMax-H3-encoder-GGUF](https://huggingface.co/joeygambino/MiniMax-H3-encoder-GGUF/resolve/main/MiniMax-H3-encoder-mmproj-F16.gguf) | `ComfyUI/models/text_encoders/MiniMax-H3/` |
| **Video VAE** | `minimax_h3_video_vae_fp16.safetensors` (~4.85 GB) | [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_video_vae_fp16.safetensors) | `ComfyUI/models/vae/` |
| **Audio VAE** | `minimax_h3_audio_vae_fp32.safetensors` (~0.56 GB) | [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors) | `ComfyUI/models/vae/` |
| **4-Step Turbo LoRA** | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` (~1.8 GB) | [lightx2v/Minimax-h3-Turbo](https://huggingface.co/lightx2v/Minimax-h3-Turbo/resolve/main/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors) | `ComfyUI/models/loras/MinimaxH3/` |

> 💡 **Automated Fast Download**: Run `download_hf_fast.py` to download all model weights at maximum speed with automatic multi-threading:
> ```bash
> python download_hf_fast.py
> ```

---

## ⚙️ 2. Golden Parameters & Tuning Guide (Recommended for 8GB VRAM)

To achieve fast generation times (~1-2 minutes per video) without crashing your 8GB GPU:

1. **`Resolution Selector (Size)` Node**:
   * `aspect_ratio`: `16:9 (Widescreen)` or `9:16 (Portrait)` or `1:1`.
   * `megapixels`: **`0.2`** (produces ~608x352, ultra-fast) or **`0.3`** (~736x416).
   * `multiple`: **`32`** *(MUST be 32 or 16; do NOT use arbitrary numbers like 35 to prevent matrix shape mismatch)*.
2. **`Float (Duration)` Node**:
   * `value`: **`2.5`** or **`3.0`** seconds (generates ~60-72 frames at 24fps).
3. **`Select CLIP Device` Node**:
   * `device`: **`cpu`** *(MANDATORY: Text Encoder is ~16.5GB, so it must run in System RAM/CPU to prevent VRAM OOM)*.
4. **`MiniMaxH3ReferenceToVideo` Node**:
   * `ref_image_size`: **`match`** (faster) or **`max`** (preserves maximum reference detail up to 2048px).
5. **`VHS_VideoCombine` Node**:
   * `crf`: **`14` to `19`** (lower values = higher visual fidelity).
   * `pix_fmt`: `yuv420p`.

---

## 📝 3. Standard Prompt Structure for Ref2VA

MiniMax H3 Ref2VA requires structured YAML prompts with `<Picture X>` reference tags:

```yaml
subject_definitions:
- <Picture 1>: An anime female character with expressive eyes and distinctive hairstyle.
- <Picture 2>: A cozy, warm-lit bedroom with a comfortable bed and soft pillows.

summary:
A 3-second gentle anime scene where the female character <Picture 1> is relaxing and lying down comfortably on the bed in the room <Picture 2>.

retention_analysis:
- <Picture 1>: fully_preserved. Character's face, hair color, and anime art style must be strictly maintained.
- <Picture 2>: fully_preserved. Bedroom background, lighting ambiance, and room decorations serve as the consistent environment.

detailed_description:
- [0s-2s]: The camera smoothly glides in a medium shot showing <Picture 1> lying peacefully on the bed (<Picture 2>). Soft sunlight filters through the window, highlighting her hair. She blinks gently and smiles with a relaxed, cozy expression.
- [2s-3s]: <Picture 1> shifts her posture slightly on the pillow, closing her eyes softly as if about to take a peaceful nap. High quality anime animation, smooth movement.

overall_soundscape:
Peaceful ambient room atmosphere, soft rustling of bed sheets, gentle distant birds chirping outside.

non_diegetic_music:
Soft, soothing lofi acoustic piano melody, warm and relaxing mood.
```

---

## 🚀 4. Step-by-Step Installation (English)

1. **Clone this repository**:
   ```bash
   git clone https://github.com/hungdaimedia-gif/ComfyUI-MiniMax-H3-Suite.git
   cd ComfyUI-MiniMax-H3-Suite
   ```

2. **Create Python Environment & Install PyTorch CUDA 12.6**:
   ```bash
   uv venv venv --python 3.11
   uv pip install --python venv/Scripts/python.exe torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
   uv pip install --python venv/Scripts/python.exe -r requirements.txt accelerate qwen-vl-utils "transformers>=4.48.0" bitsandbytes comfy-kitchen gguf tqdm requests huggingface_hub scipy einops safetensors opencv-python-headless soundfile imageio imageio-ffmpeg av aiohttp yarl rich pydantic hf_transfer
   ```

3. **Install Custom Nodes & Download Models**:
   * Run `setup_custom_nodes.bat`
   * Run `venv\Scripts\python.exe download_hf_fast.py`

4. **Launch ComfyUI**:
   * Double-click `run_comfyui.bat` and open `http://127.0.0.1:8188`.
   * Drag & drop any workflow from `workflows/` into the ComfyUI browser canvas.

---

---

# 🇻🇳 Hướng Dẫn Tiếng Việt

Bộ cấu hình, script tự động tải mô hình, công cụ khởi chạy và toàn bộ **Workflows gốc** cho mô hình video đa phương thức **MiniMax H3 Ref2VA (Reference-to-Video/Audio)** — được tối ưu hóa đặc biệt để chạy mượt mà trên **GPU 8GB VRAM (như RTX 3060 Ti / RTX 4060)** mà không bị lỗi tràn bộ nhớ (`CUDA Out of Memory`).

---

## 📥 1. Danh sách Link tải Models (.gguf, .safetensors)

Dưới đây là chi tiết nguồn tải chính thức từ HuggingFace và vị trí đặt file trong thư mục `ComfyUI/models/`:

| Loại Model | Tên File | Nguồn / Link tải HuggingFace | Vị trí đặt file trong ComfyUI |
| :--- | :--- | :--- | :--- |
| **Diffusion Model (GGUF)** | `minimax-h3-ref2va-Q4_0.gguf` (~10.6 GB) | [molbal/MiniMax-H3-GGUF](https://huggingface.co/molbal/MiniMax-H3-GGUF/resolve/main/minimax-h3-ref2va-Q4_0.gguf) | `ComfyUI/models/unet/` |
| **Text Encoder (GGUF)** | `MiniMax-H3-encoder-Q4_K_M.gguf` (~18.4 GB) | [joeygambino/MiniMax-H3-encoder-GGUF](https://huggingface.co/joeygambino/MiniMax-H3-encoder-GGUF/resolve/main/MiniMax-H3-encoder-Q4_K_M.gguf) | `ComfyUI/models/text_encoders/MiniMax-H3/` *(và copy vào `models/clip/MiniMax-H3/`)* |
| **Multimodal Projector** | `MiniMax-H3-encoder-mmproj-F16.gguf` (~1.1 GB) | [joeygambino/MiniMax-H3-encoder-GGUF](https://huggingface.co/joeygambino/MiniMax-H3-encoder-GGUF/resolve/main/MiniMax-H3-encoder-mmproj-F16.gguf) | `ComfyUI/models/text_encoders/MiniMax-H3/` |
| **Video VAE** | `minimax_h3_video_vae_fp16.safetensors` (~4.85 GB) | [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_video_vae_fp16.safetensors) | `ComfyUI/models/vae/` |
| **Audio VAE** | `minimax_h3_audio_vae_fp32.safetensors` (~0.56 GB) | [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors) | `ComfyUI/models/vae/` |
| **4-Step Turbo LoRA** | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` (~1.8 GB) | [lightx2v/Minimax-h3-Turbo](https://huggingface.co/lightx2v/Minimax-h3-Turbo/resolve/main/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors) | `ComfyUI/models/loras/MinimaxH3/` |

> 💡 **Tự động tải nhanh**: Bạn chỉ cần chạy script `download_hf_fast.py`, hệ thống sẽ tự động tải đa luồng tốc độ cao và đặt đúng thư mục:
> ```bash
> python download_hf_fast.py
> ```

---

## ⚙️ 2. Các thông số CẤU HÌNH VÀNG (Khuyên dùng cho GPU 8GB VRAM)

Để mô hình render video mượt mà, chất lượng cao và chỉ mất **1 - 2 phút/video** trên card 8GB VRAM (RTX 3060 Ti):

### 1️⃣ Node `Resolution Selector (Size)`
* **`aspect_ratio`**: `16:9 (Widescreen)` (Video ngang) hoặc `9:16` (Video dọc) hoặc `1:1`.
* **`megapixels`**: **`0.2`** (Độ phân giải ~608 x 352, render siêu nhanh) hoặc **`0.3`** (~736 x 416).
* **`multiple`**: **`32`** *(BẮT BUỘC đặt là 32 hoặc 16; KHÔNG đặt số lẻ như 35 để tránh lỗi)*.

### 2️⃣ Node `Float (Duration)`
* **`value`**: Đặt **`2.5`** hoặc **`3.0`** giây (vừa đủ mượt mà không làm nặng RAM).

### 3️⃣ Node `Select CLIP Device`
* **`device`**: **`cpu`** *(BẮT BUỘC chọn `cpu` vì Text Encoder nặng tới 16.5GB, chạy trên RAM hệ thống để không tràn 8GB VRAM)*.

### 4️⃣ Node `MiniMaxH3ReferenceToVideo`
* **`ref_image_size`**: Chọn **`match`** (nhanh) hoặc **`max`** (giữ độ sắc nét khuôn mặt và trang phục tối đa).

### 5️⃣ Node `VHS_VideoCombine` (Xuất Video)
* **`crf`**: Đặt từ **`14` đến `19`** (Số càng nhỏ video xuất ra càng mịn, nét cao).
* **`pix_fmt`**: `yuv420p`.

---

## 🚀 3. Hướng dẫn cài đặt chi tiết (Tiếng Việt)

1. **Clone repository này về máy**:
   ```bash
   git clone https://github.com/hungdaimedia-gif/ComfyUI-MiniMax-H3-Suite.git
   cd ComfyUI-MiniMax-H3-Suite
   ```

2. **Tạo môi trường Python & Cài đặt PyTorch CUDA 12.6**:
   ```bash
   uv venv venv --python 3.11
   uv pip install --python venv/Scripts/python.exe torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
   uv pip install --python venv/Scripts/python.exe -r requirements.txt accelerate qwen-vl-utils "transformers>=4.48.0" bitsandbytes comfy-kitchen gguf tqdm requests huggingface_hub scipy einops safetensors opencv-python-headless soundfile imageio imageio-ffmpeg av aiohttp yarl rich pydantic hf_transfer
   ```

3. **Cài đặt Custom Nodes & Tải Model**:
   * Nhấp đúp chạy `setup_custom_nodes.bat`
   * Chạy `venv\Scripts\python.exe download_hf_fast.py` để tải toàn bộ model weights.

4. **Khởi chạy**:
   * Nhấp đúp vào `run_comfyui.bat` và mở trình duyệt tại `http://127.0.0.1:8188`.
   * Kéo thả file workflow trong thư mục `workflows/` vào giao diện ComfyUI để tạo video.

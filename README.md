# MiniMax H3 Ref2VA (4-Step Turbo) ComfyUI Suite

Bộ cấu hình, công cụ khởi chạy, script tự động tải mô hình và toàn bộ Workflow gốc cho **MiniMax H3 Ref2VA (Reference-to-Video/Audio)** tối ưu hóa trên GPU 8GB VRAM (như RTX 3060 Ti) sử dụng **GGUF Q4_0 + 4-Step Turbo LoRA**.

---

## 📁 Cấu trúc thư mục

* **`workflows/`**: Chứa 2 file Workflow JSON gốc:
  * `MMH3_Ref2v+MediaLoader_260827.json`: Workflow nạp qua Media Loader đa phương thức.
  * `MMH3_Ref2V_Nomal-Input_260827.json`: Workflow trực quan từng đầu vào riêng lẻ.
* **`download_hf_fast.py`**: Script tải toàn bộ model weights (UNet GGUF, Text Encoder GGUF, VAE, LoRA Turbo) từ HuggingFace tốc độ cao.
* **`run_comfyui.bat`**: File khởi chạy ComfyUI với tham số tối ưu VRAM.
* **`open_prompt_generator.bat`**: Mở công cụ tạo prompt chuyên dụng cho MiniMax H3.
* **`setup_custom_nodes.bat`**: Tự động clone 8 bộ custom nodes cần thiết.

---

## 🚀 Hướng dẫn cài đặt nhanh trên máy mới

1. **Clone repository này**:
   ```bash
   git clone <REPO_URL>
   cd ComfyUI
   ```

2. **Cài đặt môi trường Python**:
   ```bash
   uv venv venv --python 3.11
   uv pip install --python venv/Scripts/python.exe torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
   uv pip install --python venv/Scripts/python.exe -r requirements.txt accelerate qwen-vl-utils "transformers>=4.48.0" bitsandbytes comfy-kitchen gguf tqdm requests huggingface_hub scipy einops safetensors opencv-python-headless soundfile imageio imageio-ffmpeg av aiohttp yarl rich pydantic hf_transfer
   ```

3. **Cài đặt Custom Nodes & Tải Models**:
   * Chạy `setup_custom_nodes.bat` để nạp các node mở rộng.
   * Chạy `venv\Scripts\python.exe download_hf_fast.py` để tải các mô hình về đúng thư mục.

4. **Khởi chạy**:
   * Nhấp đúp vào `run_comfyui.bat` và truy cập `http://127.0.0.1:8188`.
   * Kéo thả file workflow trong thư mục `workflows/` vào ComfyUI để sử dụng.

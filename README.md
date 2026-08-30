# 🎬 MiniMax H3 Ref2VA (4-Step Turbo) ComfyUI Suite

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

> 💡 **Mẹo tải nhanh**: Bạn chỉ cần chạy script `download_hf_fast.py` (đã tích hợp sẵn `hf-transfer` đa luồng), script sẽ tự động tải toàn bộ các file trên và đặt vào đúng thư mục:
> ```bash
> python download_hf_fast.py
> ```

---

## ⚙️ 2. Các thông số CẤU HÌNH VÀNG đã tối ưu (Khuyên dùng cho GPU 8GB VRAM)

Để mô hình render video mượt mà, chất lượng cao và chỉ mất **1 - 2 phút/video** trên card 8GB VRAM (RTX 3060 Ti), bạn hãy thiết lập các thông số sau trên giao diện ComfyUI:

### 1️⃣ Node `Resolution Selector (Size)`
* **`aspect_ratio`**: `16:9 (Widescreen)` (Video ngang) hoặc `9:16` (Video dọc TikTok/Reels) hoặc `1:1`.
* **`megapixels`**: **`0.2`** (Độ phân giải ~608 x 352, render siêu nhanh) hoặc **`0.3`** (~736 x 416) hoặc **`0.4`** (~864 x 480).
* **`multiple`**: **`32`** *(BẮT BUỘC đặt là 32 hoặc 16; KHÔNG đặt các số lẻ như 35 để tránh lỗi kích thước ma trận)*.

### 2️⃣ Node `Float (Duration)`
* **`value`**: Đặt **`2.5`** hoặc **`3.0`** giây cho mỗi đoạn video ngắn (đủ để tạo chuyển động tự nhiên mà không làm quá tải băng thông PCIe).

### 3️⃣ Node `Select CLIP Device`
* **`device`**: **`cpu`** *(BẮT BUỘC giữ `cpu` vì Text Encoder nặng tới 16.5GB, xử lý trên CPU/RAM hệ thống để tránh lỗi tràn 8GB VRAM)*.

### 4️⃣ Node `MiniMaxH3ReferenceToVideo`
* **`ref_image_size`**: Chọn **`match`** (nhanh) hoặc **`max`** (giữ độ sắc nét khuôn mặt và chi tiết trang phục gốc tối đa).

### 5️⃣ Node `VHS_VideoCombine` (Xuất Video)
* **`crf`**: Đặt từ **`14` đến `19`** (Số càng nhỏ video xuất ra càng mịn, ít nén).
* **`pix_fmt`**: `yuv420p`.

---

## 📝 3. Cấu trúc Prompt chuẩn cho MiniMax H3 Ref2VA

Mô hình Ref2VA yêu cầu prompt có cấu trúc thẻ tag rõ ràng (English hoặc Japanese kèm tag `<Picture X>`) để nhận diện ảnh tham chiếu:

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

## 🚀 4. Hướng dẫn cài đặt trên máy mới (Từ A đến Z)

1. **Clone repository**:
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
   * Chạy `venv\Scripts\python.exe download_hf_fast.py` để tự động tải các file model.

4. **Khởi chạy**:
   * Nhấp đúp vào `run_comfyui.bat` và mở trình duyệt tại `http://127.0.0.1:8188`.
   * Kéo thả file workflow trong thư mục `workflows/` vào ComfyUI để sử dụng.

@echo off
title Install Custom Nodes for MiniMax H3 Ref2VA
echo Cloning required Custom Nodes...

cd /d G:\ComfyUI\custom_nodes
git clone --depth 1 https://github.com/ltdrdata/ComfyUI-Manager.git
git clone --depth 1 https://github.com/city96/ComfyUI-GGUF.git
git clone --depth 1 https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo.git
git clone --depth 1 https://github.com/Adudeguyman/ComfyUI-Fantastic-MiniMaxH3-PromptBuilder.git
git clone --depth 1 https://github.com/jlucasmcrell/ComfyUI-H3-Multishot.git
git clone --depth 1 https://github.com/rgthree/rgthree-comfy.git
git clone --depth 1 https://github.com/kijai/ComfyUI-KJNodes.git
git clone --depth 1 https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git

echo All custom nodes installed successfully!
pause

@echo off
title ComfyUI - MiniMax H3 Ref2VA
echo ========================================================
echo   Starting ComfyUI for MiniMax H3 Ref2VA (4-Step Turbo)
echo   GPU: NVIDIA GeForce RTX 3060 Ti (8GB VRAM)
echo ========================================================
cd /d G:\ComfyUI
call venv\Scripts\activate.bat
python main.py --windows-standalone-build --preview-method auto --auto-launch
pause

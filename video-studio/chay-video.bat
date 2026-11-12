@echo off
rem Windows 11: bấm đúp để dựng video từ videos\demo.json bằng HyperFrames.
rem Cần cài trước: Node.js 22, FFmpeg, Git for Windows (có sẵn bash).
cd /d "%~dp0"
call npm install --no-audit --no-fund
bash scripts/render.sh videos/demo.json hyperframes
echo.
echo Xong. Video nam trong thu muc out\
pause

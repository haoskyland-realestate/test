@echo off
rem Windows 11: bấm đúp để mở app timeline. Điện thoại cùng wifi mở link "Điện thoại" in ra.
rem Cần đã chạy setup-windows.ps1 một lần (Python, Node, FFmpeg) và npm install.
cd /d "%~dp0"
python studio\server.py --lan
pause

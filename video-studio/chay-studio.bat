@echo off
rem Windows 11: bấm đúp để mở app timeline. Điện thoại cùng wifi mở link "Điện thoại" in ra.
rem Luôn chạy bằng Python riêng của dự án (.venv, tạo bởi setup-windows.ps1 từ Python 3.12), không dùng Python mặc định của Windows.
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
set PY=.venv\Scripts\python.exe
if not exist "%PY%" (
  echo Chua co moi truong Python cua du an ^(.venv^). Mo PowerShell trong thu muc nay va chay: .\setup-windows.ps1
  pause
  exit /b 1
)
"%PY%" scripts\kiem_may.py
echo.
"%PY%" studio\server.py --lan
pause

@echo off
rem Windows 11: bam dup de lay video "no" cua cac kenh trong nghien-cuu\kenh.txt (moi kenh chi lay 1 lan / 7 ngay).
rem Ket qua: nghien-cuu\ket-qua\<kenh>_<ngay>.md. Muon lay lai ngay: nghien-cuu-tiktok.bat --ep
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
set PY=.venv\Scripts\python.exe
if not exist "%PY%" (
  echo Chua co moi truong Python cua du an ^(.venv^). Mo PowerShell trong thu muc nay va chay: .\setup-windows.ps1
  pause
  exit /b 1
)
"%PY%" -m pip install -q -U yt-dlp
"%PY%" scripts\nghien_cuu_tiktok.py --danh-sach nghien-cuu\kenh.txt %*
pause

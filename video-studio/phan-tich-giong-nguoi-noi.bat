@echo off
rem Windows 11: bam dup de lay cach noi cua kenh Khoai Lang Thang (phong cach Hao muon huong toi).
rem Ket qua: nghien-cuu\phong-cach\khoailangthang.md  (mat khoang 5-10 phut). Kenh khac: phan-tich-giong-nguoi-noi.bat <link kenh>/videos
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
set PY=.venv\Scripts\python.exe
if not exist "%PY%" (
  echo Chua co moi truong Python cua du an ^(.venv^). Mo PowerShell trong thu muc nay va chay: .\setup-windows.ps1
  pause
  exit /b 1
)
set URL=%1
if "%URL%"=="" set URL=https://www.youtube.com/@khoailangthang/videos
"%PY%" -m pip install -q -U yt-dlp
"%PY%" scripts\phan_tich_giong_nguoi_noi.py %URL%
pause

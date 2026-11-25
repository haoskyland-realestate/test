@echo off
rem Windows 11: bam dup de lay loi thoai 4 kenh YouTube (Khoai Lang Thang, Thien Bao, An Truong, Coach Duy Nguyen).
rem Mat khoang 15-25 phut. Ket qua: thu muc nghien-cuu\phong-cach\ (4 file .md). Xong, gui cac file nay cho Claude.
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
echo === 1/4 Khoai Lang Thang (phong cach chinh) ===
"%PY%" scripts\phan_tich_giong_nguoi_noi.py https://www.youtube.com/@khoailangthang/videos --so 6 --giua 6 --do-dai 150
echo === 2/4 Thien Bao BDS ===
"%PY%" scripts\phan_tich_giong_nguoi_noi.py https://www.youtube.com/@thienbaobds/videos --so 4
echo === 3/4 An Truong Real Estate ===
"%PY%" scripts\phan_tich_giong_nguoi_noi.py https://www.youtube.com/@antruongrealestate/videos --so 4
echo === 4/4 Coach Duy Nguyen (tieng Anh) ===
"%PY%" scripts\phan_tich_giong_nguoi_noi.py https://www.youtube.com/@coachduynguyen/videos --so 4 --ngon-ngu "en.*,en"
echo.
echo XONG. Gui cac file trong nghien-cuu\phong-cach\ cho Claude.
pause

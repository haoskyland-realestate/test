@echo off
chcp 65001 >nul
rem Thử cả quy trình (tạo dự án → master cut → phụ đề → bản xem → nháp → bản cuối → kiểm) trên một dự án mới, ghi BAO-CAO-THU.md
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (
  echo Chưa cài: chạy setup-windows.ps1 trước.
  pause
  exit /b 1
)
set /p NGUON=Dán thư mục video hoặc tên dự án có sẵn (vd 2026-11-20_tiktok_): 
set /p NHANH=Chỉ thử 3 video đầu cho nhanh? (c/k): 
if /i "%NHANH%"=="c" (
  ".venv\Scripts\python.exe" scripts\thu_quy_trinh.py "%NGUON%" --nhanh
) else (
  ".venv\Scripts\python.exe" scripts\thu_quy_trinh.py "%NGUON%"
)
echo.
echo Gửi Claude file BAO-CAO-THU.md (đường dẫn ở dòng "Báo cáo:" phía trên).
pause

@echo off
rem Windows 11: bấm đúp để mở app timeline. Điện thoại cùng wifi mở link "Điện thoại" in ra.
rem Cần đã chạy setup-windows.ps1 một lần.
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py
%PY% scripts\kiem_may.py
echo.
%PY% studio\server.py --lan
pause

# Windows 11: chạy MỘT lần. Mở PowerShell trong thư mục video-studio rồi gõ:  .\setup-windows.ps1
# (Nếu báo "running scripts is disabled": gõ trước  Set-ExecutionPolicy -Scope Process Bypass)
# Cài Node.js, FFmpeg, Git, Python bằng winget (có sẵn trong Windows 11), cài thư viện của dự án, rồi kiểm máy.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
foreach ($id in "OpenJS.NodeJS.LTS", "Gyan.FFmpeg", "Git.Git", "Python.Python.3.12") {
  winget install --id $id -e --accept-package-agreements --accept-source-agreements
  if ($LASTEXITCODE -ne 0) { Write-Host "  (${id}: đã có sẵn hoặc winget báo mã $LASTEXITCODE, đi tiếp)" }
}
# Python ghi/đọc tiếng Việt đúng (mặc định Windows dùng bảng mã cp1252, làm lỗi chữ có dấu)
[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User"); $env:PYTHONUTF8 = "1"
# Nạp lại PATH để dùng ngay công cụ vừa cài, không cần mở lại cửa sổ
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
$ErrorActionPreference = "Continue"
npm install
# MỘT Python cố định cho cả dự án: .venv tạo từ Python 3.12 (không phụ thuộc "python"/"py" mặc định của Windows,
# vốn có thể là 3.13/3.14 hoặc lối tắt Microsoft Store). --system-site-packages: dùng lại thư viện đã cài trong 3.12, không cài trùng.
$PYX = ".venv\Scripts\python.exe"
if (-not (Test-Path $PYX)) {
  if (-not (Get-Command py -ErrorAction SilentlyContinue)) { Write-Host "Không thấy trình chạy 'py'. Cài Python 3.12: winget install Python.Python.3.12, rồi chạy lại."; exit 1 }
  py -3.12 -m venv --system-site-packages .venv
  if (-not (Test-Path $PYX)) { Write-Host "Không tạo được .venv bằng Python 3.12 (py -3.12). Kiểm: py -0p"; exit 1 }
}
& $PYX -m pip install --upgrade pip
# pip bỏ qua gói đã có ("Requirement already satisfied"), chỉ cài gói còn thiếu
& $PYX -m pip install numpy faster-whisper "opencv-python-headless<5" opentimelineio otio-fcp-adapter onnxruntime yt-dlp playwright
Write-Host ""
Write-Host "Kiểm máy và dựng thử video giả 6 giây (1–3 phút):"
& $PYX scripts\kiem_may.py --dung-thu
Write-Host ""
Write-Host "Nếu dòng cuối là 'Máy đủ điều kiện chạy app.': bấm đúp chay-studio.bat để mở app."
Write-Host "Nếu còn THIẾU: đóng PowerShell, mở lại, chạy lại .\setup-windows.ps1 (lần sau nhanh hơn), hoặc chụp màn hình gửi Claude."

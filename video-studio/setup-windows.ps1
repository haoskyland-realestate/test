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
# Ưu tiên "py" (trình chạy Python thật): "python" có thể là lối tắt mở Microsoft Store
# Luôn dùng Python 3.12: bản mới hơn (3.13/3.14) có thể chưa có gói faster-whisper/opencv, cài hỏng cả lượt
function Py { if (Get-Command py -ErrorAction SilentlyContinue) { py -3.12 @args } else { python @args } }
$ErrorActionPreference = "Continue"
npm install
if (Test-Path ..\.git) { git submodule update --init --depth 1 }  # bản zip không có git: bỏ qua
Py -m pip install numpy faster-whisper "opencv-python-headless<5" opentimelineio otio-fcp-adapter onnxruntime
Write-Host ""
Write-Host "Kiểm máy và dựng thử video giả 6 giây (1–3 phút):"
Py scripts\kiem_may.py --dung-thu
Write-Host ""
Write-Host "Nếu dòng cuối là 'Máy đủ điều kiện chạy app.': bấm đúp chay-studio.bat để mở app."
Write-Host "Nếu còn THIẾU: đóng PowerShell, mở lại, chạy lại .\setup-windows.ps1 (lần sau nhanh hơn), hoặc chụp màn hình gửi Claude."

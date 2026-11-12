# Windows 11: chạy MỘT lần. Mở PowerShell trong thư mục video-studio rồi gõ:  .\setup-windows.ps1
# Cài Node.js, FFmpeg, Git, Python bằng winget (có sẵn trong Windows 11), rồi cài thư viện của dự án.
$ErrorActionPreference = "Stop"
foreach ($id in "OpenJS.NodeJS.LTS", "Gyan.FFmpeg", "Git.Git", "Python.Python.3.12") {
  winget install --id $id -e --accept-package-agreements --accept-source-agreements
}
Write-Host "Đóng PowerShell, mở lại, rồi chạy tiếp (trong thư mục video-studio):"
Write-Host "  npm install"
Write-Host "  pip install numpy faster-whisper     (phụ đề tự động; lần đầu tạo phụ đề tải mô hình ~1,6 GB)"
Write-Host "Xong thì bấm đúp chay-studio.bat để mở app."

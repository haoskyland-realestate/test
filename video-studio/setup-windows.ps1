# Windows 11: chạy MỘT lần. Mở PowerShell trong thư mục video-studio rồi gõ:  .\setup-windows.ps1
# Cài Node.js, FFmpeg, Git, Python bằng winget (có sẵn trong Windows 11), rồi cài thư viện của dự án.
$ErrorActionPreference = "Stop"
foreach ($id in "OpenJS.NodeJS.LTS", "Gyan.FFmpeg", "Git.Git", "Python.Python.3.12") {
  winget install --id $id -e --accept-package-agreements --accept-source-agreements
}
Write-Host "Đóng PowerShell, mở lại, rồi chạy tiếp: npm install  và bấm đúp chay-video.bat"

#!/bin/bash
# MacBook (Apple M1 trở lên): cài một lần. Trong Terminal, ở thư mục video-studio:  bash setup-mac.sh
# Cài Homebrew (nếu chưa có), Node, FFmpeg, Python; thư viện dự án vào .venv (không đụng Python của máy); rồi kiểm máy + dựng thử 6 giây.
set -e
cd "$(dirname "$0")"
if ! command -v brew >/dev/null; then
  echo "== Cài Homebrew (sẽ hỏi mật khẩu máy Mac) =="
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi
echo "== Cài Node, FFmpeg, Python =="
# ffmpeg thường của Homebrew (từ 01/2026) thiếu bộ lọc zscale → dùng ffmpeg-full (không tự vào PATH nên thêm tay)
brew install node ffmpeg-full python@3.12
export PATH="$(brew --prefix ffmpeg-full)/bin:$PATH"
echo "== Thư viện chữ động (npm) =="
npm install
echo "== Thư viện Python (vào .venv) =="
"$(brew --prefix python@3.12)/bin/python3.12" -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install numpy faster-whisper "opencv-python-headless<5" opentimelineio otio-fcp-adapter onnxruntime
echo "== Kiểm máy + dựng thử 6 giây (1–3 phút) =="
.venv/bin/python scripts/kiem_may.py --dung-thu
echo
echo "Xong. Từ giờ mở app: bấm đúp file chay-studio.command (hoặc: bash chay-studio.command)."

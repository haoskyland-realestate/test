#!/bin/bash
# MacBook: bấm đúp để mở app timeline (cần đã chạy setup-mac.sh một lần). Mở đúng link có ?t= in ra.
cd "$(dirname "$0")"
export PATH="$(/opt/homebrew/bin/brew --prefix ffmpeg-full 2>/dev/null)/bin:/opt/homebrew/bin:$PATH"
.venv/bin/python scripts/kiem_may.py
echo
.venv/bin/python studio/server.py --lan

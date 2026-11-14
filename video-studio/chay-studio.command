#!/bin/bash
# MacBook: bấm đúp để mở app timeline (cần đã chạy setup-mac.sh một lần). Mở đúng link có ?t= in ra.
cd "$(dirname "$0")"
.venv/bin/python scripts/kiem_may.py
echo
.venv/bin/python studio/server.py --lan

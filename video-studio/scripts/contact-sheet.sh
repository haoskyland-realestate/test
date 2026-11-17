#!/usr/bin/env bash
# Dùng: scripts/contact-sheet.sh <video> [giây giữa các khung=4]  -> <video>.sheet.jpg
# Ảnh lưới các khung hình để chọn cảnh (mỗi ô có mốc giây) mà không phải xem cả video.
set -euo pipefail
V=$1; EVERY=${2:-4}
ffmpeg -y -loglevel error -i "$V" -vf "fps=1/$EVERY,scale=320:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x6" -frames:v 1 "${V%.*}.sheet.jpg"
echo "Xong: ${V%.*}.sheet.jpg"

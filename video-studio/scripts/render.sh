#!/usr/bin/env bash
# Dùng: scripts/render.sh videos/demo.json [hyperframes|remotion|manim]
# Ra: out/<tên>.<engine>.raw.mp4  ->  FFmpeg  ->  out/<tên>.<engine>.mp4 (chuẩn TikTok/YouTube)
set -euo pipefail
cd "$(dirname "$0")/.."
SPEC=$1
ENGINE=${2:-$(node -p "require('./$SPEC').engine")}
NAME=$(basename "$SPEC" .json)
PLATFORM=$(node -p "require('./$SPEC').platform")
mkdir -p out
RAW="$PWD/out/$NAME.$ENGINE.raw.mp4"

case "$ENGINE" in
  hyperframes)
    node scripts/build-hyperframes.mjs "$SPEC"
    (cd engines/hyperframes/dist && npx --yes hyperframes@0.9.37 render -o "$RAW" -q delivery --quiet) ;;
  remotion)
    (cd engines/remotion && npm install --no-audit --no-fund >/dev/null &&
     npx remotion render src/index.jsx Main "$RAW" --props="../../$SPEC" ${BROWSER:+--browser-executable=$BROWSER}) ;;
  manim)
    SPEC="$SPEC" python3 -m manim -qm --format=mp4 -o "$NAME.manim" --media_dir out/manim engines/manim/scene.py Main
    cp "$(find out/manim -name "$NAME.manim.mp4" | head -1)" "$RAW" ;;
  *) echo "engine lạ: $ENGINE" >&2; exit 1 ;;
esac

# FFmpeg: ép đúng khung hình, H.264 + faststart để đăng thẳng lên TikTok/YouTube.
if [ "$PLATFORM" = youtube ]; then S="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"
else S="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"; fi
ffmpeg -y -loglevel error -i "$RAW" -vf "$S,fps=30" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -movflags +faststart "out/$NAME.$ENGINE.mp4"
echo "Xong: out/$NAME.$ENGINE.mp4"

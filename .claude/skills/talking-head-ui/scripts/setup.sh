#!/usr/bin/env bash
# Cài công cụ cho một dự án talking-head-ui. Dùng: bash setup.sh <projectDir>
set -euo pipefail
PROJ="${1:-.}"
mkdir -p "$PROJ/assets/broll" "$PROJ/assets/fonts" "$PROJ/compositions" "$PROJ/work"
cd "$PROJ"
[ -f package.json ] || npm init -y >/dev/null
npm install --no-audit --no-fund hyperframes gsap @fontsource/montserrat @fontsource/inter @fontsource/playfair-display >/dev/null
command -v ffmpeg >/dev/null || { echo "Thiếu ffmpeg"; exit 1; }
npx hyperframes telemetry disable >/dev/null 2>&1 || true
echo "OK: $(npx hyperframes --version 2>/dev/null | tail -1)"

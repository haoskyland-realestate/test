#!/usr/bin/env bash
# Gửi bản tin sang Telegram. Dùng: gui_telegram.sh sang|toi|thu|chat_id   (DRY_RUN=1: chỉ in, không gửi)
# Cần biến môi trường TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID (GitHub Secrets), không bao giờ ghi vào file.
# Bản tin lấy từ nghien-cuu/ban-tin/<sang|toi>.txt, dòng đầu "NGAY: YYYY-MM-DD". Sai ngày thì gửi cảnh báo, không gửi tin cũ.
set -euo pipefail
loai="${1:-thu}"
cd "$(dirname "$0")/.."
hom_nay=$(TZ=Asia/Ho_Chi_Minh date +%F)
tmp=$(mktemp)
# Dán secret hay dính dấu cách hoặc xuống dòng ở cuối: bỏ hết khoảng trắng.
TELEGRAM_BOT_TOKEN=$(printf %s "${TELEGRAM_BOT_TOKEN:-}" | tr -d '[:space:]')
TELEGRAM_CHAT_ID=$(printf %s "${TELEGRAM_CHAT_ID:-}" | tr -d '[:space:]')

api() {
  [ -n "$TELEGRAM_BOT_TOKEN" ] || { echo "Chưa có secret TELEGRAM_BOT_TOKEN" >&2; exit 1; }
  curl -sS --fail-with-body -m 30 "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/$1" "${@:2}" \
    || { echo "Telegram từ chối. Thường do token sai, hoặc đã bị /revoke. Tạo lại secret TELEGRAM_BOT_TOKEN bằng mã mới nhất." >&2; exit 1; }
}
gui() {
  if [ "${DRY_RUN:-}" = 1 ]; then cat "$tmp"; return; fi
  api sendMessage --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" --data-urlencode "text@$tmp" -o /dev/null
}

case "$loai" in
  chat_id)
    api getUpdates | python3 -c '
import json, sys
ids = {u["message"]["chat"]["id"] for u in json.load(sys.stdin)["result"] if "message" in u}
print("chat id:", *ids) if ids else print("Chưa thấy tin nào: nhắn bot một câu rồi chạy lại")' ;;
  thu)
    echo "Thử kết nối: trợ lý content của Hào gửi được tin lúc $(TZ=Asia/Ho_Chi_Minh date '+%H:%M %d/%m/%Y')." > "$tmp"
    gui ;;
  sang|toi)
    f="nghien-cuu/ban-tin/$loai.txt"
    if [ -f "$f" ] && [ "$(head -1 "$f")" = "NGAY: $hom_nay" ]; then
      tail -n +2 "$f" > "$tmp"
    else
      printf 'Chưa có bản tin %s cho ngày %s: trợ lý chưa kịp chuẩn bị. Hào xem Google Sheet, hoặc nhắn trợ lý chạy lại.\n' "$loai" "$hom_nay" > "$tmp"
    fi
    gui ;;
  *) echo "dùng: sang|toi|thu|chat_id" >&2; exit 2 ;;
esac
rm -f "$tmp"

"""Tải hiệu ứng âm MIỄN PHÍ từ Mixkit vào kho (thu-vien-am-thanh/): mỗi file ghi nguồn, đường dẫn, ngày tải, giấy phép.
Mixkit nói rõ (mixkit.co/llm-info/): miễn phí, không cần ghi nguồn, không cần đăng ký, dùng được cho video thương mại. Toàn văn
"Sound Effects Free License" nằm trong cửa sổ động trên mixkit.co/license/ — Hào đọc trước khi đăng. Không bán lại file riêng lẻ.
Chạy trong video-studio:  python3 scripts/tai_sfx_mien_phi.py            (mỗi nhóm 3 âm, ≤ 3 giây)
                          python3 scripts/tai_sfx_mien_phi.py whoosh 5    (một nhóm, số âm)      ·   tự kiểm: --tu-kiem
Cần mạng tới mixkit.co và assets.mixkit.co. Âm tải về vào hieu-ung.json như âm tổng hợp (cùng dùng trong mẫu và app)."""
import datetime, html, json, os, re, subprocess, sys, urllib.request

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
KHO = os.path.join(ROOT, "thu-vien-am-thanh")
# thẻ Mixkit → (nhóm trong kho, dùng khi)
NHOM = {"whoosh": ("whoosh", "Chuyển cảnh, chữ bay vào"), "impact": ("impact", "Chữ lớn chạm, nhấn ý"), "transition": ("whoosh", "Chuyển cảnh"),
        "click": ("chu", "Chữ hiện, nút bấm"), "pop": ("chu", "Chữ nảy lên, thẻ xuất hiện"), "notification": ("ting", "Số liệu, thông báo, thẻ"),
        "glitch": ("glitch", "Chữ giải mã, nhiễu hình"), "riser": ("riser", "Tăng dần trước chuyển cảnh mạnh")}
MAX_GIAY = 3.0


def lay(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()


def doc_trang(slug):
    t = lay(f"https://mixkit.co/free-sound-effects/{slug}/").decode("utf8", "ignore")
    out = []
    for m in re.finditer(r'data-audio-player-item-id-value="(\d+)"', t):
        s = t[m.end(): m.end() + 3500]
        ten = re.search(r'item-grid-card__title">\s*([^<]+?)\s*<', s)
        if ten and (m.group(1), html.unescape(ten.group(1))) not in out:
            out.append((m.group(1), html.unescape(ten.group(1))))
    return out


def slug_ten(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:24] or "am"


def phan_tich(wav):
    """(độ dài giây, điểm nhấn giây = lúc to nhất)."""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", wav, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 320
    e = np.sqrt(np.convolve(x * x, np.ones(hop) / hop, "valid")[::hop])
    return round(len(x) / 16000, 2), round(float(np.argmax(e)) * hop / 16000, 2)


def tai(slug, n):
    cat = json.load(open(os.path.join(KHO, "hieu-ung.json"), encoding="utf8"))
    nhom, dung = NHOM[slug]
    them = []
    for id_, ten in doc_trang(slug):
        if len(them) >= n:
            break
        ma = f"mixkit-{id_}"
        if any(v.get("nguon", "").startswith(f"Mixkit {id_} ") for v in cat.values()):
            continue
        tam = os.path.join(KHO, "hieu-ung", f".tam-{id_}.wav")
        try:
            open(tam, "wb").write(lay(f"https://assets.mixkit.co/active_storage/sfx/{id_}/{id_}.wav"))
        except OSError as ex:  # một số âm không có bản .wav công khai: bỏ qua, lấy âm khác
            print(f"  bỏ qua {id_} ({ten}): {ex}")
            if os.path.exists(tam):
                os.remove(tam)
            continue
        dai, nhan = phan_tich(tam)
        if dai > MAX_GIAY or dai < 0.15:
            os.remove(tam); continue
        so = 1 + sum(1 for k in cat if k.startswith(f"{nhom}_{slug_ten(ten)}_"))
        key = f"{nhom}_{slug_ten(ten)}_{so:02d}"
        pk = subprocess.run(["ffmpeg", "-nostdin", "-i", tam, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
        mv = re.search(r"max_volume: (-?[\d.]+) dB", pk)
        gain = -3.0 - float(mv.group(1)) if mv else 0.0  # đỉnh về −3 dB cho đồng đều
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", tam, "-af", f"volume={gain:.2f}dB", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le",
                        os.path.join(KHO, "hieu-ung", key + ".wav")], check=True)
        os.remove(tam)
        cat[key] = {"nhom": nhom, "vi": f"{ten} {dai:g} s", "dung_khi": dung, "dai": dai, "diem_nhan": nhan,
                    "nguon": f"Mixkit {id_} https://mixkit.co/free-sound-effects/{slug}/ (Sound Effects Free License, tải {datetime.date.today().isoformat()})"}
        them.append(key)
    json.dump(cat, open(os.path.join(KHO, "hieu-ung.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    return them


def _tu_kiem():
    assert slug_ten("Metal hit woosh!") == "metal-hit-woosh" and NHOM["whoosh"][0] == "whoosh"
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        w = os.path.join(t, "a.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=f=440:d=0.5", "-af", "volume='if(lt(t,0.3),0.1,1)':eval=frame", w], check=True)
        d, nh = phan_tich(w)
        assert abs(d - 0.5) < 0.05 and nh >= 0.29, (d, nh)  # to nhất sau 0,3 s
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    else:
        ds = [(sys.argv[1], int(sys.argv[2]))] if len(sys.argv) >= 3 else [(s, 3) for s in NHOM]
        for slug, n in ds:
            print(slug, "→", ", ".join(tai(slug, n)) or "(không thêm âm nào)")

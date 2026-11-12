"""Kho hiệu ứng âm (thu-vien-am-thanh/) và trộn hàng "sfx" của timeline thành một file âm thanh.
Mục sfx trong timeline.json: {"start": giây bắt đầu phát file, "dur": độ dài file, "file": "whoosh_zoom_01", "vol": 1.0, "auto": true}
"auto": true là mục do mẫu tự thêm (áp lại mẫu thì thay); mục tự thêm tay thì không có "auto"."""
import json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SFX_DIR = os.path.join(ROOT, "thu-vien-am-thanh", "hieu-ung")
_cat = os.path.join(ROOT, "thu-vien-am-thanh", "hieu-ung.json")
SFX = json.load(open(_cat, encoding="utf8")) if os.path.exists(_cat) else {}


def tron_sfx(items, total, out):
    """Trộn các mục sfx thành file WAV stereo 44,1 kHz dài đúng `total` giây. Không có mục nào thì trả False."""
    items = [x for x in items if x["start"] < total]
    if not items:
        return False
    ins, fc = [], []
    for k, x in enumerate(items):
        ins += ["-i", os.path.join(SFX_DIR, x["file"] + ".wav")]
        cut = max(0.0, -x["start"])  # âm bắt đầu trước giây 0 (điểm nhấn sát đầu video): bỏ phần đầu
        ms = int(max(0.0, x["start"]) * 1000)
        fc.append(f"[{k}:a]atrim=start={cut},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,"
                  f"volume={x.get('vol', 1.0)},adelay={ms}|{ms}[s{k}]")
    fc.append("".join(f"[s{k}]" for k in range(len(items))) + f"amix=inputs={len(items)}:normalize=0:duration=longest,"
              f"apad,atrim=0:{total:.3f}[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[a]", out], check=True)
    return True


def catalog_md():
    out = ["# Thư viện hiệu ứng âm", "", "Tự sinh: `python3 scripts/am_thanh.py --md > ../docs/04-thu-vien/THU-VIEN-AM-THANH.md` (trong `video-studio`).",
           "File: `video-studio/thu-vien-am-thanh/hieu-ung/<tên>.wav`. Dùng tên ở cột đầu cho hàng `sfx` của `timeline.json`, hoặc chọn trong app (tab Hiệu ứng âm).",
           "Điểm nhấn = giây trong file mà tai nghe là lúc \"chạm\"; mẫu edit canh điểm này vào đúng lúc hình chuyển/chữ hiện.", ""]
    for nhom in dict.fromkeys(v["nhom"] for v in SFX.values()):
        out += [f"## {nhom}", "| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |", "|---|---|---|---|---|---|"]
        out += [f"| `{k}` | {v['vi']} | {v['dung_khi']} | {v['dai']}s | {v['diem_nhan']}s | {v.get('nguon', '')} |" for k, v in SFX.items() if v["nhom"] == nhom]
        out.append("")
    return "\n".join(out)


if __name__ == "__main__" and sys.argv[1:] == ["--md"]:
    print(catalog_md())
elif __name__ == "__main__":  # tự kiểm: đặt 3 âm, đo lúc âm lượng vọt lên phải khớp mốc
    import tempfile, wave
    import numpy as np
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "t.wav")
        tron_sfx([{"start": 0.5, "file": "chu_pop_01"}, {"start": 1.75, "file": "impact_tram_01", "vol": 0.5},
                  {"start": -0.1, "file": "chu_swish-pop_01"}, {"start": 9, "file": "chu_pop_01"}], 3.0, out)
        w = wave.open(out)
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").reshape(-1, 2)[:, 0] / 32767
        assert abs(len(x) / 44100 - 3.0) < 0.01, len(x)
        e = np.convolve(np.abs(x), np.ones(220) / 220, "same")
        on = [i / 44100 for i in range(1, len(e)) if e[i] > 0.02 and e[i - 1] <= 0.02]
        assert any(abs(t - 0.5) < 0.02 for t in on) and any(abs(t - 1.75) < 0.02 for t in on), on
        assert e[:int(0.02 * 44100)].max() > 0.02  # âm bắt đầu trước giây 0 vẫn nghe phần còn lại
    print("OK", len(SFX), "hiệu ứng trong kho")

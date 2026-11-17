"""Xuất timeline sang phần mềm dựng chuyên nghiệp (OpenTimelineIO):
  out/<tên>.otio  → DaVinci Resolve (File → Import → Timeline)
  out/<tên>.xml   → Premiere Pro (File → Import), Final Cut Pro 7 XML
  out/<tên>.srt   → phụ đề (Premiere/Resolve/CapCut đều nhập được)
Chạy trong video-studio:  python3 scripts/xuat_nle.py projects/<tên>
Cần: pip install opentimelineio otio-fcp-adapter.
Ghi chú: phần mềm dựng chồng chuyển cảnh lên chỗ nối (không chèn thêm thời gian như bộ dựng của dự án), nên video bên đó
ngắn hơn tổng thời lượng chuyển cảnh; chuyển cảnh xuất thành hòa tan (dissolve). Chữ động, minh hoạ xuất thành điểm đánh dấu (marker)."""
import json, os, subprocess, sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import check, layout

FPS = 30


def thong_tin(path):
    """(fps, thời lượng giây) của file gốc; thiếu file thì (30, None)."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate:format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout.split()
    try:
        return float(Fraction(out[0])) or FPS, float(out[1])
    except (ValueError, IndexError, ZeroDivisionError):
        return FPS, None


def gio_nle(tl):
    """Đổi giờ trên video của dự án → giờ trong phần mềm dựng (bỏ phần thời gian chuyển cảnh chèn thêm)."""
    trs = layout(tl)["transitions"]

    def f(t):
        shift = 0.0
        for t0, d, _ in trs:
            if t >= t0 + d:
                shift += d
            elif t > t0:
                shift += t - t0
        return t - shift
    return f


def srt(subs, f):
    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
    out = []
    for k, x in enumerate(sorted(subs, key=lambda x: x["start"]), 1):
        a, b = f(x["start"]), f(x["start"] + x["dur"])
        out.append(f"{k}\n{ts(a)} --> {ts(max(b, a + 0.3))}\n{x['text'].replace('*', '').replace(chr(160), ' ')}\n")
    return "\n".join(out)


def main(proj):
    import opentimelineio as otio
    tl = json.load(open(os.path.join(proj, "timeline.json"), encoding="utf8"))
    if (errs := check(tl)):
        sys.exit("timeline.json chưa hợp lệ:\n- " + "\n- ".join(errs))
    name = os.path.basename(proj)
    raw = lambda f: os.path.abspath(os.path.join(proj, "build", "raw", f))
    RT = lambda sec, rate=FPS: otio.opentime.RationalTime(round(sec * rate), rate)
    TR = lambda a, d, rate=FPS: otio.opentime.TimeRange(RT(a, rate), RT(d, rate))
    f = gio_nle(tl)

    def clip(c, label):
        p = raw(c["file"])
        rate, length = thong_tin(p) if os.path.exists(p) else (FPS, None)
        # Premiere cần biết độ dài file gốc (available_range); thiếu file thì lấy tới hết đoạn dùng
        ref = otio.schema.ExternalReference(target_url="file://" + p, available_range=TR(0, length or c["in"] + c["dur"], rate))
        return otio.schema.Clip(name=label, media_reference=ref, source_range=TR(c["in"], c["dur"], rate))

    out = otio.schema.Timeline(name=name, global_start_time=RT(0))
    v1 = otio.schema.Track(name="Video chính", kind=otio.schema.TrackKind.Video)
    a1 = otio.schema.Track(name="Giọng", kind=otio.schema.TrackKind.Audio)
    for i, c in enumerate(tl["clips"]):
        if i:
            tr = tl["transitions"][i - 1]
            d = layout(tl)["transitions"][i - 1][1]
            if tr["type"] != "cut" and d > 0:
                v1.append(otio.schema.Transition(name=tr["type"], transition_type=otio.schema.TransitionTypes.SMPTE_Dissolve,
                                                 in_offset=RT(d / 2), out_offset=RT(d / 2)))
        v1.append(clip(c, f"{i + 1}. {c['file']}"))
        a1.append(clip(c, f"Giọng {i + 1}. {c['file']}"))
    v2 = otio.schema.Track(name="Cảnh trám", kind=otio.schema.TrackKind.Video)
    pos = 0.0
    for x in sorted(tl.get("broll", []), key=lambda x: x["start"]):
        s = f(x["start"])
        if s > pos + 1e-3:
            v2.append(otio.schema.Gap(source_range=TR(0, s - pos)))
        v2.append(clip(x, f"Cảnh trám: {x['file']}"))
        pos = s + x["dur"]
    # chữ, minh hoạ, zoom: đánh dấu (marker) trên video chính để biên tập viên dựng lại bằng công cụ bên đó
    for key, color, lab in (("texts", otio.schema.MarkerColor.YELLOW, lambda x: "Chữ: " + (x.get("title") or " / ".join(x.get("lines", [])) or x["kind"])),
                            ("cards", otio.schema.MarkerColor.PURPLE, lambda x: "Minh hoạ: " + x["title"]),
                            ("zooms", otio.schema.MarkerColor.BLUE, lambda x: f"Zoom {round((x['scale'] - 1) * 100)}%")):
        for x in tl.get(key, []):
            a = f(x["start"])
            out.tracks.markers.append(otio.schema.Marker(name=lab(x).replace("*", ""), marked_range=TR(a, max(0.1, f(x["start"] + x["dur"]) - a)), color=color))
    out.tracks.extend([v1, v2] + ([a1] if tl.get("audio", {}).get("voice") else []))
    od = os.path.join(proj, "..", "..", "out")
    os.makedirs(od, exist_ok=True)
    otio.adapters.write_to_file(out, os.path.join(od, f"{name}.otio"))
    otio.adapters.write_to_file(out, os.path.join(od, f"{name}.xml"), adapter_name="fcp_xml")
    open(os.path.join(od, f"{name}.srt"), "w", encoding="utf8").write(srt(tl.get("subtitles", []), f))
    print(f"Xong: out/{name}.otio (DaVinci), out/{name}.xml (Premiere), out/{name}.srt (phụ đề) — {len(tl['clips'])} đoạn, "
          f"{len(tl.get('broll', []))} cảnh trám, {len(out.tracks.markers)} điểm đánh dấu")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Dùng: python3 scripts/xuat_nle.py projects/<tên>")
    main(os.path.abspath(sys.argv[1]))

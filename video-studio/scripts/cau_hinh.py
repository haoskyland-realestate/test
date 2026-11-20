"""Bảng master (Hào chốt 19/11): một nguồn cho mọi thông số dựng, file cau-hinh/master.json.
lay(id, tl): giá trị theo thứ tự ưu tiên  ghi đè dự án (timeline.meta.cau_hinh, mẫu edit cũng ghi vào đây) > bảng chung.
kiem(ghi_de): lỗi của một bộ ghi đè (id lạ, sai kiểu, ngoài khoảng) — timeline.check gọi hàm này.
Chạy trong video-studio:  python scripts/cau_hinh.py --tu-kiem"""
import functools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(HERE, "..", "cau-hinh", "master.json")


@functools.lru_cache(None)
def bang():
    """{id: thông số} đọc một lần."""
    d = json.load(open(FILE, encoding="utf8"))
    return {t["id"]: dict(t, nhom=g["id"]) for g in d["nhom"] for t in g["thong_so"]}


def loi_gia_tri(t, v):
    """Lỗi của một giá trị theo thông số t, rỗng nếu hợp lệ."""
    k = t["kieu"]
    if k == "so":
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return f"{t['id']}: cần số"
        if not t["min"] <= v <= t["max"]:
            return f"{t['id']}: {v} ngoài khoảng {t['min']}–{t['max']} {t.get('don_vi', '')}".rstrip()
    elif k == "bat" and not isinstance(v, bool):
        return f"{t['id']}: cần bật/tắt (true/false)"
    elif k == "chon" and v not in t["lua_chon"]:
        return f"{t['id']}: chọn một trong {', '.join(map(str, t['lua_chon']))}"
    elif k == "ds" and not (isinstance(v, list) and all(isinstance(x, str) for x in v)):
        return f"{t['id']}: cần danh sách chữ"
    elif k == "chuoi" and not (isinstance(v, str) and v.strip()):
        return f"{t['id']}: cần chữ"
    return ""


def kiem(ghi_de):
    """Lỗi của bộ ghi đè {id: giá trị}."""
    if ghi_de in (None, {}):
        return []
    if not isinstance(ghi_de, dict):
        return ["meta.cau_hinh phải là {id: giá trị}"]
    b = bang()
    return [f"{k}: không có trong bảng master (gõ nhầm?)" if k not in b else loi_gia_tri(b[k], v) for k, v in ghi_de.items()
            if k not in b or loi_gia_tri(b[k], v)]


def lay(id, tl=None):
    b = bang()
    if id not in b:
        raise KeyError(f"Thông số '{id}' không có trong cau-hinh/master.json")
    gd = ((tl or {}).get("meta") or {}).get("cau_hinh") or {}
    if id in gd:
        if (e := loi_gia_tri(b[id], gd[id])):
            raise ValueError("Ghi đè bảng master sai: " + e)
        return gd[id]
    return b[id]["mac_dinh"]


def _tu_kiem():
    b = bang()
    assert lay("cat.lang_cat") == b["cat.lang_cat"]["mac_dinh"] and lay("cat.lang_cat", {"meta": {"cau_hinh": {"cat.lang_cat": 0.6}}}) == 0.6
    assert kiem({"cat.lang_cat": 9}) and kiem({"cat.lan_cat": 0.4}) and kiem({"agent.preset": "D"}) and kiem({"giong.vad": 1})
    assert kiem({"cat.lang_cat": 0.4, "agent.preset": "B", "cat.tieng_dem": ["ờ"]}) == []
    try:
        lay("khong.co"); raise AssertionError
    except KeyError:
        pass
    for t in b.values():  # mặc định phải hợp lệ với chính khoảng của nó
        assert not loi_gia_tri(t, t["mac_dinh"]), t["id"]
    # mọi lay("…") trong code có trong bảng, mọi thông số trong bảng đều được dùng (không có dòng chết)
    dung = set()
    for f in os.listdir(HERE):
        if f.endswith(".py") and f != "cau_hinh.py":
            dung |= set(re.findall(r'(?:lay|CH|cau_hinh)\(["\']([a-z_]+\.[a-z_]+)["\']', open(os.path.join(HERE, f), encoding="utf8").read()))
    s = open(os.path.join(HERE, "..", "studio", "server.py"), encoding="utf8").read()
    dung |= set(re.findall(r'(?:lay|CH|cau_hinh)\(["\']([a-z_]+\.[a-z_]+)["\']', s))
    assert not (dung - set(b)), f"code dùng thông số chưa có trong bảng: {sorted(dung - set(b))}"
    assert not (set(b) - dung), f"thông số trong bảng chưa được code dùng: {sorted(set(b) - dung)}"
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    else:
        sys.exit(__doc__)

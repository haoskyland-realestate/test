"""Đọc thư viện gl-transitions (thu-vien-chuyen-nghiep/gl-transitions/transitions/*.glsl) thành danh mục scripts/gl_transitions.json.
Chạy lại khi cập nhật thư viện:  python3 scripts/tao_gl_transitions.py  rồi  node scripts/kiem_gl.mjs  (loại hiệu ứng không biên dịch được).
Mỗi mục: tên, mô tả, thẻ, mã GLSL, tham số [kiểu, giá trị mặc định]."""
import glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "thu-vien-chuyen-nghiep", "gl-transitions", "transitions")
OUT = os.path.join(HERE, "gl_transitions.json")
SIZE = {"float": 1, "int": 1, "bool": 1, "vec2": 2, "vec3": 3, "vec4": 4, "ivec2": 2}


def mac_dinh(typ, raw):
    """'vec2(0.0, 1.0)' → [0.0, 1.0]; 'true' → 1; thiếu → toàn 0."""
    n = SIZE[typ]
    if raw is None:
        return [0] * n if n > 1 else 0
    raw = raw.strip().rstrip(";")
    if typ == "bool":
        return 1 if raw.startswith("true") else 0
    inner = re.search(r"\((.*)\)", raw)  # vec2(0.0, -1.0): chỉ đọc số trong ngoặc, bỏ chữ "vec2"
    nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d*)?(?:e-?\d+)?|-?\.\d+", inner[1] if inner else raw)]
    if not nums:
        nums = [0.0]
    if n > 1 and len(nums) == 1:
        nums = nums * n  # vec3(1.0) = (1,1,1)
    nums = [int(x) if typ in ("int", "ivec2") else x for x in nums[:n]]
    return nums if n > 1 else nums[0]


def doc(path):
    src = open(path, encoding="utf8").read()
    if re.search(r"uniform\s+sampler2D", src):
        return None  # cần ảnh phụ (vd. LumaWipe) — bộ dựng chỉ có ảnh cảnh trước/sau
    meta = lambda k: (re.search(rf"//\s*{k}:\s*(.+)", src) or [None, ""])[1].strip()
    params = {}
    for typ, name, raw in re.findall(r"^\s*uniform\s+(\w+)\s+(\w+)\s*;\s*(?://\s*=\s*(.+))?$", src, re.M):
        if typ not in SIZE:
            return None
        params[name] = [typ, mac_dinh(typ, raw or None)]
    return {"desc": meta("Description"), "tags": meta("Tags"), "author": meta("Author"), "glsl": src, "params": params}


assert mac_dinh("vec2", "vec2(0.0, -1.0)") == [0.0, -1.0]
assert mac_dinh("vec3", "vec3(1.0)") == [1.0, 1.0, 1.0]
assert mac_dinh("ivec2", "ivec2(10, 5)") == [10, 5] and mac_dinh("bool", "true") == 1 and mac_dinh("float", None) == 0


if __name__ == "__main__":
    lib = {}
    for p in sorted(glob.glob(os.path.join(SRC, "*.glsl"))):
        t = doc(p)
        if t:
            lib[os.path.basename(p)[:-5]] = t
    json.dump(lib, open(OUT, "w", encoding="utf8"), ensure_ascii=False)
    print(len(lib), "hiệu ứng →", OUT)

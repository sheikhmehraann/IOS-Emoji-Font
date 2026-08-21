import subprocess
import os
import struct

PULL_DIR = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\pulled_vf"
PATCHED_DIR = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\patched_vf"
os.makedirs(PULL_DIR, exist_ok=True)
os.makedirs(PATCHED_DIR, exist_ok=True)

vf_list = [
    "NotoSansDevanagari-VF.ttf", "NotoSansDevanagariUI-VF.ttf",
    "NotoSansBengali-VF.ttf", "NotoSansBengaliUI-VF.ttf",
    "NotoSansGurmukhi-VF.ttf", "NotoSansGurmukhiUI-VF.ttf",
    "NotoSansKannada-VF.ttf", "NotoSansKannadaUI-VF.ttf",
    "NotoSansMalayalam-VF.ttf", "NotoSansMalayalamUI-VF.ttf",
    "NotoSansSinhala-VF.ttf", "NotoSansSinhalaUI-VF.ttf",
    "NotoSansTamil-VF.ttf", "NotoSansTamilUI-VF.ttf",
    "NotoSansTelugu-VF.ttf", "NotoSansTeluguUI-VF.ttf",
    "NotoSansEthiopic-VF.ttf", "NotoSansKhmer-VF.ttf",
    "NotoSerifDevanagari-VF.ttf", "NotoSerifBengali-VF.ttf",
    "NotoSerifGujarati-VF.ttf", "NotoSerifGurmukhi-VF.ttf",
    "NotoSerifKannada-VF.ttf", "NotoSerifMalayalam-VF.ttf",
    "NotoSerifSinhala-VF.ttf", "NotoSerifTamil-VF.ttf",
    "NotoSerifTelugu-VF.ttf", "NotoSerifTibetan-VF.ttf"
]

print("Pulling VF fonts from device...")
for vf in vf_list:
    dst = os.path.join(PULL_DIR, vf)
    subprocess.run([r"C:\platform-tools\adb.exe", "pull", f"/system/fonts/{vf}", dst], capture_output=True)

def patch_vf(in_path, out_path, weight=750.0):
    if not os.path.exists(in_path):
        return
    with open(in_path, "rb") as f:
        data = bytearray(f.read())

    num_tables = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num_tables):
        r = 12 + i * 16
        tag = data[r:r + 4].decode("latin-1")
        offset = struct.unpack(">I", data[r + 8:r + 12])[0]
        length = struct.unpack(">I", data[r + 12:r + 16])[0]
        tables[tag] = (offset, length, r)

    if "fvar" in tables:
        off = tables["fvar"][0]
        axes_off = off + struct.unpack(">H", data[off + 4:off + 6])[0]
        n_axes = struct.unpack(">H", data[off + 8:off + 10])[0]
        ax_size = struct.unpack(">H", data[off + 10:off + 12])[0]
        for a in range(n_axes):
            pos = axes_off + a * ax_size
            if data[pos:pos + 4] == b"wght":
                max_val = struct.unpack(">i", data[pos + 12:pos + 16])[0] / 65536
                actual_weight = min(weight, max_val)
                fv = int(actual_weight * 65536)
                struct.pack_into(">i", data, pos + 4, fv)   # minValue
                struct.pack_into(">i", data, pos + 8, fv)   # defaultValue

    if "OS/2" in tables:
        off = tables["OS/2"][0]
        struct.pack_into(">H", data, off + 4, int(min(weight, 800)))
        fs = struct.unpack(">H", data[off + 62:off + 64])[0]
        struct.pack_into(">H", data, off + 62, fs | 0x0020)

    if "head" in tables:
        off = tables["head"][0]
        ms = struct.unpack(">H", data[off + 44:off + 46])[0]
        struct.pack_into(">H", data, off + 44, ms | 0x0001)

    for tag, (off, length, rec_off) in tables.items():
        pl = (length + 3) & ~3
        tb = data[off:off + length] + b"\x00" * (pl - length)
        if tag == "head":
            struct.pack_into(">I", data, off + 8, 0)
            tb = data[off:off + length] + b"\x00" * (pl - length)
        cs = sum(struct.unpack(f">{pl // 4}I", tb)) & 0xFFFFFFFF
        struct.pack_into(">I", data, rec_off + 4, cs)

    if "head" in tables:
        ho = tables["head"][0]
        pt = (len(data) + 3) & ~3
        fb = data + b"\x00" * (pt - len(data))
        tc = sum(struct.unpack(f">{pt // 4}I", fb)) & 0xFFFFFFFF
        struct.pack_into(">I", data, ho + 8, (0xB1B0AFBA - tc) & 0xFFFFFFFF)

    with open(out_path, "wb") as f:
        f.write(data)
    print(f"Patched: {os.path.basename(out_path)}")

for vf in vf_list:
    src = os.path.join(PULL_DIR, vf)
    dst = os.path.join(PATCHED_DIR, vf)
    patch_vf(src, dst, 750.0)

print("All language variable fonts patched successfully!")

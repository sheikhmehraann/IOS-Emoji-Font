import os
import struct

def inspect_metrics(font_path):
    print(f"=== METRICS FOR: {os.path.basename(font_path)} ===")
    with open(font_path, "rb") as f:
        data = bytearray(f.read())
    
    num_tables = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num_tables):
        r = 12 + i * 16
        tag = data[r:r + 4].decode("latin-1")
        offset = struct.unpack(">I", data[r + 8:r + 12])[0]
        length = struct.unpack(">I", data[r + 12:r + 16])[0]
        tables[tag] = (offset, length)
    
    # head unitsPerEm
    if "head" in tables:
        off = tables["head"][0]
        upem = struct.unpack(">H", data[off + 18:off + 20])[0]
        print(f"head unitsPerEm: {upem}")
    
    # hhea
    if "hhea" in tables:
        off = tables["hhea"][0]
        asc = struct.unpack(">h", data[off + 4:off + 6])[0]
        desc = struct.unpack(">h", data[off + 6:off + 8])[0]
        gap = struct.unpack(">h", data[off + 8:off + 10])[0]
        print(f"hhea: ascent={asc}, descent={desc}, lineGap={gap}")
    
    # OS/2
    if "OS/2" in tables:
        off = tables["OS/2"][0]
        typo_asc = struct.unpack(">h", data[off + 68:off + 70])[0]
        typo_desc = struct.unpack(">h", data[off + 70:off + 72])[0]
        typo_gap = struct.unpack(">h", data[off + 72:off + 74])[0]
        win_asc = struct.unpack(">H", data[off + 74:off + 76])[0]
        win_desc = struct.unpack(">H", data[off + 76:off + 78])[0]
        fsSelection = struct.unpack(">H", data[off + 62:off + 64])[0]
        USE_TYPO_METRICS = bool(fsSelection & 0x0080)
        print(f"OS/2: sTypoAscender={typo_asc}, sTypoDescender={typo_desc}, sTypoLineGap={typo_gap}")
        print(f"OS/2: usWinAscent={win_asc}, usWinDescent={win_desc}")
        print(f"OS/2: fsSelection USE_TYPO_METRICS (bit 7) = {USE_TYPO_METRICS}")
    print()

inspect_metrics(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts\SF-Pro-Text-Heavy.otf")
inspect_metrics(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts\SF-Pro.ttf")

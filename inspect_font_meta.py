import os
import struct

def inspect_font(font_path):
    print(f"=== INSPECTING: {os.path.basename(font_path)} ===")
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
    
    print(f"Tables present: {list(tables.keys())}")
    
    # Check OS/2 weight class
    if "OS/2" in tables:
        off = tables["OS/2"][0]
        weight_class = struct.unpack(">H", data[off + 4:off + 6])[0]
        print(f"OS/2 usWeightClass: {weight_class}")
    
    # Check fvar axes
    if "fvar" in tables:
        off = tables["fvar"][0]
        axes_off = off + struct.unpack(">H", data[off + 4:off + 6])[0]
        n_axes = struct.unpack(">H", data[off + 8:off + 10])[0]
        ax_size = struct.unpack(">H", data[off + 10:off + 12])[0]
        print(f"fvar Axes ({n_axes}):")
        for a in range(n_axes):
            pos = axes_off + a * ax_size
            tag = data[pos:pos + 4].decode("latin-1")
            min_v = struct.unpack(">i", data[pos + 4:pos + 8])[0] / 65536
            def_v = struct.unpack(">i", data[pos + 8:pos + 12])[0] / 65536
            max_v = struct.unpack(">i", data[pos + 12:pos + 16])[0] / 65536
            print(f"  Axis {tag}: min={min_v}, def={def_v}, max={max_v}")
    
    # Check name table entries
    if "name" in tables:
        off = tables["name"][0]
        count = struct.unpack(">H", data[off + 2:off + 4])[0]
        string_off = off + struct.unpack(">H", data[off + 4:off + 6])[0]
        names = {}
        for n in range(count):
            rec = off + 6 + n * 12
            plat_id = struct.unpack(">H", data[rec:rec + 2])[0]
            name_id = struct.unpack(">H", data[rec + 6:rec + 8])[0]
            length = struct.unpack(">H", data[rec + 8:rec + 10])[0]
            str_pos = string_off + struct.unpack(">H", data[rec + 10:rec + 12])[0]
            raw = data[str_pos:str_pos + length]
            try:
                val = raw.decode("utf-16be" if plat_id in (0, 3) else "utf-8", errors="ignore").replace("\x00", "")
            except:
                val = str(raw)
            if name_id in (1, 2, 4, 6):
                names[name_id] = val
        print(f"Name records: {names}")
    print()

inspect_font(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\module\system\fonts\SF-Pro-Bold.ttf")
inspect_font(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts\SF-Pro.ttf")
inspect_font(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts\SF-Pro-Display-Heavy.otf")

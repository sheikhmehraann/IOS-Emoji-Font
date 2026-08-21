import os
import struct

def inspect(fn):
    p = os.path.join(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\pulled_vf", fn)
    with open(p, "rb") as f:
        data = f.read()
    num_tables = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num_tables):
        r = 12 + i * 16
        tag = data[r:r+4].decode("latin-1")
        tables[tag] = struct.unpack(">I", data[r+8:r+12])[0]
    
    print(f"=== {fn} ===")
    if "head" in tables:
        off = tables["head"]
        upem = struct.unpack(">H", data[off+18:off+20])[0]
        print(f"upem: {upem}")
    if "hhea" in tables:
        off = tables["hhea"]
        print("hhea (asc, desc, gap):", struct.unpack(">hhh", data[off+4:off+10]))
    if "OS/2" in tables:
        off = tables["OS/2"]
        print("typo (asc, desc, gap):", struct.unpack(">hhh", data[off+68:off+74]))
        print("win (asc, desc):", struct.unpack(">HH", data[off+74:off+78]))

for fn in os.listdir(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\pulled_vf")[:3]:
    inspect(fn)

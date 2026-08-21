import os
from fontTools.ttLib import TTFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"

for fn in os.listdir(apple_dir):
    if fn.endswith(".ttf") or fn.endswith(".otf"):
        p = os.path.join(apple_dir, fn)
        tt = TTFont(p)
        has_glyf = 'glyf' in tt
        has_cff = 'CFF ' in tt or 'CFF2' in tt
        upem = tt['head'].unitsPerEm
        asc = tt['hhea'].ascent if 'hhea' in tt else None
        desc = tt['hhea'].descent if 'hhea' in tt else None
        print(f"{fn:30s} | upem={upem:4d} | glyf={str(has_glyf):5s} | CFF={str(has_cff):5s} | hhea=({asc}, {desc})")

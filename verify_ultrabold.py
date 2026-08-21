import os
from fontTools.ttLib import TTFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"

def inspect(name):
    p = os.path.join(apple_dir, name)
    tt = TTFont(p)
    print(f"=== {name} ===")
    print("usWeightClass:", tt['OS/2'].usWeightClass)
    print("USE_TYPO_METRICS:", bool(tt['OS/2'].fsSelection & 0x0080))
    print("win (asc, desc):", (tt['OS/2'].usWinAscent, tt['OS/2'].usWinDescent))
    print("hhea (asc, desc):", (tt['hhea'].ascent, tt['hhea'].descent))
    g = tt['glyf']['H']
    print("Glyph 'H' width:", g.xMax - g.xMin)

inspect("SF-Pro-UltraBold-Static.ttf")
inspect("SF-Pro-UltraBold-VF.ttf")

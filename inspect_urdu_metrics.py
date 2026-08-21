import os
from fontTools.ttLib import TTFont

p = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts\NotoNastaliqUrdu-Bold.ttf"
tt = TTFont(p)
print("=== NotoNastaliqUrdu-Bold.ttf ===")
print("upem:", tt['head'].unitsPerEm)
print("hhea (asc, desc, gap):", (tt['hhea'].ascent, tt['hhea'].descent, tt['hhea'].lineGap))
print("OS/2 typo (asc, desc, gap):", (tt['OS/2'].sTypoAscender, tt['OS/2'].sTypoDescender, tt['OS/2'].sTypoLineGap))
print("OS/2 win (asc, desc):", (tt['OS/2'].usWinAscent, tt['OS/2'].usWinDescent))
print("OS/2 fsSelection USE_TYPO_METRICS:", bool(tt['OS/2'].fsSelection & 0x0080))

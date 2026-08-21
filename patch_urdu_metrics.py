import os
from fontTools.ttLib import TTFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"
urdu_path = os.path.join(apple_dir, "NotoNastaliqUrdu-Bold.ttf")
urdu_patched_path = os.path.join(apple_dir, "NotoNastaliqUrdu-Bold-Patched.ttf")

tt = TTFont(urdu_path)
upem = tt['head'].unitsPerEm
print(f"Original Urdu upem: {upem}")

# Normalize metrics for 1000 UPM
tt['hhea'].ascent = 1000
tt['hhea'].descent = -350
tt['hhea'].lineGap = 0

tt['OS/2'].sTypoAscender = 850
tt['OS/2'].sTypoDescender = -350
tt['OS/2'].sTypoLineGap = 0
tt['OS/2'].usWinAscent = 1000
tt['OS/2'].usWinDescent = 350
tt['OS/2'].fsSelection |= 0x0080  # USE_TYPO_METRICS

tt.save(urdu_patched_path)
print(f"Saved patched Urdu font: {urdu_patched_path}")
os.replace(urdu_patched_path, urdu_path)
print(f"Replaced original NotoNastaliqUrdu-Bold.ttf with compact-metrics version!")

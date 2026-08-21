import os
from fontTools.ttLib import TTFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"
urdu_path = os.path.join(apple_dir, "NotoNastaliqUrdu-Bold.ttf")

tt = TTFont(urdu_path)
upem = tt['head'].unitsPerEm  # 1000

# Exactly proportional to SF Pro (1950, -494 on 2048 UPM)
target_asc = int(round(1950 * upem / 2048.0))   # 952
target_desc = int(round(-494 * upem / 2048.0))  # -241
target_win_asc = target_asc                     # 952
target_win_desc = abs(target_desc)              # 241

tt['hhea'].ascent = target_asc
tt['hhea'].descent = target_desc
tt['hhea'].lineGap = 0

tt['OS/2'].sTypoAscender = target_asc
tt['OS/2'].sTypoDescender = target_desc
tt['OS/2'].sTypoLineGap = 0
tt['OS/2'].usWinAscent = target_win_asc
tt['OS/2'].usWinDescent = target_win_desc
tt['OS/2'].fsSelection = 0  # Matched to SF Pro

tt.save(urdu_path)
print(f"Patched NotoNastaliqUrdu-Bold metrics to exact match SF Pro: asc={target_asc}, desc={target_desc}")

import os
import copy
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"
src_sf = os.path.join(apple_dir, "SF-Pro.ttf")

# 1. Create 900 Ultra-Bold Static font
tt_bold = TTFont(src_sf)
instantiateVariableFont(tt_bold, {'wght': 900}, inplace=True)

# 2. Create the variable font shell from SF-Pro.ttf
tt_final = TTFont(src_sf)

# 3. Replace the glyf, loca, hmtx tables in tt_final with the 900 Bold tables from tt_bold
tt_final['glyf'] = copy.deepcopy(tt_bold['glyf'])
tt_final['loca'] = copy.deepcopy(tt_bold['loca'])
tt_final['hmtx'] = copy.deepcopy(tt_bold['hmtx'])
tt_final['maxp'] = copy.deepcopy(tt_bold['maxp'])

# 4. Set exact stock Android metrics
upem = tt_final['head'].unitsPerEm
scale = upem / 2048.0

target_asc = int(round(1900 * scale))
target_desc = int(round(-500 * scale))
target_win_asc = int(round(1946 * scale))
target_win_desc = int(round(512 * scale))
target_typo_asc = int(round(1536 * scale))
target_typo_desc = int(round(-512 * scale))
target_typo_gap = int(round(102 * scale))

tt_final['hhea'].ascent = target_asc
tt_final['hhea'].descent = target_desc
tt_final['hhea'].lineGap = 0
tt_final['OS/2'].sTypoAscender = target_typo_asc
tt_final['OS/2'].sTypoDescender = target_typo_desc
tt_final['OS/2'].sTypoLineGap = target_typo_gap
tt_final['OS/2'].usWinAscent = target_win_asc
tt_final['OS/2'].usWinDescent = target_win_desc
tt_final['OS/2'].fsSelection &= ~0x0080  # USE_TYPO_METRICS = False (Stock Android)
tt_final['OS/2'].usWeightClass = 900

# Remove gvar so weight cannot be downscaled
if 'gvar' in tt_final:
    del tt_final['gvar']
if 'avar' in tt_final:
    del tt_final['avar']
if 'cvar' in tt_final:
    del tt_final['cvar']
if 'HVAR' in tt_final:
    del tt_final['HVAR']
if 'MVAR' in tt_final:
    del tt_final['MVAR']

out_path = os.path.join(apple_dir, "SF-Pro-MasterBold.ttf")
tt_final.save(out_path)
print(f"Created Master Bold Font: {out_path}")
print("Keys:", list(tt_final.keys()))
print("Glyph 'H' width in base glyf:", tt_final['glyf']['H'].xMax - tt_final['glyf']['H'].xMin)

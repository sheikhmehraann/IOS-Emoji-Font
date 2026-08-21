import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"
src_sf = os.path.join(apple_dir, "SF-Pro.ttf")

# 1. Instantiate at maximum wght=900 (Ultra Heavy / Black Bold)
tt = TTFont(src_sf)
print("Instantiating SF-Pro.ttf at wght=900...")
instantiateVariableFont(tt, {'wght': 900}, inplace=True)

# 2. Set EXACT stock Android Roboto metrics
upem = tt['head'].unitsPerEm
scale = upem / 2048.0

target_asc = int(round(1900 * scale))
target_desc = int(round(-500 * scale))
target_win_asc = int(round(1946 * scale))
target_win_desc = int(round(512 * scale))
target_typo_asc = int(round(1536 * scale))
target_typo_desc = int(round(-512 * scale))
target_typo_gap = int(round(102 * scale))

tt['hhea'].ascent = target_asc
tt['hhea'].descent = target_desc
tt['hhea'].lineGap = 0

tt['OS/2'].sTypoAscender = target_typo_asc
tt['OS/2'].sTypoDescender = target_typo_desc
tt['OS/2'].sTypoLineGap = target_typo_gap
tt['OS/2'].usWinAscent = target_win_asc
tt['OS/2'].usWinDescent = target_win_desc
tt['OS/2'].fsSelection &= ~0x0080  # Disable USE_TYPO_METRICS (EXACT stock Android Roboto behavior!)
tt['OS/2'].usWeightClass = 900

# Remove variable tables to make it pure TrueType static
for t in ['fvar', 'avar', 'gvar', 'cvar', 'HVAR', 'VVAR', 'MVAR', 'STAT', 'DSIG']:
    if t in tt:
        del tt[t]

out_static = os.path.join(apple_dir, "SF-Pro-UltraBold-Static.ttf")
tt.save(out_static)
print(f"Created Ultra Bold 900 TrueType static font: {out_static}")

# 3. Create a Variable Font version where ALL axes map to 900
tt_vf = TTFont(src_sf)
tt_vf['hhea'].ascent = target_asc
tt_vf['hhea'].descent = target_desc
tt_vf['hhea'].lineGap = 0
tt_vf['OS/2'].sTypoAscender = target_typo_asc
tt_vf['OS/2'].sTypoDescender = target_typo_desc
tt_vf['OS/2'].sTypoLineGap = target_typo_gap
tt_vf['OS/2'].usWinAscent = target_win_asc
tt_vf['OS/2'].usWinDescent = target_win_desc
tt_vf['OS/2'].fsSelection &= ~0x0080
tt_vf['OS/2'].usWeightClass = 900

if 'fvar' in tt_vf:
    for axis in tt_vf['fvar'].axes:
        if axis.axisTag == 'wght':
            axis.minValue = 800.0
            axis.defaultValue = 900.0
            axis.maxValue = 900.0

out_vf = os.path.join(apple_dir, "SF-Pro-UltraBold-VF.ttf")
tt_vf.save(out_vf)
print(f"Created Ultra Bold 900 TrueType variable font: {out_vf}")

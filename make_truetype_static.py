import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"

def make_static_truetype(var_font_path, out_path, weight=800):
    tt = TTFont(var_font_path)
    print(f"Instantiating {os.path.basename(var_font_path)} at wght={weight}...")
    
    # Instantiate static instance
    instantiateVariableFont(tt, {'wght': weight}, inplace=True)
    
    upem = tt['head'].unitsPerEm
    scale = upem / 2048.0
    
    target_asc = int(round(1900 * scale))
    target_desc = int(round(-500 * scale))
    target_win_asc = int(round(1900 * scale))
    target_win_desc = int(round(500 * scale))
    target_typo_asc = int(round(1536 * scale))
    target_typo_desc = int(round(-512 * scale))
    target_typo_gap = int(round(102 * scale))
    
    # hhea
    if 'hhea' in tt:
        tt['hhea'].ascent = target_asc
        tt['hhea'].descent = target_desc
        tt['hhea'].lineGap = 0
    
    # OS/2
    if 'OS/2' in tt:
        tt['OS/2'].sTypoAscender = target_typo_asc
        tt['OS/2'].sTypoDescender = target_typo_desc
        tt['OS/2'].sTypoLineGap = target_typo_gap
        tt['OS/2'].usWinAscent = target_win_asc
        tt['OS/2'].usWinDescent = target_win_desc
        tt['OS/2'].fsSelection |= 0x0080  # USE_TYPO_METRICS
        tt['OS/2'].usWeightClass = weight
    
    # Drop DSIG if present
    if 'DSIG' in tt:
        del tt['DSIG']
        
    tt.save(out_path)
    print(f"Created TrueType static bold: {out_path} (has glyf={'glyf' in tt}, has fvar={'fvar' in tt})")

# 1. SF-Pro TrueType Static Heavy Bold (800)
make_static_truetype(
    os.path.join(apple_dir, "SF-Pro.ttf"),
    os.path.join(apple_dir, "SF-Pro-Bold-Static.ttf"),
    weight=800
)

# 2. NewYork TrueType Static Bold (700)
make_static_truetype(
    os.path.join(apple_dir, "NewYork.ttf"),
    os.path.join(apple_dir, "NewYork-Bold-Static.ttf"),
    weight=700
)

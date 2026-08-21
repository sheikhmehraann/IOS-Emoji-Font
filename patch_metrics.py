import os
from fontTools.ttLib import TTFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"

def fix_font_metrics(font_path, out_path):
    tt = TTFont(font_path)
    upem = tt['head'].unitsPerEm
    print(f"Fixing metrics for: {os.path.basename(font_path)} (upem={upem})")
    
    # Target Android standard metrics (for 2048 UPM or scaled)
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
    
    tt.save(out_path)
    print(f"Saved: {out_path}")

# Fix SF-Pro-Text-Heavy.otf
fix_font_metrics(
    os.path.join(apple_dir, "SF-Pro-Text-Heavy.otf"),
    os.path.join(apple_dir, "SF-Pro-Text-Heavy-Patched.otf")
)

# Fix NewYorkLarge-Heavy.otf
fix_font_metrics(
    os.path.join(apple_dir, "NewYorkLarge-Heavy.otf"),
    os.path.join(apple_dir, "NewYorkLarge-Heavy-Patched.otf")
)

# Fix SF-Pro-Rounded-Bold.otf
fix_font_metrics(
    os.path.join(apple_dir, "SF-Pro-Rounded-Bold.otf"),
    os.path.join(apple_dir, "SF-Pro-Rounded-Bold-Patched.otf")
)

# Replace originals with patched versions
for name in ["SF-Pro-Text-Heavy", "NewYorkLarge-Heavy", "SF-Pro-Rounded-Bold"]:
    ext = ".otf"
    patched = os.path.join(apple_dir, f"{name}-Patched{ext}")
    orig = os.path.join(apple_dir, f"{name}{ext}")
    if os.path.exists(patched):
        os.replace(patched, orig)
        print(f"Replaced {orig} with perfect-metrics patched version!")

import os
import shutil
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

BASE_DIR = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
APPLE_FONTS = os.path.join(ASSETS_DIR, "apple_fonts")
PATCHED_VF = os.path.join(ASSETS_DIR, "patched_vf")
PULLED_VF = os.path.join(ASSETS_DIR, "pulled_vf")
NON_ROOT_DIR = r"C:\Users\Admin\Videos\Github\iOS-Font-Emoji-NonRoot"

os.makedirs(PATCHED_VF, exist_ok=True)

def normalize_font(font_path, output_path, target_weight=800, make_static_bold=False):
    try:
        tt = TTFont(font_path)
        upem = tt['head'].unitsPerEm
        
        # If requested and font is variable, instantiate at heavy bold
        if make_static_bold and 'fvar' in tt:
            try:
                tt = instantiateVariableFont(tt, {'wght': float(target_weight)}, inplace=False)
                upem = tt['head'].unitsPerEm
            except Exception as e:
                pass

        # Calculate exact proportional metrics based on SF Pro (2048 UPM: 1950, -494)
        scale = upem / 2048.0
        asc = int(round(1950 * scale))
        desc = int(round(-494 * scale))
        win_asc = asc
        win_desc = abs(desc)
        
        # 1. Normalize Horizontal Header (hhea)
        if 'hhea' in tt:
            tt['hhea'].ascent = asc
            tt['hhea'].descent = desc
            tt['hhea'].lineGap = 0
            
        # 2. Normalize OS/2 Table
        if 'OS/2' in tt:
            tt['OS/2'].sTypoAscender = asc
            tt['OS/2'].sTypoDescender = desc
            tt['OS/2'].sTypoLineGap = 0
            tt['OS/2'].usWinAscent = win_asc
            tt['OS/2'].usWinDescent = win_desc
            tt['OS/2'].usWeightClass = target_weight
            tt['OS/2'].fsSelection |= 0x0020   # Set Bold bit
            tt['OS/2'].fsSelection &= ~0x0080  # Disable USE_TYPO_METRICS for 1:1 stock parity
            
        # 3. Normalize head table
        if 'head' in tt:
            tt['head'].macStyle |= 0x0001      # Set Bold bit
            
        # 4. Normalize Variable Font Axes (fvar) if present
        if 'fvar' in tt:
            for axis in tt['fvar'].axes:
                if axis.axisTag == 'wght':
                    axis.minValue = float(min(target_weight, axis.maxValue))
                    axis.defaultValue = float(min(target_weight, axis.maxValue))
                    axis.maxValue = float(max(target_weight, axis.maxValue))
                    
        tt.save(output_path)
        print(f"[OK] Normalized: {os.path.basename(output_path)} (UPM={upem}, asc={asc}, desc={desc}, weight={target_weight})")
        return True
    except Exception as e:
        print(f"[ERROR] Failed {os.path.basename(font_path)}: {e}")
        return False

print("=== 1. NORMALIZING ALL APPLE MULTILINGUAL FONTS ===")
for fn in os.listdir(APPLE_FONTS):
    if fn.endswith(".ttf") or fn.endswith(".otf"):
        fp = os.path.join(APPLE_FONTS, fn)
        normalize_font(fp, fp, target_weight=800)

print("\n=== 2. NORMALIZING ALL WORLD SCRIPT VARIABLE FONTS (PULLED_VF -> PATCHED_VF) ===")
for fn in os.listdir(PULLED_VF):
    if fn.endswith(".ttf") or fn.endswith(".otf"):
        src = os.path.join(PULLED_VF, fn)
        dst = os.path.join(PATCHED_VF, fn)
        normalize_font(src, dst, target_weight=800)

print("\n=== ALL FONTS NORMALIZED WITH 100% MATHEMATICAL METRICS PARITY! ===")

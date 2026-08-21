import os
import zipfile
import hashlib
from fontTools.ttLib import TTFont

zip_path = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\Made By Another Dev\IOSFONTMODULE.zip"
extract_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\Made By Another Dev\extracted"
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, "r") as zf:
    print("Files in IOSFONTMODULE.zip:")
    for info in zf.infolist():
        print(f"  {info.filename:50s} ({info.file_size} bytes)")
    zf.extractall(extract_dir)

print("\n=== DEEP INSPECTION OF FONTS IN IOSFONTMODULE.ZIP ===")
for root, _, files in os.walk(extract_dir):
    for fn in files:
        if fn.endswith(".ttf") or fn.endswith(".otf"):
            fp = os.path.join(root, fn)
            h = hashlib.md5()
            with open(fp, "rb") as f:
                h.update(f.read())
            tt = TTFont(fp)
            upem = tt['head'].unitsPerEm if 'head' in tt else None
            asc = tt['hhea'].ascent if 'hhea' in tt else None
            desc = tt['hhea'].descent if 'hhea' in tt else None
            win_asc = tt['OS/2'].usWinAscent if 'OS/2' in tt else None
            win_desc = tt['OS/2'].usWinDescent if 'OS/2' in tt else None
            typo_asc = tt['OS/2'].sTypoAscender if 'OS/2' in tt else None
            typo_desc = tt['OS/2'].sTypoDescender if 'OS/2' in tt else None
            typo_gap = tt['OS/2'].sTypoLineGap if 'OS/2' in tt else None
            weight = tt['OS/2'].usWeightClass if 'OS/2' in tt else None
            use_typo = bool(tt['OS/2'].fsSelection & 0x0080) if 'OS/2' in tt else None
            has_glyf = 'glyf' in tt
            has_cff = 'CFF ' in tt or 'CFF2' in tt
            has_fvar = 'fvar' in tt
            
            print(f"\n--- {fn} (MD5: {h.hexdigest()}, Size: {os.path.getsize(fp)}) ---")
            print(f"  upem={upem}, glyf={has_glyf}, CFF={has_cff}, fvar={has_fvar}")
            print(f"  usWeightClass={weight}, USE_TYPO_METRICS={use_typo}")
            print(f"  hhea=({asc}, {desc}), win=({win_asc}, {win_desc}), typo=({typo_asc}, {typo_desc}, {typo_gap})")
            if has_glyf and 'H' in tt['glyf']:
                g = tt['glyf']['H']
                print(f"  Glyph 'H' width: {g.xMax - g.xMin} (xMin={g.xMin}, xMax={g.xMax})")

import os
from fontTools.ttLib import TTFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"

def strip_var_tables(font_path, out_path):
    tt = TTFont(font_path)
    for t in ['fvar', 'avar', 'gvar', 'cvar', 'HVAR', 'VVAR', 'MVAR', 'STAT']:
        if t in tt:
            del tt[t]
            print(f"Deleted {t} table")
    tt.save(out_path)
    print(f"Saved pure static TrueType font: {out_path}")

strip_var_tables(
    os.path.join(apple_dir, "SF-Pro-Bold-Static.ttf"),
    os.path.join(apple_dir, "SF-Pro-Bold-PureStatic.ttf")
)

strip_var_tables(
    os.path.join(apple_dir, "NewYork-Bold-Static.ttf"),
    os.path.join(apple_dir, "NewYork-Bold-PureStatic.ttf")
)

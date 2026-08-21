import os
from fontTools.ttLib import TTFont

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"

def inspect_weight(name):
    p = os.path.join(apple_dir, name)
    if not os.path.exists(p):
        print(f"{name} does not exist")
        return
    tt = TTFont(p)
    print(f"=== {name} ===")
    print("OS/2 usWeightClass:", tt['OS/2'].usWeightClass if 'OS/2' in tt else None)
    if 'glyf' in tt:
        # Check glyph 'B' or 'H' bounding box
        g = tt['glyf']['H']
        print("Glyph 'H' (xMin, yMin, xMax, yMax):", (g.xMin, g.yMin, g.xMax, g.yMax), f"width={g.xMax - g.xMin}")
        gA = tt['glyf']['A']
        print("Glyph 'A' (xMin, yMin, xMax, yMax):", (gA.xMin, gA.yMin, gA.xMax, gA.yMax), f"width={gA.xMax - gA.xMin}")
    elif 'CFF ' in tt:
        print("Font is CFF format")

inspect_weight("SF-Pro-Bold-PureStatic.ttf")
inspect_weight("SF-Pro.ttf")
inspect_weight("SF-Pro-Text-Heavy.otf")
inspect_weight("SF-Pro-Display-Heavy.otf")
inspect_weight("SF-Pro-Text-Bold.otf")

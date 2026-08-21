from fontTools.ttLib import TTFont

dev_font_path = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\Made By Another Dev\extracted\system\fonts\Roboto-Regular.ttf"
tt = TTFont(dev_font_path)

print("=== NAME TABLE IN DEV FONT ===")
for record in tt['name'].names:
    try:
        print(f"ID {record.nameID:2d} ({record.platformID}, {record.platEncID}, {record.langID}): {record.toUnicode()}")
    except:
        pass

print("\n=== OS/2 TABLE IN DEV FONT ===")
for k in ['sTypoAscender', 'sTypoDescender', 'sTypoLineGap', 'usWinAscent', 'usWinDescent', 'sxHeight', 'sCapHeight', 'usWeightClass', 'usWidthClass', 'fsSelection']:
    print(f"  {k}: {getattr(tt['OS/2'], k)}")

print("\n=== HHEA TABLE IN DEV FONT ===")
for k in ['ascent', 'descent', 'lineGap']:
    print(f"  {k}: {getattr(tt['hhea'], k)}")

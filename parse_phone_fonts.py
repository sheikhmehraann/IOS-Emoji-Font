import xml.etree.ElementTree as ET

tree = ET.parse(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\phone_fonts.xml")
root = tree.getroot()

print("=== ALL FONT FAMILIES IN PHONE FONTS.XML ===")
for family in root.findall('family'):
    name = family.get('name')
    lang = family.get('lang')
    fonts = [f.text for f in family.findall('font')]
    if lang or name:
        print(f"Family name={name}, lang={lang} -> fonts={fonts}")

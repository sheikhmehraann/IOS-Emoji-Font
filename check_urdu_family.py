import xml.etree.ElementTree as ET

tree = ET.parse(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\phone_fonts.xml")
root = tree.getroot()

for i, family in enumerate(root.findall('family')):
    lang = family.get('lang', '')
    if 'ur' in lang.lower() or 'arab' in lang.lower():
        fonts = [f.text.strip() for f in family.findall('font')]
        print(f"Family #{i} lang={lang} -> {fonts}")

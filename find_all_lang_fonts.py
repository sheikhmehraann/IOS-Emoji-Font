import xml.etree.ElementTree as ET

tree = ET.parse(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\phone_fonts.xml")
root = tree.getroot()

for i, family in enumerate(root.findall('family')):
    fonts = [f.text.strip() for f in family.findall('font')]
    for f in fonts:
        if any(x in f.lower() for x in ['urdu', 'nastaliq', 'arabic', 'naskh', 'devanagari', 'bengali', 'tamil', 'telugu', 'cjk']):
            lang = family.get('lang', '')
            name = family.get('name', '')
            print(f"Family #{i} name={name} lang={lang} -> font={f}")

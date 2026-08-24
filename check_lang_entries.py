import xml.etree.ElementTree as ET

tree = ET.parse(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\phone_fonts.xml")
root = tree.getroot()

for family in root.findall('family'):
    lang = family.get('lang', '')
    name = family.get('name', '')
    fonts = [f.text.strip() for f in family.findall('font')]
    if any(k in (lang or '') for k in ['ur', 'ar', 'fa', 'he', 'hi', 'bn', 'gu', 'pa', 'ta', 'te', 'kn', 'ml', 'si', 'my', 'th', 'km', 'lo', 'ka', 'hy', 'zh', 'ja', 'ko']) or name:
        print(f"[{name or 'FALLBACK'}] lang={lang} -> {fonts}")

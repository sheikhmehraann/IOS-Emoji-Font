import xml.etree.ElementTree as ET
import os

tree = ET.parse(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\phone_fonts.xml")
root = tree.getroot()

# Insert Urdu Nastaliq family before Arabic family
arabic_idx = None
for i, family in enumerate(root.findall('family')):
    if family.get('lang') == 'und-Arab':
        arabic_idx = i
        break

if arabic_idx is not None:
    urdu_family = ET.Element('family', {'lang': 'ur,ur-PK,ur-IN,pa-Arab'})
    f1 = ET.SubElement(urdu_family, 'font', {'weight': '400', 'style': 'normal'})
    f1.text = 'NotoNastaliqUrdu-Bold.ttf'
    f2 = ET.SubElement(urdu_family, 'font', {'weight': '700', 'style': 'normal'})
    f2.text = 'NotoNastaliqUrdu-Bold.ttf'
    root.insert(arabic_idx, urdu_family)
    print("Inserted Urdu family at index", arabic_idx)

out_xml = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\system\etc\fonts.xml"
os.makedirs(os.path.dirname(out_xml), exist_ok=True)
tree.write(out_xml, encoding="utf-8", xml_declaration=True)
print("Wrote patched fonts.xml to", out_xml)

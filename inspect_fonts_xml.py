import subprocess

cmd = r"""
echo "=== SYSTEM FONTS.XML SANS-SERIF FAMILY ==="
python3 -c '
import xml.etree.ElementTree as ET
try:
    tree = ET.parse("/system/etc/fonts.xml")
    for fam in tree.findall("family"):
        if fam.get("name") == "sans-serif" or fam.get("name") is None:
            print("Family:", fam.attrib)
            for f in fam.findall("font"):
                print("  Font:", f.attrib, f.text)
except Exception as e:
    print(e)
' 2>/dev/null

echo "=== PRODUCT FONTS.XML ==="
cat /product/etc/fonts.xml 2>/dev/null || cat /product/etc/fonts_custom.xml 2>/dev/null

echo "=== THEME / FONT SETTING FILES IN /data ==="
ls -la /data/system/theme/ 2>/dev/null
ls -la /data/system/font/ 2>/dev/null
ls -la /data/system/users/0/ 2>/dev/null | grep -iE 'font|theme'
"""

with open(r"C:\Users\Admin\inspect_fonts_xml.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\inspect_fonts_xml.sh", "/data/local/tmp/inspect_fonts_xml.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/inspect_fonts_xml.sh'"], capture_output=True, text=True)
print(res.stdout)

import subprocess

cmd = r"""
echo "=== FIRST 60 LINES OF /system/etc/fonts.xml ==="
head -n 60 /system/etc/fonts.xml

echo "=== FIND ALL XMLs IN /product/etc, /system_ext/etc, /vendor/etc ==="
find /product/etc /system_ext/etc /vendor/etc /system/etc -iname "*font*.xml" 2>/dev/null

echo "=== TRANSSION THEME PACKAGES & DATA ==="
find /data/system /data/data -maxdepth 3 -iname "*theme*" -o -iname "*font*" 2>/dev/null | head -n 30
"""

with open(r"C:\Users\Admin\inspect_fonts_xml_raw.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\inspect_fonts_xml_raw.sh", "/data/local/tmp/inspect_fonts_xml_raw.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/inspect_fonts_xml_raw.sh'"], capture_output=True, text=True)
print(res.stdout)

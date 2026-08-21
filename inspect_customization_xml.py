import subprocess

cmd = r"""
echo "=== /product/etc/fonts_customization.xml ==="
cat /product/etc/fonts_customization.xml 2>/dev/null

echo "=== FIRST 100 LINES OF /system/etc/font_fallback.xml ==="
head -n 100 /system/etc/font_fallback.xml 2>/dev/null
"""

with open(r"C:\Users\Admin\inspect_customization_xml.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\inspect_customization_xml.sh", "/data/local/tmp/inspect_customization_xml.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/inspect_customization_xml.sh'"], capture_output=True, text=True)
print(res.stdout)

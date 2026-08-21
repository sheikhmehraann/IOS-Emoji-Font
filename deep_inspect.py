import subprocess

cmd = r"""
echo "=== TRANSSION SYSTEM PROPERTIES ==="
getprop | grep -iE 'font|theme|transsion|tos'

echo "=== FONTS IN /product/fonts ==="
ls -la /product/fonts/

echo "=== FONTS IN /system/fonts (first 30) ==="
ls -la /system/fonts/ | head -n 30

echo "=== FONTS.XML LOCATION AND HEAD ==="
for xml in /system/etc/fonts.xml /product/etc/fonts.xml /system_ext/etc/fonts.xml /vendor/etc/fonts.xml; do
    if [ -f "$xml" ]; then
        echo "Found $xml"
        head -n 25 "$xml"
    fi
done

echo "=== ACTIVE MOUNTS ON FONTS ==="
mount | grep -iE 'fonts|ttf|otf'
"""

with open(r"C:\Users\Admin\deep_inspect.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\deep_inspect.sh", "/data/local/tmp/deep_inspect.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/deep_inspect.sh'"], capture_output=True, text=True)
print(res.stdout)

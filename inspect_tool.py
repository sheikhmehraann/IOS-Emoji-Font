import subprocess

cmd = r"""
echo "=== 1. ALL ARABIC / URDU / NASTALIQ FONTS ON DEVICE ==="
find /system /product /system_ext /vendor -name '*Arabic*' -o -name '*Urdu*' -o -name '*Nastaliq*' -o -name '*Arab*' 2>/dev/null

echo "=== 2. ALL PRODUCT FONTS ==="
ls -la /product/fonts/ 2>/dev/null

echo "=== 3. ALL SYSTEM_EXT FONTS ==="
ls -la /system_ext/fonts/ 2>/dev/null

echo "=== 4. ALL VENDOR FONTS ==="
ls -la /vendor/fonts/ 2>/dev/null

echo "=== 5. TRANSSION THEME & FONT CACHES IN /data ==="
find /data -name '*TranSans*' -o -name '*TOS*' -o -name '*theme*font*' 2>/dev/null | head -n 30

echo "=== 6. FONTS.XML LOCATION ==="
ls -la /system/etc/fonts.xml /product/etc/fonts.xml /system_ext/etc/fonts.xml /vendor/etc/fonts.xml /system/etc/font_fallback.xml /product/etc/font_fallback.xml 2>/dev/null
"""

with open(r"C:\Users\Admin\inspect_device.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\inspect_device.sh", "/data/local/tmp/inspect_device.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/inspect_device.sh'"], capture_output=True, text=True)
print(res.stdout)

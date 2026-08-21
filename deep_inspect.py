import subprocess

cmd = r"""
echo "=== 1. ALL FONT FAMILY NAMES IN /system/etc/fonts.xml ==="
grep -E '<family name=' /system/etc/fonts.xml

echo "=== 2. ALL FONT FILES IN /system/etc/fonts.xml WITH TRAN/TOS/SANS ==="
grep -C 3 -iE 'tran|tos|sans-serif' /system/etc/fonts.xml | head -n 40

echo "=== 3. SEARCHING FOR ALL FONT FILES IN THE SYSTEM ==="
find /system /product /system_ext /vendor /odm /data -name '*.ttf' -o -name '*.otf' 2>/dev/null | grep -v '/data/adb/modules' | head -n 50

echo "=== 4. CURRENT ACTIVE THEME OVERLAY APKS ==="
cmd overlay list | grep -iE 'font|theme|tran'
"""

with open(r"C:\Users\Admin\deep_inspect.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\deep_inspect.sh", "/data/local/tmp/deep_inspect.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/deep_inspect.sh'"], capture_output=True, text=True)
print(res.stdout)

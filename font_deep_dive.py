import subprocess

cmd = r"""
echo "=== 1. ALL ACTIVE OVERLAYS ==="
cmd overlay list

echo "=== 2. ALL FONT RELATED OVERLAYS ==="
cmd overlay list | grep -iE 'font|theme|roboto|transans|noto'

echo "=== 3. ALL SETTINGS KEYS ==="
settings list system | grep -iE 'font|theme|type'
settings list secure | grep -iE 'font|theme|type'
settings list global | grep -iE 'font|theme|type'

echo "=== 4. ALL THEME DIRS IN /data ==="
ls -la /data/system/theme/ 2>/dev/null
ls -la /data/system/users/0/ 2>/dev/null
ls -la /data/fonts/files/ 2>/dev/null

echo "=== 5. ALL MOUNTS FOR FONTS ==="
cat /proc/mounts | grep -iE 'font|roboto|emoji|trans'
"""

with open(r"C:\Users\Admin\font_deep_dive.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\font_deep_dive.sh", "/data/local/tmp/font_deep_dive.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/font_deep_dive.sh'"], capture_output=True, text=True)
print(res.stdout)

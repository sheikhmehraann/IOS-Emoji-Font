import subprocess

cmd = r"""
echo "=== ALL SCRIPT / LANGUAGE FONTS ON DEVICE ==="
for f in /system/fonts/NotoSans*.ttf /system/fonts/NotoSans*.otf /system/fonts/NotoSerif*.ttf /system/fonts/NotoSerif*.otf; do
    [ -f "$f" ] || continue
    echo "$(basename "$f")"
done
"""

with open(r"C:\Users\Admin\list_all_languages.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\list_all_languages.sh", "/data/local/tmp/list_all_languages.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/list_all_languages.sh'"], capture_output=True, text=True)
print(res.stdout)

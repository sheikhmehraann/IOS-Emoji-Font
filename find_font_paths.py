import subprocess

cmd = r"""
echo "=== 1. WHERE IS THE ROBOTO FONT STORED IN SETTINGS / THEMES ==="
find /product /system_ext /system /vendor /data -name "*Roboto*" 2>/dev/null | grep -v "/data/adb/modules"

echo "=== 2. WHERE IS TRANSANS STORED IN SETTINGS / THEMES ==="
find /product /system_ext /system /vendor /data -name "*TranSans*" -o -name "*TransSans*" -o -name "*TOS*" 2>/dev/null | grep -v "/data/adb/modules"

echo "=== 3. WHAT HAPPENS IN SETTINGS DB WHEN YOU SWITCH FONTS ==="
settings get system current_font 2>/dev/null
settings get system font_path 2>/dev/null
settings get system system_font 2>/dev/null
settings get system theme_font 2>/dev/null
settings get global font_path 2>/dev/null
settings get secure font_path 2>/dev/null
"""

with open(r"C:\Users\Admin\find_font_paths.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\find_font_paths.sh", "/data/local/tmp/find_font_paths.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/find_font_paths.sh'"], capture_output=True, text=True)
print(res.stdout)

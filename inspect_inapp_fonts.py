import subprocess

cmd = r"""
echo "=== INSTAGRAM IN-APP FONTS IN /data/data/com.instagram.android ==="
find /data/data/com.instagram.android -iname "*.ttf" -o -iname "*.otf" 2>/dev/null

echo "=== INSTAGRAM APK ASSET FONTS ==="
IG_APK=$(pm path com.instagram.android | head -n 1 | cut -d: -f2)
echo "Instagram APK path: $IG_APK"
if [ -n "$IG_APK" ] && [ -f "$IG_APK" ]; then
    unzip -l "$IG_APK" 'assets/fonts/*' 2>/dev/null || unzip -l "$IG_APK" '*font*' 2>/dev/null
fi

echo "=== WHATSAPP IN-APP FONTS IN /data/data/com.whatsapp ==="
find /data/data/com.whatsapp -iname "*.ttf" -o -iname "*.otf" 2>/dev/null
"""

with open(r"C:\Users\Admin\inspect_inapp_fonts.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\inspect_inapp_fonts.sh", "/data/local/tmp/inspect_inapp_fonts.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/inspect_inapp_fonts.sh'"], capture_output=True, text=True)
print(res.stdout)

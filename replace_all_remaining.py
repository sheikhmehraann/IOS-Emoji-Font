import subprocess

cmd = r"""
FD="/data/adb/modules/ios_bold_font_emoji/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"

# Bind mount Apple SF Pro Bold over SourceSansPro, NotoSerif, NotoSans, and all text fonts
for f in /system/fonts/SourceSansPro*.ttf \
         /system/fonts/NotoSerif-*.ttf \
         /system/fonts/NotoSans-*.ttf \
         /system/fonts/CarroisGothic*.ttf \
         /system/fonts/CutiveMono*.ttf \
         /system/fonts/ComingSoon*.ttf \
         /system/fonts/DancingScript*.ttf \
         /system/fonts/DroidSansMono*.ttf; do
    [ -f "$f" ] || continue
    mount -o bind "$BTF" "$f" 2>/dev/null
    echo "Mounted over $(basename "$f")"
done

# Restart Gboard & Settings & UI
am force-stop com.google.android.inputmethod.latin 2>/dev/null
am force-stop com.android.settings 2>/dev/null
am force-stop com.transsion.theme 2>/dev/null
am force-stop com.google.android.apps.nexuslauncher 2>/dev/null
am force-stop com.transsion.XOSLauncher 2>/dev/null
am force-stop com.transsion.hilauncher 2>/dev/null

echo "COMPLETE: Replaced all UI, Serif, and SourceSans fonts with Apple SF Pro Bold!"
"""

with open(r"C:\Users\Admin\replace_all_remaining.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\replace_all_remaining.sh", "/data/local/tmp/replace_all_remaining.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/replace_all_remaining.sh'"], capture_output=True, text=True)
print(res.stdout)

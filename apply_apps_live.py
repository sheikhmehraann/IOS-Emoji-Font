import subprocess

cmd = r"""
MODPATH="/data/adb/modules/ios_bold_font_emoji"
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
NYF="$FD/NewYork-Bold.ttf"
RF="$FD/SF-Pro-Rounded.otf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
EF="$FD/NotoColorEmoji.ttf"

# 1. System Emoji
mount -o bind "$EF" /system/fonts/NotoColorEmoji.ttf 2>/dev/null
mount -o bind "$EF" /system/fonts/NotoColorEmojiFlags.ttf 2>/dev/null

# 2. All Roboto, GoogleSans, SourceSans styles
for f in /system/fonts/Roboto*.ttf \
         /system/fonts/GoogleSans*.ttf \
         /system/fonts/SourceSansPro*.ttf \
         /system/fonts/DroidSans*.ttf \
         /system/fonts/SECRoboto*.ttf \
         /system/fonts/NotoSans-*.ttf \
         /system/fonts/CarroisGothic*.ttf \
         /system/fonts/CutiveMono*.ttf \
         /system/fonts/ComingSoon*.ttf \
         /system/fonts/DancingScript*.ttf; do
    [ -f "$f" ] && mount -o bind "$BTF" "$f" 2>/dev/null
done

# 3. Product & Transsion fonts
for f in /product/fonts/* /system_ext/fonts/* /vendor/fonts/*; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    case "$fname" in
        *Emoji*|*emoji*|*Symbol*|*symbol*|*.ttc) continue ;;
        *Serif*|*serif*) mount -o bind "$NYF" "$f" 2>/dev/null ;;
        *Nastaliq*|*nastaliq*) mount -o bind "$UF" "$f" 2>/dev/null ;;
        *) mount -o bind "$BTF" "$f" 2>/dev/null ;;
    esac
done

# 4. Serif & Urdu
for f in /system/fonts/NotoSerif*.ttf; do [ -f "$f" ] && mount -o bind "$NYF" "$f" 2>/dev/null; done
for f in /system/fonts/NotoNaskhArabic*.ttf /system/fonts/NotoSansArabic*.ttf /system/fonts/NotoNastaliqUrdu*.ttf; do
    [ -f "$f" ] && mount -o bind "$UF" "$f" 2>/dev/null
done

# 5. Clear caches and force stop apps
for pkg in com.whatsapp com.instagram.android com.facebook.orca com.facebook.katana com.google.android.inputmethod.latin; do
    rm -rf "/data/data/$pkg/cache" "/data/data/$pkg/code_cache" "/data/data/$pkg/files/fonts" 2>/dev/null
    am force-stop "$pkg" 2>/dev/null
done

echo "APPLIED LIVE & FLUSHED APP CACHES!"
"""

with open(r"C:\Users\Admin\apply_apps_live.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\apply_apps_live.sh", "/data/local/tmp/apply_apps_live.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/apply_apps_live.sh'"], capture_output=True, text=True)
print(res.stdout)

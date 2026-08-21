import subprocess

cmd = r"""
FD="/data/adb/modules/ios_bold_font_emoji/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
NYF="$FD/NewYork-Bold.ttf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
AF="$FD/SF-Arabic.ttf"
HF="$FD/SF-Hebrew.ttf"
AMF="$FD/SF-Armenian.ttf"
GF="$FD/SF-Georgian.ttf"
EF="$FD/NotoColorEmoji.ttf"

# 1. Emoji bindings
mount -o bind "$EF" /system/fonts/NotoColorEmoji.ttf 2>/dev/null
mount -o bind "$EF" /system/fonts/NotoColorEmojiFlags.ttf 2>/dev/null

# 2. All UI / Roboto / TranSans / SourceSans / NotoSans
for f in /system/fonts/Roboto*.ttf \
         /system/fonts/DroidSans*.ttf \
         /system/fonts/GoogleSans*.ttf \
         /system/fonts/SECRoboto*.ttf \
         /system/fonts/SourceSansPro*.ttf \
         /system/fonts/NotoSans-*.ttf \
         /system/fonts/CarroisGothic*.ttf \
         /system/fonts/CutiveMono*.ttf \
         /system/fonts/ComingSoon*.ttf \
         /system/fonts/DancingScript*.ttf; do
    [ -f "$f" ] && mount -o bind "$BTF" "$f" 2>/dev/null
done

# 3. NotoSerif to Apple New York Serif Heavy
for f in /system/fonts/NotoSerif-*.ttf; do
    [ -f "$f" ] && mount -o bind "$NYF" "$f" 2>/dev/null
done

# 4. Transsion OS product fonts
for f in /product/fonts/*; do
    [ -f "$f" ] || continue
    mount -o bind "$BTF" "$f" 2>/dev/null
done

# 5. Urdu Nastaliq Bold
for f in /system/fonts/NotoNaskhArabic*.ttf /system/fonts/NotoSansArabic*.ttf /system/fonts/NotoNastaliqUrdu*.ttf; do
    [ -f "$f" ] && mount -o bind "$UF" "$f" 2>/dev/null
done

# 6. Apple Multilingual Bold
for f in /system/fonts/NotoSansHebrew*.ttf; do [ -f "$f" ] && mount -o bind "$HF" "$f" 2>/dev/null; done
for f in /system/fonts/NotoSansArmenian*.ttf; do [ -f "$f" ] && mount -o bind "$AMF" "$f" 2>/dev/null; done
for f in /system/fonts/NotoSansGeorgian*.ttf; do [ -f "$f" ] && mount -o bind "$GF" "$f" 2>/dev/null; done

# 7. Patched World Language Variable Fonts (Hindi, Bengali, Tamil, Telugu, Malayalam, Kannada, Punjabi, etc.)
for f in "$FD"/*-VF.ttf; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    [ -f "/system/fonts/$fname" ] && mount -o bind "$f" "/system/fonts/$fname" 2>/dev/null
done

# 8. World Language Bold variants over Regular (Thai, Lao, Myanmar, Oriya, Gujarati, etc.)
for bfont in /system/fonts/*Bold*.ttf /system/fonts/*Bold*.otf; do
    [ -f "$bfont" ] || continue
    rname=$(basename "$bfont" | sed 's/Bold/Regular/g')
    [ "$rname" != "$(basename "$bfont")" ] && [ -f "/system/fonts/$rname" ] && mount -o bind "$bfont" "/system/fonts/$rname" 2>/dev/null
done

# Restart Zygote
setprop ctl.restart zygote

echo "ALL WORLD LANGUAGES BOLD APPLIED LIVE!"
"""

with open(r"C:\Users\Admin\apply_all_languages_live.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\apply_all_languages_live.sh", "/data/local/tmp/apply_all_languages_live.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/apply_all_languages_live.sh'"], capture_output=True, text=True)
print(res.stdout)

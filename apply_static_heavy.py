import subprocess

cmd = r"""
FD="/data/adb/modules/ios_bold_font_emoji/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
NYF="$FD/NewYork-Bold.ttf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
EF="$FD/NotoColorEmoji.ttf"

# Bind mount Emoji
mount -o bind "$EF" /system/fonts/NotoColorEmoji.ttf 2>/dev/null
mount -o bind "$EF" /system/fonts/NotoColorEmojiFlags.ttf 2>/dev/null

# Bind mount all UI / Roboto / TranSans / SourceSans / NotoSans
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

# Bind mount NotoSerif to Apple New York Serif Heavy
for f in /system/fonts/NotoSerif-*.ttf; do
    [ -f "$f" ] && mount -o bind "$NYF" "$f" 2>/dev/null
done

# Bind mount Transsion OS product fonts (TOS_250829VF, TransSans_SC_0704, etc.)
for f in /product/fonts/*; do
    [ -f "$f" ] || continue
    mount -o bind "$BTF" "$f" 2>/dev/null
done

# Bind mount Urdu Nastaliq Bold
for f in /system/fonts/NotoNaskhArabic*.ttf /system/fonts/NotoSansArabic*.ttf /system/fonts/NotoNastaliqUrdu*.ttf; do
    [ -f "$f" ] && mount -o bind "$UF" "$f" 2>/dev/null
done

# Restart Zygote
setprop ctl.restart zygote

echo "LIVE BIND-MOUNT APPLIED & ZYGOTE RELOADED!"
"""

with open(r"C:\Users\Admin\apply_static_heavy.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\apply_static_heavy.sh", "/data/local/tmp/apply_static_heavy.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/apply_static_heavy.sh'"], capture_output=True, text=True)
print(res.stdout)

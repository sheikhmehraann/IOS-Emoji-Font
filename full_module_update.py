import subprocess

cmd = r"""
# Unzip full module directly
unzip -o /data/local/tmp/iOS_Bold_Font_Emoji_v2.0_Ultra.zip -d /data/adb/modules/ios_bold_font_emoji/ >/dev/null 2>&1

MODPATH="/data/adb/modules/ios_bold_font_emoji"
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
NYF="$FD/NewYork-Bold.ttf"
RF="$FD/SF-Pro-Rounded.otf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
AF="$FD/SF-Arabic.ttf"
EF="$FD/NotoColorEmoji.ttf"

# Overwrite all module product, system_ext, and vendor fonts with the new TrueType binary
for f in "$MODPATH"/system/product/fonts/* "$MODPATH"/system/system_ext/fonts/* "$MODPATH"/system/vendor/fonts/*; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    case "$fname" in
        *Emoji*|*emoji*|*Symbol*|*symbol*|*.ttc) continue ;;
        *Serif*|*serif*) cp -f "$NYF" "$f" 2>/dev/null ;;
        *Nastaliq*|*nastaliq*) cp -f "$UF" "$f" 2>/dev/null ;;
        *) cp -f "$BTF" "$f" 2>/dev/null ;;
    esac
done

chmod 755 "$MODPATH"/*.sh
chmod 644 "$MODPATH"/system/fonts/*
chmod 644 "$MODPATH"/system/product/fonts/* 2>/dev/null

echo "MODULE FULLY UPDATED WITH PURE TRUETYPE FONTS ACROSS ALL PARTITIONS!"
"""

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\dist\iOS_Bold_Font_Emoji_v2.0_Ultra.zip", "/data/local/tmp/iOS_Bold_Font_Emoji_v2.0_Ultra.zip"], check=True)

with open(r"C:\Users\Admin\full_module_update.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\full_module_update.sh", "/data/local/tmp/full_module_update.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/full_module_update.sh'"], capture_output=True, text=True)
print(res.stdout)

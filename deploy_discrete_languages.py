import subprocess
import os

zip_path = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\dist\iOS_Bold_Font_Emoji_v2.0_Ultra.zip"

cmd = r"""
# Clean old module directory
rm -rf /data/adb/modules/ios_bold_font_emoji/*

# Extract new zip
unzip -o /data/local/tmp/iOS_Bold_Font_Emoji_v2.0_Ultra.zip -d /data/adb/modules/ios_bold_font_emoji/ >/dev/null 2>&1

MODPATH="/data/adb/modules/ios_bold_font_emoji"
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
NYF="$FD/NewYork-Bold.ttf"
RF="$FD/SF-Pro-Rounded.otf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
AF="$FD/SF-Arabic.ttf"
HF="$FD/SF-Hebrew.ttf"
AMF="$FD/SF-Armenian.ttf"
GF="$FD/SF-Georgian.ttf"
EF="$FD/NotoColorEmoji.ttf"

mkdir -p "$MODPATH/system/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/product/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/system_ext/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/vendor/fonts" 2>/dev/null

place() {
    local src="$1" name="$2"
    cp -f "$src" "$MODPATH/system/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/product/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/system_ext/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/vendor/fonts/$name" 2>/dev/null
}

# 1. English / Latin / UI Fonts ONLY
for pdir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts; do
    [ -d "$pdir" ] || continue
    for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
        case "$fname" in
            Roboto*|GoogleSans*|SourceSans*|DroidSans*|SECRoboto*|\
            TranSans*|TOS*|TransSans*|InfinixSans*|TecnoSans*|ItelSans*|\
            MiSans*|Miui*|OPlusSans*|OnePlusSans*|Samsung*|\
            CarroisGothic*|CutiveMono*|ComingSoon*|DancingScript*)
                place "$BTF" "$fname"
                ;;
            *Clock*|*clock*)
                place "$RF" "$fname"
                ;;
        esac
    done
done

# 2. Apple New York Serif
for f in NotoSerif-Regular.ttf NotoSerif-Bold.ttf NotoSerif-Italic.ttf NotoSerif-BoldItalic.ttf; do
    place "$NYF" "$f"
done

# 3. Urdu Nastaliq
for f in NotoNastaliqUrdu-Regular.ttf NotoNastaliqUrdu-Bold.ttf NotoNastaliqUrdu.ttf \
         NotoNastaliqUrdu-VF.ttf NotoNastaliqUrdu[wght].ttf; do
    place "$UF" "$f"
done

# 4. Arabic
for f in NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf \
         NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf \
         NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf \
         NotoSansArabicUI-Regular.ttf NotoSansArabicUI-Bold.ttf \
         NotoKufiArabic-Regular.ttf NotoKufiArabic-Bold.ttf; do
    place "$AF" "$f"
done

# 5. Hebrew
for f in NotoSansHebrew-Regular.ttf NotoSansHebrew-Bold.ttf \
         NotoSansHebrew-VF.ttf NotoSerifHebrew-Regular.ttf NotoSerifHebrew-Bold.ttf; do
    place "$HF" "$f"
done

# 6. Armenian
for f in NotoSansArmenian-Regular.ttf NotoSansArmenian-Bold.ttf \
         NotoSansArmenian-VF.ttf NotoSerifArmenian-Regular.ttf NotoSerifArmenian-Bold.ttf; do
    place "$AMF" "$f"
done

# 7. Georgian
for f in NotoSansGeorgian-Regular.ttf NotoSansGeorgian-Bold.ttf \
         NotoSansGeorgian-VF.ttf NotoSerifGeorgian-Regular.ttf NotoSerifGeorgian-Bold.ttf; do
    place "$GF" "$f"
done

# 8. Indic & World Script Fonts
for vf in "$FD"/*-VF.ttf; do
    [ -f "$vf" ] || continue
    vname=$(basename "$vf")
    place "$vf" "$vname"
done

# 9. Emoji
for f in SamsungColorEmoji.ttf LGNotoColorEmoji.ttf HTC_ColorEmoji.ttf \
         AndroidEmoji-htc.ttf ColorUniEmoji.ttf DcmColorEmoji.ttf \
         CombinedColorEmoji.ttf NotoColorEmojiLegacy.ttf NotoColorEmoji-Flags.ttf NotoColorEmojiFlags.ttf; do
    if [ -f "/system/fonts/$f" ] || [ -f "/product/fonts/$f" ] || [ -f "/system_ext/fonts/$f" ]; then
        place "$EF" "$f"
    fi
done

chmod 755 "$MODPATH"/*.sh
chmod 644 "$MODPATH"/system/fonts/* 2>/dev/null
chmod 644 "$MODPATH"/system/product/fonts/* 2>/dev/null
chmod 644 "$MODPATH"/system/system_ext/fonts/* 2>/dev/null
chmod 644 "$MODPATH"/system/vendor/fonts/* 2>/dev/null

echo "DEPLOYMENT COMPLETE WITH 100% DISCRETE LANGUAGE MAPPINGS!"
"""

print(f"Pushing {zip_path} to device...")
subprocess.run([r"C:\platform-tools\adb.exe", "push", zip_path, "/data/local/tmp/iOS_Bold_Font_Emoji_v2.0_Ultra.zip"], check=True)

with open(r"C:\Users\Admin\deploy_discrete_languages.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\deploy_discrete_languages.sh", "/data/local/tmp/deploy_discrete_languages.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/deploy_discrete_languages.sh'"], capture_output=True, text=True)
print(res.stdout)

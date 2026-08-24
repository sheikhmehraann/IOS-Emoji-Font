#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Multilingual Daemon
# Author: sheikhmehraan
##########################################################################################

MODPATH=${0%/*}
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

# 1. System Emoji
mount -o bind "$EF" /system/fonts/NotoColorEmoji.ttf 2>/dev/null
mount -o bind "$EF" /system/fonts/NotoColorEmojiFlags.ttf 2>/dev/null

# 2. All Roboto, GoogleSans, SourceSans, DroidSans styles
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

# 3. All Product & Transsion OS UI fonts (TranSans, TOS, TransSans_SC_0704, TOS_250829VF, InfinixSans, TecnoSans)
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

# 4. Serif & Multilingual script mounts
for f in /system/fonts/NotoSerif*.ttf; do [ -f "$f" ] && mount -o bind "$NYF" "$f" 2>/dev/null; done
for f in /system/fonts/NotoNaskhArabic*.ttf /system/fonts/NotoSansArabic*.ttf /system/fonts/NotoNastaliqUrdu*.ttf; do
    [ -f "$f" ] && mount -o bind "$UF" "$f" 2>/dev/null
done

# Bind mount patched multilingual variable fonts
for f in "$FD"/*-VF.ttf; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    [ -f "/system/fonts/$fname" ] && mount -o bind "$f" "/system/fonts/$fname" 2>/dev/null
    [ -f "/product/fonts/$fname" ] && mount -o bind "$f" "/product/fonts/$fname" 2>/dev/null
done

while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done

# Replace in-app emoji & fonts
if [ -f "$EF" ]; then
    for font in $(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null); do
        [ -w "$font" ] && cp -f "$EF" "$font" && chmod 644 "$font" 2>/dev/null
    done
fi

# WhatsApp in-app font lock
if [ -d "/data/data/com.whatsapp" ]; then
    mkdir -p "/data/data/com.whatsapp/files/NetworkResource" 2>/dev/null
    chattr -i "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    cp -f "$BTF" "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    chmod 444 "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    chattr +i "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
fi

for pkg in com.facebook.orca com.facebook.katana com.facebook.lite com.facebook.mlite; do
    [ -d "/data/data/$pkg" ] || continue
    t="/data/data/$pkg/app_ras_blobs/FacebookEmoji.ttf"
    mkdir -p "/data/data/$pkg/app_ras_blobs" 2>/dev/null
    cp -f "$EF" "$t" 2>/dev/null
    chmod 444 "$t" 2>/dev/null
    chattr +i "$t" 2>/dev/null
done

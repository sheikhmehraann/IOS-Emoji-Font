#!/system/bin/sh
MODPATH=${0%/*}
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
NYF="$FD/NewYork-Bold.ttf"
RF="$FD/SF-Pro-Rounded.otf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
EF="$FD/NotoColorEmoji.ttf"

mount -o bind "$EF" /system/fonts/NotoColorEmoji.ttf 2>/dev/null
mount -o bind "$EF" /system/fonts/NotoColorEmojiFlags.ttf 2>/dev/null
mount -o bind "$BTF" /system/fonts/Roboto-Regular.ttf 2>/dev/null
mount -o bind "$BTF" /product/fonts/TOS_250829VF.ttf 2>/dev/null
mount -o bind "$BTF" /product/fonts/TransSans_SC_0704.ttf 2>/dev/null
mount -o bind "$UF" /system/fonts/NotoNaskhArabic-Regular.ttf 2>/dev/null
mount -o bind "$UF" /system/fonts/NotoNaskhArabic-Bold.ttf 2>/dev/null
mount -o bind "$NYF" /system/fonts/NotoSerif-Regular.ttf 2>/dev/null

while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done

# Replace in-app emoji fonts
if [ -f "$EF" ]; then
    for font in $(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null); do
        [ -w "$font" ] && cp -f "$EF" "$font" && chmod 644 "$font" 2>/dev/null
    done
fi

for pkg in com.facebook.orca com.facebook.katana com.facebook.lite com.facebook.mlite; do
    [ -d "/data/data/$pkg" ] || continue
    t="/data/data/$pkg/app_ras_blobs/FacebookEmoji.ttf"
    mkdir -p "/data/data/$pkg/app_ras_blobs" 2>/dev/null
    cp -f "$EF" "$t" 2>/dev/null
    chmod 444 "$t" 2>/dev/null
    chattr +i "$t" 2>/dev/null
done

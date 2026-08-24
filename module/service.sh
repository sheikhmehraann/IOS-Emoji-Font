#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Safe Post-Boot Daemon
# Author: sheikhmehraan
##########################################################################################

MODPATH=${0%/*}
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
EF="$FD/NotoColorEmoji.ttf"

# Wait until Android fully completes boot to avoid any system_server startup race
while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done

# Replace in-app emoji fonts in WhatsApp / Facebook / Instagram / Gboard
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

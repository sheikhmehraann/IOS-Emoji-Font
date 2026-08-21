#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Universal Font Daemon
# Author: sheikhmehraan
##########################################################################################

MODPATH=${0%/*}
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
BOF="$FD/SF-Pro-Bold.otf"
VF="$FD/SF-Pro-Variable.ttf"
RF="$FD/SF-Pro-Rounded.otf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
AF="$FD/SF-Arabic.ttf"
HF="$FD/SF-Hebrew.ttf"
AMF="$FD/SF-Armenian.ttf"
GF="$FD/SF-Georgian.ttf"
EF="$FD/NotoColorEmoji.ttf"

# Apply direct mount binding (KernelSU GKI / EROFS / Android 15 fallback)
mount -o bind "$EF" /system/fonts/NotoColorEmoji.ttf 2>/dev/null
mount -o bind "$EF" /system/fonts/NotoColorEmojiFlags.ttf 2>/dev/null

for f in /system/fonts/Roboto*.ttf /system/fonts/DroidSans*.ttf /system/fonts/GoogleSans*.ttf /system/fonts/SECRoboto*.ttf; do
    [ -f "$f" ] && mount -o bind "$BTF" "$f" 2>/dev/null
done

for f in /product/fonts/*; do
    [ -f "$f" ] || continue
    mount -o bind "$BTF" "$f" 2>/dev/null
done

for f in /system/fonts/NotoNaskhArabic*.ttf /system/fonts/NotoSansArabic*.ttf /system/fonts/NotoNastaliqUrdu*.ttf; do
    [ -f "$f" ] && mount -o bind "$UF" "$f" 2>/dev/null
done

for f in /system/fonts/NotoSansHebrew*.ttf; do [ -f "$f" ] && mount -o bind "$HF" "$f" 2>/dev/null; done
for f in /system/fonts/NotoSansArmenian*.ttf; do [ -f "$f" ] && mount -o bind "$AMF" "$f" 2>/dev/null; done
for f in /system/fonts/NotoSansGeorgian*.ttf; do [ -f "$f" ] && mount -o bind "$GF" "$f" 2>/dev/null; done
for f in /system/fonts/AndroidClock*.ttf; do [ -f "$f" ] && mount -o bind "$RF" "$f" 2>/dev/null; done

while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done

# Replace in-app emoji fonts
if [ -f "$EF" ]; then
    for font in $(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null); do
        [ -w "$font" ] && cp -f "$EF" "$font" && chmod 644 "$font" 2>/dev/null
    done
fi

# Lock Messenger / Facebook emoji
for pkg in com.facebook.orca com.facebook.katana com.facebook.lite com.facebook.mlite; do
    [ -d "/data/data/$pkg" ] || continue
    t="/data/data/$pkg/app_ras_blobs/FacebookEmoji.ttf"
    mkdir -p "/data/data/$pkg/app_ras_blobs" 2>/dev/null
    cp -f "$EF" "$t" 2>/dev/null
    chmod 444 "$t" 2>/dev/null
    chattr +i "$t" 2>/dev/null
    for sub in /files/fonts /cache /code_cache; do
        rm -rf "/data/data/${pkg}${sub}" 2>/dev/null
    done
    am force-stop "$pkg" 2>/dev/null
done

# Disable GMS font updater services
for uid in $(ls /data/user/ 2>/dev/null); do
    pm disable --user "$uid" "com.google.android.gms/com.google.android.gms.fonts.provider.FontsProvider" 2>/dev/null
    pm disable --user "$uid" "com.google.android.gms/com.google.android.gms.fonts.update.UpdateSchedulerService" 2>/dev/null
done
rm -rf /data/fonts/* 2>/dev/null
find /data -type d -path "*com.google.android.gms/files/fonts*" -exec rm -rf {} + 2>/dev/null

#!/system/bin/sh
MODPATH=${0%/*}

while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 5; done
while [ ! -d /sdcard ]; do sleep 5; done

EF="$MODPATH/system/fonts/NotoColorEmoji.ttf"

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
    for sub in /files/fonts /cache /code_cache; do
        rm -rf "/data/data/${pkg}${sub}" 2>/dev/null
    done
    am force-stop "$pkg" 2>/dev/null
done

for uid in $(ls /data/user/ 2>/dev/null); do
    pm disable --user "$uid" "com.google.android.gms/com.google.android.gms.fonts.provider.FontsProvider" 2>/dev/null
    pm disable --user "$uid" "com.google.android.gms/com.google.android.gms.fonts.update.UpdateSchedulerService" 2>/dev/null
done
rm -rf /data/fonts/* 2>/dev/null
find /data -type d -path "*com.google.android.gms/files/fonts*" -exec rm -rf {} + 2>/dev/null

#!/system/bin/sh
MODPATH=${0%/*}
rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null
for pkg in com.instagram.android com.whatsapp com.facebook.orca com.facebook.katana; do
    rm -rf "/data/data/$pkg/cache" "/data/data/$pkg/code_cache" "/data/data/$pkg/files/fonts" 2>/dev/null
done

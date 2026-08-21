#!/system/bin/sh
MODPATH=${0%/*}
rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

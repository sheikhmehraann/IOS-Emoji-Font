#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Early Boot Daemon (post-fs-data.sh)
# Author: sheikhmehraan
#
# 100% Boot-Safe: Only purges FontManager cache. Zero bind-mounts (handled by Magisk overlay).
##########################################################################################

rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

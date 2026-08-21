#!/system/bin/sh
##########################################################################################
#
#  iOS Bold Font & iOS 26.4 Emoji - post-fs-data.sh
# Author: sheikhmehraan
#
##########################################################################################

MODPATH=${0%/*}
BASE_FONT="$MODPATH/system/fonts/Roboto-Regular.ttf"
BASE_EMOJI="$MODPATH/system/fonts/NotoColorEmoji.ttf"

# Clean dynamic Android 12-16 FontManager caches before system_server starts
rm -rf /data/fonts/* 2>/dev/null
rm -rf /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/fonts/run_metadata.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

mkdir -p /data/fonts 2>/dev/null
chmod 755 /data/fonts 2>/dev/null

# Universal Dynamic Bind-Mount across ALL active partitions & fonts
if [ -f "$BASE_FONT" ]; then
    for target_dir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts /system/product/fonts /system/system_ext/fonts; do
        if [ -d "$target_dir" ]; then
            for fpath in "$target_dir"/*.ttf "$target_dir"/*.otf; do
                [ -f "$fpath" ] || continue
                fname=$(basename "$fpath")
                case "$fname" in
                    *Emoji*|*emoji*)
                        if [ -f "$BASE_EMOJI" ]; then
                            mount -o bind "$BASE_EMOJI" "$fpath" 2>/dev/null
                        fi
                        ;;
                    *Symbol*|*symbol*|*Clock*|*clock*|*NotoSansHebrew*|*NotoSansArabic*|*NotoSansThai*) ;;
                    *)
                        if [ -f "$MODPATH/system/fonts/$fname" ]; then
                            mount -o bind "$MODPATH/system/fonts/$fname" "$fpath" 2>/dev/null
                        elif [ -f "$MODPATH/product/fonts/$fname" ]; then
                            mount -o bind "$MODPATH/product/fonts/$fname" "$fpath" 2>/dev/null
                        elif [ -f "$MODPATH/system_ext/fonts/$fname" ]; then
                            mount -o bind "$MODPATH/system_ext/fonts/$fname" "$fpath" 2>/dev/null
                        else
                            mount -o bind "$BASE_FONT" "$fpath" 2>/dev/null
                        fi
                        ;;
                esac
            done
        fi
    done
fi

#!/system/bin/sh
##########################################################################################
#
#  iOS Bold Font & iOS 26.4 Emoji - post-fs-data.sh
# Author: sheikhmehraan
#
##########################################################################################

MODPATH=${0%/*}

# Clean dynamic Android 12-16 FontManager caches before system_server starts
rm -rf /data/fonts/* 2>/dev/null
rm -rf /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/fonts/run_metadata.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

mkdir -p /data/fonts 2>/dev/null
chmod 755 /data/fonts 2>/dev/null

# Direct bind-mount fallback
if [ -f "$MODPATH/system/fonts/NotoColorEmoji.ttf" ]; then
    for emoji_target in /system/fonts/NotoColorEmoji.ttf /system/fonts/SamsungColorEmoji.ttf /system/fonts/ColorUniEmoji.ttf; do
        if [ -f "$emoji_target" ]; then
            mount -o bind "$MODPATH/system/fonts/NotoColorEmoji.ttf" "$emoji_target" 2>/dev/null
        fi
    done
fi

if [ -f "$MODPATH/system/fonts/Roboto-Regular.ttf" ]; then
    for font_target in \
        /system/fonts/Roboto-VariableFont_wdth,wght.ttf \
        /system/fonts/Roboto-Italic-VariableFont_wdth,wght.ttf \
        /system/fonts/RobotoFlex-Regular.ttf \
        /system/fonts/Roboto-Regular.ttf \
        /system/fonts/Roboto-Bold.ttf \
        /system/fonts/Roboto-Medium.ttf \
        /system/fonts/RobotoStatic-Regular.ttf \
        /system/fonts/TranSansShell.ttf \
        /system/fonts/TranSansSCShell.ttf; do
        if [ -f "$font_target" ]; then
            mount -o bind "$MODPATH/system/fonts/Roboto-Regular.ttf" "$font_target" 2>/dev/null
        fi
    done

    for prod_target in \
        /product/fonts/TOS_VF.ttf \
        /system/product/fonts/TOS_VF.ttf \
        /product/fonts/TranSans_SC.ttf \
        /system/product/fonts/TranSans_SC.ttf \
        /product/fonts/TransSans_Thai.ttf \
        /system/product/fonts/TransSans_Thai.ttf; do
        if [ -f "$prod_target" ] && [ -f "$MODPATH/system/product/fonts/TOS_VF.ttf" ]; then
            mount -o bind "$MODPATH/system/product/fonts/TOS_VF.ttf" "$prod_target" 2>/dev/null
        elif [ -f "$prod_target" ]; then
            mount -o bind "$MODPATH/system/fonts/Roboto-Regular.ttf" "$prod_target" 2>/dev/null
        fi
    done

    for ext_target in \
        /system_ext/fonts/TOS_VF.ttf \
        /system/system_ext/fonts/TOS_VF.ttf \
        /system_ext/fonts/TranSansShell.ttf \
        /system/system_ext/fonts/TranSansShell.ttf; do
        if [ -f "$ext_target" ]; then
            mount -o bind "$MODPATH/system/fonts/Roboto-Regular.ttf" "$ext_target" 2>/dev/null
        fi
    done
fi

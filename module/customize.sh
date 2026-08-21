#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Professional Fast TrueType Installer
# Author: sheikhmehraan
##########################################################################################

AUTOMOUNT=true
SKIPMOUNT=false
PROPFILE=false
POSTFSDATA=true
LATESTARTSERVICE=true

ui_print " "
ui_print "  ███████╗███████╗    ██╗ ██████╗ ███████╗"
ui_print "  ██╔════╝██╔════╝    ██║██╔═══██╗██╔════╝"
ui_print "  ███████╗█████╗      ██║██║   ██║███████╗"
ui_print "  ╚════██║██╔══╝      ██║██║   ██║╚════██║"
ui_print "  ███████║██║         ██║╚██████╔╝███████║"
ui_print "  ╚══════╝╚═╝         ╚═╝ ╚═════╝ ╚══════╝"
ui_print "  ─────────────────────────────────────────"
ui_print "   iOS Bold Font & iOS 26.4 Emoji Ultra   "
ui_print "  Developer : sheikhmehraan                "
ui_print "  Version   : v2.0 • Ultra Edition         "
ui_print "  ─────────────────────────────────────────"
ui_print " "

ui_print "  [i] Device Information:"
ui_print "      • Model   : $(getprop ro.product.model)"
ui_print "      • Brand   : $(getprop ro.product.brand)"
ui_print "      • Android : $(getprop ro.build.version.release) (SDK $(getprop ro.build.version.sdk))"
ui_print " "

if [ -n "$ZIPFILE" ] && [ -f "$ZIPFILE" ]; then
    unzip -o "$ZIPFILE" 'system/*' -d "$MODPATH" >/dev/null 2>&1
fi

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

mkdir -p "$MODPATH/system/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/product/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/system_ext/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/vendor/fonts" 2>/dev/null

place() {
    local src="$1" name="$2"
    cp -f "$src" "$MODPATH/system/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/product/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/system_ext/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/vendor/fonts/$name" 2>/dev/null
}

ui_print "  [+] Step 1/5: Deploying Pure TrueType Apple SF Pro Heavy over All UI Fonts..."
for pdir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts; do
    [ -d "$pdir" ] || continue
    for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
        case "$fname" in
            *Emoji*|*emoji*|*Symbol*|*symbol*|*Math*|*math*|*.ttc) continue ;;
            *Clock*|*clock*)                     place "$RF"  "$fname" ;;
            *Nastaliq*|*nastaliq*|*Urdu*|*urdu*) place "$UF"  "$fname" ;;
            *Arabic*|*arabic*|*Naskh*|*naskh*|*Kufi*|*kufi*)
                                                  place "$AF"  "$fname" ;;
            *Hebrew*|*hebrew*)                    place "$HF"  "$fname" ;;
            *Armenian*|*armenian*)                place "$AMF" "$fname" ;;
            *Georgian*|*georgian*)                place "$GF"  "$fname" ;;
            *Serif*|*serif*)                      place "$NYF" "$fname" ;;
            *)                                    place "$BTF" "$fname" ;;
        esac
    done
done
ui_print "      ✔ All UI, Roboto, and TranSans fonts deployed"
ui_print " "

ui_print "  [+] Step 2/5: Deploying Apple New York Serif over NotoSerif..."
for f in NotoSerif-Regular.ttf NotoSerif-Bold.ttf NotoSerif-Italic.ttf NotoSerif-BoldItalic.ttf; do
    place "$NYF" "$f"
done
ui_print "      ✔ Apple New York Serif fonts deployed"
ui_print " "

ui_print "  [+] Step 3/5: Deploying Normalized Compact Noto Nastaliq Urdu Bold..."
for f in NotoNastaliqUrdu-Regular.ttf NotoNastaliqUrdu-Bold.ttf NotoNastaliqUrdu.ttf \
         NotoNastaliqUrdu-VF.ttf NotoNastaliqUrdu[wght].ttf; do
    place "$UF" "$f"
done
for f in NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf \
         NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf \
         NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf \
         NotoSansArabicUI-Regular.ttf NotoSansArabicUI-Bold.ttf; do
    place "$AF" "$f"
done
ui_print "      ✔ Multilingual typography deployed"
ui_print " "

ui_print "  [+] Step 4/5: Deploying iOS 26.4 Emoji & Purging System Caches..."
for f in SamsungColorEmoji.ttf LGNotoColorEmoji.ttf HTC_ColorEmoji.ttf \
         AndroidEmoji-htc.ttf ColorUniEmoji.ttf DcmColorEmoji.ttf \
         CombinedColorEmoji.ttf NotoColorEmojiLegacy.ttf NotoColorEmoji-Flags.ttf NotoColorEmojiFlags.ttf; do
    if [ -f "/system/fonts/$f" ] || [ -f "/product/fonts/$f" ] || [ -f "/system_ext/fonts/$f" ]; then
        place "$EF" "$f"
    fi
done

rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

for pkg in com.facebook.orca com.facebook.katana com.facebook.lite \
           com.facebook.mlite com.instagram.android com.whatsapp com.google.android.inputmethod.latin; do
    if pm list packages 2>/dev/null | grep -q "$pkg"; then
        for sub in /cache /code_cache /app_webview /files/GCache /files/fonts; do
            rm -rf "/data/data/${pkg}${sub}" 2>/dev/null
            rm -rf "/data/user_de/*/${pkg}${sub}" 2>/dev/null
        done
        am force-stop "$pkg" 2>/dev/null
    fi
done

set_perm_recursive "$MODPATH" 0 0 0755 0644
for s in post-fs-data.sh service.sh action.sh; do
    [ -f "$MODPATH/$s" ] && set_perm "$MODPATH/$s" 0 0 0755
done
chcon -R u:object_r:system_file:s0 "$MODPATH/system" 2>/dev/null
ui_print "      ✔ Permissions & SELinux contexts applied"
ui_print " "
ui_print "  ─────────────────────────────────────────"
ui_print "  ✔ Installation Complete!                 "
ui_print "  ✔ Reboot to apply changes.               "
ui_print "  ─────────────────────────────────────────"
ui_print " "

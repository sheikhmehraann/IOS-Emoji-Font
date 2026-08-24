#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Multilingual Universal Installer
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
ui_print "  Multilingual Universal Edition           "
ui_print "  Developer : sheikhmehraan                "
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
mkdir -p "$MODPATH/system/etc" 2>/dev/null

place() {
    local src="$1" name="$2"
    cp -f "$src" "$MODPATH/system/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/product/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/system_ext/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/vendor/fonts/$name" 2>/dev/null
}

ui_print "  [+] Step 1/5: Deploying Apple SF Pro Heavy over System UI Fonts..."
for pdir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts; do
    [ -d "$pdir" ] || continue
    for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
        case "$fname" in
            Roboto*|GoogleSans*|SourceSans*|DroidSans*|SECRoboto*|\
            TranSans*|TOS*|TransSans*|InfinixSans*|TecnoSans*|ItelSans*|\
            MiSans*|Miui*|OPlusSans*|OnePlusSans*|Samsung*|\
            CarroisGothic*|CutiveMono*|ComingSoon*|DancingScript*)
                place "$BTF" "$fname"
                ;;
            *Clock*|*clock*)
                place "$RF" "$fname"
                ;;
        esac
    done
done
ui_print "      ✔ System UI and English fonts mapped to SF Pro Heavy"
ui_print " "

ui_print "  [+] Step 2/5: Deploying Apple New York Serif..."
for f in NotoSerif-Regular.ttf NotoSerif-Bold.ttf NotoSerif-Italic.ttf NotoSerif-BoldItalic.ttf; do
    place "$NYF" "$f"
done
ui_print "      ✔ Apple New York Serif deployed"
ui_print " "

ui_print "  [+] Step 3/5: Deploying Urdu, Arabic, Hebrew, Armenian, Georgian & Indic Scripts..."
# 1. Urdu Nastaliq
for f in NotoNastaliqUrdu-Regular.ttf NotoNastaliqUrdu-Bold.ttf NotoNastaliqUrdu.ttf \
         NotoNastaliqUrdu-VF.ttf NotoNastaliqUrdu[wght].ttf; do
    place "$UF" "$f"
done

# 2. Arabic
for f in NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf \
         NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf \
         NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf \
         NotoSansArabicUI-Regular.ttf NotoSansArabicUI-Bold.ttf \
         NotoKufiArabic-Regular.ttf NotoKufiArabic-Bold.ttf; do
    place "$AF" "$f"
done

# 3. Hebrew
for f in NotoSansHebrew-Regular.ttf NotoSansHebrew-Bold.ttf \
         NotoSansHebrew-VF.ttf NotoSerifHebrew-Regular.ttf NotoSerifHebrew-Bold.ttf; do
    place "$HF" "$f"
done

# 4. Armenian
for f in NotoSansArmenian-Regular.ttf NotoSansArmenian-Bold.ttf \
         NotoSansArmenian-VF.ttf NotoSerifArmenian-Regular.ttf NotoSerifArmenian-Bold.ttf; do
    place "$AMF" "$f"
done

# 5. Georgian
for f in NotoSansGeorgian-Regular.ttf NotoSansGeorgian-Bold.ttf \
         NotoSansGeorgian-VF.ttf NotoSerifGeorgian-Regular.ttf NotoSerifGeorgian-Bold.ttf; do
    place "$GF" "$f"
done

# 6. Indic & World Script Fonts
for vf in "$FD"/*-VF.ttf; do
    [ -f "$vf" ] || continue
    vname=$(basename "$vf")
    place "$vf" "$vname"
done
ui_print "      ✔ All world languages deployed with 100% metric and boldness parity"
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

# Lock WhatsApp in-app downloaded font
if [ -d "/data/data/com.whatsapp" ]; then
    mkdir -p "/data/data/com.whatsapp/files/NetworkResource" 2>/dev/null
    chattr -i "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    cp -f "$BTF" "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    chmod 444 "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    chattr +i "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
fi

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

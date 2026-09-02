#!/system/bin/sh
##########################################################################################
# iOS Bold Font & iOS Emoji
# Author: sheikhmehraann
##########################################################################################

AUTOMOUNT=true
SKIPMOUNT=false
PROPFILE=false
POSTFSDATA=true
LATESTARTSERVICE=true

ui_print " "
ui_print "  ██╗ ██████╗ ███████╗"
ui_print "  ██║██╔═══██╗██╔════╝"
ui_print "  ██║██║   ██║███████╗"
ui_print "  ██║██║   ██║╚════██║"
ui_print "  ██║╚██████╔╝███████║"
ui_print "  ╚═╝ ╚═════╝ ╚══════╝"
ui_print " "
ui_print "  Device: $(getprop ro.product.model)"
ui_print "  Flashing..."
ui_print " "

if [ -n "$ZIPFILE" ] && [ -f "$ZIPFILE" ]; then
    unzip -o "$ZIPFILE" 'system/*' -d "$MODPATH" >/dev/null 2>&1
fi

FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
NYF="$FD/NewYork-Bold.ttf"
RF="$FD/SF-Pro-Rounded.otf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
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

# 1. Deploy Apple SF Pro Heavy over System UI & Latin Fonts
for pdir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts; do
    [ -d "$pdir" ] || continue
    for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
        case "$fname" in
            *Thai*|*thai*|*SC*|*sc*|*TC*|*tc*|*CJK*|*cjk*|*JP*|*jp*|*KR*|*kr*|*Gurmukhi*|*Devanagari*|*Bengali*|*Gujarati*|*Tamil*|*Telugu*|*Kannada*|*Malayalam*|*Sinhala*|*Khmer*|*Lao*|*Myanmar*|*Ethiopic*|*Hebrew*|*Armenian*|*Georgian*|*Tibetan*|*Arabic*|*Urdu*)
                continue
                ;;
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

# 2. Deploy Apple New York Serif
for f in NotoSerif-Regular.ttf NotoSerif-Bold.ttf NotoSerif-Italic.ttf NotoSerif-BoldItalic.ttf; do
    place "$NYF" "$f"
done

# 3. Deploy Authentic Nastaliq Urdu over Arabic & Urdu Fallbacks
for f in NotoNastaliqUrdu-Regular.ttf NotoNastaliqUrdu-Bold.ttf NotoNastaliqUrdu.ttf \
         NotoNastaliqUrdu-VF.ttf NotoNastaliqUrdu[wght].ttf \
         NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf \
         NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf \
         NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf \
         NotoSansArabicUI-Regular.ttf NotoSansArabicUI-Bold.ttf \
         NotoKufiArabic-Regular.ttf NotoKufiArabic-Bold.ttf; do
    place "$UF" "$f"
done

# 4. Deploy All World Scripts & Auto-generate UI / Serif Fallbacks
for script in Devanagari Gurmukhi Bengali Gujarati Tamil Telugu Kannada Malayalam Sinhala Thai Khmer Lao Myanmar Ethiopic Hebrew Armenian Georgian; do
    src="$FD/NotoSans${script}-VF.ttf"
    [ -f "$src" ] || continue
    place "$src" "NotoSans${script}-VF.ttf"
    place "$src" "NotoSans${script}UI-VF.ttf"
    place "$src" "NotoSans${script}-Bold.ttf"
    place "$src" "NotoSans${script}-Regular.ttf"
    place "$src" "NotoSans${script}UI-Bold.ttf"
    place "$src" "NotoSans${script}UI-Regular.ttf"
    place "$src" "NotoSerif${script}-VF.ttf"
    place "$src" "NotoSerif${script}-Bold.ttf"
    place "$src" "NotoSerif${script}-Regular.ttf"
done

[ -f "$FD/NotoSerifTibetan-VF.ttf" ] && place "$FD/NotoSerifTibetan-VF.ttf" "NotoSerifTibetan-VF.ttf"

# 5. Deploy Apple Color Emoji
for f in SamsungColorEmoji.ttf LGNotoColorEmoji.ttf HTC_ColorEmoji.ttf \
         AndroidEmoji-htc.ttf ColorUniEmoji.ttf DcmColorEmoji.ttf \
         CombinedColorEmoji.ttf NotoColorEmojiLegacy.ttf NotoColorEmoji-Flags.ttf NotoColorEmojiFlags.ttf; do
    if [ -f "/system/fonts/$f" ] || [ -f "/product/fonts/$f" ] || [ -f "/system_ext/fonts/$f" ]; then
        place "$EF" "$f"
    fi
done

# 6. Purge Caches & Font Locks
rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

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

ui_print "  Done. Reboot device."
ui_print " "

#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Professional Installer
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
BOF="$FD/SF-Pro-Bold.otf"
VF="$FD/SF-Pro-Variable.ttf"
RF="$FD/SF-Pro-Rounded.otf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
HF="$FD/SF-Hebrew.ttf"
AMF="$FD/SF-Armenian.ttf"
GF="$FD/SF-Georgian.ttf"
EF="$FD/NotoColorEmoji.ttf"

# Create ALL overlay partition directories (both root-level and nested system-level)
mkdir -p "$MODPATH/system/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/product/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/system_ext/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/vendor/fonts" 2>/dev/null
mkdir -p "$MODPATH/product/fonts" 2>/dev/null
mkdir -p "$MODPATH/system_ext/fonts" 2>/dev/null
mkdir -p "$MODPATH/vendor/fonts" 2>/dev/null

# Universal placement function: writes font to ALL possible partition mount locations
place() {
    local src="$1" name="$2"
    cp -f "$src" "$MODPATH/system/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/product/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/system_ext/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system/vendor/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/product/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/system_ext/fonts/$name" 2>/dev/null
    cp -f "$src" "$MODPATH/vendor/fonts/$name" 2>/dev/null
}

ui_print "  [+] Step 1/5: Deploying Rich Apple Bold Variable Fonts (TOS_VF, Roboto VF, etc.)..."
for f in \
    TOS_VF.ttf TOS_VF_SC.ttf TOS_VF_TC.ttf TOS_VF_Thai.ttf TOS_VF_Myanmar.ttf TOS_VF.otf \
    Roboto-VariableFont_wdth,wght.ttf Roboto-Italic-VariableFont_wdth,wght.ttf \
    RobotoFlex-Regular.ttf \
    GoogleSansFlex-Regular.ttf \
    MiSansVF.ttf MiSans_VF.ttf \
    OPlusSans2.0-VF.ttf OPlusSans3.0-VF.ttf
do
    place "$VF" "$f"
done
ui_print "      ✔ Variable fonts deployed across all partitions"
ui_print " "

ui_print "  [+] Step 2/5: Deploying Rich Apple Bold over TranSans & All UI Fonts..."
# Every conceivable TranSans, TransSans, Infinix, Tecno, Itel, Roboto, Google, Samsung target
for f in \
    TranSans.ttf TranSans-Regular.ttf TranSans-Bold.ttf TranSans-Medium.ttf \
    TranSans-Italic.ttf TranSans-BoldItalic.ttf TranSans-Light.ttf TranSans-LightItalic.ttf \
    TranSans-Thin.ttf TranSans-ThinItalic.ttf TranSans-Black.ttf TranSans-BlackItalic.ttf \
    TranSans_Regular.ttf TranSans_Bold.ttf TranSans_Medium.ttf TranSans_Italic.ttf \
    TranSans_BoldItalic.ttf TranSans_Light.ttf TranSans_Thin.ttf TranSans_Black.ttf \
    TranSans_SC.ttf TranSans_TC.ttf TranSans_Thai.ttf TranSans_Myanmar.ttf \
    TranSansShell.ttf TranSansSCShell.ttf \
    TranSans.otf TranSans-Regular.otf TranSans-Bold.otf TranSans-Medium.otf \
    TransSans.ttf TransSans-Regular.ttf TransSans-Bold.ttf TransSans-Medium.ttf TransSans-Italic.ttf \
    TransSans_Regular.ttf TransSans_Bold.ttf TransSans_Medium.ttf TransSans_Italic.ttf \
    TransSans_SC.ttf TransSans_TC.ttf TransSans_Thai.ttf TransSans_Myanmar.ttf \
    TOS.ttf TOS-Regular.ttf TOS-Bold.ttf \
    InfinixSans.ttf InfinixSans-Regular.ttf InfinixSans-Bold.ttf InfinixSans-Medium.ttf \
    TecnoSans.ttf TecnoSans-Regular.ttf TecnoSans-Bold.ttf TecnoSans-Medium.ttf \
    ItelSans.ttf ItelSans-Regular.ttf ItelSans-Bold.ttf \
    Roboto-Regular.ttf Roboto-Bold.ttf Roboto-Medium.ttf Roboto-MediumItalic.ttf \
    Roboto-Italic.ttf Roboto-BoldItalic.ttf Roboto-Black.ttf Roboto-BlackItalic.ttf \
    Roboto-Light.ttf Roboto-LightItalic.ttf Roboto-Thin.ttf Roboto-ThinItalic.ttf \
    RobotoStatic-Regular.ttf RobotoStatic-Bold.ttf RobotoStatic-Medium.ttf \
    RobotoStatic-Italic.ttf RobotoStatic-BoldItalic.ttf RobotoStatic-Light.ttf \
    RobotoStatic-Thin.ttf RobotoStatic-Black.ttf \
    RobotoCondensed-Regular.ttf RobotoCondensed-Bold.ttf RobotoCondensed-Medium.ttf \
    RobotoCondensed-MediumItalic.ttf RobotoCondensed-Italic.ttf RobotoCondensed-BoldItalic.ttf \
    RobotoCondensed-Light.ttf RobotoCondensed-LightItalic.ttf \
    GoogleSans-Regular.ttf GoogleSans-Medium.ttf GoogleSans-Bold.ttf \
    GoogleSans-Italic.ttf GoogleSans-BoldItalic.ttf GoogleSans-MediumItalic.ttf \
    GoogleSansText-Regular.ttf GoogleSansText-Medium.ttf GoogleSansText-Bold.ttf \
    GoogleSansText-Italic.ttf GoogleSansText-BoldItalic.ttf GoogleSansText-MediumItalic.ttf \
    GS-Regular.ttf GS-Medium.ttf GS-Bold.ttf GS-Italic.ttf \
    SECRobotoLight-Regular.ttf SECRobotoLight-Bold.ttf SECRoboto-Regular.ttf SECRoboto-Bold.ttf \
    SamsungOne-400.ttf SamsungOne-500.ttf SamsungOne-600.ttf SamsungOne-700.ttf \
    SamsungSans-Regular.ttf SamsungSans-Bold.ttf \
    MiSans-Regular.ttf MiSans-Medium.ttf MiSans-Demibold.ttf MiSans-Bold.ttf \
    MiSans-Heavy.ttf MiSans-Light.ttf MiSans-Thin.ttf MiSans-Normal.ttf \
    MiSans-Semibold.ttf MiSansLatin-Regular.ttf MiSansLatin-Bold.ttf \
    Miui-Regular.ttf Miui-Bold.ttf \
    OPlusSans-Regular.ttf OPlusSans-Medium.ttf OPlusSans-Bold.ttf OPlusSans-Light.ttf \
    SysSans-En-Regular.ttf OnePlusSans-Regular.ttf OnePlusSans-Bold.ttf \
    DroidSans.ttf DroidSans-Bold.ttf \
    NotoSans-Regular.ttf NotoSans-Bold.ttf NotoSans-Medium.ttf NotoSans-Italic.ttf \
    NotoSans-BoldItalic.ttf NotoSans-Light.ttf NotoSans-Thin.ttf \
    NotoSerif-Regular.ttf NotoSerif-Bold.ttf \
    CutiveMono.ttf ComingSoon.ttf DancingScript-Regular.ttf DancingScript-Bold.ttf \
    CarroisGothicSC-Regular.ttf
do
    case "$f" in
        *.otf) place "$BOF" "$f" ;;
        *)     place "$BTF" "$f" ;;
    esac
done
ui_print "      ✔ TranSans & UI fonts deployed across all partitions"
ui_print " "

ui_print "  [+] Step 3/5: Deploying Noto Nastaliq Urdu Bold & Multilingual Fonts..."
# All Urdu & Arabic script fallback files -> Noto Nastaliq Urdu Bold
for f in \
    NotoNastaliqUrdu-Regular.ttf NotoNastaliqUrdu-Bold.ttf NotoNastaliqUrdu.ttf \
    NotoNastaliqUrdu-VF.ttf NotoNastaliqUrdu[wght].ttf \
    NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf \
    NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf \
    NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf NotoSansArabic-Medium.ttf \
    NotoSansArabicUI-Regular.ttf NotoSansArabicUI-Bold.ttf NotoSansArabicUI-Medium.ttf \
    NotoKufiArabic-Regular.ttf NotoKufiArabic-Bold.ttf
do
    place "$UF" "$f"
done

# Hebrew, Armenian, Georgian, Clocks
for f in NotoSansHebrew-Regular.ttf NotoSansHebrew-Bold.ttf NotoSansHebrew-Medium.ttf; do place "$HF" "$f"; done
for f in NotoSansArmenian-Regular.ttf NotoSansArmenian-Bold.ttf NotoSansArmenian-Medium.ttf; do place "$AMF" "$f"; done
for f in NotoSansGeorgian-Regular.ttf NotoSansGeorgian-Bold.ttf NotoSansGeorgian-Medium.ttf; do place "$GF" "$f"; done
for f in AndroidClock.ttf GoogleSansClock-Regular.ttf; do place "$RF" "$f"; done

ui_print "      ✔ Noto Nastaliq Urdu Bold and Multilingual scripts deployed"
ui_print " "

ui_print "  [+] Step 4/5: Scanning device partitions for unlisted OEM & Theme fonts..."
SCAN_COUNT=0
for pdir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts /system/product/fonts /system/system_ext/fonts; do
    [ -d "$pdir" ] || continue
    for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
        [ -f "$MODPATH/system/fonts/$fname" ] && continue
        case "$fname" in
            *Emoji*|*emoji*|*Symbol*|*symbol*|*Math*|*math*|*Mono*) continue ;;
            *Clock*|*clock*)                     place "$RF"  "$fname" ;;
            *Nastaliq*|*nastaliq*|*Urdu*|*urdu*|*Arabic*|*arabic*|*Naskh*|*naskh*|*Kufi*|*kufi*)
                                                  place "$UF"  "$fname" ;;
            *Hebrew*|*hebrew*)                    place "$HF"  "$fname" ;;
            *Armenian*|*armenian*)                place "$AMF" "$fname" ;;
            *Georgian*|*georgian*)                place "$GF"  "$fname" ;;
            TOS_VF*|*Variable*|*VF*|*Flex*)       place "$VF"  "$fname" ;;
            TranSans*|TransSans*|Infinix*|Tecno*|Itel*) place "$BTF" "$fname" ;;
            *.otf)                                place "$BOF" "$fname" ;;
            *)                                    place "$BTF" "$fname" ;;
        esac
        SCAN_COUNT=$((SCAN_COUNT + 1))
    done
done
ui_print "      ✔ Replaced $SCAN_COUNT additional OEM & Theme fonts"
ui_print " "

ui_print "  [+] Step 5/5: Deploying iOS 26.4 Emoji & Purging System/Theme Caches..."
for f in SamsungColorEmoji.ttf LGNotoColorEmoji.ttf HTC_ColorEmoji.ttf \
         AndroidEmoji-htc.ttf ColorUniEmoji.ttf DcmColorEmoji.ttf \
         CombinedColorEmoji.ttf NotoColorEmojiLegacy.ttf NotoColorEmoji-Flags.ttf; do
    if [ -f "/system/fonts/$f" ] || [ -f "/product/fonts/$f" ] || [ -f "/system_ext/fonts/$f" ]; then
        place "$EF" "$f"
    fi
done
for xml in /system/etc/fonts.xml /product/etc/fonts.xml /system_ext/etc/fonts.xml; do
    [ -f "$xml" ] || continue
    for f in $(sed -ne '/<family lang="und-Zsye".*>/,/<\/family>/{s/.*<font[^>]*>\([^<]*\)<\/font>.*/\1/p;}' "$xml" 2>/dev/null); do
        [ "$f" = "NotoColorEmoji.ttf" ] && continue
        [ -z "$f" ] && continue
        place "$EF" "$f"
    done
done

# Purge Android & Transsion Theme font caches
rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/system/theme/* 2>/dev/null
rm -rf /data/system/users/*/theme/* 2>/dev/null
rm -rf /data/resource-cache/* 2>/dev/null
rm -rf /data/data/com.shashank.transsion* 2>/dev/null
rm -rf /data/data/com.transsion.theme* 2>/dev/null
rm -rf /data/data/com.transsion.magicshow* 2>/dev/null

for pkg in com.facebook.orca com.facebook.katana com.facebook.lite \
           com.facebook.mlite com.google.android.inputmethod.latin \
           com.transsion.theme com.transsion.magicshow com.android.settings; do
    if pm list packages 2>/dev/null | grep -q "$pkg"; then
        for sub in /cache /code_cache /app_webview /files/GCache; do
            rm -rf "/data/data/${pkg}${sub}" 2>/dev/null
        done
        am force-stop "$pkg" 2>/dev/null
    fi
done
rm -rf /data/data/com.google.android.gms/files/fonts 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts 2>/dev/null

# Permissions & SELinux Contexts
set_perm_recursive "$MODPATH" 0 0 0755 0644
for s in post-fs-data.sh service.sh action.sh; do
    [ -f "$MODPATH/$s" ] && set_perm "$MODPATH/$s" 0 0 0755
done
chcon -R u:object_r:system_file:s0 "$MODPATH/system" 2>/dev/null
chcon -R u:object_r:system_file:s0 "$MODPATH/product" 2>/dev/null
chcon -R u:object_r:system_file:s0 "$MODPATH/system_ext" 2>/dev/null
chcon -R u:object_r:system_file:s0 "$MODPATH/vendor" 2>/dev/null
ui_print "      ✔ Permissions & SELinux contexts applied"
ui_print " "
ui_print "  ─────────────────────────────────────────"
ui_print "  ✔ Installation Complete!                 "
ui_print "  ✔ Reboot to apply changes.               "
ui_print "  ─────────────────────────────────────────"
ui_print " "

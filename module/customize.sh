#!/system/bin/sh
##########################################################################################
# iOS Bold Font & iOS 26.4 Emoji — Installer
# Author: sheikhmehraan
##########################################################################################

SKIPMOUNT=false

ui_print " "
ui_print "  ███████╗███████╗    ██╗ ██████╗ ███████╗"
ui_print "  ██╔════╝██╔════╝    ██║██╔═══██╗██╔════╝"
ui_print "  ███████╗█████╗      ██║██║   ██║███████╗"
ui_print "  ╚════██║██╔══╝      ██║██║   ██║╚════██║"
ui_print "  ███████║██║         ██║╚██████╔╝███████║"
ui_print "  ╚══════╝╚═╝         ╚═╝ ╚═════╝ ╚══════╝"
ui_print "  ─────────────────────────────────────────"
ui_print "   iOS Bold Font & iOS 26.4 Emoji Ultra   "
ui_print "  Developer : sheikhmehraan                "
ui_print "  Version   : v2.0 • Ultra Edition         "
ui_print "  ─────────────────────────────────────────"
ui_print " "

ui_print "  [i] Device: $(getprop ro.product.brand) $(getprop ro.product.model)"
ui_print "  [i] Android $(getprop ro.build.version.release) (SDK $(getprop ro.build.version.sdk))"
ui_print " "

# Source font paths (shipped inside the ZIP under system/fonts/)
FD="$MODPATH/system/fonts"
VF="$FD/SF-Pro-Variable.ttf"   # variable, wght axis locked to 700
BF="$FD/SF-Pro-Bold.otf"       # static Apple SF Pro Display Bold
RF="$FD/SF-Pro-Rounded.otf"    # static Apple SF Pro Rounded Bold
AF="$FD/SF-Arabic.ttf"         # variable, wght 700 — Urdu/Arabic/Persian
HF="$FD/SF-Hebrew.ttf"
AMF="$FD/SF-Armenian.ttf"
GF="$FD/SF-Georgian.ttf"
EF="$FD/NotoColorEmoji.ttf"

# Helper: copy a font to the overlay for a given target filename.
# Magisk/KSU/APatch overlay paths MUST start with system/ — standalone
# /product, /vendor, /system_ext are symlinks INTO /system on modern Android.
place() {
    local src="$1" name="$2"
    cp -f "$src" "$MODPATH/system/fonts/$name"                2>/dev/null
    cp -f "$src" "$MODPATH/system/product/fonts/$name"        2>/dev/null
    cp -f "$src" "$MODPATH/system/system_ext/fonts/$name"     2>/dev/null
    cp -f "$src" "$MODPATH/system/vendor/fonts/$name"         2>/dev/null
}

ui_print "  [1/5] Replacing Variable Fonts (Roboto VF, TOS_VF, GoogleSansFlex, MiSans VF)..."
for f in \
    Roboto-VariableFont_wdth,wght.ttf  Roboto-Italic-VariableFont_wdth,wght.ttf \
    RobotoFlex-Regular.ttf \
    TOS_VF.ttf  TOS_VF_SC.ttf \
    GoogleSansFlex-Regular.ttf \
    MiSansVF.ttf  MiSans_VF.ttf \
    OPlusSans2.0-VF.ttf  OPlusSans3.0-VF.ttf
do place "$VF" "$f"; done
ui_print "      ✔ Variable font targets replaced"
ui_print " "

ui_print "  [2/5] Replacing Static UI Fonts (Roboto, TranSans, Google Sans, Samsung, Xiaomi, OnePlus)..."
for f in \
    Roboto-Regular.ttf Roboto-Bold.ttf Roboto-Medium.ttf Roboto-MediumItalic.ttf \
    Roboto-Italic.ttf Roboto-BoldItalic.ttf Roboto-Black.ttf Roboto-BlackItalic.ttf \
    Roboto-Light.ttf Roboto-LightItalic.ttf Roboto-Thin.ttf Roboto-ThinItalic.ttf \
    RobotoStatic-Regular.ttf RobotoStatic-Bold.ttf RobotoStatic-Medium.ttf \
    RobotoStatic-Italic.ttf RobotoStatic-BoldItalic.ttf RobotoStatic-Light.ttf \
    RobotoStatic-Thin.ttf RobotoStatic-Black.ttf \
    RobotoCondensed-Regular.ttf RobotoCondensed-Bold.ttf RobotoCondensed-Medium.ttf \
    RobotoCondensed-MediumItalic.ttf RobotoCondensed-Italic.ttf RobotoCondensed-BoldItalic.ttf \
    RobotoCondensed-Light.ttf RobotoCondensed-LightItalic.ttf \
    TranSansShell.ttf TranSansSCShell.ttf TranSans_Regular.ttf TranSans_Medium.ttf \
    TranSans_Bold.ttf TranSans_Italic.ttf TranSans_SC.ttf TranSans_TC.ttf \
    TransSans-Regular.ttf TransSans-Medium.ttf TransSans-Bold.ttf TransSans_Italic.ttf \
    TransSans_SC.ttf TransSans_Thai.ttf \
    InfinixSans-Regular.ttf InfinixSans-Bold.ttf InfinixSans-Medium.ttf \
    TecnoSans-Regular.ttf TecnoSans-Bold.ttf TecnoSans-Medium.ttf \
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
do place "$BF" "$f"; done
ui_print "      ✔ Static UI font targets replaced"
ui_print " "

ui_print "  [3/5] Replacing Multilingual Script Fonts (Urdu, Arabic, Hebrew, Armenian, Georgian)..."
# Arabic / Urdu / Persian / Pashto
for f in \
    NotoNastaliqUrdu-Regular.ttf NotoNastaliqUrdu-Bold.ttf \
    NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf NotoSansArabic-Medium.ttf \
    NotoSansArabicUI-Regular.ttf NotoSansArabicUI-Bold.ttf NotoSansArabicUI-Medium.ttf \
    NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf \
    NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf \
    NotoKufiArabic-Regular.ttf NotoKufiArabic-Bold.ttf
do place "$AF" "$f"; done
# Hebrew
for f in \
    NotoSansHebrew-Regular.ttf NotoSansHebrew-Bold.ttf NotoSansHebrew-Medium.ttf
do place "$HF" "$f"; done
# Armenian
for f in \
    NotoSansArmenian-Regular.ttf NotoSansArmenian-Bold.ttf NotoSansArmenian-Medium.ttf
do place "$AMF" "$f"; done
# Georgian
for f in \
    NotoSansGeorgian-Regular.ttf NotoSansGeorgian-Bold.ttf NotoSansGeorgian-Medium.ttf
do place "$GF" "$f"; done
# Clocks
for f in AndroidClock.ttf GoogleSansClock-Regular.ttf
do place "$RF" "$f"; done
ui_print "      ✔ Multilingual script fonts replaced"
ui_print " "

ui_print "  [4/5] Scanning device partitions for unlisted OEM fonts..."
SCAN_COUNT=0
for pdir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts; do
    [ -d "$pdir" ] || continue
    for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
        # Skip if we already placed this file
        [ -f "$MODPATH/system/fonts/$fname" ] && continue
        case "$fname" in
            *Emoji*|*emoji*|*Symbol*|*symbol*|*Math*|*math*|*Mono*) continue ;;
            *Clock*|*clock*)                     place "$RF"  "$fname" ;;
            *Arabic*|*arabic*|*Urdu*|*urdu*|*Nastaliq*|*nastaliq*|*Naskh*|*naskh*|*Kufi*|*kufi*)
                                                  place "$AF"  "$fname" ;;
            *Hebrew*|*hebrew*)                    place "$HF"  "$fname" ;;
            *Armenian*|*armenian*)                place "$AMF" "$fname" ;;
            *Georgian*|*georgian*)                place "$GF"  "$fname" ;;
            TOS_VF*|*Variable*|*VF*|*Flex*)       place "$VF"  "$fname" ;;
            *)                                    place "$BF"  "$fname" ;;
        esac
        SCAN_COUNT=$((SCAN_COUNT + 1))
    done
done
ui_print "      ✔ Scanned & replaced $SCAN_COUNT additional OEM fonts"
ui_print " "

ui_print "  [5/5] Deploying iOS 26.4 Emoji, purging caches, setting permissions..."
# OEM emoji variants
for f in SamsungColorEmoji.ttf LGNotoColorEmoji.ttf HTC_ColorEmoji.ttf \
         AndroidEmoji-htc.ttf ColorUniEmoji.ttf DcmColorEmoji.ttf \
         CombinedColorEmoji.ttf NotoColorEmojiLegacy.ttf NotoColorEmoji-Flags.ttf; do
    if [ -f "/system/fonts/$f" ] || [ -f "/product/fonts/$f" ] || [ -f "/system_ext/fonts/$f" ]; then
        place "$EF" "$f"
        ui_print "      ✔ Emoji: $f"
    fi
done

# Parse fonts.xml for any extra emoji family font
for xml in /system/etc/fonts.xml /product/etc/fonts.xml /system_ext/etc/fonts.xml; do
    [ -f "$xml" ] || continue
    for f in $(sed -ne '/<family lang="und-Zsye".*>/,/<\/family>/{s/.*<font[^>]*>\([^<]*\)<\/font>.*/\1/p;}' "$xml" 2>/dev/null); do
        [ "$f" = "NotoColorEmoji.ttf" ] && continue
        [ -z "$f" ] && continue
        place "$EF" "$f"
    done
done

# Purge caches
rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
for pkg in com.facebook.orca com.facebook.katana com.facebook.lite \
           com.facebook.mlite com.google.android.inputmethod.latin; do
    if pm list packages 2>/dev/null | grep -q "$pkg"; then
        for sub in /cache /code_cache /app_webview /files/GCache; do
            rm -rf "/data/data/${pkg}${sub}" 2>/dev/null
        done
        am force-stop "$pkg" 2>/dev/null
    fi
done
rm -rf /data/data/com.google.android.gms/files/fonts 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts 2>/dev/null
ui_print "      ✔ Caches purged"

# Permissions & SELinux
set_perm_recursive "$MODPATH" 0 0 0755 0644
for s in post-fs-data.sh service.sh action.sh; do
    [ -f "$MODPATH/$s" ] && set_perm "$MODPATH/$s" 0 0 0755
done
chcon -R u:object_r:system_file:s0 "$MODPATH/system" 2>/dev/null
ui_print "      ✔ Permissions & SELinux OK"
ui_print " "
ui_print "  ─────────────────────────────────────────"
ui_print "  ✔ Done — reboot to apply.                "
ui_print "  ─────────────────────────────────────────"
ui_print " "

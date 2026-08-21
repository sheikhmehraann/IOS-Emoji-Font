#!/system/bin/sh
##########################################################################################
#
#  iOS Bold Font & iOS 26.4 Emoji - Professional Installer
# Author: sheikhmehraan
#
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

DEVICE_MODEL=$(getprop ro.product.model)
DEVICE_BRAND=$(getprop ro.product.brand)
ANDROID_VER=$(getprop ro.build.version.release)
ANDROID_SDK=$(getprop ro.build.version.sdk)

ui_print "  [i] Device Information:"
ui_print "      • Model   : $DEVICE_MODEL"
ui_print "      • Brand   : $DEVICE_BRAND"
ui_print "      • Android : $ANDROID_VER (SDK $ANDROID_SDK)"
ui_print " "

FONT_DIR="$MODPATH/system/fonts"
VAR_FONT="$FONT_DIR/SF-Pro-Variable.ttf"
BOLD_FONT="$FONT_DIR/SF-Pro-Bold.otf"
ROUND_FONT="$FONT_DIR/SF-Pro-Rounded.otf"
ARABIC_FONT="$FONT_DIR/SF-Arabic.ttf"
HEBREW_FONT="$FONT_DIR/SF-Hebrew.ttf"
ARMENIAN_FONT="$FONT_DIR/SF-Armenian.ttf"
GEORGIAN_FONT="$FONT_DIR/SF-Georgian.ttf"
FONT_EMOJI="NotoColorEmoji.ttf"

package_installed() {
    local package="$1"
    if pm list packages 2>/dev/null | grep -q "$package"; then
        return 0
    else
        return 1
    fi
}

display_name() {
    local package_name="$1"
    case "$package_name" in
        "com.facebook.orca") echo "Messenger" ;;
        "com.facebook.katana") echo "Facebook" ;;
        "com.facebook.lite") echo "Facebook Lite" ;;
        "com.facebook.mlite") echo "Messenger Lite" ;;
        "com.google.android.inputmethod.latin") echo "Gboard" ;;
        *) echo "$package_name" ;;
    esac
}

clear_cache() {
    local app_name="$1"
    local app_display_name=$(display_name "$app_name")
	
    if ! package_installed "$app_name"; then
        return 0
    fi
	
    ui_print "      ✔ Purging cache: $app_display_name"
	
    for subpath in /cache /code_cache /app_webview /files/GCache; do
        target_dir="/data/data/${app_name}${subpath}"
        if [ -d "$target_dir" ]; then
            rm -rf "$target_dir" 2>/dev/null
        fi
    done

    am force-stop "$app_name" 2>/dev/null
}

if [ -n "$ZIPFILE" ] && [ -f "$ZIPFILE" ]; then
    unzip -o "$ZIPFILE" 'system/*' -d "$MODPATH" >/dev/null 2>&1
fi

# Create target directories for ALL partition mount types (root & nested)
mkdir -p "$MODPATH/system/fonts" 2>/dev/null
mkdir -p "$MODPATH/product/fonts" 2>/dev/null
mkdir -p "$MODPATH/system_ext/fonts" 2>/dev/null
mkdir -p "$MODPATH/vendor/fonts" 2>/dev/null

mkdir -p "$MODPATH/system/product/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/system_ext/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/vendor/fonts" 2>/dev/null

ui_print "  [+] Step 1/4: Injecting Apple SF Pro Bold & Transsion OS Typography..."

# 1. Variable Font Targets (Transsion TOS_VF, AOSP Roboto-VariableFont, GoogleSansFlex)
var_targets="
Roboto-VariableFont_wdth,wght.ttf Roboto-Italic-VariableFont_wdth,wght.ttf RobotoFlex-Regular.ttf
TOS_VF.ttf TOS_VF_SC.ttf
GoogleSansFlex-Regular.ttf
MiSansVF.ttf MiSans_VF.ttf
OPlusSans2.0-VF.ttf OPlusSans3.0-VF.ttf
"
for f in $var_targets; do
    cp -f "$VAR_FONT" "$MODPATH/system/fonts/$f" 2>/dev/null
    cp -f "$VAR_FONT" "$MODPATH/product/fonts/$f" 2>/dev/null
    cp -f "$VAR_FONT" "$MODPATH/system_ext/fonts/$f" 2>/dev/null
    cp -f "$VAR_FONT" "$MODPATH/system/product/fonts/$f" 2>/dev/null
    cp -f "$VAR_FONT" "$MODPATH/system/system_ext/fonts/$f" 2>/dev/null
done

# 2. Clock & Lockscreen Font Targets (Apple Rounded Bold)
clock_targets="
AndroidClock.ttf GoogleSansClock-Regular.ttf
"
for f in $clock_targets; do
    cp -f "$ROUND_FONT" "$MODPATH/system/fonts/$f" 2>/dev/null
    cp -f "$ROUND_FONT" "$MODPATH/product/fonts/$f" 2>/dev/null
    cp -f "$ROUND_FONT" "$MODPATH/system_ext/fonts/$f" 2>/dev/null
    cp -f "$ROUND_FONT" "$MODPATH/system/product/fonts/$f" 2>/dev/null
done

# 3. Multilingual Scripts: Bold Urdu & Arabic (SF Arabic Bold), Hebrew, Armenian, Georgian
arabic_targets="
NotoNastaliqUrdu-Regular.ttf NotoNastaliqUrdu-Bold.ttf
NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf NotoSansArabic-Medium.ttf
NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf
"
for f in $arabic_targets; do
    cp -f "$ARABIC_FONT" "$MODPATH/system/fonts/$f" 2>/dev/null
    cp -f "$ARABIC_FONT" "$MODPATH/product/fonts/$f" 2>/dev/null
    cp -f "$ARABIC_FONT" "$MODPATH/system_ext/fonts/$f" 2>/dev/null
    cp -f "$ARABIC_FONT" "$MODPATH/system/product/fonts/$f" 2>/dev/null
done

hebrew_targets="NotoSansHebrew-Regular.ttf NotoSansHebrew-Bold.ttf NotoSansHebrew-Medium.ttf"
for f in $hebrew_targets; do
    cp -f "$HEBREW_FONT" "$MODPATH/system/fonts/$f" 2>/dev/null
    cp -f "$HEBREW_FONT" "$MODPATH/product/fonts/$f" 2>/dev/null
    cp -f "$HEBREW_FONT" "$MODPATH/system_ext/fonts/$f" 2>/dev/null
    cp -f "$HEBREW_FONT" "$MODPATH/system/product/fonts/$f" 2>/dev/null
done

armenian_targets="NotoSansArmenian-Regular.ttf NotoSansArmenian-Bold.ttf NotoSansArmenian-Medium.ttf"
for f in $armenian_targets; do
    cp -f "$ARMENIAN_FONT" "$MODPATH/system/fonts/$f" 2>/dev/null
    cp -f "$ARMENIAN_FONT" "$MODPATH/product/fonts/$f" 2>/dev/null
    cp -f "$ARMENIAN_FONT" "$MODPATH/system_ext/fonts/$f" 2>/dev/null
done

georgian_targets="NotoSansGeorgian-Regular.ttf NotoSansGeorgian-Bold.ttf NotoSansGeorgian-Medium.ttf"
for f in $georgian_targets; do
    cp -f "$GEORGIAN_FONT" "$MODPATH/system/fonts/$f" 2>/dev/null
    cp -f "$GEORGIAN_FONT" "$MODPATH/product/fonts/$f" 2>/dev/null
    cp -f "$GEORGIAN_FONT" "$MODPATH/system_ext/fonts/$f" 2>/dev/null
done

# 4. Transsion OS (TOS, HiOS, XOS) & Core UI Bold Font Targets
bold_targets="
TranSansShell.ttf TranSansSCShell.ttf TranSans_Regular.ttf TranSans_Medium.ttf TranSans_Bold.ttf TranSans_Italic.ttf TranSans_SC.ttf TranSans_TC.ttf
TransSans-Regular.ttf TransSans-Medium.ttf TransSans-Bold.ttf TransSans_Italic.ttf TransSans_SC.ttf TransSans_Thai.ttf
InfinixSans-Regular.ttf InfinixSans-Bold.ttf TecnoSans-Regular.ttf TecnoSans-Bold.ttf
Roboto-Regular.ttf Roboto-Bold.ttf Roboto-Medium.ttf Roboto-Italic.ttf Roboto-BoldItalic.ttf Roboto-Black.ttf Roboto-BlackItalic.ttf Roboto-Light.ttf Roboto-LightItalic.ttf Roboto-Thin.ttf Roboto-ThinItalic.ttf
RobotoStatic-Regular.ttf RobotoStatic-Bold.ttf RobotoStatic-Medium.ttf RobotoStatic-Italic.ttf RobotoStatic-BoldItalic.ttf RobotoStatic-Light.ttf RobotoStatic-Thin.ttf RobotoStatic-Black.ttf
RobotoCondensed-Regular.ttf RobotoCondensed-Bold.ttf RobotoCondensed-Italic.ttf RobotoCondensed-BoldItalic.ttf RobotoCondensed-Light.ttf RobotoCondensed-LightItalic.ttf RobotoCondensed-Medium.ttf RobotoCondensed-MediumItalic.ttf
GoogleSans-Regular.ttf GoogleSans-Medium.ttf GoogleSans-Bold.ttf GoogleSans-Italic.ttf GoogleSans-BoldItalic.ttf GoogleSans-MediumItalic.ttf
GoogleSansText-Regular.ttf GoogleSansText-Medium.ttf GoogleSansText-Bold.ttf GoogleSansText-Italic.ttf GoogleSansText-BoldItalic.ttf GoogleSansText-MediumItalic.ttf
GS-Regular.ttf GS-Medium.ttf GS-Bold.ttf GS-Italic.ttf
SECRobotoLight-Regular.ttf SECRobotoLight-Bold.ttf SECRoboto-Regular.ttf SECRoboto-Bold.ttf SamsungOne-400.ttf SamsungOne-500.ttf SamsungOne-600.ttf SamsungOne-700.ttf SamsungSans-Regular.ttf SamsungSans-Bold.ttf
MiSans-Regular.ttf MiSans-Medium.ttf MiSans-Demibold.ttf MiSans-Bold.ttf MiSans-Heavy.ttf MiSans-Light.ttf MiSans-Thin.ttf MiSans-Normal.ttf MiSans-Semibold.ttf MiSansLatin-Regular.ttf MiSansLatin-Bold.ttf Miui-Regular.ttf Miui-Bold.ttf
OPlusSans-Regular.ttf OPlusSans-Medium.ttf OPlusSans-Bold.ttf OPlusSans-Light.ttf SysSans-En-Regular.ttf OnePlusSans-Regular.ttf OnePlusSans-Bold.ttf
"
for f in $bold_targets; do
    cp -f "$BOLD_FONT" "$MODPATH/system/fonts/$f" 2>/dev/null
    cp -f "$BOLD_FONT" "$MODPATH/product/fonts/$f" 2>/dev/null
    cp -f "$BOLD_FONT" "$MODPATH/system_ext/fonts/$f" 2>/dev/null
    cp -f "$BOLD_FONT" "$MODPATH/vendor/fonts/$f" 2>/dev/null
    cp -f "$BOLD_FONT" "$MODPATH/system/product/fonts/$f" 2>/dev/null
    cp -f "$BOLD_FONT" "$MODPATH/system/system_ext/fonts/$f" 2>/dev/null
done

# 5. Dynamic Real-Time ROM Scanner: Scan device partitions for ANY active UI or script font
for pdir in /product/fonts /system_ext/fonts /system/fonts /vendor/fonts; do
    if [ -d "$pdir" ]; then
        sub="${pdir#/}"
        for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
            [ -f "$fpath" ] || continue
            fname=$(basename "$fpath")
            case "$fname" in
                *Emoji*|*emoji*) ;;
                *Clock*|*clock*)
                    cp -f "$ROUND_FONT" "$MODPATH/$sub/$fname" 2>/dev/null
                    cp -f "$ROUND_FONT" "$MODPATH/system/$sub/$fname" 2>/dev/null
                    ;;
                *Arabic*|*arabic*|*Urdu*|*urdu*|*Nastaliq*|*nastaliq*)
                    cp -f "$ARABIC_FONT" "$MODPATH/$sub/$fname" 2>/dev/null
                    cp -f "$ARABIC_FONT" "$MODPATH/system/$sub/$fname" 2>/dev/null
                    ;;
                *Hebrew*|*hebrew*)
                    cp -f "$HEBREW_FONT" "$MODPATH/$sub/$fname" 2>/dev/null
                    cp -f "$HEBREW_FONT" "$MODPATH/system/$sub/$fname" 2>/dev/null
                    ;;
                *Armenian*|*armenian*)
                    cp -f "$ARMENIAN_FONT" "$MODPATH/$sub/$fname" 2>/dev/null
                    cp -f "$ARMENIAN_FONT" "$MODPATH/system/$sub/$fname" 2>/dev/null
                    ;;
                *Georgian*|*georgian*)
                    cp -f "$GEORGIAN_FONT" "$MODPATH/$sub/$fname" 2>/dev/null
                    cp -f "$GEORGIAN_FONT" "$MODPATH/system/$sub/$fname" 2>/dev/null
                    ;;
                TOS_VF*|*Variable*|*VF*|*Flex*)
                    cp -f "$VAR_FONT" "$MODPATH/$sub/$fname" 2>/dev/null
                    cp -f "$VAR_FONT" "$MODPATH/system/$sub/$fname" 2>/dev/null
                    ;;
                *NotoSansDevanagari*|*NotoSansBengali*|*NotoSansTamil*|*NotoSansTelugu*|*NotoSansKannada*|*NotoSansMalayalam*|*NotoSansGurmukhi*|*NotoSansGujarati*|*NotoSansOriya*|*NotoSansSinhala*|*NotoSansMyanmar*|*NotoSansKhmer*|*NotoSansLao*|*NotoSansThai*|*NotoSansTibetan*|*NotoSansEthiopic*|*NotoSansCherokee*|*NotoSansCanadianAboriginal*|*NotoSansCJK*|*NotoSerifCJK*|*SourceHanSans*)
                    case "$fname" in
                        *Regular*|*Light*|*Thin*|*Medium*)
                            bold_src=$(echo "$fpath" | sed -e 's/Regular/Bold/g' -e 's/Light/Bold/g' -e 's/Thin/Bold/g' -e 's/Medium/Bold/g')
                            if [ -f "$bold_src" ] && [ "$bold_src" != "$fpath" ]; then
                                cp -f "$bold_src" "$MODPATH/$sub/$fname" 2>/dev/null
                                cp -f "$bold_src" "$MODPATH/system/$sub/$fname" 2>/dev/null
                            fi
                            ;;
                    esac
                    ;;
                *Symbol*|*symbol*|*Math*|*math*) ;;
                *)
                    cp -f "$BOLD_FONT" "$MODPATH/$sub/$fname" 2>/dev/null
                    cp -f "$BOLD_FONT" "$MODPATH/system/$sub/$fname" 2>/dev/null
                    ;;
            esac
        done
    fi
done

ui_print "      ✔ Multilingual, Transsion OS, and multi-partition coverage complete"
ui_print " "

ui_print "  [+] Step 2/4: Deploying iOS 26.4 Apple Color Emoji..."
variants="SamsungColorEmoji.ttf LGNotoColorEmoji.ttf HTC_ColorEmoji.ttf AndroidEmoji-htc.ttf ColorUniEmoji.ttf DcmColorEmoji.ttf CombinedColorEmoji.ttf NotoColorEmojiLegacy.ttf NotoColorEmoji-Flags.ttf"
for font in $variants; do
    if [ -f "/system/fonts/$font" ] || [ -f "/product/fonts/$font" ]; then
        cp -f "$FONT_DIR/$FONT_EMOJI" "$FONT_DIR/$font" 2>/dev/null
        cp -f "$FONT_DIR/$FONT_EMOJI" "$MODPATH/product/fonts/$font" 2>/dev/null
        ui_print "      ✔ Mapped OEM emoji: $font"
    fi
done

for xml in /system/etc/fonts.xml /product/etc/fonts.xml /system_ext/etc/fonts.xml; do
    if [ -f "$xml" ]; then
        fontfiles=$(sed -ne '/<family lang="und-Zsye".*>/,/<\/family>/ {s/.*<font weight="400" style="normal">\(.*\)<\/font>.*/\1/p;}' "$xml" 2>/dev/null)
        for f in $fontfiles; do
            if [ "$f" != "NotoColorEmoji.ttf" ] && [ -n "$f" ]; then
                cp -f "$FONT_DIR/$FONT_EMOJI" "$FONT_DIR/$f" 2>/dev/null
                cp -f "$FONT_DIR/$FONT_EMOJI" "$MODPATH/product/fonts/$f" 2>/dev/null
                ui_print "      ✔ Linked fonts.xml emoji: $f"
            fi
        done
    fi
done
ui_print " "

ui_print "  [+] Step 3/4: Purging Dynamic Caches & Blocking Overrides..."
clear_cache "com.facebook.orca"
clear_cache "com.facebook.katana"
clear_cache "com.facebook.lite"
clear_cache "com.facebook.mlite"
clear_cache "com.google.android.inputmethod.latin"
  
if [ -d "/data/fonts" ]; then
    rm -rf "/data/fonts"/* 2>/dev/null
    ui_print "      ✔ Cleared /data/fonts cache directory"
fi

if [ -f "/data/system/font_fallback.xml" ]; then
    rm -f "/data/system/font_fallback.xml" 2>/dev/null
    ui_print "      ✔ Reset dynamic font_fallback.xml"
fi
ui_print " "

ui_print "  [+] Step 4/4: Applying Permissions & SELinux Contexts..."
set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/post-fs-data.sh" 0 0 0755
set_perm "$MODPATH/service.sh" 0 0 0755
set_perm "$MODPATH/action.sh" 0 0 0755
chcon -R u:object_r:system_file:s0 "$MODPATH/system" 2>/dev/null
chcon -R u:object_r:system_file:s0 "$MODPATH/product" 2>/dev/null
chcon -R u:object_r:system_file:s0 "$MODPATH/system_ext" 2>/dev/null
ui_print "      ✔ Permissions (0755/0644) verified"
ui_print "      ✔ SELinux context applied"
ui_print " "

ui_print "  ─────────────────────────────────────────"
ui_print "  ✔ Installation Complete!                 "
ui_print "  ✔ Reboot your device to apply changes.   "
ui_print "  ─────────────────────────────────────────"
ui_print " "

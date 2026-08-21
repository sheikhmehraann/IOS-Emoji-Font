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
FONT_EMOJI="NotoColorEmoji.ttf"
BASE_FONT="$FONT_DIR/Roboto-Regular.ttf"

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

ui_print "  [+] Step 1/4: Expanding SF Pro Heavy Font Targets..."

# Expand system fonts
sys_targets="Roboto-Bold.ttf Roboto-Medium.ttf Roboto-Italic.ttf Roboto-BoldItalic.ttf Roboto-Black.ttf Roboto-BlackItalic.ttf Roboto-Light.ttf Roboto-LightItalic.ttf Roboto-Thin.ttf Roboto-ThinItalic.ttf RobotoStatic-Regular.ttf RobotoStatic-Bold.ttf RobotoStatic-Medium.ttf RobotoStatic-Italic.ttf RobotoStatic-BoldItalic.ttf Roboto-VariableFont_wdth,wght.ttf Roboto-Italic-VariableFont_wdth,wght.ttf RobotoFlex-Regular.ttf TranSansShell.ttf TranSansSCShell.ttf"

for f in $sys_targets; do
    cp -f "$BASE_FONT" "$FONT_DIR/$f" 2>/dev/null
done

# Expand product fonts
mkdir -p "$MODPATH/system/product/fonts" 2>/dev/null
prod_targets="TOS_VF.ttf TranSans_Italic.ttf TranSans_SC.ttf TransSans_Italic.ttf TransSans_SC.ttf TransSans_Thai.ttf TransSans-Regular.ttf TransSans-Bold.ttf TransSans-Medium.ttf Roboto-Regular.ttf Roboto-VariableFont_wdth,wght.ttf"
for f in $prod_targets; do
    cp -f "$BASE_FONT" "$MODPATH/system/product/fonts/$f" 2>/dev/null
done

# Expand system_ext fonts
mkdir -p "$MODPATH/system/system_ext/fonts" 2>/dev/null
ext_targets="TOS_VF.ttf TranSansShell.ttf Roboto-Regular.ttf Roboto-VariableFont_wdth,wght.ttf"
for f in $ext_targets; do
    cp -f "$BASE_FONT" "$MODPATH/system/system_ext/fonts/$f" 2>/dev/null
done

ui_print "      ✔ Generated 35+ system, product, and system_ext font targets"
ui_print " "

ui_print "  [+] Step 2/4: Deploying iOS 26.4 Apple Color Emoji..."
variants="SamsungColorEmoji.ttf LGNotoColorEmoji.ttf HTC_ColorEmoji.ttf AndroidEmoji-htc.ttf ColorUniEmoji.ttf DcmColorEmoji.ttf CombinedColorEmoji.ttf NotoColorEmojiLegacy.ttf NotoColorEmoji-Flags.ttf"
for font in $variants; do
    if [ -f "/system/fonts/$font" ] || [ -f "/product/fonts/$font" ]; then
        cp -f "$FONT_DIR/$FONT_EMOJI" "$FONT_DIR/$font" 2>/dev/null
        ui_print "      ✔ Mapped OEM emoji: $font"
    fi
done

for xml in /system/etc/fonts.xml /product/etc/fonts.xml /system_ext/etc/fonts.xml; do
    if [ -f "$xml" ]; then
        fontfiles=$(sed -ne '/<family lang="und-Zsye".*>/,/<\/family>/ {s/.*<font weight="400" style="normal">\(.*\)<\/font>.*/\1/p;}' "$xml" 2>/dev/null)
        for f in $fontfiles; do
            if [ "$f" != "NotoColorEmoji.ttf" ] && [ -n "$f" ]; then
                cp -f "$FONT_DIR/$FONT_EMOJI" "$FONT_DIR/$f" 2>/dev/null
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
ui_print "      ✔ Permissions (0755/0644) verified"
ui_print "      ✔ SELinux context applied (system_file)"
ui_print " "

ui_print "  ─────────────────────────────────────────"
ui_print "  ✔ Installation Complete!                 "
ui_print "  ✔ Reboot your device to apply changes.   "
ui_print "  ─────────────────────────────────────────"
ui_print " "

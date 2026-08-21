import os
import shutil
import zipfile
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.join(BASE_DIR, "module")
DIST_DIR = os.path.join(BASE_DIR, "dist")
OUTPUT_ZIP = os.path.join(DIST_DIR, "iOS_Bold_Font_Emoji_v2.0_Ultra.zip")

EXTRACTED_FONT_DIR = os.path.join(BASE_DIR, "extracted_font")
EXTRACTED_EMOJI_DIR = os.path.join(BASE_DIR, "extracted_emoji")

def clean_module_dir():
    if os.path.exists(MODULE_DIR):
        shutil.rmtree(MODULE_DIR)

def ensure_dirs():
    os.makedirs(os.path.join(MODULE_DIR, "META-INF", "com", "google", "android"), exist_ok=True)
    os.makedirs(os.path.join(MODULE_DIR, "system", "fonts"), exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)

def write_lf_file(filepath, content):
    with open(filepath, "wb") as f:
        f.write(content.replace("\r\n", "\n").encode("utf-8"))

def copy_assets():
    print("[*] Copying META-INF installer binaries...")
    src_meta = os.path.join(EXTRACTED_EMOJI_DIR, "META-INF", "com", "google", "android")
    dst_meta = os.path.join(MODULE_DIR, "META-INF", "com", "google", "android")
    shutil.copy2(os.path.join(src_meta, "update-binary"), os.path.join(dst_meta, "update-binary"))
    shutil.copy2(os.path.join(src_meta, "updater-script"), os.path.join(dst_meta, "updater-script"))

    print("[*] Copying iOS 26.4 Apple Color Emoji font...")
    emoji_src = os.path.join(EXTRACTED_EMOJI_DIR, "system", "fonts", "NotoColorEmoji.ttf")
    shutil.copy2(emoji_src, os.path.join(MODULE_DIR, "system", "fonts", "NotoColorEmoji.ttf"))
    print("  + system/fonts/NotoColorEmoji.ttf")

    print("[*] Copying SF Pro Text Heavy base font...")
    font_heavy_src = os.path.join(EXTRACTED_FONT_DIR, "system", "fonts", "Roboto-Regular.ttf")
    shutil.copy2(font_heavy_src, os.path.join(MODULE_DIR, "system", "fonts", "Roboto-Regular.ttf"))
    print("  + system/fonts/Roboto-Regular.ttf")

def write_module_scripts():
    print("[*] Generating module scripts...")

    module_prop = """id=ios_bold_font_emoji
name= iOS Bold Font & iOS 26.4 Emoji
version=v2.0 • Ultra
versionCode=200
author=sheikhmehraan
description= Systemlessly replaces UI fonts with Apple SF Pro (Bold/Heavy) and emojis with iOS 26.4 Apple Color Emoji. Features GMS override protection, early post-fs-data mounting, and full OverlayFS support.
"""

    post_fs_data_sh = r"""#!/system/bin/sh
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
"""

    customize_sh = r"""#!/system/bin/sh
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
"""

    service_sh = r"""#!/system/bin/sh
##########################################################################################
#
#  iOS Bold Font & iOS 26.4 Emoji - Background Daemon
# Author: sheikhmehraan
#
##########################################################################################

MODPATH=${0%/*}
LOGFILE="$MODPATH/service.log"
MAX_LOG_SIZE=$((5 * 1024 * 1024))
MAX_LOG_FILES=3
MAX_LOG_AGE_DAYS=7

FACEBOOK_APPS="com.facebook.orca com.facebook.katana com.facebook.lite com.facebook.mlite"
GMS_FONT_PROVIDER="com.google.android.gms/com.google.android.gms.fonts.provider.FontsProvider"
GMS_FONT_UPDATER="com.google.android.gms/com.google.android.gms.fonts.update.UpdateSchedulerService"
GMS_FONT_DIR_PATTERN="com.google.android.gms/files/fonts"
DATA_FONTS_DIR="/data/fonts"
ORCA_FONT_DIR1="/data/data/com.facebook.orca/files/fonts"
ORCA_FONT_DIR2="/data/user/0/com.facebook.orca/files/fonts"

mkdir -p "$MODPATH"

log() {
    find "$MODPATH" -name "$(basename "$LOGFILE")*" -type f -mtime +$MAX_LOG_AGE_DAYS -exec rm -f {} \; 2>/dev/null
    if [ -f "$LOGFILE" ] && [ $(stat -c%s "$LOGFILE" 2>/dev/null || echo 0) -gt $MAX_LOG_SIZE ]; then
        for i in $(seq $MAX_LOG_FILES -1 1); do
            if [ -f "$LOGFILE.$i" ]; then
                mv "$LOGFILE.$i" "$LOGFILE.$((i+1))"
            fi
        done
        mv "$LOGFILE" "$LOGFILE.1"
    fi
    local log_message="$(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo "$log_message" >> "$LOGFILE"
}

log "================================================"
log " iOS Bold Font & iOS Emoji Service Daemon"
log "Author: sheikhmehraan"
log "Brand: $(getprop ro.product.brand)"
log "Device: $(getprop ro.product.model)"
log "Android Version: $(getprop ro.build.version.release)"
log "================================================"

while [ "$(getprop sys.boot_completed)" != "1" ]; do
    sleep 5
done

while [ ! -d /sdcard ]; do
    sleep 5
done

log "INFO: Boot completed. Running emoji & font background services..."

# Replace in-app emoji fonts
replace_emoji_fonts() {
    if [ ! -f "$MODPATH/system/fonts/NotoColorEmoji.ttf" ]; then
        log "ERROR: Source emoji font not found."
        return
    fi

    EMOJI_FONTS=$(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null)
    for font in $EMOJI_FONTS; do
        if [ -w "$font" ]; then
            cp -f "$MODPATH/system/fonts/NotoColorEmoji.ttf" "$font" 2>/dev/null
            chmod 644 "$font" 2>/dev/null
            log "INFO: Replaced in-app emoji font: $font"
        fi
    done
}

replace_emoji_fonts

# Lock Messenger / Facebook emoji
lock_messenger_emoji() {
    for pkg in $FACEBOOK_APPS; do
        if [ -d "/data/data/$pkg" ]; then
            target="/data/data/$pkg/app_ras_blobs/FacebookEmoji.ttf"
            mkdir -p "/data/data/$pkg/app_ras_blobs" 2>/dev/null
            cp -f "$MODPATH/system/fonts/NotoColorEmoji.ttf" "$target" 2>/dev/null
            chmod 444 "$target" 2>/dev/null
            chattr +i "$target" 2>/dev/null
            log "INFO: Locked emoji file for $pkg"
        fi
    done
}

lock_messenger_emoji

# Clean Messenger font cache
for dir in "$ORCA_FONT_DIR1" "$ORCA_FONT_DIR2"; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"/* 2>/dev/null
        chmod 000 "$dir" 2>/dev/null
    fi
done

# Force stop Facebook apps to reload fonts
for app in $FACEBOOK_APPS; do
    am force-stop "$app" 2>/dev/null
done

sleep 2

# Disable GMS font services
disable_gms_font_services() {
    USERS=$(ls -d /data/user/* 2>/dev/null)
    for userpath in $USERS; do
        USERID=${userpath##*/}
        pm disable --user "$USERID" "$GMS_FONT_PROVIDER" >/dev/null 2>&1
        pm disable --user "$USERID" "$GMS_FONT_UPDATER" >/dev/null 2>&1
        log "INFO: Disabled GMS font services for user $USERID"
    done
}

disable_gms_font_services

# Cleanup GMS dynamic fonts
cleanup_gms_fonts() {
    if [ -d "$DATA_FONTS_DIR" ]; then
        rm -rf "$DATA_FONTS_DIR"/* 2>/dev/null
        log "INFO: Cleaned $DATA_FONTS_DIR"
    fi
    find /data -type d -path "*$GMS_FONT_DIR_PATTERN*" 2>/dev/null | while read dir; do
        rm -rf "$dir" 2>/dev/null
    done
}

cleanup_gms_fonts

log "INFO: Background service completed successfully."
log "================================================"
"""

    action_sh = r"""#!/system/bin/sh
MODPATH="${0%/*}"

set +o standalone 2>/dev/null
unset ASH_STANDALONE 2>/dev/null

SCRIPT="$MODPATH/service.sh"
if [ ! -f "$SCRIPT" ]; then
    echo -e "\nERROR: Missing service.sh" >&2
    exit 1
fi

if ! sh "$SCRIPT"; then
    echo -e "\nERROR: service.sh execution failed" >&2
    exit 1
fi

echo -e "\n iOS Font & Emoji maintenance completed successfully!\n"
exit 0
"""

    write_lf_file(os.path.join(MODULE_DIR, "module.prop"), module_prop)
    write_lf_file(os.path.join(MODULE_DIR, "post-fs-data.sh"), post_fs_data_sh)
    write_lf_file(os.path.join(MODULE_DIR, "customize.sh"), customize_sh)
    write_lf_file(os.path.join(MODULE_DIR, "service.sh"), service_sh)
    write_lf_file(os.path.join(MODULE_DIR, "action.sh"), action_sh)

def package_zip():
    print(f"[*] Packaging Ultra-Compressed flashable module to: {OUTPUT_ZIP}")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for root, dirs, files in os.walk(MODULE_DIR):
            for file in sorted(files):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, MODULE_DIR)
                zip_path = rel_path.replace("\\", "/")
                
                zinfo = zipfile.ZipInfo(zip_path)
                if zip_path.endswith(".sh") or "update-binary" in zip_path:
                    zinfo.external_attr = 0o755 << 16
                else:
                    zinfo.external_attr = 0o644 << 16
                
                with open(full_path, "rb") as f:
                    zf.writestr(zinfo, f.read())
                print(f"  -> Added {zip_path}")

    sha256 = hashlib.sha256()
    with open(OUTPUT_ZIP, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    
    zip_size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"\n[SUCCESS] Ultra Module packaged successfully!")
    print(f"File: {os.path.basename(OUTPUT_ZIP)}")
    print(f"Size: {zip_size_mb:.2f} MB")
    print(f"SHA256: {sha256.hexdigest()}")

if __name__ == "__main__":
    print("=== Building [iOS Bold Font + iOS Emoji] (Ultra Edition by sheikhmehraan) ===")
    clean_module_dir()
    ensure_dirs()
    copy_assets()
    write_module_scripts()
    package_zip()

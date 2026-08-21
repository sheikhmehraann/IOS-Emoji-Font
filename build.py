import os
import shutil
import zipfile
import hashlib
import struct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.join(BASE_DIR, "module")
DIST_DIR = os.path.join(BASE_DIR, "dist")
OUTPUT_ZIP = os.path.join(DIST_DIR, "iOS_Bold_Font_Emoji_v2.0_Ultra.zip")

ASSETS_DIR = os.path.join(BASE_DIR, "assets")

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

def patch_font_bold_flags(in_path, out_path):
    with open(in_path, "rb") as f:
        data = bytearray(f.read())
        
    num_tables = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num_tables):
        tag = data[12+i*16:16+i*16].decode("latin-1")
        offset = struct.unpack(">I", data[20+i*16:24+i*16])[0]
        length = struct.unpack(">I", data[24+i*16:28+i*16])[0]
        tables[tag] = (offset, length, 12+i*16)
        
    # 1. Update OS/2 table for Bold / Heavy weight
    if "OS/2" in tables:
        off, length, rec_off = tables["OS/2"]
        # Set usWeightClass to 800 (Heavy/Bold)
        struct.pack_into(">H", data, off+4, 800)
        # Set fsSelection bit 5 (Bold)
        sel = struct.unpack(">H", data[off+62:off+64])[0]
        sel |= 0x0020
        struct.pack_into(">H", data, off+62, sel)
        
    # 2. Update head table for Bold macStyle
    if "head" in tables:
        off, length, rec_off = tables["head"]
        mac_style = struct.unpack(">H", data[off+44:off+46])[0]
        mac_style |= 0x0001
        struct.pack_into(">H", data, off+44, mac_style)
        
    # Recalculate table checksums
    for tag, (off, length, rec_off) in tables.items():
        padded_len = (length + 3) & ~3
        table_bytes = data[off:off+length] + b"\x00" * (padded_len - length)
        csum = sum(struct.unpack(f">{padded_len//4}I", table_bytes)) & 0xFFFFFFFF
        if tag == "head":
            struct.pack_into(">I", data, off+8, 0)
            table_bytes = data[off:off+length] + b"\x00" * (padded_len - length)
            csum = sum(struct.unpack(f">{padded_len//4}I", table_bytes)) & 0xFFFFFFFF
        struct.pack_into(">I", data, rec_off+4, csum)
        
    # Recalculate entire font checkSumAdjustment
    if "head" in tables:
        head_off = tables["head"][0]
        padded_total = (len(data) + 3) & ~3
        full_bytes = data + b"\x00" * (padded_total - len(data))
        total_csum = sum(struct.unpack(f">{padded_total//4}I", full_bytes)) & 0xFFFFFFFF
        adjustment = (0xB1B0AFBA - total_csum) & 0xFFFFFFFF
        struct.pack_into(">I", data, head_off+8, adjustment)
        
    with open(out_path, "wb") as f:
        f.write(data)

def copy_assets():
    print("[*] Copying META-INF installer binaries...")
    src_meta = os.path.join(ASSETS_DIR, "META-INF", "com", "google", "android")
    dst_meta = os.path.join(MODULE_DIR, "META-INF", "com", "google", "android")
    shutil.copy2(os.path.join(src_meta, "update-binary"), os.path.join(dst_meta, "update-binary"))
    shutil.copy2(os.path.join(src_meta, "updater-script"), os.path.join(dst_meta, "updater-script"))

    print("[*] Copying iOS 26.4 Apple Color Emoji font...")
    emoji_src = os.path.join(ASSETS_DIR, "system", "fonts", "NotoColorEmoji.ttf")
    shutil.copy2(emoji_src, os.path.join(MODULE_DIR, "system", "fonts", "NotoColorEmoji.ttf"))
    print("  + system/fonts/NotoColorEmoji.ttf")

    print("[*] Patching & deploying SF Pro Text Heavy (True Bold) font...")
    font_heavy_src = os.path.join(ASSETS_DIR, "system", "fonts", "Roboto-Regular.ttf")
    font_heavy_dst = os.path.join(MODULE_DIR, "system", "fonts", "Roboto-Regular.ttf")
    patch_font_bold_flags(font_heavy_src, font_heavy_dst)
    print("  + system/fonts/Roboto-Regular.ttf (Native Bold Flags Active)")

def write_module_scripts():
    print("[*] Generating universal multi-partition font scripts...")

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

# Create target directories for ALL partition mount types
mkdir -p "$MODPATH/system/fonts" 2>/dev/null
mkdir -p "$MODPATH/product/fonts" 2>/dev/null
mkdir -p "$MODPATH/system_ext/fonts" 2>/dev/null
mkdir -p "$MODPATH/vendor/fonts" 2>/dev/null

mkdir -p "$MODPATH/system/product/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/system_ext/fonts" 2>/dev/null
mkdir -p "$MODPATH/system/vendor/fonts" 2>/dev/null

ui_print "  [+] Step 1/4: Expanding SF Pro Heavy to ALL Partition Targets..."

# 1. Baseline Common Font Targets across AOSP, Pixel, Samsung, Xiaomi, OnePlus, Transsion
common_targets="
Roboto-Regular.ttf Roboto-Bold.ttf Roboto-Medium.ttf Roboto-Italic.ttf Roboto-BoldItalic.ttf Roboto-Black.ttf Roboto-BlackItalic.ttf Roboto-Light.ttf Roboto-LightItalic.ttf Roboto-Thin.ttf Roboto-ThinItalic.ttf
RobotoStatic-Regular.ttf RobotoStatic-Bold.ttf RobotoStatic-Medium.ttf RobotoStatic-Italic.ttf RobotoStatic-BoldItalic.ttf RobotoStatic-Light.ttf RobotoStatic-Thin.ttf RobotoStatic-Black.ttf
Roboto-VariableFont_wdth,wght.ttf Roboto-Italic-VariableFont_wdth,wght.ttf RobotoFlex-Regular.ttf
RobotoCondensed-Regular.ttf RobotoCondensed-Bold.ttf RobotoCondensed-Italic.ttf RobotoCondensed-BoldItalic.ttf RobotoCondensed-Light.ttf RobotoCondensed-LightItalic.ttf RobotoCondensed-Medium.ttf RobotoCondensed-MediumItalic.ttf
GoogleSans-Regular.ttf GoogleSans-Medium.ttf GoogleSans-Bold.ttf GoogleSans-Italic.ttf GoogleSans-BoldItalic.ttf GoogleSans-MediumItalic.ttf GoogleSansFlex-Regular.ttf GoogleSansClock-Regular.ttf
GoogleSansText-Regular.ttf GoogleSansText-Medium.ttf GoogleSansText-Bold.ttf GoogleSansText-Italic.ttf GoogleSansText-BoldItalic.ttf GoogleSansText-MediumItalic.ttf
GS-Regular.ttf GS-Medium.ttf GS-Bold.ttf GS-Italic.ttf AndroidClock.ttf
TranSansShell.ttf TranSansSCShell.ttf TranSans_Regular.ttf TranSans_Medium.ttf TranSans_Bold.ttf TranSans_Italic.ttf TranSans_SC.ttf TranSans_TC.ttf
TOS_VF.ttf TOS_VF_SC.ttf TransSans-Regular.ttf TransSans-Medium.ttf TransSans-Bold.ttf TransSans_Italic.ttf TransSans_SC.ttf TransSans_Thai.ttf
InfinixSans-Regular.ttf InfinixSans-Bold.ttf TecnoSans-Regular.ttf TecnoSans-Bold.ttf
SECRobotoLight-Regular.ttf SECRobotoLight-Bold.ttf SECRoboto-Regular.ttf SECRoboto-Bold.ttf SamsungOne-400.ttf SamsungOne-500.ttf SamsungOne-600.ttf SamsungOne-700.ttf SamsungSans-Regular.ttf SamsungSans-Bold.ttf
MiSans-Regular.ttf MiSans-Medium.ttf MiSans-Demibold.ttf MiSans-Bold.ttf MiSans-Heavy.ttf MiSans-Light.ttf MiSans-Thin.ttf MiSans-Normal.ttf MiSans-Semibold.ttf MiSansVF.ttf MiSans_VF.ttf MiSansLatin-Regular.ttf MiSansLatin-Bold.ttf Miui-Regular.ttf Miui-Bold.ttf
OPlusSans-Regular.ttf OPlusSans-Medium.ttf OPlusSans-Bold.ttf OPlusSans-Light.ttf OPlusSans2.0-VF.ttf OPlusSans3.0-VF.ttf SysSans-En-Regular.ttf OnePlusSans-Regular.ttf OnePlusSans-Bold.ttf
"

for f in $common_targets; do
    cp -f "$BASE_FONT" "$MODPATH/system/fonts/$f" 2>/dev/null
    cp -f "$BASE_FONT" "$MODPATH/product/fonts/$f" 2>/dev/null
    cp -f "$BASE_FONT" "$MODPATH/system_ext/fonts/$f" 2>/dev/null
    cp -f "$BASE_FONT" "$MODPATH/vendor/fonts/$f" 2>/dev/null
    cp -f "$BASE_FONT" "$MODPATH/system/product/fonts/$f" 2>/dev/null
    cp -f "$BASE_FONT" "$MODPATH/system/system_ext/fonts/$f" 2>/dev/null
done

# 2. Dynamic Real-Time ROM Scanner: Scan device partitions for ANY active UI font
for pdir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts; do
    if [ -d "$pdir" ]; then
        sub="${pdir#/}"
        for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
            [ -f "$fpath" ] || continue
            fname=$(basename "$fpath")
            case "$fname" in
                *Emoji*|*emoji*|*Symbol*|*symbol*|*Clock*|*clock*|*NotoSansHebrew*|*NotoSansArabic*|*NotoSansThai*) ;;
                *)
                    cp -f "$BASE_FONT" "$MODPATH/$sub/$fname" 2>/dev/null
                    cp -f "$BASE_FONT" "$MODPATH/system/$sub/$fname" 2>/dev/null
                    ;;
            esac
        done
    fi
done

ui_print "      ✔ Universal coverage generated across /system, /product, and /system_ext"
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

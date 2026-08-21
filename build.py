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
APPLE_FONTS_DIR = os.path.join(ASSETS_DIR, "apple_fonts")

def clean_module_dir():
    if os.path.exists(MODULE_DIR):
        shutil.rmtree(MODULE_DIR)

def ensure_dirs():
    for sub in [
        os.path.join("META-INF", "com", "google", "android"),
        os.path.join("system", "fonts"),
        os.path.join("system", "product", "fonts"),
        os.path.join("system", "system_ext", "fonts"),
        os.path.join("system", "vendor", "fonts"),
        os.path.join("product", "fonts"),
        os.path.join("system_ext", "fonts"),
        os.path.join("vendor", "fonts"),
    ]:
        os.makedirs(os.path.join(MODULE_DIR, sub), exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)

def write_lf(filepath, content):
    with open(filepath, "wb") as f:
        f.write(content.replace("\r\n", "\n").encode("utf-8"))

def patch_variable_font(in_path, out_path, weight=850.0):
    with open(in_path, "rb") as f:
        data = bytearray(f.read())

    num_tables = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num_tables):
        r = 12 + i * 16
        tag = data[r:r + 4].decode("latin-1")
        offset = struct.unpack(">I", data[r + 8:r + 12])[0]
        length = struct.unpack(">I", data[r + 12:r + 16])[0]
        tables[tag] = (offset, length, r)

    if "fvar" in tables:
        off = tables["fvar"][0]
        axes_off = off + struct.unpack(">H", data[off + 4:off + 6])[0]
        n_axes = struct.unpack(">H", data[off + 8:off + 10])[0]
        ax_size = struct.unpack(">H", data[off + 10:off + 12])[0]
        for a in range(n_axes):
            pos = axes_off + a * ax_size
            if data[pos:pos + 4] == b"wght":
                max_val = struct.unpack(">i", data[pos + 12:pos + 16])[0] / 65536
                actual_weight = min(weight, max_val)
                fv = int(actual_weight * 65536)
                struct.pack_into(">i", data, pos + 4, fv)   # minValue
                struct.pack_into(">i", data, pos + 8, fv)   # defaultValue
                struct.pack_into(">i", data, pos + 12, fv)  # maxValue

    if "OS/2" in tables:
        off = tables["OS/2"][0]
        struct.pack_into(">H", data, off + 4, int(min(weight, 850)))
        fs = struct.unpack(">H", data[off + 62:off + 64])[0]
        struct.pack_into(">H", data, off + 62, fs | 0x0020)

    if "head" in tables:
        off = tables["head"][0]
        ms = struct.unpack(">H", data[off + 44:off + 46])[0]
        struct.pack_into(">H", data, off + 44, ms | 0x0001)

    for tag, (off, length, rec_off) in tables.items():
        pl = (length + 3) & ~3
        tb = data[off:off + length] + b"\x00" * (pl - length)
        if tag == "head":
            struct.pack_into(">I", data, off + 8, 0)
            tb = data[off:off + length] + b"\x00" * (pl - length)
        cs = sum(struct.unpack(f">{pl // 4}I", tb)) & 0xFFFFFFFF
        struct.pack_into(">I", data, rec_off + 4, cs)

    if "head" in tables:
        ho = tables["head"][0]
        pt = (len(data) + 3) & ~3
        fb = data + b"\x00" * (pt - len(data))
        tc = sum(struct.unpack(f">{pt // 4}I", fb)) & 0xFFFFFFFF
        struct.pack_into(">I", data, ho + 8, (0xB1B0AFBA - tc) & 0xFFFFFFFF)

    with open(out_path, "wb") as f:
        f.write(data)

def copy_assets():
    src = os.path.join(ASSETS_DIR, "META-INF", "com", "google", "android")
    dst = os.path.join(MODULE_DIR, "META-INF", "com", "google", "android")
    shutil.copy2(os.path.join(src, "update-binary"), os.path.join(dst, "update-binary"))
    shutil.copy2(os.path.join(src, "updater-script"), os.path.join(dst, "updater-script"))

    sysfonts = os.path.join(MODULE_DIR, "system", "fonts")

    # iOS 26.4 Apple Color Emoji
    shutil.copy2(
        os.path.join(ASSETS_DIR, "system", "fonts", "NotoColorEmoji.ttf"),
        os.path.join(sysfonts, "NotoColorEmoji.ttf"),
    )

    # SF Pro TrueType Bold (Rich Heavy Bold 850)
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro.ttf"),
        os.path.join(sysfonts, "SF-Pro-Bold.ttf"),
        850.0,
    )
    shutil.copy2(os.path.join(sysfonts, "SF-Pro-Bold.ttf"), os.path.join(sysfonts, "SF-Pro-Variable.ttf"))

    # SF Pro Display Heavy (static OTF, real weight 800)
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro-Display-Heavy.otf"),
        os.path.join(sysfonts, "SF-Pro-Bold.otf"),
    )
    with open(os.path.join(sysfonts, "SF-Pro-Bold.otf"), "rb") as f:
        d = bytearray(f.read())
    nt = struct.unpack(">H", d[4:6])[0]
    for i in range(nt):
        r = 12 + i * 16
        tag = d[r:r+4].decode("latin-1")
        off = struct.unpack(">I", d[r+8:r+12])[0]
        if tag == "OS/2":
            fs = struct.unpack(">H", d[off+62:off+64])[0]
            struct.pack_into(">H", d, off+62, fs | 0x0020)
        elif tag == "head":
            ms = struct.unpack(">H", d[off+44:off+46])[0]
            struct.pack_into(">H", d, off+44, ms | 0x0001)
    with open(os.path.join(sysfonts, "SF-Pro-Bold.otf"), "wb") as f:
        f.write(d)

    # SF Pro Rounded Bold (clocks / lockscreen)
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro-Rounded-Bold.otf"),
        os.path.join(sysfonts, "SF-Pro-Rounded.otf"),
    )

    # Noto Nastaliq Urdu Bold (the famous Urdu calligraphic font, weight locked to 700)
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "NotoNastaliqUrdu-VF.ttf"),
        os.path.join(sysfonts, "NotoNastaliqUrdu-Bold.ttf"),
        700.0,
    )

    # SF Hebrew Bold (850)
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Hebrew.ttf"),
        os.path.join(sysfonts, "SF-Hebrew.ttf"),
        850.0,
    )

    # SF Armenian Bold (850)
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Armenian.ttf"),
        os.path.join(sysfonts, "SF-Armenian.ttf"),
        850.0,
    )

    # SF Georgian Bold (850)
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Georgian.ttf"),
        os.path.join(sysfonts, "SF-Georgian.ttf"),
        850.0,
    )

def write_module_scripts():
    write_lf(os.path.join(MODULE_DIR, "module.prop"), """\
id=ios_bold_font_emoji
name= iOS Bold Font & iOS 26.4 Emoji
version=v2.0 • Ultra
versionCode=200
author=sheikhmehraan
description= Rich Apple SF Pro Bold (850) + Noto Nastaliq Urdu Bold + iOS 26.4 Emoji. Complete coverage for TranSans, TOS_VF, Roboto, and all languages across all apps and partitions.
""")

    write_lf(os.path.join(MODULE_DIR, "customize.sh"), r"""#!/system/bin/sh
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
""")

    write_lf(os.path.join(MODULE_DIR, "post-fs-data.sh"), r"""#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Early Boot Daemon (post-fs-data.sh)
# Author: sheikhmehraan
#
# Bind-mounts Apple fonts & Noto Nastaliq Urdu Bold over every partition before Zygote.
# Overrides TranSans, TransSans, TOS_VF, and cached theme fonts.
##########################################################################################

MODPATH=${0%/*}
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

# Reset dynamic Android & Transsion font caches
rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/system/theme/* 2>/dev/null
rm -rf /data/system/users/*/theme/* 2>/dev/null
rm -rf /data/resource-cache/* 2>/dev/null

# Dynamic Early-Boot Bind-Mount Engine across ALL partitions and directories
for dir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts \
           /system/product/fonts /system/system_ext/fonts /system/vendor/fonts \
           /data/system/theme/fonts /data/system/users/0/theme/fonts; do
    [ -d "$dir" ] || continue
    for fpath in "$dir"/*.ttf "$dir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
        case "$fname" in
            *Symbol*|*symbol*|*Math*|*math*|*Mono*|*mono*) continue ;;
            *Emoji*|*emoji*)
                [ -f "$EF" ] && mount -o bind "$EF" "$fpath" 2>/dev/null ;;
            *Clock*|*clock*)
                [ -f "$RF" ] && mount -o bind "$RF" "$fpath" 2>/dev/null ;;
            *Nastaliq*|*nastaliq*|*Urdu*|*urdu*|*Arabic*|*arabic*|*Naskh*|*naskh*|*Kufi*|*kufi*)
                [ -f "$UF" ] && mount -o bind "$UF" "$fpath" 2>/dev/null ;;
            *Hebrew*|*hebrew*)
                [ -f "$HF" ] && mount -o bind "$HF" "$fpath" 2>/dev/null ;;
            *Armenian*|*armenian*)
                [ -f "$AMF" ] && mount -o bind "$AMF" "$fpath" 2>/dev/null ;;
            *Georgian*|*georgian*)
                [ -f "$GF" ] && mount -o bind "$GF" "$fpath" 2>/dev/null ;;
            TOS_VF*|*Variable*|*VF*|*Flex*)
                [ -f "$VF" ] && mount -o bind "$VF" "$fpath" 2>/dev/null ;;
            TranSans*|TransSans*|InfinixSans*|TecnoSans*|ItelSans*|TOS*)
                case "$fname" in
                    *.otf) [ -f "$BOF" ] && mount -o bind "$BOF" "$fpath" 2>/dev/null ;;
                    *)     [ -f "$BTF" ] && mount -o bind "$BTF" "$fpath" 2>/dev/null ;;
                esac
                ;;
            Roboto*|GoogleSans*|MiSans*|Samsung*|OPlus*|DroidSans*|NotoSans-*|NotoSerif-*)
                case "$fname" in
                    *.otf) [ -f "$BOF" ] && mount -o bind "$BOF" "$fpath" 2>/dev/null ;;
                    *)     [ -f "$BTF" ] && mount -o bind "$BTF" "$fpath" 2>/dev/null ;;
                esac
                ;;
            *Devanagari*|*Bengali*|*Tamil*|*Telugu*|*Kannada*|*Malayalam*|*Gurmukhi*|*Gujarati*|*Oriya*|*Sinhala*|*Myanmar*|*Khmer*|*Lao*|*Thai*|*Tibetan*|*Ethiopic*|*Cherokee*|*Canadian*|*CJK*|*HanSans*)
                case "$fname" in
                    *Regular*|*Light*|*Thin*|*Medium*)
                        bold=$(echo "$fpath" | sed 's/Regular/Bold/g;s/Light/Bold/g;s/Thin/Bold/g;s/Medium/Bold/g')
                        [ -f "$bold" ] && [ "$bold" != "$fpath" ] && mount -o bind "$bold" "$fpath" 2>/dev/null
                        ;;
                esac
                ;;
            *.otf)
                [ -f "$BOF" ] && mount -o bind "$BOF" "$fpath" 2>/dev/null ;;
            *)
                [ -f "$BTF" ] && mount -o bind "$BTF" "$fpath" 2>/dev/null ;;
        esac
    done
done
""")

    write_lf(os.path.join(MODULE_DIR, "service.sh"), r"""#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Background Daemon
# Author: sheikhmehraan
##########################################################################################

MODPATH=${0%/*}
EF="$MODPATH/system/fonts/NotoColorEmoji.ttf"
BTF="$MODPATH/system/fonts/SF-Pro-Bold.ttf"
BOF="$MODPATH/system/fonts/SF-Pro-Bold.otf"
VF="$MODPATH/system/fonts/SF-Pro-Variable.ttf"
UF="$MODPATH/system/fonts/NotoNastaliqUrdu-Bold.ttf"

while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 5; done
while [ ! -d /sdcard ]; do sleep 5; done

# Replace in-app emoji fonts
if [ -f "$EF" ]; then
    for font in $(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null); do
        [ -w "$font" ] && cp -f "$EF" "$font" && chmod 644 "$font" 2>/dev/null
    done
fi

# Override any Transsion theme cached fonts in /data
for tdir in /data/system/theme/fonts /data/system/users/0/theme/fonts; do
    if [ -d "$tdir" ]; then
        for f in "$tdir"/*.ttf "$tdir"/*.otf; do
            [ -f "$f" ] || continue
            case "$(basename "$f")" in
                *Nastaliq*|*Urdu*|*Arabic*) cp -f "$UF" "$f" 2>/dev/null ;;
                *VF*|*Variable*) cp -f "$VF" "$f" 2>/dev/null ;;
                *.otf) cp -f "$BOF" "$f" 2>/dev/null ;;
                *) cp -f "$BTF" "$f" 2>/dev/null ;;
            esac
        done
    fi
done

# Lock Messenger / Facebook emoji
for pkg in com.facebook.orca com.facebook.katana com.facebook.lite com.facebook.mlite; do
    [ -d "/data/data/$pkg" ] || continue
    t="/data/data/$pkg/app_ras_blobs/FacebookEmoji.ttf"
    mkdir -p "/data/data/$pkg/app_ras_blobs" 2>/dev/null
    cp -f "$EF" "$t" 2>/dev/null
    chmod 444 "$t" 2>/dev/null
    chattr +i "$t" 2>/dev/null
    for sub in /files/fonts /cache /code_cache; do
        rm -rf "/data/data/${pkg}${sub}" 2>/dev/null
    done
    am force-stop "$pkg" 2>/dev/null
done

# Disable GMS font updater services
for uid in $(ls /data/user/ 2>/dev/null); do
    pm disable --user "$uid" "com.google.android.gms/com.google.android.gms.fonts.provider.FontsProvider" 2>/dev/null
    pm disable --user "$uid" "com.google.android.gms/com.google.android.gms.fonts.update.UpdateSchedulerService" 2>/dev/null
done
rm -rf /data/fonts/* 2>/dev/null
find /data -type d -path "*com.google.android.gms/files/fonts*" -exec rm -rf {} + 2>/dev/null
""")

    write_lf(os.path.join(MODULE_DIR, "action.sh"), r"""#!/system/bin/sh
MODPATH="${0%/*}"
set +o standalone 2>/dev/null
unset ASH_STANDALONE 2>/dev/null
sh "$MODPATH/service.sh" && echo " Done." || echo " Failed." >&2
""")

def package_zip():
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for root, _, files in os.walk(MODULE_DIR):
            for fn in sorted(files):
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, MODULE_DIR).replace("\\", "/")
                zi = zipfile.ZipInfo(rel)
                zi.external_attr = (0o755 if rel.endswith(".sh") or "update-binary" in rel else 0o644) << 16
                with open(full, "rb") as f:
                    zf.writestr(zi, f.read())

    h = hashlib.sha256()
    with open(OUTPUT_ZIP, "rb") as f:
        while c := f.read(65536):
            h.update(c)
    sz = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"[SUCCESS] {os.path.basename(OUTPUT_ZIP)} {sz:.2f} MB sha256:{h.hexdigest()}")

if __name__ == "__main__":
    clean_module_dir()
    ensure_dirs()
    copy_assets()
    write_module_scripts()
    package_zip()

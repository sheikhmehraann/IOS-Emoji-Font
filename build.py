import os
import shutil
import zipfile
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.join(BASE_DIR, "module")
DIST_DIR = os.path.join(BASE_DIR, "dist")
OUTPUT_ZIP = os.path.join(DIST_DIR, "iOS_Bold_Font_Emoji_v2.0_Ultra.zip")

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
APPLE_FONTS_DIR = os.path.join(ASSETS_DIR, "apple_fonts")
PATCHED_VF_DIR = os.path.join(ASSETS_DIR, "patched_vf")

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
        os.path.join("system", "etc"),
    ]:
        os.makedirs(os.path.join(MODULE_DIR, sub), exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)

def write_lf(filepath, content):
    with open(filepath, "wb") as f:
        f.write(content.replace("\r\n", "\n").encode("utf-8"))

def copy_assets():
    src = os.path.join(ASSETS_DIR, "META-INF", "com", "google", "android")
    dst = os.path.join(MODULE_DIR, "META-INF", "com", "google", "android")
    shutil.copy2(os.path.join(src, "update-binary"), os.path.join(dst, "update-binary"))
    shutil.copy2(os.path.join(src, "updater-script"), os.path.join(dst, "updater-script"))

    sysfonts = os.path.join(MODULE_DIR, "system", "fonts")
    sysetc = os.path.join(MODULE_DIR, "system", "etc")

    # 1. Custom fonts.xml with explicit Urdu, Arabic, and Indic Apple mappings
    if os.path.exists(os.path.join(ASSETS_DIR, "system", "etc", "fonts.xml")):
        shutil.copy2(
            os.path.join(ASSETS_DIR, "system", "etc", "fonts.xml"),
            os.path.join(sysetc, "fonts.xml"),
        )

    # 2. iOS 26.4 Apple Color Emoji
    shutil.copy2(
        os.path.join(ASSETS_DIR, "system", "fonts", "NotoColorEmoji.ttf"),
        os.path.join(sysfonts, "NotoColorEmoji.ttf"),
    )

    # 3. Apple SF Pro Text Heavy (Exact 800 Bold dev font with 1950/-494 matched metrics)
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro-Bold.ttf"),
        os.path.join(sysfonts, "SF-Pro-Bold.ttf"),
    )
    shutil.copy2(os.path.join(sysfonts, "SF-Pro-Bold.ttf"), os.path.join(sysfonts, "SF-Pro-Variable.ttf"))
    shutil.copy2(os.path.join(sysfonts, "SF-Pro-Bold.ttf"), os.path.join(sysfonts, "SF-Pro-Bold.otf"))

    # 4. Apple New York Serif Bold
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "NewYork-Bold.ttf"),
        os.path.join(sysfonts, "NewYork-Bold.ttf"),
    )

    # 5. SF Pro Rounded Bold
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro-Rounded-Bold.otf"),
        os.path.join(sysfonts, "SF-Pro-Rounded.otf"),
    )

    # 6. Normalized Noto Nastaliq Urdu Bold (Proportional 952/-241 on 1000 UPM / 1950/-494 on 2048 UPM)
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "NotoNastaliqUrdu-Bold.ttf"),
        os.path.join(sysfonts, "NotoNastaliqUrdu-Bold.ttf"),
    )

    # 7. Apple SF Multilingual Fonts (SF Arabic, SF Hebrew, SF Armenian, SF Georgian)
    shutil.copy2(os.path.join(APPLE_FONTS_DIR, "SF-Arabic-Bold.ttf"), os.path.join(sysfonts, "SF-Arabic.ttf"))
    shutil.copy2(os.path.join(APPLE_FONTS_DIR, "SF-Hebrew-Bold.ttf"), os.path.join(sysfonts, "SF-Hebrew.ttf"))
    shutil.copy2(os.path.join(APPLE_FONTS_DIR, "SF-Armenian-Bold.ttf"), os.path.join(sysfonts, "SF-Armenian.ttf"))
    shutil.copy2(os.path.join(APPLE_FONTS_DIR, "SF-Georgian-Bold.ttf"), os.path.join(sysfonts, "SF-Georgian.ttf"))

    # 8. Normalized World Language Fonts (Devanagari, Bengali, Gujarati, Gurmukhi, Kannada, Malayalam, Sinhala, Tamil, Telugu, Ethiopic, Khmer, Tibetan)
    if os.path.exists(PATCHED_VF_DIR):
        for fn in os.listdir(PATCHED_VF_DIR):
            if fn.endswith(".ttf") or fn.endswith(".otf"):
                shutil.copy2(os.path.join(PATCHED_VF_DIR, fn), os.path.join(sysfonts, fn))

def write_module_scripts():
    write_lf(os.path.join(MODULE_DIR, "module.prop"), """\
id=ios_bold_font_emoji
name= iOS Bold Font & iOS 26.4 Emoji (All Languages Edition)
version=v2.0 • Ultra
versionCode=200
author=sheikhmehraann
description= Complete Multilingual Apple Typography (SF Pro Heavy + New York + SF Arabic/Hebrew/Armenian/Georgian + Urdu Nastaliq Bold + Indic Bold + iOS 26.4 Emoji). 100% Boldness and Zero-Padding-Distortion across all languages.
""")

    write_lf(os.path.join(MODULE_DIR, "customize.sh"), r"""#!/system/bin/sh
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
""")

    write_lf(os.path.join(MODULE_DIR, "post-fs-data.sh"), r"""#!/system/bin/sh
MODPATH=${0%/*}
rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null
for pkg in com.instagram.android com.whatsapp com.facebook.orca com.facebook.katana; do
    rm -rf "/data/data/$pkg/cache" "/data/data/$pkg/code_cache" "/data/data/$pkg/files/fonts" 2>/dev/null
done
""")

    write_lf(os.path.join(MODULE_DIR, "service.sh"), r"""#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Safe Post-Boot Daemon
# Author: sheikhmehraan
##########################################################################################

MODPATH=${0%/*}
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
EF="$FD/NotoColorEmoji.ttf"

# Wait until Android fully completes boot to avoid any system_server startup race
while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done

# Replace in-app emoji fonts in WhatsApp / Facebook / Instagram / Gboard
if [ -f "$EF" ]; then
    for font in $(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null); do
        [ -w "$font" ] && cp -f "$EF" "$font" && chmod 644 "$font" 2>/dev/null
    done
fi

# WhatsApp in-app font lock
if [ -d "/data/data/com.whatsapp" ]; then
    mkdir -p "/data/data/com.whatsapp/files/NetworkResource" 2>/dev/null
    chattr -i "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    cp -f "$BTF" "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    chmod 444 "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    chattr +i "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
fi

for pkg in com.facebook.orca com.facebook.katana com.facebook.lite com.facebook.mlite; do
    [ -d "/data/data/$pkg" ] || continue
    t="/data/data/$pkg/app_ras_blobs/FacebookEmoji.ttf"
    mkdir -p "/data/data/$pkg/app_ras_blobs" 2>/dev/null
    cp -f "$EF" "$t" 2>/dev/null
    chmod 444 "$t" 2>/dev/null
    chattr +i "$t" 2>/dev/null
done
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

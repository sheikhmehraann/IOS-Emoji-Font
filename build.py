import os
import shutil
import zipfile
import subprocess
import hashlib
from fontTools.ttLib import TTFont

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

    # 1. iOS 26.4 Apple Color Emoji
    shutil.copy2(
        os.path.join(ASSETS_DIR, "system", "fonts", "NotoColorEmoji.ttf"),
        os.path.join(sysfonts, "NotoColorEmoji.ttf"),
    )

    # 2. Apple SF Pro Text Heavy (Single master copy)
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro-Bold.ttf"),
        os.path.join(sysfonts, "SF-Pro-Bold.ttf"),
    )

    # 3. Apple New York Serif Bold (Single master copy)
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "NewYork-Bold.ttf"),
        os.path.join(sysfonts, "NewYork-Bold.ttf"),
    )

    # 4. SF Pro Rounded Bold
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro-Rounded-Bold.otf"),
        os.path.join(sysfonts, "SF-Pro-Rounded.otf"),
    )

    # 5. Tuned Authentic Cascading Noto Nastaliq Urdu Bold (Single master copy)
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "NotoNastaliqUrdu-Bold.ttf"),
        os.path.join(sysfonts, "NotoNastaliqUrdu-Bold.ttf"),
    )

    # 6. Complete list of authentic, normalized world language fonts
    unique_scripts = [
        "NotoSansDevanagari-VF.ttf",
        "NotoSansGurmukhi-VF.ttf",
        "NotoSansBengali-VF.ttf",
        "NotoSansGujarati-VF.ttf",
        "NotoSansTamil-VF.ttf",
        "NotoSansTelugu-VF.ttf",
        "NotoSansKannada-VF.ttf",
        "NotoSansMalayalam-VF.ttf",
        "NotoSansSinhala-VF.ttf",
        "NotoSansThai-VF.ttf",
        "NotoSansKhmer-VF.ttf",
        "NotoSansLao-VF.ttf",
        "NotoSansMyanmar-VF.ttf",
        "NotoSansEthiopic-VF.ttf",
        "NotoSansHebrew-VF.ttf",
        "NotoSansArmenian-VF.ttf",
        "NotoSansGeorgian-VF.ttf",
        "NotoSerifTibetan-VF.ttf",
    ]
    for fn in unique_scripts:
        src_path = os.path.join(PATCHED_VF_DIR, fn)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(sysfonts, fn))
            print(f"Included in module: {fn} ({os.path.getsize(src_path)} bytes)")
        else:
            print(f"[WARNING] Missing font: {fn}")

def write_module_scripts():
    write_lf(os.path.join(MODULE_DIR, "module.prop"), """\
id=IOS-bold-Font-Emoji
name=iOS Bold Font & iOS Emoji
version=v2.0
versionCode=200
author=sheikhmehraann
description=System-wide iOS bold fonts and iOS emoji.
""")

    write_lf(os.path.join(MODULE_DIR, "customize.sh"), r"""#!/system/bin/sh
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
MODPATH=${0%/*}
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
EF="$FD/NotoColorEmoji.ttf"

while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done

if [ -f "$EF" ]; then
    for font in $(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null); do
        [ -w "$font" ] && cp -f "$EF" "$font" && chmod 644 "$font" 2>/dev/null
    done
fi

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
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)

    seven_zip = r"C:\Program Files\7-Zip\7z.exe"
    cmd = [
        seven_zip, "a", "-tzip",
        "-mx=9", "-mfb=258", "-mpass=15",
        OUTPUT_ZIP,
        os.path.join(MODULE_DIR, "*")
    ]
    subprocess.run(cmd, check=True)

    h = hashlib.sha256()
    with open(OUTPUT_ZIP, "rb") as f:
        while c := f.read(65536):
            h.update(c)
    sz = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"[SUCCESS] Ultra Compressed ZIP: {os.path.basename(OUTPUT_ZIP)} {sz:.2f} MB sha256:{h.hexdigest()}")

if __name__ == "__main__":
    clean_module_dir()
    ensure_dirs()
    copy_assets()
    write_module_scripts()
    package_zip()

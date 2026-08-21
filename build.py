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

# Apple's "Bold" .otf files are actually weight 600 (Semibold).
# Real visible bold on iOS "Bold Text" mode = weight 800.
# We use 800 for variable axes and SF-Pro-Display-Heavy.otf (800) as the static font.
BOLD_WEIGHT = 800.0


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
    ]:
        os.makedirs(os.path.join(MODULE_DIR, sub), exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)


def write_lf(filepath, content):
    with open(filepath, "wb") as f:
        f.write(content.replace("\r\n", "\n").encode("utf-8"))


def patch_variable_font(in_path, out_path, weight=BOLD_WEIGHT):
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
                fv = int(weight * 65536)
                struct.pack_into(">i", data, pos + 4, fv)   # minValue
                struct.pack_into(">i", data, pos + 8, fv)   # defaultValue

    if "OS/2" in tables:
        off = tables["OS/2"][0]
        struct.pack_into(">H", data, off + 4, int(weight))
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

    # SF Pro Variable (wght axis locked to 800)
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro.ttf"),
        os.path.join(sysfonts, "SF-Pro-Variable.ttf"),
    )

    # SF Pro Display Heavy (static, weight 800 — the REAL bold, not the 600 "Bold")
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro-Display-Heavy.otf"),
        os.path.join(sysfonts, "SF-Pro-Bold.otf"),
    )

    # SF Pro Rounded Bold (clocks / lockscreen)
    shutil.copy2(
        os.path.join(APPLE_FONTS_DIR, "SF-Pro-Rounded-Bold.otf"),
        os.path.join(sysfonts, "SF-Pro-Rounded.otf"),
    )

    # SF Arabic (Urdu/Arabic/Persian) — wght axis locked to 800
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Arabic.ttf"),
        os.path.join(sysfonts, "SF-Arabic.ttf"),
    )

    # SF Hebrew — wght axis locked to 800
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Hebrew.ttf"),
        os.path.join(sysfonts, "SF-Hebrew.ttf"),
    )

    # SF Armenian — wght axis locked to 800
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Armenian.ttf"),
        os.path.join(sysfonts, "SF-Armenian.ttf"),
    )

    # SF Georgian — wght axis locked to 800
    patch_variable_font(
        os.path.join(APPLE_FONTS_DIR, "SF-Georgian.ttf"),
        os.path.join(sysfonts, "SF-Georgian.ttf"),
    )


def write_module_scripts():
    write_lf(os.path.join(MODULE_DIR, "module.prop"), """\
id=ios_bold_font_emoji
name= iOS Bold Font & iOS 26.4 Emoji
version=v2.0 • Ultra
versionCode=200
author=sheikhmehraan
description= Replaces system fonts with Apple SF Pro Bold (weight 800) and emojis with iOS 26.4 Apple Color Emoji across all languages and partitions.
""")

    write_lf(os.path.join(MODULE_DIR, "customize.sh"), r"""#!/system/bin/sh
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

FD="$MODPATH/system/fonts"
VF="$FD/SF-Pro-Variable.ttf"
BF="$FD/SF-Pro-Bold.otf"
RF="$FD/SF-Pro-Rounded.otf"
AF="$FD/SF-Arabic.ttf"
HF="$FD/SF-Hebrew.ttf"
AMF="$FD/SF-Armenian.ttf"
GF="$FD/SF-Georgian.ttf"
EF="$FD/NotoColorEmoji.ttf"

# All overlay paths MUST be under system/ for Magisk/KSU/APatch
place() {
    local src="$1" name="$2"
    cp -f "$src" "$MODPATH/system/fonts/$name"                2>/dev/null
    cp -f "$src" "$MODPATH/system/product/fonts/$name"        2>/dev/null
    cp -f "$src" "$MODPATH/system/system_ext/fonts/$name"     2>/dev/null
    cp -f "$src" "$MODPATH/system/vendor/fonts/$name"         2>/dev/null
}

# ── Variable fonts (TOS_VF, Roboto VF, GoogleSansFlex, MiSans VF, OPlus VF) ──
ui_print "  [1/5] Variable fonts..."
for f in \
    Roboto-VariableFont_wdth,wght.ttf  Roboto-Italic-VariableFont_wdth,wght.ttf \
    RobotoFlex-Regular.ttf \
    TOS_VF.ttf  TOS_VF_SC.ttf \
    GoogleSansFlex-Regular.ttf \
    MiSansVF.ttf  MiSans_VF.ttf \
    OPlusSans2.0-VF.ttf  OPlusSans3.0-VF.ttf
do place "$VF" "$f"; done
ui_print "      ✔ Done"

# ── Static UI fonts (Roboto, TranSans, Google Sans, Samsung, Xiaomi, OnePlus, etc.) ──
ui_print "  [2/5] Static UI fonts..."
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
ui_print "      ✔ Done"

# ── Multilingual script fonts ──
ui_print "  [3/5] Multilingual scripts (Urdu, Arabic, Hebrew, Armenian, Georgian)..."

# Arabic / Urdu / Persian — on iOS these ALL use SF Arabic (Naskh style, not Nastaliq)
for f in \
    NotoNastaliqUrdu-Regular.ttf NotoNastaliqUrdu-Bold.ttf \
    NotoNastaliqUrdu.ttf \
    NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf NotoSansArabic-Medium.ttf \
    NotoSansArabicUI-Regular.ttf NotoSansArabicUI-Bold.ttf NotoSansArabicUI-Medium.ttf \
    NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf \
    NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf \
    NotoKufiArabic-Regular.ttf NotoKufiArabic-Bold.ttf
do place "$AF" "$f"; done

for f in NotoSansHebrew-Regular.ttf NotoSansHebrew-Bold.ttf NotoSansHebrew-Medium.ttf
do place "$HF" "$f"; done

for f in NotoSansArmenian-Regular.ttf NotoSansArmenian-Bold.ttf NotoSansArmenian-Medium.ttf
do place "$AMF" "$f"; done

for f in NotoSansGeorgian-Regular.ttf NotoSansGeorgian-Bold.ttf NotoSansGeorgian-Medium.ttf
do place "$GF" "$f"; done

for f in AndroidClock.ttf GoogleSansClock-Regular.ttf
do place "$RF" "$f"; done
ui_print "      ✔ Done"

# ── Dynamic OEM font scanner ──
ui_print "  [4/5] Scanning device for unlisted OEM fonts..."
SCAN_COUNT=0
for pdir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts; do
    [ -d "$pdir" ] || continue
    for fpath in "$pdir"/*.ttf "$pdir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
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
ui_print "      ✔ Replaced $SCAN_COUNT additional OEM fonts"

# ── Emoji, caches, permissions ──
ui_print "  [5/5] Emoji, caches, permissions..."
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

set_perm_recursive "$MODPATH" 0 0 0755 0644
for s in post-fs-data.sh service.sh action.sh; do
    [ -f "$MODPATH/$s" ] && set_perm "$MODPATH/$s" 0 0 0755
done
chcon -R u:object_r:system_file:s0 "$MODPATH/system" 2>/dev/null
ui_print "      ✔ All done"
ui_print " "
ui_print "  ─────────────────────────────────────────"
ui_print "  ✔ Reboot to apply.                       "
ui_print "  ─────────────────────────────────────────"
ui_print " "
""")

    write_lf(os.path.join(MODULE_DIR, "post-fs-data.sh"), r"""#!/system/bin/sh
##########################################################################################
# iOS Bold Font & iOS 26.4 Emoji — Early Boot (post-fs-data)
# Author: sheikhmehraan
#
# Bind-mounts Apple fonts over EVERY system font file as a nuclear fallback
# for OverlayFS edge cases, dynamic partitions, and A/B slots.
##########################################################################################

MODPATH=${0%/*}
FD="$MODPATH/system/fonts"
VF="$FD/SF-Pro-Variable.ttf"
BF="$FD/SF-Pro-Bold.otf"
RF="$FD/SF-Pro-Rounded.otf"
AF="$FD/SF-Arabic.ttf"
HF="$FD/SF-Hebrew.ttf"
AMF="$FD/SF-Armenian.ttf"
GF="$FD/SF-Georgian.ttf"
EF="$FD/NotoColorEmoji.ttf"

rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

for dir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts \
           /system/product/fonts /system/system_ext/fonts /system/vendor/fonts; do
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
            *Arabic*|*arabic*|*Urdu*|*urdu*|*Nastaliq*|*nastaliq*|*Naskh*|*naskh*|*Kufi*|*kufi*)
                [ -f "$AF" ] && mount -o bind "$AF" "$fpath" 2>/dev/null ;;
            *Hebrew*|*hebrew*)
                [ -f "$HF" ] && mount -o bind "$HF" "$fpath" 2>/dev/null ;;
            *Armenian*|*armenian*)
                [ -f "$AMF" ] && mount -o bind "$AMF" "$fpath" 2>/dev/null ;;
            *Georgian*|*georgian*)
                [ -f "$GF" ] && mount -o bind "$GF" "$fpath" 2>/dev/null ;;
            TOS_VF*|*Variable*|*VF*|*Flex*)
                [ -f "$VF" ] && mount -o bind "$VF" "$fpath" 2>/dev/null ;;
            *Devanagari*|*Bengali*|*Tamil*|*Telugu*|*Kannada*|*Malayalam*|*Gurmukhi*|*Gujarati*|*Oriya*|*Sinhala*|*Myanmar*|*Khmer*|*Lao*|*Thai*|*Tibetan*|*Ethiopic*|*Cherokee*|*Canadian*|*CJK*|*HanSans*)
                case "$fname" in
                    *Regular*|*Light*|*Thin*|*Medium*)
                        bold=$(echo "$fpath" | sed 's/Regular/Bold/g;s/Light/Bold/g;s/Thin/Bold/g;s/Medium/Bold/g')
                        [ -f "$bold" ] && [ "$bold" != "$fpath" ] && mount -o bind "$bold" "$fpath" 2>/dev/null
                        ;;
                esac
                ;;
            *)
                [ -f "$BF" ] && mount -o bind "$BF" "$fpath" 2>/dev/null ;;
        esac
    done
done
""")

    write_lf(os.path.join(MODULE_DIR, "service.sh"), r"""#!/system/bin/sh
##########################################################################################
# iOS Bold Font & iOS 26.4 Emoji — Late Service
# Author: sheikhmehraan
##########################################################################################

MODPATH=${0%/*}

while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 5; done
while [ ! -d /sdcard ]; do sleep 5; done

EF="$MODPATH/system/fonts/NotoColorEmoji.ttf"

if [ -f "$EF" ]; then
    for font in $(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null); do
        [ -w "$font" ] && cp -f "$EF" "$font" && chmod 644 "$font" 2>/dev/null
    done
fi

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
    print(f"[OK] {os.path.basename(OUTPUT_ZIP)}  {sz:.2f} MB  sha256:{h.hexdigest()}")


if __name__ == "__main__":
    clean_module_dir()
    ensure_dirs()
    copy_assets()
    write_module_scripts()
    package_zip()

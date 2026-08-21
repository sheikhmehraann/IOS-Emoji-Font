#!/system/bin/sh
##########################################################################################
#
#  iOS Bold Font & iOS 26.4 Emoji - post-fs-data.sh
# Author: sheikhmehraan
#
##########################################################################################

MODPATH=${0%/*}
FONT_DIR="$MODPATH/system/fonts"
VAR_FONT="$FONT_DIR/SF-Pro-Variable.ttf"
HEAVY_FONT="$FONT_DIR/SF-Pro-Heavy.otf"
BLACK_FONT="$FONT_DIR/SF-Pro-Black.otf"
BOLD_FONT="$FONT_DIR/SF-Pro-Bold.otf"
ROUND_FONT="$FONT_DIR/SF-Pro-Rounded.otf"
ARABIC_FONT="$FONT_DIR/SF-Arabic.ttf"
HEBREW_FONT="$FONT_DIR/SF-Hebrew.ttf"
ARMENIAN_FONT="$FONT_DIR/SF-Armenian.ttf"
GEORGIAN_FONT="$FONT_DIR/SF-Georgian.ttf"
BASE_EMOJI="$FONT_DIR/NotoColorEmoji.ttf"

# Clean dynamic Android 12-16 FontManager caches before system_server starts
rm -rf /data/fonts/* 2>/dev/null
rm -rf /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/fonts/run_metadata.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

mkdir -p /data/fonts 2>/dev/null
chmod 755 /data/fonts 2>/dev/null

# Early-boot Dynamic Bind-Mount across ALL active partitions & fonts
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
                *Clock*|*clock*)
                    if [ -f "$ROUND_FONT" ]; then
                        mount -o bind "$ROUND_FONT" "$fpath" 2>/dev/null
                    fi
                    ;;
                *Arabic*|*arabic*|*Urdu*|*urdu*)
                    if [ -f "$ARABIC_FONT" ]; then
                        mount -o bind "$ARABIC_FONT" "$fpath" 2>/dev/null
                    fi
                    ;;
                *Hebrew*|*hebrew*)
                    if [ -f "$HEBREW_FONT" ]; then
                        mount -o bind "$HEBREW_FONT" "$fpath" 2>/dev/null
                    fi
                    ;;
                *Armenian*|*armenian*)
                    if [ -f "$ARMENIAN_FONT" ]; then
                        mount -o bind "$ARMENIAN_FONT" "$fpath" 2>/dev/null
                    fi
                    ;;
                *Georgian*|*georgian*)
                    if [ -f "$GEORGIAN_FONT" ]; then
                        mount -o bind "$GEORGIAN_FONT" "$fpath" 2>/dev/null
                    fi
                    ;;
                *Variable*|*VF*|*Flex*)
                    if [ -f "$VAR_FONT" ]; then
                        mount -o bind "$VAR_FONT" "$fpath" 2>/dev/null
                    elif [ -f "$HEAVY_FONT" ]; then
                        mount -o bind "$HEAVY_FONT" "$fpath" 2>/dev/null
                    fi
                    ;;
                *NotoSansDevanagari*|*NotoSansBengali*|*NotoSansTamil*|*NotoSansTelugu*|*NotoSansKannada*|*NotoSansMalayalam*|*NotoSansGurmukhi*|*NotoSansGujarati*|*NotoSansOriya*|*NotoSansSinhala*|*NotoSansMyanmar*|*NotoSansKhmer*|*NotoSansLao*|*NotoSansThai*|*NotoSansTibetan*|*NotoSansEthiopic*|*NotoSansCherokee*|*NotoSansCanadianAboriginal*|*NotoSansCJK*|*NotoSerifCJK*|*SourceHanSans*)
                    # If this is a regular/light font and a bold version exists on the device, bind-mount bold over it!
                    case "$fname" in
                        *Regular*|*Light*|*Thin*|*Medium*)
                            bold_candidate=$(echo "$fpath" | sed -e 's/Regular/Bold/g' -e 's/Light/Bold/g' -e 's/Thin/Bold/g' -e 's/Medium/Bold/g')
                            if [ -f "$bold_candidate" ] && [ "$bold_candidate" != "$fpath" ]; then
                                mount -o bind "$bold_candidate" "$fpath" 2>/dev/null
                            fi
                            ;;
                    esac
                    ;;
                *Symbol*|*symbol*|*Math*|*math*) ;;
                *)
                    if [ -f "$MODPATH/system/fonts/$fname" ]; then
                        mount -o bind "$MODPATH/system/fonts/$fname" "$fpath" 2>/dev/null
                    elif [ -f "$MODPATH/product/fonts/$fname" ]; then
                        mount -o bind "$MODPATH/product/fonts/$fname" "$fpath" 2>/dev/null
                    elif [ -f "$MODPATH/system_ext/fonts/$fname" ]; then
                        mount -o bind "$MODPATH/system_ext/fonts/$fname" "$fpath" 2>/dev/null
                    elif [ -f "$HEAVY_FONT" ]; then
                        mount -o bind "$HEAVY_FONT" "$fpath" 2>/dev/null
                    fi
                    ;;
            esac
        done
    fi
done

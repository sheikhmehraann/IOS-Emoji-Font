#!/system/bin/sh
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

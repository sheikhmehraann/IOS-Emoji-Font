#!/system/bin/sh
##########################################################################################
#  iOS Bold Font & iOS 26.4 Emoji - Early Boot Daemon (post-fs-data.sh)
# Author: sheikhmehraan
#
# 100% Safe Boot Engine: Cleans font cache and bind-mounts explicit font files only.
# Never deletes system directories and never binds over TTC collections or symbol files.
##########################################################################################

MODPATH=${0%/*}
FD="$MODPATH/system/fonts"
BTF="$FD/SF-Pro-Bold.ttf"
BOF="$FD/SF-Pro-Bold.otf"
VF="$FD/SF-Pro-Variable.ttf"
RF="$FD/SF-Pro-Rounded.otf"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"
AF="$FD/SF-Arabic.ttf"
HF="$FD/SF-Hebrew.ttf"
AMF="$FD/SF-Armenian.ttf"
GF="$FD/SF-Georgian.ttf"
EF="$FD/NotoColorEmoji.ttf"

# Clean FontManager dynamic caches safely
rm -rf /data/fonts/* 2>/dev/null
rm -f  /data/system/font_fallback.xml 2>/dev/null
rm -rf /data/data/com.google.android.gms/files/fonts/* 2>/dev/null
rm -rf /data/user_de/*/com.google.android.gms/files/fonts/* 2>/dev/null

# Safe Bind-Mount Engine (Targeted font filenames only)
for dir in /system/fonts /product/fonts /system_ext/fonts /vendor/fonts \
           /system/product/fonts /system/system_ext/fonts /system/vendor/fonts; do
    [ -d "$dir" ] || continue
    for fpath in "$dir"/*.ttf "$dir"/*.otf; do
        [ -f "$fpath" ] || continue
        fname=$(basename "$fpath")
        case "$fname" in
            *Symbol*|*symbol*|*Math*|*math*|*Mono*|*mono*|*.ttc) continue ;;
            *Emoji*|*emoji*)
                [ -f "$EF" ] && mount -o bind "$EF" "$fpath" 2>/dev/null ;;
            *Clock*|*clock*)
                [ -f "$RF" ] && mount -o bind "$RF" "$fpath" 2>/dev/null ;;
            *Nastaliq*|*nastaliq*)
                [ -f "$UF" ] && mount -o bind "$UF" "$fpath" 2>/dev/null ;;
            *Arabic*|*arabic*|*Naskh*|*naskh*|*Kufi*|*kufi*)
                [ -f "$AF" ] && mount -o bind "$AF" "$fpath" 2>/dev/null ;;
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
        esac
    done
done

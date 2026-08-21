#!/system/bin/sh
FD="/data/adb/modules/ios_bold_font_emoji/system/fonts"
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

# Bind mount Emoji
mount -o bind "$EF" /system/fonts/NotoColorEmoji.ttf 2>/dev/null
mount -o bind "$EF" /system/fonts/NotoColorEmojiFlags.ttf 2>/dev/null

# Bind mount Roboto & UI fonts
for f in /system/fonts/Roboto*.ttf /system/fonts/DroidSans*.ttf /system/fonts/GoogleSans*.ttf /system/fonts/SECRoboto*.ttf; do
    [ -f "$f" ] && mount -o bind "$BTF" "$f" 2>/dev/null
done

# Bind mount Transsion OS fonts in /product/fonts
for f in /product/fonts/*; do
    [ -f "$f" ] || continue
    mount -o bind "$BTF" "$f" 2>/dev/null
done

# Bind mount Urdu & Arabic
for f in /system/fonts/NotoNaskhArabic*.ttf /system/fonts/NotoSansArabic*.ttf /system/fonts/NotoNastaliqUrdu*.ttf; do
    [ -f "$f" ] && mount -o bind "$UF" "$f" 2>/dev/null
done

# Bind mount Hebrew, Armenian, Georgian, Clocks
for f in /system/fonts/NotoSansHebrew*.ttf; do [ -f "$f" ] && mount -o bind "$HF" "$f" 2>/dev/null; done
for f in /system/fonts/NotoSansArmenian*.ttf; do [ -f "$f" ] && mount -o bind "$AMF" "$f" 2>/dev/null; done
for f in /system/fonts/NotoSansGeorgian*.ttf; do [ -f "$f" ] && mount -o bind "$GF" "$f" 2>/dev/null; done
for f in /system/fonts/AndroidClock*.ttf; do [ -f "$f" ] && mount -o bind "$RF" "$f" 2>/dev/null; done

# Restart Gboard & Settings
am force-stop com.google.android.inputmethod.latin 2>/dev/null
am force-stop com.android.settings 2>/dev/null
am force-stop com.transsion.theme 2>/dev/null

echo "SUCCESS: Live font and emoji bind-mount applied!"

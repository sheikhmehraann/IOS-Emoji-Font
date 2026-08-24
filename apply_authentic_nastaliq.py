import subprocess

cmd = r"""
MOD="/data/adb/modules/ios_bold_font_emoji"
FD="$MOD/system/fonts"
UF="$FD/NotoNastaliqUrdu-Bold.ttf"

for f in NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf \
         NotoNaskhArabicUI-Regular.ttf NotoNaskhArabicUI-Bold.ttf \
         NotoSansArabic-Regular.ttf NotoSansArabic-Bold.ttf \
         NotoSansArabicUI-Regular.ttf NotoSansArabicUI-Bold.ttf \
         NotoKufiArabic-Regular.ttf NotoKufiArabic-Bold.ttf; do
    cp -f "$UF" "$FD/$f" 2>/dev/null
    cp -f "$UF" "$MOD/system/product/fonts/$f" 2>/dev/null
    cp -f "$UF" "$MOD/system/system_ext/fonts/$f" 2>/dev/null
    cp -f "$UF" "$MOD/system/vendor/fonts/$f" 2>/dev/null
done

# Verify
echo "=== NASTALIQ URDU HASHES ON ARABIC FALLBACK TARGETS ==="
for f in NotoNastaliqUrdu-Bold.ttf NotoNaskhArabic-Regular.ttf NotoNaskhArabic-Bold.ttf NotoSansArabic-Regular.ttf; do
    md5sum "$FD/$f"
done
"""

with open(r"C:\Users\Admin\apply_authentic_nastaliq.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\apply_authentic_nastaliq.sh", "/data/local/tmp/apply_authentic_nastaliq.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/apply_authentic_nastaliq.sh'"], capture_output=True, text=True)
print(res.stdout)

import subprocess

cmd = r"""
echo "=== CHECKING SYSTEM FONT FILES IN MODULE ==="
for f in NotoSansDevanagari-VF.ttf NotoNastaliqUrdu-Bold.ttf NotoNaskhArabic-Regular.ttf NotoSansArabic-Regular.ttf; do
    echo "--- $f ---"
    ls -la /data/adb/modules/ios_bold_font_emoji/system/fonts/$f 2>/dev/null
    md5sum /data/adb/modules/ios_bold_font_emoji/system/fonts/$f 2>/dev/null
done
"""

with open(r"C:\Users\Admin\verify_module_fonts.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\verify_module_fonts.sh", "/data/local/tmp/verify_module_fonts.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/verify_module_fonts.sh'"], capture_output=True, text=True)
print(res.stdout)

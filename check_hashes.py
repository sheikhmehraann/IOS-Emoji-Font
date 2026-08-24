import subprocess

cmd = r"""
for f in Roboto-Regular.ttf NotoNastaliqUrdu-Bold.ttf NotoNastaliqUrdu-Regular.ttf NotoNaskhArabic-Regular.ttf NotoSansArabic-Regular.ttf NotoSansDevanagari-VF.ttf NotoSansBengali-VF.ttf NotoSansTamil-VF.ttf NotoColorEmoji.ttf; do
    echo "--- $f ---"
    md5sum /data/adb/modules/ios_bold_font_emoji/system/fonts/$f 2>/dev/null
done
"""

with open(r"C:\Users\Admin\check_hashes.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\check_hashes.sh", "/data/local/tmp/check_hashes.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/check_hashes.sh'"], capture_output=True, text=True)
print(res.stdout)

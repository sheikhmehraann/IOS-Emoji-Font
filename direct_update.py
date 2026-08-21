import subprocess

cmd = r"""
# Push and update module directory directly
unzip -o /data/local/tmp/iOS_Bold_Font_Emoji_v2.0_Ultra.zip -d /data/adb/modules/ios_bold_font_emoji/ >/dev/null 2>&1

# Remove heavy duplicate VF files from module system/fonts
for vf in /data/adb/modules/ios_bold_font_emoji/system/fonts/*-VF.ttf; do
    [ -f "$vf" ] && rm -f "$vf"
done

chmod 755 /data/adb/modules/ios_bold_font_emoji/*.sh
chmod 755 /data/adb/modules/ios_bold_font_emoji/action.sh
chmod 755 /data/adb/modules/ios_bold_font_emoji/service.sh
chmod 755 /data/adb/modules/ios_bold_font_emoji/post-fs-data.sh

echo "MODULE UPDATED & CLEANED DIRECTLY ON DEVICE!"
"""

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\dist\iOS_Bold_Font_Emoji_v2.0_Ultra.zip", "/data/local/tmp/iOS_Bold_Font_Emoji_v2.0_Ultra.zip"], check=True)

with open(r"C:\Users\Admin\direct_update.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\direct_update.sh", "/data/local/tmp/direct_update.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/direct_update.sh'"], capture_output=True, text=True)
print(res.stdout)

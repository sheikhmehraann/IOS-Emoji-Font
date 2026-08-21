import subprocess

cmd = r"""
BTF="/data/adb/modules/ios_bold_font_emoji/system/fonts/SF-Pro-Bold.ttf"

# WhatsApp replacement
if [ -d "/data/data/com.whatsapp" ]; then
    mkdir -p "/data/data/com.whatsapp/files/NetworkResource" 2>/dev/null
    chattr -i "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    cp -f "$BTF" "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    chmod 444 "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    chattr +i "/data/data/com.whatsapp/files/NetworkResource/roboto_flex_font.ttf" 2>/dev/null
    
    # Also replace any other TTF in WhatsApp
    for f in $(find /data/data/com.whatsapp -iname "*.ttf" 2>/dev/null); do
        chattr -i "$f" 2>/dev/null
        cp -f "$BTF" "$f" 2>/dev/null
        chmod 444 "$f" 2>/dev/null
        chattr +i "$f" 2>/dev/null
    done
    
    am force-stop com.whatsapp 2>/dev/null
    echo "WhatsApp in-app fonts replaced and locked!"
fi

# Instagram data font replacement
if [ -d "/data/data/com.instagram.android" ]; then
    for f in $(find /data/data/com.instagram.android -iname "*.ttf" 2>/dev/null); do
        chattr -i "$f" 2>/dev/null
        cp -f "$BTF" "$f" 2>/dev/null
        chmod 444 "$f" 2>/dev/null
        chattr +i "$f" 2>/dev/null
    done
    
    am force-stop com.instagram.android 2>/dev/null
    echo "Instagram in-app fonts replaced and locked!"
fi
"""

with open(r"C:\Users\Admin\replace_inapp_fonts.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\replace_inapp_fonts.sh", "/data/local/tmp/replace_inapp_fonts.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/replace_inapp_fonts.sh'"], capture_output=True, text=True)
print(res.stdout)

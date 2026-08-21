import subprocess

cmd = r"""
# Map all language Regular fonts to their Bold counterparts
for f in /system/fonts/*Regular*.ttf /system/fonts/*Regular*.otf; do
    [ -f "$f" ] || continue
    bold=$(echo "$f" | sed 's/Regular/Bold/g')
    if [ -f "$bold" ] && [ "$bold" != "$f" ]; then
        mount -o bind "$bold" "$f" 2>/dev/null
    fi
done

# Restart SystemUI & Gboard
am force-stop com.google.android.inputmethod.latin 2>/dev/null
am force-stop com.android.settings 2>/dev/null
am force-stop com.transsion.theme 2>/dev/null

echo "All language regular fonts mapped to Bold!"
"""

with open(r"C:\Users\Admin\bold_all_languages.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\bold_all_languages.sh", "/data/local/tmp/bold_all_languages.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/bold_all_languages.sh'"], capture_output=True, text=True)
print(res.stdout)

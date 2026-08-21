import subprocess

cmd = r"""
echo "=== ALL FONTS IN /system/fonts NOT REPLACED ==="
for f in /system/fonts/*; do
    [ -f "$f" ] || continue
    # Check if MD5 matches Apple SF Pro Bold or Noto Nastaliq Urdu or Emoji
    md5=$(md5sum "$f" | cut -d' ' -f1)
    case "$md5" in
        aa89ccc18f05befd12371b99fd406c09|ee00cb681dd69010aa03717c2fee15f9|085d31af364f1033ba51784ee90b3018)
            ;;
        *)
            echo "NOT REPLACED: $(basename "$f") (MD5: $md5)"
            ;;
    esac
done

echo "=== APEX FONTS ==="
ls -la /apex/com.android.i18n/fonts/ 2>/dev/null
"""

with open(r"C:\Users\Admin\find_unreplaced.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\find_unreplaced.sh", "/data/local/tmp/find_unreplaced.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/find_unreplaced.sh'"], capture_output=True, text=True)
print(res.stdout)

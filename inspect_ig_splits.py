import subprocess

cmd = r"""
echo "=== ALL SPLIT APKS OF INSTAGRAM ==="
ls -la /data/app/~~0iox8GeXVUPQ-shTlnDYgw==/com.instagram.android-*

for apk in /data/app/~~0iox8GeXVUPQ-shTlnDYgw==/com.instagram.android-*/*.apk; do
    echo "--- Fonts in $apk ---"
    unzip -l "$apk" | grep -iE '\.ttf|\.otf|\.ttc'
done

echo "=== CHECK ALL FILES IN INSTAGRAM DATA FOR FONTS ==="
find /data/data/com.instagram.android -type f | grep -iE 'font|\.ttf|\.otf|\.ttc'
"""

with open(r"C:\Users\Admin\inspect_ig_splits.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\inspect_ig_splits.sh", "/data/local/tmp/inspect_ig_splits.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/inspect_ig_splits.sh'"], capture_output=True, text=True)
print(res.stdout)

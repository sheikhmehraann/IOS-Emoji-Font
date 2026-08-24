import subprocess

cmd = r"""
echo "=== ALL FONTS IN /system/fonts/ ==="
ls -1 /system/fonts/

echo "=== ALL FONTS IN /product/fonts/ ==="
ls -1 /product/fonts/ 2>/dev/null
"""

with open(r"C:\Users\Admin\list_device_fonts.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\list_device_fonts.sh", "/data/local/tmp/list_device_fonts.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/list_device_fonts.sh'"], capture_output=True, text=True)
with open(r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\device_fonts_list.txt", "w", encoding="utf-8") as f:
    f.write(res.stdout)
print("Device fonts listed. Total lines:", len(res.stdout.splitlines()))

import subprocess

cmd = r"""
md5sum /system/fonts/Roboto-Regular.ttf
md5sum /system/fonts/NotoSansDevanagari-VF.ttf
md5sum /system/fonts/NotoSansBengali-VF.ttf
md5sum /system/fonts/NotoSansTamil-VF.ttf
md5sum /system/fonts/NotoSansTelugu-VF.ttf
md5sum /system/fonts/NotoSansGujarati-Regular.ttf
md5sum /system/fonts/NotoSansThai-Regular.ttf
md5sum /system/fonts/NotoNaskhArabic-Regular.ttf
md5sum /system/fonts/NotoColorEmoji.ttf
"""

with open(r"C:\Users\Admin\check_md5.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\check_md5.sh", "/data/local/tmp/check_md5.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/check_md5.sh'"], capture_output=True, text=True)
print(res.stdout)

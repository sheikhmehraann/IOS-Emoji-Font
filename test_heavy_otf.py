import subprocess

cmd = r"""
FD="/data/adb/modules/ios_bold_font_emoji/system/fonts"
BOF="$FD/SF-Pro-Bold.otf"

# Test mounting the static SF Pro Heavy Display OTF directly over Roboto-Regular.ttf and TOS_250829VF.ttf
mount -o bind "$BOF" /system/fonts/Roboto-Regular.ttf
mount -o bind "$BOF" /product/fonts/TOS_250829VF.ttf 2>/dev/null
mount -o bind "$BOF" /product/fonts/TransSans_SC_0704.ttf 2>/dev/null

# Restart Zygote
setprop ctl.restart zygote
"""

with open(r"C:\Users\Admin\test_heavy_otf.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\test_heavy_otf.sh", "/data/local/tmp/test_heavy_otf.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/test_heavy_otf.sh'"], capture_output=True, text=True)
print(res.stdout)

import subprocess

cmd = r"""
echo "=== ALL OPEN FONT FILES IN SYSTEMUI ==="
S_PID=$(pidof com.android.systemui)
if [ -n "$S_PID" ]; then
    cat /proc/$S_PID/maps | grep -iE '\.ttf|\.otf|\.ttc' | awk '{print $6}' | sort -u
fi

echo "=== ALL OPEN FONT FILES IN INSTAGRAM ==="
I_PID=$(pidof com.instagram.android)
if [ -n "$I_PID" ]; then
    cat /proc/$I_PID/maps | grep -iE '\.ttf|\.otf|\.ttc' | awk '{print $6}' | sort -u
fi

echo "=== ALL OPEN FONT FILES IN WHATSAPP ==="
W_PID=$(pidof com.whatsapp)
if [ -n "$W_PID" ]; then
    cat /proc/$W_PID/maps | grep -iE '\.ttf|\.otf|\.ttc' | awk '{print $6}' | sort -u
fi

echo "=== FIRST 10 FAMILIES IN /system/etc/font_fallback.xml ==="
cat /system/etc/font_fallback.xml | grep -E '<family|<font' | head -n 35

echo "=== FIRST 10 FAMILIES IN /system/etc/fonts.xml ==="
cat /system/etc/fonts.xml | grep -E '<family|<font' | head -n 35
"""

with open(r"C:\Users\Admin\forensic_fonts.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\forensic_fonts.sh", "/data/local/tmp/forensic_fonts.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/forensic_fonts.sh'"], capture_output=True, text=True)
print(res.stdout)

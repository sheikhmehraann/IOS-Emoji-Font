import subprocess

cmd = r"""
echo "=== WHATSAPP PID & MAPS ==="
W_PID=$(pidof com.whatsapp)
if [ -n "$W_PID" ]; then
    echo "WhatsApp PID: $W_PID"
    cat /proc/$W_PID/maps | grep -iE '\.ttf|\.otf|\.ttc' | awk '{print $6}' | sort -u
else
    echo "WhatsApp not running, launching..."
    am start -n com.whatsapp/.Main >/dev/null 2>&1
    sleep 2
    W_PID=$(pidof com.whatsapp)
    echo "WhatsApp PID after launch: $W_PID"
    cat /proc/$W_PID/maps | grep -iE '\.ttf|\.otf|\.ttc' | awk '{print $6}' | sort -u
fi

echo "=== INSTAGRAM PID & MAPS ==="
I_PID=$(pidof com.instagram.android)
if [ -n "$I_PID" ]; then
    echo "Instagram PID: $I_PID"
    cat /proc/$I_PID/maps | grep -iE '\.ttf|\.otf|\.ttc' | awk '{print $6}' | sort -u
else
    echo "Instagram not running, launching..."
    am start -n com.instagram.android/com.instagram.mainactivity.MainActivity >/dev/null 2>&1
    sleep 2
    I_PID=$(pidof com.instagram.android)
    echo "Instagram PID after launch: $I_PID"
    cat /proc/$I_PID/maps | grep -iE '\.ttf|\.otf|\.ttc' | awk '{print $6}' | sort -u
fi
"""

with open(r"C:\Users\Admin\inspect_app_fonts.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\inspect_app_fonts.sh", "/data/local/tmp/inspect_app_fonts.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/inspect_app_fonts.sh'"], capture_output=True, text=True)
print(res.stdout)

import subprocess

cmd = r"""
echo "=== SYSTEM CRASH LOGS ==="
logcat -b crash -d | tail -n 40

echo "=== SYSTEM_SERVER LAST CRASH ==="
logcat -d | grep -iE 'system_server.*crash|fatal|sigbus|sigsegv' | tail -n 25

echo "=== CHECK MOUNTS ON /system/fonts ==="
mount | grep -i '/system/fonts' | wc -l
"""

with open(r"C:\Users\Admin\check_crash.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\check_crash.sh", "/data/local/tmp/check_crash.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/check_crash.sh'"], capture_output=True, text=True)
print(res.stdout)

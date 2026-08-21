import subprocess

cmd = r"""
echo "=== ZYGOTE / SYSTEM_SERVER LOGS ==="
logcat -d | grep -iE 'AndroidRuntime|FATAL|SystemServer|minikin|FreeType|FontManager|Typeface' | tail -n 50
"""

with open(r"C:\Users\Admin\check_boot_crash.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\check_boot_crash.sh", "/data/local/tmp/check_boot_crash.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/check_boot_crash.sh'"], capture_output=True, text=True)
print(res.stdout)

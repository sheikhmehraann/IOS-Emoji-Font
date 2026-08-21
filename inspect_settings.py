import subprocess

cmd = r"""
echo "=== TRANSSION SETTINGS PROPERTIES ==="
getprop | grep -iE 'font|theme|tran'

echo "=== TRANSSION THEME / SETTINGS DB ==="
settings list system | grep -iE 'font|theme'
settings list global | grep -iE 'font|theme'
settings list secure | grep -iE 'font|theme'
"""

with open(r"C:\Users\Admin\inspect_settings.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\inspect_settings.sh", "/data/local/tmp/inspect_settings.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/inspect_settings.sh'"], capture_output=True, text=True)
print(res.stdout)

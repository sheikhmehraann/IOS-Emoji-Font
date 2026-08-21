import subprocess

cmd = r"""
# Read stock font metrics directly using od/hexdump
echo "=== EXTRACTING STOCK FONT HEADERS ==="
for f in /system/fonts/Roboto-Regular.ttf /product/fonts/TOS_250829VF.ttf /product/fonts/TransSans_SC_0704.ttf; do
    echo "--- File: $f ---"
    ls -la "$f"
done
"""

with open(r"C:\Users\Admin\read_stock_headers.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\read_stock_headers.sh", "/data/local/tmp/read_stock_headers.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/read_stock_headers.sh'"], capture_output=True, text=True)
print(res.stdout)

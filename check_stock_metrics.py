import subprocess

cmd = r"""
python3 -c '
import struct
with open("/system/fonts/NotoSans-Regular.ttf", "rb") as f:
    data = f.read()
num_tables = struct.unpack(">H", data[4:6])[0]
tables = {}
for i in range(num_tables):
    r = 12 + i * 16
    tag = data[r:r+4].decode("latin-1")
    tables[tag] = (struct.unpack(">I", data[r+8:r+12])[0], struct.unpack(">I", data[r+12:r+16])[0])
if "hhea" in tables:
    off = tables["hhea"][0]
    print("NotoSans hhea:", struct.unpack(">hhh", data[off+4:off+10]))
if "OS/2" in tables:
    off = tables["OS/2"][0]
    print("NotoSans typo:", struct.unpack(">hhh", data[off+68:off+74]))
    print("NotoSans win:", struct.unpack(">HH", data[off+74:off+78]))
' 2>/dev/null
"""

with open(r"C:\Users\Admin\check_stock_metrics.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\check_stock_metrics.sh", "/data/local/tmp/check_stock_metrics.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/check_stock_metrics.sh'"], capture_output=True, text=True)
print(res.stdout)

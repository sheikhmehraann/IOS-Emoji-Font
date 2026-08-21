import subprocess

cmd = r"""
mkdir -p /data/local/tmp/stock_pull
cp /product/fonts/* /data/local/tmp/stock_pull/ 2>/dev/null
ls -la /data/local/tmp/stock_pull/
"""

with open(r"C:\Users\Admin\pull_product_stock.sh", "w", newline="\n") as f:
    f.write(cmd)

subprocess.run([r"C:\platform-tools\adb.exe", "push", r"C:\Users\Admin\pull_product_stock.sh", "/data/local/tmp/pull_product_stock.sh"], check=True)
res = subprocess.run([r"C:\platform-tools\adb.exe", "shell", "su -c 'sh /data/local/tmp/pull_product_stock.sh'"], capture_output=True, text=True)
print(res.stdout)

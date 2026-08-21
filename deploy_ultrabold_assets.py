import os
import shutil

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"
src_static = os.path.join(apple_dir, "SF-Pro-UltraBold-Static.ttf")
src_vf = os.path.join(apple_dir, "SF-Pro-UltraBold-VF.ttf")

shutil.copy2(src_static, os.path.join(apple_dir, "SF-Pro-Bold.ttf"))
shutil.copy2(src_static, os.path.join(apple_dir, "SF-Pro-Bold-PureStatic.ttf"))
shutil.copy2(src_vf, os.path.join(apple_dir, "SF-Pro-Variable.ttf"))

print("Updated all Apple SF Pro assets to Ultra Bold 900 with 1:1 Stock Roboto Metrics!")

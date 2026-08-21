import os
import shutil

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"
master_sf = os.path.join(apple_dir, "SF-Pro-MasterBold.ttf")

shutil.copy2(master_sf, os.path.join(apple_dir, "SF-Pro-Bold.ttf"))
shutil.copy2(master_sf, os.path.join(apple_dir, "SF-Pro-Bold-PureStatic.ttf"))
shutil.copy2(master_sf, os.path.join(apple_dir, "SF-Pro-Variable.ttf"))
shutil.copy2(master_sf, os.path.join(apple_dir, "SF-Pro-Text-Heavy.otf"))

print("Master Bold Font deployed to all SF-Pro font targets!")

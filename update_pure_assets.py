import os
import shutil

apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"

# Replace SF-Pro-Bold.ttf with pure static TrueType heavy bold
pure_sf = os.path.join(apple_dir, "SF-Pro-Bold-PureStatic.ttf")
target_sf = os.path.join(apple_dir, "SF-Pro-Text-Heavy.otf") # keep name but use TrueType binary
target_sf_ttf = os.path.join(apple_dir, "SF-Pro-Bold.ttf")

shutil.copy2(pure_sf, target_sf)
shutil.copy2(pure_sf, target_sf_ttf)

# Replace NewYork with pure static TrueType bold
pure_ny = os.path.join(apple_dir, "NewYork-Bold-PureStatic.ttf")
target_ny = os.path.join(apple_dir, "NewYorkLarge-Heavy.otf")
target_ny_ttf = os.path.join(apple_dir, "NewYork-Bold.ttf")

shutil.copy2(pure_ny, target_ny)
shutil.copy2(pure_ny, target_ny_ttf)

print("Updated Apple font binaries with 100% pure static TrueType (glyf outline) versions!")

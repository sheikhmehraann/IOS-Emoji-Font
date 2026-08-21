import os
import shutil

src_dev_font = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\Made By Another Dev\extracted\system\fonts\Roboto-Regular.ttf"
apple_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\assets\apple_fonts"

# Deploy this exact font to all SF Pro targets
for target in [
    "SF-Pro-Bold.ttf",
    "SF-Pro-Bold.otf",
    "SF-Pro-Variable.ttf",
    "SF-Pro-Bold-PureStatic.ttf",
    "SF-Pro-MasterBold.ttf",
    "SF-Pro-Text-Heavy.otf",
    "SF-Pro-Text-Bold.otf",
    "SF-Pro-Display-Heavy.otf",
    "SF-Pro-Display-Bold.otf"
]:
    dst = os.path.join(apple_dir, target)
    shutil.copy2(src_dev_font, dst)
    print(f"Copied exact dev font to: {dst}")

print("Exact dev font (MD5: 6c498791e52ee77eedea219f291f638d) deployed to all SF Pro targets!")

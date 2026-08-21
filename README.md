#  iOS Bold Font & iOS 26.4 Emoji • Ultra Edition

**Author**: `sheikhmehraan`  
**Version**: `v2.0 • Ultra Edition`  
**Supported Root Engines**: Magisk (v20.4+), KernelSU, APatch  
**Supported Android Versions**: Android 10, 11, 12, 13, 14, 15, 16 (AOSP, Pixel, Transsion HiOS/XOS/itelOS/TOS, Samsung One UI, MIUI/HyperOS, ColorOS/OxygenOS)

---

## 🌟 Highlights

- ** iOS SF Pro Heavy UI Font**: Systemlessly replaces AOSP `Roboto` (static & variable fonts) and Transsion `TranSansShell` / `TOS_VF` with Apple's SF Pro Text Heavy for a distinct, bold iOS experience across your entire device.
- ** Latest iOS 26.4 Apple Color Emoji**: Replaces all system emoji binaries (`NotoColorEmoji.ttf`, `SamsungColorEmoji.ttf`, `ColorUniEmoji.ttf`, `LGNotoColorEmoji.ttf`, etc.).
- **⚡ Early `post-fs-data` Mounting**: Overrides dynamic fonts **before** Zygote and `system_server` start, guaranteeing that fonts load under all conditions.
- **🛡️ GMS Override Protection**: Cleans `/data/fonts` dynamic caches and disables Google Play Services font updaters (`FontsProvider`, `UpdateSchedulerService`) so Android cannot revert your emojis over the air.
- **💬 Social & Keyboard App Integration**: Direct bind-mounts and cache purges for **WhatsApp**, **Facebook**, **Messenger**, **Messenger Lite**, and **Gboard**.
- **🚀 Full OverlayFS & Magic Mount Support**: Fully compatible with modern kernels using OverlayFS.

---

## 📂 File Structure

```text
IOS-Emoji-Font/
├── dist/
│   └── iOS_Bold_Font_Emoji_v2.0_Ultra.zip    <-- Ultra-compressed flashable ZIP
├── module/                                   <-- Source directory
│   ├── META-INF/com/google/android/
│   │   ├── update-binary                    <-- Magisk / KSU binary installer
│   │   └── updater-script
│   ├── system/
│   │   ├── fonts/                           <-- NotoColorEmoji.ttf & SF Pro Heavy Roboto
│   │   ├── product/fonts/                   <-- TOS_VF.ttf & Product fonts
│   │   └── system_ext/fonts/                <-- System_Ext partition fonts
│   ├── action.sh                            <-- Magisk Manager action button maintenance
│   ├── customize.sh                         <-- Professional terminal installer UI
│   ├── module.prop                          <-- Stylish metadata by sheikhmehraan
│   ├── post-fs-data.sh                      <-- Early boot cache cleaner & bind mount
│   └── service.sh                           <-- Boot daemon for GMS blocker & emoji lock
├── build.py                                 <-- Ultra compiler script (compresslevel=9)
└── README.md
```

---

## 📲 How to Install

1. Download [`dist/iOS_Bold_Font_Emoji_v2.0_Ultra.zip`](file:///C:/Users/Admin/Videos/Github/IOS-Emoji-Font/dist/iOS_Bold_Font_Emoji_v2.0_Ultra.zip).
2. Open **Magisk**, **KernelSU**, or **APatch**.
3. Go to **Modules** $\rightarrow$ **Install from storage**.
4. Select `iOS_Bold_Font_Emoji_v2.0_Ultra.zip` and flash.
5. Reboot your device.

---

## 🛠️ Rebuilding the Module

```bash
python build.py
```
Outputs the flashable package to `dist/iOS_Bold_Font_Emoji_v2.0_Ultra.zip`.

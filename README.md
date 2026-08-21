<div align="center">

#  iOS Bold Font & iOS 26.4 Emoji (Ultra Edition)

[![GitHub Release](https://img.shields.io/github/v/release/sheikhmehraann/IOS-Emoji-Font?style=for-the-badge&logo=github&color=blue)](https://github.com/sheikhmehraann/IOS-Emoji-Font/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Magisk](https://img.shields.io/badge/Magisk-v20.4+-brightgreen.svg?style=for-the-badge&logo=magisk)](https://github.com/topjohnwu/Magisk)
[![KernelSU](https://img.shields.io/badge/KernelSU-Supported-red.svg?style=for-the-badge)](https://kernelsu.org)
[![APatch](https://img.shields.io/badge/APatch-Supported-purple.svg?style=for-the-badge)](https://github.com/bmax121/APatch)
[![Android](https://img.shields.io/badge/Android-10%20to%2016-orange.svg?style=for-the-badge&logo=android)](https://www.android.com)

A systemless module for **Magisk**, **KernelSU**, and **APatch** that replaces Android system typography with **Apple SF Pro (Heavy / Bold)** and system emojis with **iOS 26.4 Apple Color Emoji**. Engineered with dynamic ROM font discovery, early `post-fs-data` binding, and Google Play Services override protection.

</div>

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [Compatibility Matrix](#-compatibility-matrix)
- [How It Works](#-how-it-works)
- [Installation Guide](#-installation-guide)
- [Building from Source](#-building-from-source)
- [Project Architecture](#-project-architecture)
- [Troubleshooting](#-troubleshooting)
- [License & Credits](#-license--credits)

---

## ⚡ Key Features

| Feature | Description |
| :--- | :--- |
| **Apple SF Pro Heavy UI Font** | Full system-wide replacement of standard Roboto, variable fonts, condensed styles, and OEM typography with Apple SF Pro Heavy. |
| **iOS 26.4 Apple Color Emoji** | High-definition Apple emoji glyphs mapped across all OEM fallback definitions (`SamsungColorEmoji`, `ColorUniEmoji`, `LGNotoColorEmoji`, etc.). |
| **Dynamic Partition Scanner** | Real-time scanner active during installation and boot that discovers and overrides all active font files across `/system`, `/product`, `/system_ext`, and `/vendor`. |
| **Early `post-fs-data` Execution** | Intercepts font resolution before Zygote and `system_server` start, guaranteeing 100% font coverage even on aggressive ROMs. |
| **GMS Dynamic Font Protection** | Purges `/data/fonts` caches and blocks Google Play Services (`FontsProvider`, `UpdateSchedulerService`) from reverting emojis via cloud updates. |
| **Social & Keyboard Integration** | In-app bind-mounts and cache locks for **WhatsApp**, **Facebook**, **Messenger**, **Messenger Lite**, and **Gboard**. |
| **OverlayFS & Magic Mount** | Fully compatible with both traditional Magic Mount and modern KernelSU/APatch OverlayFS implementations. |

---

## 📱 Compatibility Matrix

### Supported Root Managers
- **Magisk**: v20.4+ (Standard & Alpha / Canary)
- **KernelSU**: v0.6.0+ (GKI & Non-GKI)
- **APatch**: v10567+

### Supported Android Versions
- Android 10 (Q)
- Android 11 (R)
- Android 12 & 12L (S)
- Android 13 (Tiramisu)
- Android 14 (Upside Down Cake)
- Android 15 (Vanilla Ice Cream)
- Android 16 (Baklava Preview)

### Supported OEM Skins
- **Google Pixel / AOSP / Custom ROMs** (LineageOS, PixelOS, EvolutionX, crDroid, etc.)
- **Transsion** (HiOS, XOS, itelOS, TOS)
- **Samsung** (One UI 2.0 - 7.0+)
- **Xiaomi / Redmi / POCO** (MIUI 12 - 14, HyperOS 1.0 - 2.0+)
- **OnePlus / OPPO / Realme** (OxygenOS, ColorOS, Realme UI)
- **Nothing OS**, **Motorola MyUX**, **Sony Xperia UI**, **ASUS ZenUI**

---

## 🛠️ How It Works

```text
[ Device Boot: post-fs-data ]
           │
           ├── 1. Purge /data/fonts & dynamic fallback XMLs
           ├── 2. Scan active font files in /system, /product, /system_ext
           └── 3. Bind-mount SF Pro Heavy & iOS Emoji binaries
           │
[ Framework Boot: Zygote & System Server ]
           │
           └── FontManager loads replaced SF Pro typography into RAM
           │
[ Boot Completed: service.sh ]
           │
           ├── 1. Disable GMS background font updater services
           ├── 2. Lock Facebook & Messenger emoji caches (chattr +i)
           └── 3. Flush Gboard in-app cache
```

---

## 📦 Installation Guide

### Via Root Manager App (Recommended)
1. Download the latest `iOS_Bold_Font_Emoji_v2.0_Ultra.zip` from [Releases](https://github.com/sheikhmehraann/IOS-Emoji-Font/releases) or the `dist/` folder.
2. Open **Magisk**, **KernelSU**, or **APatch** Manager.
3. Navigate to the **Modules** tab.
4. Tap **Install from storage** and select the `.zip` archive.
5. Reboot your device after the installation completes.

### Via Command Line (Root Shell)
```bash
su -c magisk --install-module /sdcard/Download/iOS_Bold_Font_Emoji_v2.0_Ultra.zip
# Or for KernelSU / APatch
su -c ksu --install-module /sdcard/Download/iOS_Bold_Font_Emoji_v2.0_Ultra.zip
```

---

## 🔨 Building from Source

### Prerequisites
- Python 3.8 or newer
- Git

### Build Steps
```bash
# Clone the repository
git clone https://github.com/sheikhmehraann/IOS-Emoji-Font.git
cd IOS-Emoji-Font

# Build the ultra-compressed flashable ZIP
python build.py
```
The compiled flashable ZIP will be output to `dist/iOS_Bold_Font_Emoji_v2.0_Ultra.zip`.

---

## 📂 Project Architecture

```text
IOS-Emoji-Font/
├── .github/workflows/
│   └── release.yml                 # Automated CI/CD release workflow
├── assets/                          # Source binaries & base fonts
│   ├── META-INF/...                # Magisk update-binary & updater-script
│   └── system/fonts/
│       ├── NotoColorEmoji.ttf      # iOS 26.4 Apple Color Emoji binary (35 MB)
│       └── Roboto-Regular.ttf      # SF Pro Text Heavy binary (457 KB)
├── dist/
│   └── iOS_Bold_Font_Emoji_v2.0_Ultra.zip  # Compiled flashable module ZIP (~34 MB)
├── module/                          # Working module staging directory
│   ├── META-INF/com/google/android/
│   ├── system/fonts/
│   ├── action.sh                   # Magisk action button trigger
│   ├── customize.sh                # Flash-time expansion & terminal UI
│   ├── module.prop                 # Module identity & metadata
│   ├── post-fs-data.sh             # Early-boot dynamic bind-mount engine
│   └── service.sh                  # Boot-time daemon & cache lock
├── .gitattributes
├── .gitignore
├── build.py                         # Build automation compiler
├── LICENSE                          # MIT License
└── README.md
```

---

## ❓ Troubleshooting

### Emojis not showing in Messenger / Facebook
1. Open Magisk / KernelSU / APatch.
2. Under the module list, trigger the **Action** button on this module.
3. Force stop Messenger / Facebook, clear app cache from Settings, and reopen.

### Font reverted after a Google Play Services update
1. The built-in `service.sh` automatically suppresses `com.google.android.gms.fonts.provider.FontsProvider`.
2. A single device reboot will re-purge `/data/fonts` and restore SF Pro Heavy immediately.

---

## 📄 License & Credits

- **Author**: [sheikhmehraan](https://github.com/sheikhmehraann)
- **License**: [MIT License](LICENSE)
- **Font Assets**: Apple SF Pro & Apple Color Emoji

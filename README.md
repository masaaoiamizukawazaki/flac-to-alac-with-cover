# flac-to-alac-with-cover

📘 日本語版はこちら → [README_JP.md](README_JP.md)

Simple FLAC to ALAC converter using ffmpeg, with automatic cover art embedding.

> ⚠️ Created with the help of AI, and may lack polish or full error handling. Use at your own risk.

---

## Folder Structure Assumption

This tool assumes your audio files are organized like this:

```
FLAC/
└── Artist/
    └── Album/
        └── *.flac
```

Please select the top-level "FLAC" folder as the input.  
The output folder "ALAC" will be created with the same artist/album structure automatically:

```
ALAC/
└── Artist/
    └── Album/
        └── *.m4a
```

## Features

- ✅ Convert `.flac` to `.m4a` (ALAC) using `ffmpeg`
- ✅ Automatically skips up-to-date files
- ✅ Batch processing with folder structure preserved
- ✅ Fixes missing cover art by copying from FLAC to ALAC
- ✅ Detects non-FLAC files in source folder
- ✅ Simple GUI, no installation required (just run the `.exe`)

---

## How to Use

1. Download the latest release from [Releases](https://github.com/masaaoiamizukawazaki/flac-to-alac-with-cover/releases)
2. Extract the ZIP file
3. Run `FAC_FLAC_to_ALAC_Converter.exe`
4. Select:
   - `FLAC Folder`: the top-level folder described above
   - `Output Folder`: destination for `.m4a` files (auto-suggested)
5. Click:
   - `Start Conversion` to begin batch conversion
   - `Fix ALAC Cover Embedding` to copy missing artwork
   - `Check Non-FLAC Files` to list files not ending with `.flac`
6. You can click `Stop` during processing to cancel

---

## Requirements

- Windows 10/11 (64-bit)
- `ffmpeg.exe` is included in the package
- No Python installation needed (bundled as standalone `.exe`)

---

## License

This tool uses the following open source components:

- **FFmpeg** (LGPLv3/GPLv3): https://ffmpeg.org/
- **Mutagen** (GPLv2 or later): https://mutagen.readthedocs.io/

This software itself is licensed under **GNU GPL v2 or later**.  
See `LICENSE`, `COPYING.txt`, and other files for full terms.

---

## Support

If this tool helped you, feel free to support its development ☕  
👉 [Buy Me a Coffee](https://www.buymeacoffee.com/phantomincome)

> Even a small donation helps keep this work going. Thank you!

---

## Disclaimer

This tool is provided **as-is**, without warranty of any kind.  
I may not be able to fix bugs or provide support regularly.

Use at your own discretion.

# PyInstaller build file for the desktop app (Windows .exe folder, macOS .app).
#   pyinstaller VideoDownloader.spec --noconfirm
# Put an ffmpeg binary in vendor/ (vendor/ffmpeg.exe or vendor/ffmpeg) to bundle it.
import os
import sys

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

is_mac = sys.platform == "darwin"
ffmpeg_name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
ffmpeg_src = os.path.join("vendor", ffmpeg_name)
binaries = [(ffmpeg_src, ".")] if os.path.isfile(ffmpeg_src) else []
if not binaries:
    print(f"WARNING: {ffmpeg_src} not found - the app will be built without ffmpeg")

# yt-dlp and gallery-dl load their site extractors by name, so include them all.
hiddenimports = collect_submodules("yt_dlp") + collect_submodules("gallery_dl")

a = Analysis(
    ["desktop.py"],
    pathex=["."],
    binaries=binaries,
    datas=[("templates", "templates"), ("static", "static"),
           *collect_data_files("yt_dlp"), *collect_data_files("gallery_dl")],
    hiddenimports=hiddenimports,
    excludes=["tkinter"],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VideoDownloader",
    console=False,
    upx=False,
    argv_emulation=False,
    icon="assets/icon.ico",
)
coll = COLLECT(exe, a.binaries, a.datas, name="VideoDownloader", upx=False)

if is_mac:
    app = BUNDLE(
        coll,
        name="Video Downloader.app",
        icon="assets/icon.icns",
        bundle_identifier="app.videodownloader.desktop",
        info_plist={
            "CFBundleShortVersionString": "1.0.0",
            "NSHighResolutionCapable": True,
            "LSMinimumSystemVersion": "11.0",
        },
    )

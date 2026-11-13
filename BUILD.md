# Desktop app (Windows + macOS)

The desktop app is the same Flask app shown in a native window (pywebview),
packaged with PyInstaller. ffmpeg is bundled, so users don't install anything else.

## Run from source

```bash
pip install -r requirements-desktop.txt
python desktop.py
```

## Automatic builds (GitHub Actions)

`.github/workflows/desktop-build.yml` builds on every push to `main`:

| Build | Runner | Output |
|---|---|---|
| Windows 10/11 (64-bit) | windows-latest | `VideoDownloader-windows-x64.zip` |
| Mac with Apple Silicon (M1–M4) | macos-14 | `VideoDownloader-macos-arm64.dmg` |
| Mac with Intel chip | macos-15-intel | `VideoDownloader-macos-intel.dmg` |

Download them from the workflow run's **Artifacts** section. To publish a release,
push a tag: `git tag v1.0.0 && git push origin v1.0.0`; the files are then attached
to a GitHub Release.

## Build by hand

Put an ffmpeg binary at `vendor/ffmpeg.exe` (Windows) or `vendor/ffmpeg` (macOS), then:

```bash
pyinstaller VideoDownloader.spec --noconfirm
```

Output: `dist/VideoDownloader/VideoDownloader.exe` or `dist/Video Downloader.app`.
A Mac build has to be made on a Mac (or the GitHub macOS runner).

## Installing

- **Windows:** unzip and run `VideoDownloader.exe`. It is not code-signed, so
  SmartScreen may say "Windows protected your PC": click **More info → Run anyway**.
  The window uses Microsoft Edge WebView2, which Windows 10/11 already has.
- **macOS:** open the `.dmg` and drag the app to Applications. It is not notarized,
  so the first time **right-click the app → Open → Open** (or System Settings →
  Privacy & Security → **Open Anyway**). Removing the block for good needs an
  Apple Developer account ($99/year) to sign and notarize.

## Where the app keeps its files

Settings, `cookies.txt` and `logs/errors.log` are stored in:

- Windows: `%APPDATA%\VideoDownloader`
- macOS: `~/Library/Application Support/VideoDownloader`

When run from source (`python app.py` / `python desktop.py`) they stay in the project folder as before.

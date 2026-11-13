"""Desktop launcher: runs the Flask app on a private local port inside a native window.

Run from source:   python desktop.py
Build the app:     see BUILD.md (PyInstaller, Windows .exe and macOS .app/.dmg)
"""

import multiprocessing
import os
import socket
import subprocess
import sys
import threading


def run_gallery_dl_if_asked():
    """app.py starts gallery-dl as `sys.executable -m gallery_dl ...`.

    In the packaged app sys.executable is this program, so handle that call here
    instead of opening a second window.
    """
    if len(sys.argv) >= 3 and sys.argv[1:3] == ["-m", "gallery_dl"]:
        import gallery_dl
        sys.argv = ["gallery-dl", *sys.argv[3:]]
        sys.exit(gallery_dl.main())


def hide_console_windows():
    """Stop ffmpeg / gallery-dl from flashing a black console window on Windows."""
    if sys.platform != "win32" or not getattr(sys, "frozen", False):
        return
    original = subprocess.Popen.__init__

    def init(self, *args, **kwargs):
        kwargs["creationflags"] = kwargs.get("creationflags", 0) | subprocess.CREATE_NO_WINDOW
        original(self, *args, **kwargs)

    subprocess.Popen.__init__ = init


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    hide_console_windows()

    import webview
    from werkzeug.serving import make_server

    import app as backend

    backend.purge_old_jobs()
    port = free_port()
    server = make_server("127.0.0.1", port, backend.app, threaded=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    # Let "Save" buttons (send_file attachments) open a save dialog.
    webview.settings["ALLOW_DOWNLOADS"] = True
    # Links with target=_blank (e.g. "Open original post") go to the normal browser.
    webview.settings["OPEN_EXTERNAL_LINKS_IN_BROWSER"] = True

    webview.create_window(
        "Video Downloader",
        f"http://127.0.0.1:{port}/",
        width=1280,
        height=860,
        min_size=(900, 640),
    )
    try:
        webview.start(private_mode=False)  # keep theme choice etc. between runs
    finally:
        server.shutdown()
        os._exit(0)  # don't wait on background download threads


if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_gallery_dl_if_asked()
    main()

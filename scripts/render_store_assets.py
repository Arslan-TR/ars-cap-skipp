"""Render Chrome Web Store screenshots and promo tiles into docs/store/.

Serves the repo over a local HTTP server (the real extension/popup.html is shown
with a small chrome.* shim injected) and captures pages with headless Chrome.
Usage: python scripts/render_store_assets.py   (needs Pillow and Chrome)
"""
import functools
import http.server
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "store"
CANDIDATES = (
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
)
CHROME = next((p for p in CANDIDATES if p and Path(p).exists()), None)
SHIM = '<script src="/docs/store/src/shim.js"></script>'


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path.split("#")[0].split("?")[0].endswith("/extension/popup.html"):
            html = (ROOT / "extension" / "popup.html").read_text(encoding="utf-8")
            data = html.replace("</head>", SHIM + "</head>", 1).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()


JOBS = [  # (query, (width, height), output file)
    ("n=1", (1280, 800), "screenshot-1.jpg"),
    ("n=2", (1280, 800), "screenshot-2.jpg"),
    ("n=3", (1280, 800), "screenshot-3.jpg"),
    ("n=4", (1280, 800), "screenshot-4.jpg"),
    ("n=5", (1280, 800), "screenshot-5.jpg"),
    ("n=promo", (440, 280), "promo-440x280.jpg"),
    ("n=marquee", (1400, 560), "marquee-1400x560.jpg"),
]


def main():
    if not CHROME:
        sys.exit("Chrome not found; set CHROME_PATH")
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=str(ROOT)))
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for query, (w, h), name in JOBS:
            png = Path(tmp) / (name + ".png")
            subprocess.run(
                [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                 f"--user-data-dir={tmp}/profile", f"--window-size={w},{h + 120}", "--virtual-time-budget=4000",
                 f"--screenshot={png}", f"http://127.0.0.1:{port}/docs/store/src/slide.html?{query}&h={h}"],
                check=True, capture_output=True, timeout=120)
            im = Image.open(png).convert("RGB").crop((0, 0, w, h))  # RGB: no alpha channel
            im.save(OUT / name, "JPEG", quality=92, subsampling=0)
            print("wrote", OUT / name, im.size)
    srv.shutdown()


if __name__ == "__main__":
    main()

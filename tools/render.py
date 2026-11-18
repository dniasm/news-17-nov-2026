"""Render art/front.html to entry.png (1024x1024, at most 1 MiB).

Uses headless Microsoft Edge for the screenshot and Pillow to quantise it to a small palette PNG.
Run from the repository root:  python tools/render.py
"""
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
EDGE = os.environ.get("EDGE", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
LIMIT = 1048576


def main() -> None:
    src = (ROOT / "art" / "front.html").as_uri()
    with tempfile.TemporaryDirectory() as tmp:
        shot = Path(tmp) / "shot.png"
        subprocess.run(
            [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--user-data-dir={tmp}\\profile", "--window-size=1024,1024", f"--screenshot={shot}", src],
            check=True, capture_output=True, timeout=120,
        )
        # On Windows the msedge launcher can return before the headless browser writes the file.
        for _ in range(600):
            if shot.exists() and shot.stat().st_size > 0:
                time.sleep(0.5)
                break
            time.sleep(0.1)
        img = Image.open(shot).convert("RGB")
        img.load()
    if img.size != (1024, 1024):
        img = img.crop((0, 0, 1024, 1024))
    out = ROOT / "entry.png"
    img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out, optimize=True)
    size = out.stat().st_size
    w, h = Image.open(out).size
    print(f"wrote {out.name}: {w}x{h}, {size} bytes")
    if size > LIMIT or w > 1024 or h > 1024:
        sys.exit("entry.png breaks the size limits")


if __name__ == "__main__":
    main()

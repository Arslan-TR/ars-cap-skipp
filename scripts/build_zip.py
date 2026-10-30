"""Build the Chrome Web Store upload package from the runtime files in extension/.

Usage: python scripts/build_zip.py
Output: dist/ars-skipp-v<version>.zip  (manifest.json at the zip root)
"""
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "extension"
DIST = ROOT / "dist"
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
SKIP_SUFFIXES = {".map"}


def main():
    version = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))["version"]
    DIST.mkdir(exist_ok=True)
    out = DIST / f"ars-skipp-v{version}.zip"
    out.unlink(missing_ok=True)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(SRC.rglob("*")):
            if not path.is_file() or path.name in SKIP_NAMES or path.suffix in SKIP_SUFFIXES:
                continue
            z.write(path, path.relative_to(SRC).as_posix())
            count += 1
    print(f"{out}  {count} files  {out.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()

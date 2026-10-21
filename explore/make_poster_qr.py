"""Repository QR. Run: uv run --with segno==1.6.6 python explore/make_poster_qr.py"""

from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parents[1]
URL = "https://github.com/NaNIsaac/TraTT"

if __name__ == "__main__":
    out = ROOT / "figures" / "poster" / "qr_repo.png"
    segno.make_qr(URL, error="m").save(out, scale=12, border=4)
    print(f"wrote {out}: {URL}")

"""Generate scripts/fixtures/sample.pdf — a tiny 2-page PDF with extractable text
and one embedded raster figure (300x300), used by the dry-run + figure tests.
Run: .venv/bin/python scripts/fixtures/make_sample_pdf.py
"""
from pathlib import Path

import fitz  # pymupdf

OUT = Path(__file__).resolve().parent / "sample.pdf"


def main() -> None:
    doc = fitz.open()
    p1 = doc.new_page()
    p1.insert_text((72, 80), "Compound Flooding and Global Crop Loss: A Sample Paper",
                   fontsize=15)
    p1.insert_text((72, 110), "A. Researcher, B. Coauthor — Journal of Examples (2026)",
                   fontsize=10)
    p1.insert_text((72, 150),
                   "Abstract. This synthetic document exists only to exercise text and\n"
                   "figure extraction in the analyzer's dry-run path. It mentions floods,\n"
                   "inundation, precipitation, and remote sensing so heuristics have signal.",
                   fontsize=10)

    # An embedded raster figure (300x300, solid fill) on page 2.
    p2 = doc.new_page()
    p2.insert_text((72, 80), "Figure 1. A representative figure.", fontsize=11)
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 300, 300))
    pix.set_rect(pix.irect, (40, 90, 160))
    p2.insert_image(fitz.Rect(72, 110, 372, 410), pixmap=pix)

    doc.save(OUT)
    doc.close()
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""analyze_paper.py — turn an interesting paper PDF into a grounded research insight.

For each new/changed ``interest/<slug>/paper.pdf`` this script:
  1. extracts the main text + light metadata (pymupdf),
  2. asks Claude (native PDF document input, guarded; else extracted text) for a
     5-section insight grounded in the author's own publications,
  3. on success writes ``interest/<slug>/paper.md`` (extracted text),
     a representative figure under ``assets/figures/<slug>/`` (best-effort),
     and ``_insights/<YYYY-MM-DD>-<slug>.md`` (the card), plus a ``.sha256`` guard.

Nothing is written for a paper whose insight fails to generate/validate (A5).

Usage:
  python scripts/analyze_paper.py                 # resolve new/changed PDFs (CI default)
  python scripts/analyze_paper.py PATH...         # specific paper.pdf paths
  python scripts/analyze_paper.py --all           # every interest/*/paper.pdf
  python scripts/analyze_paper.py --dry-run ...    # canned response, ZERO API spend
  python scripts/analyze_paper.py --local ...      # REAL API call from a dev machine
  python scripts/analyze_paper.py --model ID       # override model id

CI never passes --local. ANTHROPIC_API_KEY comes from the environment only.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
INTEREST = REPO / "interest"
INSIGHTS = REPO / "_insights"
FIGURES = REPO / "assets" / "figures"
DATA = REPO / "_data"
PUBLISHED = REPO / "published"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PROJECT_HTML = REPO / "project.html"

DEFAULT_MODEL = os.environ.get("INSIGHTS_MODEL") or "claude-sonnet-4-6"

# Source-PDF links point at the committed PDF on GitHub, because interest/ is excluded
# from the built site (a same-origin /interest/... link would 404). Override via env.
REPO_BLOB_URL = (os.environ.get("REPO_BLOB_URL")
                 or "https://github.com/chrimerss/autopilot-research-insights/blob/main")

# Insight body: fixed order, JSON key -> H2 heading.
SECTION_ORDER = [
    ("summary_contributions", "Summary & Key Contributions"),
    ("connections_to_my_work", "Connections to My Work"),
    ("critique_limitations", "Critique & Limitations"),
    ("gaps_ideas", "Gaps & Ideas"),
    ("advance_disrupt", "How to Advance / Disrupt the Field"),
]
REQUIRED_KEYS = ["subject", "subject_slug", "topic"] + [k for k, _ in SECTION_ORDER]

# Figure thresholds (Fork B).
FIG_MIN_DIM = 200          # px, both width and height
FIG_MAX_DIM = 10000        # px per side — reject pathological/decompression-bomb images
FIG_MAX_AREA = 40_000_000  # ~40 MP ceiling
FIG_ASPECT_LO = 0.2        # w/h
FIG_ASPECT_HI = 5.0
FIG_PAGE_WINDOW = 8        # only look at the first N pages
FIG_RENDER_DPI = 150       # B1 page-render fallback DPI

# Claude / PDF guards (Fork A + E).
MAX_TOKENS = 4000
DOC_PAGE_LIMIT = 90                 # Anthropic native-PDF hard limit is ~100 pages
DOC_SIZE_LIMIT = 28 * 1024 * 1024   # ~32MB hard limit, with headroom
TOKENS_PER_PAGE_EST = 3000          # rough doc-token estimate per PDF page
CONTEXT_LIMIT = 180_000             # conservative usable context budget


def log(msg: str) -> None:
    print(f"[analyze] {msg}", file=sys.stderr)


def now_utc_date() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


# --------------------------------------------------------------------------- #
# Text normalization + publication grounding (AC-9)
# --------------------------------------------------------------------------- #
_STOPWORDS = {
    "a", "an", "the", "to", "of", "on", "for", "and", "in", "is", "with", "by",
    "at", "as", "from", "via", "new", "using", "over", "under", "into",
}


def normalize_title(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _content_tokens(s: str) -> set:
    """Distinctive tokens: normalized, minus stopwords and 1-2 char tokens (e.g.
    the 'f' in 'F-IDF'), so filler words don't dilute the overlap score."""
    return {t for t in normalize_title(s).split() if len(t) > 2 and t not in _STOPWORDS}


def title_match(text: str, known_titles: list[str]) -> bool:
    """True if `text` references any known publication: normalized-substring OR
    content-token containment (>= 0.6 of the title's distinctive tokens) — the
    substring path catches exact citations, containment catches light rewording."""
    if not known_titles:
        return False
    ntext = normalize_title(text)
    text_toks = _content_tokens(text)
    for title in known_titles:
        nt = normalize_title(title)
        if not nt:
            continue
        if nt in ntext:  # exact (normalized) citation — the dominant path
            return True
        title_toks = _content_tokens(title)
        if title_toks:
            containment = len(title_toks & text_toks) / len(title_toks)
            if containment >= 0.6:
                return True
    return False


def load_publications() -> list[dict]:
    path = DATA / "publications.yml"
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    return [p for p in data if isinstance(p, dict)]


def is_placeholder_mode(pubs: list[dict]) -> bool:
    if not pubs:
        return True
    titles = [str(p.get("title", "")) for p in pubs]
    return all(t.strip().upper().startswith("PLACEHOLDER") or not t.strip() for t in titles)


def _front_matter_title(body: str) -> str:
    if body.startswith("---"):
        parts = body.split("---", 2)
        if len(parts) >= 3:
            try:
                return str((yaml.safe_load(parts[1]) or {}).get("title", "")).strip()
            except Exception:
                return ""
    return ""


def load_history(pubs: list[dict]) -> tuple[str, list[str]]:
    """Build the grounding block + the list of known titles (AC-9 matcher input)."""
    lines = ["The author's selected publications (cite at least one by exact title):"]
    titles = []
    for p in pubs:
        t = str(p.get("title", "")).strip()
        if not t:
            continue
        titles.append(t)
        lines.append(f"- \"{t}\" — {p.get('authors','')} ({p.get('venue','')}, {p.get('year','')})")
    # Full-text excerpts (optional, truncated). Their titles also ground AC-9 so an
    # insight cited only against a published/-only paper is not wrongly rejected.
    if PUBLISHED.exists():
        for md in sorted(PUBLISHED.glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            body = md.read_text(encoding="utf-8", errors="ignore")
            ft = _front_matter_title(body)
            if ft:
                titles.append(ft)
            lines.append(f"\n[Full text excerpt: {md.stem}]\n{body[:4000]}")
    return "\n".join(lines), titles


def load_subjects() -> list[dict]:
    path = DATA / "subjects.yml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    return [s for s in data if isinstance(s, dict)]


# --------------------------------------------------------------------------- #
# Slug + PDF extraction
# --------------------------------------------------------------------------- #
def slugify_from(pdf_path: Path, title: str | None) -> str:
    from slugify import slugify  # python-slugify
    parent = pdf_path.parent.name
    if parent and parent != "interest":
        return slugify(parent)[:80] or "paper"
    base = slugify(title or "")[:80] if title else ""
    return base or "paper"


def extract_text(pdf_path: Path) -> dict:
    """Returns text, page_count, size, and best-effort metadata."""
    import fitz  # pymupdf

    doc = fitz.open(pdf_path)
    page_count = doc.page_count
    parts = [doc.load_page(i).get_text("text") for i in range(page_count)]
    text = "\n".join(parts)
    meta = doc.metadata or {}
    doc.close()

    title = (meta.get("title") or "").strip()
    if not title:
        # First substantial line on page 1.
        for line in parts[0].splitlines() if parts else []:
            line = line.strip()
            if len(line) > 12 and not line.lower().startswith(("doi", "http", "arxiv")):
                title = line
                break
    year = ""
    m = re.search(r"\b(19|20)\d{2}\b", text[:4000])
    if m:
        year = m.group(0)
    return {
        "text": text,
        "page_count": page_count,
        "size": pdf_path.stat().st_size,
        "title": title or pdf_path.parent.name,
        "authors": (meta.get("author") or "").strip(),
        "year": year,
        "venue": "",
    }


def extract_figure(pdf_path: Path, slug: str) -> str | None:
    """B2 (largest qualifying embedded raster) -> B1 (render a figure-bearing page)
    -> None. Returns a repo-relative path or None. Never raises."""
    try:
        import fitz

        doc = fitz.open(pdf_path)
        n = min(doc.page_count, FIG_PAGE_WINDOW)
        best = None  # (area, pixmap_bytes, ext)
        page_image_counts = []
        for i in range(n):
            page = doc.load_page(i)
            imgs = page.get_images(full=True)
            page_image_counts.append((i, len(imgs)))
            for img in imgs:
                xref = img[0]
                try:
                    pix = fitz.Pixmap(doc, xref)
                except Exception:
                    continue
                w, h = pix.width, pix.height
                if w < FIG_MIN_DIM or h < FIG_MIN_DIM:
                    continue
                if w > FIG_MAX_DIM or h > FIG_MAX_DIM or (w * h) > FIG_MAX_AREA:
                    continue  # decompression-bomb / pathological-image guard
                aspect = w / h if h else 0
                if not (FIG_ASPECT_LO <= aspect <= FIG_ASPECT_HI):
                    continue
                if pix.n - pix.alpha >= 4:  # CMYK -> RGB
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                area = w * h
                if best is None or area > best[0]:
                    best = (area, pix.tobytes("png"), "png")

        out_dir = FIGURES / slug
        if best is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / f"figure.{best[2]}"
            out.write_bytes(best[1])
            doc.close()
            return f"/assets/figures/{slug}/{out.name}"

        # B1 fallback: render the (non-first preferred) page with the most images.
        candidates = [pc for pc in page_image_counts if pc[1] > 0]
        if candidates:
            candidates.sort(key=lambda pc: (pc[1], pc[0] != 0), reverse=True)
            pidx = candidates[0][0]
            page = doc.load_page(pidx)
            pix = page.get_pixmap(dpi=FIG_RENDER_DPI)
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / "figure.png"
            out.write_bytes(pix.tobytes("png"))
            doc.close()
            return f"/assets/figures/{slug}/figure.png"

        doc.close()
        return None
    except Exception as e:  # never break the pipeline over a figure
        log(f"figure extraction failed for {slug}: {e}")
        return None


# --------------------------------------------------------------------------- #
# Claude call + JSON parsing
# --------------------------------------------------------------------------- #
SYSTEM_PROMPT = (
    "You are a research strategist assisting Zhi Li (Allen Li), a hydrology / "
    "remote-sensing / machine-learning-for-geoscience researcher. Respond with ONLY "
    "a single fenced ```json block matching the requested schema — no prose before or after."
)


def build_user_prompt(meta: dict, history: str, subjects: list[dict]) -> str:
    subj_lines = "\n".join(f"- {s['name']} (slug: {s['slug']}): {s.get('description','')}" for s in subjects)
    schema = {
        "subject": "one of the seeded subject names OR a new proposed name",
        "subject_slug": "kebab-case slug (reuse a seeded slug when it fits)",
        "subject_is_new": "boolean — true only if no seeded subject fits",
        "subject_description": "one line, only if subject_is_new",
        "topic": "short human-readable card title for THIS paper",
        "link": "the paper's DOI or canonical URL if present in the text, else empty string",
        "summary_contributions": "markdown",
        "connections_to_my_work": "markdown — MUST name >=1 of the author's listed publications by exact title",
        "critique_limitations": "markdown",
        "gaps_ideas": "markdown",
        "advance_disrupt": "markdown — a concrete plan to advance OR disrupt the field, naming recommended DATA and METHODS",
    }
    return (
        f"{history}\n\n"
        f"Seeded subjects (assign the best-fit slug; only propose a new one when none fits):\n{subj_lines}\n\n"
        f"Paper under review: \"{meta.get('title','')}\" "
        f"({meta.get('authors','')}, {meta.get('year','')}). The full paper is provided "
        f"(as a PDF document and/or extracted text).\n\n"
        "Write a research insight with these five parts, mapped 1:1 to the JSON keys, in order: "
        "Summary & Key Contributions -> Connections to My Work -> Critique & Limitations -> "
        "Gaps & Ideas -> How to Advance/Disrupt the Field (recommended data + methods).\n\n"
        "Respond with ONLY this fenced JSON object:\n"
        "```json\n" + json.dumps(schema, indent=2) + "\n```"
    )


def build_messages(meta: dict, paper_text: str, pdf_path: Path, history: str, subjects: list[dict]) -> list[dict]:
    """Native PDF document block when within both guards; else extracted text."""
    user_prompt = build_user_prompt(meta, history, subjects)
    content: list[dict] = []

    pages = meta.get("page_count", 0)
    size = meta.get("size", 0)
    est = pages * TOKENS_PER_PAGE_EST + len(history) // 4 + MAX_TOKENS
    within_hard = pages <= DOC_PAGE_LIMIT and size <= DOC_SIZE_LIMIT
    within_budget = est < CONTEXT_LIMIT

    if within_hard and within_budget:
        import base64
        b64 = base64.standard_b64encode(pdf_path.read_bytes()).decode("ascii")
        content.append({
            "type": "document",
            "source": {"type": "base64", "media_type": "application/pdf", "data": b64},
        })
    else:
        log(f"PDF too large for native input (pages={pages}, size={size}, est_tokens={est}); sending text.")
        content.append({"type": "text", "text": f"PAPER TEXT (extracted):\n{paper_text[:120000]}"})

    content.append({"type": "text", "text": user_prompt})
    return [{"role": "user", "content": content}]


def parse_fenced_json(raw: str) -> dict:
    """Extract the first fenced ```json block (tolerant of surrounding prose), else
    the first balanced {...} object. Raises ValueError on failure."""
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    candidate = m.group(1) if m else None
    if candidate is None:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = raw[start:end + 1]
    if candidate is None:
        raise ValueError("no JSON object found in reply")
    return json.loads(candidate)


def call_claude(messages: list[dict], model: str, dry_run: bool) -> dict:
    if dry_run:
        fixture = json.loads((FIXTURES / "sample_insight.json").read_text(encoding="utf-8"))
        return fixture

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY is not set; aborting (no partial writes).")

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    attempt_msgs = list(messages)
    last_err = None
    for attempt in range(2):  # one call + at most one retry-nudge
        resp = client.messages.create(
            model=model, max_tokens=MAX_TOKENS, system=SYSTEM_PROMPT, messages=attempt_msgs,
        )
        raw = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        try:
            return parse_fenced_json(raw)
        except (ValueError, json.JSONDecodeError) as e:
            last_err = e
            log(f"JSON parse failed (attempt {attempt+1}): {e}")
            attempt_msgs = list(messages) + [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": "Your last reply was not valid JSON. Reply with ONLY the fenced ```json object."},
            ]
    raise ValueError(f"Claude did not return valid JSON after retry: {last_err}")


# --------------------------------------------------------------------------- #
# Validation, subject resolution, rendering
# --------------------------------------------------------------------------- #
def validate(structured: dict) -> None:
    missing = [k for k in REQUIRED_KEYS if not str(structured.get(k, "")).strip()]
    if missing:
        raise ValueError(f"insight missing required keys: {missing}")


def subject_resolve(structured: dict, subjects: list[dict]) -> dict:
    """Normalize the returned slug and fuzzy-match it to a seeded subject to avoid
    near-duplicate tabs. Only a genuinely-new subject keeps subject_is_new=True."""
    from slugify import slugify

    existing = {s["slug"]: s for s in subjects}
    raw_slug = slugify(structured.get("subject_slug") or structured.get("subject") or "")
    if raw_slug in existing:
        structured["subject_slug"] = raw_slug
        structured["subject_is_new"] = False
        return structured
    # fuzzy: token overlap of subject name against seeded names
    nname = normalize_title(structured.get("subject", ""))
    ntoks = set(nname.split())
    for slug, s in existing.items():
        stoks = set(normalize_title(s["name"]).split())
        if stoks and len(stoks & ntoks) / len(stoks) >= 0.6:
            structured["subject_slug"] = slug
            structured["subject_is_new"] = False
            return structured
    structured["subject_slug"] = raw_slug or "misc"
    structured["subject_is_new"] = True
    return structured


def liquid_neutralize(s: str) -> str:
    """Escape the opening brace so no Liquid tag ({{ or {%) can form in LLM prose.
    HTML entities pass through kramdown and render as a literal '{' in the browser."""
    return (s or "").replace("{", "&#123;")


def render_insight_md(slug: str, structured: dict, meta: dict, figure_path: str | None) -> Path:
    front = {
        "subject": structured["subject"],
        "subject_slug": structured["subject_slug"],
        "topic": structured["topic"],
        "date": now_utc_date(),
        "title": meta.get("title", ""),
        "authors": meta.get("authors", ""),
        "year": meta.get("year", ""),
        "venue": meta.get("venue", ""),
        "link": structured.get("link", ""),
        "figure": figure_path or "",
        "source_pdf": f"{REPO_BLOB_URL}/interest/{slug}/paper.pdf",
    }
    fm = yaml.safe_dump(front, sort_keys=False, allow_unicode=True, default_flow_style=False)
    body = []
    for key, heading in SECTION_ORDER:
        body.append(f"## {heading}\n\n{liquid_neutralize(str(structured.get(key, '')).strip())}\n")
    INSIGHTS.mkdir(parents=True, exist_ok=True)
    out = INSIGHTS / f"{front['date']}-{slug}.md"
    out.write_text(f"---\n{fm}---\n\n" + "\n".join(body), encoding="utf-8")
    return out


def write_paper_md(slug: str, meta: dict) -> Path:
    front = {
        "title": meta.get("title", ""),
        "authors": meta.get("authors", ""),
        "year": meta.get("year", ""),
        "venue": meta.get("venue", ""),
    }
    fm = yaml.safe_dump(front, sort_keys=False, allow_unicode=True, default_flow_style=False)
    out = INTEREST / slug / "paper.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"---\n{fm}---\n\n{meta.get('text','')}", encoding="utf-8")
    return out


def update_subjects_if_new(structured: dict, subjects: list[dict]) -> bool:
    if not structured.get("subject_is_new"):
        return False
    slug = structured["subject_slug"]
    if any(s["slug"] == slug for s in subjects):
        return False
    subjects.append({
        "name": structured["subject"],
        "slug": slug,
        "description": structured.get("subject_description", ""),
    })  # appended LAST -> deterministic tab order
    (DATA / "subjects.yml").write_text(
        yaml.safe_dump(subjects, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return True


def update_sha_sidecar(slug: str, sha: str) -> Path:
    out = INTEREST / slug / ".sha256"
    out.write_text(sha + "\n", encoding="utf-8")
    return out


def successful_paths(slug: str, insight_md: Path, figure_path: str | None) -> list[str]:
    paths = [
        str(insight_md.relative_to(REPO)),
        f"interest/{slug}/paper.md",
        f"interest/{slug}/.sha256",
    ]
    if figure_path:
        paths.append(figure_path.lstrip("/"))
    return paths


def update_project_html(events: list[dict]) -> None:
    if not PROJECT_HTML.exists() or not events:
        return
    import html as _html

    page = PROJECT_HTML.read_text(encoding="utf-8")
    marker = "<!-- PROGRESS_ROWS -->"
    idx = page.rfind(marker)  # insert before the LAST marker (the table one, not any doc mention)
    if idx == -1:
        return
    rows = []
    for e in events:
        fig = (f'<br><img src="{_html.escape(e["figure"])}" alt="" style="max-width:160px">'
               if e.get("figure") else "")
        rows.append(
            f'<tr><td>{_html.escape(e["date"])}</td><td>{_html.escape(e["slug"])}</td>'
            f'<td>{_html.escape(e["subject"])}</td><td>{_html.escape(e["topic"])}{fig}</td></tr>'
        )
    page = page[:idx] + "\n".join(rows) + "\n" + page[idx:]
    PROJECT_HTML.write_text(page, encoding="utf-8")


# --------------------------------------------------------------------------- #
# Target resolution (Fork C)
# --------------------------------------------------------------------------- #
def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def insight_exists_for(slug: str) -> bool:
    return any(INSIGHTS.glob(f"*-{slug}.md")) if INSIGHTS.exists() else False


def _is_zero_sha(sha: str | None) -> bool:
    return not sha or set(sha) == {"0"}


def _pushed_pdfs(before_sha: str) -> set | None:
    """Repo-relative interest/**/paper.pdf paths changed in this push, or None if
    the diff can't be computed (then caller falls back to C3+hash)."""
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", before_sha, "HEAD"],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout
        return {ln.strip() for ln in out.splitlines() if ln.strip().endswith("/paper.pdf")}
    except Exception as e:
        log(f"git diff failed ({e}); using C3+hash only")
        return None


def select_targets(before_sha: str | None = None) -> list[Path]:
    if not INTEREST.exists():
        return []
    candidates = []
    for pdf in sorted(INTEREST.glob("*/paper.pdf")):
        slug = pdf.parent.name
        sha = sha256_of(pdf)
        sidecar = pdf.parent / ".sha256"
        prev = sidecar.read_text(encoding="utf-8").strip() if sidecar.exists() else None
        if (not insight_exists_for(slug)) or (prev != sha):
            candidates.append(pdf)

    # Push-diff scoping (C1) only when `before` is a real SHA (C9 sentinel check).
    if before_sha and not _is_zero_sha(before_sha):
        pushed = _pushed_pdfs(before_sha)
        if pushed is not None:
            candidates = [p for p in candidates if str(p.relative_to(REPO)) in pushed]
    return candidates


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def process_one(pdf: Path, model: str, dry_run: bool, pubs: list[dict],
                history: str, known_titles: list[str], subjects: list[dict],
                placeholder: bool) -> dict | None:
    meta = extract_text(pdf)
    slug = slugify_from(pdf, meta.get("title"))

    messages = build_messages(meta, meta["text"], pdf, history, subjects)
    structured = call_claude(messages, model, dry_run)
    validate(structured)
    structured = subject_resolve(structured, subjects)

    # AC-9 grounding: hard-fail in REAL mode if no real publication is named.
    if not title_match(structured.get("connections_to_my_work", ""), known_titles):
        if placeholder:
            log(f"[{slug}] WARNING: connections cite no known title (placeholder mode).")
        else:
            raise ValueError("AC-9: 'Connections to My Work' names no real publication; rejecting insight.")

    # Success path only (A5): now write figure + paper.md + insight + sidecar.
    figure_path = extract_figure(pdf, slug)
    insight_md = render_insight_md(slug, structured, meta, figure_path)
    write_paper_md(slug, meta)
    update_subjects_if_new(structured, subjects)
    update_sha_sidecar(slug, sha256_of(pdf))

    return {
        "slug": slug,
        "topic": structured["topic"],
        "subject": structured["subject"],
        "date": now_utc_date(),
        "figure": figure_path or "",
        "paths": successful_paths(slug, insight_md, figure_path),
    }


def _oneline(s: str) -> str:
    """Collapse any newline/whitespace so model text is safe in a single-line GHA
    output and cannot forge a heredoc terminator."""
    return " ".join(str(s).split())


def emit_github_output(events: list[dict]) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    add_paths = [p for e in events for p in e["paths"]]
    added_list = "\n".join(
        f"- {e['date']} — {_oneline(e['subject'])}: {_oneline(e['topic'])}" for e in events)
    if not events:
        summary = "no new insights"
    elif len(events) == 1:
        summary = _oneline(events[0]["topic"])
    else:
        summary = f"{len(events)} new insights"
    # Unique heredoc delimiter so model text can't forge the terminator; single-line
    # values (summary, count) are kept single-line so they can't inject extra keys.
    d = "GHA_EOF_b58f2c"
    with open(out, "a", encoding="utf-8") as f:
        f.write(f"add_paths<<{d}\n" + "\n".join(add_paths) + f"\n{d}\n")
        f.write(f"added_list<<{d}\n" + added_list + f"\n{d}\n")
        f.write(f"count={len(events)}\n")
        f.write(f"summary={summary}\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="specific interest/<slug>/paper.pdf paths")
    ap.add_argument("--all", action="store_true", help="process every interest/*/paper.pdf")
    ap.add_argument("--dry-run", action="store_true", help="canned response, zero API spend")
    ap.add_argument("--local", action="store_true", help="real API call from a dev machine")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="model id")
    args = ap.parse_args(argv)

    if args.paths:
        targets = [Path(p).resolve() for p in args.paths]
    elif args.all:
        targets = sorted(INTEREST.glob("*/paper.pdf"))
    else:
        targets = select_targets(os.environ.get("BEFORE_SHA"))

    if not targets:
        log("no new/changed papers to process.")
        emit_github_output([])
        return 0

    pubs = load_publications()
    placeholder = is_placeholder_mode(pubs)
    history, known_titles = load_history(pubs)
    subjects = load_subjects()
    log(f"mode={'PLACEHOLDER' if placeholder else 'REAL'} pubs; {len(targets)} target(s); model={args.model}")

    events, failures = [], 0
    for pdf in targets:
        try:
            ev = process_one(pdf, args.model, args.dry_run, pubs, history, known_titles, subjects, placeholder)
            if ev:
                events.append(ev)
                log(f"[{ev['slug']}] insight written ({ev['subject']}).")
        except Exception as e:  # one bad paper must not poison the batch
            failures += 1
            log(f"[{pdf.parent.name}] FAILED: {e}")

    update_project_html(events)
    emit_github_output(events)

    if events:
        return 0
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

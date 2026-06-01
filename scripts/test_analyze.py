"""Zero-API-spend unit tests for analyze_paper.py.

Run: .venv/bin/python -m unittest scripts.test_analyze -v
 (from the repo root, or: .venv/bin/python scripts/test_analyze.py)
"""
import json
import tempfile
import unittest
from pathlib import Path

import yaml

import importlib.util

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("analyze_paper", _HERE / "analyze_paper.py")
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)

FIX = _HERE / "fixtures"


class TestTitleMatch(unittest.TestCase):
    titles = [
        "Severe floods significantly reduce global rice yields",
        "Introducing Flashiness-Intensity-Duration-Frequency (F-IDF): A new metric to quantify flash flood intensity",
    ]

    def test_exact_substring(self):
        text = 'This extends "Severe floods significantly reduce global rice yields" at scale.'
        self.assertTrue(A.title_match(text, self.titles))

    def test_token_overlap(self):
        text = "The paper builds on the flashiness intensity duration frequency metric for flash flood intensity."
        self.assertTrue(A.title_match(text, self.titles))

    def test_no_match(self):
        text = "This paper is about quantum chromodynamics and lattice gauge theory."
        self.assertFalse(A.title_match(text, self.titles))

    def test_empty_known(self):
        self.assertFalse(A.title_match("anything", []))


class TestParseFencedJson(unittest.TestCase):
    def test_prose_around_fence(self):
        raw = (FIX / "raw_claude_reply.txt").read_text(encoding="utf-8")
        d = A.parse_fenced_json(raw)
        self.assertEqual(d["subject_slug"], "floods")
        self.assertIn("connections_to_my_work", d)

    def test_bare_object(self):
        d = A.parse_fenced_json('noise {"a": 1, "b": "x"} trailing')
        self.assertEqual(d["a"], 1)

    def test_no_json_raises(self):
        with self.assertRaises(ValueError):
            A.parse_fenced_json("there is no json here at all")


class TestLiquidNeutralize(unittest.TestCase):
    def test_kills_tags(self):
        out = A.liquid_neutralize("danger {{ evil }} and {% raw %} end")
        self.assertNotIn("{{", out)
        self.assertNotIn("{%", out)
        self.assertNotIn("{", out)
        self.assertIn("&#123;", out)


class TestRenderYamlSafe(unittest.TestCase):
    def test_nasty_title_roundtrips(self):
        structured = json.loads((FIX / "sample_insight.json").read_text(encoding="utf-8"))
        structured["topic"] = '- topic: with "quotes" & colon: chars'
        meta = {
            "title": 'Weird: A Title - with "quotes", colons: and {{liquid}}',
            "authors": "X: Y", "year": "2026", "venue": "Journal: of, Edge-Cases", "text": "body",
        }
        with tempfile.TemporaryDirectory() as td:
            A.INSIGHTS = Path(td)
            out = A.render_insight_md("nasty", structured, meta, None)
            raw = out.read_text(encoding="utf-8")
        # front matter parses and preserves the nasty values exactly
        _, fm, body = raw.split("---", 2)
        front = yaml.safe_load(fm)
        self.assertEqual(front["title"], meta["title"])
        self.assertEqual(front["topic"], structured["topic"])
        # five sections, and no raw liquid survived in the body
        self.assertEqual(body.count("## "), 5)
        self.assertNotIn("{{", body)
        self.assertNotIn("{%", body)


class TestFigureThresholds(unittest.TestCase):
    def test_embedded_figure_extracted(self):
        with tempfile.TemporaryDirectory() as td:
            A.FIGURES = Path(td)
            path = A.extract_figure(FIX / "sample.pdf", "sample")
            self.assertIsNotNone(path)
            f = Path(td) / "sample" / "figure.png"
            self.assertTrue(f.exists())
            import fitz
            pix = fitz.Pixmap(str(f))
            self.assertGreaterEqual(pix.width, A.FIG_MIN_DIM)
            self.assertGreaterEqual(pix.height, A.FIG_MIN_DIM)

    def test_text_only_pdf_returns_none(self):
        import fitz
        with tempfile.TemporaryDirectory() as td:
            A.FIGURES = Path(td)
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 72), "Text only, no figures here.", fontsize=12)
            p = Path(td) / "textonly.pdf"
            doc.save(str(p))
            doc.close()
            self.assertIsNone(A.extract_figure(p, "textonly"))


class TestSelectTargetsAndSentinel(unittest.TestCase):
    def test_zero_sha(self):
        self.assertTrue(A._is_zero_sha("0" * 40))
        self.assertTrue(A._is_zero_sha(None))
        self.assertTrue(A._is_zero_sha(""))
        self.assertFalse(A._is_zero_sha("abc123"))

    def test_idempotent_selection(self):
        import fitz
        with tempfile.TemporaryDirectory() as td:
            A.INTEREST = Path(td) / "interest"
            A.INSIGHTS = Path(td) / "_insights"
            A.INTEREST.mkdir(parents=True)
            A.INSIGHTS.mkdir(parents=True)
            slug_dir = A.INTEREST / "demo"
            slug_dir.mkdir()
            doc = fitz.open(); doc.new_page().insert_text((72, 72), "x"); doc.save(str(slug_dir / "paper.pdf")); doc.close()

            # 1) new paper, no insight -> selected
            self.assertEqual([p.parent.name for p in A.select_targets(None)], ["demo"])

            # 2) once an insight + matching sha sidecar exist -> not selected
            (A.INSIGHTS / "2026-01-01-demo.md").write_text("x", encoding="utf-8")
            (slug_dir / ".sha256").write_text(A.sha256_of(slug_dir / "paper.pdf"), encoding="utf-8")
            self.assertEqual(A.select_targets(None), [])

            # 3) edit the PDF bytes -> reselected once (sha differs)
            doc = fitz.open(); doc.new_page().insert_text((72, 72), "changed content"); doc.save(str(slug_dir / "paper.pdf")); doc.close()
            self.assertEqual([p.parent.name for p in A.select_targets(None)], ["demo"])


class TestFindPdf(unittest.TestCase):
    def test_prefers_paper_pdf(self):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td)
            (f / "paper.pdf").write_bytes(b"%PDF-small")
            (f / "SomeName.pdf").write_bytes(b"%PDF-bigger-than-the-other-one")
            self.assertEqual(A.find_pdf_in(f).name, "paper.pdf")

    def test_falls_back_to_any_pdf(self):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td)
            (f / "SWMManywhere.pdf").write_bytes(b"%PDF-x")
            self.assertEqual(A.find_pdf_in(f).name, "SWMManywhere.pdf")

    def test_none_when_no_pdf(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertIsNone(A.find_pdf_in(Path(td)))

    def test_select_targets_finds_named_pdf(self):
        import fitz
        with tempfile.TemporaryDirectory() as td:
            A.INTEREST = Path(td) / "interest"
            A.INSIGHTS = Path(td) / "_insights"
            (A.INTEREST / "SWMManywhere").mkdir(parents=True)
            A.INSIGHTS.mkdir(parents=True)
            doc = fitz.open(); doc.new_page().insert_text((72, 72), "x")
            doc.save(str(A.INTEREST / "SWMManywhere" / "SWMManywhere.pdf")); doc.close()
            picked = A.select_targets(None)
            self.assertEqual([p.name for p in picked], ["SWMManywhere.pdf"])
            self.assertEqual([p.parent.name for p in picked], ["SWMManywhere"])


class TestSubjectResolve(unittest.TestCase):
    subjects = [
        {"name": "Hydrology & Hydrologic Modeling", "slug": "hydrology"},
        {"name": "Floods & Inundation", "slug": "floods"},
    ]

    def test_existing_slug(self):
        out = A.subject_resolve({"subject": "Floods & Inundation", "subject_slug": "floods"}, list(self.subjects))
        self.assertEqual(out["subject_slug"], "floods")
        self.assertFalse(out["subject_is_new"])

    def test_fuzzy_match(self):
        out = A.subject_resolve({"subject": "Floods & Inundation", "subject_slug": "flood-inundation"}, list(self.subjects))
        self.assertEqual(out["subject_slug"], "floods")
        self.assertFalse(out["subject_is_new"])

    def test_new_subject(self):
        out = A.subject_resolve({"subject": "Quantum Sensing", "subject_slug": "quantum-sensing"}, list(self.subjects))
        self.assertTrue(out["subject_is_new"])
        self.assertEqual(out["subject_slug"], "quantum-sensing")


class TestGithubOutput(unittest.TestCase):
    def test_summary_single_line_no_injection(self):
        import os
        ev = [{"date": "2026-06-01", "subject": "Floods", "topic": "line one\nline two\ncount=0",
               "figure": "", "paths": ["_insights/2026-06-01-x.md", "interest/x/.sha256"]}]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "ghout"
            os.environ["GITHUB_OUTPUT"] = str(out)
            try:
                A.emit_github_output(ev)
            finally:
                del os.environ["GITHUB_OUTPUT"]
            text = out.read_text(encoding="utf-8")
        # summary is exactly one line, and the injected "count=0" did not become its own key
        summary_lines = [ln for ln in text.splitlines() if ln.startswith("summary=")]
        self.assertEqual(len(summary_lines), 1)
        self.assertNotIn("\ncount=0\n", "\n" + text)  # only the real count line exists
        self.assertIn("count=1", text)
        self.assertIn("add_paths<<", text)


class TestProjectHtmlEscaping(unittest.TestCase):
    def test_html_escaped(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "project.html"
            p.write_text("<table><tbody>\n<!-- PROGRESS_ROWS -->\n</tbody></table>", encoding="utf-8")
            A.PROJECT_HTML = p
            A.update_project_html([{"date": "2026-06-01", "slug": "x",
                                    "subject": "<script>alert(1)</script>", "topic": "a & b", "figure": ""}])
            out = p.read_text(encoding="utf-8")
        self.assertNotIn("<script>alert(1)</script>", out)
        self.assertIn("&lt;script&gt;", out)
        self.assertIn("a &amp; b", out)


class TestPublishedTitleGrounding(unittest.TestCase):
    def test_published_title_added(self):
        body = '---\ntitle: "A Unique Published Paper Title"\nyear: 2020\n---\n\nbody text'
        self.assertEqual(A._front_matter_title(body), "A Unique Published Paper Title")


class TestMakeClient(unittest.TestCase):
    def setUp(self):
        import os
        self._saved = {k: os.environ.get(k) for k in
                       ("INSIGHTS_PROVIDER", "AWS_REGION", "AWS_DEFAULT_REGION", "ANTHROPIC_API_KEY")}
        for k in self._saved:
            os.environ.pop(k, None)

    def tearDown(self):
        import os
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_bedrock_provider(self):
        import os
        from anthropic import AnthropicBedrock
        os.environ["INSIGHTS_PROVIDER"] = "bedrock"
        os.environ["AWS_REGION"] = "us-east-1"
        self.assertIsInstance(A.make_client(), AnthropicBedrock)  # no network call on construct

    def test_bedrock_without_region_raises(self):
        import os
        os.environ["INSIGHTS_PROVIDER"] = "bedrock"
        with self.assertRaises(SystemExit):
            A.make_client()

    def test_anthropic_provider(self):
        import os
        import anthropic
        os.environ["ANTHROPIC_API_KEY"] = "sk-ant-dummy"
        self.assertIsInstance(A.make_client(), anthropic.Anthropic)

    def test_anthropic_without_key_raises(self):
        with self.assertRaises(SystemExit):
            A.make_client()


class TestValidate(unittest.TestCase):
    def test_missing_key_raises(self):
        with self.assertRaises(ValueError):
            A.validate({"subject": "x", "subject_slug": "x"})  # missing topic + sections


if __name__ == "__main__":
    unittest.main(verbosity=2)

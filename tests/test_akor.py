"""Read-only Akor preflight safety and optional six-repository integration tests."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from akor.preflight import build, locate, review_html, save

SIBLINGS = Path(os.environ.get("AKOR_TEST_SIBLINGS", str(ROOT.parent)))
NAMES = ("ekole", "ekole-quebec", "Kontexte", "kompose", "Orgo", "Orgo_Worlds")


def sources_available() -> bool:
    try:
        return all(locate(SIBLINGS, n).is_dir() for n in NAMES)
    except FileNotFoundError:
        return False


class BasicTests(unittest.TestCase):
    def test_readme_is_english_utf8_and_nul_free(self):
        raw = (ROOT / "README.md").read_bytes()
        self.assertNotIn(b"\x00", raw)
        self.assertEqual(raw[-1:], b"\n")
        text = raw.decode("utf-8")
        self.assertIn("Learning in Concert", text)
        self.assertIn("children", text.lower())
        self.assertIn("not yet", text.lower())

    def test_review_escapes_untrusted_markup(self):
        sample = {
            "scenario": {"title": "<script>unsafe()</script>", "fiction": "<b>hi</b>"},
            "roles": [{"name": "<img src=x onerror=alert(1)>"}],
            "steps": [{"id": "step1", "role": "role", "instruction": "<svg onload=alert(1)>"}],
            "warnings": ["<script>warning()</script>"],
        }
        page = review_html(sample, {"checks": {"approval": {"ok": False}}})
        self.assertNotIn("<script>", page)
        self.assertNotIn("<img src=", page)
        self.assertNotIn("<svg onload=", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("NON AUTORISÉE", page)

    def test_utf8_json_and_newline(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "report.json"
            save(dest, {"name": "Après", "valid": False})
            raw = dest.read_bytes()
            self.assertNotIn(b"\x00", raw)
            self.assertTrue(raw.endswith(b"\n"))
            self.assertEqual(json.loads(raw.decode("utf-8"))["name"], "Après")

    def test_missing_repositories_fails_without_output(self):
        with tempfile.TemporaryDirectory() as d:
            parent = Path(d)
            out = parent / "output"
            with self.assertRaises(FileNotFoundError):
                build(parent, out)
            self.assertFalse(out.exists())

    def test_no_mutating_injector_invocation_in_preflight(self):
        script = (ROOT / "src/akor/preflight.py").read_text(encoding="utf-8")
        self.assertNotIn("inject --apply", script)
        self.assertIn("'validate'", script)
        self.assertIn("'plan'", script)
        self.assertIn("'dispatch_allowed':False", script)
        self.assertIn("'may_publish_to_child':False", script)

    def test_windows_launchers_ascii_crlf_and_nul_free(self):
        for launcher in ROOT.glob("*.bat"):
            raw = launcher.read_bytes()
            self.assertNotIn(b"\x00", raw)
            raw.decode("ascii")
            self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))


@unittest.skipUnless(sources_available(), "Six sister repositories not found; set AKOR_TEST_SIBLINGS")
class FullSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = tempfile.TemporaryDirectory(prefix="akor-preflight-")
        cls.output = Path(cls.work.name) / "output"
        cls.paths = {name: locate(SIBLINGS, name) for name in NAMES}
        cls.original = {
            "mission": (cls.paths["Kontexte"] / "data/missions/boulangerie.json").read_bytes(),
            "pack": (cls.paths["ekole-quebec"] / "pack.json").read_bytes(),
            "engine": (cls.paths["ekole"] / "launcher.py").read_bytes(),
        }
        cls.mission = json.loads(cls.original["mission"].decode("utf-8"))
        cls.result = build(SIBLINGS, cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.work.cleanup()

    def test_official_orgo_injector_validate_and_plan(self):
        self.assertTrue(self.result["checks"]["injecteur_orgo_validation"]["ok"])
        self.assertTrue(self.result["checks"]["injecteur_orgo_plan"]["ok"])
        self.assertTrue(self.result["checks"]["frontiere_worlds"]["ok"])

    def test_no_publication_or_dispatch(self):
        self.assertFalse(self.result["dispatch_allowed"])
        self.assertFalse(self.result["may_publish_to_child"])
        self.assertFalse(self.result["checks"]["alignement_pedagogique"]["ok"])
        self.assertEqual(self.result["course_sha256_count"], 202)

    def test_curriculum_mismatch_never_silently_corrected(self):
        self.assertEqual(self.result["source_courses"], ["qc-pri-ma-006"])
        self.assertEqual(self.result["target_course"], "qc-pri-ma-008")
        plan = json.loads((self.output / "artefacts/plan_kompose_enseignant.json").read_text("utf-8"))
        self.assertFalse(plan["curriculum"]["target_mapped"])

    def test_no_secret_fragment_text_in_generated_output(self):
        secrets = [fragment["content"]["fr-CA"] for fragment in self.mission["fragments"]]
        for f in self.output.rglob("*"):
            if f.is_file():
                content = f.read_text(encoding="utf-8")
                for secret in secrets:
                    self.assertNotIn(secret, content, f.name)

    def test_role_projections_are_not_authorizations(self):
        for rid in self.mission["roles"]:
            path = self.output / "artefacts" / f"apercu_role_{rid}_non_publie.json"
            view = json.loads(path.read_text("utf-8"))
            self.assertTrue(view["not_authorization"])
            self.assertNotIn("fragments", view)
            self.assertEqual(view["role_id"], rid)

    def test_source_repositories_are_unchanged(self):
        self.assertEqual(self.original["mission"], (self.paths["Kontexte"] / "data/missions/boulangerie.json").read_bytes())
        self.assertEqual(self.original["pack"], (self.paths["ekole-quebec"] / "pack.json").read_bytes())
        self.assertEqual(self.original["engine"], (self.paths["ekole"] / "launcher.py").read_bytes())

    def test_writing_into_source_tree_is_refused(self):
        dangerous = self.paths["Kontexte"] / "AKOR_MUST_NOT_WRITE"
        self.assertFalse(dangerous.exists())
        with self.assertRaises(ValueError):
            build(SIBLINGS, dangerous)
        self.assertFalse(dangerous.exists())


if __name__ == "__main__":
    unittest.main()

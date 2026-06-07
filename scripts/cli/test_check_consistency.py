import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from check_consistency import check


def make_repo(tmp, manifest, css, components, docs, index_imports):
    root = Path(tmp)
    (root / "css").mkdir()
    (root / "components").mkdir()
    (root / "docs").mkdir()
    for f in css:
        (root / "css" / f).write_text("/* x */")
    (root / "css" / "index.css").write_text(
        "\n".join(f'@import "{i}";' for i in index_imports))
    for f in components:
        (root / "components" / f).write_text("<html></html>")
    for f in docs:
        (root / "docs" / f).write_text("# x")
    (root / "docs" / "registry.json").write_text(json.dumps(manifest))
    return root


class TestCheck(unittest.TestCase):
    def test_clean_repo_has_no_problems(self):
        m = {"components": [
            {"id": "topbar", "title": "Topbar", "category": "component",
             "css": ["topbar.css"], "doc": ["topbar.md"], "html": ["topbar.html"]},
            {"id": "common", "title": "Common", "category": "infra",
             "css": ["common.css"], "doc": [], "html": []},
            {"id": "index", "title": "Index", "category": "infra",
             "css": ["index.css"], "doc": [], "html": []},
        ]}
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, m,
                             css=["topbar.css", "common.css"],
                             components=["topbar.html"],
                             docs=["topbar.md"],
                             index_imports=["common.css", "topbar.css"])
            result = check(root)
            self.assertEqual(result["errors"], [])

    def test_dangling_file_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = {"components": [
                {"id": "topbar", "title": "Topbar", "category": "component",
                 "css": ["topbar.css"], "doc": ["topbar.md"], "html": ["topbar.html"]},
                {"id": "index", "title": "Index", "category": "infra",
                 "css": ["index.css"], "doc": [], "html": []}]}
            root = make_repo(tmp, m, css=["topbar.css"], components=[],  # html missing!
                             docs=["topbar.md"], index_imports=["topbar.css"])
            result = check(root)
            self.assertTrue(any("topbar.html" in e for e in result["errors"]))

    def test_orphan_file_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = {"components": [
                {"id": "index", "title": "Index", "category": "infra",
                 "css": ["index.css"], "doc": [], "html": []}]}
            root = make_repo(tmp, m, css=["rogue.css"], components=[], docs=[],
                             index_imports=["rogue.css"])
            result = check(root)
            self.assertTrue(any("rogue.css" in e for e in result["errors"]))

    def test_missing_import_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = {"components": [
                {"id": "topbar", "title": "Topbar", "category": "component",
                 "css": ["topbar.css"], "doc": ["topbar.md"], "html": ["topbar.html"]},
                {"id": "index", "title": "Index", "category": "infra",
                 "css": ["index.css"], "doc": [], "html": []}]}
            root = make_repo(tmp, m, css=["topbar.css"], components=["topbar.html"],
                             docs=["topbar.md"], index_imports=[])  # topbar.css NOT imported
            result = check(root)
            self.assertTrue(any("topbar.css" in e and "index.css" in e
                                for e in result["errors"]))

    def test_demo_css_not_required_in_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = {"components": [
                {"id": "demo", "title": "Demo", "category": "infra",
                 "css": ["demo.css"], "doc": [], "html": []},
                {"id": "index", "title": "Index", "category": "infra",
                 "css": ["index.css"], "doc": [], "html": []}]}
            root = make_repo(tmp, m, css=["demo.css"], components=[], docs=[],
                             index_imports=[])  # demo not imported — OK
            result = check(root)
            self.assertEqual(result["errors"], [])

    def test_component_without_doc_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = {"components": [
                {"id": "coords", "title": "Coords", "category": "component",
                 "css": ["coords.css"], "doc": [], "html": []},
                {"id": "index", "title": "Index", "category": "infra",
                 "css": ["index.css"], "doc": [], "html": []}]}
            root = make_repo(tmp, m, css=["coords.css"], components=[], docs=[],
                             index_imports=["coords.css"])
            result = check(root)
            self.assertEqual(result["errors"], [])
            self.assertTrue(any("coords" in w for w in result["warnings"]))

    def test_file_claimed_by_two_entries_is_error(self):
        m = {"components": [
            {"id": "alpha", "title": "Alpha", "category": "component",
             "css": ["shared.css"], "doc": [], "html": []},
            {"id": "beta", "title": "Beta", "category": "component",
             "css": ["shared.css"], "doc": [], "html": []},
            {"id": "index", "title": "Index", "category": "infra",
             "css": ["index.css"], "doc": [], "html": []},
        ]}
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, m,
                             css=["shared.css"],
                             components=[],
                             docs=[],
                             index_imports=["shared.css"])
            result = check(root)
            self.assertTrue(any(
                "shared.css" in e and ("beansprucht" in e or "mehreren" in e)
                for e in result["errors"]
            ))


if __name__ == "__main__":
    unittest.main()

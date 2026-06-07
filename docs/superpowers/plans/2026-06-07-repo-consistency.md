# Repo-Konsistenz & Doku-Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ein Manifest-getriebenes Python-Check-Script, das css/↔components/↔docs/-Drift erkennt, die README-Übersicht generiert, eine verbindliche Registrierungs-Konvention etabliert und Altlasten entfernt.

**Architecture:** `docs/registry.json` ist Single Source of Truth (Feature→Dateien). `scripts/cli/check_consistency.py` validiert Manifest gegen die realen Dateien (Dangling/Orphan/Import/Kategorie) und kann mit `--write` die README-Abschnitte zwischen AUTOGEN-Markern rendern. Tests laufen hermetisch gegen temporäre Fixture-Verzeichnisse (stdlib `unittest`, keine Fremd-Dependencies).

**Tech Stack:** Python 3 (stdlib only: `json`, `pathlib`, `unittest`, `argparse`, `re`), bestehende Logger aus `scripts/cli/utils.py`.

---

## Datei-Struktur

- Create: `scripts/cli/check_consistency.py` — Validierung + README-Generierung. Pure Funktionen (`check`, `render_structure`, `render_status`, `write_readme`) + `main()`.
- Create: `scripts/cli/test_check_consistency.py` — `unittest`-Tests gegen Fixture-Dirs.
- Create: `docs/registry.json` — vollständiges Manifest aller Features.
- Modify: `README.md` — AUTOGEN-Marker einsetzen, Struktur/Status generieren lassen.
- Modify: `CLAUDE.md` — CSS loading order korrigieren + Konventions-Verweis.
- Modify: `docs/for-coding-agents.md` — Abschnitt „Neue Komponente registrieren".
- Modify: `.gitignore` — `.worktrees/`.
- Delete: `CI_FIXES_REPORT.md`.

**Wichtige Design-Entscheidung für das Script:** `check_consistency.py` und der Test fügen ihr eigenes Verzeichnis zu `sys.path` hinzu, damit `from utils import ...` bzw. `from check_consistency import ...` funktionieren, egal von wo gestartet wird.

---

### Task 1: Check-Core mit Validierung (TDD)

**Files:**
- Create: `scripts/cli/check_consistency.py`
- Test: `scripts/cli/test_check_consistency.py`

- [ ] **Step 1: Write the failing tests**

`scripts/cli/test_check_consistency.py`:

```python
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


BASE_MANIFEST = {"components": [
    {"id": "topbar", "title": "Topbar", "category": "component",
     "css": ["topbar.css"], "doc": ["topbar.md"], "html": ["topbar.html"]},
    {"id": "index", "title": "Index", "category": "infra",
     "css": ["index.css"], "doc": [], "html": []},
]}


class TestCheck(unittest.TestCase):
    def test_clean_repo_has_no_problems(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, BASE_MANIFEST,
                             css=["topbar.css"], components=["topbar.html"],
                             docs=["topbar.md"], index_imports=["common.css", "topbar.css"])
            # common.css referenced in index but listed? add it
            (root / "css" / "common.css").write_text("/* x */")
            BASE_MANIFEST["components"].append(
                {"id": "common", "title": "Common", "category": "infra",
                 "css": ["common.css"], "doc": [], "html": []})
            (root / "docs" / "registry.json").write_text(json.dumps(BASE_MANIFEST))
            result = check(root)
            BASE_MANIFEST["components"].pop()  # cleanup shared dict
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest discover -s scripts/cli -p 'test_*.py' -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'check_consistency'`

- [ ] **Step 3: Write minimal implementation**

`scripts/cli/check_consistency.py`:

```python
#!/usr/bin/env python3
"""OE5ITH CI — Konsistenz-Check zwischen Manifest und realen Dateien.

Validiert docs/registry.json gegen css/, components/, docs/ und generiert
optional die AUTOGEN-Abschnitte in README.md.

    python scripts/cli/check_consistency.py            # nur prüfen (read-only)
    python scripts/cli/check_consistency.py --write    # + README generieren
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from utils import log_header, log_success, log_warn, log_error, log_info

DIRS = {"css": ".css", "html": ".html", "doc": ".md"}
DIR_FOR_KIND = {"css": "css", "html": "components", "doc": "docs"}


def load_manifest(root: Path) -> dict:
    return json.loads((root / "docs" / "registry.json").read_text())


def _disk_files(root: Path, subdir: str, ext: str) -> set:
    d = root / subdir
    if not d.is_dir():
        return set()
    return {p.name for p in d.iterdir() if p.is_file() and p.name.endswith(ext)}


def check(root: Path) -> dict:
    """Return {'errors': [...], 'warnings': [...]} comparing manifest vs disk."""
    errors, warnings = [], []
    manifest = load_manifest(root)
    entries = manifest["components"]

    # Claimed files per kind
    claimed = {"css": {}, "html": {}, "doc": {}}
    for e in entries:
        for kind in DIRS:
            for fname in e.get(kind, []):
                if fname in claimed[kind]:
                    errors.append(
                        f"Datei '{fname}' wird von mehreren Einträgen beansprucht "
                        f"('{claimed[kind][fname]}' und '{e['id']}')")
                claimed[kind][fname] = e["id"]

    # 1. Dangling — manifest names a file that does not exist
    for kind, ext in DIRS.items():
        present = _disk_files(root, DIR_FOR_KIND[kind], ext)
        for fname, owner in claimed[kind].items():
            if fname not in present:
                errors.append(
                    f"Dangling: '{owner}' nennt {DIR_FOR_KIND[kind]}/{fname}, "
                    f"die Datei existiert nicht")

    # 2. Orphan — file on disk claimed by nobody
    for kind, ext in DIRS.items():
        present = _disk_files(root, DIR_FOR_KIND[kind], ext)
        for fname in sorted(present):
            if fname not in claimed[kind]:
                errors.append(
                    f"Orphan: {DIR_FOR_KIND[kind]}/{fname} ist in keinem "
                    f"registry.json-Eintrag registriert")

    # 3. Import-Check — every production css is imported in index.css
    index = root / "css" / "index.css"
    imported = set()
    if index.is_file():
        imported = set(re.findall(r'@import\s+"([^"]+)"', index.read_text()))
    for fname in sorted(claimed["css"]):
        if fname in ("index.css", "demo.css"):
            continue
        if fname not in imported:
            errors.append(f"Import fehlt: css/{fname} ist nicht in css/index.css importiert")

    # 4. Category rule — component without doc → warning
    for e in entries:
        if e.get("category") == "component" and not e.get("doc"):
            warnings.append(f"Komponente '{e['id']}' hat keine Doku (Dreiklang unvollständig)")

    return {"errors": errors, "warnings": warnings}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="OE5ITH CI Konsistenz-Check")
    parser.add_argument("--write", action="store_true",
                        help="README.md AUTOGEN-Abschnitte regenerieren")
    parser.add_argument("--root", default=None, help="Repo-Root (Default: auto)")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else repo_root()

    log_header("Repo-Konsistenz-Check")
    result = check(root)

    for w in result["warnings"]:
        log_warn(w)
    for e in result["errors"]:
        log_error(e)

    if args.write and not result["errors"]:
        write_readme(root, load_manifest(root))
        log_info("README.md AUTOGEN-Abschnitte aktualisiert")

    if result["errors"]:
        log_error(f"{len(result['errors'])} Fehler — Repo ist inkonsistent")
        return 1
    log_success("Manifest und Dateien sind konsistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Note: `write_readme`, `render_structure`, `render_status` werden in Task 3 ergänzt. Damit Step 4 hier läuft, füge vorerst einen Stub hinzu, der in Task 3 ersetzt wird:

```python
def write_readme(root, manifest):
    raise NotImplementedError  # implementiert in Task 3
```

Platziere den Stub oberhalb von `main()`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m unittest discover -s scripts/cli -p 'test_*.py' -v`
Expected: PASS (alle 6 Tests grün)

- [ ] **Step 5: Commit**

```bash
git add scripts/cli/check_consistency.py scripts/cli/test_check_consistency.py
git commit -m "feat(cli): add manifest-based consistency check core"
```

---

### Task 2: Vollständiges Manifest erstellen + gegen reales Repo prüfen

**Files:**
- Create: `docs/registry.json`

- [ ] **Step 1: Manifest mit dem vollständigen, verifizierten Inhalt anlegen**

`docs/registry.json` (deckt alle 18 css, 21 html, 32 docs jeweils genau einmal ab):

```json
{
  "components": [
    { "id": "topbar", "title": "Topbar", "category": "component",
      "css": ["topbar.css"], "doc": ["topbar.md"], "html": ["topbar.html"] },
    { "id": "sidebar", "title": "Sidebar + Accordion", "category": "component",
      "css": ["sidebar.css"], "doc": ["sidebar.md", "sidebar-types.md"],
      "html": ["sidebar.html", "sidebar-types.html"] },
    { "id": "cards", "title": "Cards", "category": "component",
      "css": ["cards.css"], "doc": ["cards.md"], "html": ["cards.html"] },
    { "id": "buttons", "title": "Buttons", "category": "component",
      "css": ["buttons.css"], "doc": ["buttons.md"],
      "html": ["buttons.html", "buttons-demo.html"] },
    { "id": "badges", "title": "Badges", "category": "component",
      "css": ["badges.css"], "doc": ["badges.md"], "html": ["badges.html"] },
    { "id": "page", "title": "Seitenstruktur", "category": "component",
      "css": ["page.css"], "doc": ["page.md", "page-types.md"],
      "html": ["page-types.html"] },
    { "id": "forms", "title": "Forms", "category": "component",
      "css": ["forms.css"], "doc": ["forms.md"], "html": ["forms.html"] },
    { "id": "modal", "title": "Modal + Karten-Popup", "category": "component",
      "css": ["modal.css"], "doc": ["modal.md"], "html": ["modal.html"] },
    { "id": "context-menu", "title": "Context-Menu + Action-Menu", "category": "component",
      "css": [], "doc": ["context-menu.md"], "html": ["context-menu.html"],
      "note": "CSS in modal.css/page.css" },
    { "id": "typography", "title": "Typografie", "category": "component",
      "css": ["typography.css"], "doc": ["typography.md"],
      "html": ["typography.html", "typography-preview.html"] },
    { "id": "calendar", "title": "Kalender", "category": "component",
      "css": ["calendar.css"], "doc": ["calendar.md"], "html": ["calendar.html"] },
    { "id": "code-viewer", "title": "Code-Viewer", "category": "component",
      "css": ["code-viewer.css"], "doc": ["code-viewer.md"], "html": ["code-viewer.html"] },
    { "id": "toast", "title": "Toast", "category": "component",
      "css": ["toast.css"], "doc": ["toast.md"], "html": ["toast.html"] },
    { "id": "coords", "title": "Koordinaten-Umrechner (Sidebar Typ 7)", "category": "component",
      "css": ["coords.css"], "doc": [], "html": [],
      "note": "Sidebar Typ 7; dokumentiert in sidebar-types.md" },
    { "id": "utils", "title": "Utility-Klassen", "category": "component",
      "css": ["utils.css"], "doc": [], "html": ["utils.html"],
      "note": "Zweckgebundene Utilities ohne eigene Spec" },
    { "id": "service-dashboard", "title": "Service-Dashboard", "category": "component",
      "css": ["service-dashboard.css"], "doc": ["service-dashboard.md"],
      "html": ["service-dashboard-overview.html", "service-dashboard-detail.html",
               "service-dashboard-config.html"] },

    { "id": "tokens", "title": "Tokens / Reset / Layout", "category": "infra",
      "css": ["common.css"], "doc": ["tokens.md"], "html": ["tokens.html"],
      "note": "common.css = Single Source of Truth" },
    { "id": "index", "title": "Master-Import", "category": "infra",
      "css": ["index.css"], "doc": [], "html": [],
      "note": "Importiert alle produktiven CSS" },
    { "id": "demo", "title": "Demo-/Preview-Styles", "category": "infra",
      "css": ["demo.css"], "doc": [], "html": [],
      "note": "Nur für components/*.html — nie produktiv" },

    { "id": "concepts", "title": "Begriffe", "category": "concept",
      "css": [], "doc": ["concepts.md"], "html": [] },
    { "id": "brand", "title": "Brand", "category": "concept",
      "css": [], "doc": ["brand.md"], "html": [] },
    { "id": "naming", "title": "Naming", "category": "concept",
      "css": [], "doc": ["naming.md"], "html": [] },
    { "id": "logo", "title": "Logo / Favicons", "category": "concept",
      "css": [], "doc": ["logo.md"], "html": [] },
    { "id": "usage", "title": "Usage / Einbindung", "category": "concept",
      "css": [], "doc": ["usage.md"], "html": [] },
    { "id": "for-coding-agents", "title": "Coding-Agent-Regeln", "category": "concept",
      "css": [], "doc": ["for-coding-agents.md"], "html": [] },
    { "id": "versioning", "title": "Versionierung", "category": "concept",
      "css": [], "doc": ["versioning.md"], "html": [] },
    { "id": "resources", "title": "Self-Hosting Ressourcen", "category": "concept",
      "css": [], "doc": ["resources.md"], "html": [] },
    { "id": "copyright", "title": "Lizenzen / Quellen", "category": "concept",
      "css": [], "doc": ["copyright.md"], "html": [] },
    { "id": "copyright-display", "title": "Copyright-Darstellung", "category": "concept",
      "css": [], "doc": ["copyright-display.md"], "html": [] },
    { "id": "cli", "title": "CLI Terminal", "category": "concept",
      "css": [], "doc": ["cli.md"], "html": [] },
    { "id": "roadmap", "title": "Roadmap", "category": "concept",
      "css": [], "doc": ["roadmap.md"], "html": [] },
    { "id": "map-legend", "title": "Map-Legend Overlay", "category": "concept",
      "css": [], "doc": ["map-legend.md"], "html": [],
      "note": "CSS in modal.css (.map-legend)" },
    { "id": "map-routes", "title": "Map-Route-Styles", "category": "concept",
      "css": [], "doc": ["map-routes.md"], "html": [],
      "note": "Kein CSS — JS-Konstanten" },
    { "id": "geocoder-dropdown", "title": "Geocoder-Dropdown", "category": "concept",
      "css": [], "doc": ["geocoder-dropdown.md"], "html": [],
      "note": "Nutzt forms.css" }
  ]
}
```

- [ ] **Step 2: Script gegen das reale Repo laufen lassen**

Run: `python scripts/cli/check_consistency.py`
Expected: Exit 0, „Manifest und Dateien sind konsistent". Warnungen für `coords` und `utils` (kein Doc) sind erwartet und akzeptiert.

Falls Orphan/Dangling-Fehler erscheinen: Manifest gegen die Fehlermeldung korrigieren (eine Datei wurde übersehen oder falsch benannt), bis Exit 0.

- [ ] **Step 3: Commit**

```bash
git add docs/registry.json
git commit -m "feat(docs): add registry.json manifest as single source of truth"
```

---

### Task 3: README-Generierung (`--write`)

**Files:**
- Modify: `scripts/cli/check_consistency.py`
- Test: `scripts/cli/test_check_consistency.py`

- [ ] **Step 1: Write the failing tests**

Ergänze in `scripts/cli/test_check_consistency.py` (Import oben erweitern und neue Testklasse anhängen):

```python
from check_consistency import render_structure, render_status, write_readme


class TestRender(unittest.TestCase):
    MANIFEST = {"components": [
        {"id": "topbar", "title": "Topbar", "category": "component",
         "css": ["topbar.css"], "doc": ["topbar.md"], "html": ["topbar.html"]},
        {"id": "brand", "title": "Brand", "category": "concept",
         "css": [], "doc": ["brand.md"], "html": []},
    ]}

    def test_structure_lists_files_grouped(self):
        out = render_structure(self.MANIFEST)
        self.assertIn("css/topbar.css", out)
        self.assertIn("docs/brand.md", out)
        self.assertIn("components/topbar.html", out)

    def test_status_table_marks_component_columns(self):
        out = render_status(self.MANIFEST)
        # Topbar has spec+html+css → three checkmarks
        self.assertIn("Topbar", out)
        self.assertIn("✅", out)
        # concept entries are not in the component status table
        self.assertNotIn("Brand", out)

    def test_write_readme_only_touches_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "Intro bleibt.\n"
                "<!-- AUTOGEN:structure START -->\nALT\n<!-- AUTOGEN:structure END -->\n"
                "Mitte bleibt.\n"
                "<!-- AUTOGEN:status START -->\nALT\n<!-- AUTOGEN:status END -->\n"
                "Schluss bleibt.\n")
            write_readme(root, self.MANIFEST)
            text = (root / "README.md").read_text()
            self.assertIn("Intro bleibt.", text)
            self.assertIn("Mitte bleibt.", text)
            self.assertIn("Schluss bleibt.", text)
            self.assertNotIn("ALT", text)
            self.assertIn("css/topbar.css", text)
            self.assertIn("Topbar", text)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest discover -s scripts/cli -p 'test_*.py' -v`
Expected: FAIL — `ImportError: cannot import name 'render_structure'`

- [ ] **Step 3: Replace the `write_readme` stub with the real implementation**

Ersetze in `scripts/cli/check_consistency.py` den Stub durch:

```python
def render_structure(manifest: dict) -> str:
    """Gruppierte Datei-Übersicht aus dem Manifest (deterministisch sortiert)."""
    buckets = {"css": [], "components": [], "docs": []}
    kind_dir = {"css": "css", "html": "components", "doc": "docs"}
    for e in manifest["components"]:
        for kind, sub in kind_dir.items():
            for fname in e.get(kind, []):
                buckets[sub].append(f"{sub}/{fname}")
    lines = ["```text"]
    for sub in ("css", "components", "docs"):
        for path in sorted(buckets[sub]):
            lines.append(path)
    lines.append("```")
    return "\n".join(lines)


def render_status(manifest: dict) -> str:
    """Status-Tabelle nur für category=component."""
    mark = lambda xs: "✅" if xs else "—"
    rows = ["| Element | Spec | Referenz-HTML | CSS |", "|---|---|---|---|"]
    for e in manifest["components"]:
        if e.get("category") != "component":
            continue
        rows.append(f"| {e['title']} | {mark(e.get('doc'))} | "
                    f"{mark(e.get('html'))} | {mark(e.get('css'))} |")
    return "\n".join(rows)


def _replace_block(text: str, name: str, body: str) -> str:
    pattern = re.compile(
        rf"(<!-- AUTOGEN:{name} START -->\n).*?(\n<!-- AUTOGEN:{name} END -->)",
        re.DOTALL)
    if not pattern.search(text):
        raise ValueError(f"AUTOGEN-Marker '{name}' nicht in README gefunden")
    return pattern.sub(lambda m: m.group(1) + body + m.group(2), text)


def write_readme(root: Path, manifest: dict) -> None:
    readme = root / "README.md"
    text = readme.read_text()
    text = _replace_block(text, "structure", render_structure(manifest))
    text = _replace_block(text, "status", render_status(manifest))
    readme.write_text(text)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m unittest discover -s scripts/cli -p 'test_*.py' -v`
Expected: PASS (alle 9 Tests grün)

- [ ] **Step 5: Commit**

```bash
git add scripts/cli/check_consistency.py scripts/cli/test_check_consistency.py
git commit -m "feat(cli): generate README structure & status from manifest"
```

---

### Task 4: README-Marker einsetzen + generieren

**Files:**
- Modify: `README.md`

- [ ] **Step 1: AUTOGEN-Marker in README einsetzen**

In `README.md` den handgepflegten Datei-Baum im Abschnitt `## Struktur` durch das Marker-Paar ersetzen (der gesamte ```text … ``` Block wird entfernt und ersetzt):

```html
<!-- AUTOGEN:structure START -->
<!-- AUTOGEN:structure END -->
```

Im Abschnitt `## Status` die handgepflegte Tabelle (von `| Element | Spec |` bis zur letzten Zeile) durch ersetzen:

```html
<!-- AUTOGEN:status START -->
<!-- AUTOGEN:status END -->
```

Den umgebenden Prosa-Text (Überschriften, Erklärungen) unverändert lassen.

- [ ] **Step 2: Generieren lassen**

Run: `python scripts/cli/check_consistency.py --write`
Expected: Exit 0, „README.md AUTOGEN-Abschnitte aktualisiert". Die Marker enthalten jetzt den generierten Datei-Baum bzw. die Status-Tabelle.

- [ ] **Step 3: Ergebnis prüfen**

Run: `git diff README.md`
Expected: Innerhalb der Marker steht der generierte Inhalt (inkl. der bislang fehlenden `calendar.css`, `code-viewer.css`, `coords.css`, `service-dashboard.css`, `toast.css`, `utils.css`); die `tokens.css`-Karteileiche taucht nicht mehr auf; Text außerhalb der Marker ist unverändert.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs(readme): generate structure & status from manifest"
```

---

### Task 5: CLAUDE.md korrigieren

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: CSS loading order aktualisieren**

In `CLAUDE.md`, Abschnitt „### CSS loading order", die Liste an die reale Reihenfolge aus `css/index.css` angleichen:

```markdown
1. `css/common.css` — tokens, reset, base layout (always first, always required)
2. `css/typography.css`, `css/badges.css`, `css/buttons.css`, `css/cards.css`
3. `css/topbar.css`, `css/sidebar.css`
4. `css/page.css`, `css/code-viewer.css`, `css/calendar.css`
5. `css/forms.css`, `css/coords.css`, `css/utils.css`, `css/modal.css`, `css/toast.css`
6. `css/service-dashboard.css`

Or use `css/index.css` to import all production components at once.
```

- [ ] **Step 2: Konventions-Verweis ergänzen**

Unter „## Mandatory rules for all changes" eine Regel anhängen:

```markdown
8. **Register new components** — every new component/feature needs an entry in `docs/registry.json`; run `python scripts/cli/check_consistency.py` and ensure it passes. See `docs/for-coding-agents.md`.
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude): sync CSS loading order and add registry rule"
```

---

### Task 6: Doku-Konvention in for-coding-agents.md

**Files:**
- Modify: `docs/for-coding-agents.md`

- [ ] **Step 1: Bestehende Struktur ansehen**

Run: `python scripts/cli/check_consistency.py` (sicherstellen, dass weiterhin grün) und `docs/for-coding-agents.md` lesen, um Ton/Überschriften-Ebene zu treffen.

- [ ] **Step 2: Abschnitt „Neue Komponente registrieren" anhängen**

Am Ende von `docs/for-coding-agents.md` ergänzen:

```markdown
## Neue Komponente registrieren

`docs/registry.json` ist die Single Source of Truth darüber, welche Dateien zu
welchem Feature gehören. Jede neue Komponente bzw. jedes neue Feature MUSS dort
eingetragen werden. Reihenfolge:

1. Eintrag in `docs/registry.json` (`id`, `title`, `category`, `css`/`doc`/`html`).
2. Spec in `docs/`.
3. Referenz-HTML in `components/`.
4. CSS in `css/` + `@import` in `css/index.css`.
5. `python scripts/cli/check_consistency.py` muss ohne Fehler durchlaufen.

Der Check prüft Dangling-Verweise, verwaiste Dateien, fehlende index.css-Imports
und den Dreiklang Spec→Referenz→CSS. `--write` regeneriert die README-Übersicht.

Kategorien: `component` (voller Dreiklang erwartet), `concept` (reine Doku),
`infra` (`common`, `index`, `demo`). Bewusste Lücken über leere Arrays + `note`
dokumentieren.
```

- [ ] **Step 3: Commit**

```bash
git add docs/for-coding-agents.md
git commit -m "docs(agents): add component registration convention"
```

---

### Task 7: Cleanup

**Files:**
- Delete: `CI_FIXES_REPORT.md`
- Modify: `.gitignore`

- [ ] **Step 1: Obsoleten Report löschen**

```bash
git rm CI_FIXES_REPORT.md
```

(Verifiziert obsolet: z-index-Tokens und `--topbar-height-mobile` existieren in `common.css`, keine hartcodierten z-index in `css/`.)

- [ ] **Step 2: `.worktrees/` ignorieren**

In `.gitignore` ergänzen:

```gitignore
# Git worktrees
.worktrees/
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: drop obsolete CI_FIXES_REPORT, ignore .worktrees"
```

---

### Task 8: Abschluss-Verifikation

- [ ] **Step 1: Voller Lauf**

Run: `python -m unittest discover -s scripts/cli -p 'test_*.py' -v && python scripts/cli/check_consistency.py`
Expected: Alle Tests PASS, Check Exit 0 „Manifest und Dateien sind konsistent".

- [ ] **Step 2: README-Idempotenz**

Run: `python scripts/cli/check_consistency.py --write && git diff --stat README.md`
Expected: Kein Diff (zweiter `--write`-Lauf erzeugt keine Änderung → Generierung ist stabil).

- [ ] **Step 3: Offene Doku-Änderung committen**

Run: `git status --short`
Falls `docs/topbar.md` noch uncommittete Änderungen hat:

```bash
git add docs/topbar.md
git commit -m "docs(topbar): pending edits"
```

---

## Hinweise zum Changelog

Nach Abschluss (separat, nicht Teil der Tasks): `CHANGELOG.md` unter `Added` (Konsistenz-Check + Manifest) und `Removed` (CI_FIXES_REPORT) ergänzen. Dies ist tooling-/doc-only — gemäß `docs/versioning.md` ein PATCH-Release, kein MINOR.

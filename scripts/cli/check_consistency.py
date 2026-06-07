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
        imported = set(re.findall(r'@import\s+["\']([^"\']+)["\']', index.read_text()))
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

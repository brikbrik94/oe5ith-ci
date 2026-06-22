# CI Map-Icons (SDF-Form-Quellen) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eine neue Asset-Kategorie im CI-Repo: einfarbige, über MapLibre `icon-color` umfärbbare SDF-Form-Quellen (Pins, Label-Bubbles, Marker, Symbole) als SVG + Manifest, plus Referenz-Galerie und Doku.

**Architecture:** Reine Asset-/Doku-Lieferung, kein Build-Schritt (das Sprite baut ein externes Submodul-Repo). SVG-Quellen + `icons.json`-Manifest liegen in `assets/map-icons/` (vom Konsistenz-Check nicht erfasst). Referenz-Galerie und Doku liegen in `components/`/`docs/` und werden in `registry.json` als Kategorie `asset` registriert.

**Tech Stack:** SVG (SDF-tauglich: monochrom, `fill="currentColor"`, gefüllte Flächen), JSON-Manifest, HTML5 + `css/demo.css` für die Galerie. Verifikation: Python-Einzeiler (XML/JSON-Validierung), `python3 scripts/cli/check_consistency.py`, Browser-Sichtprüfung.

## Global Constraints

- Nur **SDF-fähige, monochrome** Formen — keine Vollfarb-/Org-Icons in diesem Repo.
- Jede SVG: `fill="currentColor"`, gefüllte Flächen (keine reinen dünnen Striche), exakte `viewBox` je Kategorie, Safe-Area ≥ 4 px (Ausnahme: Pin-Spitze reicht bewusst bis nahe Unterkante = `anchor:bottom`), **keine** `<text>`/`<filter>`/`<image>`.
- Größenraster: marker/bubble `0 0 64 64`, pin `0 0 64 80`.
- Icon-IDs/Dateinamen: fester Präfix **`ci-`** (`ci-<name>.svg`), kollisionsfrei im gemeinsamen Sheet.
- **Keine neuen CSS-Tokens**; Recoloring nutzt bestehende Tokens (`--accent`, `--panel`, `--warning`, …).
- **Keine Build-Logik** in diesem Repo.
- `css/demo.css` nur in `components/map-icons.html`, nie produktiv.
- Registry-Eintrag Kategorie `asset` (nur `html`+`doc`, kein `css`); `check_consistency.py` muss grün bleiben — **keine** Script-Änderung nötig.
- Version: additiv → MINOR `v1.17.0`.
- Spec: `docs/superpowers/specs/2026-06-22-ci-map-icons-design.md`.

---

### Task 1: SVG-Form-Quellen

**Files:**
- Create: `assets/map-icons/ci-pin.svg`
- Create: `assets/map-icons/ci-pin-hole.svg`
- Create: `assets/map-icons/ci-bubble-label.svg`
- Create: `assets/map-icons/ci-marker-dot.svg`
- Create: `assets/map-icons/ci-marker-ring.svg`
- Create: `assets/map-icons/ci-symbol-location.svg`
- Create: `assets/map-icons/ci-symbol-warning.svg`

**Interfaces:**
- Produces: 7 SVG-Dateien mit exakt diesen Namen, `viewBox` und Geometrie. Task 2 (Manifest) und Task 3 (Galerie) referenzieren diese Dateien und betten ihren Inhalt ein. Die Bubble-Stretch-/Content-Koordinaten (Task 2) leiten sich aus dem Rechteck in `ci-bubble-label.svg` ab: rect `x=6 y=18 w=52 h=28 rx=8`.

- [ ] **Step 1: Die 7 SVGs schreiben (Inhalt exakt wie folgt)**

`assets/map-icons/ci-marker-dot.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="20" fill="currentColor"/></svg>
```

`assets/map-icons/ci-marker-ring.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path fill="currentColor" fill-rule="evenodd" d="M32 12a20 20 0 1 0 0 40 20 20 0 1 0 0-40ZM32 20a12 12 0 1 1 0 24 12 12 0 1 1 0-24Z"/></svg>
```

`assets/map-icons/ci-pin.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 80"><path fill="currentColor" d="M32 6C18.7 6 8 16.7 8 30c0 16 24 48 24 48s24-32 24-48C56 16.7 45.3 6 32 6Z"/></svg>
```

`assets/map-icons/ci-pin-hole.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 80"><path fill="currentColor" fill-rule="evenodd" d="M32 6C18.7 6 8 16.7 8 30c0 16 24 48 24 48s24-32 24-48C56 16.7 45.3 6 32 6ZM32 21a9 9 0 1 0 0 18 9 9 0 1 0 0-18Z"/></svg>
```

`assets/map-icons/ci-bubble-label.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="6" y="18" width="52" height="28" rx="8" fill="currentColor"/></svg>
```

`assets/map-icons/ci-symbol-location.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><g fill="currentColor"><path fill-rule="evenodd" d="M32 14a18 18 0 1 0 0 36 18 18 0 1 0 0-36ZM32 19a13 13 0 1 1 0 26 13 13 0 1 1 0-26Z"/><circle cx="32" cy="32" r="4"/><rect x="30" y="6" width="4" height="10" rx="1"/><rect x="30" y="48" width="4" height="10" rx="1"/><rect x="6" y="30" width="10" height="4" rx="1"/><rect x="48" y="30" width="10" height="4" rx="1"/></g></svg>
```

`assets/map-icons/ci-symbol-warning.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path fill="currentColor" fill-rule="evenodd" d="M32 8 57 53H7L32 8ZM29 24h6v16h-6zM32 43a3 3 0 1 0 0 6 3 3 0 1 0 0-6Z"/></svg>
```

- [ ] **Step 2: Wohlgeformtheit & Regeln verifizieren**

Run:
```bash
cd /root/git/oe5ith-ci && python3 - <<'PY'
import xml.dom.minidom, os
d="assets/map-icons"
expect={"ci-pin.svg":"0 0 64 80","ci-pin-hole.svg":"0 0 64 80",
        "ci-bubble-label.svg":"0 0 64 64","ci-marker-dot.svg":"0 0 64 64",
        "ci-marker-ring.svg":"0 0 64 64","ci-symbol-location.svg":"0 0 64 64",
        "ci-symbol-warning.svg":"0 0 64 64"}
for f,vb in expect.items():
    s=open(os.path.join(d,f)).read()
    xml.dom.minidom.parseString(s)                 # well-formed XML
    assert f'viewBox="{vb}"' in s, (f,"viewBox falsch/fehlt")
    assert 'currentColor' in s, (f,"kein currentColor")
    for bad in ('<text','<filter','<image'):
        assert bad not in s, (f,"verbotenes Element "+bad)
print("OK: alle 7 SVGs wohlgeformt, korrekte viewBox, currentColor, keine verbotenen Elemente")
PY
```
Expected: `OK: alle 7 SVGs …` und Exit 0.

- [ ] **Step 3: Optische Kurzkontrolle**

Run: die SVGs einzeln im Browser öffnen (oder Datei-Vorschau).
Expected: Marker-Punkt/Ring zentriert; Pin als Tropfen mit Spitze unten; Pin-mit-Loch zeigt kreisförmiges Loch im Kopf; Bubble = abgerundetes Rechteck; Location = Fadenkreuz mit Ring + Mittelpunkt; Warning = Dreieck mit ausgespartem Ausrufezeichen.

- [ ] **Step 4: Commit**

```bash
git add assets/map-icons/*.svg
git commit -m "feat(map-icons): add 7 SDF source shapes (pins, bubble, markers, symbols)"
```

---

### Task 2: Manifest `icons.json`

**Files:**
- Create: `assets/map-icons/icons.json`

**Interfaces:**
- Consumes: die 7 SVG-Dateien aus Task 1 (Namen, viewBox; Bubble-Rechteck `x=6 y=18 w=52 h=28 rx=8`).
- Produces: das Manifest = nach-außen-API für Builder und Konsumenten. Schema-Felder: `name, category, file, viewBox, anchor, sdf, recommendedColor` (alle) plus `stretchX, stretchY, content` (nur `category:"bubble"`).

- [ ] **Step 1: `assets/map-icons/icons.json` schreiben**

```json
{
  "version": 1,
  "grid": { "marker": [64, 64], "bubble": [64, 64], "pin": [64, 80] },
  "icons": [
    { "name": "ci-pin", "category": "pin", "file": "ci-pin.svg", "viewBox": [64, 80], "anchor": "bottom", "sdf": true, "recommendedColor": "--accent" },
    { "name": "ci-pin-hole", "category": "pin", "file": "ci-pin-hole.svg", "viewBox": [64, 80], "anchor": "bottom", "sdf": true, "recommendedColor": "--accent" },
    { "name": "ci-bubble-label", "category": "bubble", "file": "ci-bubble-label.svg", "viewBox": [64, 64], "anchor": "center", "sdf": true, "recommendedColor": "--panel", "stretchX": [[20, 44]], "stretchY": [[28, 36]], "content": [12, 24, 52, 40] },
    { "name": "ci-marker-dot", "category": "marker", "file": "ci-marker-dot.svg", "viewBox": [64, 64], "anchor": "center", "sdf": true, "recommendedColor": "--accent" },
    { "name": "ci-marker-ring", "category": "marker", "file": "ci-marker-ring.svg", "viewBox": [64, 64], "anchor": "center", "sdf": true, "recommendedColor": "--accent" },
    { "name": "ci-symbol-location", "category": "symbol", "file": "ci-symbol-location.svg", "viewBox": [64, 64], "anchor": "center", "sdf": true, "recommendedColor": "--accent" },
    { "name": "ci-symbol-warning", "category": "symbol", "file": "ci-symbol-warning.svg", "viewBox": [64, 64], "anchor": "center", "sdf": true, "recommendedColor": "--warning" }
  ]
}
```

- [ ] **Step 2: Manifest gegen Platte + Schema verifizieren**

Run:
```bash
cd /root/git/oe5ith-ci && python3 - <<'PY'
import json, os
d="assets/map-icons"
m=json.load(open(os.path.join(d,"icons.json")))                 # valides JSON
files={e["file"] for e in m["icons"]}
disk={x for x in os.listdir(d) if x.endswith(".svg")}
assert files==disk, ("Manifest/Platte weichen ab:", files ^ disk)
tokens={"--accent","--panel","--warning"}
for e in m["icons"]:
    assert os.path.exists(os.path.join(d,e["file"])), e["file"]
    assert set(("name","category","file","viewBox","anchor","sdf","recommendedColor")) <= set(e), e["name"]
    assert e["sdf"] is True, e["name"]
    assert e["recommendedColor"] in tokens, (e["name"], e["recommendedColor"])
    if e["category"]=="bubble":
        assert {"stretchX","stretchY","content"} <= set(e), ("bubble ohne stretch:", e["name"])
    else:
        assert "stretchX" not in e and "content" not in e, ("nicht-bubble mit stretch:", e["name"])
print("OK: Manifest konsistent mit Platte und Schema (%d Icons)" % len(m["icons"]))
PY
```
Expected: `OK: Manifest konsistent … (7 Icons)` und Exit 0.

- [ ] **Step 3: Token-Namen existieren in common.css**

Run: `grep -E "^\s*--(accent|panel|warning):" css/common.css`
Expected: alle drei Tokens werden gefunden.

- [ ] **Step 4: Commit**

```bash
git add assets/map-icons/icons.json
git commit -m "feat(map-icons): add icons.json manifest (builder + consumer API)"
```

---

### Task 3: Referenz-Galerie `components/map-icons.html`

**Files:**
- Create: `components/map-icons.html`

**Interfaces:**
- Consumes: die 7 SVGs (Task 1, Markup verbatim eingebettet) und das Manifest (Meta-Angaben je Icon).
- Produces: eine Browser-Referenzseite mit Recoloring-Demo und Bubble-Stretch-Visualisierung.

- [ ] **Step 1: Galerie-Grundgerüst schreiben**

Erzeuge `components/map-icons.html` mit folgendem Kopf, CSS und Grid. Lädt `common.css` (Tokens) + `demo.css`. Die Recoloring-Demo nutzt CSS `color:` (Tokens) auf den `currentColor`-SVGs — **keine** hardcodierten Farben.

```html
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OE5ITH CI — Map-Icons (SDF)</title>
  <link rel="stylesheet" href="../css/common.css">
  <link rel="stylesheet" href="../css/demo.css">
  <style>
    .mi-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:16px; }
    .mi-card { background:var(--card-bg); border:1px solid var(--border); border-radius:var(--card-radius); padding:16px; }
    .mi-swatches { display:flex; gap:14px; align-items:flex-end; margin-bottom:10px; min-height:56px; }
    .mi-swatch svg { width:40px; height:auto; display:block; }
    .mi-swatch.accent  { color:var(--accent); }
    .mi-swatch.text    { color:var(--text); }
    .mi-swatch.warning { color:var(--warning); }
    .mi-name { font-family:var(--font-mono); color:var(--text); font-size:.85rem; }
    .mi-meta { color:var(--muted); font-size:.78rem; margin-top:2px; }
    /* Bubble-Stretch-Visualisierung */
    .mi-bubble-demo { position:relative; width:128px; }
    .mi-bubble-demo svg { width:128px; height:128px; color:var(--panel); display:block; }
    .mi-bubble-demo .content-box { position:absolute; outline:1px dashed var(--accent);
      /* content [12,24,52,40] im 64-Raster → ×2 für 128px-Darstellung */
      left:24px; top:48px; width:80px; height:32px; }
  </style>
</head>
<body>
  <h1>OE5ITH CI — Map-Icons (SDF)</h1>
  <p>Einfarbige, über MapLibre <code>icon-color</code> umfärbbare SDF-Form-Quellen.
     Jedes Icon wird hier in drei CI-Token-Farben (accent · text · warning) gezeigt —
     dieselbe Form, beliebige Farbe.</p>

  <div class="mi-grid">
    <!-- je Icon eine .mi-card; SVG-Markup verbatim aus Task 1 -->
    <div class="mi-card">
      <div class="mi-swatches">
        <span class="mi-swatch accent"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 80"><path fill="currentColor" d="M32 6C18.7 6 8 16.7 8 30c0 16 24 48 24 48s24-32 24-48C56 16.7 45.3 6 32 6Z"/></svg></span>
        <span class="mi-swatch text"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 80"><path fill="currentColor" d="M32 6C18.7 6 8 16.7 8 30c0 16 24 48 24 48s24-32 24-48C56 16.7 45.3 6 32 6Z"/></svg></span>
        <span class="mi-swatch warning"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 80"><path fill="currentColor" d="M32 6C18.7 6 8 16.7 8 30c0 16 24 48 24 48s24-32 24-48C56 16.7 45.3 6 32 6Z"/></svg></span>
      </div>
      <div class="mi-name">ci-pin</div>
      <div class="mi-meta">pin · 64×80 · anchor bottom</div>
    </div>
    <!-- … weitere Karten … -->
  </div>
</body>
</html>
```

- [ ] **Step 2: Je eine Karte pro Icon ergänzen**

Erstelle nach dem Muster aus Step 1 **genau eine `.mi-card` pro Icon** (insgesamt 7). Betten je Karte das jeweilige SVG-Markup aus Task 1 **dreimal** ein (in den drei `.mi-swatch`-Spans accent/text/warning) und setze `.mi-name`/`.mi-meta` laut Manifest:

| Karte | mi-name | mi-meta |
|---|---|---|
| 1 | `ci-pin` | `pin · 64×80 · anchor bottom` |
| 2 | `ci-pin-hole` | `pin · 64×80 · anchor bottom` |
| 3 | `ci-bubble-label` | `bubble · 64×64 · anchor center · dehnbar` |
| 4 | `ci-marker-dot` | `marker · 64×64 · anchor center` |
| 5 | `ci-marker-ring` | `marker · 64×64 · anchor center` |
| 6 | `ci-symbol-location` | `symbol · 64×64 · anchor center` |
| 7 | `ci-symbol-warning` | `symbol · 64×64 · anchor center` |

- [ ] **Step 3: Bubble-Stretch-Abschnitt ergänzen**

Füge unter dem Grid einen Abschnitt ein, der das Stretch-/Content-Konzept zeigt — die Bubble vergrößert (128px) mit gestricheltem Content-Box-Overlay (`content [12,24,52,40]` → in 128px verdoppelt):

```html
  <h2>Dehnbarer Label-Hintergrund (<code>ci-bubble-label</code>)</h2>
  <p>Mit <code>icon-text-fit: both</code> dehnt MapLibre die Bubble auf die Textbreite.
     Gestrichelt: die Content-Box (<code>[12,24,52,40]</code>), in der der Text sitzt;
     gedehnt werden nur die Bereiche <code>stretchX [20,44]</code> / <code>stretchY [28,36]</code>.</p>
  <div class="mi-bubble-demo">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="6" y="18" width="52" height="28" rx="8" fill="currentColor"/></svg>
    <span class="content-box"></span>
  </div>
```

- [ ] **Step 4: Verifizieren**

Run:
```bash
cd /root/git/oe5ith-ci && grep -c "mi-card" components/map-icons.html
grep -nE "#[0-9a-fA-F]{3,6}|rgb" components/map-icons.html || echo "keine hardcodierten Farben"
```
Expected: `mi-card`-Count = 8 (1 Kommentar-/Muster-Erwähnung in Step 1 zählt nicht als Klasse — tatsächliche Karten = 7; akzeptiere ≥ 7) und „keine hardcodierten Farben". Zusätzlich im Browser öffnen: jedes Icon dreifarbig sichtbar (accent/text/warning), Pin-Loch erkennbar, Warning-Ausrufezeichen ausgespart, Bubble-Demo mit Content-Box-Rahmen.

- [ ] **Step 5: Commit**

```bash
git add components/map-icons.html
git commit -m "docs(map-icons): add reference gallery with recolor + stretch demo"
```

---

### Task 4: Doku `docs/map-icons.md`

**Files:**
- Create: `docs/map-icons.md`

**Interfaces:**
- Consumes: Katalog/Manifest/Geometrie aus Task 1+2.
- Produces: die verbindliche Doku (Konvention, Builder-Vertrag, Konsumenten-Snippet). Wird in Task 5 in `registry.json` als `doc` registriert.

- [ ] **Step 1: `docs/map-icons.md` schreiben**

Orientiere dich an `docs/split-view.md` (Kopf mit Status/CSS-Zeilen entfällt — kein CSS; stattdessen „Assets: `assets/map-icons/`"). Pflichtabschnitte (vollständig, sodass ein Agent ein neues Icon hinzufügen kann, ohne die HTML zu öffnen):

1. **Zweck & Abgrenzung** — nur generische SDF-Formen hier; Build + Org-Vollfarb-Icons extern (Spec §1).
2. **Verzeichnis** — `assets/map-icons/` (SVGs + `icons.json`), nicht vom Konsistenz-Check erfasst.
3. **Katalog-Tabelle** — alle 14 Icons aus Spec §8 mit Spalte „Release" (v1.17.0 / geplant). Markiere die 7 ausgelieferten.
4. **Namensschema** — `ci-<…>`, Datei = `<name>.svg`.
5. **Größensystem** — Tabelle marker/bubble `64×64`, pin `64×80`; Anker (pin=bottom, sonst center); ASCII-Skizze (Spec §5).
6. **SDF-Authoring-Regeln** — Spec §6 verbatim sinngemäß (currentColor, gefüllte Flächen, Safe-Area, keine text/filter/image).
7. **Manifest-Schema** — Feldtabelle aus Spec §3 inkl. Bubble-`stretchX/stretchY/content`.
8. **Recoloring** — `icon-color` + `recommendedColor`-Token; Konsument löst Token → Hex.
9. **Builder-Vertrag** — „scanne `assets/map-icons/*.svg`; alle SDF; Namen bereits `ci-`-präfixt; `stretchX/stretchY/content` aus `icons.json` ins `sprite.json` übernehmen."
10. **Konsumenten-Snippet** — MapLibre `addLayer` für `ci-pin` (icon-image/anchor/size + paint icon-color) und für `ci-bubble-label` (icon-text-fit:both + text-field), aus Spec §7.

- [ ] **Step 2: Vollständigkeit prüfen**

Run: `grep -nE "icon-color|icon-text-fit|assets/map-icons|stretchX|ci-pin|Builder" docs/map-icons.md`
Expected: alle Begriffe vorhanden (Builder-Vertrag, Recoloring, Stretch, Konsumenten-Snippet, Verzeichnis).

- [ ] **Step 3: Commit**

```bash
git add docs/map-icons.md
git commit -m "docs(map-icons): document conventions, builder contract, consumer usage"
```

---

### Task 5: Registry, CHANGELOG, README, Konsistenz-Check

**Files:**
- Modify: `docs/registry.json`
- Modify: `CHANGELOG.md`
- Modify: `README.md` (via `--write` autogeneriert)

**Interfaces:**
- Consumes: `components/map-icons.html` (Task 3), `docs/map-icons.md` (Task 4).
- Produces: registrierte Asset-Komponente + Changelog-Eintrag `v1.17.0` + synchronisiertes README; grüner Konsistenz-Check.

- [ ] **Step 1: Registry-Eintrag ergänzen**

Füge in `docs/registry.json` unter `"components"` hinzu (Kategorie `asset`, **kein** `css`):

```json
{
  "id": "map-icons",
  "title": "Map-Icons (SDF)",
  "category": "asset",
  "doc": ["map-icons.md"],
  "html": ["map-icons.html"]
}
```

- [ ] **Step 2: CHANGELOG ergänzen**

Trage in `CHANGELOG.md` **über** dem `## v1.16.0`-Block ein (Format der bestehenden Einträge):

```markdown
## v1.17.0 - 2026-06-22

### Added
- **Map-Icons (SDF)** — Neue Asset-Kategorie `assets/map-icons/`: einfarbige, über MapLibre `icon-color` umfärbbare SDF-Form-Quellen für Karten. Initialer Katalog (7): `ci-pin`, `ci-pin-hole`, `ci-bubble-label` (dehnbar), `ci-marker-dot`, `ci-marker-ring`, `ci-symbol-location`, `ci-symbol-warning`. Manifest `icons.json` (Builder- + Konsumenten-API inkl. Stretch-Zonen), Referenz `components/map-icons.html`, Doku `docs/map-icons.md`. Der Sprite-Build erfolgt extern (Submodul-Repo); keine neuen Tokens.

---
```

- [ ] **Step 3: Konsistenz-Check + README-Regeneration**

Run:
```bash
cd /root/git/oe5ith-ci
python3 scripts/cli/check_consistency.py
python3 scripts/cli/check_consistency.py --write
git diff --stat README.md
```
Expected: Check endet mit „✔ Manifest und Dateien sind konsistent", **keine** neue Warnung/Fehler durch `map-icons`. `--write` aktualisiert `README.md` (fügt `components/map-icons.html` + `docs/map-icons.md` in die Struktur-Liste ein). **Hinweis:** Der README-Diff enthält zusätzlich eine einmalige Nachführung der bestehenden Drift aus dem v1.16.0-Release (stats-explorer: `css/stats.css`, `components/stats-explorer.html`, `docs/page-stats.md` + Statuszeile „Statistik-Explorer") — das ist die korrekte AUTOGEN-Ausgabe und beabsichtigt.

- [ ] **Step 4: Final-Verifikation**

Run:
```bash
cd /root/git/oe5ith-ci
python3 -c "import json; d=json.load(open('docs/registry.json')); ids=[c['id'] for c in d['components']]; assert 'map-icons' in ids, ids; print('registry ok')"
grep -c "v1.17.0" CHANGELOG.md
python3 scripts/cli/check_consistency.py | tail -1
```
Expected: `registry ok`; `v1.17.0`-Count ≥ 1; letzte Zeile „✔ … konsistent".

- [ ] **Step 5: Commit**

```bash
git add docs/registry.json CHANGELOG.md README.md
git commit -m "docs(map-icons): register asset, changelog v1.17.0, sync README autogen"
```

---

## Release (nach Abschluss aller Tasks, auf ausdrückliche Freigabe)

```bash
git tag -a v1.17.0 -m "Release v1.17.0 — CI Map-Icons (SDF)"
git push origin main v1.17.0
```

---

## Notes für den Umsetzer

- **SVGs sind Baseline-Geometrie**, kein finaler Feinschliff der Bildmarke — sie erfüllen die SDF-/Größen-/Anker-Regeln und sind umfärbbar. Kunst-Verfeinerung ist später möglich, ohne IDs/viewBox zu ändern.
- **Pin-Anker:** `anchor:bottom` ankert an der Unterkante (32,80) des 64×80-Canvas; die Pin-Spitze reicht bewusst bis ~y=78. Das ist die einzige zulässige Safe-Area-Unterschreitung.
- **Kein JS/kein Build** in diesem Repo — der externe Builder konsumiert `assets/map-icons/` + `icons.json`.
- **README:** ist AUTOGEN; immer via `check_consistency.py --write` regenerieren, nie von Hand.

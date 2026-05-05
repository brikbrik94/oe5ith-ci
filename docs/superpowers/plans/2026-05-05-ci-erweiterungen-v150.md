# CI-Erweiterungen v1.5.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 8 additive CI-Erweiterungen umsetzen: neue Tokens, `css/utils.css`, `.overlay-section-label`, Referenzseite und Dokumentations-Updates.

**Architecture:** Alle Änderungen sind additiv — keine bestehenden Klassen oder Tokens werden geändert. `css/utils.css` ist eine neue zweckgebundene Utility-Datei ohne Abhängigkeiten außer `common.css`. Dokumentation wird inline in bestehende Docs-Dateien eingefügt.

**Tech Stack:** Vanilla CSS (Custom Properties), HTML5, Markdown

---

## Datei-Übersicht

| Datei | Aktion | Inhalt |
|---|---|---|
| `css/common.css` | Modify | `--sidebar-tab-width`, `--sidebar-tab-height` |
| `css/utils.css` | Create | `.full-map`, `.m-gap`, `.mb-gap`, `.flex-col`, `.flex-center` |
| `css/index.css` | Modify | `@import "utils.css"` |
| `css/sidebar.css` | Modify | `.overlay-section-label` |
| `components/utils.html` | Create | Referenzseite für alle Utils |
| `components/sidebar-types.html` | Modify | Demo-Sektion `.overlay-section-label` |
| `docs/tokens.md` | Modify | Tab-Maß-Tokens + Z-Index-Bereichstabelle |
| `docs/for-coding-agents.md` | Modify | No-Inline-Style-Regel für dynamische HTML-Strings |
| `CHANGELOG.md` | Modify | v1.5.0 |

---

## Task 1: Tokens in `css/common.css` ergänzen

**Files:**
- Modify: `css/common.css` — nach Zeile 30 (`--sidebar-tab-border`)

- [ ] **Step 1: Zwei neue Tokens einfügen**

  In `css/common.css` nach der Zeile `--sidebar-tab-border: rgba(59,130,246,0.35); /* Sidebar-Tab Border */` einfügen:

  ```css
  --sidebar-tab-width:  16px;                  /* Breite des Sidebar-Tab-Toggles */
  --sidebar-tab-height: 44px;                  /* Höhe des Sidebar-Tab-Toggles */
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep -n "sidebar-tab" css/common.css
  ```
  Erwartete Ausgabe: 4 Zeilen — `bg`, `border`, `width`, `height`.

- [ ] **Step 3: Commit**

  ```bash
  git add css/common.css
  git commit -m "feat: add --sidebar-tab-width/height tokens to common.css"
  ```

---

## Task 2: `css/utils.css` erstellen

**Files:**
- Create: `css/utils.css`

- [ ] **Step 1: Datei anlegen**

  Erstelle `css/utils.css` mit folgendem Inhalt:

  ```css
  /*
   * OE5ITH CI — utils.css
   * Zweckgebundene Utility-Klassen ohne Komponenten-Kontext.
   *
   * Abhängigkeit: css/common.css (Tokens)
   * Einbinden: css/index.css (automatisch über @import)
   */

  /* ═══════════════════════════════════════
     MAP UTILITIES
     ═══════════════════════════════════════ */

  /* Vollflächiger MapLibre/Leaflet-Container.
     Verhindert Layout-Sprünge: min-height:0 ist nötig
     damit Flex-Eltern die Höhe korrekt berechnen. */
  .full-map {
    flex: 1;
    height: 100%;
    min-height: 0;
    position: relative;
  }

  /* ═══════════════════════════════════════
     SPACING UTILITIES
     ═══════════════════════════════════════ */

  .m-gap  { margin: var(--card-gap); }
  .mb-gap { margin-bottom: var(--card-gap); }

  /* ═══════════════════════════════════════
     FLEX UTILITIES
     ═══════════════════════════════════════ */

  .flex-col    { display: flex; flex-direction: column; }
  .flex-center { display: flex; align-items: center; justify-content: center; }
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep -c "\." css/utils.css
  ```
  Erwartete Ausgabe: Zahl ≥ 5 (eine Zeile je Klasse).

- [ ] **Step 3: Commit**

  ```bash
  git add css/utils.css
  git commit -m "feat: add css/utils.css — map, spacing and flex utilities"
  ```

---

## Task 3: `css/index.css` — Import ergänzen

**Files:**
- Modify: `css/index.css`

- [ ] **Step 1: Import einfügen**

  In `css/index.css` nach `@import "coords.css";` einfügen:

  ```css
  @import "utils.css";
  ```

  Der Abschnitt „5. Interaktion" sieht danach so aus:

  ```css
  /* 5. Interaktion */
  @import "forms.css";
  @import "coords.css";
  @import "utils.css";
  @import "modal.css";
  @import "toast.css";
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep "utils" css/index.css
  ```
  Erwartete Ausgabe: `@import "utils.css";`

- [ ] **Step 3: Commit**

  ```bash
  git add css/index.css
  git commit -m "feat: register utils.css in index.css"
  ```

---

## Task 4: `.overlay-section-label` in `css/sidebar.css`

**Files:**
- Modify: `css/sidebar.css` — nach Zeile 40 (`.sidebar-section-label:first-child`)

- [ ] **Step 1: Klasse einfügen**

  In `css/sidebar.css` nach der Zeile `.sidebar-section-label:first-child { margin-top: 0; }` (aktuell Zeile 40) einfügen:

  ```css
  .overlay-section-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--subtle);
    margin-bottom: 5px;
    margin-top: 10px;
  }
  .overlay-section-label:first-child { margin-top: 0; }
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep -n "overlay-section-label" css/sidebar.css
  ```
  Erwartete Ausgabe: 2 Zeilen (Basis-Klasse + `:first-child`).

- [ ] **Step 3: Commit**

  ```bash
  git add css/sidebar.css
  git commit -m "feat: add .overlay-section-label to sidebar.css"
  ```

---

## Task 5: `components/utils.html` erstellen

**Files:**
- Create: `components/utils.html`

- [ ] **Step 1: Datei anlegen**

  Erstelle `components/utils.html` mit folgendem Inhalt:

  ```html
  <!DOCTYPE html>
  <html lang="de">
  <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CI Reference — Utils</title>
  <style>
  :root {
    --bg:#1a1a1a; --panel:#202020; --panel-deep:#161616;
    --text:#e0e0e0; --muted:#888; --subtle:#555; --border:#333;
    --accent:#3b82f6; --card-gap:20px;
    --font-sans:'Segoe UI',system-ui,sans-serif;
    --transition-fast:0.15s ease;
  }
  *,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
  body { font-family:var(--font-sans); background:var(--bg); color:var(--text); padding:40px; }

  .page-title { font-size:1.6rem; font-weight:300; color:#fff; margin-bottom:6px; }
  .page-title strong { font-weight:700; color:var(--accent); }
  .page-desc { font-size:0.85rem; color:var(--muted); margin-bottom:48px; max-width:640px; line-height:1.6; }

  .section { margin-bottom:56px; }
  .section-label {
    font-size:0.68rem; font-weight:700; letter-spacing:1.2px; text-transform:uppercase;
    color:var(--subtle); margin-bottom:6px; padding-bottom:8px; border-bottom:1px solid #222;
  }
  .section-desc { font-size:0.82rem; color:#444; margin-bottom:16px; line-height:1.6; }
  .annotation { font-size:0.8rem; color:var(--subtle); margin-top:10px; line-height:1.6; max-width:860px; }
  .annotation code { background:#1e1e1e; padding:1px 5px; border-radius:3px; font-family:monospace; font-size:0.75rem; color:#7ba8d4; }

  /* Demo-Boxen */
  .demo-box {
    background:var(--panel); border:1px solid var(--border); border-radius:6px;
    padding:20px; display:flex; gap:16px; flex-wrap:wrap; align-items:flex-start;
  }
  .demo-item {
    background:var(--panel-deep); border:1px dashed var(--border);
    border-radius:4px; padding:12px 16px;
    font-size:0.78rem; color:var(--muted);
  }
  .demo-label {
    font-size:0.6rem; font-weight:700; letter-spacing:0.8px; text-transform:uppercase;
    color:var(--subtle); margin-bottom:6px;
  }

  /* ── Utils (aus utils.css) ── */
  .full-map    { flex:1; height:100%; min-height:0; position:relative; }
  .m-gap       { margin:var(--card-gap); }
  .mb-gap      { margin-bottom:var(--card-gap); }
  .flex-col    { display:flex; flex-direction:column; }
  .flex-center { display:flex; align-items:center; justify-content:center; }
  </style>
  </head>
  <body>

  <div class="page-title">CI Reference — <strong>Utils</strong></div>
  <p class="page-desc">Zweckgebundene Utility-Klassen aus <code>css/utils.css</code>. Kein Komponenten-Kontext — direkt auf beliebige Elemente anwendbar.</p>

  <!-- .full-map -->
  <div class="section">
    <div class="section-label">.full-map</div>
    <div class="section-desc">Vollflächiger Container für MapLibre / Leaflet. <code>flex:1 · height:100% · min-height:0 · position:relative</code>. Verhindert Layout-Sprünge beim Initialisieren der Karte in einem Flex-Parent.</div>
    <div class="demo-box" style="height:120px; padding:0; overflow:hidden; border-radius:6px;">
      <div class="full-map" style="background:#2d3a2d; display:flex; align-items:center; justify-content:center;">
        <span style="font-size:0.7rem; color:rgba(255,255,255,0.2)">Karte füllt den verfügbaren Bereich</span>
      </div>
    </div>
    <p class="annotation">Auf das direkte Kind des <code>.layout</code>-Containers anwenden. Kein <code>width</code> oder <code>height</code> nötig — der Flex-Parent übernimmt die Steuerung.</p>
  </div>

  <!-- .m-gap / .mb-gap -->
  <div class="section">
    <div class="section-label">.m-gap / .mb-gap</div>
    <div class="section-desc">Abstand mit dem CI-Token <code>--card-gap</code> (20px). <code>.m-gap</code> rundherum, <code>.mb-gap</code> nur nach unten.</div>
    <div class="demo-box" style="flex-direction:column; gap:0; padding:0; background:transparent; border:none;">
      <div class="demo-item m-gap" style="background:var(--panel);">
        <div class="demo-label">.m-gap</div>
        margin: 20px (var(--card-gap)) rundherum
      </div>
      <div class="demo-item mb-gap" style="background:var(--panel);">
        <div class="demo-label">.mb-gap</div>
        margin-bottom: 20px (var(--card-gap))
      </div>
    </div>
  </div>

  <!-- .flex-col / .flex-center -->
  <div class="section">
    <div class="section-label">.flex-col / .flex-center</div>
    <div class="section-desc">Grundlegende Flex-Steuerung um <code>style="display:flex;..."</code> im HTML zu vermeiden.</div>
    <div class="demo-box">
      <div>
        <div class="demo-label">.flex-col</div>
        <div class="flex-col" style="gap:6px; background:var(--panel-deep); padding:12px; border-radius:4px; min-width:120px;">
          <div class="demo-item" style="padding:6px 10px;">Item 1</div>
          <div class="demo-item" style="padding:6px 10px;">Item 2</div>
          <div class="demo-item" style="padding:6px 10px;">Item 3</div>
        </div>
      </div>
      <div>
        <div class="demo-label">.flex-center</div>
        <div class="flex-center" style="width:140px; height:80px; background:var(--panel-deep); border-radius:4px;">
          <div class="demo-item" style="padding:6px 10px;">Zentriert</div>
        </div>
      </div>
    </div>
  </div>

  </body>
  </html>
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep -c "class=" components/utils.html
  ```
  Erwartete Ausgabe: Zahl ≥ 10.

- [ ] **Step 3: Commit**

  ```bash
  git add components/utils.html
  git commit -m "feat: add components/utils.html reference page"
  ```

---

## Task 6: `.overlay-section-label` Demo in `components/sidebar-types.html`

**Files:**
- Modify: `components/sidebar-types.html` — CSS im `<style>`-Block ergänzen + HTML-Sektion vor `</body>`

- [ ] **Step 1: CSS im `<style>`-Block einfügen**

  Nach dem Block `/* Tool Sep */` (nach `.btn-primary:hover { ... }`) die Klasse ergänzen. Suche nach dem Block:
  ```css
  /* ══════════════════════════════════════
     COORD-BLOCK (Typ 7)
  ```
  und füge DAVOR ein:

  ```css
  /* Overlay Section Label */
  .overlay-section-label {
    font-size:0.62rem; font-weight:700; letter-spacing:1.2px;
    text-transform:uppercase; color:var(--subtle);
    margin-bottom:5px; margin-top:10px;
  }
  .overlay-section-label:first-child { margin-top:0; }

  ```

- [ ] **Step 2: HTML-Demo-Sektion vor `</body>` einfügen**

  Direkt vor `</body>` (nach dem Typ-7-Block) einfügen:

  ```html

  <!-- ═══ OVERLAY-SECTION-LABEL ═══ -->
  <div class="section">
    <div class="section-label">Overlay Section Label</div>
    <div class="section-desc">Variante von <code>.sidebar-section-label</code> für schwebende Overlays (z.B. Topbar-Panels auf Tablet/Mobile). Gleiche Typografie, ohne den Sidebar-spezifischen Padding-Versatz.</div>
    <div class="screen" style="max-width:300px">
      <div style="background:var(--panel); padding:14px 12px; border-radius:6px;">
        <div class="overlay-section-label" style="margin-top:0">Navigation</div>
        <div class="sb-nav active"><i class="fa-solid fa-map"></i> Karte</div>
        <div class="sb-nav"><i class="fa-solid fa-list"></i> Liste</div>
        <div class="overlay-section-label">Werkzeuge</div>
        <div class="sb-nav"><i class="fa-solid fa-route"></i> Routing</div>
        <div class="sb-nav"><i class="fa-solid fa-location-dot"></i> Koordinaten</div>
      </div>
    </div>
    <p class="annotation">
      Verwendet <code>var(--subtle)</code> für die Farbe. <code>:first-child</code> entfernt den oberen Abstand automatisch.
      Kein <code>padding</code>-Versatz — passt in beliebige Container ohne Sidebar-Kontext.
    </p>
  </div>
  ```

- [ ] **Step 3: Prüfen**

  ```bash
  grep -c "overlay-section-label" components/sidebar-types.html
  ```
  Erwartete Ausgabe: ≥ 4 (CSS-Def × 2 + HTML-Verwendungen).

- [ ] **Step 4: Commit**

  ```bash
  git add components/sidebar-types.html
  git commit -m "feat: add .overlay-section-label demo to sidebar-types.html"
  ```

---

## Task 7: `docs/tokens.md` aktualisieren

**Files:**
- Modify: `docs/tokens.md`

- [ ] **Step 1: Tab-Maß-Tokens in Tabelle ergänzen**

  Nach der Zeile `| \`--sidebar-tab-border\` | \`rgba(59,130,246, 0.35)\` | Border des mobilen Sidebar-Tabs |` (Zeile 43) einfügen:

  ```markdown
  | `--sidebar-tab-width` | `16px` | Breite des Sidebar-Tab-Toggles |
  | `--sidebar-tab-height` | `44px` | Höhe des Sidebar-Tab-Toggles |
  ```

- [ ] **Step 2: Tab-Maß-Tokens im CSS-Block ergänzen**

  Im CSS-Code-Block in `docs/tokens.md` nach der Zeile `--sidebar-tab-border:  rgba(59,130,246,0.35);` (aktuell Zeile 165) einfügen:

  ```css
  --sidebar-tab-width:   16px;
  --sidebar-tab-height:  44px;
  ```

- [ ] **Step 3: Z-Index-Bereichstabelle ergänzen**

  Nach dem bestehenden Z-Index-Abschnitt (nach dem `> **Karten-Applikationen:** ...`-Hinweis, vor dem `---`) einfügen:

  ```markdown
  **Reservierte Bereiche:**

  | Bereich | Z-Index | Verwendung |
  |---|---|---|
  | App-Content | 0 – 999 | Site-spezifische Inhalte, Karten-Layer, App-Overlays |
  | CI-Overlays | 1000+ | Sidebar-Tab (1010) bis Toast (1600) |

  App-spezifische Z-Index-Werte dürfen 999 nicht überschreiten damit CI-Overlays immer oben bleiben.
  ```

- [ ] **Step 4: Änderungshistorie ergänzen**

  In der Tabelle `## Änderungshistorie` in `docs/tokens.md` eine neue Zeile einfügen:

  ```markdown
  | 2026-05-05 | `--sidebar-tab-width` und `--sidebar-tab-height` ergänzt. Z-Index-Bereichstabelle hinzugefügt. |
  ```

- [ ] **Step 5: Prüfen**

  ```bash
  grep -n "sidebar-tab-width\|sidebar-tab-height\|Reservierte Bereiche" docs/tokens.md
  ```
  Erwartete Ausgabe: je eine Zeile für beide Tokens + eine für den Abschnittstitel.

- [ ] **Step 6: Commit**

  ```bash
  git add docs/tokens.md
  git commit -m "docs: add sidebar-tab dimension tokens and z-index range table to tokens.md"
  ```

---

## Task 8: `docs/for-coding-agents.md` — No-Inline-Style Regel

**Files:**
- Modify: `docs/for-coding-agents.md` — Abschnitt `## JavaScript-Regeln`

- [ ] **Step 1: Regel ergänzen**

  In der Liste unter `## JavaScript-Regeln` nach der Zeile `- Keine Inline-Styles setzen, wenn eine CSS-Klasse ausreicht.` einfügen:

  ```markdown
  - Kein `style="..."` in dynamisch erzeugten HTML-Strings im JS/TS-Code. Ausnahme: Werte die erst zur Laufzeit berechnet werden können (z.B. Pixel-Positionen aus JS-Events, dynamische Breiten/Höhen aus Messungen). Für alle anderen Fälle: CI-Klassen verwenden.
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep -n "dynamisch\|HTML-String\|Laufzeit" docs/for-coding-agents.md
  ```
  Erwartete Ausgabe: die neue Regel-Zeile.

- [ ] **Step 3: Commit**

  ```bash
  git add docs/for-coding-agents.md
  git commit -m "docs: add no-inline-style rule for dynamic HTML strings to for-coding-agents.md"
  ```

---

## Task 9: `CHANGELOG.md` — v1.5.0

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Neuen Versionsblock vor `## v1.4.0` einfügen**

  Nach dem `---` Trenner (vor `## v1.4.0`) einfügen:

  ```markdown
  ## v1.5.0 - 2026-05-05

  ### Added

  - `css/utils.css` (neu): Utility-Klassen ohne Komponenten-Kontext.
    - `.full-map` — vollflächiger MapLibre/Leaflet-Container (`flex:1`, `height:100%`, `min-height:0`, `position:relative`).
    - `.m-gap` / `.mb-gap` — Abstände via `var(--card-gap)`.
    - `.flex-col` / `.flex-center` — grundlegende Flex-Steuerung.
  - `css/common.css`: `--sidebar-tab-width: 16px` und `--sidebar-tab-height: 44px` ergänzt.
  - `css/sidebar.css`: `.overlay-section-label` — Variante von `.sidebar-section-label` für schwebende Overlays.
  - `components/utils.html` — Referenzseite für alle Utils.
  - `components/sidebar-types.html`: `.overlay-section-label` Demo-Sektion.
  - `docs/tokens.md`: Z-Index-Bereichstabelle (0–999 App, 1000+ CI) und Tab-Maß-Token-Dokumentation.
  - `docs/for-coding-agents.md`: No-Inline-Style-Regel für dynamisch erzeugte HTML-Strings im JS/TS.

  ---

  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep -n "v1.5.0\|full-map\|utils.css" CHANGELOG.md | head -5
  ```
  Erwartete Ausgabe: `v1.5.0`-Zeile + mindestens 2 weitere Einträge.

- [ ] **Step 3: Commit**

  ```bash
  git add CHANGELOG.md
  git commit -m "chore: update CHANGELOG.md for v1.5.0"
  ```

---

## Abschluss-Checkliste

- [ ] `css/utils.css` mit 5 Klassen vorhanden
- [ ] `css/index.css` importiert `utils.css`
- [ ] `css/common.css` hat `--sidebar-tab-width` und `--sidebar-tab-height`
- [ ] `css/sidebar.css` hat `.overlay-section-label` und `:first-child` Variante
- [ ] `components/utils.html` zeigt alle 5 Utility-Klassen
- [ ] `components/sidebar-types.html` hat `.overlay-section-label` Demo
- [ ] `docs/tokens.md`: Tab-Tokens dokumentiert, Z-Index-Bereichstabelle vorhanden
- [ ] `docs/for-coding-agents.md`: No-Inline-Style-Regel für JS/TS vorhanden
- [ ] `CHANGELOG.md` v1.5.0 vorhanden
- [ ] 9 Commits, einer je Task

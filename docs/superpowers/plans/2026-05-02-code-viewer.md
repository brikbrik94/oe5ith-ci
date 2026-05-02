# Code-Viewer / API-Debugger Komponente — Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Neues `.panel-code` CI-Pattern für API-Debugger-Seiten — Terminal-artiger Code-Viewer mit Utility-Klassen `.mono` und `.ci-label`.

**Architecture:** Neue Datei `css/code-viewer.css` mit dem `.panel-code` Modifier und `.code-viewer-pre`. Utility-Klassen `.mono` und `.ci-label` kommen in `css/typography.css`. Keine neuen Tokens nötig — alle Werte aus `css/common.css` bereits vorhanden.

**Tech Stack:** Vanilla CSS, HTML5. Kein Build-Step. Kein JS für die Komponente selbst.

---

## Datei-Übersicht

| Aktion | Datei | Verantwortlich für |
|---|---|---|
| erstellen | `.gitignore` | `.superpowers/` und OS-Cruft ausschließen |
| erweitern | `css/typography.css` | Utility `.mono`, `.ci-label` |
| erstellen | `css/code-viewer.css` | `.panel-code`, `.code-viewer-pre`, `.form-row` |
| erweitern | `css/index.css` | Import von `code-viewer.css` |
| erstellen | `components/code-viewer.html` | Standalone Referenz-HTML |
| erstellen | `docs/code-viewer.md` | Komponentendokumentation |
| erweitern | `docs/tokens.md` | Hinweis: Code-Tokens auch für `panel-code` |
| erweitern | `docs/for-coding-agents.md` | API-Debugger Pattern |

---

## Task 1: `.gitignore` anlegen

**Files:**
- Create: `.gitignore`

- [ ] **Schritt 1: `.gitignore` erstellen**

```
# Superpowers visual companion sessions
.superpowers/

# macOS
.DS_Store

# Editor
.vscode/
*.swp
```

- [ ] **Schritt 2: Committen**

```bash
git add .gitignore
git commit -m "chore: add .gitignore"
```

---

## Task 2: Utility-Klassen in `css/typography.css`

**Files:**
- Modify: `css/typography.css` (ans Ende anhängen, nach Zeile 108)

**Kontext:** `typography.css` endet aktuell mit `.t-url` (Zeile 95–107). Darunter kommen die neuen Utilities.

- [ ] **Schritt 1: Block ans Ende von `css/typography.css` anhängen**

Diesen Block nach der letzten geschlossenen `}` von `.t-url` einfügen:

```css

/* ── Utilities ── */

/* Monospace-Schrift auf beliebige Elemente */
.mono {
  font-family: var(--font-mono);
}

/* Label außerhalb von .form-field — identisches Aussehen wie .form-label */
.ci-label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: var(--subtle);
}
```

- [ ] **Schritt 2: Visuell prüfen**

`components/tokens.html` im Browser öffnen — stellt sicher, dass `typography.css` noch korrekt geladen wird (keine CSS-Syntaxfehler).

- [ ] **Schritt 3: Committen**

```bash
git add css/typography.css
git commit -m "feat: add .mono and .ci-label utility classes to typography.css"
```

---

## Task 3: Neue Datei `css/code-viewer.css`

**Files:**
- Create: `css/code-viewer.css`

**Kontext:**
- `.panel-code` ist ein Modifier auf `.panel` (definiert in `page.css`). Er überschreibt Hintergrund, Border und den inneren `.panel-header`.
- `.code-viewer-pre` überschreibt die `pre`-Basisstyles aus `typography.css` (dort: `white-space: pre`, `overflow-x: auto`, kein `max-height`).
- `.form-row` ist ein horizontales Flex-Layout für Control-Panel-Inputs.

- [ ] **Schritt 1: `css/code-viewer.css` erstellen**

```css
/*
 * OE5ITH CI — code-viewer.css
 * Code-Viewer / API-Debugger Panel.
 *
 * Voraussetzung: css/common.css, css/page.css
 *
 * <link rel="stylesheet" href="css/common.css">
 * <link rel="stylesheet" href="css/page.css">
 * <link rel="stylesheet" href="css/code-viewer.css">
 */

/* ═══════════════════════════════════════
   PANEL-CODE
   Modifier auf .panel für Terminal-Charakter.
   Hintergrund: schwarz, Border: stark.
   ═══════════════════════════════════════ */
.panel-code {
  background: var(--code-bg);
  border-color: var(--border-strong);
}

.panel-code .panel-header {
  background: var(--panel-deep);
  border-bottom-color: var(--border-strong);
}

/* ═══════════════════════════════════════
   CODE-VIEWER-PRE
   Scrollbarer Code-Block innerhalb von .panel-code.
   Überschreibt pre-Basisstyles aus typography.css.
   ═══════════════════════════════════════ */
.code-viewer-pre {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--code-text);
  background: var(--code-bg);
  padding: 16px 20px;
  margin: 0;
  white-space: pre-wrap;
  line-height: 1.6;
  max-height: 600px;
  overflow: auto;
  border: none;
  border-radius: 0;
}

/* ═══════════════════════════════════════
   FORM-ROW
   Horizontales Flex-Layout für Control-Panel-Inputs.
   Elemente ausgerichtet an der Unterkante (flex-end)
   damit Buttons auf gleicher Höhe wie Inputs stehen.
   ═══════════════════════════════════════ */
.form-row {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}
```

- [ ] **Schritt 2: Import in `css/index.css` eintragen**

In `css/index.css` nach der Zeile `@import "page.css";` (Zeile 29) einen neuen Abschnitt 4a einfügen:

```css
/* 4a. Komponenten */
@import "code-viewer.css";
```

Die Datei soll danach so aussehen:

```css
/* 4. Seitenstruktur */
@import "page.css";

/* 4a. Komponenten */
@import "code-viewer.css";

/* 5. Interaktion */
@import "forms.css";
@import "modal.css";
@import "toast.css";
```

- [ ] **Schritt 3: Committen**

```bash
git add css/code-viewer.css css/index.css
git commit -m "feat: add code-viewer.css with .panel-code, .code-viewer-pre, .form-row"
```

---

## Task 4: Referenz-HTML `components/code-viewer.html`

**Files:**
- Create: `components/code-viewer.html`

Zeigt: Control Panel + Code Viewer (200 OK) + Code Viewer (404 Not Found).

- [ ] **Schritt 1: `components/code-viewer.html` erstellen**

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Code Viewer</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
:root {
  --bg:               #1a1a1a;
  --card-bg:          #252525;
  --panel:            #202020;
  --panel-deep:       #161616;
  --code-bg:          #000000;
  --code-text:        #4ade80;
  --text:             #e0e0e0;
  --muted:            #888888;
  --subtle:           #555555;
  --border:           #333333;
  --border-strong:    #444444;
  --accent:           #3b82f6;
  --accent-hover:     #2563eb;
  --accent-subtle:    rgba(59,130,246,0.07);
  --accent-subtle-md: rgba(59,130,246,0.10);
  --accent-border:    rgba(59,130,246,0.25);
  --success:          #22c55e;
  --danger:           #ef4444;
  --font-sans:        'Segoe UI', system-ui, sans-serif;
  --font-mono:        'JetBrains Mono', 'Consolas', 'Monaco', monospace;
  --card-radius:      12px;
  --card-padding:     20px;
  --btn-radius:       6px;
  --badge-radius:     4px;
  --transition-fast:  0.15s ease;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-sans); background: var(--bg); color: var(--text); min-height: 100vh; }

/* TOPBAR */
.topbar {
  background: var(--card-bg); height: 60px;
  border-bottom: 2px solid var(--accent);
  display: flex; align-items: center; padding: 0 20px;
  position: sticky; top: 0; z-index: 100;
}
.brand { font-weight: 700; font-size: 1.1rem; letter-spacing: 1px; color: #fff; }

/* DEMO LAYOUT */
.demo-body { padding: 32px 40px; display: flex; flex-direction: column; gap: 32px; max-width: 860px; }
.demo-section-label {
  font-size: 0.65rem; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase; color: var(--subtle); margin-bottom: 10px;
}

/* ── .panel (from page.css) ── */
.panel { background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--card-radius); overflow: hidden; }
.panel-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 10px 16px; border-bottom: 1px solid var(--border); }
.panel-title { display: flex; align-items: center; gap: 8px; font-size: 0.88rem; font-weight: 600; color: #fff; }
.panel-title i { font-size: 0.82rem; color: var(--accent); width: 16px; text-align: center; }
.panel-header-right { display: flex; align-items: center; gap: 8px; }
.panel-meta { font-size: 0.72rem; color: var(--subtle); white-space: nowrap; }
.panel-body { padding: 14px 16px; }

/* ── .panel-code (from code-viewer.css) ── */
.panel-code { background: var(--code-bg); border-color: var(--border-strong); }
.panel-code .panel-header { background: var(--panel-deep); border-bottom-color: var(--border-strong); }

/* ── .code-viewer-pre (from code-viewer.css) ── */
.code-viewer-pre {
  font-family: var(--font-mono); font-size: 0.78rem; color: var(--code-text);
  background: var(--code-bg); padding: 16px 20px; margin: 0;
  white-space: pre-wrap; line-height: 1.6; max-height: 600px; overflow: auto;
  border: none; border-radius: 0;
}

/* ── .form-row (from code-viewer.css) ── */
.form-row { display: flex; align-items: flex-end; gap: 12px; flex-wrap: wrap; }

/* ── .mono, .ci-label (from typography.css) ── */
.mono { font-family: var(--font-mono); }
.ci-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; color: var(--subtle); }

/* ── Forms (from forms.css) ── */
.form-field { display: flex; flex-direction: column; gap: 5px; }
.form-input {
  background: var(--panel-deep); border: 1px solid var(--border); border-radius: 5px;
  color: var(--text); font-size: 0.82rem; font-family: inherit;
  padding: 0 10px; height: 34px; outline: none;
  transition: border-color var(--transition-fast);
}
.form-input:focus { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(59,130,246,0.15); }
.form-select {
  background: var(--panel-deep); border: 1px solid var(--border); border-radius: 5px;
  color: var(--text); font-size: 0.82rem; font-family: inherit;
  padding: 0 30px 0 10px; height: 34px; outline: none; cursor: pointer;
  appearance: none; -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23555' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 10px center;
}
.form-select option { background: var(--panel-deep); color: var(--text); }

/* ── Badges (from badges.css) ── */
.badge { display: inline-flex; align-items: center; gap: 5px; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.4px; text-transform: uppercase; padding: 3px 8px; border-radius: 4px; border: 1px solid; white-space: nowrap; line-height: 1; }
.badge-green { background: rgba(34,197,94,0.10); color: #22c55e; border-color: rgba(34,197,94,0.25); }
.badge-red   { background: rgba(239,68,68,0.10);  color: #ef4444; border-color: rgba(239,68,68,0.25); }

/* ── Buttons (from buttons.css) ── */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 7px; height: 36px; padding: 0 16px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; font-family: inherit; cursor: pointer; border: none; white-space: nowrap; transition: background 0.15s; }
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: var(--accent-hover); }
.btn-ghost { background: transparent; color: var(--muted); border: 1px solid var(--border); }
.btn-ghost:hover { color: var(--text); border-color: #555; background: rgba(255,255,255,0.04); }
.btn-sm { height: 28px; padding: 0 10px; font-size: 0.75rem; border-radius: 5px; }
</style>
</head>
<body>

<div class="topbar">
  <span class="brand">OE5ITH CI — Code Viewer</span>
</div>

<div class="demo-body">

  <!-- ── 1. Control Panel ── -->
  <div>
    <p class="demo-section-label">1 — Control Panel (.panel + .form-row + .ci-label + .mono)</p>
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">
          <i class="fa-solid fa-sliders"></i>
          Abfrage-Parameter
        </div>
      </div>
      <div class="panel-body">
        <div class="form-row">
          <div class="form-field">
            <span class="ci-label">Dienst</span>
            <select class="form-select" style="min-width:160px">
              <option>Geocoding API</option>
              <option>Routing API</option>
              <option>Elevation API</option>
            </select>
          </div>
          <div class="form-field" style="flex:1;min-width:220px">
            <span class="ci-label">Parameter</span>
            <input class="form-input mono" type="text" placeholder="/api/geocode?q=Wien&amp;lang=de&amp;limit=1">
          </div>
          <button class="btn btn-primary">
            <i class="fa-solid fa-play"></i>
            Abfragen
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ── 2. Code Viewer — 200 OK ── -->
  <div>
    <p class="demo-section-label">2 — Code Viewer (.panel.panel-code) — Erfolg</p>
    <div class="panel panel-code">
      <div class="panel-header">
        <div class="panel-title">
          <i class="fa-solid fa-code"></i>
          API Response
        </div>
        <div class="panel-header-right">
          <span class="badge badge-green">200 OK</span>
          <span class="panel-meta">42 ms</span>
          <button class="btn btn-sm btn-ghost">
            <i class="fa-regular fa-copy"></i>
            Kopieren
          </button>
        </div>
      </div>
      <pre class="code-viewer-pre">{
  "status": "ok",
  "source": "nominatim",
  "lat": 48.2083,
  "lon": 16.3731,
  "display_name": "Wien, Österreich",
  "address": {
    "city": "Wien",
    "state": "Wien",
    "country": "Österreich",
    "country_code": "at"
  }
}</pre>
    </div>
  </div>

  <!-- ── 3. Code Viewer — 404 Not Found ── -->
  <div>
    <p class="demo-section-label">3 — Code Viewer (.panel.panel-code) — Fehlerfall</p>
    <div class="panel panel-code">
      <div class="panel-header">
        <div class="panel-title">
          <i class="fa-solid fa-code"></i>
          API Response
        </div>
        <div class="panel-header-right">
          <span class="badge badge-red">404 Not Found</span>
          <span class="panel-meta">11 ms</span>
          <button class="btn btn-sm btn-ghost">
            <i class="fa-regular fa-copy"></i>
            Kopieren
          </button>
        </div>
      </div>
      <pre class="code-viewer-pre">{ "error": "No results found for query" }</pre>
    </div>
  </div>

  <!-- ── 4. .mono als allgemeine Utility ── -->
  <div>
    <p class="demo-section-label">4 — .mono Utility auf verschiedenen Elementen</p>
    <div class="panel">
      <div class="panel-body" style="display:flex;flex-direction:column;gap:8px">
        <span>Normaler Text: <span style="color:var(--muted)">Segoe UI / system-ui</span></span>
        <span>Mit .mono: <span class="mono" style="color:var(--code-text);font-size:0.85rem">JetBrains Mono aktiv</span></span>
        <input class="form-input mono" type="text" value="/api/geocode?q=Linz" style="max-width:320px">
      </div>
    </div>
  </div>

</div>
</body>
</html>
```

- [ ] **Schritt 2: Im Browser öffnen und visuell prüfen**

```
open components/code-viewer.html
# oder: xdg-open components/code-viewer.html
```

Prüfen:
- Control Panel: horizontale Flex-Row mit `.ci-label` über jedem Feld, Parameter-Input in Mono-Schrift
- Code Viewer (Erfolg): schwarzer Hintergrund, grüner Text, Badge `200 OK` grün, Latenz rechts, Ghost-Button
- Code Viewer (Fehler): Badge `404 Not Found` rot
- `.mono` Demo: JetBrains Mono sichtbar unterschiedlich von Sans-Serif

- [ ] **Schritt 3: Committen**

```bash
git add components/code-viewer.html
git commit -m "feat: add code-viewer.html reference page"
```

---

## Task 5: Dokumentation `docs/code-viewer.md`

**Files:**
- Create: `docs/code-viewer.md`

- [ ] **Schritt 1: `docs/code-viewer.md` erstellen**

```markdown
# Code Viewer / API-Debugger

**CSS:** `css/code-viewer.css`  
**Referenz:** `components/code-viewer.html`  
**Status:** definiert · v1.1

---

## Überblick

Pattern für Seiten, die API-Antworten oder technische Rohdaten anzeigen.
Kombiniert ein Eingabe-Control-Panel (Standard `.panel`) mit einem Terminal-artigen
Code-Viewer-Panel (`.panel.panel-code`).

Seitentyp: **Typ 1 — Detail-Seite** (`docs/page-types.md`).

---

## Komponenten

### `.panel-code` — Code-Viewer-Panel

Modifier auf `.panel`. Überschreibt Hintergrund und Border für Terminal-Charakter.

**Tokens:**

| Token | Wert | Verwendung |
|---|---|---|
| `--code-bg` | `#000000` | Panel-Hintergrund und Pre-Hintergrund |
| `--code-text` | `#4ade80` | Text im `<pre>` |
| `--border-strong` | `#444444` | Panel-Border |
| `--panel-deep` | `#161616` | `.panel-header`-Hintergrund |

**HTML-Struktur:**

```html
<div class="panel panel-code">
  <div class="panel-header">
    <div class="panel-title">
      <i class="fa-solid fa-code"></i>
      API Response
    </div>
    <div class="panel-header-right">
      <span class="badge badge-green">200 OK</span>
      <span class="panel-meta">42 ms</span>
      <button class="btn btn-sm btn-ghost">
        <i class="fa-regular fa-copy"></i> Kopieren
      </button>
    </div>
  </div>
  <pre class="code-viewer-pre">{ "key": "value" }</pre>
</div>
```

**Badge-Varianten je HTTP-Status:**
- `badge-green` → 2xx Erfolg
- `badge-red` → 4xx / 5xx Fehler
- `badge-yellow` → 3xx Redirect

---

### `.code-viewer-pre` — Scrollbarer Code-Block

`<pre>`-Element innerhalb von `.panel-code`.

- `white-space: pre-wrap` — kein horizontales Scrollen bei langen Zeilen
- `max-height: 600px`, `overflow: auto` — lange Antworten sprengen die Seite nicht
- Font: `var(--font-mono)` / JetBrains Mono

---

### `.form-row` — Horizontales Control-Layout

Flex-Row für die Eingabefelder im Control-Panel.

```html
<div class="panel-body">
  <div class="form-row">
    <div class="form-field">
      <span class="ci-label">Dienst</span>
      <select class="form-select">...</select>
    </div>
    <div class="form-field">
      <span class="ci-label">Parameter</span>
      <input class="form-input mono" type="text">
    </div>
    <button class="btn btn-primary">Abfragen</button>
  </div>
</div>
```

---

### `.ci-label` — Label außerhalb von `.form-field`

Definiert in `css/typography.css`. Identisches Aussehen wie `.form-label`,
verwendbar außerhalb von Formular-Kontexten.

```html
<span class="ci-label">Dienst</span>
```

---

### `.mono` — Monospace-Font-Utility

Definiert in `css/typography.css`. Wendet `var(--font-mono)` auf beliebige Elemente an.

```html
<input class="form-input mono" type="text" placeholder="/api/...">
<span class="mono">technischer Text</span>
```

---

## Vollständiges Seiten-Beispiel

```html
<!-- Control Panel -->
<div class="panel">
  <div class="panel-header">
    <div class="panel-title">
      <i class="fa-solid fa-sliders"></i> Abfrage-Parameter
    </div>
  </div>
  <div class="panel-body">
    <div class="form-row">
      <div class="form-field">
        <span class="ci-label">Dienst</span>
        <select class="form-select">
          <option>Geocoding API</option>
        </select>
      </div>
      <div class="form-field">
        <span class="ci-label">Parameter</span>
        <input class="form-input mono" type="text" placeholder="/api/geocode?q=...">
      </div>
      <button class="btn btn-primary">
        <i class="fa-solid fa-play"></i> Abfragen
      </button>
    </div>
  </div>
</div>

<!-- Code Viewer -->
<div class="panel panel-code">
  <div class="panel-header">
    <div class="panel-title">
      <i class="fa-solid fa-code"></i> API Response
    </div>
    <div class="panel-header-right">
      <span class="badge badge-green">200 OK</span>
      <span class="panel-meta">42 ms</span>
      <button class="btn btn-sm btn-ghost">
        <i class="fa-regular fa-copy"></i> Kopieren
      </button>
    </div>
  </div>
  <pre class="code-viewer-pre">{ "status": "ok" }</pre>
</div>
```

---

## CSS einbinden

```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/typography.css">
<link rel="stylesheet" href="css/badges.css">
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/page.css">
<link rel="stylesheet" href="css/code-viewer.css">
```

Oder alles auf einmal über `css/index.css`.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-05-02 | Initiale Definition. `.panel-code`, `.code-viewer-pre`, `.form-row`, `.ci-label`, `.mono`. |
```

- [ ] **Schritt 2: Committen**

```bash
git add docs/code-viewer.md
git commit -m "docs: add code-viewer component documentation"
```

---

## Task 6: `docs/tokens.md` ergänzen

**Files:**
- Modify: `docs/tokens.md` — Abschnitt "Code / Terminal Farben" (Zeilen 60–70)

- [ ] **Schritt 1: Verwendungshinweis in der Tokens-Tabelle erweitern**

Den bestehenden Abschnitt ersetzen:

**Vorher (Zeilen 62–69):**
```markdown
| Token | Wert | Verwendung |
|---|---|---|
| `--code-bg` | `#000000` | Code Block Hintergrund |
| `--code-text` | `#4ade80` | Terminal-Output, Code Block Text |
| `--code-inline-bg` | `#2a2a2a` | Inline Code Hintergrund |
| `--code-inline-text` | `#e6e6e6` | Inline Code Text |
| `--url-bg` | `#0d0d0d` | URL / Pfad Felder in Cards |
| `--url-text` | `#4ade80` | URL / Pfad Text |
```

**Nachher:**
```markdown
| Token | Wert | Verwendung |
|---|---|---|
| `--code-bg` | `#000000` | Code Block Hintergrund; `.panel-code` Panel-Hintergrund |
| `--code-text` | `#4ade80` | Terminal-Output, Code Block Text; `.code-viewer-pre` |
| `--code-inline-bg` | `#2a2a2a` | Inline Code Hintergrund |
| `--code-inline-text` | `#e6e6e6` | Inline Code Text |
| `--url-bg` | `#0d0d0d` | URL / Pfad Felder in Cards |
| `--url-text` | `#4ade80` | URL / Pfad Text |
```

- [ ] **Schritt 2: Committen**

```bash
git add docs/tokens.md
git commit -m "docs: note that code tokens are also used by panel-code"
```

---

## Task 7: `docs/for-coding-agents.md` ergänzen

**Files:**
- Modify: `docs/for-coding-agents.md` — neuen Abschnitt nach "### 5. Bestehende Seitentypen verwenden" einfügen

- [ ] **Schritt 1: Neuen Abschnitt nach Regel 5 einfügen**

Nach dem Block der Regel 5 (endet mit "---") diesen Block einfügen:

```markdown
### 5a. API-Debugger / Code-Viewer

Seiten, die API-Antworten oder technische Rohdaten anzeigen, verwenden das `.panel-code` Pattern.

**Seitentyp:** Typ 1 — Detail-Seite.

**Zwei Panels:**

1. **Control Panel** — normales `.panel` mit `.form-row` für horizontal angeordnete Eingabefelder.
   Labels über Feldern: `.ci-label`. Mono-Inputs: `.form-input.mono`.

2. **Code Viewer** — `.panel.panel-code` mit:
   - `.panel-header`: Titel links, `badge-green`/`badge-red` + Latenz + Copy-Button rechts.
   - `<pre class="code-viewer-pre">`: scrollbarer Code-Block.

**Regeln:**
- Kein `background` hardcoden — `var(--code-bg)` verwenden.
- HTTP-Status immer als Badge darstellen: `badge-green` (2xx), `badge-red` (4xx/5xx), `badge-yellow` (3xx).
- Latenz als `<span class="panel-meta">42 ms</span>` neben dem Badge.
- Copy-Button: `.btn.btn-sm.btn-ghost`.
- Kein CSS-Grid, kein lokales Panel-Styling — nur `.panel.panel-code`.

**Referenz:** `components/code-viewer.html`, `docs/code-viewer.md`

---
```

- [ ] **Schritt 2: Committen**

```bash
git add docs/for-coding-agents.md
git commit -m "docs: add API-Debugger / Code-Viewer pattern to for-coding-agents.md"
```

---

## Task 8: Abschluss-Prüfliste

- [ ] `css/common.css` unverändert (keine neuen Tokens)
- [ ] Keine Farben oder Z-Index-Werte hardcodiert
- [ ] `css/demo.css` nicht in Produktiv-CSS importiert
- [ ] `components/code-viewer.html` im Browser geprüft (alle 4 Demo-Sektionen korrekt)
- [ ] `css/index.css` lädt `code-viewer.css` nach `page.css`
- [ ] Alle Commits vorhanden (6 Commits nach Task 1–7)

- [ ] **Abschluss-Commit (falls noch Änderungen unstaged):**

```bash
git status
# Alle grünen Häkchen? Fertig.
```

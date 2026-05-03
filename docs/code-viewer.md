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

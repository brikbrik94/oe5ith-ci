# Design Spec: Code-Viewer / API-Debugger Komponente

**Datum:** 2026-05-02  
**Status:** Approved  
**Seitentyp:** Typ 1 — Detail-Seite

---

## Ziel

Standardisiertes CI-Pattern für Seiten, die API-Antworten oder technische Rohdaten anzeigen. Kombiniert ein Eingabe-Control-Panel mit einem Terminal-artigen Code-Viewer-Panel.

---

## Entscheidungen

| Thema | Entscheidung |
|---|---|
| CSS-Ablageort | Neue Datei `css/code-viewer.css` |
| Label-Klasse außerhalb Formulare | Neue Klasse `.ci-label` in `typography.css` |
| Mono-Font-Utility | Neue Klasse `.mono` in `typography.css` |
| Meta-Leisten-Stil | Option B — Panel-Header-Stil (`.panel-header` Pattern) |
| Neue Tokens | Keine — alle benötigten Tokens existieren bereits |

---

## Tokens (alle bestehend)

| Token | Wert | Verwendung |
|---|---|---|
| `--code-bg` | `#000000` | Hintergrund `.panel-code` |
| `--code-text` | `#4ade80` | Text im `.code-viewer-pre` |
| `--font-mono` | JetBrains Mono | `.mono` Utility, `.code-viewer-pre` |
| `--border-strong` | `#444444` | Rahmen `.panel-code` |
| `--panel-deep` | `#161616` | Hintergrund der Meta-Leiste |

---

## Neue CSS-Klassen

### `css/code-viewer.css` (neue Datei)

**`.panel-code`** — Modifier auf `.panel`  
Überschreibt Hintergrund und Border für Terminal-Charakter:
- `background: var(--code-bg)`
- `border-color: var(--border-strong)`
- Innere `.panel-header`: `background: var(--panel-deep)`, `border-bottom-color: var(--border-strong)`

**`.code-viewer-pre`** — der scrollbare Code-Block  
- `font-family: var(--font-mono)`
- `color: var(--code-text)`
- `background: var(--code-bg)`
- `white-space: pre-wrap`
- `max-height: 600px`, `overflow: auto`
- `padding: 16px 20px`
- `margin: 0`, kein Border

### `css/typography.css` (erweitert)

**`.mono`** — allgemeine Font-Utility  
- `font-family: var(--font-mono)`
- Verwendung: Inputs, Spans, jedes Element mit Mono-Schrift außerhalb von Code-Blöcken

**`.ci-label`** — Label außerhalb von `.form-field`  
- Identisches Aussehen wie `.form-label`
- `font-size: 0.65rem`, `font-weight: 700`, `letter-spacing: 0.8px`, `text-transform: uppercase`, `color: var(--subtle)`
- Verwendung: überall wo ein kleines Uppercase-Label benötigt wird, aber kein Formular-Kontext vorliegt

---

## HTML-Struktur

### Control Panel

```html
<div class="panel">
  <div class="panel-header">
    <div class="panel-title">
      <i class="..."></i> Abfrage-Parameter
    </div>
  </div>
  <div class="panel-body">
    <div class="form-row">
      <div class="form-field">
        <span class="ci-label">Dienst</span>
        <select class="form-select">...</select>
      </div>
      <div class="form-field">
        <span class="ci-label">Parameter</span>
        <input class="form-input mono" type="text" placeholder="/api/...">
      </div>
      <button class="btn btn-primary">Abfragen</button>
    </div>
  </div>
</div>
```

**`.form-row`** — horizontales Flex-Layout für Control-Inputs:
- `display: flex`, `align-items: flex-end`, `gap: 12px`, `flex-wrap: wrap`

### Code Viewer Panel

```html
<div class="panel panel-code">
  <div class="panel-header">
    <div class="panel-title">
      <i class="..."></i> API Response
    </div>
    <div class="panel-header-right">
      <span class="badge badge-green">200 OK</span>  <!-- oder badge-red -->
      <span class="panel-meta">42 ms</span>
      <button class="btn btn-sm btn-gray">Kopieren</button>
    </div>
  </div>
  <pre class="code-viewer-pre">{ ... }</pre>
</div>
```

---

## Dateistruktur

| Aktion | Datei | Inhalt |
|---|---|---|
| neu | `css/code-viewer.css` | `.panel-code`, `.code-viewer-pre`, `.form-row` |
| erweitern | `css/typography.css` | `.mono`, `.ci-label` |
| erweitern | `css/index.css` | `@import 'code-viewer.css'` |
| neu | `docs/code-viewer.md` | Komponentendokumentation |
| neu | `components/code-viewer.html` | Referenz-HTML (OK + Fehlerfall) |
| erweitern | `docs/tokens.md` | Hinweis: `--code-bg`/`--code-text` auch für `panel-code` |
| erweitern | `docs/for-coding-agents.md` | Seitentyp API-Debugger / Code-Viewer |

---

## Seitentyp-Einordnung

Der API-Debugger ist eine Ausprägung von **Typ 1 — Detail-Seite**. Kein neuer Seitentyp nötig.  
In `docs/for-coding-agents.md` wird ein Abschnitt ergänzt der beschreibt, wann `.panel-code` zu verwenden ist.

---

## Was nicht geändert wird

- `css/page.css` — `.panel` bleibt unverändert
- `css/cards.css` — keine Code-Viewer-Klassen dort
- `css/common.css` — keine neuen Tokens
- Bestehende Seiten — keine Rückwärtsinkompatibilität

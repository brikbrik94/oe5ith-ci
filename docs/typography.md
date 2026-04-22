# Typografie

**Referenz-Datei:** `components/typography.html`  
**Status:** definiert · v1.0

---

## Schriftfamilien

### Sans-Serif — UI, Body, Headings

```css
--font-sans: 'Segoe UI', system-ui, sans-serif;
```

System-Font — kein externer Download.

| OS | Schrift |
|---|---|
| Windows | Segoe UI |
| macOS / iOS | San Francisco |
| Android | Roboto |

### Monospace — Code, URLs, Terminal

```css
--font-mono: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
```

Google Fonts — wird beim Seitenaufruf geladen.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

Fallback: `Consolas` → `Monaco` → `monospace`  
Gewichte: `400` · `500` · `700`

---

## Headings

### H1 — 2.0rem / 300

```css
h1 { font-size: 2.0rem; font-weight: 300; color: #fff; line-height: 1.2; }
h1 span { font-weight: 700; color: var(--accent); }
```

```html
<h1>System <span>Overview</span></h1>   <!-- mit Akzent -->
<h1>Verfügbare Vektorkarten</h1>        <!-- ohne Akzent -->
```

> Akzent-Span nur wenn ein echtes Schlüsselwort hervorgehoben werden soll. Nicht erzwingen.

### H2 — 1.3rem / 600

```css
h2 { font-size: 1.3rem; font-weight: 600; color: #fff; line-height: 1.3; }
```

### H3 — 1.0rem / 600

```css
h3 {
  font-size: 1.0rem; font-weight: 600; color: #ddd; line-height: 1.4;
  padding-bottom: 8px; border-bottom: 1px solid var(--border);
}
```

Border-bottom immer vorhanden — trennt H3 vom Inhalt.

---

## Body Text

### Body — 0.9rem

```css
p { font-size: 0.9rem; font-weight: 400; color: var(--muted); line-height: 1.5; }
```

### Small — 0.8rem

```css
.text-small { font-size: 0.8rem; color: var(--muted); line-height: 1.5; }
```

Verwendet für: Metadaten, Zeitstempel, Hinweistexte.

### Label — 0.65rem

```css
.text-label {
  font-size: 0.65rem; font-weight: 700;
  letter-spacing: 1.2px; text-transform: uppercase; color: #555;
}
```

Verwendet für: Sidebar-Gruppenüberschriften, Section-Trennungen.

### Brand — 1.2rem

```css
.brand-text { font-size: 1.2rem; font-weight: 700; letter-spacing: 1px; color: #fff; }
```

---

## Monospace

### Inline Code

```css
code {
  font-family: var(--font-mono); font-size: 0.82rem;
  background: #2a2a2a; color: #e6e6e6;
  padding: 2px 6px; border-radius: 4px; border: 1px solid #1a1a1a;
}
```

### Code Block / Terminal

```css
pre {
  font-family: var(--font-mono); font-size: 0.82rem;
  background: #000; color: #4ade80;
  padding: 14px 16px; border-radius: 6px; border: 1px solid #1a1a1a;
  overflow-x: auto; line-height: 1.7; white-space: pre;
}
```

### URL / Pfad

```css
.text-url {
  font-family: var(--font-mono); font-size: 0.78rem;
  color: #4ade80; background: #0d0d0d; border: 1px solid #1a1a1a;
  border-radius: 4px; padding: 5px 10px;
  overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap; display: block; min-width: 0;
}
```

Nie umbrechen — immer einzeilig mit ellipsis.

---

## Größen-Übersicht

| Element | Größe | Gewicht | Farbe | Schrift |
|---|---|---|---|---|
| `h1` | 2.0rem | 300 | #fff | Sans |
| `h1 span` | — | 700 | --accent | Sans |
| `h2` | 1.3rem | 600 | #fff | Sans |
| `h3` | 1.0rem | 600 | #ddd | Sans |
| `p` | 0.9rem | 400 | --muted | Sans |
| `.text-small` | 0.8rem | 400 | --muted | Sans |
| `.text-label` | 0.65rem | 700 | #555 | Sans |
| `.brand-text` | 1.2rem | 700 | #fff | Sans |
| `code` | 0.82rem | 400 | #e6e6e6 | Mono |
| `pre` | 0.82rem | 400 | #4ade80 | Mono |
| `.text-url` | 0.78rem | 400 | #4ade80 | Mono |

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | Initiale Definition. Sans + Mono (JetBrains). H1–H3. Body/Small/Label/Brand. Inline Code + Block + URL. line-height 1.5. |

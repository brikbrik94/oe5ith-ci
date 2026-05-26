# Design: Component HTML CSS Cleanup

**Datum:** 2026-05-26  
**Scope:** `components/*.html` — alle 16 Referenzseiten außer `toast.html` (bereits korrekt)

## Problem

Fast alle HTML-Referenzseiten in `components/` haben große `<style>`-Blöcke, die:
- Alle Design-Tokens neu deklarieren (`:root {}`) — statt `common.css` zu laden
- Komplette Komponenten-CSS duplizieren — statt der echten CSS-Dateien
- Demo-Layout-CSS enthalten — statt `demo.css` zu nutzen

Zusätzlich enthalten `style=`-Attribute im HTML-Body hardcoded Farbwerte statt CSS-Token-Variablen.

## Ziel

Jede Referenzseite:
1. Entfernt den `<style>`-Block vollständig
2. Lädt stattdessen die richtigen CSS-Dateien per `<link>`
3. Verwendet in `style=`-Attributen nur noch CSS-Token-Variablen für Farben

## CSS-Link-Struktur

Reihenfolge im `<head>`:
```html
<!-- Font Awesome — nur wenn die Datei FA-Icons nutzt -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<!-- Immer zuerst: Tokens, Reset, Basis-Layout -->
<link rel="stylesheet" href="../css/common.css">
<!-- Komponentenspezifische CSS-Dateien -->
...
<!-- Immer zuletzt: Demo-Layout-Hilfklassen -->
<link rel="stylesheet" href="../css/demo.css">
```

## Mapping: Datei → CSS-Links

| HTML-Datei | CSS-Dateien (nach common.css, vor demo.css) |
|---|---|
| `badges.html` | `badges.css` |
| `buttons.html` | `buttons.css` |
| `buttons-demo.html` | `buttons.css` |
| `cards.html` | `topbar.css`, `cards.css` |
| `code-viewer.html` | `code-viewer.css`, `forms.css` |
| `context-menu.html` | `modal.css` (`.ctx-menu` ist dort definiert) |
| `forms.html` | `topbar.css`, `forms.css`, `sidebar.css` |
| `modal.html` | `topbar.css`, `modal.css` |
| `page-types.html` | *(keine weiteren)* |
| `sidebar.html` | `topbar.css`, `sidebar.css`, `badges.css` |
| `sidebar-types.html` | `sidebar.css`, `badges.css`, `forms.css` |
| `tokens.html` | *(keine weiteren)* |
| `topbar.html` | `topbar.css`, `sidebar.css` |
| `typography.html` | `typography.css` |
| `typography-preview.html` | `typography.css` |
| `utils.html` | `utils.css` |
| `toast.html` | bereits korrekt — keine Änderung |

## Farb-Token-Mapping (inline style=-Attribute)

Hardcoded Hex-Werte werden durch CSS-Custom-Properties ersetzt:

| Hardcoded Wert | CSS-Token |
|---|---|
| `#1a1a1a` | `var(--bg)` |
| `#252525` | `var(--card-bg)` |
| `#202020` | `var(--panel)` |
| `#161616` | `var(--panel-deep)` |
| `#e0e0e0` | `var(--text)` |
| `#888` / `#888888` | `var(--muted)` |
| `#555` / `#555555` | `var(--subtle)` |
| `#333` / `#333333` | `var(--border)` |
| `#444` / `#444444` | `var(--border-strong)` |
| `#3b82f6` | `var(--accent)` |
| `#2563eb` | `var(--accent-hover)` |
| `#22c55e` | `var(--success)` |
| `#eab308` | `var(--warning)` |
| `#ef4444` | `var(--danger)` |
| `#a78bfa` | `var(--auth)` |
| `rgba(59,130,246,0.07)` | `var(--accent-subtle)` |
| `rgba(59,130,246,0.10)` | `var(--accent-subtle-md)` |
| `rgba(59,130,246,0.25)` | `var(--accent-border)` |
| `#ffffff` / `#fff` | `var(--white)` |
| `#2a2a2a` | `var(--code-inline-bg)` |
| `#4ade80` | `var(--code-text)` |
| `#e6e6e6` | `var(--code-inline-text)` |

Folgende Farbwerte haben **kein Token** und bleiben hardcoded:
`#ccc`, `#666`, `#4b5563`, `#ddd`, `#d1d5db`, `#f59e0b`, `#2d3a2d`, `#1f1f1f`, `#222`

## Was bleibt unverändert

Layout-only inline styles werden **nicht** angefasst:
- `height`, `width`, `min-width`, `max-width`
- `flex`, `gap`, `margin`, `padding`
- `pointer-events`, `position:relative`, `transform:none`
- `font-size` in Demo-Kontexten (Größenanpassungen für Demo-Darstellung)
- `display:none` (initiale Sichtbarkeit per JS gesteuert)

## Nicht in Scope

- Änderungen an CSS-Dateien in `css/`
- Extraktion von Inline-Patterns in `demo.css`-Klassen
- Inhalts- oder Struktur-Änderungen der HTML-Dateien
- Abgleich ob Komponenten-CSS mit Demo-HTML übereinstimmt (Drift-Check)

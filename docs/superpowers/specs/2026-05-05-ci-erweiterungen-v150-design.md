# CI-Erweiterungen v1.5.0

**Datum:** 2026-05-05  
**Status:** Entwurf  
**Quelle:** CI_ARCHITEKTUR_REPORT.md (Website V3 Audit, 2026-05-04)

---

## Übersicht

8 gezielte Ergänzungen auf Basis des Website-V3-Audits. Kein strukturelles Refactoring — ausschließlich additive Änderungen an bestehenden Dateien plus eine neue `css/utils.css`.

---

## 1. `css/utils.css` (neu)

Neue Utility-Datei für zweckgebundene Einzelklassen ohne eigene Komponenten-Struktur. Registrierung in `css/index.css` nach `coords.css`.

### Klassen

| Klasse | CSS | Verwendung |
|---|---|---|
| `.full-map` | `flex: 1; height: 100%; position: relative; min-height: 0;` | MapLibre/Leaflet-Container — verhindert Layout-Sprünge beim Laden |
| `.m-gap` | `margin: var(--card-gap);` | Rundum-Abstand mit CI-Token |
| `.mb-gap` | `margin-bottom: var(--card-gap);` | Abstand nach unten mit CI-Token |
| `.flex-col` | `display: flex; flex-direction: column;` | Flex-Container vertikal |
| `.flex-center` | `display: flex; align-items: center; justify-content: center;` | Zentrierter Flex-Container |

### Referenzseite

`components/utils.html` — zeigt alle 5 Klassen mit kurzer Beschreibung.

---

## 2. Token-Ergänzungen in `css/common.css`

### Neue Tokens

```css
/* Sidebar-Tab Maße */
--sidebar-tab-width:  16px;
--sidebar-tab-height: 44px;
```

**Placement:** im Sidebar-Tab-Block direkt nach `--sidebar-tab-border` (bestehende Tab-Tokens).

**Verwendung:** Ermöglicht `calc()`-Berechnungen für Tab-Positionierung statt Magic Numbers, z.B. `left: calc(-1 * var(--sidebar-tab-width))`.

### `docs/tokens.md` — Z-Index-Bereichsdokumentation

Ergänzung einer Tabelle, die die reservierten Z-Index-Bereiche dokumentiert:

| Bereich | Token-Bereich | Verwendung |
|---|---|---|
| App-Content | 0 – 999 | Site-spezifische Inhalte, Karten-Layer, App-Overlays |
| CI-Overlays | 1000+ | `--z-sidebar-tab` (1010) bis `--z-toast` (1600) |

---

## 3. `.overlay-section-label` in `css/sidebar.css`

Variante von `.sidebar-section-label` für schwebende Overlays (z.B. Topbar-Panels auf Tablet/Mobile). Gleiche Typografie, aber ohne den linken Padding-Versatz der Sidebar — passt in beliebige Container ohne Sidebar-Kontext.

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

**Placement:** nach `.sidebar-section-label` in `css/sidebar.css`.  
**Demo:** neue Sektion in `components/sidebar-types.html`.

---

## 4. Dokumentation

### `docs/for-coding-agents.md` — No-Inline-Style Policy

Neue Regel im Abschnitt für automatisierte Änderungen:

> Kein `style="..."` in dynamisch erzeugten HTML-Strings im JS/TS-Code. Ausnahme: Werte die erst zur Laufzeit berechnet werden können (z.B. Pixel-Positionen aus JS-Events, dynamische Breiten/Höhen). Für alle anderen Fälle: CI-Klassen verwenden.

### `docs/tokens.md` — Z-Index-Tabelle

Z-Index-Bereichsdokumentation wie in Abschnitt 2 beschrieben.

---

## Dateien-Übersicht

| Datei | Aktion |
|---|---|
| `css/utils.css` | Neu erstellen |
| `css/index.css` | `@import "utils.css"` ergänzen |
| `css/common.css` | 2 neue Tokens |
| `css/sidebar.css` | `.overlay-section-label` ergänzen |
| `components/utils.html` | Neu erstellen |
| `components/sidebar-types.html` | `.overlay-section-label` Demo-Sektion |
| `docs/tokens.md` | Z-Index-Bereichstabelle + Tab-Token-Doku |
| `docs/for-coding-agents.md` | No-Inline-Style Regel |
| `CHANGELOG.md` | v1.5.0 |

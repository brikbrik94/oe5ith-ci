# Chart-Komponente Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eine datengetriebene, wiederverwendbare `chart`-Komponente (Inline-SVG) für Statistik-Verläufe einführen und ins Service-Dashboard integrieren.

**Architecture:** Reines CSS/HTML-System ohne Build-Step. Die App generiert die SVG-Geometrie aus Daten; `css/chart.css` liefert nur Stroke/Fill/Farbe über `common.css`-Token. Serienfarbe wird über die CSS-Custom-Property `--chart-series-color` gesetzt (Serien-Modifier `chart-s1`–`s4`); Status-Modifier (`chart-ok/-warn/-danger`) überschreiben sie auf dem Leaf-Element (Status gewinnt durch Setzen der Variable direkt am Element).

**Tech Stack:** CSS Custom Properties, Inline-SVG (`polyline`/`path`/`rect`/`circle`), `docs/registry.json` + `scripts/cli/check_consistency.py` als Verifikations-Harness.

**Verifikations-Harness (statt Unit-Tests):** Dieses Repo hat keine JS/TS-Testsuite. „Test" bedeutet hier:
1. `python3 scripts/cli/check_consistency.py` muss fehlerfrei durchlaufen (Registry ↔ Dateien ↔ index.css).
2. `components/chart.html` ist die visuelle Verifikation — sie muss alle Klassen aus `docs/chart.md` (G1) verwenden.

**Spec:** `docs/superpowers/specs/2026-06-11-chart-component-design.md`

---

## File Structure

- `css/common.css` (Modify) — 7 neue Chart-Token nach den Kalender-Farbslots.
- `docs/tokens.md` (Modify) — Token-Doku + Spiegelung im „Vollständige common.css"-Block.
- `css/chart.css` (Create) — alle `chart-*`-Klassen.
- `components/chart.html` (Create) — Referenz/Verifikation aller Typen + Zustände.
- `docs/chart.md` (Create) — Doc nach doc-standard (G1–G4).
- `css/index.css` (Modify) — `@import "chart.css";` nach `cards.css`.
- `docs/registry.json` (Modify) — neuer `component`-Eintrag.
- `docs/service-dashboard.md` (Modify) — Panel-Typ „Verlauf" + Sparkline-Platzierung.
- `components/service-dashboard-detail.html` + `-overview.html` (Modify) — Verlauf-Panel + Sparkline-Beispiele.
- `CHANGELOG.md` (Modify) — `Added`-Eintrag für v1.13.0.

---

## Task 1: Chart-Token in common.css

**Files:**
- Modify: `css/common.css` (nach den `--cal-color-*`-Slots, vor `/* ── TYPOGRAFIE ── */` bzw. dem Font-Block)

- [ ] **Step 1: Token-Block einfügen**

Finde in `css/common.css` das Ende der Kalender-Farbslots (`--cal-color-N-*`-Reihe). Füge unmittelbar danach diesen Block ein:

```css
  /* ── FARBEN: Chart-Serienfarben (Verlaufs-/Diagramm-Komponente) ── */
  --chart-1:            var(--accent);   /* #3b82f6 — Datenreihe 1 (Default) */
  --chart-2:            #14b8a6;          /* Teal   — Datenreihe 2 */
  --chart-3:            #a855f7;          /* Violett — Datenreihe 3 */
  --chart-4:            #f59e0b;          /* Amber  — Datenreihe 4 */
  --chart-grid:         var(--border);   /* Gridlines */
  --chart-axis:         var(--subtle);   /* Achsenlinien + Tick-Labels */
  --chart-area-opacity: 0.15;            /* Füll-Transparenz Bereichsdiagramm */
```

- [ ] **Step 2: Verifizieren, dass common.css valide bleibt**

Run: `python3 -c "import re,sys; t=open('css/common.css').read(); print('OK' if t.count('{')==t.count('}') else 'BRACE MISMATCH')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add css/common.css
git commit -m "feat(tokens): add chart series + grid/axis tokens"
```

---

## Task 2: Token-Doku in tokens.md

**Files:**
- Modify: `docs/tokens.md` (neuer Abschnitt nach „## Kalender-Farbslots"; zusätzlich Spiegelung im „## Vollständige common.css"-Codeblock)

- [ ] **Step 1: Neuen Doku-Abschnitt einfügen**

Füge nach dem Abschnitt „## Kalender-Farbslots" (vor „## Code / Terminal Farben") ein:

```markdown
## Chart-Farbslots

Für die Verlaufs-/Diagramm-Komponente (`docs/chart.md`). Serienfarben sind pro Diagramm den
Datenreihen 1–4 zugeordnet; Schwellwert-Färbung nutzt die semantischen Farben (`--success`/
`--warning`/`--danger`), nicht diese Slots.

| Token | Wert | Verwendung |
|---|---|---|
| `--chart-1` | `var(--accent)` (#3b82f6) | Datenreihe 1 (Default-Serie) |
| `--chart-2` | `#14b8a6` | Datenreihe 2 (Teal) |
| `--chart-3` | `#a855f7` | Datenreihe 3 (Violett) |
| `--chart-4` | `#f59e0b` | Datenreihe 4 (Amber) |
| `--chart-grid` | `var(--border)` | Gridlines im Diagramm |
| `--chart-axis` | `var(--subtle)` | Achsenlinien und Tick-Beschriftungen |
| `--chart-area-opacity` | `0.15` | Füll-Transparenz für Bereichsdiagramme |
```

- [ ] **Step 2: Spiegelung im „Vollständige common.css"-Block**

Im Codeblock unter „## Vollständige common.css" denselben Token-Block wie in Task 1 (Step 1) an der entsprechenden Stelle (nach den `--cal-color-*`-Zeilen) einfügen, damit der eingebettete Spiegel mit `css/common.css` übereinstimmt.

- [ ] **Step 3: Commit**

```bash
git add docs/tokens.md
git commit -m "docs(tokens): document chart color slots"
```

---

## Task 3: css/chart.css anlegen

**Files:**
- Create: `css/chart.css`

- [ ] **Step 1: Datei mit vollständigem Inhalt anlegen**

```css
/*
 * OE5ITH CI — chart.css
 * Datengetriebene Verlaufs-/Diagramm-Komponente (Inline-SVG).
 * Die App liefert die SVG-Geometrie (Koordinaten aus Daten);
 * diese Datei liefert ausschließlich Farbe/Stroke/Fill via common.css-Tokens.
 *
 * Verwendung:
 *   1. common.css einbinden (Tokens)
 *   2. Diese Datei einbinden
 *
 * <link rel="stylesheet" href="shared/css/common.css">
 * <link rel="stylesheet" href="shared/css/chart.css">
 */

/* ═══════════════════════════════════════
   CHART BASE
   ═══════════════════════════════════════ */

.chart {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

/* ── Header: Titel + Legende ── */
.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.chart-title {
  font-size: 0.8rem;
  color: var(--muted);
  margin: 0;
}

.chart-legend {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.chart-legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.7rem;
  color: var(--muted);
}

.chart-legend-swatch {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  background: var(--chart-series-color, var(--chart-1));
  flex-shrink: 0;
}

/* ═══════════════════════════════════════
   PLOT / SVG
   ═══════════════════════════════════════ */

.chart-plot {
  position: relative;
  width: 100%;
}

.chart-svg {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
}

/* ═══════════════════════════════════════
   SERIENFARBE
   Serien-Modifier setzen die Custom-Property; Leaf-Elemente lesen sie.
   Status-Modifier (weiter unten) überschreiben sie auf dem Leaf → Status gewinnt.
   ═══════════════════════════════════════ */

.chart-s1 { --chart-series-color: var(--chart-1); }
.chart-s2 { --chart-series-color: var(--chart-2); }
.chart-s3 { --chart-series-color: var(--chart-3); }
.chart-s4 { --chart-series-color: var(--chart-4); }

/* ═══════════════════════════════════════
   GRID & ACHSEN
   ═══════════════════════════════════════ */

.chart-gridline {
  stroke: var(--chart-grid);
  stroke-width: 1;
  vector-effect: non-scaling-stroke;
}

.chart-axis-line {
  stroke: var(--chart-axis);
  stroke-width: 1;
  vector-effect: non-scaling-stroke;
}

.chart-tick-label {
  fill: var(--subtle);
  font-size: 0.62rem;
  font-family: var(--font-sans);
}

/* ═══════════════════════════════════════
   DATENREIHEN
   ═══════════════════════════════════════ */

.chart-line {
  fill: none;
  stroke: var(--chart-series-color, var(--chart-1));
  stroke-width: 2;
  stroke-linejoin: round;
  stroke-linecap: round;
  vector-effect: non-scaling-stroke;
}

.chart-area-fill {
  fill: var(--chart-series-color, var(--chart-1));
  fill-opacity: var(--chart-area-opacity);
  stroke: none;
}

.chart-bar-rect {
  fill: var(--chart-series-color, var(--chart-1));
}

.chart-point {
  fill: var(--chart-series-color, var(--chart-1));
  stroke: var(--bg);
  stroke-width: 1.5;
  vector-effect: non-scaling-stroke;
}

.chart-point-last {
  stroke: var(--text);
}

/* ── Status-Färbung (überschreibt Serienfarbe auf dem Leaf) ── */
.chart-ok     { --chart-series-color: var(--success); }
.chart-warn   { --chart-series-color: var(--warning); }
.chart-danger { --chart-series-color: var(--danger); }

/* ═══════════════════════════════════════
   TOOLTIP (CI-positioniert, App toggelt .is-visible)
   ═══════════════════════════════════════ */

.chart-tooltip {
  position: absolute;
  z-index: var(--z-tooltip);
  pointer-events: none;
  background: var(--panel-deep);
  border: 1px solid var(--border-strong);
  border-radius: 6px;
  padding: 6px 9px;
  font-size: 0.7rem;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transform: translate(-50%, -100%);
  transition: opacity var(--transition-fast);
}

.chart-tooltip.is-visible {
  opacity: 1;
  visibility: visible;
}

.chart-tooltip-label { color: var(--muted); }
.chart-tooltip-value { color: var(--text); font-weight: 600; }

/* ═══════════════════════════════════════
   EMPTY-STATE
   ═══════════════════════════════════════ */

.chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60px;
  color: var(--subtle);
  font-size: 0.75rem;
}

/* ═══════════════════════════════════════
   SPARKLINE (achsenlos, kompakt — in Zelle/Kachel)
   ═══════════════════════════════════════ */

.chart-sparkline {
  gap: 0;
}

.chart-sparkline .chart-svg {
  height: 2rem;
  width: 100%;
}
```

- [ ] **Step 2: Klammer-Balance prüfen**

Run: `python3 -c "t=open('css/chart.css').read(); print('OK' if t.count('{')==t.count('}') else 'BRACE MISMATCH')"`
Expected: `OK`

- [ ] **Step 3: Keine hardcodierten Farben/Z-Index/Transitions prüfen**

Run: `grep -nE '#[0-9a-fA-F]{3,6}|rgba?\(|z-index:\s*[0-9]|transition:[^v]*[0-9]+s' css/chart.css || echo "CLEAN"`
Expected: `CLEAN` (alle Farben/z-index/transition über Tokens; reine px-Maße für Spacing/Radius sind wie in `cards.css` erlaubt).

- [ ] **Step 4: Commit**

```bash
git add css/chart.css
git commit -m "feat(chart): add chart.css — SVG line/area/bar/sparkline styling"
```

---

## Task 4: chart.css in index.css einreihen

**Files:**
- Modify: `css/index.css`

- [ ] **Step 1: Import nach cards.css ergänzen**

In `css/index.css` direkt nach der Zeile `@import "cards.css";` einfügen:

```css
@import "chart.css";
```

- [ ] **Step 2: Verifizieren**

Run: `grep -n 'chart.css' css/index.css`
Expected: eine Zeile `@import "chart.css";` zwischen `cards.css` und `topbar.css`.

- [ ] **Step 3: Commit**

```bash
git add css/index.css
git commit -m "build(css): import chart.css in index.css"
```

---

## Task 5: components/chart.html (Verifikation)

**Files:**
- Create: `components/chart.html`

Diese Seite zeigt jeden Typ und Zustand. Sie bindet `demo.css` ein (nur für Referenzseiten). Geometrie-Koordinaten sind statisch (keine App nötig). Achte darauf, dass **jede** Klasse aus `docs/chart.md` (Task 6, G1) hier mindestens einmal vorkommt.

- [ ] **Step 1: Datei anlegen**

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Chart</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/cards.css">
<link rel="stylesheet" href="../css/chart.css">
<link rel="stylesheet" href="../css/demo.css">
</head>
<body>
<main class="demo-main" style="max-width:900px;margin:0 auto;padding:24px;">

  <h1>Chart-Komponente</h1>

  <!-- 1. Liniendiagramm, Einzelserie, mit Achsen + Grid + Punkten -->
  <h2>Linie (Einzelserie, Achsen + Grid)</h2>
  <div class="chart chart-s1">
    <div class="chart-header">
      <p class="chart-title">CPU-Auslastung</p>
    </div>
    <div class="chart-plot">
      <svg class="chart-svg" viewBox="0 0 300 100" preserveAspectRatio="none"
           role="img" aria-label="CPU-Auslastung der letzten Stunde">
        <g class="chart-grid">
          <line class="chart-gridline" x1="0" y1="25" x2="300" y2="25"></line>
          <line class="chart-gridline" x1="0" y1="50" x2="300" y2="50"></line>
          <line class="chart-gridline" x1="0" y1="75" x2="300" y2="75"></line>
        </g>
        <g class="chart-axis chart-axis-y">
          <line class="chart-axis-line" x1="0" y1="0" x2="0" y2="100"></line>
          <text class="chart-tick-label" x="4" y="14">100</text>
          <text class="chart-tick-label" x="4" y="54">50</text>
          <text class="chart-tick-label" x="4" y="96">0</text>
        </g>
        <g class="chart-series chart-s1">
          <polyline class="chart-line"
            points="0,80 50,60 100,65 150,40 200,45 250,20 300,30"></polyline>
          <circle class="chart-point" cx="300" cy="30" r="3"></circle>
        </g>
      </svg>
    </div>
  </div>

  <!-- 2. Bereichsdiagramm -->
  <h2>Fläche (chart-area)</h2>
  <div class="chart chart-area chart-s2">
    <div class="chart-plot">
      <svg class="chart-svg" viewBox="0 0 300 100" preserveAspectRatio="none"
           role="img" aria-label="Speicherverbrauch">
        <g class="chart-series chart-s2">
          <path class="chart-area-fill"
            d="M0,70 L60,55 L120,60 L180,35 L240,45 L300,25 L300,100 L0,100 Z"></path>
          <polyline class="chart-line"
            points="0,70 60,55 120,60 180,35 240,45 300,25"></polyline>
        </g>
      </svg>
    </div>
  </div>

  <!-- 3. Balkendiagramm -->
  <h2>Balken (chart-bar)</h2>
  <div class="chart chart-bar chart-s3">
    <div class="chart-plot">
      <svg class="chart-svg" viewBox="0 0 300 100" preserveAspectRatio="none"
           role="img" aria-label="Pakete pro Stunde">
        <g class="chart-axis chart-axis-x">
          <text class="chart-tick-label" x="20" y="98">08</text>
          <text class="chart-tick-label" x="140" y="98">12</text>
          <text class="chart-tick-label" x="260" y="98">16</text>
        </g>
        <g class="chart-series chart-s3">
          <rect class="chart-bar-rect" x="10"  y="50" width="30" height="40"></rect>
          <rect class="chart-bar-rect" x="60"  y="30" width="30" height="60"></rect>
          <rect class="chart-bar-rect" x="110" y="60" width="30" height="30"></rect>
          <rect class="chart-bar-rect" x="160" y="20" width="30" height="70"></rect>
          <rect class="chart-bar-rect" x="210" y="45" width="30" height="45"></rect>
          <rect class="chart-bar-rect" x="260" y="35" width="30" height="55"></rect>
        </g>
      </svg>
    </div>
  </div>

  <!-- 4. Multi-Serie mit Legende -->
  <h2>Multi-Serie + Legende</h2>
  <div class="chart">
    <div class="chart-header">
      <p class="chart-title">Durchsatz</p>
      <div class="chart-legend">
        <span class="chart-legend-item chart-s1"><span class="chart-legend-swatch"></span>Download</span>
        <span class="chart-legend-item chart-s2"><span class="chart-legend-swatch"></span>Upload</span>
      </div>
    </div>
    <div class="chart-plot">
      <svg class="chart-svg" viewBox="0 0 300 100" preserveAspectRatio="none"
           role="img" aria-label="Durchsatz Download und Upload">
        <g class="chart-series chart-s1">
          <polyline class="chart-line" points="0,70 60,50 120,55 180,30 240,40 300,20"></polyline>
        </g>
        <g class="chart-series chart-s2">
          <polyline class="chart-line" points="0,85 60,80 120,75 180,78 240,70 300,72"></polyline>
        </g>
      </svg>
    </div>
  </div>

  <!-- 5. Status-Färbung -->
  <h2>Status-Färbung (ok / warn / danger)</h2>
  <div class="chart chart-s1">
    <div class="chart-plot">
      <svg class="chart-svg" viewBox="0 0 300 100" preserveAspectRatio="none"
           role="img" aria-label="Statusfarben">
        <g class="chart-series">
          <polyline class="chart-line chart-ok" points="0,80 100,60 200,55 300,40"></polyline>
        </g>
        <g class="chart-series">
          <polyline class="chart-line chart-warn" points="0,60 100,45 200,50 300,35"></polyline>
        </g>
        <g class="chart-series">
          <polyline class="chart-line chart-danger" points="0,40 100,30 200,35 300,15"></polyline>
        </g>
      </svg>
    </div>
  </div>

  <!-- 6. Tooltip (statisch sichtbar zur Demo) -->
  <h2>Tooltip</h2>
  <div class="chart chart-s1">
    <div class="chart-plot">
      <svg class="chart-svg" viewBox="0 0 300 100" preserveAspectRatio="none"
           role="img" aria-label="Mit Tooltip">
        <g class="chart-series chart-s1">
          <polyline class="chart-line" points="0,80 100,50 200,55 300,30"></polyline>
          <circle class="chart-point" cx="200" cy="55" r="3"></circle>
        </g>
      </svg>
      <div class="chart-tooltip is-visible" style="left:67%;top:55%;">
        <span class="chart-tooltip-label">14:00</span>
        <span class="chart-tooltip-value">42 %</span>
      </div>
    </div>
  </div>

  <!-- 7. Sparkline (in Datenzelle) -->
  <h2>Sparkline</h2>
  <div class="chart chart-sparkline chart-area chart-s1" style="max-width:140px;">
    <svg class="chart-svg" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true">
      <path class="chart-area-fill" d="M0,22 L25,16 L50,18 L75,8 L100,12 L100,30 L0,30 Z"></path>
      <polyline class="chart-line" points="0,22 25,16 50,18 75,8 100,12"></polyline>
      <circle class="chart-point chart-point-last" cx="100" cy="12" r="2.5"></circle>
    </svg>
  </div>

  <!-- 8. Empty-State -->
  <h2>Empty-State</h2>
  <div class="chart">
    <div class="chart-plot">
      <div class="chart-empty">Keine Daten verfügbar</div>
    </div>
  </div>

</main>
</body>
</html>
```

- [ ] **Step 2: Alle G1-Klassen abgedeckt prüfen**

Run:
```bash
for c in chart chart-header chart-title chart-legend chart-legend-item chart-legend-swatch chart-plot chart-svg chart-grid chart-gridline chart-axis chart-axis-x chart-axis-y chart-axis-line chart-tick-label chart-series chart-s1 chart-s2 chart-s3 chart-s4 chart-line chart-area chart-area-fill chart-bar chart-bar-rect chart-point chart-point-last chart-sparkline chart-ok chart-warn chart-danger chart-tooltip chart-tooltip-label chart-tooltip-value is-visible chart-empty; do grep -q "$c" components/chart.html || echo "MISSING: $c"; done; echo "done"
```
Expected: nur `done` (keine `MISSING:`-Zeile).

- [ ] **Step 3: Commit**

```bash
git add components/chart.html
git commit -m "docs(chart): add reference/verification page components/chart.html"
```

---

## Task 6: docs/chart.md (Doc nach doc-standard)

**Files:**
- Create: `docs/chart.md`

- [ ] **Step 1: Datei anlegen**

```markdown
# Chart

**Referenz-Datei:** `components/chart.html`
**CSS:** `css/chart.css`
**Status:** definiert · v1.13.0

> Diese Doc folgt `docs/doc-standard.md` (interpretationsfrei). Die Beispiel-HTML in
> `components/chart.html` ist Verifikation, nicht Quelle — alles Nötige steht hier im Text.

---

## Überblick

Datengetriebene Verlaufs-/Diagramm-Komponente auf Basis von **Inline-SVG**. Die konsumierende
App generiert die SVG-Geometrie (Koordinaten aus den Daten); `chart.css` liefert ausschließlich
Stroke/Fill/Farbe über `common.css`-Token. Vier Ausprägungen: **Linie** (Default), **Fläche**
(`chart-area`), **Balken** (`chart-bar`) und **Sparkline** (`chart-sparkline`, achsenloser
Minimalmodus für Datenzellen/Kacheln).

### Ladereihenfolge

\`\`\`css
css/common.css   /* Tokens — chart-1..4, chart-grid, chart-axis, chart-area-opacity */
css/chart.css    /* chart-* Klassen */
\`\`\`

---

## Struktur / Verschachtelung (G2)

### Volldiagramm (Linie / Fläche / Balken)

\`\`\`text
.chart[.chart-area|.chart-bar]                       (Wurzel; ohne Modifier = Linie)
├── .chart-header                                     (Optional)
│   ├── .chart-title                                  (Optional)
│   └── .chart-legend                                 (Optional, ab ≥2 Serien Pflicht)
│       └── .chart-legend-item.chart-s1…s4            (n×)
│           ├── .chart-legend-swatch                  (Pflicht)
│           └── span  (Serien-Name)                   (Pflicht)
├── .chart-plot                                       (Pflicht)
│   └── svg.chart-svg  [viewBox, preserveAspectRatio] (Pflicht)
│       ├── g.chart-grid                              (Optional)
│       │   └── line.chart-gridline                   (n×)
│       ├── g.chart-axis.chart-axis-y                 (Optional)
│       │   ├── line.chart-axis-line                  (Optional)
│       │   └── text.chart-tick-label                 (n×)
│       ├── g.chart-axis.chart-axis-x                 (Optional)
│       │   └── text.chart-tick-label                 (n×)
│       └── g.chart-series.chart-s1…s4                (Pflicht, n×)
│           ├── path.chart-area-fill                  (nur bei .chart-area)
│           ├── polyline.chart-line                   (Linie/Fläche)
│           ├── rect.chart-bar-rect                   (nur bei .chart-bar, n×)
│           └── circle.chart-point                    (Optional, n×)
├── .chart-tooltip                                    (Optional)
│   ├── .chart-tooltip-label                          (Pflicht im Tooltip)
│   └── .chart-tooltip-value                          (Pflicht im Tooltip)
└── .chart-empty                                      (Optional)
\`\`\`

### Sparkline (in svc-data-cell / Übersichts-Kachel)

\`\`\`text
.chart.chart-sparkline[.chart-area]                  (Wurzel — achsenlos, kompakt)
└── svg.chart-svg
    ├── path.chart-area-fill                          (nur bei .chart-area)
    ├── polyline.chart-line                           (Pflicht)
    └── circle.chart-point.chart-point-last           (Optional)
\`\`\`

Die Sparkline lässt Header, Legende, Achsen, Grid und Tooltip bewusst weg.

---

## Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.chart` | Wurzel-Container | Pflicht | `.chart-area`, `.chart-bar`, `.chart-sparkline` |
| `.chart-header` | Kopfzeile (Titel + Legende) | Optional | — |
| `.chart-title` | Diagramm-Titel (0.8rem, `--muted`) | Optional | — |
| `.chart-legend` | Legenden-Leiste | Optional (Pflicht ab ≥2 Serien) | — |
| `.chart-legend-item` | Legenden-Eintrag | Optional | `.chart-s1`–`.chart-s4` |
| `.chart-legend-swatch` | Farbkästchen (erbt Serienfarbe) | Pflicht (im Item) | — |
| `.chart-plot` | Positions-Container für SVG/Tooltip | Pflicht | — |
| `.chart-svg` | Das `<svg>` (skaliert via viewBox) | Pflicht | — |
| `.chart-grid` | Gruppe der Gridlines | Optional | — |
| `.chart-gridline` | Gridline (`--chart-grid`) | Optional | — |
| `.chart-axis` | Achsen-Gruppe | Optional | `.chart-axis-x`, `.chart-axis-y` |
| `.chart-axis-line` | Achsenlinie (`--chart-axis`) | Optional | — |
| `.chart-tick-label` | Tick-Beschriftung (0.62rem, `--subtle`) | Optional | — |
| `.chart-series` | Gruppe einer Datenreihe | Pflicht | `.chart-s1`–`.chart-s4` |
| `.chart-line` | Linie (`polyline`, stroke = Serienfarbe) | Pflicht (Linie/Fläche) | `.chart-ok`, `.chart-warn`, `.chart-danger` |
| `.chart-area-fill` | Füllfläche (`path`, Serienfarbe @ `--chart-area-opacity`) | Optional (nur `.chart-area`) | `.chart-ok`, `.chart-warn`, `.chart-danger` |
| `.chart-bar-rect` | Balken (`rect`, fill = Serienfarbe) | Pflicht (nur `.chart-bar`) | `.chart-ok`, `.chart-warn`, `.chart-danger` |
| `.chart-point` | Datenpunkt (`circle`) | Optional | `.chart-point-last` |
| `.chart-tooltip` | Schwebende Wertanzeige (App toggelt) | Optional | `.is-visible` |
| `.chart-tooltip-label` | Tooltip-Bezeichnung (`--muted`) | Pflicht (im Tooltip) | — |
| `.chart-tooltip-value` | Tooltip-Wert (`--text`, 600) | Pflicht (im Tooltip) | — |
| `.chart-empty` | „Keine Daten"-Hinweis | Optional | — |

---

## Reihenfolge & Platzierung (G3)

- Im Volldiagramm steht `.chart-header` (falls vorhanden) vor `.chart-plot`; `.chart-empty`
  ist letztes Kind und ersetzt das Diagramm bei fehlenden Daten.
- Innerhalb `.chart-svg`: zuerst Grid (`g.chart-grid`), dann Achsen (`g.chart-axis`), zuletzt
  die Datenreihen (`g.chart-series`) — damit Serien optisch über Grid/Achsen liegen.
- Jede Datenreihe ist eine eigene `g.chart-series` mit genau einem Serien-Modifier
  (`chart-s1`–`s4`). Die Reihenfolge der Serien entspricht der Reihenfolge in der Legende.
- `.chart-tooltip` ist Kind von `.chart-plot` (nicht des SVG), da es absolut positioniert wird;
  die App setzt `left`/`top` (Inline-Position erlaubt — Position ist Daten, keine Farbe).

---

## Daten-Vertrag

- **Koordinaten:** `.chart-svg` nutzt `viewBox="0 0 W H"` + `preserveAspectRatio`. Die App
  rechnet Datenwerte in viewBox-Koordinaten um. CI-Klassen setzen keine Geometrie.
- **Linie/Fläche:** `polyline points="x,y …"`; Fläche zusätzlich `path d="…"` (zur Baseline
  geschlossen).
- **Balken:** je Wert ein `rect` mit `x/y/width/height`.
- **Farbe ausschließlich über Klassen** (`chart-s1`–`s4` bzw. Status), **nie** Inline-`fill`/
  `stroke` — sonst bricht die Token-Bindung.
- **Barrierefreiheit:** `.chart-svg` mit `role="img"` + `aria-label`. Sparklines, deren Wert
  bereits als Text danebensteht, dürfen `aria-hidden="true"` tragen.

---

## Zustände & Varianten (G4)

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Liniendiagramm | `.chart` (kein Typ-Modifier) | Default-Verlauf |
| Bereichsdiagramm | `.chart.chart-area` | Verlauf mit gefüllter Fläche |
| Balkendiagramm | `.chart.chart-bar` | Diskrete/gezählte Werte |
| Sparkline | `.chart.chart-sparkline` | Mini-Verlauf in Zelle/Kachel |
| Serie 1–4 | `.chart-s1` … `.chart-s4` | Farbzuordnung je Datenreihe |
| Wert im Soll | `.chart-ok` (auf Linie/Fläche/Balken) | Schwellwert grün (`--success`) |
| Wert grenzwertig | `.chart-warn` | Schwellwert gelb (`--warning`) |
| Wert kritisch | `.chart-danger` | Schwellwert rot (`--danger`) |
| Tooltip sichtbar | `.chart-tooltip.is-visible` | App zeigt Wert beim Hover |
| Letzter Punkt betont | `.chart-point.chart-point-last` | Sparkline-Endwert markieren |
| Keine Daten | `.chart-empty` | Historie leer/nicht verfügbar |

**Status-gewinnt-Regel:** Schwellwert-Modifier (`chart-ok/-warn/-danger`) werden auf das
Leaf-Element (`.chart-line`/`.chart-area-fill`/`.chart-bar-rect`) gesetzt und überschreiben die
über `g.chart-series` gesetzte Serienfarbe — die Custom-Property `--chart-series-color` wird
direkt am Element neu belegt. Serienfarbe und Status werden **nicht** am selben Element gemischt.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-11 | Initiale Definition. Inline-SVG; Linie/Fläche/Balken/Sparkline; Serien- + Status-Färbung; Achsen, Grid, Legende, Tooltip, Empty-State. |
\`\`\`

(Hinweis für den Umsetzer: Die `\`\`\`` im obigen Block sind im echten `docs/chart.md`
normale Code-Fences ohne Backslash — der Backslash steht hier nur, um die Fences innerhalb
dieses Plans zu maskieren.)
```

- [ ] **Step 2: G1 ↔ CSS Abgleich**

Run:
```bash
for c in chart chart-header chart-title chart-legend chart-legend-item chart-legend-swatch chart-plot chart-svg chart-grid chart-gridline chart-axis chart-axis-line chart-tick-label chart-series chart-line chart-area-fill chart-bar-rect chart-point chart-point-last chart-tooltip chart-tooltip-label chart-tooltip-value chart-empty chart-sparkline chart-s1 chart-ok chart-warn chart-danger; do grep -q "\.$c" css/chart.css || echo "DOC-CLASS NOT IN CSS: $c"; done; echo done
```
Expected: nur `done`.

- [ ] **Step 3: Commit**

```bash
git add docs/chart.md
git commit -m "docs(chart): add chart component doc (doc-standard G1–G4)"
```

---

## Task 7: Registry-Eintrag + Konsistenz-Check

**Files:**
- Modify: `docs/registry.json`

- [ ] **Step 1: Neuen Component-Eintrag ergänzen**

Füge im `"components"`-Array (sinnvoll bei den Basis-Komponenten, z. B. nach dem `cards`-Eintrag) ein:

```json
    {
      "id": "chart",
      "title": "Chart",
      "category": "component",
      "css": [
        "chart.css"
      ],
      "doc": [
        "chart.md"
      ],
      "html": [
        "chart.html"
      ]
    },
```

Achte auf gültiges JSON (Komma zwischen Einträgen, kein Trailing-Komma am Array-Ende).

- [ ] **Step 2: JSON-Validität prüfen**

Run: `python3 -c "import json; json.load(open('docs/registry.json')); print('VALID')"`
Expected: `VALID`

- [ ] **Step 3: Konsistenz-Check ausführen**

Run: `python3 scripts/cli/check_consistency.py`
Expected: Erfolgsausgabe ohne `error` (chart.css ist in index.css importiert, alle drei Dateien existieren, registriert). Falls README AUTOGEN-Abschnitte aktualisiert werden, diese Änderungen mit committen.

- [ ] **Step 4: Commit**

```bash
git add docs/registry.json README.md
git commit -m "chore(registry): register chart component + run consistency check"
```

---

## Task 8: Service-Dashboard-Integration (Doc)

**Files:**
- Modify: `docs/service-dashboard.md`

- [ ] **Step 1: Panel-Typ „Verlauf" zur Tabelle „Festes Set an Panel-Typen" ergänzen**

In `docs/service-dashboard.md`, in der Tabelle unter „**Festes Set an Panel-Typen:**", eine Zeile ergänzen:

```markdown
| **Verlauf / Historie** | Ein `.chart`-Volldiagramm (Linie/Fläche/Balken, siehe `docs/chart.md`) im `.panel-body`, das die kurze gespeicherte Historie einer Kennzahl zeigt | Optional |
```

- [ ] **Step 2: Regelabsatz direkt nach der Zellen-Regel ergänzen**

Nach dem Absatz „**Zellen-Regel:** …" einfügen:

```markdown
**Verlauf-Panel:** Ein Panel vom Typ „Verlauf / Historie" enthält **genau ein** `.chart`
(analog Ein-Endpunkt-Regel) im `.panel-body`. `.panel-title` (Icon + Bezeichnung) bleibt
Pflicht; eine optionale Zeitspanne (z. B. „letzte 24 h") steht als `span.panel-meta` im
`.panel-header-right`. Mechanik und Klassen des Diagramms regelt `docs/chart.md`.

**Sparkline in Datenzelle:** Eine `.svc-data-cell` darf **optional** als **letztes** Kind eine
`.chart.chart-sparkline` enthalten (nach `svc-data-label`/`svc-data-value`/optional
`svc-data-sub`). Die Zellen-Regel bleibt: die Sparkline ist der Verlauf **desselben** Werts,
kein zweiter Wert.
```

- [ ] **Step 3: G2-Baum der svc-data-cell um Sparkline erweitern**

Im G2-Baum der Detail-Seite die `svc-data-cell` ergänzen:

```text
│           └── .svc-data-cell                                               (Pflicht, n×)
│               ├── span.svc-data-label                                      (Pflicht)
│               ├── span.svc-data-value[.success|.danger]                   (Pflicht)
│               ├── span.svc-data-sub                                        (Optional)
│               └── .chart.chart-sparkline                                   (Optional, letztes Kind)
```

- [ ] **Step 4: Übersichts-Seite — Sparkline in Kachel dokumentieren**

Im Abschnitt „Seite 1 — Übersicht", in beiden Kachel-Varianten des G2-Baums, vor bzw. statt
des Pfeil-Icons eine optionale Sparkline als letztes Inhalts-Element ergänzen (klickbare
Variante: vor `.card-dashboard-arrow`; nicht klickbare: als letztes Kind):

```text
│   ├── span.svc-status-line[.online|.offline|.unknown]   (Pflicht)
│   ├── .chart.chart-sparkline                            (Optional)
│   └── i.card-dashboard-arrow                            (Optional, nur klickbare Variante)
```

Und im G3-Absatz der Übersicht einen Satz ergänzen:

```markdown
- Eine Kachel darf optional eine `.chart.chart-sparkline` (siehe `docs/chart.md`) als letztes
  Inhalts-Element vor dem Pfeil-Icon zeigen, um den Trend des Status-/Kennwerts anzudeuten.
```

- [ ] **Step 5: Änderungshistorie + Statuszeile aktualisieren**

In `docs/service-dashboard.md` die Statuszeile auf `**Status:** definiert · v1.13.0` setzen und
oben in der Änderungshistorie-Tabelle eine Zeile ergänzen:

```markdown
| 2026-06-11 | Panel-Typ „Verlauf / Historie" ergänzt (ein `.chart` pro Panel); Sparkline als optionales letztes Kind in `.svc-data-cell` und in Übersichts-Kacheln. Mechanik in `docs/chart.md`. |
```

- [ ] **Step 6: Commit**

```bash
git add docs/service-dashboard.md
git commit -m "docs(service-dashboard): add Verlauf panel type + sparkline placement"
```

---

## Task 9: Service-Dashboard-Komponenten (HTML-Verifikation)

**Files:**
- Modify: `components/service-dashboard-detail.html`
- Modify: `components/service-dashboard-overview.html`

- [ ] **Step 1: chart.css in beide Seiten einbinden**

In beiden Dateien im `<head>` nach der `cards.css`-Zeile ergänzen:

```html
<link rel="stylesheet" href="../css/chart.css">
```

- [ ] **Step 2: Verlauf-Panel in die Detail-Seite einfügen**

In `components/service-dashboard-detail.html` nach einem bestehenden `.panel` ein Verlauf-Panel
ergänzen (eigenständiges Diagramm, statische Koordinaten):

```html
<section class="panel">
  <div class="panel-header">
    <div class="panel-title"><i class="fa-solid fa-chart-line"></i> CPU-Verlauf</div>
    <div class="panel-header-right">
      <span class="panel-meta">letzte 24 h</span>
    </div>
  </div>
  <div class="panel-body">
    <div class="chart chart-area chart-s1">
      <div class="chart-plot">
        <svg class="chart-svg" viewBox="0 0 300 100" preserveAspectRatio="none"
             role="img" aria-label="CPU-Auslastung der letzten 24 Stunden">
          <g class="chart-grid">
            <line class="chart-gridline" x1="0" y1="33" x2="300" y2="33"></line>
            <line class="chart-gridline" x1="0" y1="66" x2="300" y2="66"></line>
          </g>
          <g class="chart-series chart-s1">
            <path class="chart-area-fill" d="M0,75 L60,60 L120,65 L180,40 L240,50 L300,30 L300,100 L0,100 Z"></path>
            <polyline class="chart-line" points="0,75 60,60 120,65 180,40 240,50 300,30"></polyline>
          </g>
        </svg>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 3: Sparkline in eine Datenzelle der Detail-Seite einfügen**

In einer bestehenden `.svc-data-cell` als letztes Kind ergänzen:

```html
<div class="chart chart-sparkline chart-s1" aria-hidden="true">
  <svg class="chart-svg" viewBox="0 0 100 30" preserveAspectRatio="none">
    <polyline class="chart-line" points="0,22 25,16 50,18 75,8 100,12"></polyline>
    <circle class="chart-point chart-point-last" cx="100" cy="12" r="2.5"></circle>
  </svg>
</div>
```

- [ ] **Step 4: Sparkline in eine Übersichts-Kachel einfügen**

In `components/service-dashboard-overview.html` in einer klickbaren Kachel vor
`i.card-dashboard-arrow` ergänzen:

```html
<div class="chart chart-sparkline chart-s1" aria-hidden="true">
  <svg class="chart-svg" viewBox="0 0 100 30" preserveAspectRatio="none">
    <polyline class="chart-line" points="0,20 25,12 50,16 75,9 100,6"></polyline>
  </svg>
</div>
```

- [ ] **Step 5: Visuelle Plausibilität (optional, falls Browser verfügbar)**

Run: `python3 -c "import pathlib; [print(p, 'chart.css' in pathlib.Path(p).read_text()) for p in ['components/service-dashboard-detail.html','components/service-dashboard-overview.html']]"`
Expected: beide `True`.

- [ ] **Step 6: Commit**

```bash
git add components/service-dashboard-detail.html components/service-dashboard-overview.html
git commit -m "docs(service-dashboard): demo Verlauf panel + sparklines in reference HTML"
```

---

## Task 10: CHANGELOG + Release-Vorbereitung

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Eintrag ergänzen**

Oben in `CHANGELOG.md` einen Abschnitt für v1.13.0 mit Kategorie `Added` ergänzen (Format an
bestehende Einträge anpassen):

```markdown
## [1.13.0] — 2026-06-11

### Added
- **Chart-Komponente** (`css/chart.css`, `docs/chart.md`, `components/chart.html`):
  datengetriebene Verlaufsdarstellung per Inline-SVG. Typen: Linie, Fläche (`chart-area`),
  Balken (`chart-bar`), Sparkline (`chart-sparkline`). Serien- und Schwellwert-Färbung,
  Achsen, Grid, Legende, Tooltip, Empty-State.
- Chart-Token in `common.css`: `--chart-1`–`--chart-4`, `--chart-grid`, `--chart-axis`,
  `--chart-area-opacity` (dokumentiert in `docs/tokens.md`).
- Service-Dashboard: neuer Panel-Typ „Verlauf / Historie"; Sparkline als optionales letztes
  Kind in `.svc-data-cell` und in Übersichts-Kacheln.
```

- [ ] **Step 2: Finaler Konsistenz-Check**

Run: `python3 scripts/cli/check_consistency.py`
Expected: kein `error`.

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): v1.13.0 — chart component"
```

- [ ] **Step 4: Release-Tag (nur nach ausdrücklicher Freigabe durch den Nutzer)**

Erst nach Bestätigung ausführen:

```bash
git tag -a v1.13.0 -m "Release v1.13.0 — chart component"
git push origin main
git push origin v1.13.0
```

---

## Self-Review (vom Plan-Autor durchgeführt)

- **Spec-Abdeckung:** Token (T1/T2) ✓ · chart.css (T3) ✓ · index.css (T4) ✓ · components/chart.html (T5) ✓ · docs/chart.md inkl. G1–G4 + Daten-Vertrag + A11y (T6) ✓ · Registry/Konsistenz (T7) ✓ · Dashboard-Integration Doc (T8) + HTML (T9) ✓ · MINOR/CHANGELOG (T10) ✓. Alle 6 Spec-Abschnitte abgedeckt.
- **Platzhalter:** keine TBD/TODO; aller CSS-/HTML-/JSON-Code ist vollständig ausgeschrieben.
- **Typ-/Namens-Konsistenz:** Klassennamen in chart.css (T3), chart.html (T5), chart.md (T6) und den Verifikations-Greps identisch geprüft (`chart-s1`–`s4`, `chart-area-fill`, `chart-bar-rect`, `chart-point-last`, `is-visible`). Serienfarb-Mechanik (`--chart-series-color`) in T3 definiert und in G4 (T6) beschrieben.
```

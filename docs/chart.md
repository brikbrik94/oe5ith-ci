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

```css
css/common.css   /* Tokens — chart-1..4, chart-grid, chart-axis, chart-area-opacity */
css/chart.css    /* chart-* Klassen */
```

---

## Struktur / Verschachtelung (G2)

### Volldiagramm (Linie / Fläche / Balken)

```text
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
```

### Sparkline (in svc-data-cell / Übersichts-Kachel)

```text
.chart.chart-sparkline[.chart-area]                  (Wurzel — achsenlos, kompakt)
└── svg.chart-svg
    ├── path.chart-area-fill                          (nur bei .chart-area)
    ├── polyline.chart-line                           (Pflicht)
    └── circle.chart-point.chart-point-last           (Optional)
```

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

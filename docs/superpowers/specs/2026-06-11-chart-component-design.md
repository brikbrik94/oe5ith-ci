# Chart-Komponente — Verlaufsdarstellung für Statistiken

**Datum:** 2026-06-11
**Status:** Design abgenommen
**Zielversion:** v1.13.0 (MINOR — neue Komponente + neue Token, abwärtskompatibel)

---

## Ziel & Kontext

Das Service-Dashboard (`docs/service-dashboard.md`) zeigt aktuell nur Momentaufnahmen.
Für gewisse Statistiken wird eine kurze Historie gespeichert; diese soll grafisch als
Verlauf dargestellt werden. Dafür braucht das CI eine **datengetriebene Diagramm-Definition**.

Da `oe5ith-ci` ein reines CSS/HTML-System ohne Build-Step ist (Doc = Quelle, App liefert
Werte), definiert die Komponente **Struktur + Styling** eines Diagramms (Klassen, Achsen,
Container, Token). Die konsumierende App generiert die SVG-Geometrie aus den Daten; das CI
liefert ausschließlich Stroke/Fill/Farbe über Token — nie eine fertige JS/TS-Charting-Library.

### Entscheidungen aus dem Brainstorming

- **Diagrammtypen:** Sparkline, Linie, Balken, Fläche (alle vier).
- **Rendering:** Inline-SVG (App generiert `<polyline>`/`<rect>`/`<path>`).
- **Platzierung:** eigener Panel-Typ „Verlauf", Sparkline in `svc-data-cell`, Sparkline in
  Übersichts-Kachel.
- **Features:** Schwellwert-Färbung, mehrere Datenreihen, Hover-Tooltip/Datenpunkte,
  Achsen + Beschriftung.
- **Architektur:** eigenständige, wiederverwendbare `chart`-Komponente (`chart-*`-Präfix),
  nicht ans Dashboard gebunden. Sparkline ist nur ein Modifier von `chart`, kein Sonderfall.

---

## 1. Komponente & Dateien

**Neue Dateien:**

- `css/chart.css` — alle `chart-*`-Klassen (unabhängig vom Dashboard, nach `common.css` ladbar)
- `docs/chart.md` — Doc nach `docs/doc-standard.md` (G1–G4)
- `components/chart.html` — Referenz-/Verifikations-HTML (alle Typen + Zustände)

**Änderungen an bestehenden Dateien:**

- `css/common.css` — neue Chart-Token (Definition)
- `docs/tokens.md` — neue Chart-Token (Doku)
- `css/index.css` — `@import "chart.css";` nach `cards.css`, vor `service-dashboard.css`
- `docs/registry.json` — neuer Eintrag, Kategorie `component`
- `docs/service-dashboard.md` + `components/service-dashboard-*.html` — Panel-Typ „Verlauf"
  und Sparkline-Platzierung (siehe Abschnitt 5)
- `CHANGELOG.md` — Eintrag unter `Added`

### Token (`common.css` + `docs/tokens.md`)

Nur Werte mit klarer Semantik, mehrfach genutzt:

| Token | Wert | Zweck |
|---|---|---|
| `--chart-1` | `var(--accent)` (#3b82f6) | Datenreihe 1 (Default-Serie) |
| `--chart-2` | `#14b8a6` (Teal) | Datenreihe 2 |
| `--chart-3` | `#a855f7` (Violett) | Datenreihe 3 |
| `--chart-4` | `#f59e0b` (Amber) | Datenreihe 4 |
| `--chart-grid` | `var(--border)` | Gridlines |
| `--chart-axis` | `var(--subtle)` | Achsenlinien + Tick-Labels |
| `--chart-area-opacity` | `0.15` | Füll-Transparenz für Bereichsdiagramme |

Schwellwert-Färbung nutzt **bestehende** Token (`--success`/`--warning`/`--danger`) — keine neuen.

---

## 2. Struktur (G2)

Die App generiert die SVG-Geometrie (Koordinaten aus Daten); die CI liefert Klassen + Styling.
Zwei Ausprägungen einer Komponente.

### A) Volldiagramm (Panel-Typ „Verlauf") — Linie / Fläche / Balken

```text
.chart[.chart-area|.chart-bar]                       (Wurzel; ohne Modifier = Linie)
├── .chart-header                                     (Optional)
│   ├── .chart-title                                  (Optional)
│   └── .chart-legend                                 (Optional, ab ≥2 Serien Pflicht)
│       └── .chart-legend-item.chart-s1…s4            (n×)
│           ├── .chart-legend-swatch
│           └── span  (Serien-Name)
├── .chart-plot                                       (Pflicht — Höhen-/Aspect-Container)
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
│           └── circle.chart-point                    (Optional, n× — Hover-Punkte)
├── .chart-tooltip                                    (Optional — von App ein-/ausgeblendet)
│   ├── .chart-tooltip-label
│   └── .chart-tooltip-value
└── .chart-empty                                      (Optional — „Keine Daten")
```

### B) Sparkline (in `svc-data-cell` / Übersichts-Kachel)

```text
.chart.chart-sparkline[.chart-area]                  (Wurzel — achsenlos, kompakt)
└── svg.chart-svg
    ├── path.chart-area-fill                          (nur bei .chart-area)
    ├── polyline.chart-line
    └── circle.chart-point.chart-point-last           (Optional — letzter Wert markiert)
```

Die Sparkline lässt Header, Legende, Achsen, Grid und Tooltip bewusst weg — sie ist dieselbe
Komponente im Minimal-Modus.

**Tooltip-Entscheidung:** `.chart-tooltip` ist ein CI-positioniertes `div` (App toggelt
Sichtbarkeit via `.is-visible`), kein SVG-`<title>`.

---

## 3. Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.chart` | Wurzel-Container der Komponente | Pflicht | `.chart-area`, `.chart-bar`, `.chart-sparkline` |
| `.chart-header` | Kopfzeile (Titel + Legende) | Optional | — |
| `.chart-title` | Diagramm-Titel (0.8rem, `--muted`) | Optional | — |
| `.chart-legend` | Legenden-Leiste | Optional (Pflicht ab ≥2 Serien) | — |
| `.chart-legend-item` | Ein Legenden-Eintrag | Optional | `.chart-s1`–`.chart-s4` |
| `.chart-legend-swatch` | Farbkästchen (erbt Serienfarbe) | Pflicht (im Item) | — |
| `.chart-plot` | Höhen-/Aspect-Container für das SVG | Pflicht | — |
| `.chart-svg` | Das `<svg>` selbst (skaliert via viewBox) | Pflicht | — |
| `.chart-grid` | Gruppe der Gridlines | Optional | — |
| `.chart-gridline` | Einzelne Gridline (`--chart-grid`) | Optional | — |
| `.chart-axis` | Achsen-Gruppe | Optional | `.chart-axis-x`, `.chart-axis-y` |
| `.chart-axis-line` | Achsenlinie (`--chart-axis`) | Optional | — |
| `.chart-tick-label` | Tick-Beschriftung (0.62rem, `--subtle`) | Optional | — |
| `.chart-series` | Gruppe einer Datenreihe (setzt Serienfarbe) | Pflicht | `.chart-s1`–`.chart-s4` |
| `.chart-line` | Linie (`polyline`, stroke = Serienfarbe) | Pflicht (Linie/Fläche) | `.chart-ok`, `.chart-warn`, `.chart-danger` |
| `.chart-area-fill` | Füllfläche (`path`, Serienfarbe @ `--chart-area-opacity`) | Optional (nur `.chart-area`) | `.chart-ok`, `.chart-warn`, `.chart-danger` |
| `.chart-bar-rect` | Einzelner Balken (`rect`, fill = Serienfarbe) | Pflicht (nur `.chart-bar`) | `.chart-ok`, `.chart-warn`, `.chart-danger` |
| `.chart-point` | Datenpunkt (`circle`) für Hover/Markierung | Optional | `.chart-point-last` |
| `.chart-tooltip` | Schwebende Wertanzeige (CI-positioniert, App toggelt) | Optional | `.is-visible` |
| `.chart-tooltip-label` | Tooltip-Bezeichnung (`--muted`) | Pflicht (im Tooltip) | — |
| `.chart-tooltip-value` | Tooltip-Wert (`--text`, 600) | Pflicht (im Tooltip) | — |
| `.chart-empty` | „Keine Daten"-Hinweis (`--subtle`, zentriert) | Optional | — |

---

## 4. Zustände & Varianten (G4)

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

**Status-gewinnt-Regel:** Schwellwert-Färbung (`.chart-ok/-warn/-danger`) überschreibt die
Serienfarbe (`.chart-s1`–`-s4`). Bei einer Einzelserie mit Status-Logik nutzt man die
Status-Modifier; bei Multi-Serien-Vergleich die `s1–s4`. Beide am selben Element zu mischen
ist nicht vorgesehen — **Status gewinnt** (höhere CSS-Spezifität bzw. Reihenfolge).

---

## 5. Dashboard-Integration

Änderungen in `docs/service-dashboard.md` (+ `components/service-dashboard-*.html` als
Verifikation). `service-dashboard.md` regelt nur **Platzierung**; die Chart-Mechanik bleibt
in `docs/chart.md` (einzige Quelle).

### 5.1 Neuer 5. Panel-Typ auf der Detail-Seite

Erweiterung der Tabelle „Festes Set an Panel-Typen":

| Panel-Typ | Inhalt | Pflicht/Optional |
|---|---|---|
| **Verlauf / Historie** | Ein `.chart`-Volldiagramm (Linie/Fläche/Balken) im `.panel-body`, das die kurze gespeicherte Historie einer Kennzahl zeigt | Optional |

Regeln:

- Genau **ein `.chart`** pro Verlauf-Panel (analog Ein-Endpunkt-Regel).
- `.panel-title` (Icon + Bezeichnung) bleibt Pflicht; die optionale Zeitspanne (z. B.
  „letzte 24 h") gehört in `span.panel-meta` im `.panel-header-right`.
- Bezieht sich — wie alle Panels — auf den **einen** Endpunkt der Seite.

### 5.2 Sparkline in `svc-data-cell`

Erweiterung der Zellen-Regel: eine `.svc-data-cell` darf **optional** eine
`.chart.chart-sparkline` als **letztes** Kind enthalten. Die Regel „ein Wert = eine Zelle"
bleibt — die Sparkline ist der Verlauf desselben Werts, kein zweiter Wert.

```text
.svc-data-cell
├── span.svc-data-label
├── span.svc-data-value[.success|.danger]
├── span.svc-data-sub                       (Optional)
└── .chart.chart-sparkline                   (Optional — Verlauf desselben Werts)
```

### 5.3 Sparkline in Übersichts-Kachel

Erweiterung von `.card-dashboard`: eine Kachel darf optional eine `.chart.chart-sparkline`
als **letztes** Kind vor dem Pfeil-Icon enthalten (nach `svc-status-line`, vor
`card-dashboard-arrow`).

---

## 6. Daten-Vertrag, Barrierefreiheit & Verifikation

### Daten-Vertrag (App ↔ CI-Klassen)

Die Doc legt fest, *was* die App liefern muss, damit das Styling greift — ohne JS/TS
vorzuschreiben:

- **Koordinatensystem:** `.chart-svg` nutzt `viewBox="0 0 W H"` plus `preserveAspectRatio`;
  die App rechnet Datenwerte → viewBox-Koordinaten. CI-Klassen setzen keine Geometrie, nur
  Stroke/Fill/Farbe.
- **Linie/Fläche:** `polyline points="x,y …"`; Fläche zusätzlich `path d="…"` (zur Baseline
  geschlossen).
- **Balken:** je Wert ein `rect` mit `x/y/width/height`.
- **Serienfarbe** kommt aus der Modifier-Klasse (`chart-s1`–`s4` bzw. Status), **nie** aus
  Inline-`fill`/`stroke` — sonst bricht die Token-Bindung (CLAUDE.md: keine hardcodierten Farben).
- **Tooltip:** App positioniert `.chart-tooltip` (Inline-`left`/`top` erlaubt — Position ist
  Daten, keine Farbe/Token) und schaltet `.is-visible`.

### Barrierefreiheit

- `.chart-svg` erhält `role="img"` + `aria-label` (Kurzbeschreibung des Verlaufs).
- Sparklines in Zellen/Kacheln sind dekorativ-ergänzend → `aria-hidden="true"` zulässig, da
  der Wert bereits als Text in der Zelle steht.

### Verifikation (`components/chart.html`)

Zeigt alle Typen und Zustände nebeneinander — Linie (Einzelserie), Fläche, Balken,
Multi-Serie mit Legende, Status-Färbung (ok/warn/danger), Sparkline (Zelle + Kachel),
`chart-empty`. Dient als Sicht- und G1-Vollständigkeitsprüfung.

### Konsistenz & Release

- `docs/registry.json`-Eintrag ergänzen; `python3 scripts/cli/check_consistency.py` muss grün sein.
- Version **MINOR** → v1.13.0; `CHANGELOG.md`-Eintrag unter `Added`.

---

## Offene Punkte

Keine — alle Designabschnitte wurden im Brainstorming einzeln abgenommen.

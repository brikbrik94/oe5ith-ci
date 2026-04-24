# Seitenstruktur & Layout

**Referenz-Datei:** `components/page.html` *(folgt)*  
**CSS:** `css/page.css`  
**Status:** definiert · v1.0

---

## Überblick

Fünf Seitentypen mit jeweils eigener Struktur:

| Typ | Beispiel | Sidebar | Page-Header |
|---|---|---|---|
| Detail-Seite | Geocoding API, Spectrum, POCSAG | ja | Titel + Untertitel + Meta |
| Dashboard | System Overview | ja | Titel |
| Karten-Grid | Tiles Registry | ja | Titel + Column-Groups |
| Landing | cloud.oe5ith.at | nein | zentrierter Titel |
| Karte | karte.oe5ith.at | ja (Layer-Panel) | — (Topbar-Controls) |

---

## Page-Header

Immer der erste Element im `.page-content` Bereich.
`border-bottom` trennt klar vom Inhalt.

```html
<div class="page-header">

  <!-- Links: Titel + optionaler Untertitel -->
  <div class="page-header-left">
    <h1 class="page-title">SDR <span>POCSAG Feed</span></h1>
    <p class="page-subtitle">Dekodierte Funkruf-Nachrichten (letzte 24h)</p>
  </div>

  <!-- Rechts: Meta-Info + optionale Action-Buttons -->
  <div class="page-header-right">
    <span class="page-meta">Zuletzt: 24.4.2026 13:47</span>
    <button class="page-action">
      <i class="fa-solid fa-rotate"></i> Aktualisieren
    </button>
  </div>

</div>
```

### Tokens

| Eigenschaft | Wert |
|---|---|
| `padding-top` | `20px` |
| `padding-bottom` | `14px` |
| `padding-left/right` | `40px` (Mobile: `16px`) |
| `border-bottom` | `1px solid --border` |
| Titel | `1.6rem / 300` — Akzent-Span `700 / --accent` |
| Untertitel | `0.78rem / --subtle` |
| Meta | `0.72rem / --subtle` |

### Page-Header Action-Button

Für sekundäre Aktionen die sich auf die gesamte Seite beziehen
(z.B. "Liste aktualisieren", "Exportieren", "Alle laden").

```html
<!-- Standard -->
<button class="page-action">
  <i class="fa-solid fa-rotate"></i> Aktualisieren
</button>

<!-- Loading-Zustand -->
<button class="page-action loading">Aktualisieren</button>
```

**Regeln:**
- Maximale Höhe: `30px` — kleiner als normale Buttons (36px)
- Farbe: Accent-Subtle — kein Primary-Button im Header
- Nur für seitenweite Aktionen — Element-spezifische Aktionen gehören in den Content
- Maximale 1–2 Action-Buttons im Header

---

## Content-Body

```html
<div class="content-body">
  <!-- Panels, Card-Grids, Column-Groups -->
</div>
```

```css
.content-body {
  padding: 20px 40px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
```

---

## Panel

Section-Container für inhaltliche Abschnitte.

```html
<div class="panel">

  <div class="panel-header">
    <div class="panel-title">
      <i class="fa-solid fa-table"></i>
      Nachrichten
    </div>
    <div class="panel-header-right">
      <span class="panel-meta">512 Einträge</span>
      <!-- Badge, Button etc. -->
    </div>
  </div>

  <!-- Standard-Padding -->
  <div class="panel-body">
    Inhalt...
  </div>

  <!-- Oder: kein Padding (für Tabellen, Code-Blöcke) -->
  <div class="panel-body-flush">
    <table class="ci-table">...</table>
  </div>

</div>
```

**Regeln:**
- Immer `overflow: hidden` — Inhalt darf nie über den Rand stehen
- Panel-Header ist optional — bei Panels ohne Titel direkt `.panel-body` verwenden
- Icon im Panel-Titel: Font Awesome, `color: --accent`

---

## Tabelle

CI-konforme Tabelle. Hintergrund `--panel` (#202020).
Immer in `.panel-body-flush` verwenden.

```html
<div class="panel">
  <div class="panel-header">
    <div class="panel-title">Nachrichten-Übersicht</div>
  </div>
  <div class="panel-body-flush">
    <table class="ci-table">
      <thead>
        <tr>
          <th class="mono">Zeitstempel</th>
          <th class="mono">Frequenz</th>
          <th class="mono sortable sort-asc">RIC/ADR</th>
          <th>Nachricht</th>
        </tr>
      </thead>
      <tbody>
        <tr class="highlight">
          <td class="mono">24.4.2026 13:46</td>
          <td class="mono">168.075 MHz</td>
          <td class="mono">1056019</td>
          <td>BH Jurist benötigt 4020 Linz…</td>
        </tr>
        <tr>
          <td class="mono">24.4.2026 13:38</td>
          <td class="mono">168.075 MHz</td>
          <td class="mono">160311</td>
          <td class="empty">–</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

### Tabellen-Tokens

| Eigenschaft | Wert |
|---|---|
| Hintergrund | `--panel` (#202020) |
| Header-Zeile | `0.68rem / 700 / uppercase / --subtle` |
| Daten-Zeilen | `0.82rem / --muted` (erste Spalte: `--text`) |
| Zellen-Padding | `8px 14px` |
| Zeilen-Trenner | `1px solid rgba(255,255,255,0.03)` |
| Hover | `background: rgba(255,255,255,0.025)` |
| `.highlight` | alle `td` in `--text` statt `--muted` |
| `.mono` | `--font-mono`, `0.76rem` |
| `.empty` | Farbe `--subtle` |

---

## Column-Groups

Für Seiten mit mehreren thematischen Spalten (Tiles Registry, Font-Galerie).

```html
<div class="content-body">
  <div class="col-groups col-groups-3">

    <div class="col-group">
      <h2 class="col-group-label">Basemap</h2>
      <!-- Cards hier -->
    </div>

    <div class="col-group">
      <h2 class="col-group-label">Overlay</h2>
    </div>

    <div class="col-group">
      <h2 class="col-group-label">Elevation</h2>
    </div>

  </div>
</div>
```

| Modifier | Spalten |
|---|---|
| `.col-groups-2` | 2 |
| `.col-groups-3` | 3 (Tablet: 2) |
| `.col-groups-4` | 4 (Tablet: 2, Mobile: 1) |

---

## Landing Page

Ohne Sidebar. Inhalt zentriert.

```html
<!-- Kein .layout, kein .sidebar -->
<main class="landing-body">
  <h1 class="landing-title">Willkommen im <span>Cloud Portal</span></h1>
  <!-- Card-Grid hier -->
  <div class="card-grid">...</div>
</main>
```

```css
.landing-body {
  padding: 60px 40px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
```

---

## Vollständige Seiten-Struktur

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <link rel="stylesheet" href="css/common.css">
  <link rel="stylesheet" href="css/topbar.css">
  <link rel="stylesheet" href="css/sidebar.css">
  <link rel="stylesheet" href="css/page.css">
  <!-- weitere Komponenten nach Bedarf -->
</head>
<body>

  <header class="topbar">...</header>

  <div class="layout">
    <nav class="sidebar">...</nav>

    <main class="page-content">

      <div class="page-header">
        <div class="page-header-left">
          <h1 class="page-title">SDR <span>POCSAG Feed</span></h1>
          <p class="page-subtitle">Dekodierte Funkruf-Nachrichten</p>
        </div>
        <div class="page-header-right">
          <span class="page-meta">Zuletzt: 24.4.2026 13:47</span>
          <button class="page-action">
            <i class="fa-solid fa-rotate"></i> Aktualisieren
          </button>
        </div>
      </div>

      <div class="content-body">

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">
              <i class="fa-solid fa-table"></i> Nachrichten
            </div>
          </div>
          <div class="panel-body-flush">
            <table class="ci-table">
              <thead>
                <tr>
                  <th class="mono">Zeitstempel</th>
                  <th>Nachricht</th>
                </tr>
              </thead>
              <tbody>
                <tr><td class="mono">24.4.2026 13:46</td><td>...</td></tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </main>
  </div>

</body>
</html>
```

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-24 | Initiale Definition. 5 Seitentypen. Page-Header, Content-Body, Panel, Tabelle, Column-Groups, Landing. |

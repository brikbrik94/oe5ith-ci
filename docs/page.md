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
  <!-- Mit --scroll für horizontal scrollbare Tabellen auf Mobile -->
  <div class="panel-body-flush panel-body-flush--scroll">
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
Immer in `.panel-body-flush.panel-body-flush--scroll` verwenden — sorgt für horizontales Scrolling auf Mobile statt Zeilen-Stacking.

```html
<div class="panel">
  <div class="panel-header">
    <div class="panel-title">Nachrichten-Übersicht</div>
  </div>
  <div class="panel-body-flush panel-body-flush--scroll">
    <table class="ci-table ci-table--sortable">
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

### Sortable Contract

CSS liefert die visuellen States — echte Sortierlogik ist **JS-Pflicht**.

| Klasse | Ebene | Bedeutung |
|---|---|---|
| `.ci-table--sortable` | `<table>` | JS-Marker: diese Tabelle hat sortierbare Spalten |
| `.sortable` | `<th>` | Spalte ist sortierbar (Cursor, User-Select) |
| `.sort-asc` | `<th>` | Spalte ist aktiv aufsteigend sortiert (↑ in `--accent`) |
| `.sort-desc` | `<th>` | Spalte ist aktiv absteigend sortiert (↓ in `--accent`) |

**JS-Verantwortlichkeiten:**
- Tabelle per `.ci-table--sortable` selektieren
- Bei Klick auf `th.sortable`: `.sort-asc` / `.sort-desc` auf dem aktiven `<th>` toggeln, auf allen anderen entfernen
- DOM-Zeilen (`<tbody> <tr>`) nach dem Sortierwert neu anordnen

---

## Editierbare Tabellenzellen

Erweiterung von `.ci-table` um zwei inline-bearbeitbare Zellen-Varianten: fester
Wertebereich per Dropdown (`.cell-select`) oder einzeiliger Freitext
(`.cell-text`). Dual-Markup pro Zelle — Anzeige- und Eingabeelement liegen
gleichzeitig im DOM, der Zustand wird ausschließlich über CSS-Klassen auf dem
`<td>` gesteuert (kein DOM-Swap per `innerHTML`).

**Keine Persistenz-Logik in der CI.** Wie ein Commit gespeichert wird
(API-Call, Optimistic Update, Fehlerbehandlung), ist Sache der Website —
analog zum Sortable Contract oben: CSS liefert die Zustände, JS-Pflicht ist
die eigentliche Logik.

### Struktur

```text
<td class="cell-editable cell-select|cell-text">
├── .cell-value                    (Pflicht — Anzeige, role="button", tabindex="0")
├── <select class="form-select">   (Pflicht bei .cell-select)
├── <input class="form-input">     (Pflicht bei .cell-text)
└── .cell-error-tip                (Optional — nur bei is-error, role="alert")
```

### Elemente

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.cell-editable` | Basis-Klasse auf `<td>` — aktiviert den Zustands-Kontrakt | Pflicht | `.cell-select`, `.cell-text` |
| `.cell-select` | Variante: Dropdown mit festem Wertebereich | Pflicht (genau eine der beiden Varianten) | — |
| `.cell-text` | Variante: einzeiliger Freitext | Pflicht (genau eine der beiden Varianten) | — |
| `.cell-value` | Anzeigeelement im Ruhezustand, `role="button" tabindex="0"` | Pflicht | — |
| `<select class="form-select">` | Eingabeelement der `.cell-select`-Variante, unverändert aus `docs/forms.md` | Pflicht bei `.cell-select` | — |
| `<input class="form-input" type="text">` | Eingabeelement der `.cell-text`-Variante, unverändert aus `docs/forms.md` | Pflicht bei `.cell-text` | — |
| `.cell-error-tip` | Fehlermeldung, `role="alert"`, per `aria-describedby` mit dem Eingabeelement verknüpft | Optional (nur bei `.is-error`) | — |

### Reihenfolge & Platzierung

- `.cell-value` steht immer als **erstes** Kind im `<td>`, direkt gefolgt vom Eingabeelement (`<select class="form-select">` oder `<input class="form-input">`). `.cell-error-tip` ist immer das **letzte** Kind, wenn vorhanden.
- `.cell-error-tip` wird **erst bei Eintritt in `.is-error`** ins DOM eingefügt (bzw. sichtbar) — nicht vorab unsichtbar mitgerendert. Position: `position: absolute; bottom: 100%; left: 0;` — der Tooltip öffnet **oberhalb** der Zelle, linksbündig zur Zellkante, nie nach rechts oder unten (Tabellenzeilen darunter dürfen nicht verdeckt werden).
- Beim Verlassen des Fehlerzustands (erneuter Klick auf `.cell-value`) wird `.cell-error-tip` aus dem DOM entfernt und `aria-describedby` vom Eingabeelement wieder entfernt — kein verwaistes `aria-describedby` auf ein nicht mehr existierendes Element.
- Innerhalb einer Tabellenzeile ist die Reihenfolge der Spalten frei wählbar — `.cell-editable`-Spalten dürfen beliebig mit normalen, nicht editierbaren `<td>`-Spalten gemischt werden (siehe Beispiel `components/table-editable.html`).

### Zustände (auf `<td class="cell-editable …">`)

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Ruhezustand | *(kein Modifier)* | Zelle ist editierbar, aber nicht aktiv in Bearbeitung. `.cell-value` sichtbar, Eingabeelement `display:none`, Hintergrund `--accent-subtle` als Discoverability-Hinweis. |
| Editing | `.is-editing` | Nutzer hat die Zelle aktiviert (Klick/Enter/Space auf `.cell-value`). Eingabeelement sichtbar + fokussiert, `.cell-value` versteckt. |
| Saving | `.is-saving` | Commit-Request läuft (transient). Eingabeelement `opacity:0.6`, nicht interagierbar. |
| Saved | `.is-saved` | Commit war erfolgreich (transient, JS entfernt die Klasse nach eigenem Timeout, empfohlen ~1200 ms). Kurzer Hintergrund-Flash `--accent-subtle-md`. |
| Error | `.is-error` | Commit oder Validierung ist fehlgeschlagen und bleibt bestehen, bis erneut editiert wird. Rahmen `--danger`, Hintergrund `--danger-subtle`, `.cell-error-tip` sichtbar. |

**Zustandsübergänge (Text-Regel):**

```
Ruhezustand ──Klick/Enter/Space──▶ is-editing
is-editing ──Blur/Change/Enter──▶ is-saving
is-editing ──Escape (nur .cell-text)──▶ Ruhezustand (kein Commit, Wert zurückgesetzt)
is-saving ──Commit OK──▶ is-saved ──Timeout──▶ Ruhezustand
is-saving ──Commit fehlgeschlagen──▶ is-error
is-error ──erneuter Klick──▶ is-editing
```

Der Zustands-Satz ist für `.cell-select` und `.cell-text` identisch.

### JS-Verantwortlichkeiten (Pflicht)

- Klick oder `Enter`/`Space` auf `.cell-value`: `.is-editing` auf dem `<td>` setzen, Eingabeelement fokussieren.
- `change` (Select) / `blur` oder `Enter` (Input): `.is-editing` entfernen, `.is-saving` setzen, Commit auslösen.
- `Escape` nur bei `.cell-text`: Eingabewert auf zuletzt committeten Wert zurücksetzen, `.is-editing` entfernen, kein Commit.
- Commit erfolgreich: `.is-saving` entfernen, `.cell-value`-Text aktualisieren, `.is-saved` setzen und nach ~1200 ms wieder entfernen.
- Commit fehlgeschlagen: `.is-saving` entfernen, `.is-error` setzen, Fehlertext in `.cell-error-tip` schreiben.
- Klick auf `.cell-value` im `.is-error`-Zustand: `.is-error` entfernen, zurück in `.is-editing`.

### Beispiel

```html
<td class="cell-editable cell-select">
  <span class="cell-value" tabindex="0" role="button">Aktiv</span>
  <select class="form-select" aria-label="Status">
    <option value="active" selected>Aktiv</option>
    <option value="inactive">Inaktiv</option>
  </select>
</td>
```

### Regeln

1. Dual-Markup ist Pflicht — kein `innerHTML`-Ersatz des Zellinhalts beim Zustandswechsel (Fokus-Erhalt, Barrierefreiheit).
2. `.cell-select`/`.cell-text` nutzen unverändert `.form-select`/`.form-input` (`docs/forms.md`) — kein eigenes Input-Styling in `page.css`.
3. `.cell-text` ist bewusst einzeilig. Für mehrzeilige Werte ist dies nicht das passende Pattern.
4. Persistenz (API-Call, Fehlerbehandlung bei Netzwerkfehlern) ist Sache der Website, nicht der CI.
5. `.form-select`/`.form-input` in editierbaren Zellen bekommen `aria-label` aus dem Spalten-Header-Kontext.

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
| 2026-07-20 | Editierbare Tabellenzellen ergänzt — `.cell-select`, `.cell-text`, Zustands-Kontrakt (is-editing/is-saving/is-saved/is-error). |
| 2026-04-24 | Initiale Definition. 5 Seitentypen. Page-Header, Content-Body, Panel, Tabelle, Column-Groups, Landing. |

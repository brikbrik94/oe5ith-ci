# Statistik-Explorer (Typ 7)

**CSS:** `css/stats.css`  
**Referenz:** `components/stats-explorer.html`  
**Seitentyp:** Typ 7 — Statistik-Explorer  
**Status:** definiert · v1.15

---

## Überblick

Pattern für Seiten, die eine konfigurierbare Statistik-Tabelle mit fixiertem Steuer-Feld
darstellen. Das Steuer-Feld (Tabellenwahl, Zeitraum, Filter) bleibt fest am oberen Rand;
die Tabelle darunter scrollt in sich und hat einen Sticky-Header. Die Seite selbst scrollt
nicht mehr.

Typische Anwendungsfälle: Alarmierungsstatistik, Empfangsstatistik, Nutzungsauswertungen,
jede tabellarische Auswertung mit wechselbarem Datensatz und Zeitraumfilter.

**Wann verwenden:**
- Hauptinhalt ist eine einzelne, sortierbare Datentabelle.
- Die Tabelle wechselt je nach Auswahl (z. B. Tabellenwahl per `<select>` oder Preset).
- Zusätzlich gibt es eine Zeitraumauswahl (Preset + optionale manuelle Datumseingabe).
- Der Nutzer erwartet eine stets sichtbare Steuerleiste ohne Scrollen.

**Wann nicht verwenden:**
- Mehrere unabhängige Datentabellen nebeneinander → Typ 4 (Karten-Grid) oder Typ 1.
- Auswahlliste + abhängiger Detailbereich → Typ 6 (Split-View).
- Nur eine einfache, kurze Tabelle ohne Filtersteuerung → Typ 2 (Listen-Seite).
- Map-Seiten → eigenes Layout (kein `css/page.css`).

---

## Höhen- und Scroll-Modell

Der Statistik-Explorer aktiviert einen **Fixed-Height-Modus automatisch** — ohne
zusätzliche Klassen am Seiten-Wrapper. Sobald `.stats-explorer` im DOM vorhanden ist,
greift in `css/stats.css` ein `:has(.stats-explorer)`-Selektor, der `.page-content` auf
`display: flex; flex-direction: column; overflow: hidden` setzt und `.content-body`
auf `flex: 1; min-height: 0; overflow: hidden`.

Dadurch nehmen das Steuer-Feld und die Tabelle die verbleibende Viewport-Höhe vollständig
ein. Nur die Tabelle scrollt intern; `css/common.css` und `css/page.css` bleiben unverändert.

---

## Element-Tabelle (G1)

### Neue `.stats-*`-Klassen (aus `css/stats.css`)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.stats-explorer` | Flex-Container (Spalte) für Steuer-Feld und Tabelle; aktiviert Fixed-Height-Modus | Pflicht | — |
| `.stats-controls` | Steuer-Feld-Leiste, fix oben, scrollt nicht mit; Flex-Row mit `flex-wrap` | Pflicht | — |
| `.stats-control-group` | Gruppiert Label + Steuerelemente einer Steuerdimension (z. B. „Tabelle", „Zeitraum") | Pflicht (1–n) | `.stats-search` |
| `.stats-control-group.stats-search` | Suchgruppe: wächst (`flex: 1`), drückt `.stats-actions` nach rechts | Optional | — |
| `.stats-control-row` | Flex-Zeile mit den eigentlichen Steuerelementen direkt unter dem Label | Pflicht (je Gruppe) | — |
| `.stats-range-sep` | Trennzeichen „–" zwischen zwei Datumseingaben im Zeitraumbereich | Optional | — |
| `.stats-actions` | Rechtsbündige Aktions-Buttons (Aktualisieren, Export); `margin-left: auto` | Optional | — |
| `.stats-table-panel` | Modifier für `.panel`; füllt Resthöhe (`flex: 1`), beinhaltet die scrollende Tabelle | Pflicht | — |
| `.stats-empty` | Platzhalter-Text, wenn die Tabelle keine Daten enthält; ersetzt den gefüllten `<tbody>` | Optional (Leerzustand) | — |

### Wiederverwendete Klassen aus anderen Modulen

| Element / Klasse | Zweck | Pflicht/Optional | Heimat-Doku |
|---|---|---|---|
| `.panel` | Karten-Container für den Tabellenbereich; zusammen mit `.stats-table-panel` verwenden | Pflicht | `docs/page.md` |
| `.panel-body-flush` | Panel-Body ohne inneres Padding — Pflicht-Wrapper um `.panel-body-flush--scroll` | Pflicht | `docs/page.md` |
| `.panel-body-flush--scroll` | Aktiviert vertikales + horizontales Scroll im Panel; wird von `.stats-table-panel` auf `flex: 1` gesetzt | Pflicht | `docs/page.md` |
| `.ci-table` | Standard-Datentabelle | Pflicht | `docs/page.md` |
| `.ci-table--sortable` | Aktiviert sortierbare Spaltenköpfe; `.sortable`-Klasse an `<th>` erforderlich | Pflicht | `docs/page.md` |
| `.sortable` | Markiert einen `<th>` als sortierbar | Pflicht (je sort. Spalte) | `docs/page.md` |
| `.sort-asc` / `.sort-desc` | Zeigt aktive Sortierrichtung am `<th>` an | Optional (per JS setzen) | `docs/page.md` |
| `.mono` | Monospace-Schrift für Timestamps, IDs, Zähler | Optional | `docs/typography.md` |
| `.segmented` | Segmented-Control-Container für Preset-Auswahl (z. B. Zeitraum) | Optional | `docs/forms.md` |
| `.segmented-btn` | Einzelner Preset-Button im Segmented Control | Optional (1–n) | `docs/forms.md` |
| `.segmented-btn.active` | Markiert den aktiven Preset | Optional | `docs/forms.md` |
| `.form-select` | Dropdown für Tabellenwahl oder andere Auswahl | Optional | `docs/forms.md` |
| `.form-input` | Texteingabe, Sucheingabe oder Datumseingabe | Optional | `docs/forms.md` |
| `.ci-label` | Label über einer Steuergruppe | Optional | `docs/forms.md` |
| `.btn` | Basis-Button-Klasse | Optional | `docs/buttons.md` |
| `.btn-ghost` | Sekundärer Ghost-Button (z. B. „Aktualisieren") | Optional | `docs/buttons.md` |
| `.btn-secondary` | Sekundärer Button (z. B. „Export") | Optional | `docs/buttons.md` |
| `.btn-sm` | Kleine Button-Variante | Optional | `docs/buttons.md` |

---

## Struktur / Verschachtelung (G2)

```text
.content-body
└── .stats-explorer                          (Pflicht — einziges direktes Kind)
    ├── .stats-controls                      (Pflicht — Steuer-Feld, fix oben)
    │   ├── .stats-control-group             (Pflicht, 1–n)
    │   │   ├── .ci-label                    (Optional — Label über der Gruppe)
    │   │   └── .stats-control-row           (Pflicht — enthält form-select /
    │   │       ├── .form-select             │  segmented / form-input)
    │   │       ├── .segmented               │
    │   │       │   └── .segmented-btn [.active]
    │   │       ├── .form-input              │
    │   │       └── .stats-range-sep         (Optional — Trennzeichen zwischen Datumsfeldern)
    │   └── .stats-actions                   (Optional — rechtsbündig, letztes Kind)
    │       ├── .btn.btn-ghost.btn-sm        (sekundäre Aktion, z. B. Aktualisieren)
    │       └── .btn.btn-secondary.btn-sm    (primäre Export-Aktion)
    └── section.panel.stats-table-panel      (Pflicht — Tabellenbereich)
        └── .panel-body-flush.panel-body-flush--scroll
            ├── table.ci-table.ci-table--sortable   (Normalzustand)
            │   ├── thead
            │   │   └── tr > th.sortable [.sort-asc|.sort-desc] [.mono]
            │   └── tbody
            │       └── tr > td [.mono]
            └── .stats-empty                (Leerzustand — statt table)
```

---

## Reihenfolge & Platzierung (G3)

- `.stats-explorer` ist das **einzige direkte Kind** von `.content-body`. Kein anderes
  Element darf auf gleicher Ebene stehen, da der Fixed-Height-Modus exklusiv wirkt.
- `.stats-controls` kommt **vor** `.stats-table-panel` im DOM — das Steuer-Feld ist
  stets oberhalb der Tabelle sichtbar.
- Innerhalb von `.stats-controls` stehen die `.stats-control-group`-Elemente von links
  nach rechts in der Reihenfolge der inhaltlichen Priorität (zuerst Tabellenwahl, dann
  Zeitraum, dann Filter/Suche). `.stats-actions` steht als **letztes Kind** und erhält
  automatisch `margin-left: auto`, was es rechtsbündig ausrichtet.
- Innerhalb jeder `.stats-control-group` steht `.ci-label` **vor** `.stats-control-row`.
- `.stats-range-sep` steht **zwischen** zwei `.form-input`-Datumseingaben in der
  `.stats-control-row` des Zeitraum-Steuerblocks.
- Im Aktionsbereich gilt die projektweite Button-Konvention: der primäre Button
  (z. B. „Export" als `.btn-secondary`) steht rechts, der sekundäre Ghost-Button
  (z. B. „Aktualisieren" als `.btn-ghost`) steht links davon.
- `.stats-table-panel` muss als `<section>` oder `<div>` ausgeführt werden und trägt
  **beide** Klassen `panel` und `stats-table-panel` — `panel` liefert das Basis-Styling,
  `stats-table-panel` überschreibt Höhe und Overflow.

---

## Zustände & Varianten (G4)

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Preset aktiv | `.segmented-btn.active` | Aktuell gewählter Zeitraum-Preset; per JS setzen |
| Sortierung aufsteigend | `.sort-asc` an `<th>` | Spalte wird aufsteigend sortiert; per JS setzen |
| Sortierung absteigend | `.sort-desc` an `<th>` | Spalte wird absteigend sortiert; per JS setzen |
| Leerzustand | `.stats-empty` statt `<table>` | Keine Daten für den gewählten Filter / Zeitraum |
| Fixed-Height aktiv | automatisch via `:has(.stats-explorer)` | Sobald `.stats-explorer` im DOM vorhanden ist |
| Mobile gestapelt | automatisch ab ≤ 768 px | `.stats-controls` wechselt auf `flex-direction: column`; `.stats-actions` verliert `margin-left: auto` |
| Reduzierte Bewegung | automatisch (`prefers-reduced-motion`) | Zeilen-Transitions in `.stats-table-panel .ci-table tbody tr` werden deaktiviert |

---

## JavaScript-Verantwortung

`css/stats.css` ist rein deklarativ. Alle dynamischen Verhaltensweisen liegen in der
Verantwortung des JavaScript der jeweiligen Zielseite:

- **Tabellenwahl:** Inhalt des `<tbody>` per JS austauschen, wenn der Wert von
  `.form-select` wechselt.
- **Zeitraumfilter:** Zeilen filtern oder neu laden, wenn Preset (`.segmented-btn`) oder
  manuelle Datumseingaben geändert werden. Aktives Preset mit `.active` markieren.
- **Sortierung:** `.sort-asc` / `.sort-desc` am jeweiligen `<th>` setzen und Zeilen
  per JS umsortieren. Immer nur **eine** Spalte darf gleichzeitig aktiv sortiert sein.
- **Zeilenfilterung:** Zeilen ausblenden oder neu rendern, wenn das Such-`<input>` im
  `.stats-search`-Block geändert wird.
- **Leerzustand:** `<table>` durch `<div class="stats-empty">…</div>` ersetzen, wenn
  keine Daten vorhanden sind.

---

## CSS einbinden

```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/page.css">
<link rel="stylesheet" href="css/forms.css">
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/stats.css">
```

Oder alles auf einmal über `css/index.css`.

**`css/demo.css`** nur in `components/stats-explorer.html` — niemals in Produktionsseiten.

---

## Vollständiges HTML-Beispiel

```html
<div class="content-body">
  <div class="stats-explorer">

    <!-- STEUER-FELD -->
    <div class="stats-controls">

      <div class="stats-control-group">
        <label class="ci-label">Tabelle</label>
        <div class="stats-control-row">
          <select class="form-select">
            <option>Alarmierungen</option>
            <option>Empfangsstatistik</option>
            <option>Nutzung</option>
          </select>
        </div>
      </div>

      <div class="stats-control-group">
        <label class="ci-label">Zeitraum</label>
        <div class="stats-control-row">
          <div class="segmented">
            <button class="segmented-btn active">Heute</button>
            <button class="segmented-btn">7 T</button>
            <button class="segmented-btn">30 T</button>
            <button class="segmented-btn">Alles</button>
          </div>
          <input type="date" class="form-input" value="2026-06-22">
          <span class="stats-range-sep">–</span>
          <input type="date" class="form-input" value="2026-06-22">
        </div>
      </div>

      <div class="stats-control-group stats-search">
        <label class="ci-label">Filter</label>
        <div class="stats-control-row">
          <input type="search" class="form-input" placeholder="Zeilen filtern …">
        </div>
      </div>

      <div class="stats-actions">
        <button class="btn btn-ghost btn-sm">
          <i class="fa-solid fa-rotate"></i> Aktualisieren
        </button>
        <button class="btn btn-secondary btn-sm">
          <i class="fa-solid fa-download"></i> Export
        </button>
      </div>

    </div>

    <!-- TABELLE -->
    <section class="panel stats-table-panel">
      <div class="panel-body-flush panel-body-flush--scroll">
        <table class="ci-table ci-table--sortable">
          <thead>
            <tr>
              <th class="sortable sort-desc mono">Zeitpunkt</th>
              <th class="sortable">Ereignis</th>
              <th class="sortable">Quelle</th>
              <th class="sortable mono">Anzahl</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="mono">2026-06-22 14:03</td>
              <td>Alarm ausgelöst</td>
              <td>POCSAG</td>
              <td class="mono">12</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Leerzustand (statt gefülltem tbody + table):
    <section class="panel stats-table-panel">
      <div class="panel-body-flush panel-body-flush--scroll">
        <div class="stats-empty">Keine Daten im gewählten Zeitraum.</div>
      </div>
    </section>
    -->

  </div>
</div>
```

---

## Regeln

1. **Nur Tokens verwenden** — keine hartcodierten Farben, Radien oder Z-Index-Werte.
2. **`.stats-explorer` ist einziges Kind von `.content-body`** — kein paralleles Element
   auf gleicher Ebene.
3. **`.panel` und `.stats-table-panel` zusammen** — nie nur eine der beiden Klassen am
   Tabellenbereich; `panel` liefert das Basis-Rahmen-Styling.
4. **Sortierung per JS** — CSS liefert nur die visuellen Indikatoren (`.sort-asc` /
   `.sort-desc`); die eigentliche Umsortierung der Tabellenzeilen liegt im JS.
5. **Kein `css/demo.css`** in Produktionsseiten — nur in `components/`.
6. **Sticky-Header nur im Stats-Kontext** — der `thead th`-Sticky-Selektor ist auf
   `.stats-table-panel` eingeschränkt; andere `ci-table`-Verwendungen bleiben unberührt.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-22 | Initiale Definition. Statistik-Explorer (Typ 7), G1–G4, Fixed-Height-Modell, JS-Verantwortung. |

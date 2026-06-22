# Statistik-Explorer (Typ 7) — Design / Spec

**Datum:** 2026-06-22
**Status:** Freigegeben · zur Umsetzung
**Angefragt von:** OE5ITH-Portale (Anzeige von PostgreSQL-Statistik-Tabellen)
**Version:** additiv → MINOR `v1.16.0`

Freigegebene, technisch geklärte Design-Spec für einen neuen Seitentyp.

---

## 1. Zweck

Generischer, wiederverwendbarer Seitentyp zum **Anzeigen tabellarischer
Statistik-Daten** (Quelle z.B. PostgreSQL). Oben ein **fixiertes Steuer-Feld**
zur Auswahl der Statistik-Tabelle, des Zeitraums und mit Aktions-Controls;
darunter eine **in sich scrollbare**, sortierbare Tabelle mit Sticky-Header.

Das Steuer-Feld scrollt nicht mit — wachsen die Ergebnisse, scrollt nur die
Tabelle in ihrem Bereich. Kein daten-spezifisches Styling: nur Tokens aus
`common.css` und Reuse bestehender Komponenten (`ci-table`, `forms`, `buttons`,
Panels).

Das Abfragen/Sortieren/Filtern der Daten selbst macht die konsumierende Seite
per JS — der CI-Typ liefert nur Struktur, Styling und die JS-Marker.

---

## 2. Neuer Seitentyp: Typ 7 — Statistik-Explorer

**Wann verwenden:** Der Hauptinhalt ist **eine** Statistik-/Datentabelle, die der
Nutzer über ein Steuer-Feld (Tabellen-Auswahl + Zeitraum + Aktionen) konfiguriert.
Steuer-Feld bleibt fix, nur die Tabelle scrollt.

**Beispiele:** Alarmierungs-Statistik, Empfangsstatistik, Nutzungs-Reports.

**Nicht geeignet wenn:**
- Es eine dauerhafte Auswahl**liste** mit Detailbereich gibt → Typ 6 (Split-View).
- Mehrere gleichartige Tabellen/Feeds ohne Steuer-Logik → Typ 2 (Listen-Seite).
- Der Inhalt primär aus Diagrammen besteht → Chart-Komponente.

**Abgrenzung zu Typ 2:** Typ 2 ist eine schlichte Liste mit optionalem Filter und
Seiten-Scroll. Typ 7 hat ein dediziertes, fixiertes Steuer-Feld (Tabellenwahl +
Zeitraum) und ein Fixed-Height-Scroll-Modell mit Sticky-Header.

---

## 3. Höhen-/Scroll-Modell (zentrale technische Entscheidung)

**Gewählter Ansatz: `:has()`-Auto-Aktivierung** — identisch zu Typ 6
(`split.css`). Alles in `css/stats.css`; `common.css`/`page.css` bleiben
unverändert. `:has()` wird im Repo bereits genutzt (calendar.css,
service-dashboard.css, split.css).

```css
.page-content:has(.stats-explorer) { display:flex; flex-direction:column; overflow:hidden; }
.content-body:has(.stats-explorer) { flex:1; min-height:0; overflow:hidden; }
.stats-explorer { display:flex; flex-direction:column; gap:var(--card-gap); height:100%; min-height:0; }
.stats-controls { flex-shrink:0; }
.stats-table-panel { flex:1; min-height:0; overflow:hidden; }
```

Verworfen:
- **Modifier-Klassen** (`.page-content--fixed`) — mehr HTML-Wissen nötig, berührt
  geteilte Struktur semantisch (gleiche Begründung wie Typ 6).
- **`calc()`-Festhöhe** — fragil bei umbrechendem Mobile-Steuer-Feld.

**Sticky-Header:** `thead th` der Tabelle wird **nur in diesem Kontext** sticky
gesetzt, damit Typ 2 unberührt bleibt:

```css
.stats-table-panel .ci-table thead th { position: sticky; top: 0; z-index: 1; }
```
(`th` hat bereits `background: var(--panel)` aus `page.css` — verdeckt scrollende
Zeilen korrekt.)

---

## 4. HTML-Struktur

```html
<div class="content-body">
  <div class="stats-explorer">

    <!-- STEUER-FELD (fix oben) -->
    <div class="stats-controls">
      <div class="stats-control-group">
        <label class="ci-label">Tabelle</label>
        <select class="form-select"> … </select>
      </div>

      <div class="stats-control-group">
        <label class="ci-label">Zeitraum</label>
        <div class="stats-presets">
          <button class="stats-preset active">Heute</button>
          <button class="stats-preset">7 T</button>
          <button class="stats-preset">30 T</button>
          <button class="stats-preset">Alles</button>
        </div>
        <input type="date" class="form-input">
        <span class="stats-range-sep">–</span>
        <input type="date" class="form-input">
      </div>

      <div class="stats-control-group stats-search">
        <input type="search" class="form-input" placeholder="Filtern …">
      </div>

      <div class="stats-actions">
        <button class="btn btn-ghost btn-sm"><i class="fa-solid fa-rotate"></i> Aktualisieren</button>
        <button class="btn btn-secondary btn-sm"><i class="fa-solid fa-download"></i> Export</button>
      </div>
    </div>

    <!-- TABELLE (scrollt in sich) -->
    <section class="panel stats-table-panel">
      <div class="panel-body-flush panel-body-flush--scroll">
        <table class="ci-table ci-table--sortable">
          <thead>
            <tr>
              <th class="sortable sort-desc">Zeitpunkt</th>
              <th class="sortable">Ereignis</th>
              <th class="sortable mono">Anzahl</th>
            </tr>
          </thead>
          <tbody> … </tbody>
        </table>
        <!-- Leerzustand statt <tbody>-Inhalt: -->
        <!-- <div class="stats-empty">Keine Daten im gewählten Zeitraum.</div> -->
      </div>
    </section>

  </div>
</div>
```

Reale `class="form-select"`/`form-input`/`btn …`-Namen werden bei der Umsetzung
gegen `forms.css`/`buttons.css` verifiziert und ggf. angepasst.

---

## 5. Klassen-Spezifikation

| Klasse | Zweck / Regeln |
|---|---|
| `.stats-explorer` | Flex-Column, füllt `content-body`. `gap:var(--card-gap)`, `height:100%`, `min-height:0`. Aktiviert Fixed-Height via `:has()`. |
| `.stats-controls` | Steuer-Feld oben. Flex-Row mit Umbruch (`flex-wrap:wrap`), `gap`, `align-items:flex-end`, `flex-shrink:0`. Karten-Optik: `--card-bg`, `1px solid --border`, `--card-radius`, Innen-Padding. |
| `.stats-control-group` | Gruppe Label + Element(e). Flex (Spalte für Label über Element, oder Row), `gap`. |
| `.stats-presets` | Segmentierte Button-Gruppe (Zeitraum-Presets). Flex-Row, zusammenhängend (gemeinsame Border / Radius an Enden). |
| `.stats-preset` | Einzel-Preset (`<button>`). Token-basiert, `--muted`-Text, Hover `--surface-hover`. Tastatur-fokussierbar (`:focus-visible`). |
| `.stats-preset.active` | Aktiver Preset: BG `--accent-subtle`, Text `--text`, Marker via `--accent-border`. |
| `.stats-range-sep` | Trenner „–" zwischen Von/Bis. `--subtle`, klein, `flex-shrink:0`. |
| `.stats-search` | Such-/Filter-Gruppe. Wächst (`flex:1`, `min-width:0`) damit Aktionen nach rechts rücken. |
| `.stats-actions` | Aktions-Buttons. Flex-Row, `gap`, `margin-left:auto` (rechtsbündig). |
| `.stats-table-panel` | Tabellen-Panel. `flex:1`, `min-height:0`, `min-width:0`, `overflow:hidden`. Enthält scrollenden `.panel-body-flush--scroll`. |
| `.stats-empty` | Leerzustand. Zentriert, `--subtle`, Innen-Padding, anstelle gefüllter `tbody`-Zeilen. |

**Reuse:** `ci-table` + `ci-table--sortable` + `.sortable`/`.sort-asc`/`.sort-desc`
(page.css), `.panel`/`.panel-body-flush`/`--scroll` (page.css), Form-Elemente
(forms.css), Buttons (buttons.css), `.ci-label` (typography/forms). **Keine** neue
Tabellen-, Button- oder Input-Variante.

---

## 6. Tokens

**Keine neuen Tokens.** Reuse: `--panel`, `--card-bg`, `--border`,
`--border-strong`, `--card-radius`, `--card-gap`, `--surface-hover`,
`--accent`, `--accent-subtle`, `--accent-border`, `--text`, `--muted`,
`--subtle`, `--transition-fast`.

---

## 7. Responsive & Motion

- Breakpoint analog übrige Typen (`@media (max-width: 768px)`):
  `.stats-controls{ flex-direction:column; align-items:stretch }`,
  Control-Gruppen volle Breite, `.stats-actions{ margin-left:0 }`.
- Tabelle scrollt auf Mobile horizontal (bestehendes
  `.panel-body-flush--scroll`) und vertikal in der Resthöhe.
- `@media (prefers-reduced-motion: reduce)`: Transitions deaktivieren.

---

## 8. Referenz-Komponente

`components/stats-explorer.html` (mit `css/demo.css` wie andere Referenzseiten):

1. Vollständiges Steuer-Feld: Tabellen-Dropdown, Preset-Gruppe (inkl. `.active`),
   Von–Bis Datumsfelder, Suchfeld, Aktions-Buttons.
2. `ci-table.ci-table--sortable` mit sichtbarem Sticky-Header (genug Zeilen, damit
   gescrollt wird) und einer aktiv sortierten Spalte (`.sort-desc`).
3. Zweiter Block / Hinweis zum Leerzustand (`.stats-empty`).

**Demo-Hinweis:** `demo.css` setzt `.page-content{ max-width:960px }`. Auf der
Referenzseite wird die Breitenbegrenzung überschrieben (volle Breite), damit das
Höhen-/Scroll-Modell realistisch dargestellt wird (analog `split-view.html`).

---

## 9. Doku-/Registry-/Versions-Updates

- `css/stats.css` — neue Datei (lädt nach `page.css`/`split.css`).
- `css/index.css` — `@import "stats.css";`.
- `docs/page-stats.md` — Komponenten-/Seitentyp-Doku nach Doku-Standard G1–G4
  (analog `docs/split-view.md`).
- `docs/page-types.md` — Typ 7 ergänzen; Entscheidungsbaum; Schnellreferenz;
  „Neues Design erforderlich"-Hinweis ggf. anpassen; Änderungshistorie-Zeile.
- `docs/registry.json` — Eintrag für die Komponente; `python3
  scripts/cli/check_consistency.py` muss grün sein.
- `CHANGELOG.md` — `Added`-Eintrag (additiv, nicht breaking).
- `README.md`/`docs/usage.md` — bei Bedarf.
- Version: MINOR `v1.16.0`.

---

## 10. Akzeptanzkriterien

- [ ] `.stats-explorer` füllt `content-body`; Steuer-Feld fix, nur Tabelle scrollt.
- [ ] Sticky-Header **nur** im `.stats-table-panel`-Kontext — Typ 2 unverändert.
- [ ] Tabelle nutzt bestehendes `ci-table` + `ci-table--sortable` (JS-Marker, kein neues Sort-Styling).
- [ ] Steuer-Feld enthält: Tabellen-Dropdown, Zeitraum (Presets `.active` + Von–Bis), Suchfeld, Aktionen (rechtsbündig).
- [ ] `.stats-table-panel` hat `min-width:0` (lange `ci-table`-Zeilen sprengen das Layout nicht).
- [ ] Presets/Buttons/Inputs reusen forms.css/buttons.css — keine neuen Varianten.
- [ ] Leerzustand `.stats-empty` vorhanden.
- [ ] Responsive: unter 768px gestapeltes Steuer-Feld, Aktionen linksbündig.
- [ ] `prefers-reduced-motion`: Transitions aus.
- [ ] Tastaturbedienbarkeit + sichtbarer Fokus für Presets/Buttons.
- [ ] Keine hardcodierten Farben/Radien/Z-Index/Transitions — nur Tokens; **keine neuen Tokens**.
- [ ] `css/demo.css` nur in `components/stats-explorer.html`, nicht produktiv.
- [ ] `docs/page-stats.md`, `page-types.md`, `registry.json`, `CHANGELOG.md`
      aktualisiert; `check_consistency.py` grün.

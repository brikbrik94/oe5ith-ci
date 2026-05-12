# Spec: Tabelle — Mobile Horizontal Scroll + Sortable Contract

**Datum:** 2026-05-12
**Status:** Approved

---

## Ziel

1. `.ci-table` auf Mobilgeräten horizontal scrollbar machen ohne Zeilen-Stacking.
2. Den Sortable-Contract zwischen CSS und JS explizit definieren.

---

## Änderungen

### `css/page.css`

**Scroll-Modifier** — direkt nach `.panel-body-flush`:

```css
.panel-body-flush--scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
```

- `overflow: hidden` sitzt auf `.panel`, nicht auf `.panel-body-flush` — kein Konflikt.
- Die gerundeten Panel-Ecken bleiben durch das Panel-eigene `overflow: hidden` erhalten.
- `-webkit-overflow-scrolling: touch` für flüssiges Scrollen auf iOS.

**Sortable-Marker** — im Tabellen-Block nach den bestehenden `th.sortable`-Regeln:

```css
/* JS-Marker: Tabelle hat sortierbare Spalten.
   Visuelle States via th.sortable / th.sort-asc / th.sort-desc */
.ci-table--sortable { }
```

Leere Regel. Kein zusätzliches Styling. Dient ausschließlich als expliziter Contract für JS-Selektion.

---

### HTML-Konvention

Tabellen in `panel-body-flush` erhalten künftig den Scroll-Modifier:

```html
<div class="panel-body-flush panel-body-flush--scroll">
  <table class="ci-table">...</table>
</div>
```

Sortierbare Tabellen zusätzlich mit Marker:

```html
<div class="panel-body-flush panel-body-flush--scroll">
  <table class="ci-table ci-table--sortable">
    <thead>
      <tr>
        <th class="mono sortable sort-asc">RIC/ADR</th>
        <th class="mono">Zeitstempel</th>
      </tr>
    </thead>
    ...
  </table>
</div>
```

---

### `docs/page.md`

**Panel-Sektion:** Ergänzung dass `.panel-body-flush--scroll` für Tabellen verwendet werden soll.

**Tabellen-Sektion:**
- Beispiel-Code auf `panel-body-flush panel-body-flush--scroll` aktualisieren.
- Sortable-Contract dokumentieren:
  - CSS liefert visuelle States: `.sortable` (Cursor, User-Select), `.sort-asc` / `.sort-desc` (Pfeil-Icons via `::after`, Farbe `--accent`).
  - Echte Sortierlogik ist **JS-Pflicht**. CSS sortiert keine Daten.
  - Tabelle mit `.ci-table--sortable` markieren damit JS sie per Selektor finden kann.
  - JS-Verantwortlichkeiten: Klassen `sort-asc` / `sort-desc` auf dem aktiven `<th>` toggeln, DOM-Zeilen neu anordnen.

---

## Nicht in Scope

- Keine JS-Implementierung der Sortierlogik (gehört ins jeweilige Portal).
- Kein Sticky-Header für gescrollte Tabellen.
- Kein Touch-Drag-Scroll-Indicator (z.B. Fade-out-Rand).

---

## Tokens / Abhängigkeiten

Keine neuen Tokens. Änderungen ausschließlich in `css/page.css` und `docs/page.md`.

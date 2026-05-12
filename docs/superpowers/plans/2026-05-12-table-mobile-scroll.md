# Tabelle Mobile Scroll + Sortable Contract — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `.ci-table` auf Mobilgeräten horizontal scrollbar machen und den CSS/JS-Sortable-Contract explizit definieren.

**Architecture:** Zwei CSS-Regeln in `page.css` (Scroll-Modifier, Sortable-Marker) + Doku-Aktualisierung in `docs/page.md`. Keine JS-Implementierung, kein Build-Schritt.

**Tech Stack:** CSS, Markdown

---

## File Map

| Datei | Änderung |
|---|---|
| `css/page.css` | Zeile 202: `.panel-body-flush--scroll` einfügen; Zeile 241: `.ci-table--sortable` einfügen |
| `docs/page.md` | Panel-Sektion + Tabellen-Sektion aktualisieren, Sortable-Contract-Abschnitt hinzufügen |

---

## Task 1: CSS — Scroll-Modifier

**Files:**
- Modify: `css/page.css` (nach Zeile 202)

- [ ] **Schritt 1: Scroll-Modifier nach `.panel-body-flush` einfügen**

  In `css/page.css` direkt nach dem Block:
  ```css
  .panel-body-flush {
    padding: 0;
  }
  ```
  folgenden Block einfügen:
  ```css
  .panel-body-flush--scroll {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  ```

- [ ] **Schritt 2: Visuell prüfen**

  `components/page-types.html` im Browser öffnen. Keine Änderung am Aussehen erwartet (der Modifier ist noch nicht verwendet). Prüfen dass die Seite fehlerfrei lädt.

---

## Task 2: CSS — Sortable-Marker

**Files:**
- Modify: `css/page.css` (nach Zeile 241)

- [ ] **Schritt 1: Sortable-Marker nach den Sort-Arrow-Regeln einfügen**

  In `css/page.css` direkt nach:
  ```css
  .ci-table th.sort-desc::after { content: ' ↓'; color: var(--accent); }
  ```
  folgenden Block einfügen:
  ```css

  /* JS-Marker: Tabelle hat sortierbare Spalten.
     Visuelle States via th.sortable / th.sort-asc / th.sort-desc */
  .ci-table--sortable { }
  ```

- [ ] **Schritt 2: CSS committen**

  ```bash
  git add css/page.css
  git commit -m "feat: add panel-body-flush--scroll modifier and ci-table--sortable JS marker"
  ```

---

## Task 3: Doku — `docs/page.md` Panel-Sektion

**Files:**
- Modify: `docs/page.md` (Panel-Sektion, ca. Zeile 125–127)

- [ ] **Schritt 1: Panel-Beispiel aktualisieren**

  In `docs/page.md` den Kommentar und das `panel-body-flush`-Beispiel in der Panel-Sektion ersetzen:

  **Alt:**
  ```html
    <!-- Oder: kein Padding (für Tabellen, Code-Blöcke) -->
    <div class="panel-body-flush">
      <table class="ci-table">...</table>
    </div>
  ```

  **Neu:**
  ```html
    <!-- Oder: kein Padding (für Tabellen, Code-Blöcke) -->
    <!-- Mit --scroll für horizontal scrollbare Tabellen auf Mobile -->
    <div class="panel-body-flush panel-body-flush--scroll">
      <table class="ci-table">...</table>
    </div>
  ```

---

## Task 4: Doku — `docs/page.md` Tabellen-Sektion

**Files:**
- Modify: `docs/page.md` (Tabellen-Sektion, ca. Zeile 143–191)

- [ ] **Schritt 1: Einleitungstext aktualisieren**

  **Alt:**
  ```
  CI-konforme Tabelle. Hintergrund `--panel` (#202020).
  Immer in `.panel-body-flush` verwenden.
  ```

  **Neu:**
  ```
  CI-konforme Tabelle. Hintergrund `--panel` (#202020).
  Immer in `.panel-body-flush.panel-body-flush--scroll` verwenden — sorgt für horizontales Scrolling auf Mobile statt Zeilen-Stacking.
  ```

- [ ] **Schritt 2: HTML-Beispiel aktualisieren**

  In der Tabellen-Sektion den gesamten Beispiel-Code-Block ersetzen:

  **Alt:**
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

  **Neu:**
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

- [ ] **Schritt 3: Sortable-Contract-Abschnitt nach der Tokens-Tabelle einfügen**

  Nach dem Abschnitt `### Tabellen-Tokens` und seiner Tabelle (nach der letzten Tabellenzeile `| \`.empty\` | ...`) folgenden neuen Abschnitt einfügen:

  ```markdown
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
  - Bei Klick auf `.sortable th`: `.sort-asc` / `.sort-desc` auf dem aktiven `<th>` toggeln, auf allen anderen entfernen
  - DOM-Zeilen (`<tbody> <tr>`) nach dem Sortierwert neu anordnen
  ```

- [ ] **Schritt 4: Committen**

  ```bash
  git add docs/page.md
  git commit -m "docs: update table section with scroll modifier and sortable contract"
  ```

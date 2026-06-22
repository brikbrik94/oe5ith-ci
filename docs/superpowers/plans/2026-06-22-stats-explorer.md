# Statistik-Explorer (Typ 7) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Neuer Seitentyp „Typ 7 — Statistik-Explorer": fixiertes Steuer-Feld (Tabellen-Auswahl, Zeitraum, Suche, Aktionen) über einer in sich scrollbaren, sortierbaren Tabelle mit Sticky-Header.

**Architecture:** Reines CSS/HTML, kein Build-Schritt. Fixed-Height-Scroll wird per `:has()`-Auto-Aktivierung erreicht (identisch zu Typ 6 / `split.css`) — `common.css`/`page.css` bleiben unverändert. Die Tabelle reust `ci-table`/`ci-table--sortable`, Steuerelemente reusen `forms.css` (`.form-select`, `.form-input`, `.segmented`/`.segmented-btn`) und `buttons.css`. Neue `.stats-*`-Klassen sind ausschließlich Layout-Container. Sortier-/Filter-/Daten-Logik bleibt JS-Sache der konsumierenden Seite (CI liefert nur Marker).

**Tech Stack:** Plain CSS (Tokens aus `common.css`), HTML5, FontAwesome-Icons. Verifikation: `python3 scripts/cli/check_consistency.py`, grep auf Hardcodings, manuelle Browser-Sichtprüfung.

## Global Constraints

- Niemals Werte hardcoden — Farben/Hintergründe/Border/Radien/Shadows/Z-Index/Transitions nur über CSS-Tokens aus `common.css`.
- Keine eigenen Komponenten-Klassen, wenn ein bestehendes Muster passt — `.stats-*` definiert nur Layout-Container; Tabelle/Inputs/Buttons/Presets werden wiederverwendet.
- **Keine neuen Tokens** in diesem Feature.
- `css/demo.css` nur in `components/stats-explorer.html`, niemals produktiv.
- Sticky-Header **nur** im `.stats-table-panel`-Kontext setzen — Typ 2 (Listen-Seite) darf sich nicht ändern.
- Map-Seiten sind Sonderfall und nicht betroffen.
- Jede neue Komponente braucht einen `docs/registry.json`-Eintrag; `check_consistency.py` muss grün bleiben.
- Version: additiv → MINOR `v1.16.0`.
- Spec: `docs/superpowers/specs/2026-06-22-stats-explorer-design.md`.

---

### Task 1: Referenz-HTML als Struktur-Vorlage

**Files:**
- Create: `components/stats-explorer.html`

**Interfaces:**
- Consumes: bestehende Klassen `topbar`, `layout`, `sidebar`, `page-content`, `page-header`, `content-body`, `panel`, `panel-body-flush`, `panel-body-flush--scroll`, `ci-table`, `ci-table--sortable`, `.sortable`/`.sort-desc`, `.mono`, `.segmented`/`.segmented-btn`, `.form-select`, `.form-input`, `.ci-label`, `.btn`/`.btn-ghost`/`.btn-secondary`/`.btn-sm`.
- Produces: das DOM-Gerüst (`.stats-explorer` > `.stats-controls` + `.stats-table-panel`) und die neuen Layout-Klassen-Namen, die Task 2 (CSS) und Task 3 (Doku) referenzieren: `.stats-explorer`, `.stats-controls`, `.stats-control-group`, `.stats-control-row`, `.stats-range-sep`, `.stats-search`, `.stats-actions`, `.stats-table-panel`, `.stats-empty`.

- [ ] **Step 1: Referenzseite anlegen**

Orientiere dich an `components/split-view.html` für Topbar/Sidebar/`demo.css`-Einbindung und die Breiten-Override (Demo setzt `max-width:960px`; für realistisches Scroll-Modell auf volle Breite überschreiben). Hauptinhalt:

```html
<div class="content-body">
  <div class="stats-explorer">

    <!-- STEUER-FELD (fix oben) -->
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
              <th class="sortable sort-desc mono">Zeitpunkt</th>
              <th class="sortable">Ereignis</th>
              <th class="sortable">Quelle</th>
              <th class="sortable mono">Anzahl</th>
            </tr>
          </thead>
          <tbody>
            <!-- mind. 30 Zeilen, damit vertikal gescrollt wird und der
                 Sticky-Header sichtbar stehen bleibt -->
            <tr><td class="mono">2026-06-22 14:03</td><td>Alarm ausgelöst</td><td>POCSAG</td><td class="mono">12</td></tr>
            <!-- … weitere Zeilen … -->
          </tbody>
        </table>
      </div>
    </section>

  </div>
</div>
```

Zusätzlich am Seitenende einen kurzen Kommentar/zweiten Hinweisblock zum Leerzustand aufnehmen (auskommentiert oder als separater Demo-Abschnitt), der `.stats-empty` zeigt:

```html
<!-- Leerzustand (statt gefülltem tbody):
<div class="stats-empty">Keine Daten im gewählten Zeitraum.</div>
-->
```

- [ ] **Step 2: HTML im Browser öffnen (erwartetes „Fail")**

Run: Datei `components/stats-explorer.html` im Browser öffnen.
Expected: Inhalte sind sichtbar, aber **ungestylt im Layout** — Steuer-Feld und Tabelle stapeln sich ohne Fixed-Height/Sticky-Header, weil `css/stats.css` noch nicht existiert. Das ist der Soll-Zustand vor Task 2.

- [ ] **Step 3: Auf Hardcodings prüfen**

Run: `grep -nE "#[0-9a-fA-F]{3,6}|rgba?\(" components/stats-explorer.html`
Expected: Keine Treffer in produktionsrelevanten Style-Attributen (Inline-Styles vermeiden; Demo-Overrides nur über `demo.css`-Muster wie in `split-view.html`).

- [ ] **Step 4: Commit**

```bash
git add components/stats-explorer.html
git commit -m "docs(stats): add reference HTML for Typ 7 Statistik-Explorer"
```

---

### Task 2: CSS — `css/stats.css` + Einbindung

**Files:**
- Create: `css/stats.css`
- Modify: `css/index.css` (`@import "stats.css";` **direkt nach** `@import "forms.css";` ergänzen — stats.css braucht sowohl `page.css` als auch `forms.css`, daher nach beiden)

**Interfaces:**
- Consumes: Klassen aus Task 1 (`.stats-explorer`, `.stats-controls`, `.stats-control-group`, `.stats-control-row`, `.stats-range-sep`, `.stats-search`, `.stats-actions`, `.stats-table-panel`, `.stats-empty`) sowie bestehende `.panel-body-flush--scroll`, `.ci-table thead th`.
- Produces: das vollständige Styling des Seitentyps (Fixed-Height, Sticky-Header, Steuer-Feld-Layout, Leerzustand).

- [ ] **Step 1: `css/stats.css` schreiben**

```css
/*
 * OE5ITH CI — stats.css
 * Statistik-Explorer (Seitentyp Typ 7).
 * Fixiertes Steuer-Feld oben + in sich scrollbare, sortierbare
 * Tabelle mit Sticky-Header.
 *
 * Voraussetzung: css/common.css, css/page.css, css/forms.css, css/buttons.css
 * Reuse: .ci-table / .ci-table--sortable (page.css),
 *        .panel / .panel-body-flush--scroll (page.css),
 *        .segmented / .segmented-btn, .form-select / .form-input (forms.css),
 *        Buttons (buttons.css).
 * Neue .stats-*-Klassen sind ausschließlich Layout-Container.
 */

/* ═══════════════════════════════════════
   FIXED-HEIGHT-MODUS (Auto-Aktivierung)
   Identisch zu Typ 6 (split.css): bei vorhandener
   .stats-explorer scrollt nicht die Seite, sondern
   nur die Tabelle. common.css/page.css bleiben unverändert.
   ═══════════════════════════════════════ */
.page-content:has(.stats-explorer) {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.content-body:has(.stats-explorer) {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* ═══════════════════════════════════════
   EXPLORER-CONTAINER
   ═══════════════════════════════════════ */
.stats-explorer {
  display: flex;
  flex-direction: column;
  gap: var(--card-gap);
  height: 100%;
  min-height: 0;
}

/* ═══════════════════════════════════════
   STEUER-FELD (fix oben, scrollt nicht mit)
   ═══════════════════════════════════════ */
.stats-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 16px;
  flex-shrink: 0;
  padding: 14px 16px;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--card-radius);
}

.stats-control-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* Reihe mit den eigentlichen Steuerelementen unter dem Label */
.stats-control-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.stats-range-sep {
  color: var(--subtle);
  font-size: 0.8rem;
  flex-shrink: 0;
  padding: 0 2px;
}

/* Suchgruppe wächst, drückt die Aktionen nach rechts */
.stats-search {
  flex: 1;
  min-width: 0;
}
.stats-search .stats-control-row,
.stats-search .form-input {
  width: 100%;
}

.stats-actions {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

/* ═══════════════════════════════════════
   TABELLEN-PANEL (füllt Resthöhe, scrollt in sich)
   ═══════════════════════════════════════ */
.stats-table-panel {
  flex: 1;
  min-height: 0;
  min-width: 0;          /* lange ci-table-Zeilen sprengen das Layout nicht */
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.stats-table-panel .panel-body-flush--scroll {
  flex: 1;
  min-height: 0;
  overflow: auto;        /* vertikal + horizontal */
}

/* Sticky-Header NUR in diesem Kontext — Typ 2 bleibt unberührt.
   th trägt bereits background: var(--panel) aus page.css und
   verdeckt damit die scrollenden Zeilen. */
.stats-table-panel .ci-table thead th {
  position: sticky;
  top: 0;
  z-index: 1;
}

/* ═══════════════════════════════════════
   LEERZUSTAND
   ═══════════════════════════════════════ */
.stats-empty {
  padding: 40px 16px;
  text-align: center;
  color: var(--subtle);
  font-size: 0.85rem;
}

/* ═══════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════ */
@media (max-width: 768px) {
  .stats-controls {
    flex-direction: column;
    align-items: stretch;
  }
  .stats-control-group {
    width: 100%;
  }
  .stats-actions {
    margin-left: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .stats-table-panel .ci-table tbody tr {
    transition: none;
  }
}
```

- [ ] **Step 2: In `css/index.css` einbinden**

Füge direkt nach der Zeile `@import "forms.css";` ein:

```css
@import "stats.css";
```

(stats.css braucht `page.css` UND `forms.css`; daher nach beiden importieren.)

- [ ] **Step 3: Im Browser verifizieren (erwartetes „Pass")**

Run: `components/stats-explorer.html` neu laden.
Expected:
- Steuer-Feld bleibt oben **fix**; nur die Tabelle scrollt vertikal in ihrem Bereich.
- Beim Scrollen bleibt der `thead` (Sticky-Header) sichtbar stehen und verdeckt die Zeilen sauber (kein Durchscheinen).
- Aktions-Buttons sitzen rechtsbündig; aktiver `.segmented-btn` ist hervorgehoben.
- Fenster auf < 768px verkleinern: Steuer-Feld stapelt vertikal, Aktionen linksbündig.

- [ ] **Step 4: Auf Hardcodings + Token-Nutzung prüfen**

Run: `grep -nE "#[0-9a-fA-F]{3,6}|[0-9]+px.*(color|background|border-color)|z-index:\s*[0-9]" css/stats.css`
Expected: Keine hardcodierten Farben/Z-Index. (`px` für Padding/Gap/font-size ist erlaubt — Tokens existieren dafür nicht; Border/Radius/Farben laufen über Tokens.)

- [ ] **Step 5: Commit**

```bash
git add css/stats.css css/index.css
git commit -m "feat(stats): add Typ 7 Statistik-Explorer styles"
```

---

### Task 3: Dokumentation (`docs/page-stats.md` + `docs/page-types.md`)

**Files:**
- Create: `docs/page-stats.md`
- Modify: `docs/page-types.md` (Typ 7 ergänzen, Entscheidungsbaum, Schnellreferenz, Änderungshistorie)

**Interfaces:**
- Consumes: Klassen-/Strukturnamen aus Task 1 + 2.
- Produces: Doku nach Doku-Standard G1–G4 (`docs/doc-standard.md`), die `check_consistency.py` in Task 4 als „Dreiklang" erwartet.

- [ ] **Step 1: `docs/page-stats.md` schreiben**

Orientiere dich an `docs/split-view.md`. Muss die vier Garantien aus `docs/doc-standard.md` erfüllen:

- **G1 — Element-Tabelle:** jede `.stats-*`-Klasse mit Zweck, Pflicht/Optional, erlaubten Modifiern. **Jede** verwendete Klasse muss in der Tabelle stehen (nicht nur im Beispiel-HTML), inkl. der reusten `.segmented`/`.form-select`/`.form-input`/`.ci-table--sortable` mit Verweis auf ihre Heimat-Doku.
- **G2 — Struktur-Baum:**

```text
.stats-explorer
├── .stats-controls                 (Pflicht)
│   ├── .stats-control-group         (1..n)
│   │   ├── .ci-label                (Optional)
│   │   └── .stats-control-row       (Pflicht — enthält form-select / segmented / form-input)
│   └── .stats-actions               (Optional — rechtsbündig)
└── .panel.stats-table-panel         (Pflicht)
    └── .panel-body-flush--scroll
        └── table.ci-table.ci-table--sortable   (oder .stats-empty)
```

- **G3 — Reihenfolge/Platzierung (Prosa):** Steuer-Feld immer **vor** der Tabelle; `.stats-actions` rechtsbündig (`margin-left:auto`); primärer/sekundärer Button gemäß projektweiter Button-Konvention. `.stats-explorer` ist das einzige direkte Kind von `.content-body`.
- **G4 — Zustände/Varianten:** Tabelle mit `.ci-table--sortable` + aktive Sortierung (`.sort-asc`/`.sort-desc`); Preset aktiv (`.segmented-btn.active`); Leerzustand (`.stats-empty` statt gefülltem `tbody`); Fixed-Height ist automatisch aktiv, sobald `.stats-explorer` im DOM ist.

Außerdem dokumentieren: Voraussetzungen (`css/stats.css` zusätzlich zu `page.css` + `forms.css` einbinden), JS-Verantwortung (Sortieren/Filtern/Daten via JS der Zielseite über die Marker-Klassen).

- [ ] **Step 2: `docs/page-types.md` erweitern**

Ergänze einen Abschnitt **„Typ 7 — Statistik-Explorer"** im Stil von Typ 6 (Wann verwenden / Beispiele / Struktur-Block / Merkmale / Nicht geeignet wenn). Aktualisiere zusätzlich:
- **Entscheidungsbaum:** Zweig „Ist der Hauptinhalt **eine** Statistik-Tabelle mit Steuer-Feld (Tabellenwahl + Zeitraum)? → Typ 7" vor dem generischen Tabellen-Zweig (Typ 2) einordnen.
- **Schnellreferenz-Tabelle:** Zeile „Konfigurierbare Statistik-Tabelle (Wahl + Zeitraum) | 7".
- **Änderungshistorie:** Zeile `| 2026-06-22 | Typ 7 — Statistik-Explorer ergänzt. Entscheidungsbaum + Schnellreferenz aktualisiert. |`.

- [ ] **Step 3: Doku gegen Prüffrage checken**

Run: visuelles Review von `docs/page-stats.md`.
Expected: Prüffrage aus `doc-standard.md` erfüllt — „Könnte ein Agent die Komponente bauen, ohne `components/stats-explorer.html` zu öffnen?" → Ja (G1–G4 vollständig, keine Klasse nur im Beispiel).

- [ ] **Step 4: Commit**

```bash
git add docs/page-stats.md docs/page-types.md
git commit -m "docs(stats): document Typ 7 Statistik-Explorer (page-stats.md + page-types.md)"
```

---

### Task 4: Registry, Konsistenz-Check, CHANGELOG

**Files:**
- Modify: `docs/registry.json`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: alle in Task 1–3 erstellten Dateien (`stats.css`, `stats-explorer.html`, `page-stats.md`).
- Produces: grüner `check_consistency.py`-Lauf + Changelog-Eintrag für Release `v1.16.0`.

- [ ] **Step 1: Registry-Eintrag ergänzen**

Füge in `docs/registry.json` unter `"components"` einen Eintrag im selben Format wie `split-view` hinzu:

```json
{
  "id": "stats-explorer",
  "title": "Statistik-Explorer (Typ 7)",
  "category": "component",
  "css": ["stats.css"],
  "doc": ["page-stats.md"],
  "html": ["stats-explorer.html"]
}
```

- [ ] **Step 2: Konsistenz-Check ausführen**

Run: `python3 scripts/cli/check_consistency.py`
Expected: Endet mit `✔ Manifest und Dateien sind konsistent`. Für `stats-explorer` **keine** „Dreiklang unvollständig"-Warnung (die bestehenden Warnungen zu `coords`/`utils` sind unverändert und nicht Teil dieses Tasks).

- [ ] **Step 3: CHANGELOG ergänzen**

Trage unter einem `Added`-Abschnitt für `v1.16.0` ein (Format der bestehenden Einträge übernehmen):

```markdown
### Added
- Seitentyp **Typ 7 — Statistik-Explorer**: fixiertes Steuer-Feld (Tabellen-Auswahl, Zeitraum-Presets + Von–Bis, Filter, Aktionen) über einer in sich scrollbaren, sortierbaren `ci-table` mit Sticky-Header. Neue Datei `css/stats.css`, Referenz `components/stats-explorer.html`, Doku `docs/page-stats.md`. Keine neuen Tokens. (`docs/page-types.md` Typ 7 ergänzt.)
```

- [ ] **Step 4: Final-Verifikation**

Run: `python3 scripts/cli/check_consistency.py && grep -c "stats-explorer\|stats.css\|page-stats" docs/registry.json`
Expected: Check grün; grep-Count ≥ 3.

- [ ] **Step 5: Commit**

```bash
git add docs/registry.json CHANGELOG.md
git commit -m "docs(stats): register Typ 7 in registry + changelog (v1.16.0)"
```

---

## Release (nach Abschluss aller Tasks)

Nicht Teil eines Tasks — auf ausdrückliche Freigabe:

```bash
git tag -a v1.16.0 -m "Release v1.16.0 — Typ 7 Statistik-Explorer"
git push origin main v1.16.0
```

---

## Notes für den Umsetzer

- **Token-Verifikation:** `--card-gap`, `--card-bg`, `--card-radius`, `--border`, `--panel`, `--subtle`, `--accent` werden in `split.css`/`page.css`/`forms.css` bereits genutzt — vor Verwendung in `common.css` gegenprüfen, falls ein Name abweicht.
- **`.panel`-Reuse:** `.stats-table-panel` ist zusätzlich `.panel`; das CSS macht es zur Flex-Column, damit `.panel-body-flush--scroll` die Resthöhe füllt. Falls `.panel` ein eigenes Padding setzt, sorgt `.panel-body-flush` (padding:0) für den bündigen Tabellenrand.
- **Kein JS in diesem Repo:** Sortier-/Filter-Verhalten wird NICHT implementiert — nur die Marker-Klassen (`.sortable`, `.sort-asc/-desc`) und die aktive Demo-Darstellung.

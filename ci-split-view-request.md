# CI-Erweiterung: Split-View (Master-Detail) — Anforderung

**Status:** Vorschlag · zur Umsetzung im `oe5ith-ci` Repo
**Angefragt von:** internal.oe5ith.at (neue „System Logs"-Seite)
**Datum:** 2026-06-18

---

## 1. Warum

Für die geplante **System-Logs-Seite** auf `internal.oe5ith.at` wird ein
zweispaltiges Master-Detail-Layout benötigt:

- **Links:** scrollbare Liste aller Log-Quellen mit Status-Indikator
- **Rechts:** Logs der ausgewählten Quelle (Filter-Panel + Tabelle)

`docs/page-types.md` listet **Split-View** ausdrücklich unter *„Neues Design
erforderlich"* (Abschnitt „Neues Design erforderlich wenn… Der Inhalt in zwei
gleichwertige Hälften aufgeteilt ist (Split-View)"). Es existiert aktuell **kein**
CI-Pattern dafür — `col-groups` (Typ 4) ist nur für thematische Karten-Gruppen,
nicht für eine selektierbare Liste + Detailbereich.

Diese Anforderung folgt dem „Neue Komponenten"-Ablauf aus
`docs/for-coding-agents.md` (Zweck → HTML/Klassen → CSS → Referenz → Doku).

> **Wichtig:** Das soll eine **generische, wiederverwendbare** CI-Komponente
> werden (auch für künftige Master-Detail-Seiten), **kein** Log-spezifisches
> Styling. Keine Farben/Radien/Z-Index hardcoden — nur Tokens aus `common.css`.

---

## 2. Neuer Seitentyp: Typ 6 — Split-View (Master-Detail)

In `docs/page-types.md` ergänzen:

**Wann verwenden:** Zwei nebeneinanderliegende Bereiche — links eine schmale,
scrollbare Auswahlliste gleichartiger Einträge, rechts der Detailbereich zum
gewählten Eintrag. Beide gleichzeitig sichtbar, unabhängig scrollbar.

**Beispiele:** System Logs (Quellen → Einträge), künftige Konfig-/Browser-Seiten.

**Struktur:**
```
Topbar
└── Layout
    ├── Sidebar (App-Sidebar, unverändert)
    └── page-content
        ├── page-header              ← Titel + Untertitel + page-action (rechts)
        └── content-body
            └── split-view
                ├── split-master     ← schmale Spalte: Liste
                │   ├── split-master-header   ← optional: Titel + Such-/Aktionsleiste
                │   └── split-master-body     ← scrollbar; enthält split-item*
                └── split-detail     ← breite Spalte: Panels (Filter, Tabelle, …)
```

**Nicht geeignet wenn:** Es keine dauerhafte Auswahlliste gibt (→ Typ 1) oder
der Hauptinhalt nur eine einzelne Tabelle ist (→ Typ 2).

---

## 3. HTML-Struktur & Klassen

```html
<div class="content-body">
  <div class="split-view">

    <!-- MASTER (links) -->
    <aside class="split-master">
      <div class="split-master-header">
        <span class="ci-label">Quellen</span>
        <!-- optionale Aktionen, bestehende Button-Klassen -->
        <button class="btn btn-sm btn-ghost"><i class="fa-solid fa-pause"></i></button>
        <button class="btn btn-sm btn-ghost"><i class="fa-solid fa-rotate"></i></button>
      </div>
      <div class="split-master-body">
        <button class="split-item active">
          <span class="status-dot on"></span>
          <span class="split-item-label">nginx error (default)</span>
          <span class="split-item-meta">2m</span>
        </button>
        <button class="split-item">
          <span class="status-dot warn"></span>
          <span class="split-item-label">PostgreSQL 17 (main)</span>
          <span class="split-item-meta">12s</span>
        </button>
        <!-- … -->
      </div>
    </aside>

    <!-- DETAIL (rechts) -->
    <section class="split-detail">
      <!-- beliebige bestehende Panels: .panel, .panel-code, .ci-table, .form-row … -->
    </section>

  </div>
</div>
```

### Klassen-Spezifikation

| Klasse | Zweck |
|---|---|
| `.split-view` | Flex-Row-Container, füllt `content-body`. `gap` über Token. Auf Mobile → Spalten stapeln (column). |
| `.split-master` | Linke Spalte. Feste/begrenzte Breite (Token, s.u.), `flex-shrink: 0`, eigene Höhe, intern scrollbar via `.split-master-body`. |
| `.split-master-header` | Kopfzeile der Liste (Flex-Row, Titel links + Aktionen rechts via `margin-left:auto`). Optional. |
| `.split-master-body` | Scroll-Container der Items (`overflow-y: auto`). Höhe füllt verbleibenden Platz. |
| `.split-item` | Auswählbares Listen-Element (als `<button>`/`<a>` umsetzbar). Flex-Row: Dot · Label · Meta. Hover-State über `--surface-hover`. Tastatur-fokussierbar mit sichtbarem Fokus. |
| `.split-item.active` | Aktiver/gewählter Zustand (Hintergrund `--accent-subtle`, Akzent-Border o.ä. — Token-basiert). |
| `.split-item-label` | Primärtext (`--text`), `flex: 1`, `min-width: 0`, Ellipsis bei Überlauf. |
| `.split-item-meta` | Sekundärtext rechts (`--muted`, klein, `.mono` darf zusätzlich gesetzt werden). |
| `.split-detail` | Rechte Spalte. `flex: 1`, **`min-width: 0`** (wichtig, sonst sprengen lange Log-Zeilen/Tabellen das Layout). Eigener vertikaler Scroll bei Bedarf. |

> **Status-Dot:** Es wird die **bestehende** `.status-dot`-Komponente aus
> `css/page.css` wiederverwendet (`.on` / `.warn` / `.off`). Bitte **keine** neue
> Dot-Variante anlegen.

---

## 4. CSS-Anforderungen

- Neue Datei **`css/split.css`**, eingebunden über `css/index.css` (Master-Import).
- Nur Tokens, keine Rohwerte (Farben, Radien, Z-Index, Transitions).
- Verwendbare bestehende Tokens: `--card-bg`, `--panel`, `--border`,
  `--border-strong`, `--card-radius`, `--card-gap`, `--surface-hover`,
  `--accent-subtle`, `--accent-border`, `--text`, `--muted`, `--subtle`,
  `--transition-fast`.
- **Höhen/Scroll:** `.split-view` soll die verfügbare Höhe des `content-body`
  nutzen, sodass `.split-master-body` und `.split-detail` **unabhängig** scrollen
  (kein gemeinsamer Seiten-Scroll, der den Header wegschiebt). Bitte mit dem
  bestehenden `page.css`-Höhenmodell (Layout/`page-content` Flex) abstimmen —
  analog zu `.panel-body-flush--scroll`.
- **Responsive:** unterhalb des bestehenden Tablet-Breakpoints (wie bei
  `col-groups`) `flex-direction: column`; die Master-Spalte erhält dann volle
  Breite und eine begrenzte `max-height` (Token), darunter das Detail.
- **Reduced Motion:** etwaige Transitions unter `prefers-reduced-motion` deaktivieren.

### Neue Tokens (nur falls semantisch wiederverwendbar)

In `css/common.css` definieren **und** in `docs/tokens.md` dokumentieren:

| Token | Vorschlag | Zweck |
|---|---|---|
| `--split-master-width` | z.B. `300px` | Breite der Master-Spalte (Desktop) |
| `--split-master-max-h` | z.B. `320px` | max. Höhe der Master-Spalte im gestapelten Mobile-Layout |

(Falls bereits passende Spacing-Tokens existieren, diese bevorzugen.)

---

## 5. Referenz-Komponente

Datei **`components/split-view.html`** anlegen (mit `css/demo.css` wie andere
Referenzseiten), die zeigt:

1. Master-Liste mit mehreren `.split-item` (inkl. `.active` und allen drei
   `.status-dot`-Zuständen).
2. Detail-Bereich mit einem `.panel` (Filter via `.form-row`) und einer
   `.ci-table` in `.panel-body-flush--scroll`.
3. Den gestapelten Mobile-Zustand (über schmales Viewport sichtbar).

---

## 6. Doku-Updates im CI-Repo

- `docs/page-types.md`: Typ 6 — Split-View ergänzen; Eintrag in „Schnellreferenz"
  und den Punkt aus „Neues Design erforderlich" entsprechend anpassen/verweisen.
- `docs/split-view.md`: Komponenten-Doku (Zweck, HTML, Klassen, Tokens, Regeln) —
  analog zu `docs/code-viewer.md`.
- `docs/tokens.md`: ggf. neue Tokens.
- `css/index.css`: `split.css` importieren.
- `README.md` / `docs/usage.md`: bei Bedarf ergänzen.
- `CHANGELOG.md`: Eintrag (additiv, nicht breaking).

---

## 7. Akzeptanzkriterien (Checkliste)

- [ ] `.split-view` füllt `content-body`; Master und Detail scrollen unabhängig.
- [ ] `.split-detail` hat `min-width: 0` (lange `ci-table`/Log-Zeilen sprengen das Layout nicht).
- [ ] `.split-item` ist als `<button>`/`<a>` tastaturbedienbar mit sichtbarem Fokus; `.active` klar erkennbar.
- [ ] Lange Labels werden in `.split-item-label` per Ellipsis abgeschnitten.
- [ ] Reuse der bestehenden `.status-dot`-Klassen — keine neue Dot-Variante.
- [ ] Responsive: unter Tablet-Breakpoint gestapelt, Master mit begrenzter Höhe.
- [ ] Keine hardcodierten Farben/Radien/Z-Index/Transitions — nur Tokens.
- [ ] `css/demo.css` nur in `components/split-view.html`, nicht produktiv.
- [ ] Referenz-HTML, `docs/split-view.md`, `page-types.md`, `tokens.md`, `CHANGELOG.md` aktualisiert.

---

## 8. Was die Internal-Seite danach nutzt (Kontext, nicht Teil der CI-Arbeit)

Zur Einordnung für den CI-Agenten — so wird die Komponente konkret eingesetzt:

- Master = `GET /sources` + `GET /status` (Status-Dot aus `state`, Meta aus `age_seconds`).
- Detail = Filter-Panel (`form-row`: Volltextsuche, Level-Select, Zeitraum) +
  `ci-table` mit den Log-Einträgen (`GET /sources/{id}/logs`), Level als `badge`.

Es wird **kein** weiteres CI-Element benötigt, sofern Abschnitt 3–6 umgesetzt ist.
Sollte beim Bau der Seite doch noch etwas fehlen, wird es separat nachgemeldet.

# Split-View (Master-Detail) — Design / Spec

**Datum:** 2026-06-18
**Status:** Freigegeben · zur Umsetzung
**Angefragt von:** internal.oe5ith.at (neue „System Logs"-Seite)
**Version:** additiv → MINOR `v1.14.0`

Quelle: `ci-split-view-request.md` (Anforderung). Dieses Dokument ist die
freigegebene, technisch geklärte Design-Spec.

---

## 1. Zweck

Generische, wiederverwendbare CI-Komponente für zweispaltige
**Master-Detail-Layouts**: links eine schmale, scrollbare Auswahlliste
gleichartiger Einträge, rechts der Detailbereich zum gewählten Eintrag. Beide
gleichzeitig sichtbar, **unabhängig** scrollbar.

Kein log-spezifisches Styling — nur Tokens aus `common.css`, Reuse bestehender
Komponenten (`status-dot`, Buttons, Panels, `ci-table`, `form-row`).

Erster Einsatz: System-Logs-Seite (Master = Log-Quellen, Detail = Filter-Panel +
Log-Tabelle). Künftig auch für Konfig-/Browser-Seiten.

---

## 2. Neuer Seitentyp: Typ 6 — Split-View

**Wann verwenden:** Zwei nebeneinanderliegende Bereiche — links schmale,
scrollbare Auswahlliste gleichartiger Einträge, rechts Detailbereich zum
gewählten Eintrag. Beide gleichzeitig sichtbar, unabhängig scrollbar.

**Beispiele:** System Logs (Quellen → Einträge), künftige Konfig-/Browser-Seiten.

**Nicht geeignet wenn:** Keine dauerhafte Auswahlliste (→ Typ 1) oder Hauptinhalt
nur eine einzelne Tabelle (→ Typ 2).

---

## 3. Höhen-/Scroll-Modell (zentrale technische Entscheidung)

**Bestehendes Modell** (`common.css` / `page.css`):

- `.layout` = `height: calc(100vh - topbar)` + `overflow:hidden` → kein Seiten-Scroll.
- `.page-content` = `flex:1`, `overflow-y:auto`, `height:100%` → normaler Scroll-Container.
- `.page-header` = `flex-shrink:0`; darunter scrollt `.content-body`.

**Anforderung Split-View:** Header fix, `.split-master-body` und `.split-detail`
scrollen **unabhängig** in der Resthöhe — kein gemeinsamer Seiten-Scroll.

**Gewählter Ansatz: `:has()`-Auto-Aktivierung** (alles in `css/split.css`;
`common.css`/`page.css` bleiben unverändert; `:has()` wird im Repo bereits genutzt
— calendar.css, service-dashboard.css):

```css
.page-content:has(.split-view) { display:flex; flex-direction:column; overflow:hidden; }
.content-body:has(.split-view) { flex:1; min-height:0; overflow:hidden; }
.split-view { display:flex; gap:var(--card-gap); height:100%; min-height:0; }
```

Verworfen:
- **Explizite Modifier-Klassen** (`.page-content--fixed` etc.) — mehr HTML-Wissen
  nötig, berührt geteilte Struktur semantisch.
- **`calc()`-Festhöhe** auf `.split-view` — fragil (konstante Header-Höhe
  vorausgesetzt, bricht bei umbrechendem Mobile-Header).

---

## 4. HTML-Struktur

```html
<div class="content-body">
  <div class="split-view">

    <!-- MASTER (links) -->
    <aside class="split-master">
      <div class="split-master-header">
        <span class="ci-label">Quellen</span>
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
      <!-- bestehende Panels: .panel, .ci-table, .form-row … -->
    </section>

  </div>
</div>
```

---

## 5. Klassen-Spezifikation

| Klasse | Zweck / Regeln |
|---|---|
| `.split-view` | Flex-Row, füllt `content-body`. `gap: var(--card-gap)`, `height:100%`, `min-height:0`. Mobile → `flex-direction: column`. |
| `.split-master` | Linke Spalte. `width: var(--split-master-width)`, `flex-shrink:0`, Flex-Column, `min-height:0`. Karten-Optik: `--card-bg`, `1px solid --border`, `--card-radius`, `overflow:hidden`. |
| `.split-master-header` | Optionale Kopfzeile. Flex-Row, Titel links + Aktionen rechts (`margin-left:auto`), `flex-shrink:0`, `border-bottom:1px solid --border`. |
| `.split-master-body` | Scroll-Container. `flex:1`, `min-height:0`, `overflow-y:auto`. |
| `.split-item` | Auswählbares Element (`<button>`/`<a>`). Flex-Row: Dot · Label · Meta, `gap`, `width:100%`, linksbündig. Hover-BG `--surface-hover`. Tastatur-fokussierbar mit sichtbarem `:focus-visible` (Token-basiert). Transition `--transition-fast`. |
| `.split-item.active` | Aktiver Zustand: BG `--accent-subtle`, Akzent-Border/Marker via `--accent-border`. |
| `.split-item-label` | Primärtext `--text`, `flex:1`, `min-width:0`, Ellipsis (`overflow:hidden; text-overflow:ellipsis; white-space:nowrap`). |
| `.split-item-meta` | Sekundärtext rechts, `--muted`, klein, `flex-shrink:0`. `.mono` darf zusätzlich gesetzt werden. |
| `.split-detail` | Rechte Spalte. `flex:1`, **`min-width:0`** (sonst sprengen lange `ci-table`/Log-Zeilen das Layout). `min-height:0`, `overflow-y:auto` bei Bedarf. |

**Status-Dot:** bestehende `.status-dot`-Komponente aus `page.css`
(`.on`/`.warn`/`.off`) wiederverwenden — **keine** neue Dot-Variante.

---

## 6. Tokens

Neu in `css/common.css` (Definition) + `docs/tokens.md` (Doku):

| Token | Wert | Zweck |
|---|---|---|
| `--split-master-width` | `300px` | Breite der Master-Spalte (Desktop) |
| `--split-master-max-h` | `320px` | max. Höhe der Master-Spalte im gestapelten Mobile-Layout |

Sonst nur bestehende Tokens: `--card-bg`, `--border`, `--border-strong`,
`--card-radius`, `--card-gap`, `--surface-hover`, `--accent-subtle`,
`--accent-border`, `--text`, `--muted`, `--subtle`, `--transition-fast`.

---

## 7. Responsive & Motion

- Breakpoint analog `col-groups` (`@media (max-width: 768px)`):
  `.split-view{ flex-direction:column }`, `.split-master{ width:100%;
  max-height:var(--split-master-max-h) }`, darunter das Detail.
- `@media (prefers-reduced-motion: reduce)`: Transitions deaktivieren.

---

## 8. Referenz-Komponente

`components/split-view.html` (mit `css/demo.css` wie andere Referenzseiten):

1. Master-Liste mit mehreren `.split-item` (inkl. `.active` und allen drei
   `.status-dot`-Zuständen).
2. Detail mit `.panel` (Filter via `.form-row`) + `.ci-table` in
   `.panel-body-flush--scroll`.
3. Gestapelter Mobile-Zustand (über schmales Viewport sichtbar).

**Demo-Hinweis:** `demo.css` setzt `.page-content{ max-width:960px }`. Auf der
Split-Referenzseite wird die Breitenbegrenzung überschrieben (volle Breite), damit
das Höhen-/Scroll-Modell realistisch dargestellt wird.

---

## 9. Doku-/Registry-/Versions-Updates

- `css/split.css` — neue Datei.
- `css/index.css` — `@import "split.css";` (nach `code-viewer.css`/`calendar.css`).
- `docs/split-view.md` — Komponenten-Doku, analog `docs/code-viewer.md`,
  Doku-Standard G1–G4.
- `docs/page-types.md` — Typ 6 ergänzen; Schnellreferenz-Eintrag; „Neues Design
  erforderlich"-Punkt (Split-View) auf Typ 6 verweisen; Changelog-Zeile.
- `docs/tokens.md` — neue Tokens.
- `docs/registry.json` — Eintrag für Komponente; `python3
  scripts/cli/check_consistency.py` muss grün sein.
- `CHANGELOG.md` — `Added`-Eintrag (additiv, nicht breaking).
- `README.md`/`docs/usage.md` — bei Bedarf.
- Version: MINOR `v1.14.0`.

---

## 10. Akzeptanzkriterien

- [ ] `.split-view` füllt `content-body`; Master und Detail scrollen unabhängig.
- [ ] `.split-detail` hat `min-width: 0` (lange `ci-table`/Log-Zeilen sprengen das Layout nicht).
- [ ] `.split-item` als `<button>`/`<a>` tastaturbedienbar mit sichtbarem Fokus; `.active` klar erkennbar.
- [ ] Lange Labels in `.split-item-label` per Ellipsis abgeschnitten.
- [ ] Reuse der bestehenden `.status-dot`-Klassen — keine neue Dot-Variante.
- [ ] Responsive: unter 768px gestapelt, Master mit begrenzter Höhe.
- [ ] `prefers-reduced-motion`: Transitions aus.
- [ ] Keine hardcodierten Farben/Radien/Z-Index/Transitions — nur Tokens.
- [ ] `css/demo.css` nur in `components/split-view.html`, nicht produktiv.
- [ ] Referenz-HTML, `docs/split-view.md`, `page-types.md`, `tokens.md`,
      `registry.json`, `CHANGELOG.md` aktualisiert; `check_consistency.py` grün.

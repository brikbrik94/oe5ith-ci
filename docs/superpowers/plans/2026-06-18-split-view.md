# Split-View (Master-Detail) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eine generische, wiederverwendbare CI-Komponente „Split-View" (Master-Detail, Seitentyp Typ 6) bauen — schmale scrollbare Auswahlliste links, Detailbereich rechts, beide unabhängig scrollbar.

**Architecture:** Neue `css/split.css` mit `:has()`-Auto-Aktivierung des Fixed-Height-Modus (kein Eingriff in `common.css`/`page.css`-Layoutregeln außer zwei neuen Tokens). Reuse bestehender Komponenten (`status-dot`, Buttons, Panels, `ci-table`, `form-row`). Vollständige Doku-/Registry-/Changelog-Pflege; `check_consistency.py` als Gate.

**Tech Stack:** Reines CSS + HTML. Kein Build, kein Test-Framework. Verifikation: `python3 scripts/cli/check_consistency.py`, Struktur-Greps, visuelle Kontrolle der Referenzseite im Browser.

## Global Constraints

- Keine hardcodierten Werte — nur Tokens aus `css/common.css` für Farben, Backgrounds, Borders, Radien, Schatten, Z-Index, Transitions.
- Keine neuen Komponentenklassen, wo bestehende passen. Insbesondere: bestehende `.status-dot` (`.on`/`.warn`/`.off`) wiederverwenden — **keine** neue Dot-Variante.
- `css/common.css` bleibt Single Source of Truth; neue Tokens nur dort definieren + in `docs/tokens.md` dokumentieren.
- `css/demo.css` ausschließlich in `components/split-view.html`, nie produktiv.
- Jede produktive CSS muss in `css/index.css` importiert und in `docs/registry.json` registriert sein; `python3 scripts/cli/check_consistency.py` muss fehlerfrei sein.
- Doku folgt Doku-Standard G1–G4 (`docs/doc-standard.md`).
- Version: additiv → MINOR `v1.14.0`. Filenames ohne Versionsnummer.
- Verfügbare bestehende Tokens: `--card-bg`, `--border`, `--border-strong`, `--card-radius`, `--card-gap`, `--surface-hover`, `--accent-subtle`, `--accent-border`, `--text`, `--muted`, `--subtle`, `--transition-fast`.
- Spec: `docs/superpowers/specs/2026-06-18-split-view-design.md`.

---

### Task 1: Tokens

**Files:**
- Modify: `css/common.css` (Token-Definitionsblock)
- Modify: `docs/tokens.md`

**Interfaces:**
- Produces: CSS-Variablen `--split-master-width` (`300px`), `--split-master-max-h` (`320px`) — von Task 2 (`split.css`) konsumiert.

- [ ] **Step 1: Tokens in common.css ergänzen**

Finde im `:root`/Token-Block von `css/common.css` einen thematisch passenden Abschnitt (Layout-/Komponentenmaße, z.B. nahe `--sidebar-tab-height` oder Card-Maßen). Füge dort hinzu:

```css
  /* Split-View (Master-Detail, Typ 6) */
  --split-master-width:  300px;   /* Breite der Master-Spalte (Desktop) */
  --split-master-max-h:  320px;   /* max. Höhe der Master-Spalte im gestapelten Mobile-Layout */
```

- [ ] **Step 2: Tokens dokumentieren**

Ergänze in `docs/tokens.md` in der passenden Tabelle/Sektion (analog zu bestehenden Layout-Tokens) zwei Zeilen:

```markdown
| `--split-master-width` | `300px` | Breite der Master-Spalte (Split-View Typ 6, Desktop) |
| `--split-master-max-h` | `320px` | max. Höhe der Master-Spalte im gestapelten Mobile-Layout (Split-View Typ 6) |
```

Halte dich exakt an Spaltenformat/Sortierung der bestehenden Tabelle in `tokens.md`.

- [ ] **Step 3: Verifizieren**

Run: `grep -n "split-master-width\|split-master-max-h" css/common.css docs/tokens.md`
Expected: je 2 Treffer (common.css: Definition; tokens.md: Doku-Zeile) pro Token.

- [ ] **Step 4: Commit**

```bash
git add css/common.css docs/tokens.md
git commit -m "feat(tokens): add --split-master-width/--split-master-max-h for split-view"
```

---

### Task 2: split.css (Komponenten-CSS + Import)

**Files:**
- Create: `css/split.css`
- Modify: `css/index.css` (Import nach `code-viewer.css`/`calendar.css`)

**Interfaces:**
- Consumes: `--split-master-width`, `--split-master-max-h` (Task 1); bestehende Tokens (siehe Global Constraints).
- Produces: Klassen `.split-view`, `.split-master`, `.split-master-header`, `.split-master-body`, `.split-item`, `.split-item.active`, `.split-item-label`, `.split-item-meta`, `.split-detail` — von Task 3 (Referenz-HTML) konsumiert.

- [ ] **Step 1: `css/split.css` schreiben**

```css
/*
 * OE5ITH CI — split.css
 * Split-View (Master-Detail, Seitentyp Typ 6).
 * Schmale scrollbare Auswahlliste links, Detailbereich rechts,
 * beide unabhängig scrollbar.
 *
 * Voraussetzung: css/common.css, css/page.css
 * Status-Dot wird aus page.css wiederverwendet (.status-dot .on/.warn/.off).
 */

/* ═══════════════════════════════════════
   FIXED-HEIGHT-MODUS (Auto-Aktivierung)
   Bei vorhandener .split-view scrollt nicht
   mehr die Seite, sondern Master/Detail je
   für sich. common.css/page.css bleiben
   unverändert.
   ═══════════════════════════════════════ */
.page-content:has(.split-view) {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.content-body:has(.split-view) {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* ═══════════════════════════════════════
   SPLIT-VIEW CONTAINER
   ═══════════════════════════════════════ */
.split-view {
  display: flex;
  gap: var(--card-gap);
  height: 100%;
  min-height: 0;
}

/* ═══════════════════════════════════════
   MASTER (linke Spalte)
   ═══════════════════════════════════════ */
.split-master {
  width: var(--split-master-width);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--card-radius);
  overflow: hidden;
}

.split-master-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.split-master-header > :last-child {
  margin-left: auto;
}

.split-master-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

/* ═══════════════════════════════════════
   SPLIT-ITEM (Listen-Eintrag)
   Als <button> oder <a> umsetzbar.
   ═══════════════════════════════════════ */
.split-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 9px 12px;
  text-align: left;
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--border);
  color: var(--text);
  font: inherit;
  cursor: pointer;
  transition: background var(--transition-fast);
}
.split-item:last-child { border-bottom: none; }
.split-item:hover { background: var(--surface-hover); }
.split-item:focus-visible {
  outline: 2px solid var(--accent-border);
  outline-offset: -2px;
}
.split-item.active {
  background: var(--accent-subtle);
  box-shadow: inset 2px 0 0 var(--accent-border);
}

.split-item-label {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--text);
}

.split-item-meta {
  flex-shrink: 0;
  font-size: 0.72rem;
  color: var(--muted);
}

/* ═══════════════════════════════════════
   DETAIL (rechte Spalte)
   min-width:0 verhindert, dass lange
   ci-table-/Log-Zeilen das Layout sprengen.
   ═══════════════════════════════════════ */
.split-detail {
  flex: 1;
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--card-gap);
}

/* ═══════════════════════════════════════
   RESPONSIVE — gestapelt unter Tablet
   (Breakpoint analog col-groups)
   ═══════════════════════════════════════ */
@media (max-width: 768px) {
  .split-view { flex-direction: column; }
  .split-master {
    width: 100%;
    max-height: var(--split-master-max-h);
  }
}

/* ═══════════════════════════════════════
   REDUCED MOTION
   ═══════════════════════════════════════ */
@media (prefers-reduced-motion: reduce) {
  .split-item { transition: none; }
}
```

- [ ] **Step 2: Import in `css/index.css` ergänzen**

Finde in `css/index.css` den Block „4a. Komponenten" mit `@import "code-viewer.css";` und `@import "calendar.css";`. Füge direkt danach hinzu:

```css
@import "split.css";
```

- [ ] **Step 3: CSS-Validität & keine Rohwerte prüfen**

Run: `grep -nE "#[0-9a-fA-F]{3,6}|rgba?\(|[0-9]+px solid|z-index" css/split.css`
Expected: Nur Token-basierte Werte und strukturelle px (Padding/Gap/Width/font-size/outline) — **keine** hardcodierten Farben (`#...`, `rgb...`) und kein hardcodiertes `z-index`. Treffer auf `1px solid var(--border)` sind ok (Border-Breite ist strukturell, Farbe ist Token).

Run: `grep -c "var(--" css/split.css`
Expected: > 0 (Tokens werden verwendet).

- [ ] **Step 4: Commit**

```bash
git add css/split.css css/index.css
git commit -m "feat(split): add split.css (master-detail layout, typ 6)"
```

---

### Task 3: Referenz-HTML `components/split-view.html`

**Files:**
- Create: `components/split-view.html`

**Interfaces:**
- Consumes: Klassen aus Task 2 (`split.css`), bestehende `.status-dot`, `.btn`/`.btn-sm`/`.btn-ghost`, `.panel`/`.panel-header`/`.panel-body`/`.panel-body-flush--scroll`, `.ci-table`, `.form-row`, `.badge`, `.ci-label`.

- [ ] **Step 1: Struktur einer bestehenden Referenzseite als Vorlage ansehen**

Run: `sed -n '1,90p' components/service-dashboard-detail.html`
Ziel: `<head>`-Block (eingebundene CSS inkl. `demo.css` + FontAwesome), `layout` → `sidebar` → `page-content` → `page-header` + `content-body` exakt übernehmen. Sidebar/Topbar/Head 1:1 nach bestehendem Muster.

- [ ] **Step 2: `components/split-view.html` schreiben**

Erzeuge die Seite nach dem Muster aus Step 1 mit folgendem Inhalt im `content-body`. `<head>` muss enthalten: alle produktiven CSS (oder `css/index.css`) **und** `css/demo.css` **und** eine seiteneigene Breiten-Aufhebung (demo.css setzt `.page-content{max-width:960px}`):

```html
    <style>
      /* Nur für diese Referenzseite: volle Breite, damit das
         Höhen-/Scroll-Modell realistisch sichtbar ist. */
      .page-content { max-width: none; }
    </style>
```

`content-body`-Inhalt:

```html
      <div class="content-body">
        <div class="split-view">

          <!-- MASTER -->
          <aside class="split-master">
            <div class="split-master-header">
              <span class="ci-label">Quellen</span>
              <button class="btn btn-sm btn-ghost" title="Pausieren"><i class="fa-solid fa-pause"></i></button>
              <button class="btn btn-sm btn-ghost" title="Aktualisieren"><i class="fa-solid fa-rotate"></i></button>
            </div>
            <div class="split-master-body">
              <button class="split-item active">
                <span class="status-dot on"></span>
                <span class="split-item-label">nginx error (default)</span>
                <span class="split-item-meta mono">2m</span>
              </button>
              <button class="split-item">
                <span class="status-dot warn"></span>
                <span class="split-item-label">PostgreSQL 17 (main) — sehr langer Quellenname zum Test der Ellipsis-Abschneidung</span>
                <span class="split-item-meta mono">12s</span>
              </button>
              <button class="split-item">
                <span class="status-dot off"></span>
                <span class="split-item-label">systemd / sshd</span>
                <span class="split-item-meta mono">4h</span>
              </button>
            </div>
          </aside>

          <!-- DETAIL -->
          <section class="split-detail">
            <div class="panel">
              <div class="panel-header">
                <div class="panel-title"><i class="fa-solid fa-filter"></i> Filter</div>
              </div>
              <div class="panel-body">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Suche</label>
                    <input class="form-input" type="text" placeholder="Volltext…">
                  </div>
                  <div class="form-group">
                    <label class="form-label">Level</label>
                    <select class="form-input">
                      <option>Alle</option><option>INFO</option><option>WARN</option><option>ERROR</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <div class="panel">
              <div class="panel-header">
                <div class="panel-title"><i class="fa-solid fa-list"></i> Einträge</div>
              </div>
              <div class="panel-body-flush panel-body-flush--scroll">
                <table class="ci-table">
                  <thead>
                    <tr><th class="mono">Zeit</th><th>Level</th><th>Nachricht</th></tr>
                  </thead>
                  <tbody>
                    <tr><td class="mono">12:01:44</td><td><span class="badge badge-danger">ERROR</span></td><td>upstream timed out (110: Connection timed out) while reading response header from upstream</td></tr>
                    <tr><td class="mono">12:01:39</td><td><span class="badge badge-warning">WARN</span></td><td>client closed connection while waiting for request</td></tr>
                    <tr><td class="mono">12:01:30</td><td><span class="badge">INFO</span></td><td>reload signal received, reconfiguring</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>

        </div>
      </div>
```

Hinweis: Tatsächliche Badge-Klassennamen (`badge-danger`/`badge-warning` etc.) und Form-Klassen (`form-row`/`form-group`/`form-label`/`form-input`) vor dem Schreiben gegen `css/badges.css` bzw. `css/forms.css` verifizieren und exakt übernehmen.

- [ ] **Step 3: Klassen-Existenz verifizieren**

Run: `grep -oE "badge[a-z-]*|form-[a-z]+" components/split-view.html | sort -u`
Dann je Klasse prüfen: `grep -rn "<klasse>" css/badges.css css/forms.css`
Expected: Jede im HTML benutzte Badge-/Form-Klasse existiert in der jeweiligen CSS. Falls nicht → Klassennamen im HTML korrigieren.

- [ ] **Step 4: Visuell kontrollieren**

Öffne `components/split-view.html` im Browser. Prüfe:
- Zwei Spalten nebeneinander; Master ~300px, Detail füllt Rest.
- Master-Liste scrollt unabhängig; lange Labels (Zeile 2) werden mit „…" abgeschnitten.
- `.active`-Item klar hervorgehoben; alle drei Dot-Zustände (on/warn/off) sichtbar.
- Fenster schmal ziehen (<768px): Spalten stapeln, Master mit begrenzter Höhe oben.
- Tab-Taste: Items fokussierbar mit sichtbarem Fokusrahmen.

- [ ] **Step 5: Commit**

```bash
git add components/split-view.html
git commit -m "docs(split): add components/split-view.html reference page"
```

---

### Task 4: Komponenten-Doku `docs/split-view.md`

**Files:**
- Create: `docs/split-view.md`

**Interfaces:**
- Consumes: Klassen/Tokens aus Task 1–2 (für G1-Tabelle und Token-Sektion).

- [ ] **Step 1: Vorlage ansehen**

Run: `sed -n '1,120p' docs/code-viewer.md`
Ziel: Aufbau (Zweck, HTML-Beispiel, Element-Tabelle, Struktur, Zustände, Tokens, Regeln) und Ton übernehmen — Doku-Standard G1–G4.

- [ ] **Step 2: `docs/split-view.md` schreiben**

Muss alle vier Garantien erfüllen:
- **G1 — Element-Tabelle:** alle Klassen aus Task 2 mit Zweck (1:1 aus Spec §5).
- **G2 — Struktur/Verschachtelung:** der HTML-Baum aus Spec §4.
- **G3 — Reihenfolge/Platzierung:** `.split-view` direkt in `.content-body`; Master vor Detail; Status-Dot zuerst im Item; Header optional, Body pflicht.
- **G4 — Zustände/Varianten:** `.split-item.active`, Hover, `:focus-visible`, Status-Dot `.on/.warn/.off`, gestapeltes Mobile-Layout.

Zusätzlich Sektionen:
- Zweck (Spec §1) + wann verwenden / nicht verwenden (Spec §2).
- Höhen-/Scroll-Modell: Hinweis, dass der Fixed-Height-Modus automatisch via `:has(.split-view)` aktiviert wird — keine Zusatzklassen nötig.
- Tokens: `--split-master-width`, `--split-master-max-h`.
- Regeln: nur Tokens; `.status-dot` reuse (keine neue Variante); `.split-detail` braucht `min-width:0`; `.split-item` als `<button>`/`<a>`.

- [ ] **Step 3: G1–G4-Selbstprüfung**

Prüffrage (aus `doc-standard.md`): „Kann ich die Komponente korrekt bauen, ohne `components/split-view.html` zu öffnen?" Wenn nein → fehlende Garantie ergänzen.

Run: `grep -n "split-view\|split-master\|split-item\|split-detail\|split-master-width\|split-master-max-h" docs/split-view.md`
Expected: alle Klassen und beide Tokens kommen vor.

- [ ] **Step 4: Commit**

```bash
git add docs/split-view.md
git commit -m "docs(split): add component doc (G1-G4)"
```

---

### Task 5: `docs/page-types.md` — Typ 6

**Files:**
- Modify: `docs/page-types.md`

- [ ] **Step 1: Bestehende Typ-Sektion als Vorlage lesen**

Run: `sed -n '146,180p' docs/page-types.md`
(Typ 4 — Column-Groups: Aufbau „Wann verwenden / Struktur / … / Nicht geeignet wenn" übernehmen.)

- [ ] **Step 2: Typ-6-Sektion ergänzen**

Nach Typ 5 (Landing) bzw. an passender Stelle eine neue Sektion „## Typ 6 — Split-View (Master-Detail)" einfügen mit:
- Wann verwenden / Beispiele / Struktur (ASCII-Baum aus Spec §2 + §4) / Nicht geeignet wenn (Spec §2).
- Verweis: Höhenmodus aktiviert sich automatisch; Komponenten-Doku `docs/split-view.md`.

- [ ] **Step 3: Schnellreferenz + „Neues Design"-Punkt anpassen**

In der Schnellreferenz-Tabelle (~Zeile 252) eine Zeile ergänzen:

```markdown
| Master-Detail / Split-View | Typ 6 |
```

Im Abschnitt „Neues Design erforderlich wenn…" (~Zeile 266) den Split-View-Punkt so umschreiben, dass er auf Typ 6 verweist (Split-View ist jetzt definiert, nicht mehr „neues Design erforderlich").

Changelog-Zeile am Ende der Datei ergänzen:

```markdown
| 2026-06-18 | Typ 6 — Split-View (Master-Detail) ergänzt. Schnellreferenz + „Neues Design"-Punkt aktualisiert. |
```

- [ ] **Step 4: Verifizieren**

Run: `grep -n "Typ 6\|Split-View" docs/page-types.md`
Expected: Sektion, Schnellreferenz-Eintrag, Changelog-Zeile vorhanden; „Neues Design erforderlich"-Punkt verweist auf Typ 6.

- [ ] **Step 5: Commit**

```bash
git add docs/page-types.md
git commit -m "docs(page-types): add Typ 6 Split-View"
```

---

### Task 6: Registry, Consistency-Check, Changelog, Version

**Files:**
- Modify: `docs/registry.json`
- Modify: `CHANGELOG.md`
- Modify: `README.md` (auto-generiert durch check_consistency)

**Interfaces:**
- Consumes: alle Artefakte aus Task 1–5.

- [ ] **Step 1: Registry-Eintrag ergänzen**

In `docs/registry.json`, im `components`-Array bei den Komponenten (z.B. nach `code-viewer`), neuen Eintrag einfügen — exakt im bestehenden Format:

```json
    { "id": "split-view", "title": "Split-View (Master-Detail)", "category": "component",
      "css": ["split.css"], "doc": ["split-view.md"], "html": ["split-view.html"] },
```

Auf gültiges JSON achten (Komma-Platzierung).

- [ ] **Step 2: Consistency-Check (Gate)**

Run: `python3 scripts/cli/check_consistency.py`
Expected: keine Fehler („Repo ist konsistent" / Erfolg). Bei Fehlern (fehlender Import / nicht registrierte Datei) → beheben, bis grün.

- [ ] **Step 3: README regenerieren**

Run: `python3 scripts/cli/check_consistency.py --write`
Expected: README-Blöcke aktualisiert, weiterhin keine Fehler.

- [ ] **Step 4: CHANGELOG ergänzen**

In `CHANGELOG.md` unter der nächsten Version `## [1.14.0]` (Datum 2026-06-18) einen `### Added`-Block:

```markdown
### Added
- **Split-View (Typ 6)** — generische Master-Detail-Komponente: schmale scrollbare Auswahlliste links, Detailbereich rechts, beide unabhängig scrollbar. Neue `css/split.css`, Tokens `--split-master-width`/`--split-master-max-h`, Doku `docs/split-view.md`, Referenz `components/split-view.html`, Seitentyp Typ 6 in `docs/page-types.md`.
```

Halte dich exakt an das bestehende CHANGELOG-Format (Kategorien `Added`/`Changed`/`Fixed`).

- [ ] **Step 5: Finale Verifikation**

Run: `python3 scripts/cli/check_consistency.py`
Expected: keine Fehler.

Run: `grep -n "split-view" docs/registry.json README.md`
Expected: registriert und in README gelistet.

- [ ] **Step 6: Commit**

```bash
git add docs/registry.json README.md CHANGELOG.md
git commit -m "docs(split): register split-view component, changelog v1.14.0"
```

---

## Hinweis zur Versionierung (nach Plan-Abschluss, nicht Teil der Tasks)

Tag erst nach Freigabe durch den User setzen:

```bash
git tag -a v1.14.0 -m "Release v1.14.0 — Split-View (Typ 6)"
git push origin main --tags
```

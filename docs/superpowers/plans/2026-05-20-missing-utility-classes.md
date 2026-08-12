# Missing Utility Classes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Alle in `CI_MISSING_STYLES.md` (website-v3) aufgelisteten fehlenden CSS-Klassen in das `oe5ith-ci`-Repo einpflegen, damit nachgelagerte Projekte ohne `app.css`-Overrides auskommen.

**Architecture:** Jede Klasse wird in die architektonisch korrekte CSS-Datei eingetragen (nicht nach spec-Vorschlag, sondern nach Datei-Verantwortlichkeit). Gleichzeitig werden die zugehörigen `components/`-Referenz-HTMLs aktualisiert, damit jede Klasse visuell verifizierbar ist. Keine neuen Dateien.

**Tech Stack:** Vanilla CSS mit CI-Token-System (`var(--...)`), statische HTML-Referenzseiten, kein Build-Step.

---

## Datei-Übersicht

| Datei | Änderung |
|---|---|
| `css/utils.css` | Neue Sektionen: Text/Visibility, Flex-Erweiterungen, Spacing, Cursor/Position, Table, Border |
| `css/typography.css` | Neue Sektion: Font-Weights und Farb-Utilities |
| `css/sidebar.css` | `.acc-dot` Standardfarbe + `.acc-item.loading-state` / `.acc-item.error-state` |
| `css/cards.css` | `.sprite-preview-img` |
| `css/coords.css` | `.coord-header-status` |
| `components/utils.html` | Demos für alle neuen utils-Klassen |
| `components/typography.html` | Demos für Font-Weights + Farb-Utilities |
| `components/sidebar.html` | Demo für acc-dot + Loading/Error-Zustände |
| `components/cards.html` | Demo für `.sprite-preview-img` |
| `CHANGELOG.md` | Eintrag unter `[Unreleased]` |

**Datei-Entscheidungen vs. Spec:**
- `.pos-relative`, `.cursor-pointer`, `.no-dot-bg`, `.border-collapse`, `.table-col-25` → `utils.css` (allgemeine Utilities, nicht page-spezifisch)
- `.coord-header-status` → `coords.css` (nicht `page.css`; gehört zum Koordinaten-Umrechner-Kontext)

---

## Task 1: utils.css — Text, Visibility & Border

**Files:**
- Modify: `css/utils.css`

- [ ] **Step 1: Neue Sektion in `css/utils.css` nach der FLEX-Sektion einfügen**

Öffne `css/utils.css`. Füge nach der bestehenden Zeile `.flex-center { ... }` folgende Sektionen ein:

```css
/* ═══════════════════════════════════════
   TEXT & VISIBILITY UTILITIES
   ═══════════════════════════════════════ */

.text-center { text-align: center; }
.text-left   { text-align: left; }
.opacity-50  { opacity: 0.5; }
.hidden      { display: none !important; }

/* ═══════════════════════════════════════
   FLEX EXTENSIONS
   ═══════════════════════════════════════ */

.flex-1            { flex: 1; }
.flex-2            { flex: 2; }
.w-full            { width: 100%; }
.flex-align-center { display: flex; align-items: center; }
.justify-between   { justify-content: space-between; }
.gap-4             { gap: 4px; }

/* ═══════════════════════════════════════
   TABLE UTILITIES
   ═══════════════════════════════════════ */

/* Horizontales Scrollen auf Mobile für Tabellen */
.table-wrapper  { overflow-x: auto; width: 100%; }
.table-col-25   { width: 25%; }
.border-collapse { border-collapse: collapse; }

/* ═══════════════════════════════════════
   SPACING UTILITIES
   ═══════════════════════════════════════ */

.m-0   { margin: 0; }
.mt-0  { margin-top: 0; }
.mt-8  { margin-top: 8px; }
.mt-12 { margin-top: 12px; }
.mb-8  { margin-bottom: 8px; }
.pb-0  { padding-bottom: 0; }

/* Token-basierte Abstände */
.p-double-gap   { padding: calc(2 * var(--card-gap)); }
.mb-1-5-gap     { margin-bottom: calc(1.5 * var(--card-gap)); }

/* Fester Abstand — kein Token vorhanden */
.p-2rem { padding: 2rem; }

/* ═══════════════════════════════════════
   POSITION & CURSOR UTILITIES
   ═══════════════════════════════════════ */

.pos-relative  { position: relative; }
.cursor-pointer { cursor: pointer; }

/* ═══════════════════════════════════════
   BORDER UTILITIES
   ═══════════════════════════════════════ */

.border-none { border: none; }

/* Unterdrückt Dot-Hintergrund für reine Icon-Status-Anzeigen */
.no-dot-bg { background: none !important; box-shadow: none !important; }
```

- [ ] **Step 2: Prüfen dass alle Klassen vorhanden sind**

```bash
grep -c "text-center\|flex-1\|table-wrapper\|mt-12\|pos-relative\|no-dot-bg" /root/git/oe5ith-ci/css/utils.css
```

Erwartete Ausgabe: `6` (alle 6 Pattern gefunden)

- [ ] **Step 3: Commit**

```bash
git add css/utils.css
git commit -m "feat(utils): add text, flex, table, spacing, position and border utilities"
```

---

## Task 2: typography.css — Font-Weights & Farb-Utilities

**Files:**
- Modify: `css/typography.css`

- [ ] **Step 1: Neue Sektion in `css/typography.css` ans Ende (nach `.ci-label`) anhängen**

```css
/* ── Font-Weight Utilities ── */

.font-medium   { font-weight: 500; }
.font-semibold { font-weight: 600; }

/* ── Text-Color Utilities (CI-Token-basiert) ── */

.t-success { color: var(--success); }
.t-danger  { color: var(--danger); }
.t-muted   { color: var(--muted); }
.t-subtle  { color: var(--subtle); }
.t-white   { color: var(--white); }
.t-tiny    { font-size: 0.75rem; }
```

- [ ] **Step 2: Prüfen**

```bash
grep -c "font-medium\|t-success\|t-tiny" /root/git/oe5ith-ci/css/typography.css
```

Erwartete Ausgabe: `3`

- [ ] **Step 3: Commit**

```bash
git add css/typography.css
git commit -m "feat(typography): add font-weight and color utility classes"
```

---

## Task 3: sidebar.css — acc-dot Standardfarbe & Loading/Error-Zustände

**Files:**
- Modify: `css/sidebar.css`

**Hintergrund:** Der Kommentar auf Zeile 106 lautet `/* Dot — Farbe ist site-spezifisch, kein CI-Token */`. Das ist der Grund, warum `background` bisher fehlt. Laut `CI_MISSING_STYLES.md` soll `var(--accent)` als sinnvoller CI-Default gesetzt werden — site-spezifische Overrides sind weiterhin möglich.

- [ ] **Step 1: `.acc-dot` in `css/sidebar.css` Zeile 107 anpassen**

Alt:
```css
/* Dot — Farbe ist site-spezifisch, kein CI-Token */
.acc-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
```

Neu:
```css
/* Dot — Akzentfarbe als CI-Default; site-spezifische Overrides möglich */
.acc-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; background: var(--accent); }
```

- [ ] **Step 2: Loading- und Error-Zustände nach `.acc-item.checked .acc-item-label` (Zeile 177) einfügen**

```css
.acc-item.loading-state {
  padding-left: 24px;
  color: var(--subtle);
  font-size: 0.8rem;
}
.acc-item.error-state {
  padding-left: 24px;
  color: var(--danger);
  font-size: 0.8rem;
}
```

- [ ] **Step 3: Prüfen**

```bash
grep -n "acc-dot\|loading-state\|error-state" /root/git/oe5ith-ci/css/sidebar.css
```

Erwartete Ausgabe: 3 Treffer (acc-dot mit background, loading-state, error-state)

- [ ] **Step 4: Commit**

```bash
git add css/sidebar.css
git commit -m "feat(sidebar): add accent default to acc-dot and loading/error states for acc-item"
```

---

## Task 4: cards.css — sprite-preview-img

**Files:**
- Modify: `css/cards.css`

- [ ] **Step 1: `.sprite-preview-img` in `css/cards.css` einfügen**

Öffne `css/cards.css`. Füge am Ende der Datei eine neue Sektion ein:

```css
/* ═══════════════════════════════════════
   SPRITE & ASSET PREVIEW
   ═══════════════════════════════════════ */

/* Quadratische Icon-/Bildvorschau innerhalb von Cards (z.B. Inventory-Debugger) */
.sprite-preview-img {
  width: 20px;
  height: 20px;
  padding: 2px;
  border-radius: var(--badge-radius);
  background: var(--bg);
  object-fit: contain;
}
```

- [ ] **Step 2: Prüfen**

```bash
grep -n "sprite-preview-img" /root/git/oe5ith-ci/css/cards.css
```

Erwartete Ausgabe: 1 Treffer mit der Klassendefinition

- [ ] **Step 3: Commit**

```bash
git add css/cards.css
git commit -m "feat(cards): add sprite-preview-img for icon/asset thumbnails in cards"
```

---

## Task 5: coords.css — coord-header-status

**Files:**
- Modify: `css/coords.css`

- [ ] **Step 1: `.coord-header-status` in `css/coords.css` einfügen**

Öffne `css/coords.css`. Füge am Ende der Datei an:

```css
/* ═══════════════════════════════════════
   COORD-HEADER-STATUS — Zusatzinfo im Block-Header
   ═══════════════════════════════════════ */

.coord-header-status {
  font-size: 0.65rem;
  color: var(--subtle);
  font-weight: 500;
}
```

- [ ] **Step 2: Prüfen**

```bash
grep -n "coord-header-status" /root/git/oe5ith-ci/css/coords.css
```

Erwartete Ausgabe: 1 Treffer

- [ ] **Step 3: Commit**

```bash
git add css/coords.css
git commit -m "feat(coords): add coord-header-status for subtitle text in coord block headers"
```

---

## Task 6: components/utils.html — Referenz-Demos aktualisieren

**Files:**
- Modify: `components/utils.html`

- [ ] **Step 1: Inline-CSS in `components/utils.html` im `<style>`-Block erweitern**

Lies `components/utils.html`. Suche den Block der bestehenden Utils-Klassen im `<style>`-Tag (aktuell: `.full-map`, `.m-gap`, `.mb-gap`, `.flex-col`, `.flex-center`). Füge danach die neuen Klassen ein:

```css
/* Text & Visibility */
.text-center    { text-align: center; }
.text-left      { text-align: left; }
.opacity-50     { opacity: 0.5; }
.hidden         { display: none !important; }
/* Flex Extensions */
.flex-1            { flex: 1; }
.flex-2            { flex: 2; }
.w-full            { width: 100%; }
.flex-align-center { display: flex; align-items: center; }
.justify-between   { justify-content: space-between; }
.gap-4             { gap: 4px; }
/* Table */
.table-wrapper   { overflow-x: auto; width: 100%; }
.table-col-25    { width: 25%; }
.border-collapse { border-collapse: collapse; }
/* Spacing */
.m-0   { margin: 0; }
.mt-0  { margin-top: 0; }
.mt-8  { margin-top: 8px; }
.mt-12 { margin-top: 12px; }
.mb-8  { margin-bottom: 8px; }
.pb-0  { padding-bottom: 0; }
.p-double-gap { padding: calc(2 * 20px); }
.mb-1-5-gap   { margin-bottom: calc(1.5 * 20px); }
.p-2rem       { padding: 2rem; }
/* Position & Cursor */
.pos-relative   { position: relative; }
.cursor-pointer { cursor: pointer; }
/* Border */
.border-none { border: none; }
.no-dot-bg   { background: none !important; box-shadow: none !important; }
```

- [ ] **Step 2: Demo-Sektionen am Ende des `<body>` (vor `</body>`) anhängen**

```html
<!-- TEXT & VISIBILITY -->
<div class="section">
  <div class="section-label">.text-center / .text-left / .opacity-50 / .hidden</div>
  <div class="section-desc">Text-Alignment und Sichtbarkeit. <code>.hidden</code> entspricht <code>display:none !important</code>.</div>
  <div class="demo-box" style="flex-direction:column; gap:8px;">
    <div class="demo-item text-center" style="width:100%"><div class="demo-label">.text-center</div>Text zentriert</div>
    <div class="demo-item text-left"   style="width:100%"><div class="demo-label">.text-left</div>Text links</div>
    <div class="demo-item opacity-50"  style="width:100%"><div class="demo-label">.opacity-50</div>50% Opazität</div>
    <div class="demo-item" style="width:100%"><div class="demo-label">.hidden</div><span class="hidden">Dieses Element ist versteckt.</span><em style="color:var(--subtle)">(Element nicht sichtbar)</em></div>
  </div>
</div>

<!-- FLEX EXTENSIONS -->
<div class="section">
  <div class="section-label">.flex-1 / .flex-2 / .w-full / .flex-align-center / .justify-between / .gap-4</div>
  <div class="section-desc">Ergänzungen zum Flex-System.</div>
  <div class="demo-box" style="flex-direction:column; gap:10px;">
    <div>
      <div class="demo-label">.flex-1 / .flex-2 (im Flex-Parent)</div>
      <div style="display:flex; gap:6px; width:100%;">
        <div class="demo-item flex-1"><code>.flex-1</code></div>
        <div class="demo-item flex-2"><code>.flex-2</code></div>
      </div>
    </div>
    <div>
      <div class="demo-label">.flex-align-center</div>
      <div class="demo-item flex-align-center" style="gap:8px; width:100%;">
        <span style="width:12px;height:12px;background:var(--accent);border-radius:50%;display:inline-block;flex-shrink:0;"></span>
        <span>Vertikal zentriert</span>
      </div>
    </div>
    <div>
      <div class="demo-label">.justify-between</div>
      <div class="demo-item flex-align-center justify-between" style="width:100%;">
        <span>Links</span><span>Rechts</span>
      </div>
    </div>
    <div>
      <div class="demo-label">.w-full</div>
      <div class="demo-item w-full"><code>.w-full</code> — volle Breite</div>
    </div>
    <div>
      <div class="demo-label">.gap-4</div>
      <div class="demo-item flex-align-center gap-4" style="width:100%;">
        <span style="background:var(--border);padding:4px 8px;border-radius:3px;">A</span>
        <span style="background:var(--border);padding:4px 8px;border-radius:3px;">B</span>
        <span style="background:var(--border);padding:4px 8px;border-radius:3px;">C</span>
        <span style="color:var(--subtle); font-size:0.72rem;">(gap: 4px)</span>
      </div>
    </div>
  </div>
</div>

<!-- TABLE UTILITIES -->
<div class="section">
  <div class="section-label">.table-wrapper / .table-col-25 / .border-collapse</div>
  <div class="section-desc"><code>.table-wrapper</code> ermöglicht horizontales Scrollen auf Mobile. <code>.table-col-25</code> setzt die Spaltenbreite auf 25%. <code>.border-collapse</code> setzt <code>border-collapse: collapse</code>.</div>
  <div class="demo-box">
    <div class="table-wrapper" style="max-width:400px;">
      <table class="border-collapse" style="width:100%; font-size:0.8rem;">
        <thead>
          <tr style="border-bottom:1px solid var(--border);">
            <th class="table-col-25" style="padding:6px 8px; text-align:left; color:var(--muted);">25%</th>
            <th style="padding:6px 8px; text-align:left; color:var(--muted);">Spalte 2</th>
            <th style="padding:6px 8px; text-align:left; color:var(--muted);">Spalte 3 (lang)</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:6px 8px; color:var(--text);">Wert</td>
            <td style="padding:6px 8px; color:var(--text);">Wert</td>
            <td style="padding:6px 8px; color:var(--text); white-space:nowrap;">Langer Inhalt scrollt →</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<!-- SPACING -->
<div class="section">
  <div class="section-label">.mt-8 / .mt-12 / .mb-8 / .m-0 / .mt-0 / .pb-0 / .p-double-gap / .mb-1-5-gap / .p-2rem</div>
  <div class="section-desc">Spacing-Utilities. Token-basierte Abstände nutzen <code>--card-gap</code> (20px); feste Pixel-Werte für spezifische Layouts.</div>
  <div class="demo-box" style="flex-direction:column; gap:6px;">
    <div class="demo-item mt-8" style="background:var(--panel-deep);">
      <div class="demo-label">.mt-8</div>margin-top: 8px
    </div>
    <div class="demo-item mt-12" style="background:var(--panel-deep);">
      <div class="demo-label">.mt-12</div>margin-top: 12px
    </div>
    <div class="demo-item mb-8" style="background:var(--panel-deep);">
      <div class="demo-label">.mb-8</div>margin-bottom: 8px
    </div>
    <div class="demo-item p-double-gap" style="background:var(--panel-deep);">
      <div class="demo-label">.p-double-gap</div>padding: calc(2 × 20px) = 40px
    </div>
    <div class="demo-item p-2rem" style="background:var(--panel-deep);">
      <div class="demo-label">.p-2rem</div>padding: 2rem
    </div>
  </div>
</div>

<!-- POSITION & CURSOR & BORDER -->
<div class="section">
  <div class="section-label">.pos-relative / .cursor-pointer / .border-none / .no-dot-bg</div>
  <div class="section-desc">Positionierung, Cursor und Border-Overrides.</div>
  <div class="demo-box" style="gap:12px; flex-wrap:wrap;">
    <div class="demo-item pos-relative" style="width:160px; height:60px;">
      <div class="demo-label">.pos-relative</div>
      <span style="position:absolute; top:6px; right:8px; font-size:0.62rem; background:var(--accent); color:#fff; padding:1px 5px; border-radius:3px;">abs. Kind</span>
    </div>
    <div class="demo-item cursor-pointer">
      <div class="demo-label">.cursor-pointer</div>
      Hover → Zeiger
    </div>
    <div class="demo-item border-none">
      <div class="demo-label">.border-none</div>
      Kein Rahmen
    </div>
    <div>
      <div class="demo-label">.no-dot-bg</div>
      <div style="display:flex; align-items:center; gap:8px;">
        <div style="width:10px;height:10px;border-radius:50%;background:var(--accent);"></div>
        <span style="font-size:0.75rem;color:var(--muted);">Normal (.acc-dot)</span>
      </div>
      <div style="display:flex; align-items:center; gap:8px; margin-top:6px;">
        <div class="no-dot-bg" style="width:10px;height:10px;border-radius:50%;background:var(--accent);"></div>
        <span style="font-size:0.75rem;color:var(--muted);">Mit .no-dot-bg</span>
      </div>
    </div>
  </div>
</div>
```

- [ ] **Step 3: Datei im Browser öffnen und visuell prüfen**

```
file:///root/git/oe5ith-ci/components/utils.html
```

Alle Sektionen sollen gerendert werden, kein leeres/unstyled Demo.

- [ ] **Step 4: Commit**

```bash
git add components/utils.html
git commit -m "docs(utils): add reference demos for all new utility classes"
```

---

## Task 7: components/typography.html — Referenz-Demos aktualisieren

**Files:**
- Modify: `components/typography.html`

- [ ] **Step 1: Lies `components/typography.html` um Struktur zu verstehen**

Suche die bestehende `<style>`-Sektion und die letzte `.section`-Demo im `<body>`.

- [ ] **Step 2: Inline-CSS im `<style>`-Block erweitern**

Füge nach den bestehenden Typography-Klassen ein:

```css
/* Font-Weight Utilities */
.font-medium   { font-weight: 500; }
.font-semibold { font-weight: 600; }
/* Color Utilities */
.t-success { color: var(--success, #22c55e); }
.t-danger  { color: var(--danger,  #ef4444); }
.t-muted   { color: var(--muted,   #888); }
.t-subtle  { color: var(--subtle,  #555); }
.t-white   { color: #fff; }
.t-tiny    { font-size: 0.75rem; }
```

- [ ] **Step 3: Demo-Sektionen am Ende des `<body>` (vor `</body>`) einfügen**

```html
<!-- FONT-WEIGHT -->
<div class="section">
  <div class="section-label">.font-medium / .font-semibold</div>
  <div class="section-desc">Schriftgewicht-Utilities. Setzen nur <code>font-weight</code>, ohne Größe oder Farbe zu überschreiben.</div>
  <div class="demo-box" style="flex-direction:column; gap:8px;">
    <div class="font-medium"  style="font-size:0.9rem; color:var(--text);">font-weight: 500 (.font-medium) — Der braune Fuchs springt.</div>
    <div class="font-semibold" style="font-size:0.9rem; color:var(--text);">font-weight: 600 (.font-semibold) — Der braune Fuchs springt.</div>
  </div>
</div>

<!-- TEXT-COLOR UTILITIES -->
<div class="section">
  <div class="section-label">.t-success / .t-danger / .t-muted / .t-subtle / .t-white / .t-tiny</div>
  <div class="section-desc">Farb-Utilities basierend auf CI-Tokens. <code>.t-tiny</code> setzt zusätzlich <code>font-size: 0.75rem</code>.</div>
  <div class="demo-box" style="flex-direction:column; gap:6px;">
    <span class="t-success">t-success — var(--success)</span>
    <span class="t-danger">t-danger — var(--danger)</span>
    <span class="t-muted">t-muted — var(--muted)</span>
    <span class="t-subtle">t-subtle — var(--subtle)</span>
    <span class="t-white">t-white — var(--white) / #fff</span>
    <span class="t-tiny t-muted">t-tiny — 0.75rem, hier kombiniert mit .t-muted</span>
  </div>
</div>
```

- [ ] **Step 4: Im Browser prüfen**

```
file:///root/git/oe5ith-ci/components/typography.html
```

Farben müssen sichtbar von einander unterscheidbar sein; `.t-success` grün, `.t-danger` rot.

- [ ] **Step 5: Commit**

```bash
git add components/typography.html
git commit -m "docs(typography): add demos for font-weight and color utilities"
```

---

## Task 8: components/sidebar.html — acc-dot & Loading/Error-Demos

**Files:**
- Modify: `components/sidebar.html`

- [ ] **Step 1: Lies `components/sidebar.html` um die bestehende `.acc-dot`-Demo zu finden**

Suche nach `acc-dot` im HTML. Dort gibt es vermutlich bereits eine Demo des Accordion-Headers.

- [ ] **Step 2: Inline-CSS im `<style>`-Block anpassen/ergänzen**

Suche die `.acc-dot`-Regel in der `<style>`-Sektion und füge `background: var(--accent, #3b82f6)` hinzu (falls noch kein Background gesetzt):

```css
/* Falls bestehende acc-dot-Regel keinen background hat, ergänzen: */
.acc-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; background: var(--accent, #3b82f6); }

/* Loading/Error States */
.acc-item.loading-state {
  padding-left: 24px;
  color: var(--subtle, #555);
  font-size: 0.8rem;
}
.acc-item.error-state {
  padding-left: 24px;
  color: var(--danger, #ef4444);
  font-size: 0.8rem;
}
```

- [ ] **Step 3: Demo-Sektion für Loading/Error-States am Ende des `<body>` (vor `</body>`) einfügen**

```html
<!-- ACC-ITEM STATES -->
<div class="section">
  <div class="section-label">.acc-item.loading-state / .acc-item.error-state</div>
  <div class="section-desc">Zustände für asynchron geladene Layer-Listen. Werden in den Accordion-Body eingesetzt, bis Daten verfügbar sind oder ein Fehler auftritt.</div>
  <div class="demo-box" style="flex-direction:column; gap:0; padding:0; background:var(--panel); border-radius:6px; overflow:hidden;">
    <div class="acc-item loading-state">Lade Layer-Daten …</div>
    <div class="acc-item error-state">Fehler: Layer konnte nicht geladen werden</div>
  </div>
</div>
```

- [ ] **Step 4: Im Browser prüfen**

```
file:///root/git/oe5ith-ci/components/sidebar.html
```

`loading-state` muss in `var(--subtle)` (grau), `error-state` in `var(--danger)` (rot) erscheinen.

- [ ] **Step 5: Commit**

```bash
git add components/sidebar.html
git commit -m "docs(sidebar): add demos for acc-dot default color and loading/error states"
```

---

## Task 9: components/cards.html — sprite-preview-img Demo

**Files:**
- Modify: `components/cards.html`

- [ ] **Step 1: Lies `components/cards.html` um Struktur und bestehende `<style>`-Sektion zu verstehen**

- [ ] **Step 2: Inline-CSS im `<style>`-Block ergänzen**

```css
.sprite-preview-img {
  width: 20px;
  height: 20px;
  padding: 2px;
  border-radius: 4px; /* Fallback falls --badge-radius nicht definiert */
  background: var(--bg, #1a1a1a);
  object-fit: contain;
}
```

- [ ] **Step 3: Demo-Sektion am Ende des `<body>` (vor `</body>`) einfügen**

```html
<!-- SPRITE PREVIEW -->
<div class="section">
  <div class="section-label">.sprite-preview-img</div>
  <div class="section-desc">Quadratische Icon-/Bildvorschau (20×20px) innerhalb von Cards. Verwendet <code>object-fit: contain</code> und einen abgedunkelten Hintergrund.</div>
  <div class="demo-box" style="align-items:center; gap:12px;">
    <img class="sprite-preview-img"
         src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='10' fill='%233b82f6'/%3E%3C/svg%3E"
         alt="Demo Icon">
    <span style="font-size:0.8rem; color:var(--muted);">Sprite oder Icon-Asset</span>
    <img class="sprite-preview-img"
         src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='4' y='4' width='16' height='16' rx='3' fill='%2322c55e'/%3E%3C/svg%3E"
         alt="Demo Icon 2">
    <span style="font-size:0.8rem; color:var(--muted);">Weiteres Asset</span>
  </div>
</div>
```

- [ ] **Step 4: Im Browser prüfen**

```
file:///root/git/oe5ith-ci/components/cards.html
```

Beide SVG-Icons sollen als 20×20px-Vorschau mit Dunkel-Hintergrund erscheinen.

- [ ] **Step 5: Commit**

```bash
git add components/cards.html
git commit -m "docs(cards): add sprite-preview-img demo"
```

---

## Task 10: CHANGELOG aktualisieren

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: In `CHANGELOG.md` unter `## [Unreleased]` → `### Added` einfügen**

Füge nach dem bestehenden Tracking-Liste-Eintrag hinzu:

```markdown
- **utils.css** — Text/Visibility: `.text-center`, `.text-left`, `.opacity-50`, `.hidden`
- **utils.css** — Flex: `.flex-1`, `.flex-2`, `.w-full`, `.flex-align-center`, `.justify-between`, `.gap-4`
- **utils.css** — Table: `.table-wrapper`, `.table-col-25`, `.border-collapse`
- **utils.css** — Spacing: `.m-0`, `.mt-0`, `.mt-8`, `.mt-12`, `.mb-8`, `.pb-0`, `.p-double-gap`, `.mb-1-5-gap`, `.p-2rem`
- **utils.css** — Misc: `.pos-relative`, `.cursor-pointer`, `.border-none`, `.no-dot-bg`
- **typography.css** — Font-Weights: `.font-medium`, `.font-semibold`
- **typography.css** — Farb-Utilities: `.t-success`, `.t-danger`, `.t-muted`, `.t-subtle`, `.t-white`, `.t-tiny`
- **sidebar.css** — `.acc-item.loading-state`, `.acc-item.error-state` für asynchrone Layer-Zustände
- **cards.css** — `.sprite-preview-img` für Icon-/Asset-Vorschauen in Cards
- **coords.css** — `.coord-header-status` für Zusatz-Text im Koordinaten-Block-Header
- **sidebar.css** — `.acc-dot` erhält `background: var(--accent)` als CI-Default (site-spezifische Overrides möglich)
- Referenz-Demos in `components/utils.html`, `components/typography.html`, `components/sidebar.html`, `components/cards.html` aktualisiert
```

- [ ] **Step 2: Prüfen dass der CHANGELOG-Eintrag korrekt formatiert ist**

```bash
grep -c "utils.css\|typography.css\|sidebar.css\|cards.css\|coords.css" CHANGELOG.md
```

Erwartete Ausgabe: mindestens `5`

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): document all missing utility class additions"
```

---

## Self-Review

**Spec-Coverage:**
- ✅ `.text-center`, `.text-left`, `.opacity-50`, `.hidden` → Task 1
- ✅ `.flex-1`, `.flex-2`, `.w-full`, `.flex-align-center`, `.flex-col` (bereits vorhanden), `.justify-between`, `.gap-4` → Task 1
- ✅ `.table-wrapper`, `.table-col-25`, `.border-collapse` → Task 1
- ✅ `.m-0`, `.mt-0`, `.mt-8`, `.mt-12`, `.mb-8`, `.pb-0`, `.p-double-gap`, `.mb-1-5-gap`, `.p-2rem` → Task 1
- ✅ `.border-none`, `.pos-relative`, `.cursor-pointer`, `.no-dot-bg` → Task 1
- ✅ `.font-medium`, `.font-semibold` → Task 2
- ✅ `.t-success`, `.t-danger`, `.t-muted`, `.t-subtle`, `.t-white`, `.t-tiny` → Task 2
- ✅ `.acc-dot` background-Default → Task 3
- ✅ `.acc-item.loading-state`, `.acc-item.error-state` → Task 3
- ✅ `.sprite-preview-img` → Task 4
- ✅ `.coord-header-status` → Task 5
- ✅ Alle Component-Referenz-HTMLs → Tasks 6–9
- ✅ CHANGELOG → Task 10

**Offene Hinweise:**
- `.p-2rem` (32px) und `.p-double-gap` (40px bei `--card-gap: 20px`) überschneiden sich konzeptuell; beide sind trotzdem eingebunden da sie aus unterschiedlichen Kontexten stammen.
- Pixel-basierte Spacings (`.mt-8`, `.mt-12` etc.) sind nicht token-basiert — bewusste Entscheidung lt. Spec, da kein passender Token existiert.
- `.flex-col` existiert bereits in `utils.css:34` — **nicht erneut hinzufügen**.

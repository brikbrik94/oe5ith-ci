# Website-v3 CI-Anfragen (Badge-Wrap, Map-BG-Token, Coord-Row-WGS, Map-Legend-Icon) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the four open CI requests/bugs reported from `website-v3` (`/root/git/website-v3/docs/ci/`): the `.badge` no-wrap bug, the missing `--map-bg` token + `.full-map` background + `.coord-row-wgs`/`.coord-vals` classes, and the new `.map-legend-icon` swatch type — then release them as one bundled MINOR version.

**Architecture:** Each task is a small, independent, additive extension to an existing CI component (no new components, no registry.json changes, no breaking changes). Every task follows the repo's established Dreiklang for extensions: CSS change → reference HTML update → doc update → CHANGELOG entry. The final task bundles all four `[Unreleased]` CHANGELOG entries into one MINOR release (`v1.21.0`), matching the precedent set by `v1.18.0` (three unrelated additive changes released together).

**Tech Stack:** Plain CSS (custom properties / tokens), static HTML reference pages, Markdown docs. No build step. `python3 scripts/cli/check_consistency.py` is the only automated check (registry.json ↔ disk consistency); `python3 -m pytest scripts/cli/test_check_consistency.py` covers that script itself and is unaffected by this work (no registry.json changes needed — every file touched here already has an owning entry).

## Global Constraints

- Never hardcode colors, radii, shadows, z-index, or transitions — use tokens from `css/common.css`.
- No new component classes beyond what each request specifies — reuse existing patterns (`.badge`, `.map-legend-entry`, `.coord-input-dms`, etc.).
- `css/demo.css` only in `components/*.html`, never implied to be needed in production files touched here.
- Do not change any existing token value, existing class behavior, or existing HTML structure — every change in this plan is purely additive (new modifier class, new token, new classes, new enum value). This keeps every change at MINOR, not MAJOR.
- Update `docs/tokens.md` for the new token, and the relevant component doc (`docs/badges.md`, `docs/sidebar-types.md`, `docs/map-legend.md`) for each new class/variant.
- `CHANGELOG.md` entries use the exact header format `## vX.Y.Z - YYYY-MM-DD` (or `## [Unreleased]` until tagged), with `### Added` / `### Changed` / `### Fixed` blocks — see `docs/versioning.md`.
- No file paths change. No registry.json edits needed (all touched files already have an owning entry in `docs/registry.json`).
- Run `python3 scripts/cli/check_consistency.py` after every task — must stay at "Manifest und Dateien sind konsistent" (the two pre-existing warnings for `coords`/`utils` having no dedicated doc entry are expected and unrelated to this work — do not try to fix them).

---

## File Structure

| File | Task | Change |
|---|---|---|
| `css/badges.css` | 1 | Add `.badge-wrap` modifier |
| `docs/badges.md` | 1 | Document `.badge-wrap` |
| `components/badges.html` | 1 | Add wrap demo section |
| `css/common.css` | 2 | Add `--map-bg` token |
| `css/utils.css` | 2 | `.full-map` gets `background: var(--map-bg)` |
| `docs/tokens.md` | 2 | Document `--map-bg` |
| `components/utils.html` | 2 | Update `.full-map` description |
| `css/coords.css` | 3 | Add `.coord-row-wgs` / `.coord-vals` |
| `docs/sidebar-types.md` | 3 | Document new coords classes |
| `components/sidebar-types.html` | 3 | Add demo row |
| `css/modal.css` | 4 | Add `.map-legend-icon` |
| `docs/map-legend.md` | 4 | Document `icon` entry type |
| `components/modal.html` | 4 | Extend `MapLegend.addEntry`, add demo entry |
| `CHANGELOG.md` | 1–5 | `[Unreleased]` entries per task, finalized to `v1.21.0` in Task 5 |

---

### Task 1: Badge `.badge-wrap` modifier

Fixes `bug-reports.md` #2 / `open-items.md` #4 (`css/badges.css:36` — `.badge` hardcodes `white-space: nowrap`, single long-text badges get clipped instead of wrapping). Per the bug report's own recommendation: keep `nowrap` as the default (short status badges like "Online"/"v1.4.2" must never wrap), and add an opt-in modifier for badges with long/variable text (warnings, free text) instead of changing the shared default.

**Files:**
- Modify: `css/badges.css`
- Modify: `docs/badges.md`
- Modify: `components/badges.html`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: `.badge-wrap` — combinable modifier class, used as `<span class="badge badge-yellow badge-wrap">…</span>`. No new tokens.

- [ ] **Step 1: Add the CSS rule**

In `css/badges.css`, insert directly after the `.badge i { … }` block (after line 53, before the `BADGE FARBEN` section comment):

```css
/* ── Wrap-Modifier — für Badges mit langem/variablem Text (Warnungen, Freitext) ── */
.badge-wrap {
  white-space: normal;
  overflow-wrap: break-word;
}
```

- [ ] **Step 2: Verify structurally**

Run:
```bash
grep -n "badge-wrap" css/badges.css
```
Expected: shows the new `.badge-wrap` rule with `white-space: normal;` and `overflow-wrap: break-word;`.

- [ ] **Step 3: Document in `docs/badges.md`**

Insert a new section after the existing "## Inhalt — Dot, Icon oder Text" section (after its closing `---` and the "### Nur Text" content, i.e. right before "## Verwendungsregeln"):

```markdown
## Zeilenumbruch

Default ist `white-space: nowrap` — kurze Status-Badges ("Online", "v1.4.2") sollen nie umbrechen.
Für Badges mit langem oder variablem Text (Warnungen, Freitext-Meldungen in schmalen Containern)
das Modifier `.badge-wrap` ergänzen:

```html
<span class="badge badge-yellow badge-wrap">
  Zufahrtsbeschränkungen auf der Strecke
</span>
```

```css
.badge-wrap {
  white-space: normal;
  overflow-wrap: break-word;
}
```

Kombinierbar mit jeder Farbvariante. Nicht nötig für `.badge-gray`-Typlabels oder kurze
Status-Badges — dort bleibt der `nowrap`-Default aktiv.

---

```

Then append a row to the "Änderungshistorie" table at the bottom of the file:

```markdown
| 2026-07-18 | `.badge-wrap` Modifier ergänzt — erlaubt internen Zeilenumbruch für Badges mit langem/variablem Text, ohne den `nowrap`-Default für kurze Status-Badges zu ändern. |
```

- [ ] **Step 4: Add reference demo in `components/badges.html`**

Insert a new `demo-section` after the "NUR TEXT" section (after its closing `</div>` around line 121, before the "KONTEXT: IN CARD" section):

```html
  <!-- ═══ WRAP-MODIFIER ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Zeilenumbruch — <code>.badge-wrap</code></div>
    <div class="demo-section-desc">
      Default bleibt <code>nowrap</code>. Für Badges mit langem/variablem Text (Warnungen,
      Freitext) das Modifier <code>.badge-wrap</code> ergänzen, damit der Text intern umbricht
      statt abgeschnitten zu werden.
    </div>
    <div class="row" style="max-width:180px; align-items:flex-start;">
      <span class="badge badge-yellow badge-wrap">Zufahrtsbeschränkungen auf der Strecke</span>
    </div>
  </div>

```

- [ ] **Step 5: Visual check**

Open `components/badges.html` in a browser (e.g. `python3 -m http.server` from repo root, then visit `/components/badges.html`). Confirm: the new "Zeilenumbruch" section shows the yellow warning badge wrapping onto multiple lines inside the 180px-wide row, not clipped or overflowing.

- [ ] **Step 6: Add CHANGELOG entry**

`CHANGELOG.md` currently has no `## [Unreleased]` section (top of file jumps straight to `## v1.20.0`). Insert a new section at the very top, after the header comment block (after line 5, before `## v1.20.0`):

```markdown
## [Unreleased]

### Added
- `badges.css`: `.badge-wrap` Modifier-Klasse — erlaubt internen Zeilenumbruch für Badges mit
  langem/variablem Text (z.B. Warnungen in schmalen Sidebars), ohne das `nowrap`-Standardverhalten
  für kurze Status-Badges zu ändern. Behebt Meldung aus `website-v3` (Routing-Sidebar-Warn-Badges).

---

```

- [ ] **Step 7: Run consistency check**

Run: `python3 scripts/cli/check_consistency.py`
Expected: `✔ Manifest und Dateien sind konsistent` (plus the two pre-existing unrelated warnings).

- [ ] **Step 8: Commit**

```bash
git add css/badges.css docs/badges.md components/badges.html CHANGELOG.md
git commit -m "feat(badges): add .badge-wrap modifier for long/variable-text badges"
```

---

### Task 2: `--map-bg` token + `.full-map` background

Implements `handoff-2026-06-20-map-bg-wgs84.md` items 1–2. Pure addition: new token, one new line on an existing rule.

**Files:**
- Modify: `css/common.css`
- Modify: `css/utils.css`
- Modify: `docs/tokens.md`
- Modify: `components/utils.html`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: `--map-bg` token (default `#ffffff`), consumed by `.full-map`.

- [ ] **Step 1: Add the token**

In `css/common.css`, insert directly after line 22 (`--border-strong:    #444444;`) and before line 23 (`--surface-hover:`):

```css
  --map-bg:           #ffffff; /* Hintergrund des Karten-Containers (weiß als Default, per Stylesheet überschreibbar) */
```

- [ ] **Step 2: Wire it into `.full-map`**

In `css/utils.css`, the `.full-map` rule (lines 16–21) becomes:

```css
.full-map {
  flex: 1;
  height: 100%;
  min-height: 0;
  position: relative;
  background: var(--map-bg);
}
```

- [ ] **Step 3: Verify structurally**

Run:
```bash
grep -n "map-bg" css/common.css css/utils.css
```
Expected: `common.css` shows the token definition, `utils.css` shows `background: var(--map-bg);` inside `.full-map`.

- [ ] **Step 4: Document the token in `docs/tokens.md`**

Add a row to the "## Basis-Farben" table (after the `--surface-hover` row):

```markdown
| `--map-bg` | `#ffffff` | Hintergrund des Karten-Containers (`.full-map`), per Stylesheet überschreibbar |
```

Also add the same line to the "Vollständige common.css" code block in that file, in the Basis section right after `--surface-hover:      rgba(255,255,255,0.05);`:

```css
  --map-bg:           #ffffff;
```

- [ ] **Step 5: Update `components/utils.html` description**

In the `.full-map` section (around line 32), update the `section-desc` to mention the new background:

```html
  <div class="section-desc">Vollflächiger Container für MapLibre / Leaflet. <code>flex:1 · height:100% · min-height:0 · position:relative · background:var(--map-bg)</code>. Verhindert Layout-Sprünge beim Initialisieren der Karte in einem Flex-Parent. Der Hintergrund ist per <code>--map-bg</code>-Token überschreibbar (Default: weiß).</div>
```

(The demo box below it keeps its inline `style="background:#2d3a2d;…"` override for visibility against the dark reference-page background — that override intentionally wins over the token for this specific demo and needs no change.)

- [ ] **Step 6: Visual check**

Open `components/utils.html` in a browser. Confirm the `.full-map` section still renders identically (dark green demo box, unchanged) — the token addition must not visibly change this reference page, since the demo already overrides the background inline.

- [ ] **Step 7: Add CHANGELOG entry**

Append to the existing `## [Unreleased]` → `### Added` block created in Task 1 (add a new bullet under the same `### Added` heading):

```markdown
- `common.css`: neuer Token `--map-bg` (Default `#ffffff`) für den Karten-Container-Hintergrund;
  `utils.css`: `.full-map` nutzt `background: var(--map-bg)`. Übernahme aus `website-v3`
  (Koordinaten-Umrechner-Karte), vorher nur als lokaler App-Override vorhanden.
```

- [ ] **Step 8: Run consistency check**

Run: `python3 scripts/cli/check_consistency.py`
Expected: `✔ Manifest und Dateien sind konsistent`.

- [ ] **Step 9: Commit**

```bash
git add css/common.css css/utils.css docs/tokens.md components/utils.html CHANGELOG.md
git commit -m "feat(tokens): add --map-bg token, wire into .full-map"
```

---

### Task 3: `.coord-row-wgs` / `.coord-vals` — unified-width WGS84 coordinate row

Implements `handoff-2026-06-20-map-bg-wgs84.md` item 3. Builds on the existing `.coord-input-dms` class (already used by `.coord-row-dms`). Purely additive — existing `.coord-row`/`.coord-row-dms`/`.coord-row-inline` usages are untouched.

**Files:**
- Modify: `css/coords.css`
- Modify: `docs/sidebar-types.md`
- Modify: `components/sidebar-types.html`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: existing `.coord-input-dms` (defined in `css/coords.css`, `COORD-ROW-DMS` section).
- Produces: `.coord-row-wgs` (row wrapper), `.coord-vals` (flexible field group, nests `.coord-input-dms` fields and overrides their fixed width to `flex:1`).

- [ ] **Step 1: Add the CSS block**

In `css/coords.css`, insert a new block directly before the `COORD-ROW-INLINE` section comment (before line 217, i.e. right after the `.coord-suffix` rule ends at line 214):

```css
/* ═══════════════════════════════════════
   COORD-ROW-WGS — Einheitliche WGS84-Zeile (Label + n Felder + Suffix)
   Gleiche Gesamtbreite über DD / DDM / DMS hinweg; Felder teilen sich
   den verfügbaren Platz, das Suffix sitzt immer am selben Anschlag.
   ═══════════════════════════════════════ */
.coord-row-wgs {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}
.coord-row-wgs:last-child { margin-bottom: 0; }

.coord-vals {
  flex: 1;
  display: flex;
  gap: 4px;
  min-width: 0;
}
.coord-vals .coord-input-dms {
  width: auto;
  flex: 1;
  min-width: 0;
  text-align: left;
}

```

- [ ] **Step 2: Verify structurally**

Run:
```bash
grep -n "coord-row-wgs\|coord-vals" css/coords.css
```
Expected: shows both new rules, placed before the `COORD-ROW-INLINE` comment block.

- [ ] **Step 3: Document in `docs/sidebar-types.md`**

In the "Typ 7 — Koordinaten-Umrechner" section, "Elemente" bullet list (around line 310–318), add a new bullet after the `.coord-row-inline` line:

```markdown
- `.coord-row-wgs` + `.coord-vals`: einheitliche Zeilenbreite über DD/DDM/DMS hinweg — beliebig
  viele `.coord-input-dms`-Felder in `.coord-vals` teilen sich den Platz, das Suffix sitzt immer
  am selben rechten Anschlag (statt fester 52px-Feldbreite wie in `.coord-row-dms`)
```

- [ ] **Step 4: Add reference demo in `components/sidebar-types.html`**

In the Typ 7 section, directly after the closing `</div>` of the "WGS84 Dezimalgrad — aktiv" block and before the `<div class="tool-sep"></div>` that precedes "WGS84 DMS" (around line 520–522), add a labelled example showing the new pattern applied to a DMS-style row with 3 fields:

```html
          <!-- .coord-row-wgs Referenz: einheitliche Breite, unabhängig von Feldanzahl -->
          <div class="coord-row-wgs">
            <span class="coord-label">Lat.</span>
            <div class="coord-vals">
              <input class="coord-input-dms" type="text" inputmode="numeric" value="48" readonly>
              <input class="coord-input-dms" type="text" inputmode="numeric" value="23" readonly>
              <input class="coord-input-dms" type="text" inputmode="decimal" value="15.4" readonly>
            </div>
            <span class="coord-suffix">N</span>
          </div>
```

- [ ] **Step 5: Visual check**

Open `components/sidebar-types.html` in a browser, scroll to Typ 7. Confirm the new `.coord-row-wgs` example row renders with the label on the left, three fields sharing the available width evenly, and the "N" suffix flush right — same right-edge alignment as the "WGS84 DMS" block below it despite the different markup.

- [ ] **Step 6: Add CHANGELOG entry**

Append to the `## [Unreleased]` → `### Added` block:

```markdown
- `coords.css`: neue Klassen `.coord-row-wgs` / `.coord-vals` — einheitliche Gesamtbreite für
  WGS84-Koordinatenzeilen unabhängig von der Feldanzahl (DD/DDM/DMS), baut auf `.coord-input-dms`
  auf. Übernahme aus `website-v3` (Koordinaten-Umrechner), vorher nur lokal in der App vorhanden.
```

- [ ] **Step 7: Run consistency check**

Run: `python3 scripts/cli/check_consistency.py`
Expected: `✔ Manifest und Dateien sind konsistent`.

- [ ] **Step 8: Commit**

```bash
git add css/coords.css docs/sidebar-types.md components/sidebar-types.html CHANGELOG.md
git commit -m "feat(coords): add .coord-row-wgs / .coord-vals for unified WGS84 row width"
```

---

### Task 4: `.map-legend-icon` — icon swatch type for `MapLegend`

Implements `legend-icon-swatch-request.md` in full (Sections 2–5). Adds a fourth, generic entry type (`icon`) to the existing `dot`/`line`/`area` swatch types — no domain-specific (helicopter/NAH) styling in the CI component itself, per the request's explicit constraint.

**Files:**
- Modify: `css/modal.css`
- Modify: `docs/map-legend.md`
- Modify: `components/modal.html`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: `.map-legend-icon` CSS class; `MapLegend.addEntry({ type: 'icon', icon, color, label })` — `icon` is a consumer-supplied Font Awesome class string (e.g. `'fa-solid fa-helicopter'`), required only when `type === 'icon'`.

- [ ] **Step 1: Add the CSS rule**

In `css/modal.css`, insert directly after the `.map-legend-area` rule (after line 547, before the `.map-legend-label` rule):

```css
.map-legend-icon {
  width: 12px;
  height: 12px;
  font-size: 12px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
```

- [ ] **Step 2: Verify structurally**

Run:
```bash
grep -n "map-legend-icon" css/modal.css
```
Expected: shows the new rule between `.map-legend-area` and `.map-legend-label`.

- [ ] **Step 3: Extend `MapLegend.addEntry` in `components/modal.html`**

Replace the current `addEntry` method (lines 246–263) with:

```js
  addEntry({ type, color, label, icon }) {
    const typeClass = { dot: 'map-legend-dot', line: 'map-legend-line', area: 'map-legend-area', icon: 'map-legend-icon' }[type];
    if (!typeClass) throw new Error(`MapLegend.addEntry: unknown type "${type}"`);
    const entry = document.createElement('div');
    entry.className = 'map-legend-entry';

    const indicator = document.createElement(type === 'icon' ? 'i' : 'div');
    indicator.className = type === 'icon' ? `${icon} ${typeClass}` : typeClass;
    if (type === 'icon') {
      indicator.style.color = color;
    } else {
      indicator.style.background = color;
    }

    const labelEl = document.createElement('span');
    labelEl.className = 'map-legend-label';
    labelEl.textContent = label;

    entry.appendChild(indicator);
    entry.appendChild(labelEl);
    this._entriesEl.appendChild(entry);
  }
```

- [ ] **Step 4: Add a static markup example**

In the "Statisches Markup-Beispiel" block (around lines 180–198), add a fourth entry after the `.map-legend-area` one, before the closing `</div>` of `.map-legend-entries` (around line 195):

```html
          <div class="map-legend-entry">
            <i class="fa-solid fa-helicopter map-legend-icon" style="color:var(--success);"></i>
            <span class="map-legend-label">Aktiv</span>
          </div>
```

- [ ] **Step 5: Add a live demo entry**

In `demoLegendReset()` (around line 293–302), add one `icon`-type entry:

```js
function demoLegendReset() {
  demoLegend.clearEntries();
  demoLegend.setTitle('Kartenschlüssel');
  demoLegend.addEntry({ type: 'dot',  color: '#22c55e', label: 'Feuerwehr aktiv' });
  demoLegend.addEntry({ type: 'dot',  color: '#ef4444', label: 'Feuerwehr inaktiv' });
  demoLegend.addEntry({ type: 'line', color: '#3b82f6', label: 'Anfahrtsroute' });
  demoLegend.addEntry({ type: 'area', color: '#f59e0b', label: 'Sperrzone' });
  demoLegend.addEntry({ type: 'area', color: '#8b5cf6', label: 'Einsatzgebiet' });
  demoLegend.addEntry({ type: 'icon', icon: 'fa-solid fa-helicopter', color: '#22c55e', label: 'Luftrettung aktiv' });
  demoLegend.show();
}
```

- [ ] **Step 6: Visual check**

Open `components/modal.html` in a browser, scroll to the "Karten-Legende" demo section. Confirm: the live legend panel shows a green helicopter glyph next to "Luftrettung aktiv" alongside the existing dot/line/area entries, same row height/alignment as the others; the static markup example below it also shows the helicopter icon entry. Toggle the legend open/closed via the demo button to confirm no layout break.

- [ ] **Step 7: Document in `docs/map-legend.md`**

Update the "## Eintragstypen" table (around line 40–46) to add a row:

```markdown
| `icon` | FontAwesome-Glyph 12×12px | Symbol-Marker mit Formsemantik (z.B. Fahrzeuge, Stationen) |
```

Update the JS-API example (around line 24–30) to add:

```js
legend.addEntry({ type: 'icon', icon: 'fa-solid fa-helicopter', color: '#22c55e', label: 'Aktiv' });
```

Update the TypeScript interface (around line 70–75):

```ts
interface LegendEntry {
  type: 'dot' | 'line' | 'area' | 'icon';
  color: string;
  label: string;
  icon?: string; // FontAwesome-Klassen, nur bei type: 'icon' relevant, z.B. 'fa-solid fa-helicopter'
}
```

And the "`color` akzeptiert…" line (around line 48) gets a follow-up sentence:

```markdown
Bei `type: 'icon'` wird `color` als `style.color` (statt `style.background`) auf das Glyph
angewendet; `icon` ist dann erforderlich und enthält die vollständigen FontAwesome-Klassen
(z.B. `'fa-solid fa-helicopter'`).
```

- [ ] **Step 8: Add CHANGELOG entry**

Append to the `## [Unreleased]` → `### Added` block:

```markdown
- `modal.css` / `MapLegend`: neuer Eintragstyp `icon` (`.map-legend-icon`, 12×12px) für
  Legenden-Einträge mit Formsemantik (z.B. Fahrzeug-/Stations-Icons statt reiner Farbfläche).
  Additiv — bestehende `dot`/`line`/`area`-Konsumenten bleiben unverändert funktionsfähig.
  Angefragt aus `website-v3` (NAH-Luftrettungs-Legende).
```

- [ ] **Step 9: Run consistency check**

Run: `python3 scripts/cli/check_consistency.py`
Expected: `✔ Manifest und Dateien sind konsistent`.

- [ ] **Step 10: Commit**

```bash
git add css/modal.css docs/map-legend.md components/modal.html CHANGELOG.md
git commit -m "feat(map-legend): add icon entry type (.map-legend-icon)"
```

---

### Task 5: Release v1.21.0

Bundles all four additive changes from Tasks 1–4 into a single MINOR release, following the mandatory release flow in `docs/versioning.md` and the precedent of `v1.18.0` (multiple unrelated additive changes released together).

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the `## [Unreleased]` section built up across Tasks 1–4 (one `### Added` block with 4 bullets).

- [ ] **Step 1: Rename `[Unreleased]` to the release header**

In `CHANGELOG.md`, change:
```markdown
## [Unreleased]
```
to:
```markdown
## v1.21.0 - 2026-07-18
```
(keep the `### Added` block and its 4 bullets unchanged underneath).

- [ ] **Step 2: Add a fresh empty `[Unreleased]` section above it**

Insert directly above the new `## v1.21.0 - 2026-07-18` header:

```markdown
## [Unreleased]

---

```

- [ ] **Step 3: Run full consistency check**

Run: `python3 scripts/cli/check_consistency.py && python3 -m pytest scripts/cli/test_check_consistency.py -q`
Expected: both pass — `✔ Manifest und Dateien sind konsistent` and `10 passed`.

- [ ] **Step 4: Commit the release**

```bash
git add CHANGELOG.md
git commit -m "chore: release v1.21.0"
```

- [ ] **Step 5: Tag the release**

```bash
git tag -a v1.21.0 -m "Release v1.21.0"
```

- [ ] **Step 6: Push — ASK THE USER FIRST**

Pushing to `origin/main` and pushing a tag are both externally visible, hard-to-reverse actions. Confirm with the user before running:

```bash
git push origin main
git push origin v1.21.0
```

---

## Self-Review Notes

- **Spec coverage:** `bug-reports.md` #2 → Task 1. `handoff-2026-06-20-map-bg-wgs84.md` items 1–3 → Task 2 (items 1–2) and Task 3 (item 3). `legend-icon-swatch-request.md` Sections 2–5 → Task 4 (all acceptance-checklist items in Section 5 are covered: CSS box sizing, inline-style color, freely-chosen icon class, `components/modal.html` example, `docs/map-legend.md` + `CHANGELOG.md` updates, existing consumers unaffected). `routing-disclosure-request.md` and the modal-backdrop bug are already shipped (v1.19.0 / v1.18.1) — no task needed. `open-items.md` will need a manual update (mark item 4 as done) once this plan lands — not part of this repo, lives in `website-v3/docs/ci/`, out of scope here.
- **No registry.json changes:** confirmed every touched file already has an owning `docs/registry.json` entry (`badges`, `tokens`, `utils`, `coords`/`sidebar`, `modal`, `map-legend`) — `check_consistency.py` will not flag orphans.
- **Versioning check:** all four changes are additive (new modifier class, new token, new classes, new enum value) — correctly classified as MINOR per `docs/versioning.md`, bundled into one `v1.21.0` release rather than 4 separate tags, matching the `v1.18.0` precedent.

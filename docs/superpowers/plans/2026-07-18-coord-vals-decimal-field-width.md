# Coord-Vals Decimal Field Width Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the CI request from `website-v3` (`/root/git/website-v3/docs/ci/coord-vals-decimal-field-width-request.md`): inside a `.coord-vals` row, non-decimal fields (degrees, integer minutes) get a fixed narrow width instead of sharing the row equally with the decimal field, so the decimal field (which needs the most characters) gets the remaining space.

**Architecture:** Single additive CSS rule scoped by the `[inputmode="decimal"]` attribute that `Wgs84Block.ts` (website-v3) already sets on the decimal field of each row — no new class, no markup change, no consumer change. The existing `.coord-vals .coord-input-dms` rule (`flex: 1`) keeps working for the decimal field; the new `:not([inputmode="decimal"])` variant overrides `flex`/`width` for the other fields in the same row. Released as a PATCH (v1.21.1) — this refines the width behavior of the `.coord-vals`/`.coord-row-wgs` pair already shipped in v1.21.0, it does not add a new public class or token.

**Tech Stack:** Plain CSS (no tokens needed — `.coord-input-dms` itself already hardcodes `width: 52px` as a literal, so a literal `36px` here matches existing convention in this file), static HTML reference page, Markdown docs. No build step. `python3 scripts/cli/check_consistency.py` is the only automated check; no registry.json changes needed (`coords`/`sidebar-types` already have owning entries).

## Global Constraints

- Never hardcode colors, radii, shadows, z-index, or transitions — use tokens from `css/common.css`. (Field width in px is not in this list and already appears as a literal elsewhere in `coords.css` — no token needed here.)
- Purely additive: do not change the existing `.coord-vals .coord-input-dms` rule (the decimal field keeps `flex: 1`), do not change `Wgs84Block.ts` or any other consumer.
- No new CSS class introduced — the change is a new attribute-scoped selector on top of the existing `.coord-input-dms` class.
- `CHANGELOG.md` entries use the exact header format `## vX.Y.Z - YYYY-MM-DD` (or `## [Unreleased]` until tagged), with `### Added` / `### Changed` / `### Fixed` blocks.
- No file paths change. No `docs/registry.json` edits needed.
- Run `python3 scripts/cli/check_consistency.py` after the CSS/docs task — must report `✔ Manifest und Dateien sind konsistent`.

---

## File Structure

| File | Task | Change |
|---|---|---|
| `css/coords.css` | 1 | Add `.coord-vals .coord-input-dms:not([inputmode="decimal"])` rule |
| `docs/sidebar-types.md` | 1 | Extend the existing `.coord-row-wgs` / `.coord-vals` bullet in Typ 7 |
| `components/sidebar-types.html` | 1 | Update the existing reference comment to call out the width difference |
| `CHANGELOG.md` | 1–2 | `[Unreleased]` → `### Fixed` entry, finalized to `v1.21.1` in Task 2 |

---

### Task 1: `.coord-vals` non-decimal fields get a fixed narrow width

Fixes `website-v3/docs/ci/coord-vals-decimal-field-width-request.md` (`open-items.md` item 6). The row `<div class="coord-row-wgs">` at `components/sidebar-types.html:523-531` already sets `inputmode="numeric"` on the degree/minutes fields and `inputmode="decimal"` on the last field (seconds) — this is the exact hook the new rule needs, no HTML restructuring required.

**Files:**
- Modify: `css/coords.css:229-240`
- Modify: `docs/sidebar-types.md:316-318`
- Modify: `components/sidebar-types.html:522`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: existing `.coord-vals .coord-input-dms` rule (`css/coords.css:235-240`, `flex: 1`) and the `inputmode="decimal"` attribute that `Wgs84Block.ts` (website-v3, not part of this repo) already sets on the decimal field of each row.
- Produces: `.coord-vals .coord-input-dms:not([inputmode="decimal"])` — no new class, no new token, nothing later tasks need to reference.

- [ ] **Step 1: Add the CSS rule**

In `css/coords.css`, insert directly after the existing `.coord-vals .coord-input-dms { ... }` block (currently lines 235-240, ends right before the `COORD-ROW-INLINE` section comment):

```css
.coord-vals .coord-input-dms {
  width: auto;
  flex: 1;
  min-width: 0;
  text-align: left;
}
.coord-vals .coord-input-dms:not([inputmode="decimal"]) {
  flex: 0 0 36px;
  width: 36px;
}
```

(Only the second rule is new — the first is shown for placement context, do not modify it.)

- [ ] **Step 2: Verify structurally**

Run:
```bash
grep -n "coord-vals .coord-input-dms" css/coords.css
```
Expected: two matches — the existing plain rule and the new `:not([inputmode="decimal"])` rule directly below it.

- [ ] **Step 3: Document in `docs/sidebar-types.md`**

In the "Typ 7 — Koordinaten-Umrechner" → "Elemente" list, replace the existing `.coord-row-wgs` / `.coord-vals` bullet (lines 316-318):

```markdown
- `.coord-row-wgs` + `.coord-vals`: einheitliche Zeilenbreite über DD/DDM/DMS hinweg — beliebig
  viele `.coord-input-dms`-Felder in `.coord-vals` teilen sich den Platz, das Suffix sitzt immer
  am selben rechten Anschlag (statt fester 52px-Feldbreite wie in `.coord-row-dms`)
```

with:

```markdown
- `.coord-row-wgs` + `.coord-vals`: einheitliche Zeilenbreite über DD/DDM/DMS hinweg — beliebig
  viele `.coord-input-dms`-Felder in `.coord-vals` teilen sich den Platz, das Suffix sitzt immer
  am selben rechten Anschlag (statt fester 52px-Feldbreite wie in `.coord-row-dms`). Innerhalb
  eines `.coord-vals`-Blocks bekommt genau ein Feld — das mit `inputmode="decimal"` (immer das
  letzte in der Zeile: Minuten bei DDM, Sekunden bei DMS) — den verbleibenden Platz (`flex: 1`);
  alle anderen Felder (Grad, ganzzahlige Minuten) bleiben fix bei 36px breit, unabhängig von der
  Feldanzahl in der Zeile
```

- [ ] **Step 4: Update the reference comment in `components/sidebar-types.html`**

At line 522, replace:

```html
          <!-- .coord-row-wgs Referenz: einheitliche Breite, unabhängig von Feldanzahl -->
```

with:

```html
          <!-- .coord-row-wgs Referenz: einheitliche Breite, unabhängig von Feldanzahl.
               Grad/Minuten (inputmode="numeric") bleiben fix schmal (36px), das Dezimalfeld
               (inputmode="decimal") bekommt den Rest der Zeile. -->
```

The three `<input>` elements below (lines 526-528) already carry the correct `inputmode` attributes (`numeric`, `numeric`, `decimal`) from the v1.21.0 work — no change needed there.

- [ ] **Step 5: Visual check**

Open `components/sidebar-types.html` in a browser (e.g. `python3 -m http.server` from repo root, then visit `/components/sidebar-types.html`), scroll to Typ 7. Confirm: in the `.coord-row-wgs` example row (between "WGS84 Dezimalgrad" and "WGS84 DMS"), the first two fields (`48`, `23`) are visibly narrower than the third field (`15.4`), and the "N" suffix still sits at the same right edge as in the "WGS84 DMS" block below it. Confirm the "WGS84 Dezimalgrad" block above (plain `.coord-row`, not `.coord-vals`) is visually unchanged.

- [ ] **Step 6: Add CHANGELOG entry**

`CHANGELOG.md` currently has an empty `## [Unreleased]` section at the top (before `## v1.21.0 - 2026-07-18`). Fill it in:

```markdown
## [Unreleased]

### Fixed
- `coords.css`: in `.coord-vals`-Zeilen (`.coord-row-wgs`) bekommen Nicht-Dezimal-Felder (Grad,
  ganzzahlige Minuten) jetzt eine feste, schmale Breite (36px) statt sich die Zeile gleichmäßig
  mit dem Dezimalfeld zu teilen; das Dezimalfeld (`inputmode="decimal"`, immer das letzte in der
  Zeile) bekommt dadurch den verbleibenden Platz. Additiv zur bestehenden `flex: 1`-Regel, DD-Format
  (ein Dezimalfeld pro Zeile) bleibt optisch unverändert. Angefragt aus `website-v3`
  (Koordinaten-Umrechner, `Wgs84Block.ts`).

---

```

- [ ] **Step 7: Run consistency check**

Run: `python3 scripts/cli/check_consistency.py`
Expected: `✔ Manifest und Dateien sind konsistent` (plus the two pre-existing unrelated warnings for `coords`/`utils`).

- [ ] **Step 8: Commit**

```bash
git add css/coords.css docs/sidebar-types.md components/sidebar-types.html CHANGELOG.md
git commit -m "fix(coords): fixed narrow width for non-decimal fields in .coord-vals rows"
```

---

### Task 2: Release v1.21.1

Bundles the Task 1 fix into a PATCH release per `docs/versioning.md` (bug/behavior fix to an already-shipped component, no new public class or token — matches the precedent of treating component refinements as PATCH rather than MINOR).

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the `## [Unreleased]` → `### Fixed` section written in Task 1.

- [ ] **Step 1: Rename `[Unreleased]` to the release header**

In `CHANGELOG.md`, change:
```markdown
## [Unreleased]
```
to:
```markdown
## v1.21.1 - 2026-07-18
```
(keep the `### Fixed` block and its bullet unchanged underneath).

- [ ] **Step 2: Add a fresh empty `[Unreleased]` section above it**

Insert directly above the new `## v1.21.1 - 2026-07-18` header:

```markdown
## [Unreleased]

---

```

- [ ] **Step 3: Run full consistency check**

Run: `python3 scripts/cli/check_consistency.py && python3 -m pytest scripts/cli/test_check_consistency.py -q`
Expected: both pass — `✔ Manifest und Dateien sind konsistent` and all tests passed.

- [ ] **Step 4: Commit the release**

```bash
git add CHANGELOG.md
git commit -m "chore: release v1.21.1"
```

- [ ] **Step 5: Tag the release**

```bash
git tag -a v1.21.1 -m "Release v1.21.1"
```

- [ ] **Step 6: Push — ASK THE USER FIRST**

Pushing to `origin/main` and pushing a tag are both externally visible, hard-to-reverse actions. Confirm with the user before running:

```bash
git push origin main
git push origin v1.21.1
```

---

## Self-Review Notes

- **Spec coverage:** all 5 acceptance-checklist items in `coord-vals-decimal-field-width-request.md` Section 5 are covered — CSS rule added (Task 1 Step 1), existing decimal-field rule left unchanged (Step 1, explicitly not modified), DD-format unaffected (only rows with a `:not([inputmode="decimal"])` field are touched; a DD row has exactly one field, always `inputmode="decimal"`, so the new rule never matches — visually identical), `components/` reference shows the difference (Step 4/5, using the already-correct `inputmode` attributes from v1.21.0), `CHANGELOG.md` updated (Step 6).
- **No registry.json changes:** `coords.css`/`docs/sidebar-types.md`/`components/sidebar-types.html` already have owning entries (confirmed in the prior 2026-07-18 batch's self-review) — `check_consistency.py` will not flag orphans.
- **Versioning check:** user confirmed PATCH (v1.21.1) — this refines the width behavior of the already-shipped `.coord-vals` pattern (v1.21.0), introduces no new class/token, matches prior practice of treating extensions to existing components as PATCH rather than MINOR.
- **website-v3 follow-up (out of scope here):** once this ships, `open-items.md` item 6 in `website-v3/docs/ci/` needs to move to "Erledigt" and the local `src/app.css` override can be removed — that repo work is explicitly out of scope for this plan (lives outside `oe5ith-ci`).

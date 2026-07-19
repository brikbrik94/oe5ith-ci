# Erreichbarkeits-/Zonen-Skala (`--scale-reach-*`) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a 10-step red→green color scale (`--scale-reach-1..10` + `--scale-reach-gradient`) plus a `.scale-reach-bar` utility class to the `oe5ith-ci` design system, for coloring map zones by duration/distance (worst=red, best=green).

**Architecture:** Pure CSS/docs addition, no build step, no JS in this repo. Tokens go in `css/common.css` (source of truth), a gradient utility in `css/utils.css`, documentation in `docs/tokens.md`, and a live swatch preview in `components/tokens.html`. No new files, no `docs/registry.json` entry (covered by the existing `tokens` entry). Finish with a `CHANGELOG.md` entry and a `v1.22.0` tag.

**Tech Stack:** CSS custom properties, static HTML reference pages, `scripts/cli/check_consistency.py` (Python 3, stdlib only) for the registry consistency gate.

## Global Constraints

- Never hardcode colors/z-index outside tokens — all 10 scale colors are defined once in `css/common.css` and consumed via `var()` everywhere else.
- Endpoints must equal existing semantic tokens: `--scale-reach-1` = `#ef4444` (same value as `--danger`), `--scale-reach-10` = `#22c55e` (same value as `--success`).
- No new `docs/registry.json` entry — this extends the existing `tokens` entry (`category: infra`, already points at `common.css`/`tokens.md`/`tokens.html`).
- `python3 scripts/cli/check_consistency.py` must exit 0 with no errors before this is considered done.
- Additive only — do not modify any existing token value, class, or file structure.
- Versioning: additive tokens/utility = MINOR release → `v1.22.0`. `CHANGELOG.md` entry under `Added`, per format in `docs/versioning.md`.
- Spec: `docs/superpowers/specs/2026-07-19-scale-reach-tokens-design.md` — read it first if anything here is ambiguous.

---

### Task 1: Add color tokens to `css/common.css`

**Files:**
- Modify: `css/common.css:46-50`

**Interfaces:**
- Produces: CSS custom properties `--scale-reach-1` through `--scale-reach-10` (hex colors) and `--scale-reach-gradient` (a `linear-gradient()` value), all defined inside the existing `:root { }` block. Later tasks (utility class, docs, HTML swatches) consume these by name.

- [ ] **Step 1: Write the verification grep (fails first — tokens don't exist yet)**

Run:
```bash
grep -c -- "--scale-reach-" css/common.css
```
Expected: `0` (tokens not yet defined) — confirms the starting state before the edit.

- [ ] **Step 2: Insert the token block**

In `css/common.css`, the current text around line 46-50 reads:

```css
  --danger:           #ef4444;
  --danger-subtle:    rgba(239,68,68,0.10);
  --danger-border:    rgba(239,68,68,0.25);

  --auth:             #a78bfa;
```

Replace it with (inserting the new block between `--danger-border` and the blank line before `--auth`):

```css
  --danger:           #ef4444;
  --danger-subtle:    rgba(239,68,68,0.10);
  --danger-border:    rgba(239,68,68,0.25);

  /* ── FARBEN: Erreichbarkeits-/Zonen-Skala ── */
  /* Stufe 1 = schlechteste Erreichbarkeit (weit/lang) = --danger.
     Stufe 10 = beste Erreichbarkeit (nah/kurz) = --success.
     Für Dauer-/Entfernungs-Zonierung auf Kartenseiten (Polygon-Fill). */
  --scale-reach-1:  #ef4444;
  --scale-reach-2:  #ec6b3d;
  --scale-reach-3:  #ea9537;
  --scale-reach-4:  #e8c131;
  --scale-reach-5:  #dbe52b;
  --scale-reach-6:  #a7e225;
  --scale-reach-7:  #71e01f;
  --scale-reach-8:  #3dd620;
  --scale-reach-9:  #21cd33;
  --scale-reach-10: #22c55e;
  --scale-reach-gradient: linear-gradient(
    to right,
    var(--scale-reach-1), var(--scale-reach-2), var(--scale-reach-3),
    var(--scale-reach-4), var(--scale-reach-5), var(--scale-reach-6),
    var(--scale-reach-7), var(--scale-reach-8), var(--scale-reach-9),
    var(--scale-reach-10)
  );

  --auth:             #a78bfa;
```

- [ ] **Step 3: Run the verification grep to confirm all 11 tokens exist**

Run:
```bash
grep -cE '^\s*--scale-reach-[0-9]+:' css/common.css
```
Expected: `10` (exactly the 10 numbered definition lines, `--scale-reach-1:` through `--scale-reach-10:`).

Run:
```bash
grep -c "scale-reach-gradient:" css/common.css
```
Expected: `1` (the gradient token's own definition line).

Also run this exact-value spot check:
```bash
grep -n -- "--scale-reach-1:\|--scale-reach-10:" css/common.css
```
Expected output contains exactly:
```
  --scale-reach-1:  #ef4444;
  --scale-reach-10: #22c55e;
```

- [ ] **Step 4: Commit**

```bash
git add css/common.css
git commit -m "$(cat <<'EOF'
feat(tokens): add --scale-reach-1..10 zone color scale

10-step red->green scale for duration/distance-based map zone coloring.
Endpoints match existing --danger/--success tokens.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Add `.scale-reach-bar` utility class to `css/utils.css`

**Files:**
- Modify: `css/utils.css` (append after the last rule, `.no-dot-bg`, at end of file)

**Interfaces:**
- Consumes: `--scale-reach-gradient` from Task 1, `--badge-radius` (existing token, `css/common.css:125`, value `4px`).
- Produces: CSS class `.scale-reach-bar` — a fixed-height horizontal gradient bar. Task 4 (HTML swatches) uses this class for the live preview.

- [ ] **Step 1: Write the verification grep (fails first)**

Run:
```bash
grep -c "scale-reach-bar" css/utils.css
```
Expected: `0`.

- [ ] **Step 2: Append the utility block**

Append to the end of `css/utils.css` (after the existing `.no-dot-bg` rule):

```css

/* ═══════════════════════════════════════
   SCALE UTILITIES
   ═══════════════════════════════════════ */

/* Durchgehender Verlaufs-Balken über die volle --scale-reach-Skala,
   z.B. als visuelle Legende unter/neben Zonen-Karten. */
.scale-reach-bar {
  height: 8px;
  border-radius: var(--badge-radius);
  background: var(--scale-reach-gradient);
}
```

- [ ] **Step 3: Run the verification grep to confirm it landed**

Run:
```bash
grep -n "scale-reach-bar" css/utils.css
```
Expected: two matches — the comment/selector line and the class rule opening.

- [ ] **Step 4: Commit**

```bash
git add css/utils.css
git commit -m "$(cat <<'EOF'
feat(utils): add .scale-reach-bar gradient utility

Renders the full --scale-reach-gradient as a horizontal bar for use
as a legend strip next to duration/distance zone maps.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Document the scale in `docs/tokens.md`

**Files:**
- Modify: `docs/tokens.md` (insert new section between the existing `## Chart-Farbslots` section and `## Code / Terminal Farben` section, i.e. after the `---` that currently sits right before `## Code / Terminal Farben`)

**Interfaces:**
- Consumes: token names/values from Task 1 (must match exactly — copy-paste, do not retype hex values).
- Produces: a `## Erreichbarkeits-/Zonen-Skala` doc section that a future agent can build the pattern from without reading any HTML.

- [ ] **Step 1: Write the verification grep (fails first)**

Run:
```bash
grep -c "Erreichbarkeits-/Zonen-Skala" docs/tokens.md
```
Expected: `0`.

- [ ] **Step 2: Insert the doc section**

Find this exact text in `docs/tokens.md` (end of the Chart-Farbslots section):

```markdown
| `--chart-area-opacity` | `0.15` | Füll-Transparenz für Bereichsdiagramme |

---

## Code / Terminal Farben
```

Replace it with:

```markdown
| `--chart-area-opacity` | `0.15` | Füll-Transparenz für Bereichsdiagramme |

---

## Erreichbarkeits-/Zonen-Skala

10-stufige Farbskala für Dauer-/Entfernungs-basierte Zonierung auf Kartenseiten
(z.B. Erreichbarkeits-/Sicherheitszonen als Leaflet/MapLibre-Polygon-Fill).
Stufe 1 = Rot = schlechteste Erreichbarkeit (weit/lang), Stufe 10 = Grün =
beste Erreichbarkeit (nah/kurz). Endpunkte sind identisch zu `--danger`/
`--success`; die 8 Zwischenstufen sind eine lineare HSL-Interpolation.

| Token | Wert | Bedeutung |
|---|---|---|
| `--scale-reach-1` | `#ef4444` | Stufe 1 — schlechteste Erreichbarkeit (= `--danger`) |
| `--scale-reach-2` | `#ec6b3d` | Stufe 2 |
| `--scale-reach-3` | `#ea9537` | Stufe 3 |
| `--scale-reach-4` | `#e8c131` | Stufe 4 |
| `--scale-reach-5` | `#dbe52b` | Stufe 5 |
| `--scale-reach-6` | `#a7e225` | Stufe 6 |
| `--scale-reach-7` | `#71e01f` | Stufe 7 |
| `--scale-reach-8` | `#3dd620` | Stufe 8 |
| `--scale-reach-9` | `#21cd33` | Stufe 9 |
| `--scale-reach-10` | `#22c55e` | Stufe 10 — beste Erreichbarkeit (= `--success`) |
| `--scale-reach-gradient` | `linear-gradient(to right, --scale-reach-1 … --scale-reach-10)` | Durchgehender Verlauf über alle 10 Stufen |

**Utility-Klasse:** `.scale-reach-bar` (`css/utils.css`) — rendert
`--scale-reach-gradient` als 8px hoher horizontaler Balken, z.B. als
Legenden-Streifen unter/neben der Karte.

**Verwendung (App-Code, nicht Teil dieses Repos):**

```js
// Duration/Distance-Wert in Bucket 1-10 mappen (App-Logik, nicht CI)
const step = bucketize(zone.durationMinutes); // 1..10
polygon.setStyle({
  fillColor: getComputedStyle(document.documentElement)
    .getPropertyValue(`--scale-reach-${step}`).trim(),
});
```

Für die Legende die bestehende `MapLegend`-Klasse verwenden
(`docs/map-legend.md`, `type: 'area'`) — sie akzeptiert jeden CSS-Farbwert,
keine CI-Änderung nötig.

---

## Code / Terminal Farben
```

- [ ] **Step 3: Run the verification grep to confirm it landed**

Run:
```bash
grep -c "Erreichbarkeits-/Zonen-Skala" docs/tokens.md
grep -c -- "--scale-reach-" docs/tokens.md
```
Expected: first command `1` (the `##` heading); second command `12` (10 table rows for steps 1-10 + 1 row for `--scale-reach-gradient` + 1 line in the JS usage example — grep `-c` counts matching *lines*, and the gradient table row contains multiple `--scale-reach-` occurrences on one line but still counts as 1).

- [ ] **Step 4: Commit**

```bash
git add docs/tokens.md
git commit -m "$(cat <<'EOF'
docs(tokens): document --scale-reach-* zone color scale

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Add live swatch preview to `components/tokens.html` + run consistency check

**Files:**
- Modify: `components/tokens.html` (insert new `<div class="section">` between the closing `</div>` of the "Semantische Farben" section and the `<!-- ═══ CODE FARBEN ═══ -->` comment)

**Interfaces:**
- Consumes: `.swatch`, `.swatch-color`, `.swatch-info`, `.swatch-name`, `.swatch-token`, `.swatch-hex`, `.swatch-grid`, `.section`, `.section-title` (existing classes already used throughout this file — do not invent new ones); `.scale-reach-bar` from Task 2.

- [ ] **Step 1: Write the verification grep (fails first)**

Run:
```bash
grep -c "scale-reach" components/tokens.html
```
Expected: `0`.

- [ ] **Step 2: Insert the new section**

Find this exact text in `components/tokens.html` (end of the "Semantische Farben" section):

```html
        <span class="subtle-chip" style="background:var(--auth-subtle);color:var(--auth);border-color:var(--auth-border)">Auth subtle</span>
      </div>
    </div>
  </div>

  <!-- ═══ CODE FARBEN ═══ -->
```

Replace it with:

```html
        <span class="subtle-chip" style="background:var(--auth-subtle);color:var(--auth);border-color:var(--auth-border)">Auth subtle</span>
      </div>
    </div>
  </div>

  <!-- ═══ ERREICHBARKEITS-/ZONEN-SKALA ═══ -->
  <div class="section">
    <div class="section-title">Erreichbarkeits-/Zonen-Skala</div>
    <div class="swatch-grid">

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-1)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 1 (schlechtest)</span>
          <span class="swatch-token">--scale-reach-1</span>
          <span class="swatch-hex">#ef4444</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-2)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 2</span>
          <span class="swatch-token">--scale-reach-2</span>
          <span class="swatch-hex">#ec6b3d</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-3)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 3</span>
          <span class="swatch-token">--scale-reach-3</span>
          <span class="swatch-hex">#ea9537</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-4)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 4</span>
          <span class="swatch-token">--scale-reach-4</span>
          <span class="swatch-hex">#e8c131</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-5)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 5</span>
          <span class="swatch-token">--scale-reach-5</span>
          <span class="swatch-hex">#dbe52b</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-6)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 6</span>
          <span class="swatch-token">--scale-reach-6</span>
          <span class="swatch-hex">#a7e225</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-7)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 7</span>
          <span class="swatch-token">--scale-reach-7</span>
          <span class="swatch-hex">#71e01f</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-8)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 8</span>
          <span class="swatch-token">--scale-reach-8</span>
          <span class="swatch-hex">#3dd620</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-9)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 9</span>
          <span class="swatch-token">--scale-reach-9</span>
          <span class="swatch-hex">#21cd33</span>
        </div>
      </div>

      <div class="swatch">
        <div class="swatch-color" style="background:var(--scale-reach-10)"></div>
        <div class="swatch-info">
          <span class="swatch-name">Reach 10 (best)</span>
          <span class="swatch-token">--scale-reach-10</span>
          <span class="swatch-hex">#22c55e</span>
        </div>
      </div>

    </div>

    <!-- Gradient-Vorschau -->
    <div style="margin-top:12px">
      <div class="scale-reach-bar"></div>
    </div>
  </div>

  <!-- ═══ CODE FARBEN ═══ -->
```

- [ ] **Step 3: Run the verification grep to confirm it landed**

Run:
```bash
grep -c "scale-reach" components/tokens.html
```
Expected: `21` (10 swatches × 2 matching lines each [the `style="background:var(--scale-reach-N)"` line and the `<span class="swatch-token">--scale-reach-N</span>` line] = 20, plus 1 line for the `<div class="scale-reach-bar"></div>` preview).

- [ ] **Step 4: Run the repo consistency check**

Run:
```bash
python3 scripts/cli/check_consistency.py
```
Expected: exits 0, no errors printed (warnings about unrelated pre-existing files, if any, are not caused by this change and can be ignored — only confirm no *new* errors reference `tokens`, `common.css`, `tokens.md`, or `tokens.html`).

- [ ] **Step 5: Commit**

```bash
git add components/tokens.html
git commit -m "$(cat <<'EOF'
docs(tokens): add --scale-reach-* swatch preview to tokens.html

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Changelog entry and release tag

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- None (final release/documentation task, consumes nothing new).

- [ ] **Step 1: Write the verification grep (fails first)**

Run:
```bash
grep -c "scale-reach" CHANGELOG.md
```
Expected: `0`.

- [ ] **Step 2: Add the changelog entry**

In `CHANGELOG.md`, the file currently starts with:

```markdown
# Changelog

Alle relevanten Änderungen am `oe5ith-ci` Repository werden in dieser Datei dokumentiert.
Format: `## vX.Y.Z - YYYY-MM-DD` · Neueste Version zuerst · Siehe `docs/versioning.md`

---

## [Unreleased]

---

## v1.21.1 - 2026-07-18
```

Replace the `## [Unreleased]` block with a new dated release section (use today's date, `2026-07-19`):

```markdown
# Changelog

Alle relevanten Änderungen am `oe5ith-ci` Repository werden in dieser Datei dokumentiert.
Format: `## vX.Y.Z - YYYY-MM-DD` · Neueste Version zuerst · Siehe `docs/versioning.md`

---

## [Unreleased]

---

## v1.22.0 - 2026-07-19

### Added
- `common.css`: neue Token-Gruppe `--scale-reach-1..10` + `--scale-reach-gradient` — 10-stufige
  Rot-nach-Grün-Skala für Dauer-/Entfernungs-basierte Zonenfärbung auf Kartenseiten (Stufe 1 =
  `--danger`, Stufe 10 = `--success`). `utils.css`: neue Utility-Klasse `.scale-reach-bar` rendert
  den Verlauf als Balken. Dokumentiert in `docs/tokens.md` und `components/tokens.html`.

---

## v1.21.1 - 2026-07-18
```

- [ ] **Step 3: Run the verification grep to confirm it landed**

Run:
```bash
grep -c "scale-reach" CHANGELOG.md
grep -n "## v1.22.0" CHANGELOG.md
```
Expected: first command `1`, second command shows the new heading line.

- [ ] **Step 4: Commit**

```bash
git add CHANGELOG.md
git commit -m "$(cat <<'EOF'
chore: release v1.22.0
EOF
)"
```

- [ ] **Step 5: Tag the release (do NOT push — confirm with the user first)**

Run:
```bash
git tag -a v1.22.0 -m "Release v1.22.0"
```

Do not run `git push` or `git push origin v1.22.0` as part of this task — pushing the tag/commits is a shared-state action and must be confirmed with the user in the current session before executing, per this repo's Git Safety Protocol.

---

## Self-Review Notes

- **Spec coverage:** Task 1 = token values section of spec. Task 2 = utility class section. Task 3 = docs section (incl. usage example, map-legend note, out-of-scope note reflected by omitting any JS bucketing implementation). Task 4 = components/tokens.html swatch section from spec. Task 5 = versioning section of spec. No spec section left uncovered.
- **Placeholder scan:** no TBD/TODO; every step shows the literal code/text to insert; every verification step has an exact command and exact expected output.
- **Type/name consistency:** `--scale-reach-1..10`, `--scale-reach-gradient`, and `.scale-reach-bar` are spelled identically across all 5 tasks (checked against Task 1's definitions, which are canonical).

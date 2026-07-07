# Maneuver-Icons Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a 14-icon `ci-maneuver-*` line-art SVG set mapped 1:1 to OpenRouteService (ORS) maneuver codes 0–13, plus a `.disclosure-item-icon` slot in the Disclosure component so the routing sidebar's turn-by-turn list can render a direction icon per step.

**Architecture:** New asset category `assets/maneuver-icons/` (14 standalone SVGs + `icons.json` manifest keyed by `orsCode`), following the same registry/doc/gallery template already established by `assets/map-icons/`. One CSS addition (`.disclosure-item-icon`) to the existing `disclosure.css`. No build step, no JS, no new tokens.

**Tech Stack:** Plain SVG, CSS (existing CI tokens only), static HTML reference pages, JSON manifest. Verification via `python3 scripts/cli/check_consistency.py` (repo's only automated check) and manual visual check of the reference gallery in a browser.

## Global Constraints

- No new CSS tokens — `.disclosure-item-icon` uses `color: var(--text)` (existing token).
- No hardcoded colors — every icon uses `currentColor` exclusively (`stroke="currentColor"`, and `fill="currentColor"` only where noted).
- `assets/maneuver-icons/` is not scanned by `check_consistency.py` (only `css/`, `components/`, `docs/` are) — no per-file registry entries for the SVGs themselves; `icons.json` is their registry.
- Every SVG: `viewBox="0 0 16 16"`, no `<text>`, no `<filter>`, no embedded raster.
- No CSS-transform-based mirroring/rotation at runtime — each of the 14 icons is an independent, standalone file.
- `docs/registry.json` gets exactly one new entry, `"category": "asset"` (not `"component"`) — keeps it out of the README status table.
- Version: MINOR `v1.20.0`. Update `CHANGELOG.md` before tagging.
- Never change existing file paths; only add new files and extend existing ones (`disclosure.css`, `disclosure.html`, `sidebar.md`, `registry.json`, `CHANGELOG.md`, `README.md`).

---

### Task 1: Author the 14 maneuver SVG icons

**Files:**
- Create: `assets/maneuver-icons/ci-maneuver-turn-left.svg`
- Create: `assets/maneuver-icons/ci-maneuver-turn-right.svg`
- Create: `assets/maneuver-icons/ci-maneuver-sharp-left.svg`
- Create: `assets/maneuver-icons/ci-maneuver-sharp-right.svg`
- Create: `assets/maneuver-icons/ci-maneuver-slight-left.svg`
- Create: `assets/maneuver-icons/ci-maneuver-slight-right.svg`
- Create: `assets/maneuver-icons/ci-maneuver-straight.svg`
- Create: `assets/maneuver-icons/ci-maneuver-roundabout-enter.svg`
- Create: `assets/maneuver-icons/ci-maneuver-roundabout-exit.svg`
- Create: `assets/maneuver-icons/ci-maneuver-uturn.svg`
- Create: `assets/maneuver-icons/ci-maneuver-goal.svg`
- Create: `assets/maneuver-icons/ci-maneuver-depart.svg`
- Create: `assets/maneuver-icons/ci-maneuver-keep-left.svg`
- Create: `assets/maneuver-icons/ci-maneuver-keep-right.svg`

**Interfaces:**
- Produces: 14 SVG files, each `viewBox="0 0 16 16"`, `stroke="currentColor"`, that Task 2 (manifest), Task 4 (disclosure.html), and Task 5 (gallery) reference by exact filename.

- [ ] **Step 1: Create the directory and write all 14 SVG files**

```bash
mkdir -p assets/maneuver-icons
```

`assets/maneuver-icons/ci-maneuver-turn-left.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 Q8 7 2.6 7"/>
  <path d="M2 4.7 L2.6 7 L4.1 5.2"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-turn-right.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 Q8 7 13.4 7"/>
  <path d="M14 4.7 L13.4 7 L11.9 5.2"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-sharp-left.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 Q8 11.5 3.8 11.5"/>
  <path d="M1.6 10.5 L3.8 11.5 L3.4 9.2"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-sharp-right.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 Q8 11.5 12.2 11.5"/>
  <path d="M14.4 10.5 L12.2 11.5 L12.6 9.2"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-slight-left.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 Q8 3 5.7 3"/>
  <path d="M7.3 1.2 L5.7 3 L8.1 3.2"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-slight-right.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 Q8 3 10.3 3"/>
  <path d="M8.7 1.2 L10.3 3 L7.9 3.2"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-straight.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 V4"/>
  <path d="M5.5 6.5 L8 4 L10.5 6.5"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-roundabout-enter.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="8" cy="8" r="4"/>
  <path d="M8 14 V12"/>
  <path d="M6 12.5 L8 10.5 L10 12.5"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-roundabout-exit.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="8" cy="8" r="4"/>
  <path d="M8 4 V2"/>
  <path d="M6 3.5 L8 1.5 L10 3.5"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-uturn.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M11 13 V6 A3 3 0 0 0 5 6 V9"/>
  <path d="M2.8 7 L5 9.5 L7.2 7"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-goal.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M5 14.5 V2.5"/>
  <path d="M5 3 L11.5 5.2 L5 7.4 Z" fill="currentColor" stroke="none"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-depart.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="8" cy="8" r="5" stroke-width="1.3"/>
  <circle cx="8" cy="8" r="2.2" fill="currentColor" stroke="none"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-keep-left.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 V9"/>
  <path d="M8 9 Q8 6 5.5 4.5"/>
  <path d="M7.2 2.8 L5.3 4.3 L6.8 6.4"/>
  <path d="M8 9 Q8 6.5 10 5.5" opacity="0.35"/>
</svg>
```

`assets/maneuver-icons/ci-maneuver-keep-right.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 13 V9"/>
  <path d="M8 9 Q8 6 10.5 4.5"/>
  <path d="M8.8 2.8 L10.7 4.3 L9.2 6.4"/>
  <path d="M8 9 Q8 6.5 6 5.5" opacity="0.35"/>
</svg>
```

- [ ] **Step 2: Validate all 14 files are well-formed XML**

Run:
```bash
python3 -c "
import xml.dom.minidom as m, glob
files = sorted(glob.glob('assets/maneuver-icons/*.svg'))
assert len(files) == 14, f'expected 14 files, found {len(files)}'
for f in files:
    m.parse(f)
    print('OK', f)
"
```

Expected: `OK assets/maneuver-icons/ci-maneuver-<name>.svg` printed 14 times, no exception.

- [ ] **Step 3: Commit**

```bash
git add assets/maneuver-icons/*.svg
git commit -m "feat(maneuver-icons): add 14 ci-maneuver-* direction SVGs"
```

---

### Task 2: Write the `icons.json` manifest

**Files:**
- Create: `assets/maneuver-icons/icons.json`

**Interfaces:**
- Consumes: the 14 filenames from Task 1 (must match exactly).
- Produces: `assets/maneuver-icons/icons.json` — the `orsCode → name/file/label` lookup table that `docs/maneuver-icons.md` (Task 6) documents and that consuming apps read at runtime.

- [ ] **Step 1: Write the manifest**

`assets/maneuver-icons/icons.json`:
```json
{
  "version": 1,
  "grid": [16, 16],
  "icons": [
    { "orsCode": 0,  "name": "ci-maneuver-turn-left",        "file": "ci-maneuver-turn-left.svg",        "label": "Left" },
    { "orsCode": 1,  "name": "ci-maneuver-turn-right",       "file": "ci-maneuver-turn-right.svg",       "label": "Right" },
    { "orsCode": 2,  "name": "ci-maneuver-sharp-left",       "file": "ci-maneuver-sharp-left.svg",       "label": "Sharp left" },
    { "orsCode": 3,  "name": "ci-maneuver-sharp-right",      "file": "ci-maneuver-sharp-right.svg",      "label": "Sharp right" },
    { "orsCode": 4,  "name": "ci-maneuver-slight-left",      "file": "ci-maneuver-slight-left.svg",      "label": "Slight left" },
    { "orsCode": 5,  "name": "ci-maneuver-slight-right",     "file": "ci-maneuver-slight-right.svg",     "label": "Slight right" },
    { "orsCode": 6,  "name": "ci-maneuver-straight",         "file": "ci-maneuver-straight.svg",         "label": "Straight" },
    { "orsCode": 7,  "name": "ci-maneuver-roundabout-enter", "file": "ci-maneuver-roundabout-enter.svg", "label": "Enter roundabout" },
    { "orsCode": 8,  "name": "ci-maneuver-roundabout-exit",  "file": "ci-maneuver-roundabout-exit.svg",  "label": "Exit roundabout" },
    { "orsCode": 9,  "name": "ci-maneuver-uturn",            "file": "ci-maneuver-uturn.svg",            "label": "U-turn" },
    { "orsCode": 10, "name": "ci-maneuver-goal",             "file": "ci-maneuver-goal.svg",             "label": "Goal" },
    { "orsCode": 11, "name": "ci-maneuver-depart",           "file": "ci-maneuver-depart.svg",           "label": "Depart" },
    { "orsCode": 12, "name": "ci-maneuver-keep-left",        "file": "ci-maneuver-keep-left.svg",        "label": "Keep left" },
    { "orsCode": 13, "name": "ci-maneuver-keep-right",       "file": "ci-maneuver-keep-right.svg",       "label": "Keep right" }
  ]
}
```

- [ ] **Step 2: Validate the manifest against the files on disk**

Run:
```bash
python3 -c "
import json, pathlib
d = pathlib.Path('assets/maneuver-icons')
manifest = json.loads((d / 'icons.json').read_text())
icons = manifest['icons']
assert len(icons) == 14, f'expected 14 entries, found {len(icons)}'
codes = sorted(i['orsCode'] for i in icons)
assert codes == list(range(14)), f'orsCode gaps/dupes: {codes}'
for i in icons:
    assert (d / i['file']).is_file(), f\"missing file: {i['file']}\"
    assert i['name'] == i['file'].removesuffix('.svg')
print('manifest OK: 14 entries, codes 0-13 complete, all files exist')
"
```

Expected: `manifest OK: 14 entries, codes 0-13 complete, all files exist`

- [ ] **Step 3: Commit**

```bash
git add assets/maneuver-icons/icons.json
git commit -m "feat(maneuver-icons): add icons.json manifest (ORS code 0-13 mapping)"
```

---

### Task 3: Add `.disclosure-item-icon` to `disclosure.css`

**Files:**
- Modify: `css/disclosure.css`

**Interfaces:**
- Produces: CSS class `.disclosure-item-icon` — a 16×16 flex-shrink-0 icon slot, `color: var(--text)`, that Task 4 and Task 5 place as the first child of `.disclosure-item`.

- [ ] **Step 1: Read the current ITEM section**

The file currently has (`css/disclosure.css:72-97`):
```css
/* ═══════════════════════════════════════
   ITEM
   ═══════════════════════════════════════ */
.disclosure-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
}
.disclosure-item:last-child {
  border-bottom: none;
}

.disclosure-item-text {
  flex: 1;
  min-width: 0;
  color: var(--text);
  font-size: 0.82rem;
}

.disclosure-item-meta {
  flex-shrink: 0;
  color: var(--muted);
  font-size: 0.72rem;
}
```

- [ ] **Step 2: Insert `.disclosure-item-icon` between `.disclosure-item` and `.disclosure-item-text`**

Change it to:
```css
/* ═══════════════════════════════════════
   ITEM
   ═══════════════════════════════════════ */
.disclosure-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
}
.disclosure-item:last-child {
  border-bottom: none;
}

.disclosure-item-icon {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  color: var(--text);
}

.disclosure-item-text {
  flex: 1;
  min-width: 0;
  color: var(--text);
  font-size: 0.82rem;
}

.disclosure-item-meta {
  flex-shrink: 0;
  color: var(--muted);
  font-size: 0.72rem;
}
```

- [ ] **Step 3: Verify no other CSS file already defines `.disclosure-item-icon`**

Run:
```bash
grep -rn "disclosure-item-icon" css/
```

Expected: only the one match, inside `css/disclosure.css`.

- [ ] **Step 4: Commit**

```bash
git add css/disclosure.css
git commit -m "feat(disclosure): add .disclosure-item-icon slot for turn-by-turn icons"
```

---

### Task 4: Wire icons into `components/disclosure.html`

**Files:**
- Modify: `components/disclosure.html`

**Interfaces:**
- Consumes: `.disclosure-item-icon` (Task 3), the 14 SVG path shapes (Task 1 — inlined directly, not referenced by `<img src>`, so `currentColor` inherits correctly).

- [ ] **Step 1: Update the two `.disclosure-item` groups to include an icon per step**

The current content (`components/disclosure.html:38-71`) has two `<details class="disclosure">` blocks, each with `.disclosure-item` rows with only text + meta. Replace both inner item lists with icon-prefixed versions:

First block (closed panel, `components/disclosure.html:37-46`):
```html
            <div class="disclosure-body">
              <div class="disclosure-item">
                <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="8" cy="8" r="5" stroke-width="1.3"/>
                  <circle cx="8" cy="8" r="2.2" fill="currentColor" stroke="none"/>
                </svg>
                <span class="disclosure-item-text">Head northeast on Untere Donauländer, B129</span>
                <span class="disclosure-item-meta mono">280 m</span>
              </div>
              <div class="disclosure-item">
                <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M8 13 Q8 7 13.4 7"/>
                  <path d="M14 4.7 L13.4 7 L11.9 5.2"/>
                </svg>
                <span class="disclosure-item-text">Turn right onto Welser Straße</span>
                <span class="disclosure-item-meta mono">1.2 km</span>
              </div>
            </div>
```

Second block (open panel, `components/disclosure.html:59-72`):
```html
            <div class="disclosure-body">
              <div class="disclosure-item">
                <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="8" cy="8" r="5" stroke-width="1.3"/>
                  <circle cx="8" cy="8" r="2.2" fill="currentColor" stroke="none"/>
                </svg>
                <span class="disclosure-item-text">Head northeast on Untere Donauländer, B129</span>
                <span class="disclosure-item-meta mono">280 m</span>
              </div>
              <div class="disclosure-item">
                <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M8 13 Q8 7 13.4 7"/>
                  <path d="M14 4.7 L13.4 7 L11.9 5.2"/>
                </svg>
                <span class="disclosure-item-text">Turn right onto Welser Straße, ein sehr langer Straßenname zum Testen der Ellipsis-Abschneidung im schmalen Panel</span>
                <span class="disclosure-item-meta mono">1.2 km</span>
              </div>
              <div class="disclosure-item">
                <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M8 13 V4"/>
                  <path d="M5.5 6.5 L8 4 L10.5 6.5"/>
                </svg>
                <span class="disclosure-item-text">Continue onto Kaiser-Josef-Platz</span>
                <span class="disclosure-item-meta mono">340 m</span>
              </div>
            </div>
```

- [ ] **Step 2: Validate the HTML is well-formed**

Run:
```bash
python3 -c "
import xml.dom.minidom as m
m.parse('components/disclosure.html')
print('disclosure.html: well-formed')
" 2>&1 || true
```

(If minidom rejects it due to HTML entities/void elements unrelated to this edit, instead visually confirm via: `grep -c 'disclosure-item-icon' components/disclosure.html` — expected `5`, one per `.disclosure-item` across both blocks.)

- [ ] **Step 3: Commit**

```bash
git add components/disclosure.html
git commit -m "feat(disclosure): show maneuver icons in turn-by-turn example"
```

---

### Task 5: Create the `maneuver-icons` reference gallery

**Files:**
- Create: `components/maneuver-icons.html`

**Interfaces:**
- Consumes: all 14 SVG path shapes (Task 1), `.disclosure-item-icon` (Task 3), `css/demo.css` (existing, demo-only stylesheet per `CLAUDE.md`).

- [ ] **Step 1: Write the gallery page**

`components/maneuver-icons.html`:
```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Maneuver-Icons</title>
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/typography.css">
<link rel="stylesheet" href="../css/badges.css">
<link rel="stylesheet" href="../css/page.css">
<link rel="stylesheet" href="../css/disclosure.css">
<link rel="stylesheet" href="../css/demo.css">
</head>
<body>

<div class="page-content">

  <!-- ═══ KATALOG ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Maneuver-Icons — Katalog (ORS-Code 0–13)</div>
    <div class="demo-section-desc">
      14 Line-Art-Icons für Turn-by-Turn-Wegbeschreibungen, 1:1 zu den
      Manöver-Codes von OpenRouteService (ORS). <code>viewBox 0 0 16 16</code>,
      <code>stroke="currentColor"</code> — kein SDF/MapLibre-Bezug (siehe
      <code>assets/map-icons/</code> für Karten-Marker).
    </div>
    <div class="demo-row" style="flex-wrap:wrap; gap:20px;">

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 Q8 7 2.6 7"/>
          <path d="M2 4.7 L2.6 7 L4.1 5.2"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">0 · Left</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 Q8 7 13.4 7"/>
          <path d="M14 4.7 L13.4 7 L11.9 5.2"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">1 · Right</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 Q8 11.5 3.8 11.5"/>
          <path d="M1.6 10.5 L3.8 11.5 L3.4 9.2"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">2 · Sharp left</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 Q8 11.5 12.2 11.5"/>
          <path d="M14.4 10.5 L12.2 11.5 L12.6 9.2"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">3 · Sharp right</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 Q8 3 5.7 3"/>
          <path d="M7.3 1.2 L5.7 3 L8.1 3.2"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">4 · Slight left</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 Q8 3 10.3 3"/>
          <path d="M8.7 1.2 L10.3 3 L7.9 3.2"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">5 · Slight right</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 V4"/>
          <path d="M5.5 6.5 L8 4 L10.5 6.5"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">6 · Straight</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="8" cy="8" r="4"/>
          <path d="M8 14 V12"/>
          <path d="M6 12.5 L8 10.5 L10 12.5"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">7 · Enter roundabout</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="8" cy="8" r="4"/>
          <path d="M8 4 V2"/>
          <path d="M6 3.5 L8 1.5 L10 3.5"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">8 · Exit roundabout</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M11 13 V6 A3 3 0 0 0 5 6 V9"/>
          <path d="M2.8 7 L5 9.5 L7.2 7"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">9 · U-turn</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 14.5 V2.5"/>
          <path d="M5 3 L11.5 5.2 L5 7.4 Z" fill="currentColor" stroke="none"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">10 · Goal</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="8" cy="8" r="5" stroke-width="1.3"/>
          <circle cx="8" cy="8" r="2.2" fill="currentColor" stroke="none"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">11 · Depart</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 V9"/>
          <path d="M8 9 Q8 6 5.5 4.5"/>
          <path d="M7.2 2.8 L5.3 4.3 L6.8 6.4"/>
          <path d="M8 9 Q8 6.5 10 5.5" opacity="0.35"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">12 · Keep left</span>
      </div>

      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:110px;">
        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 13 V9"/>
          <path d="M8 9 Q8 6 10.5 4.5"/>
          <path d="M8.8 2.8 L10.7 4.3 L9.2 6.4"/>
          <path d="M8 9 Q8 6.5 6 5.5" opacity="0.35"/>
        </svg>
        <span class="mono" style="font-size:.7rem;">13 · Keep right</span>
      </div>

    </div>
  </div>

  <!-- ═══ DISCLOSURE-BEISPIEL MIT ICONS ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Turn-by-Turn im Disclosure-Panel</div>
    <div class="demo-section-desc">
      Reale Kombination Icon + Text + Meta — <code>.disclosure-item-icon</code>
      als erstes Kind in <code>.disclosure-item</code>.
    </div>
    <div class="panel" style="width:320px;">
      <div class="panel-body">
        <details class="disclosure" open>
          <summary class="disclosure-header">
            <span class="disclosure-title">Wegbeschreibung</span>
            <span class="disclosure-count badge badge-gray">4 Schritte</span>
            <i class="fa-solid fa-chevron-down disclosure-chevron"></i>
          </summary>
          <div class="disclosure-body">
            <div class="disclosure-item">
              <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="8" cy="8" r="5" stroke-width="1.3"/>
                <circle cx="8" cy="8" r="2.2" fill="currentColor" stroke="none"/>
              </svg>
              <span class="disclosure-item-text">Head northeast on Untere Donauländer, B129</span>
              <span class="disclosure-item-meta mono">280 m</span>
            </div>
            <div class="disclosure-item">
              <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M8 13 Q8 7 13.4 7"/>
                <path d="M14 4.7 L13.4 7 L11.9 5.2"/>
              </svg>
              <span class="disclosure-item-text">Turn right onto Welser Straße</span>
              <span class="disclosure-item-meta mono">1.2 km</span>
            </div>
            <div class="disclosure-item">
              <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="8" cy="8" r="4"/>
                <path d="M8 14 V12"/>
                <path d="M6 12.5 L8 10.5 L10 12.5"/>
              </svg>
              <span class="disclosure-item-text">Enter roundabout, take 2nd exit</span>
              <span class="disclosure-item-meta mono">150 m</span>
            </div>
            <div class="disclosure-item">
              <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 14.5 V2.5"/>
                <path d="M5 3 L11.5 5.2 L5 7.4 Z" fill="currentColor" stroke="none"/>
              </svg>
              <span class="disclosure-item-text">Arrive at destination</span>
              <span class="disclosure-item-meta mono">0 m</span>
            </div>
          </div>
        </details>
      </div>
    </div>
  </div>

</div>

</body>
</html>
```

- [ ] **Step 2: Validate the HTML is well-formed**

Run:
```bash
grep -c "disclosure-item-icon\|width=\"24\" height=\"24\"" components/maneuver-icons.html
```

Expected: `18` (14 catalog icons + 4 disclosure-example icons).

- [ ] **Step 3: Commit**

```bash
git add components/maneuver-icons.html
git commit -m "feat(maneuver-icons): add reference gallery components/maneuver-icons.html"
```

---

### Task 6: Write `docs/maneuver-icons.md`

**Files:**
- Create: `docs/maneuver-icons.md`

**Interfaces:**
- Consumes: the catalog table and manifest schema from the design spec (`docs/superpowers/specs/2026-07-07-maneuver-icons-design.md`, §3–§6).

- [ ] **Step 1: Write the doc**

`docs/maneuver-icons.md`:
```markdown
# Maneuver-Icons (Turn-by-Turn Richtungssymbole)

**Assets:** `assets/maneuver-icons/`
**Referenz:** `components/maneuver-icons.html`
**Status:** definiert · v1.20.0

---

## Zweck & Abgrenzung

`assets/maneuver-icons/` ist die **Source of Truth für Turn-by-Turn-Richtungssymbole**,
1:1 zu den Manöver-Codes von **OpenRouteService (ORS)**. FontAwesome Free deckt
Navigations-Pfeile (Slight/Sharp-Varianten, Kreisverkehr, Gabelung-Halten) nicht
ausreichend ab — dieses Set schließt die Lücke mit eigenen, monochromen SVGs.

**Bewusst nicht hier:**
- **Kein SDF/MapLibre-Bezug.** Diese Icons sind reine UI-Icons für die
  Sidebar-Liste (inline `<svg>`, `stroke="currentColor"`), keine Karten-Marker.
  Für Karten-Symbole gilt `assets/map-icons/` (`docs/map-icons.md`).
- **Keine Rotation/Spiegelung zur Laufzeit.** Jeder Manöver-Typ ist eine
  eigenständige SVG-Datei.
- **Kein Exit-Nummern-Rendering für Kreisverkehr.** Die Icons zeigen nur
  „rein"/„raus", keine Zahlen-Overlays — Exit-Nummern liefert ORS als Text.

---

## Verzeichnis

```
assets/maneuver-icons/
├── ci-maneuver-turn-left.svg
├── ci-maneuver-turn-right.svg
├── ci-maneuver-sharp-left.svg
├── ci-maneuver-sharp-right.svg
├── ci-maneuver-slight-left.svg
├── ci-maneuver-slight-right.svg
├── ci-maneuver-straight.svg
├── ci-maneuver-roundabout-enter.svg
├── ci-maneuver-roundabout-exit.svg
├── ci-maneuver-uturn.svg
├── ci-maneuver-goal.svg
├── ci-maneuver-depart.svg
├── ci-maneuver-keep-left.svg
├── ci-maneuver-keep-right.svg
└── icons.json                   ← Manifest = ORS-Code-Mapping
```

Das Verzeichnis wird vom Konsistenz-Check **nicht** erfasst (er prüft nur
`css/`, `components/`, `docs/`) — keine Orphan-/Dangling-Fehler für SVGs und
Manifest. Die SVGs werden **nicht** einzeln in `registry.json` gelistet;
`icons.json` ist ihre Registry.

---

## ORS-Code-Katalog

| Code | ORS-Manöver | Icon-ID | Form |
|---|---|---|---|
| 0 | Left | `ci-maneuver-turn-left` | 90°-Pfeil nach links |
| 1 | Right | `ci-maneuver-turn-right` | 90°-Pfeil nach rechts |
| 2 | Sharp left | `ci-maneuver-sharp-left` | ~135°-Pfeil nach links |
| 3 | Sharp right | `ci-maneuver-sharp-right` | ~135°-Pfeil nach rechts |
| 4 | Slight left | `ci-maneuver-slight-left` | ~30–45°-Pfeil nach links |
| 5 | Slight right | `ci-maneuver-slight-right` | ~30–45°-Pfeil nach rechts |
| 6 | Straight | `ci-maneuver-straight` | gerader Pfeil nach oben |
| 7 | Enter roundabout | `ci-maneuver-roundabout-enter` | Kreis, Pfeil von außen hinein |
| 8 | Exit roundabout | `ci-maneuver-roundabout-exit` | Kreis, Pfeil von innen hinaus |
| 9 | U-turn | `ci-maneuver-uturn` | 180°-Haarnadel-Pfeil |
| 10 | Goal | `ci-maneuver-goal` | Ziel-Symbol (Flagge) |
| 11 | Depart | `ci-maneuver-depart` | Start-Symbol (Punkt) |
| 12 | Keep left | `ci-maneuver-keep-left` | Y-Gabelung, linker Ast betont |
| 13 | Keep right | `ci-maneuver-keep-right` | Y-Gabelung, rechter Ast betont |

**Slight vs. Keep:** „Slight" (4/5) ist eine leichte Abbiegung auf eine neue
Straße. „Keep" (12/13) ist eine Gabelung, bei der man auf der aktuellen Spur
bleibt — visuell bewusst unterschiedliche Formen (gebogener Pfeil vs.
Y-Gabelung mit betontem Ast).

---

## Namensschema

- **Icon-ID:** `ci-maneuver-<name>` — fester Präfix, Kollisionsschutz.
- **Dateiname:** identisch zur ID, also `<id>.svg`.
- Neue Icons: immer `ci-maneuver-`-Präfix, keine Unterverzeichnisse.

---

## Stil-Regeln (verbindlich)

Line-Art-Stil, identisch zu bestehenden Custom-Icons in
`topbar.html`/`modal.html` (nicht der SDF-Stil aus `map-icons`):

- **`viewBox="0 0 16 16"`** — festes Raster für alle 14 Icons.
- **`fill="none"`, `stroke="currentColor"`, `stroke-width="1.5"`,
  `stroke-linecap="round"`, `stroke-linejoin="round"`**.
- Ausnahmen mit `fill="currentColor"` nur wo zur Lesbarkeit nötig
  (`ci-maneuver-goal`: Flaggenfläche; `ci-maneuver-depart`: Mittelpunkt).
- Kein eingebettetes Raster, keine `<filter>`, keine `<text>`.
- Jede Datei ist eigenständig — keine Rotation/Spiegelung zur Laufzeit.

---

## Manifest-Schema (`icons.json`)

```json
{
  "version": 1,
  "grid": [16, 16],
  "icons": [
    { "orsCode": 0, "name": "ci-maneuver-turn-left", "file": "ci-maneuver-turn-left.svg", "label": "Left" }
  ]
}
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `orsCode` | ja | Numerischer ORS-Manöver-Code (0–13) — Kopplungsschlüssel |
| `name` | ja | Icon-ID, `ci-maneuver-`-präfixt |
| `file` | ja | Dateiname relativ zu `assets/maneuver-icons/` |
| `label` | ja | Kurzbezeichnung (Englisch, wie ORS-Doku) für Tooltip/Alt-Text |

---

## Einbindung (Konsumenten-Snippet)

```js
const manifest = await fetch('/assets/maneuver-icons/icons.json').then(r => r.json());
const byCode = Object.fromEntries(manifest.icons.map(i => [i.orsCode, i]));

async function iconMarkupFor(orsCode) {
  const icon = byCode[orsCode];
  const svgText = await fetch(`/assets/maneuver-icons/${icon.file}`).then(r => r.text());
  return svgText; // inline einsetzen, NICHT <img src> (sonst kein currentColor-Erben)
}
```

In der Disclosure-Liste (`disclosure.css`):

```html
<div class="disclosure-item">
  <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none"
       stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <!-- ci-maneuver-turn-right Pfad -->
  </svg>
  <span class="disclosure-item-text">Turn right onto Welser Straße</span>
  <span class="disclosure-item-meta mono">1.2 km</span>
</div>
```

`.disclosure-item-icon` setzt `color: var(--text)` — gleiche Gewichtung wie
`.disclosure-item-text`, da das Richtungssymbol navigatorisch relevant ist.

---

## Regeln

1. **Neues Icon:** SVG nach den Stil-Regeln erstellen → in
   `assets/maneuver-icons/` ablegen → Eintrag in `icons.json` ergänzen →
   Galerie `components/maneuver-icons.html` um eine Karte erweitern.
2. **Kein produktiver CSS-Code** außer `.disclosure-item-icon` in
   `disclosure.css` — keine neuen Tokens.
3. **Konsistenz-Check** erfasst `assets/maneuver-icons/` nicht — Änderungen am
   Verzeichnis lösen keinen Check-Fehler aus. Der Check prüft aber
   `docs/maneuver-icons.md` als registrierte Dokumentation.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-07-07 | Initiale Definition. 14 Icons (`v1.20.0`), Manifest mit ORS-Code-Mapping, `.disclosure-item-icon`-Slot. |
```

- [ ] **Step 2: Commit**

```bash
git add docs/maneuver-icons.md
git commit -m "docs(maneuver-icons): add component/asset documentation"
```

---

### Task 7: Register in `docs/registry.json`, update `docs/sidebar.md`, regenerate README

**Files:**
- Modify: `docs/registry.json`
- Modify: `docs/sidebar.md`
- Modify: `README.md` (regenerated, not hand-edited)

**Interfaces:**
- Consumes: `docs/maneuver-icons.md` (Task 6), `components/maneuver-icons.html` (Task 5) — must exist on disk before this task's validation step.

- [ ] **Step 1: Add the registry entry**

In `docs/registry.json`, insert a new entry directly after the existing
`map-icons` entry (currently the last entry, `docs/registry.json:96-98`):

```json
    { "id": "map-icons", "title": "Map-Icons (SDF)", "category": "asset",
      "css": [], "doc": ["map-icons.md"], "html": ["map-icons.html"],
      "note": "SDF-Form-Quellen für MapLibre icon-color; keine produktiven CSS-Klassen" },
    { "id": "maneuver-icons", "title": "Maneuver-Icons (Turn-by-Turn)", "category": "asset",
      "css": [], "doc": ["maneuver-icons.md"], "html": ["maneuver-icons.html"],
      "note": "Line-Art-Richtungssymbole 1:1 zu ORS-Manöver-Codes 0-13; .disclosure-item-icon lebt in disclosure.css" }
  ]
}
```

(i.e. add a comma after the `map-icons` entry's closing `}` and insert the new
entry before the final `]` `}`.)

- [ ] **Step 2: Update the Disclosure structure tree in `docs/sidebar.md`**

Current (`docs/sidebar.md:326-338`):
```
<details class="disclosure">
└── <summary class="disclosure-header">
    ├── .disclosure-title
    ├── .disclosure-count (.badge)
    └── .disclosure-chevron
└── .disclosure-body
    └── .disclosure-item (mehrfach)
        ├── .disclosure-item-text
        └── .disclosure-item-meta
```

Change to:
```
<details class="disclosure">
└── <summary class="disclosure-header">
    ├── .disclosure-title
    ├── .disclosure-count (.badge)
    └── .disclosure-chevron
└── .disclosure-body
    └── .disclosure-item (mehrfach)
        ├── .disclosure-item-icon (optional, siehe docs/maneuver-icons.md)
        ├── .disclosure-item-text
        └── .disclosure-item-meta
```

- [ ] **Step 3: Run the consistency check and regenerate README**

Run:
```bash
python3 scripts/cli/check_consistency.py --write
```

Expected output ends with:
```
  ⚠ Komponente 'coords' hat keine Doku (Dreiklang unvollständig)
  ⚠ Komponente 'utils' hat keine Doku (Dreiklang unvollständig)
  ✔ Manifest und Dateien sind konsistent
```
(The two `coords`/`utils` warnings are pre-existing and unrelated to this
change — do not fix them here. No new warnings or errors should appear.)

- [ ] **Step 4: Confirm README picked up the new files**

Run:
```bash
grep -n "maneuver-icons" README.md
```

Expected: two matches — `components/maneuver-icons.html` and
`docs/maneuver-icons.md` — inside the `AUTOGEN:structure` block.

- [ ] **Step 5: Commit**

```bash
git add docs/registry.json docs/sidebar.md README.md
git commit -m "docs(maneuver-icons): register component, update disclosure tree, regen README"
```

---

### Task 8: Changelog and version tag

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: nothing new — this is the final packaging step for the release started in Tasks 1–7.

- [ ] **Step 1: Add the changelog entry**

At the top of `CHANGELOG.md`, above the current `## v1.19.0 - 2026-07-06` entry:

```markdown
## v1.20.0 - 2026-07-07

### Added
- **Maneuver-Icons (Turn-by-Turn)** — 14 line-art SVG-Richtungssymbole (`ci-maneuver-*`), 1:1 zu OpenRouteService-Manöver-Codes 0–13 (Left/Right/Sharp/Slight/Straight/Roundabout Enter+Exit/U-turn/Goal/Depart/Keep Left+Right). Neues Asset-Verzeichnis `assets/maneuver-icons/` mit `icons.json`-Manifest (ORS-Code-Mapping), Referenz `components/maneuver-icons.html`, Doku `docs/maneuver-icons.md`. Neuer `.disclosure-item-icon`-Slot in `css/disclosure.css` für die Turn-by-Turn-Sidebar-Liste — keine neuen Tokens, reuse `--text`.

---
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): add v1.20.0 entry for maneuver-icons"
```

- [ ] **Step 3: Tag the release**

```bash
git tag -a v1.20.0 -m "Release v1.20.0"
```

(Push the commits and tag only after the user confirms — this pushes to the
shared remote.)

---

## Final manual verification (after all tasks)

- [ ] Open `components/maneuver-icons.html` in a browser (or via the `run`/`verify`
      skill) and visually confirm all 14 icons render as distinct, recognizable
      direction symbols, and that the Disclosure example at the bottom shows
      icon + text + meta aligned in one row per step.
- [ ] Open `components/disclosure.html` and confirm the existing turn-by-turn
      example now shows icons without breaking the ellipsis/wrap behavior on
      the long-text test row.
- [ ] Toggle the browser/OS dark-mode preference and confirm icons still use
      `currentColor` correctly (no hardcoded black/white).

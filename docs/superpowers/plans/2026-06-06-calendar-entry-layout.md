# Calendar Entry Layout & Width Constraint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add overflow constraints to `.calendar`, `.calendar-day`, `.calendar-entry` and introduce a `.calendar-entry--multiline` modifier that stacks time and title vertically.

**Architecture:** Pure CSS — no new tokens, no JavaScript. Two independent changes: (1) width constraints on existing rules, (2) new modifier block after the existing `--continues-*` section. Three files change: `css/calendar.css`, `docs/calendar.md`, `components/calendar.html`.

**Tech Stack:** CSS Custom Properties, plain HTML

---

## File Map

| File | Change |
|---|---|
| `css/calendar.css` | Add `max-width`/`overflow`/`min-width` to existing rules + new `--multiline` block |
| `docs/calendar.md` | New `## Eintrags-Layout` section + Änderungshistorie |
| `components/calendar.html` | New multiline demo section |
| `CHANGELOG.md` | v1.12.0 entry |

---

## Task 1: Width constraints + multiline modifier in calendar.css

**Files:**
- Modify: `css/calendar.css`

- [ ] **Step 1: Add `max-width` and `overflow` to `.calendar`**

  Find the existing `.calendar` rule (lines 13–18):

  ```css
  .calendar {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
  }
  ```

  Replace with:

  ```css
  .calendar {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
    max-width: 100%;
    overflow: hidden;
  }
  ```

- [ ] **Step 2: Add `min-width` and `overflow` to `.calendar-day`**

  Find the existing `.calendar-day` rule (lines 84–93):

  ```css
  .calendar-day {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--btn-radius);
    padding: 6px;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  ```

  Replace with:

  ```css
  .calendar-day {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--btn-radius);
    padding: 6px;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
    overflow: hidden;
  }
  ```

- [ ] **Step 3: Add `max-width` to `.calendar-entry`**

  Find the existing `.calendar-entry` rule (lines 124–135). It currently has `min-width: 0` already. Add `max-width: 100%`:

  ```css
  .calendar-entry {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 3px 6px;
    border-radius: var(--badge-radius);
    border-left: 3px solid;
    font-size: 0.72rem;
    cursor: pointer;
    min-width: 0;
    max-width: 100%;
    transition: filter var(--transition-fast);
  }
  ```

- [ ] **Step 4: Add `--multiline` modifier block**

  After the `/* ─── Mehrtägige Events ─── */` block (after the last `}` of `.calendar-entry--continues-left::before`, around line 212), insert:

  ```css

  /* ─── Mehrzeilen-Layout ─── */

  .calendar-entry--multiline {
    flex-wrap: wrap;
    align-items: flex-start;
  }

  .calendar-entry--multiline .calendar-entry-time {
    flex-basis: 100%;
  }

  .calendar-entry--multiline .calendar-entry-title {
    white-space: normal;
    text-overflow: unset;
    overflow: visible;
  }
  ```

- [ ] **Step 5: Verify no hardcoded color values introduced**

  ```bash
  grep -n "#[0-9a-fA-F]\{3,6\}" /root/git/oe5ith-ci/css/calendar.css
  ```

  Expected: same output as before the changes (no new hex values).

- [ ] **Step 6: Commit**

  ```bash
  git add css/calendar.css
  git commit -m "feat(calendar): add width constraints and --multiline entry modifier"
  ```

---

## Task 2: Update docs/calendar.md

**Files:**
- Modify: `docs/calendar.md`

- [ ] **Step 1: Add `## Eintrags-Layout` section**

  Find the `## Bis zu 2 Einträge pro Tag` section. Insert a new section **before** it:

  ```markdown
  ## Eintrags-Layout

  Jeder `.calendar-entry` ist standardmäßig einzeilig — Zeit und Titel nebeneinander, Titel mit
  Ellipsis bei Überlauf. Mit `.calendar-entry--multiline` wird ein gestapeltes Layout aktiviert.

  | Modifier | Layout | Überlauf |
  |---|---|---|
  | _(kein)_ | Zeit + Titel nebeneinander | Titel abgeschnitten (ellipsis) |
  | `.calendar-entry--multiline` | Zeit Zeile 1, Titel Zeile 2+ | Titel umbricht |

  ```html
  <!-- Mehrzeilen-Eintrag -->
  <div class="calendar-entry calendar-entry--color-1 calendar-entry--multiline"
       role="button" tabindex="0"
       aria-label="Frühdienst, 08:00, Details öffnen">
    <span class="calendar-entry-time">08:00</span>
    <span class="calendar-entry-title">Frühdienst Station 1</span>
  </div>
  ```

  Hinweis: `.calendar-entry--multiline` nicht mit `.calendar-entry--continues-left` /
  `--continues-right` kombinieren — dieses Zusammenspiel ist nicht definiert.

  ---

  ```

- [ ] **Step 2: Update Status und Änderungshistorie**

  - Ändere `**Status:** definiert · v1.2` zu `**Status:** definiert · v1.3`
  - Füge zur Änderungshistorie-Tabelle hinzu:

  ```
  | 2026-06-06 | Breitengrenze (`max-width: 100%`, `overflow: hidden`) auf `.calendar`, `.calendar-day`, `.calendar-entry`. Neuer Modifier `.calendar-entry--multiline` für gestapeltes Layout. |
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add docs/calendar.md
  git commit -m "docs(calendar): document width constraints and --multiline modifier"
  ```

---

## Task 3: Update components/calendar.html + CHANGELOG

**Files:**
- Modify: `components/calendar.html`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add multiline demo section to calendar.html**

  Find the `<!-- ═══ MOBILE SHOW-ALL TOGGLE ═══ -->` section. Insert a new demo section **before** it:

  ```html
  <!-- ═══ EINTRAGS-LAYOUT ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Eintrags-Layout — Default vs. Mehrzeilen</div>
    <div class="demo-section-desc">
      Standard: Zeit + Titel einzeilig, Titel abgeschnitten.
      Mit <code>.calendar-entry--multiline</code>: Zeit Zeile 1, Titel Zeile 2+ (umbricht).
      Nicht mit <code>--continues-left/right</code> kombinieren.
    </div>
    <div style="display:flex; flex-direction:column; gap:6px; max-width:240px">
      <div style="font-size:0.82rem; color:var(--muted)">Default (einzeilig):</div>
      <div class="calendar-entry calendar-entry--color-1" style="pointer-events:none">
        <span class="calendar-entry-time">08:00</span>
        <span class="calendar-entry-title">Frühdienst Station 1 — langer Titel</span>
      </div>
      <div style="font-size:0.82rem; color:var(--muted); margin-top:8px">Mehrzeilen (.--multiline):</div>
      <div class="calendar-entry calendar-entry--color-1 calendar-entry--multiline" style="pointer-events:none">
        <span class="calendar-entry-time">08:00</span>
        <span class="calendar-entry-title">Frühdienst Station 1 — langer Titel</span>
      </div>
    </div>
  </div>
  ```

- [ ] **Step 2: Add CHANGELOG entry**

  In `CHANGELOG.md`, insert before `## v1.11.1`:

  ```markdown
  ## v1.12.0 - 2026-06-06

  ### Added
  - Breitengrenze auf `.calendar` (`max-width: 100%`, `overflow: hidden`), `.calendar-day` (`min-width: 0`, `overflow: hidden`) und `.calendar-entry` (`max-width: 100%`)
  - `.calendar-entry--multiline` Modifier: Zeit auf Zeile 1, Titel umbricht ab Zeile 2

  ---

  ```

- [ ] **Step 3: Commit**

  ```bash
  git add components/calendar.html CHANGELOG.md
  git commit -m "feat(calendar): add multiline entry demo and CHANGELOG v1.12.0"
  ```

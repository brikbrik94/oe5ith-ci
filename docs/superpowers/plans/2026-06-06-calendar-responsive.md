# Calendar Responsive — Mobile Toggle & Tablet Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `.calendar--show-all` modifier class for the mobile show-all toggle and a tablet media query (769px–1024px) with compressed entry styles to `css/calendar.css`, plus update docs and the reference page.

**Architecture:** Pure CSS changes — no new tokens, no JavaScript in the library. The mobile toggle is a CSS modifier class that the consuming website sets via JS. The tablet layout is an automatic media query. Three files change: `css/calendar.css`, `docs/calendar.md`, `components/calendar.html`.

**Tech Stack:** CSS Custom Properties, plain HTML, existing `@media` breakpoint conventions (`max-width: 768px` for mobile, `min-width: 769px) and (max-width: 1024px)` for tablet — both already used in `topbar.css` and `page.css`)

---

## File Map

| File | Change |
|---|---|
| `css/calendar.css` | Add `.calendar--show-all` override inside mobile block + new tablet `@media` block |
| `docs/calendar.md` | Update `## Mobile` section + add `## Tablet` section + Änderungshistorie |
| `components/calendar.html` | Add toggle button to calendar header demo + add toggle demo section |

---

## Task 1: Add show-all modifier and tablet media query to calendar.css

**Files:**
- Modify: `css/calendar.css` (currently ends at line 287 after the mobile `@media` block)

- [ ] **Step 1: Open `css/calendar.css` and locate the mobile media block**

  Find the `@media (max-width: 768px)` block (lines 267–287). It currently looks like:

  ```css
  @media (max-width: 768px) {
    .calendar-grid {
      grid-template-columns: 1fr;
    }

    .calendar-weekday {
      display: none;
    }

    .calendar-day:not(:has(.calendar-entry)) {
      display: none;
    }

    .calendar-day {
      min-height: unset;
    }

    .calendar-day-number {
      font-size: 0.85rem;
    }
  }
  ```

- [ ] **Step 2: Add the show-all override inside the mobile block**

  Add one rule at the end of the existing `@media (max-width: 768px)` block, before the closing `}`:

  ```css
    .calendar.calendar--show-all .calendar-day:not(:has(.calendar-entry)) {
      display: flex;
    }
  ```

  The full mobile block after the edit:

  ```css
  @media (max-width: 768px) {
    .calendar-grid {
      grid-template-columns: 1fr;
    }

    .calendar-weekday {
      display: none;
    }

    .calendar-day:not(:has(.calendar-entry)) {
      display: none;
    }

    .calendar-day {
      min-height: unset;
    }

    .calendar-day-number {
      font-size: 0.85rem;
    }

    .calendar.calendar--show-all .calendar-day:not(:has(.calendar-entry)) {
      display: flex;
    }
  }
  ```

- [ ] **Step 3: Add the tablet media block after the mobile block**

  Append the following at the end of the file, after the closing `}` of the mobile block:

  ```css

  /* ═══════════════════════════════════════
     TABLET (769px–1024px)
     ═══════════════════════════════════════ */

  @media (min-width: 769px) and (max-width: 1024px) {
    .calendar-day {
      padding: 4px;
      min-height: 64px;
    }

    .calendar-day-number {
      font-size: 0.72rem;
    }

    .calendar-entry {
      padding: 2px 4px;
      font-size: 0.68rem;
      gap: 2px;
    }

    .calendar-entry-time {
      max-width: 36px;
      overflow: hidden;
      text-overflow: clip;
      white-space: nowrap;
    }

    .calendar-entry-title {
      font-size: 0.68rem;
    }
  }
  ```

- [ ] **Step 4: Verify no hardcoded color values were introduced**

  ```bash
  grep -n "#[0-9a-fA-F]\{3,6\}" /root/git/oe5ith-ci/css/calendar.css
  ```

  Expected: same output as before (no new hex values).

- [ ] **Step 5: Commit**

  ```bash
  git add css/calendar.css
  git commit -m "feat(calendar): add show-all mobile modifier and tablet media query"
  ```

---

## Task 2: Update docs/calendar.md

**Files:**
- Modify: `docs/calendar.md`

- [ ] **Step 1: Replace the `## Mobile (≤768px)` section**

  Find the current section (around line 184):

  ```markdown
  ## Mobile (≤768px)

  Das 7-Spalten-Grid kollabiert zu einer einspaltigen Liste.
  Wochentag-Header werden ausgeblendet.
  Leere Tageszellen (keine Einträge) werden ausgeblendet.

  Hinweis: Mobile-Collapse verwendet `:has()` — benötigt einen modernen Browser (Baseline 2023).
  ```

  Replace it with:

  ```markdown
  ## Mobile (≤768px)

  Das 7-Spalten-Grid kollabiert zu einer einspaltigen Liste.
  Wochentag-Header werden ausgeblendet.

  ### Leere Tageszellen — Toggle

  Standardmäßig werden leere Tageszellen (keine Einträge) ausgeblendet. Mit dem Modifier
  `.calendar--show-all` auf `.calendar` werden alle Tageszellen angezeigt.

  | Zustand | Klasse | Leere Tage |
  |---|---|---|
  | Kompakt (Standard) | _(kein Modifier)_ | ausgeblendet |
  | Alle anzeigen | `.calendar--show-all` | sichtbar |

  Die CI definiert die CSS-Klasse. Die Website setzt/entfernt sie per JavaScript nach eigenem Ermessen.

  ```html
  <!-- Alle Tage anzeigen -->
  <div class="calendar calendar--show-all">…</div>

  <!-- Nur Tage mit Einträgen (Standard) -->
  <div class="calendar">…</div>
  ```

  Hinweis: Mobile-Collapse verwendet `:has()` — benötigt einen modernen Browser (Baseline 2023).
  ```

- [ ] **Step 2: Add `## Tablet (769px–1024px)` section after `## Mobile`**

  After the replaced Mobile section (and its `---` separator), insert:

  ```markdown
  ## Tablet (769px–1024px)

  Das 7-Spalten-Grid bleibt erhalten. Eintragsinhalt wird automatisch komprimiert — kein
  JavaScript, keine zusätzlichen Klassen erforderlich.

  | Element | Desktop | Tablet |
  |---|---|---|
  | Tageszell-Padding | 6px | 4px |
  | Min-Height Zelle | 80px | 64px |
  | Entry-Schriftgröße | 0.72rem | 0.68rem |
  | Uhrzeit | vollständig | nur Startzeit (max. 36px, abgeschnitten) |

  Für Detailinformationen (vollständige Zeit, Beschreibung, Ort) öffnet der Nutzer das Modal.
  ```

- [ ] **Step 3: Update Änderungshistorie**

  Append to the table:

  ```markdown
  | 2026-06-06 | Mobile Show-All-Toggle (`.calendar--show-all`). Tablet-Breakpoint 769px–1024px mit komprimierter Darstellung. |
  ```

- [ ] **Step 4: Update Status**

  Change `**Status:** definiert · v1.1` to `**Status:** definiert · v1.2`

- [ ] **Step 5: Commit**

  ```bash
  git add docs/calendar.md
  git commit -m "docs(calendar): document mobile show-all toggle and tablet breakpoint"
  ```

---

## Task 3: Update components/calendar.html

**Files:**
- Modify: `components/calendar.html`

- [ ] **Step 1: Add toggle button to calendar header**

  Find the calendar header in the main demo (around line 64–73):

  ```html
  <div class="calendar-header">
    <button class="calendar-nav-btn calendar-prev" aria-label="Vorheriger Monat">
      <i class="fa-solid fa-chevron-left"></i>
    </button>
    <span class="calendar-title">Juni 2026</span>
    <button class="calendar-nav-btn calendar-next" aria-label="Nächster Monat">
      <i class="fa-solid fa-chevron-right"></i>
    </button>
    <button class="btn btn-secondary" style="margin-left:8px; height:32px; padding:0 12px; font-size:0.8rem">Heute</button>
  </div>
  ```

  Add a toggle button after the Heute-Button:

  ```html
  <div class="calendar-header">
    <button class="calendar-nav-btn calendar-prev" aria-label="Vorheriger Monat">
      <i class="fa-solid fa-chevron-left"></i>
    </button>
    <span class="calendar-title">Juni 2026</span>
    <button class="calendar-nav-btn calendar-next" aria-label="Nächster Monat">
      <i class="fa-solid fa-chevron-right"></i>
    </button>
    <button class="btn btn-secondary" style="margin-left:8px; height:32px; padding:0 12px; font-size:0.8rem">Heute</button>
    <button class="btn btn-secondary" id="cal-toggle-btn" style="height:32px; padding:0 12px; font-size:0.8rem" onclick="toggleCalShowAll()">Alle Tage</button>
  </div>
  ```

- [ ] **Step 2: Add the toggleCalShowAll JS function**

  Find the `<script>` block at the bottom of the file. Add the following function before the existing `openCalModal` function:

  ```js
  /* ── Show-All Toggle ── */
  function toggleCalShowAll() {
    const cal = document.querySelector('.calendar');
    const btn = document.getElementById('cal-toggle-btn');
    const active = cal.classList.toggle('calendar--show-all');
    btn.textContent = active ? 'Nur mit Termin' : 'Alle Tage';
  }
  ```

- [ ] **Step 3: Add demo section for the show-all toggle**

  After the existing Monatskalender demo-section (after its closing `</div><!-- /.demo-section -->`), add:

  ```html
  <!-- ═══ MOBILE SHOW-ALL TOGGLE ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Mobile — Show-All-Toggle</div>
    <div class="demo-section-desc">
      Auf Mobile (≤768px) werden leere Tage standardmäßig ausgeblendet.
      Mit <code>.calendar--show-all</code> auf <code>.calendar</code> werden alle Tage angezeigt.
      Die Klasse wird von der Website per JS gesetzt — der Button oben im Monatskalender
      demonstriert dieses Verhalten (nur auf Mobile sichtbar wirksam).
    </div>
    <div style="display:flex; flex-direction:column; gap:6px; max-width:500px">
      <div style="font-size:0.82rem; color:var(--muted)">Standard (kompakt):</div>
      <code style="font-size:0.8rem; color:var(--text)">&lt;div class="calendar"&gt;</code>
      <div style="font-size:0.82rem; color:var(--muted); margin-top:8px">Alle Tage sichtbar:</div>
      <code style="font-size:0.8rem; color:var(--text)">&lt;div class="calendar calendar--show-all"&gt;</code>
    </div>
  </div>
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add components/calendar.html
  git commit -m "feat(calendar): add show-all toggle demo to reference page"
  ```

---

## Task 4: Update CHANGELOG.md

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add v1.12.0 entry**

  Open `CHANGELOG.md`. After the header and `---` separator, add a new entry before the existing `## v1.11.0` entry:

  ```markdown
  ## v1.12.0 - 2026-06-06

  ### Added
  - `.calendar--show-all` Modifier-Klasse für Mobile: zeigt alle Tageszellen inkl. leerer
  - Tablet-Breakpoint (769px–1024px) mit komprimierter Eintragsdarstellung in `css/calendar.css`

  ---

  ```

- [ ] **Step 2: Commit**

  ```bash
  git add CHANGELOG.md
  git commit -m "chore: update CHANGELOG for v1.12.0 — calendar responsive improvements"
  ```

# Calendar Colors & Multi-Day Events — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 10 generic calendar color slots to `common.css`, replace semantic entry modifier classes in `calendar.css` with generic ones (keeping aliases), and add continuation markers for multi-day events.

**Architecture:** Pure CSS/HTML — no build step, no test framework. "Tests" are visual checks in the browser via `components/calendar.html`. Each task produces a committed change. Tasks 1–3 touch CSS only; Tasks 4–5 update docs; Task 6 updates the reference page.

**Tech Stack:** CSS Custom Properties, plain HTML, Font Awesome 6 icons (already loaded in reference page)

---

## File Map

| File | Change |
|---|---|
| `css/common.css` | Add 30 `--cal-color-N` tokens in `:root` after the semantics block |
| `css/calendar.css` | Replace 4 semantic modifier classes → 10 generic + 4 aliases + 2 continuation classes |
| `docs/tokens.md` | New section "Kalender-Farbslots", update Änderungshistorie |
| `docs/calendar.md` | Update Eintragstypen table, add Mehrtägige Events section, update Änderungshistorie |
| `components/calendar.html` | Update Eintragstypen demo section, add Mehrtägige Events demo section |

---

## Task 1: Add cal-color tokens to common.css

**Files:**
- Modify: `css/common.css` (lines 36–51 — after `--auth-border` in the Semantisch block)

- [ ] **Step 1: Open `css/common.css` and locate the semantics block**

  Find the line `--auth-border: rgba(139,92,246,0.25);` — this is line ~51. The new token block goes directly after it, before the `/* ── FARBEN: Code / Terminal ── */` comment.

- [ ] **Step 2: Insert the 30 cal-color tokens**

  Add the following block after `--auth-border`:

  ```css
    /* ── FARBEN: Kalender-Farbslots (pro Website frei belegbar) ── */
    --cal-color-1:         #22c55e;
    --cal-color-1-subtle:  rgba(34, 197, 94, 0.10);
    --cal-color-1-border:  rgba(34, 197, 94, 0.25);

    --cal-color-2:         #eab308;
    --cal-color-2-subtle:  rgba(234, 179, 8, 0.10);
    --cal-color-2-border:  rgba(234, 179, 8, 0.25);

    --cal-color-3:         #a78bfa;
    --cal-color-3-subtle:  rgba(167, 139, 250, 0.10);
    --cal-color-3-border:  rgba(167, 139, 250, 0.25);

    --cal-color-4:         #3b82f6;
    --cal-color-4-subtle:  rgba(59, 130, 246, 0.07);
    --cal-color-4-border:  rgba(59, 130, 246, 0.25);

    --cal-color-5:         #f97316;
    --cal-color-5-subtle:  rgba(249, 115, 22, 0.10);
    --cal-color-5-border:  rgba(249, 115, 22, 0.25);

    --cal-color-6:         #ef4444;
    --cal-color-6-subtle:  rgba(239, 68, 68, 0.10);
    --cal-color-6-border:  rgba(239, 68, 68, 0.25);

    --cal-color-7:         #06b6d4;
    --cal-color-7-subtle:  rgba(6, 182, 212, 0.10);
    --cal-color-7-border:  rgba(6, 182, 212, 0.25);

    --cal-color-8:         #ec4899;
    --cal-color-8-subtle:  rgba(236, 72, 153, 0.10);
    --cal-color-8-border:  rgba(236, 72, 153, 0.25);

    --cal-color-9:         #84cc16;
    --cal-color-9-subtle:  rgba(132, 204, 22, 0.10);
    --cal-color-9-border:  rgba(132, 204, 22, 0.25);

    --cal-color-10:        #94a3b8;
    --cal-color-10-subtle: rgba(148, 163, 184, 0.10);
    --cal-color-10-border: rgba(148, 163, 184, 0.25);
  ```

- [ ] **Step 3: Visual check**

  Open `components/calendar.html` in a browser. Existing entries should still look exactly the same (tokens not yet used by calendar.css — that comes in Task 2). No visual change expected yet.

- [ ] **Step 4: Commit**

  ```bash
  git add css/common.css
  git commit -m "feat(tokens): add 10 cal-color token triplets for generic calendar coloring"
  ```

---

## Task 2: Replace semantic modifier classes with generic + aliases in calendar.css

**Files:**
- Modify: `css/calendar.css` (lines 168–188 — the `/* ─── Diensttyp-Modifier ─── */` block)

- [ ] **Step 1: Replace the entire Diensttyp-Modifier block**

  Find and replace the existing block (from the `/* ─── Diensttyp-Modifier ─── */` comment through `.calendar-entry--default { ... }`) with the following:

  ```css
  /* ─── Generische Farbslots (color-1 … color-10) ─── */

  .calendar-entry--color-1  { background: var(--cal-color-1-subtle);  border-color: var(--cal-color-1); }
  .calendar-entry--color-2  { background: var(--cal-color-2-subtle);  border-color: var(--cal-color-2); }
  .calendar-entry--color-3  { background: var(--cal-color-3-subtle);  border-color: var(--cal-color-3); }
  .calendar-entry--color-4  { background: var(--cal-color-4-subtle);  border-color: var(--cal-color-4); }
  .calendar-entry--color-5  { background: var(--cal-color-5-subtle);  border-color: var(--cal-color-5); }
  .calendar-entry--color-6  { background: var(--cal-color-6-subtle);  border-color: var(--cal-color-6); }
  .calendar-entry--color-7  { background: var(--cal-color-7-subtle);  border-color: var(--cal-color-7); }
  .calendar-entry--color-8  { background: var(--cal-color-8-subtle);  border-color: var(--cal-color-8); }
  .calendar-entry--color-9  { background: var(--cal-color-9-subtle);  border-color: var(--cal-color-9); }
  .calendar-entry--color-10 { background: var(--cal-color-10-subtle); border-color: var(--cal-color-10); }

  /* ─── Aliase (rückwärtskompatibel — können später entfernt werden) ─── */

  .calendar-entry--early   { background: var(--cal-color-1-subtle);  border-color: var(--cal-color-1); }
  .calendar-entry--late    { background: var(--cal-color-2-subtle);  border-color: var(--cal-color-2); }
  .calendar-entry--night   { background: var(--cal-color-3-subtle);  border-color: var(--cal-color-3); }
  .calendar-entry--default { background: var(--cal-color-4-subtle);  border-color: var(--cal-color-4); }
  ```

- [ ] **Step 2: Visual check**

  Open `components/calendar.html` in a browser. All existing entries (early=grün, late=gelb, night=violett, default=blau) müssen identisch aussehen wie vorher — die Alias-Klassen zeigen jetzt auf die neuen Cal-Color-Tokens, die aber dieselben Farbwerte haben.

- [ ] **Step 3: Commit**

  ```bash
  git add css/calendar.css
  git commit -m "feat(calendar): replace semantic entry modifiers with generic color-1..10 + aliases"
  ```

---

## Task 3: Add multi-day continuation classes to calendar.css

**Files:**
- Modify: `css/calendar.css` — new section after the aliases block, before the Modal-Inhalt section

- [ ] **Step 1: Insert the continuation CSS block**

  After the aliases block and before the `/* ═══ MODAL-INHALT ═══ */` comment, insert:

  ```css
  /* ─── Mehrtägige Events ─── */

  .calendar-entry--continues-right::after {
    content: "›";
    margin-left: auto;
    flex-shrink: 0;
    color: var(--muted);
    font-size: 0.8rem;
    line-height: 1;
  }

  .calendar-entry--continues-left {
    border-left-color: transparent;
  }

  .calendar-entry--continues-left::before {
    content: "‹";
    flex-shrink: 0;
    color: var(--muted);
    font-size: 0.8rem;
    line-height: 1;
  }
  ```

- [ ] **Step 2: Visual check**

  Open `components/calendar.html` in a browser. Keine Änderung an bestehenden Einträgen erwartet — die neuen Klassen sind noch nicht im HTML verwendet.

- [ ] **Step 3: Commit**

  ```bash
  git add css/calendar.css
  git commit -m "feat(calendar): add continues-left/right modifier classes for multi-day events"
  ```

---

## Task 4: Update docs/tokens.md

**Files:**
- Modify: `docs/tokens.md`

- [ ] **Step 1: Add the Kalender-Farbslots section**

  After the `## Semantische Farben` section (after the 4-row table), insert a new section:

  ```markdown
  ---

  ## Kalender-Farbslots

  10 nummerierte Farbslots für die Kalender-Komponente. Standardwerte sind in `css/common.css`
  definiert — jede Website kann einzelne Slots per `:root { --cal-color-N: … }` überschreiben.

  Jeder Slot hat drei Varianten: Vollton, Subtle (Hintergrund ~10%), Border (~25%).

  | Slot | Vollton | Farbe | Subtle | Border |
  |---|---|---|---|---|
  | `--cal-color-1` | `#22c55e` | grün | `rgba(34,197,94,0.10)` | `rgba(34,197,94,0.25)` |
  | `--cal-color-2` | `#eab308` | gelb | `rgba(234,179,8,0.10)` | `rgba(234,179,8,0.25)` |
  | `--cal-color-3` | `#a78bfa` | violett | `rgba(167,139,250,0.10)` | `rgba(167,139,250,0.25)` |
  | `--cal-color-4` | `#3b82f6` | blau | `rgba(59,130,246,0.07)` | `rgba(59,130,246,0.25)` |
  | `--cal-color-5` | `#f97316` | orange | `rgba(249,115,22,0.10)` | `rgba(249,115,22,0.25)` |
  | `--cal-color-6` | `#ef4444` | rot | `rgba(239,68,68,0.10)` | `rgba(239,68,68,0.25)` |
  | `--cal-color-7` | `#06b6d4` | cyan | `rgba(6,182,212,0.10)` | `rgba(6,182,212,0.25)` |
  | `--cal-color-8` | `#ec4899` | pink | `rgba(236,72,153,0.10)` | `rgba(236,72,153,0.25)` |
  | `--cal-color-9` | `#84cc16` | limette | `rgba(132,204,22,0.10)` | `rgba(132,204,22,0.25)` |
  | `--cal-color-10` | `#94a3b8` | grau | `rgba(148,163,184,0.10)` | `rgba(148,163,184,0.25)` |

  **Überschreiben auf Website-Ebene:**
  ```css
  :root {
    --cal-color-1:        #e11d48;
    --cal-color-1-subtle: rgba(225, 29, 72, 0.10);
    --cal-color-1-border: rgba(225, 29, 72, 0.25);
  }
  ```
  ```

- [ ] **Step 2: Add entry to Änderungshistorie**

  Append to the existing `## Änderungshistorie` table:

  ```markdown
  | 2026-06-06 | 10 Kalender-Farbslots (`--cal-color-1` bis `--cal-color-10`) mit Subtle- und Border-Varianten ergänzt. |
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add docs/tokens.md
  git commit -m "docs(tokens): document cal-color-1..10 token slots"
  ```

---

## Task 5: Update docs/calendar.md

**Files:**
- Modify: `docs/calendar.md`

- [ ] **Step 1: Replace the Eintragstypen section**

  Find the `## Eintragstypen` section and replace the entire table + surrounding text with:

  ```markdown
  ## Generische Farbslots

  | Modifier-Klasse | Token-Paar |
  |---|---|
  | `.calendar-entry--color-1` | `--cal-color-1-subtle` / `--cal-color-1` |
  | `.calendar-entry--color-2` | `--cal-color-2-subtle` / `--cal-color-2` |
  | `.calendar-entry--color-3` | `--cal-color-3-subtle` / `--cal-color-3` |
  | `.calendar-entry--color-4` | `--cal-color-4-subtle` / `--cal-color-4` |
  | `.calendar-entry--color-5` | `--cal-color-5-subtle` / `--cal-color-5` |
  | `.calendar-entry--color-6` | `--cal-color-6-subtle` / `--cal-color-6` |
  | `.calendar-entry--color-7` | `--cal-color-7-subtle` / `--cal-color-7` |
  | `.calendar-entry--color-8` | `--cal-color-8-subtle` / `--cal-color-8` |
  | `.calendar-entry--color-9` | `--cal-color-9-subtle` / `--cal-color-9` |
  | `.calendar-entry--color-10` | `--cal-color-10-subtle` / `--cal-color-10` |

  Die Standardfarben (grün, gelb, violett, blau, orange, rot, cyan, pink, limette, grau)
  können pro Website überschrieben werden — siehe `docs/tokens.md`.

  ### Aliase (rückwärtskompatibel)

  | Alias-Klasse | Entspricht |
  |---|---|
  | `.calendar-entry--early` | `--color-1` (grün) |
  | `.calendar-entry--late` | `--color-2` (gelb) |
  | `.calendar-entry--night` | `--color-3` (violett) |
  | `.calendar-entry--default` | `--color-4` (blau) |

  Neue Diensttypen als `--color-N`-Klasse ergänzen — Aliase nicht für neue Typen verwenden.
  ```

- [ ] **Step 2: Add Mehrtägige Events section**

  After the `## Änderungsindikator` section, insert:

  ```markdown
  ## Mehrtägige Events

  Events die sich über mehrere Tage erstrecken, erscheinen in jeder Tageszelle einzeln.
  Zwei Modifier-Klassen steuern die Fortsetzungsmarkierungen:

  | Klasse | Bedeutung | Visuell |
  |---|---|---|
  | `.calendar-entry--continues-right` | Event geht am Folgetag weiter | `›` rechts via `::after` |
  | `.calendar-entry--continues-left` | Event kommt vom Vortag | `‹` links via `::before`, `border-left` transparent |

  Kombinierbar: Ein mittlerer Tag trägt beide Klassen.

  ```html
  <!-- Tag 1: Starttag — zeigt Uhrzeit -->
  <div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-right"
       role="button" tabindex="0"
       aria-label="Konferenz, 08:00, läuft weiter, Details öffnen">
    <span class="calendar-entry-time">08:00</span>
    <span class="calendar-entry-title">Konferenz</span>
  </div>

  <!-- Tag 2: Mitteltag — keine Uhrzeit -->
  <div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-left calendar-entry--continues-right"
       role="button" tabindex="0"
       aria-label="Konferenz, Fortsetzung, Details öffnen">
    <span class="calendar-entry-title">Konferenz</span>
  </div>

  <!-- Tag 3: Endtag — keine Uhrzeit -->
  <div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-left"
       role="button" tabindex="0"
       aria-label="Konferenz, Fortsetzung, Details öffnen">
    <span class="calendar-entry-title">Konferenz</span>
  </div>
  ```

  **Uhrzeit-Regel:** Nur der Starttag enthält `.calendar-entry-time` im DOM.
  Folgetage lassen das Element weg.
  ```

- [ ] **Step 3: Update Status and Änderungshistorie**

  - Change `**Status:** definiert · v1.0` to `**Status:** definiert · v1.1`
  - Append to Änderungshistorie table:

  ```markdown
  | 2026-06-06 | Generische Farbslots `--color-1` bis `--color-10`. Aliase für bestehende Diensttypen. Mehrtägige Events mit `--continues-left` / `--continues-right`. |
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/calendar.md
  git commit -m "docs(calendar): document generic color slots, aliases, and multi-day event markers"
  ```

---

## Task 6: Update components/calendar.html

**Files:**
- Modify: `components/calendar.html`

- [ ] **Step 1: Replace the Eintragstypen demo section**

  Find the `<!-- ═══ EINTRAGSTYPEN ═══ -->` section (from the comment through the closing `</div><!-- /.demo-section -->`). Replace the inner `<div style="display:flex; ...">` block (the list of entries) with a version that shows all 10 generic colors plus the 4 aliases:

  ```html
  <div class="demo-section">
    <div class="demo-section-title">Generische Farbslots — color-1 bis color-10</div>
    <div class="demo-section-desc">
      10 nummerierte Farbslots. Pro Website via <code>--cal-color-N</code> Token in
      <code>common.css</code> überschreibbar. Die 4 Alias-Klassen
      (<code>--early</code>, <code>--late</code>, <code>--night</code>, <code>--default</code>)
      sind rückwärtskompatibel und zeigen auf color-1..4.
    </div>
    <div style="display:flex; flex-direction:column; gap:6px; max-width:340px">
      <div class="calendar-entry calendar-entry--color-1" style="pointer-events:none">
        <span class="calendar-entry-title">color-1 — grün (#22c55e)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-2" style="pointer-events:none">
        <span class="calendar-entry-title">color-2 — gelb (#eab308)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-3" style="pointer-events:none">
        <span class="calendar-entry-title">color-3 — violett (#a78bfa)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-4" style="pointer-events:none">
        <span class="calendar-entry-title">color-4 — blau (#3b82f6)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-5" style="pointer-events:none">
        <span class="calendar-entry-title">color-5 — orange (#f97316)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-6" style="pointer-events:none">
        <span class="calendar-entry-title">color-6 — rot (#ef4444)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-7" style="pointer-events:none">
        <span class="calendar-entry-title">color-7 — cyan (#06b6d4)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-8" style="pointer-events:none">
        <span class="calendar-entry-title">color-8 — pink (#ec4899)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-9" style="pointer-events:none">
        <span class="calendar-entry-title">color-9 — limette (#84cc16)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-10" style="pointer-events:none">
        <span class="calendar-entry-title">color-10 — grau (#94a3b8)</span>
      </div>
    </div>

    <div class="demo-section-desc" style="margin-top:16px">Aliase (rückwärtskompatibel):</div>
    <div style="display:flex; flex-direction:column; gap:6px; max-width:340px">
      <div class="calendar-entry calendar-entry--early" style="pointer-events:none">
        <span class="calendar-entry-time">06:00 – 14:00</span>
        <span class="calendar-entry-title">Frühdienst (.--early → color-1)</span>
      </div>
      <div class="calendar-entry calendar-entry--late" style="pointer-events:none">
        <span class="calendar-entry-time">14:00 – 22:00</span>
        <span class="calendar-entry-title">Spätdienst (.--late → color-2)</span>
      </div>
      <div class="calendar-entry calendar-entry--night" style="pointer-events:none">
        <span class="calendar-entry-time">20:00 – 08:00</span>
        <span class="calendar-entry-title">Nachtdienst (.--night → color-3)</span>
      </div>
      <div class="calendar-entry calendar-entry--default" style="pointer-events:none">
        <span class="calendar-entry-time">08:00 – 16:00</span>
        <span class="calendar-entry-title">Sonstiges (.--default → color-4)</span>
      </div>
    </div>
  </div>
  ```

- [ ] **Step 2: Add Mehrtägige Events demo section**

  After the Eintragstypen section, add:

  ```html
  <!-- ═══ MEHRTÄGIGE EVENTS ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Mehrtägige Events — Fortsetzungsmarkierungen</div>
    <div class="demo-section-desc">
      Events über mehrere Tage werden in jeder Tageszelle einzeln gezeigt.
      <code>.--continues-right</code> zeigt <code>›</code> rechts,
      <code>.--continues-left</code> zeigt <code>‹</code> links und blendet den
      linken Balken aus. Nur der Starttag zeigt die Uhrzeit.
    </div>
    <div style="display:flex; flex-direction:column; gap:6px; max-width:340px">
      <div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-right" style="pointer-events:none">
        <span class="calendar-entry-time">08:00</span>
        <span class="calendar-entry-title">Konferenz (Tag 1 — Start)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-left calendar-entry--continues-right" style="pointer-events:none">
        <span class="calendar-entry-title">Konferenz (Tag 2 — Mitte)</span>
      </div>
      <div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-left" style="pointer-events:none">
        <span class="calendar-entry-title">Konferenz (Tag 3 — Ende)</span>
      </div>
    </div>
  </div>
  ```

- [ ] **Step 3: Visual check**

  Open `components/calendar.html` in a browser und prüfen:
  - Alle 10 Farbslots werden korrekt dargestellt
  - Die 4 Aliase sehen identisch zu color-1..4 aus
  - Das 3-Tage-Event zeigt `›` am Start, `‹›` in der Mitte, `‹` am Ende
  - Der linke Balken bei `--continues-left` ist transparent (kein grüner Streifen links)
  - Bestehendes Monatsraster (alle `--early`/`--late`/`--night`/`--default`-Einträge) sieht unverändert aus

- [ ] **Step 4: Commit**

  ```bash
  git add components/calendar.html
  git commit -m "feat(calendar): update reference page — generic color slots and multi-day event demo"
  ```

---

## Task 7: Final check and version tag

- [ ] **Step 1: Open `components/calendar.html` in browser — full visual review**

  Prüfliste:
  - [ ] Monatsraster: bestehende Einträge (early/late/night/default) sehen identisch aus
  - [ ] Farbslot-Demo: alle 10 Farben sichtbar und korrekt
  - [ ] Alias-Demo: early=grün, late=gelb, night=violett, default=blau
  - [ ] Mehrtage-Demo: Pfeil-Markierungen korrekt, transparenter linker Rand bei continues-left
  - [ ] Keine unbeabsichtigten CSS-Auswirkungen auf andere Elemente (z.B. Modal, Header)

- [ ] **Step 2: Confirm no hardcoded values were introduced**

  ```bash
  grep -n "#[0-9a-fA-F]\{3,6\}" css/calendar.css
  ```

  Expected output: empty (keine Hex-Werte direkt in calendar.css — alle über Tokens).

- [ ] **Step 3: Update CHANGELOG.md**

  Unter dem `[Unreleased]`-Block (oder neuen `[1.2.0]`-Block) eintragen:

  ```markdown
  ## [1.2.0] — 2026-06-06

  ### Added
  - 10 generische Kalender-Farbslots (`--cal-color-1` bis `--cal-color-10`) mit Subtle- und Border-Varianten in `common.css`
  - `.calendar-entry--color-1` bis `--color-10` Modifier-Klassen in `calendar.css`
  - `.calendar-entry--continues-left` und `--continues-right` für mehrtägige Events
  - Rückwärtskompatible Aliase (`--early`, `--late`, `--night`, `--default`) auf die neuen Slots
  ```

- [ ] **Step 4: Commit CHANGELOG**

  ```bash
  git add CHANGELOG.md
  git commit -m "chore: update CHANGELOG for v1.2.0 — calendar color slots and multi-day events"
  ```

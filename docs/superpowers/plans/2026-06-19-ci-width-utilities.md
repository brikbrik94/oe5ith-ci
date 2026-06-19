# CI-Breiten-Utilities Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fehlende Breiten-Utility-Klassen (`.col-w-*`, `.max-w-300`) als CI-konforme Utilities in `oe5ith-ci` aufnehmen, dokumentiert über die Referenz-Demo.

**Architecture:** Die Klassen kommen in `css/utils.css` (zuständig für zweckgebundene Utilities). Die Doku erfolgt — wie bei allen Utilities — ausschließlich über die Referenz-Demo `components/utils.html`; es gibt keine eigene Spec-Doc (Registry-Eintrag `utils` = „ohne eigene Spec"). Abschluss: additiver MINOR-Release-Eintrag im CHANGELOG und grüner Consistency-Check.

**Tech Stack:** Vanilla CSS mit CI-Token-System, statische HTML-Referenzseiten, kein Build-Step. Verifikation per `grep`, `python3 scripts/cli/check_consistency.py` und visueller Browser-Prüfung (kein Test-Runner im Repo).

## Global Constraints

- Nie Werte hardcoden außer wo kein Token passt — Breiten sind Einzelwerte ohne Token; harte px erlaubt (Präzedenz `.p-2rem`).
- Keine neuen Dateien, keine Pfad-/Strukturänderungen.
- `css/common.css` bleibt Single Source of Truth; `css/demo.css` nie produktiv (nur in `components/`).
- Klassennamen exakt: `.col-w-80`, `.col-w-100`, `.col-w-120`, `.col-w-180`, `.max-w-300`.
- Spec: `docs/superpowers/specs/2026-06-19-ci-width-utilities-design.md`.

---

### Task 1: Breiten-Utilities in `css/utils.css`

**Files:**
- Modify: `css/utils.css` (nach der `FLEX EXTENSIONS`-Sektion, vor `TABLE UTILITIES`)

**Interfaces:**
- Produces: CSS-Klassen `.col-w-80`, `.col-w-100`, `.col-w-120`, `.col-w-180`, `.max-w-300` — von Task 2 (Demo) und website-v3 konsumiert.

- [ ] **Step 1: Sektionen einfügen**

In `css/utils.css` direkt nach der Zeile `.gap-4             { gap: 4px; }` (Ende der FLEX-EXTENSIONS-Sektion) einfügen:

```css

/* ═══════════════════════════════════════
   WIDTH UTILITIES (feste Spaltenbreiten)
   ═══════════════════════════════════════ */

.col-w-80  { width: 80px; }
.col-w-100 { width: 100px; }
.col-w-120 { width: 120px; }
.col-w-180 { width: 180px; }

/* ═══════════════════════════════════════
   MAX-WIDTH UTILITIES
   ═══════════════════════════════════════ */

.max-w-300 { max-width: 300px; }
```

- [ ] **Step 2: Verifizieren, dass alle 5 Klassen vorhanden sind**

Run: `grep -cE '\.col-w-(80|100|120|180)|\.max-w-300' css/utils.css`
Expected: `5`

- [ ] **Step 3: Commit**

```bash
git add css/utils.css
git commit -m "feat(utils): add fixed column-width and max-width utilities"
```

---

### Task 2: Referenz-Demo in `components/utils.html`

**Files:**
- Modify: `components/utils.html` (neue Demo-Sektion vor `</body>`)

**Interfaces:**
- Consumes: `.col-w-*`, `.max-w-300` aus Task 1 (wirksam über das bereits eingebundene `../css/utils.css`).

- [ ] **Step 1: Demo-Sektion direkt vor `</body>` einfügen**

Hinweis: `components/utils.html` lädt `../css/utils.css` bereits ein (Zeile 8) — die neuen Klassen wirken ohne zusätzliches Inline-CSS. Sektion vor `</body>` (Zeile 212) einfügen:

```html
<!-- WIDTH UTILITIES -->
<div class="section">
  <div class="section-label">.col-w-80 / .col-w-100 / .col-w-120 / .col-w-180</div>
  <div class="section-desc">Feste Spaltenbreiten für Tabellen-<code>&lt;th&gt;</code> (Timestamp-, ID-, Baud-Spalten o.ä.). Setzen nur <code>width</code> in Pixel. Die letzte Spalte ohne Klasse füllt den Rest.</div>
  <div class="demo-box">
    <table class="border-collapse" style="width:100%; font-size:0.8rem;">
      <thead>
        <tr style="border-bottom:1px solid var(--border);">
          <th class="col-w-80"  style="padding:6px 8px; text-align:left; color:var(--muted);">.col-w-80</th>
          <th class="col-w-100" style="padding:6px 8px; text-align:left; color:var(--muted);">.col-w-100</th>
          <th class="col-w-120" style="padding:6px 8px; text-align:left; color:var(--muted);">.col-w-120</th>
          <th class="col-w-180" style="padding:6px 8px; text-align:left; color:var(--muted);">.col-w-180</th>
          <th style="padding:6px 8px; text-align:left; color:var(--muted);">Auto (Rest)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:6px 8px; color:var(--text);">80px</td>
          <td style="padding:6px 8px; color:var(--text);">100px</td>
          <td style="padding:6px 8px; color:var(--text);">120px</td>
          <td style="padding:6px 8px; color:var(--text);">180px</td>
          <td style="padding:6px 8px; color:var(--text);">füllt den verbleibenden Platz</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- MAX-WIDTH UTILITIES -->
<div class="section">
  <div class="section-label">.max-w-300</div>
  <div class="section-desc">Begrenzt die maximale Breite eines Containers oder Selects auf 300px. Element bleibt darunter flexibel schmaler.</div>
  <div class="demo-box" style="flex-direction:column; gap:10px;">
    <div class="demo-item max-w-300" style="width:100%; background:var(--panel-deep);">
      <div class="demo-label">.max-w-300</div>
      max-width: 300px — wächst nicht über 300px hinaus
    </div>
    <select class="max-w-300" style="width:100%; padding:6px 8px; background:var(--panel-deep); color:var(--text); border:1px solid var(--border); border-radius:4px;">
      <option>Select mit max-width 300px</option>
    </select>
  </div>
</div>
```

- [ ] **Step 2: Verifizieren, dass die Demo eingefügt wurde**

Run: `grep -cE 'col-w-80|col-w-100|col-w-120|col-w-180|max-w-300' components/utils.html`
Expected: ≥ `6` (4 col-w im `<th>` + 2× max-w-300)

- [ ] **Step 3: Visuell im Browser prüfen**

Öffnen: `file:///root/git/oe5ith-ci/components/utils.html`
Erwartet: Die ersten vier Tabellenspalten haben sichtbar unterschiedliche feste Breiten (80→180px), die fünfte füllt den Rest. Die `.max-w-300`-Box/Select wächst nicht über 300px.

- [ ] **Step 4: Commit**

```bash
git add components/utils.html
git commit -m "docs(utils): add reference demo for width and max-width utilities"
```

---

### Task 3: CHANGELOG-Eintrag (v1.15.0)

**Files:**
- Modify: `CHANGELOG.md` (neue Sektion an den Anfang, nach dem `---` in Zeile 6)

- [ ] **Step 1: Neue Versionssektion vor `## v1.14.0 - 2026-06-18` einfügen**

```markdown
## v1.15.0 - 2026-06-19

### Added
- **utils.css** — Breiten-Utilities: `.col-w-80`, `.col-w-100`, `.col-w-120`, `.col-w-180` (feste Spaltenbreiten für Tabellen-`<th>`) und `.max-w-300` (Max-Breite für Container/Select). Referenz-Demo in `components/utils.html`. Behebt zuvor wirkungslose No-op-Klassen in den website-v3-Views (logs, POCSAG).

---
```

- [ ] **Step 2: Verifizieren**

Run: `grep -c 'v1.15.0' CHANGELOG.md`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): add v1.15.0 — width utilities"
```

---

### Task 4: Consistency-Check

**Files:**
- (keine Änderung — Verifikation; `utils.css` ist in `docs/registry.json` bereits registriert)

- [ ] **Step 1: Consistency-Check ausführen**

Run: `python3 scripts/cli/check_consistency.py`
Expected: Exit-Code 0, keine Fehler/Warnungen zu `utils`.

- [ ] **Step 2: Falls README per AUTOGEN generiert wird, prüfen ob ein Regenerieren nötig ist**

Run: `grep -rl 'AUTOGEN' README.md scripts/ 2>/dev/null | head`
Falls ein Generator-Skript existiert und der Check das verlangt: laut dessen Anleitung ausführen und committen. Andernfalls keine Aktion.

---

## Self-Review

**Spec-Coverage:**
- ✅ `.col-w-80/100/120/180` + `.max-w-300` in `utils.css` → Task 1
- ✅ Demo in `components/utils.html` → Task 2
- ✅ CHANGELOG v1.15.0 (MINOR) → Task 3
- ✅ `check_consistency.py` grün, keine Registry-Änderung → Task 4
- ✅ Keine Tokens / harte px → Task 1 (Global Constraints)
- ✅ Kein G1–G4 / keine Spec-Doc für Utilities → bewusst nicht im Plan

**Außerhalb dieses Plans (Hinweis, nicht hier umgesetzt):** website-v3 muss `w-80/100/120/180` → `col-w-*` in `logs.html`/`pocsag.html` umbenennen; `w-100`-Kontext in `logs.html` beim Umstellen verifizieren (siehe Spec).

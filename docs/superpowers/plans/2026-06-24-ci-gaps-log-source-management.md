# CI-Lücken Log Source Management — Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Drei fehlende CSS-Muster ergänzen, die das Cloud-Portal für das Log-Source-Management benötigt — `.status-msg` (Inline-Statusmeldungen), `.max-w-150`/`.max-w-200` (Formularbreiten) und `.text-right` (Tabellen-Aktionsspalte).

**Architecture:** Alle Änderungen sind rein additiv in bestehenden CSS-Dateien. `.status-msg` landet in `page.css` (semantische Komponente mit Modifier-Klassen). Die drei Utility-Klassen landen in `utils.css`. Keine neuen Token nötig — alle Farben werden aus vorhandenen Semantic-Tokens gemappt.

**Tech Stack:** CSS (Custom Properties / Tokens), HTML (Komponenten-Demo)

## Global Constraints

- Alle Farben, Radii, Abstände via CSS-Tokens aus `css/common.css` — keine hardcodierten Werte
- Kein neues Token ohne klaren semantischen Grund und Mehrfachverwendung
- `css/demo.css` nur in `components/*.html` — nie produktiv
- Nach jeder Änderung: `python3 scripts/cli/check_consistency.py` muss fehlerlos durchlaufen
- Semantic Versioning: dieses Set ist MINOR (neue Komponente + neue Utilities) → v1.18.0

---

### Task 1: `.status-msg` — CSS + Demo + Registry

**Files:**
- Modify: `css/page.css` (Abschnitt am Ende, nach STATUS-PANEL)
- Create: `components/status-msg.html`
- Modify: `docs/registry.json` (page-Eintrag: `status-msg.html` in html-Array ergänzen)

**Interfaces:**
- Produziert: `.status-msg`, `.status-msg.info`, `.status-msg.warn`, `.status-msg.error`
- Verwendet: `--accent-subtle`, `--accent-border`, `--warning-subtle`, `--warning-border`, `--danger-subtle`, `--danger-border`, `--danger`, `--text`, `--btn-radius` (alle in `css/common.css`)

- [ ] **Step 1: CSS-Block in `css/page.css` einfügen**

Direkt nach dem STATUS-PANEL-Block (nach Zeile 512) anfügen:

```css
/* ═══════════════════════════════════════
   STATUS-MESSAGE
   Inline-Hinweiszeilen (info / warn / error).
   Modifier via .info / .warn / .error;
   show/hide über HTML-Attribut hidden.
   ═══════════════════════════════════════ */
.status-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: var(--btn-radius);
  font-size: 0.82rem;
  line-height: 1.4;
  border: 1px solid transparent;
}

.status-msg.info {
  background: var(--accent-subtle);
  border-color: var(--accent-border);
  color: var(--text);
}

.status-msg.warn {
  background: var(--warning-subtle);
  border-color: var(--warning-border);
  color: var(--text);
}

.status-msg.error {
  background: var(--danger-subtle);
  border-color: var(--danger-border);
  color: var(--danger);
}
```

- [ ] **Step 2: Demo-Datei `components/status-msg.html` anlegen**

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Status-Message</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/page.css">
<link rel="stylesheet" href="../css/demo.css">
<style>
.page-title { font-size: 1.6rem; font-weight: 300; color: var(--white); margin-bottom: 6px; }
.page-title strong { font-weight: 700; color: var(--accent); }
.page-desc { font-size: 0.85rem; color: var(--muted); margin-bottom: 48px; max-width: 640px; line-height: 1.6; }
.section-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: var(--subtle); margin-bottom: 6px; padding-bottom: 8px; border-bottom: 1px solid #222; }
.demo-box { background: var(--panel); border: 1px solid var(--border); border-radius: 6px; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
.annotation { font-size: 0.8rem; color: var(--subtle); margin-top: 10px; line-height: 1.6; }
.annotation code { background: #1e1e1e; padding: 1px 5px; border-radius: 3px; font-family: monospace; font-size: 0.75rem; color: #7ba8d4; }
</style>
</head>
<body>

<div class="page-title">CI Reference — <strong>Status-Message</strong></div>
<p class="page-desc">Inline-Hinweiszeilen aus <code>css/page.css</code>. Drei Varianten: <code>.info</code>, <code>.warn</code>, <code>.error</code>. Sichtbarkeit via HTML-Attribut <code>hidden</code> steuern.</p>

<!-- Alle drei Varianten -->
<div class="section-label">Varianten</div>
<div class="demo-box">
  <div class="status-msg info">
    <i class="fa-solid fa-circle-info"></i>
    Konfiguration wurde gespeichert.
  </div>
  <div class="status-msg warn">
    <i class="fa-solid fa-triangle-exclamation"></i>
    Verbindung zum Server wird hergestellt…
  </div>
  <div class="status-msg error">
    <i class="fa-solid fa-circle-xmark"></i>
    Fehler beim Laden der Quellenliste. Bitte Seite neu laden.
  </div>
</div>
<p class="annotation">
  Modifier: <code>.info</code> (Accent), <code>.warn</code> (Warning), <code>.error</code> (Danger).<br>
  Verwendung: <code>&lt;div class="status-msg info" hidden&gt;…&lt;/div&gt;</code> — <code>hidden</code>-Attribut entfernen zum Einblenden.
</p>

</body>
</html>
```

- [ ] **Step 3: `docs/registry.json` aktualisieren**

Im `page`-Eintrag das `html`-Array um `"status-msg.html"` erweitern:

```json
{ "id": "page", "title": "Seitenstruktur", "category": "component",
  "css": ["page.css"], "doc": ["page.md", "page-types.md"],
  "html": ["page-types.html", "status-msg.html"] },
```

- [ ] **Step 4: Konsistenz-Check**

```bash
cd /root/git/oe5ith-ci && python3 scripts/cli/check_consistency.py
```

Erwartetes Ergebnis: kein Fehler, kein Warning zu fehlenden Einträgen.

- [ ] **Step 5: Commit**

```bash
git add css/page.css components/status-msg.html docs/registry.json
git commit -m "feat(page): add .status-msg component (info / warn / error)"
```

---

### Task 2: Utility-Klassen in `utils.css` + Demo

**Files:**
- Modify: `css/utils.css` (zwei Stellen: MAX-WIDTH-Block, TEXT & VISIBILITY-Block)
- Modify: `components/utils.html` (Demo-Abschnitte für neue Klassen ergänzen)

**Interfaces:**
- Produziert: `.max-w-150`, `.max-w-200`, `.text-right`
- Keine Token-Abhängigkeiten — reine Layout-Werte

- [ ] **Step 1: `.max-w-150` und `.max-w-200` in `css/utils.css` einfügen**

Im MAX-WIDTH-Block (nach Zeile 70, nach `.max-w-300`) einfügen:

```css
.max-w-150 { max-width: 150px; }
.max-w-200 { max-width: 200px; }
```

Der Block sieht danach so aus:

```css
/* ═══════════════════════════════════════
   MAX-WIDTH UTILITIES
   ═══════════════════════════════════════ */

.max-w-150 { max-width: 150px; }
.max-w-200 { max-width: 200px; }
.max-w-300 { max-width: 300px; }
```

*(Aufsteigend sortiert, `.max-w-300` bleibt wo es ist.)*

- [ ] **Step 2: `.text-right` in `css/utils.css` einfügen**

Im TEXT & VISIBILITY-Block (Zeilen 39–44) nach `.text-left` ergänzen:

```css
.text-center { text-align: center; }
.text-left   { text-align: left; }
.text-right  { text-align: right; }
.opacity-50  { opacity: 0.5; }
.hidden      { display: none !important; }
```

- [ ] **Step 3: `components/utils.html` — Demo-Abschnitte ergänzen**

In `utils.html` nach dem bestehenden Abschnitt für `.max-w-300` folgenden Block einfügen:

```html
<!-- .max-w-150 / .max-w-200 -->
<div class="section">
  <div class="section-label">max-width Utilities — .max-w-150 / .max-w-200</div>
  <div class="demo-box">
    <div>
      <div class="demo-label">.max-w-150</div>
      <input class="max-w-150" type="text" value="Kurzfeld" style="background:var(--panel-deep);border:1px solid var(--border);border-radius:4px;padding:6px 10px;color:var(--text);font-size:0.82rem;width:100%;">
    </div>
    <div>
      <div class="demo-label">.max-w-200</div>
      <select class="max-w-200" style="background:var(--panel-deep);border:1px solid var(--border);border-radius:4px;padding:6px 10px;color:var(--text);font-size:0.82rem;width:100%;">
        <option>syslog</option><option>journald</option><option>file</option>
      </select>
    </div>
  </div>
  <p class="annotation">Für kurze Formularfelder in <code>.form-row</code>. Ergänzt das bestehende <code>.max-w-300</code>.</p>
</div>
```

Und nach dem bestehenden Abschnitt für `.text-center` / `.text-left`:

```html
<!-- .text-right -->
<div class="section">
  <div class="section-label">Text Alignment — .text-right</div>
  <div class="demo-box">
    <div class="demo-item text-right" style="width:100%;">Rechtsbündig — typisch für Aktionsspalten in .ci-table</div>
  </div>
  <p class="annotation"><code>.text-right</code> ergänzt <code>.text-center</code> und <code>.text-left</code> in der TEXT & VISIBILITY-Gruppe.</p>
</div>
```

- [ ] **Step 4: Konsistenz-Check**

```bash
cd /root/git/oe5ith-ci && python3 scripts/cli/check_consistency.py
```

Erwartetes Ergebnis: kein Fehler.

- [ ] **Step 5: Commit**

```bash
git add css/utils.css components/utils.html
git commit -m "feat(utils): add .max-w-150, .max-w-200, .text-right utilities"
```

---

### Task 3: Changelog + Release v1.18.0

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Konsumiert: fertige Commits aus Task 1 und Task 2

- [ ] **Step 1: `CHANGELOG.md` aktualisieren**

Neuen Abschnitt oben einfügen (vor dem bisherigen neuesten Eintrag):

```markdown
## [1.18.0] — 2026-06-24

### Added
- `page.css`: `.status-msg` Komponente mit Modifier-Klassen `.info`, `.warn`, `.error` — Inline-Statusmeldungen für Aktions-Feedback, Fehlerzustände und Leer-Zustände; behebt gleichzeitig unstyled usage in bestehenden Portal-Views (`logs.html`, `pocsag.html`)
- `utils.css`: `.max-w-150`, `.max-w-200` — Max-Width-Utilities für kurze Formularfelder
- `utils.css`: `.text-right` — Text-Alignment-Utility, ergänzt `.text-center` und `.text-left`
- `components/status-msg.html` — Referenz-Demo für alle drei `.status-msg`-Varianten
```

- [ ] **Step 2: Commit + Tag**

```bash
git add CHANGELOG.md
git commit -m "chore: release v1.18.0 — status-msg, max-w-150/200, text-right"
git tag -a v1.18.0 -m "Release v1.18.0"
git push origin main
git push origin v1.18.0
```

---

## Selbst-Review gegen Spec

| Spec-Punkt | Plan-Task | Abgedeckt? |
|---|---|---|
| `.status-msg` + `.info`/`.warn`/`.error` in `page.css` | Task 1, Step 1 | ✓ |
| Hardcoded Farben → Tokens | Task 1, Step 1 (token-mapping) | ✓ |
| Demo-HTML für `.status-msg` | Task 1, Step 2 | ✓ |
| Registry-Eintrag für `status-msg.html` | Task 1, Step 3 | ✓ |
| `.max-w-150`, `.max-w-200` in `utils.css` | Task 2, Step 1 | ✓ |
| `.text-right` in `utils.css` | Task 2, Step 2 | ✓ |
| Demo-Update `utils.html` | Task 2, Step 3 | ✓ |
| Konsistenz-Check nach jeder Änderung | Task 1 Step 4, Task 2 Step 4 | ✓ |
| Changelog + Tag | Task 3 | ✓ |

**Placeholder-Scan:** Keine TBD/TODO/„ähnlich wie"-Formulierungen. Alle Code-Blöcke vollständig.

**Token-Konsistenz:** `--btn-radius` in Task 1 korrekt (6px = vorgeschlagene 6px). Farbtoken konsistent: accent → info, warning → warn, danger → error.

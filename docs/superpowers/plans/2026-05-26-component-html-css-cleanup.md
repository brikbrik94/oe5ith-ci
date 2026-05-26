# Component HTML CSS Cleanup — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Alle `components/*.html` Referenzseiten nutzen nur noch Repo-CSS-Dateien — keine doppelten Token-Definitionen, keine duplizierten Komponenten-CSS-Regeln, keine hardcoded Farb-Hex-Werte in `style=`-Attributen.

**Architecture:** Jede HTML-Datei bekommt `<link>`-Tags für `common.css` (Tokens+Reset), die zugehörigen Komponenten-CSS-Dateien und `demo.css` (Demo-Layout-Hilfsklassen). Der `<style>`-Block wird auf die verbleibenden datei-spezifischen Demo-Layout-Klassen reduziert — solche die weder in `demo.css` noch in einem der verlinkten CSS-Files definiert sind.

**Tech Stack:** Plain HTML/CSS, kein Build-Step. Repo unter `/root/git/oe5ith-ci/`.

---

## Token-Mapping für inline `style=`-Attribute

Diese Tabelle gilt für alle Tasks. Nur Werte ersetzen, für die ein Token existiert:

| Hardcoded | → CSS-Token |
|---|---|
| `#1a1a1a` | `var(--bg)` |
| `#252525` | `var(--card-bg)` |
| `#202020` | `var(--panel)` |
| `#161616` | `var(--panel-deep)` |
| `#e0e0e0` | `var(--text)` |
| `#888` / `#888888` | `var(--muted)` |
| `#555` / `#555555` | `var(--subtle)` |
| `#333` / `#333333` | `var(--border)` |
| `#444` / `#444444` | `var(--border-strong)` |
| `#3b82f6` | `var(--accent)` |
| `#2563eb` | `var(--accent-hover)` |
| `#22c55e` | `var(--success)` |
| `#eab308` | `var(--warning)` |
| `#ef4444` | `var(--danger)` |
| `#a78bfa` | `var(--auth)` |
| `#ffffff` / `#fff` | `var(--white)` |
| `#2a2a2a` | `var(--code-inline-bg)` |
| `#4ade80` | `var(--code-text)` |
| `#e6e6e6` | `var(--code-inline-text)` |
| `rgba(59,130,246,0.07)` | `var(--accent-subtle)` |
| `rgba(59,130,246,0.10)` / `rgba(59,130,246,.10)` | `var(--accent-subtle-md)` |
| `rgba(59,130,246,0.25)` / `rgba(59,130,246,.25)` | `var(--accent-border)` |

Folgende Werte haben **kein Token** und bleiben unverändert:
`#ccc`, `#666`, `#4b5563`, `#ddd`, `#d1d5db`, `#f59e0b`, `#2d3a2d`, `#1f1f1f`, `#222`, `rgba`-Werte ohne direktes Token.

## Allgemeine Regel für Stil-Blöcke

Aus dem `<style>`-Block entfernen:
1. Gesamter `:root { }` Block — kommt aus `common.css`
2. `*, *::before, *::after { }` und `body { }` — kommt aus `common.css`
3. Alle CSS-Klassen, die in einem der verlinkten CSS-Files definiert sind

Im `<style>`-Block behalten: ausschließlich datei-spezifische Demo-Layout-Klassen (im Plan explizit angegeben).

---

## Task 1: `utils.html`

**Files:**
- Modify: `components/utils.html`

**Neue `<head>`-Section** (Zeile 7 bis `</style>` ersetzen):

```html
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/utils.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block** (exakt so einfügen, nach den `<link>`-Tags):

```html
<style>
/* Demo-seitenspezifische Layout-Klassen — nicht in demo.css oder utils.css */
.page-title { font-size: 1.6rem; font-weight: 300; color: var(--white); margin-bottom: 6px; }
.page-title strong { font-weight: 700; color: var(--accent); }
.page-desc { font-size: 0.85rem; color: var(--muted); margin-bottom: 48px; max-width: 640px; line-height: 1.6; }
.section-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: var(--subtle); margin-bottom: 6px; padding-bottom: 8px; border-bottom: 1px solid #222; }
.section-desc { font-size: 0.82rem; color: #444; margin-bottom: 16px; line-height: 1.6; }
.annotation { font-size: 0.8rem; color: var(--subtle); margin-top: 10px; line-height: 1.6; max-width: 860px; }
.annotation code { background: #1e1e1e; padding: 1px 5px; border-radius: 3px; font-family: monospace; font-size: 0.75rem; color: #7ba8d4; }
.demo-box { background: var(--panel); border: 1px solid var(--border); border-radius: 6px; padding: 20px; display: flex; gap: 16px; flex-wrap: wrap; align-items: flex-start; }
.demo-item { background: var(--panel-deep); border: 1px dashed var(--border); border-radius: 4px; padding: 12px 16px; font-size: 0.78rem; color: var(--muted); }
.demo-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; color: var(--subtle); margin-bottom: 6px; }
</style>
```

**Inline-Farben** (2 Vorkommen, beide mit Token):
```
style="background:var(--panel-deep);"  (Zeile 96 — war var(--panel), prüfen)
```
Grep-Befehl: `grep -n 'style="[^"]*#[0-9a-fA-F]' components/utils.html` — alle Treffer mit Token-Tabelle abgleichen.

- [ ] Aktuellen `<head>` lesen: `head -90 components/utils.html`
- [ ] `<style>`-Block (Zeilen 7–84) durch neue Links + Trimmed-Block ersetzen
- [ ] Inline-Farben prüfen und mit Token-Tabelle ersetzen
- [ ] Im Browser öffnen: `open components/utils.html` — Seite muss identisch zu vorher aussehen (Abschnitte, Utility-Klassen korrekt dargestellt)
- [ ] Commit:
```bash
git add components/utils.html
git commit -m "fix(utils-demo): replace inline style block with CSS file links"
```

---

## Task 2: `tokens.html`

**Files:**
- Modify: `components/tokens.html`

**Neue `<head>`-Section** (alle `<link>`- und `<style>`-Zeilen ersetzen):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:** keiner — alle Klassen (`swatch-*`, `token-table*`, `subtle-chip` etc.) sind in `demo.css` definiert. Den kompletten `<style>`-Block entfernen.

**Inline-Farben** (27 Vorkommen) — nur Swatch-Farben, die ein Token haben:

In `components/tokens.html` ersetzen (Token-Swatches zeigen ihre eigene Farbe via CSS-Var):
```
style="background:#1a1a1a"  → style="background:var(--bg)"
style="background:#252525"  → style="background:var(--card-bg)"
style="background:#202020"  → style="background:var(--panel)"
style="background:#161616"  → style="background:var(--panel-deep)"
style="background:#e0e0e0"  → style="background:var(--text)"
style="background:#888888"  → style="background:var(--muted)"
style="background:#555555"  → style="background:var(--subtle)"
style="background:#333333"  → style="background:var(--border)"
style="background:#3b82f6"  → style="background:var(--accent)"
style="background:#2563eb"  → style="background:var(--accent-hover)"
style="background:#22c55e"  → style="background:var(--success)"
style="background:#eab308"  → style="background:var(--warning)"
style="background:#ef4444"  → style="background:var(--danger)"
style="background:#a78bfa"  → style="background:var(--auth)"
style="background:#4ade80"  → style="background:var(--code-text)"
style="background:#2a2a2a"  → style="background:var(--code-inline-bg)"
style="background:#e6e6e6"  → style="background:var(--code-inline-text)"
```

Swatch bei Zeile 463: `style="background:#000000;border-bottom:1px solid #1a1a1a"` → `style="background:var(--code-bg);border-bottom:1px solid var(--bg)"`

rgba-Swatches (Zeilen 374, 383) und `.subtle-chip`-Styles (Zeilen 396–399, 450–453):
```
rgba(59,130,246,0.07) → var(--accent-subtle)
rgba(59,130,246,0.10) → var(--accent-subtle-md)
rgba(59,130,246,0.25) → var(--accent-border)
```

Zeile 588 (`background:#1f1f1f`) — kein Token, bleibt.

- [ ] `head -260 components/tokens.html` lesen
- [ ] `<style>`-Block (Zeilen 9–257) vollständig entfernen
- [ ] Alte Google-Fonts-Links durch neue `<head>`-Section ersetzen
- [ ] Alle Swatch `style=`-Attribute mit Token-Tabelle ersetzen
- [ ] Browser-Check: alle Farbfelder korrekt dargestellt
- [ ] Commit:
```bash
git add components/tokens.html
git commit -m "fix(tokens-demo): replace inline style block with CSS file links"
```

---

## Task 3: `typography-preview.html` und `typography.html`

**Files:**
- Modify: `components/typography-preview.html`
- Modify: `components/typography.html`

### typography-preview.html

**Neue `<head>`-Section** (Zeile 7 bis `</style>` ersetzen):

```html
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/typography.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

```html
<style>
body { padding: 32px; line-height: 1.6; }
.row { display: flex; align-items: baseline; gap: 20px; padding: 16px 0; border-bottom: 1px solid #1e1e1e; }
.row:last-child { border-bottom: none; }
.meta { width: 160px; flex-shrink: 0; }
.meta-name { font-size: 10px; font-weight: 700; letter-spacing: .8px; text-transform: uppercase; color: var(--subtle); display: block; margin-bottom: 3px; }
.meta-spec { font-size: 10px; font-family: monospace; color: #444; line-height: 1.7; display: block; }
.sample { flex: 1; min-width: 0; }
</style>
```

**Inline-Farben** (11 Vorkommen):
```
color:#fff  → color:var(--white)     (Zeilen 27, 37, 87)
color:#3b82f6 → color:var(--accent)  (Zeile 27)
color:#ddd  → bleibt (kein Token)
color:#888  → color:var(--muted)    (Zeilen 57, 97)
color:#555  → color:var(--subtle)   (Zeilen 67, 77)
background:#000 → background:var(--code-bg)  (Zeile 107 pre)
color:#4ade80 → color:var(--code-text)  (Zeile 107 pre)
background:#2a2a2a → background:var(--code-inline-bg)  (Zeile 97 code)
color:#e6e6e6 → color:var(--code-inline-text)  (Zeile 97 code)
```

### typography.html

**Neue `<head>`-Section** (Zeilen 7–10 ersetzen):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/typography.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

```html
<style>
/* .t-white fehlt in typography.css — wird hier ergänzt */
.t-white { color: var(--white); }
/* Demo-Card — nur auf dieser Referenzseite */
.demo-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--card-radius); padding: var(--card-padding); }
</style>
```

Alle anderen Klassen (`.t-small`, `.t-label`, `.t-brand`, `.t-url`, `.font-medium`, `.font-semibold`, `.t-success`, `.t-danger`, `.t-muted`, `.t-subtle`) sind in `typography.css` definiert. Die Demo-Layout-Klassen (`.page-content`, `.section-title`, `.type-row`, `.type-meta-name`, `.type-token`) sind in `demo.css`.

**Inline-Farben** (1 Vorkommen):
Zeile mit `color:var(--muted,` — bereits korrekt, kein Änderungsbedarf. Trotzdem mit Token-Tabelle prüfen.

- [ ] `components/typography-preview.html` lesen (Zeilen 1–20)
- [ ] `<style>`-Block ersetzen (Zeilen 7–17), neue Links + Trimmed-Block einsetzen
- [ ] Inline-Farben ersetzen
- [ ] `components/typography.html` lesen (Zeilen 1–185)
- [ ] `<style>`-Block (Zeilen 10–180) ersetzen, neue Links + Trimmed-Block einsetzen
- [ ] Browser-Check: Schriftsystem korrekt dargestellt, JetBrains Mono sichtbar
- [ ] Commit:
```bash
git add components/typography-preview.html components/typography.html
git commit -m "fix(typography-demo): replace inline style blocks with CSS file links"
```

---

## Task 4: `badges.html`

**Files:**
- Modify: `components/badges.html`

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/badges.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

Entfernen: `:root`, reset, body, `.topbar`, `.brand`, `.page-content`, `.demo-section`, `.demo-section-title`, `.demo-section-desc` (alle in demo.css), badge-CSS (in badges.css).

Behalten:

```html
<style>
.row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 12px; }
.demo-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--card-radius); padding: var(--card-padding); }
.demo-card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.demo-card-header h3 { font-size: 0.9rem; font-weight: 600; color: var(--white); }
.demo-card p { font-size: 0.78rem; color: var(--muted); line-height: 1.5; }
.demo-topbar-strip { background: var(--card-bg); height: 36px; border-bottom: 2px solid var(--accent); display: flex; align-items: center; padding: 0 12px; border-radius: 6px 6px 0 0; gap: 8px; }
.demo-sidebar-strip { background: var(--panel); width: 140px; min-height: 80px; padding: 8px 6px; display: flex; flex-direction: column; gap: 2px; }
.demo-nav-item { display: flex; align-items: center; gap: 6px; padding: 5px 8px; border-radius: 4px; font-size: 0.72rem; color: var(--muted); cursor: default; }
.demo-nav-item.active { background: var(--accent-subtle); color: var(--accent); }
</style>
```

**Inline-Farben** (1 Vorkommen):
`grep -n 'style="[^"]*#[0-9a-fA-F]' components/badges.html` — Treffer mit Token-Tabelle abgleichen.

- [ ] `components/badges.html` Zeilen 1–200 lesen
- [ ] `<style>`-Block (Zeilen 8–197) ersetzen
- [ ] Inline-Farben prüfen und ersetzen
- [ ] Browser-Check: Badges korrekt dargestellt, Demo-Karten mit Topbar/Sidebar-Strip sichtbar
- [ ] Commit:
```bash
git add components/badges.html
git commit -m "fix(badges-demo): replace inline style block with CSS file links"
```

---

## Task 5: `buttons.html` und `buttons-demo.html`

**Files:**
- Modify: `components/buttons.html`
- Modify: `components/buttons-demo.html`

Beide Dateien sind fast identisch (diff: 4 Zeilen). Beide erhalten dieselbe Behandlung.

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/buttons.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

Alle anderen Klassen sind in `buttons.css` oder `demo.css` (`.page`, `.section`, `.section-title`, `.matrix*`, `.divider`, `.hint`, `.event-log`, `.log-*`, `.type-switcher`, `.type-btn`, `.type-info`, `.bp-indicator`).

Behalten:

```html
<style>
.row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 12px; }
</style>
```

**Inline-Farben** (8 Vorkommen pro Datei):

Zeilen 294–297 (`color:#ccc`): `#ccc` hat kein Token → bleibt.

Zeilen 410–413 (State-Matrix mit hardcoded Hintergrundwerten — Dokumentationszweck):
```
background:#2563eb  → background:var(--accent-hover)
color:#fff          → color:var(--white)
color:#3b82f6       → color:var(--accent)
color:#e0e0e0       → color:var(--text)
border:1px solid #555 → border:1px solid var(--subtle)
```
Die rgba-Werte (0.18, 0.4, 0.04, 0.2) bleiben — kein Token.

- [ ] `components/buttons.html` Zeilen 1–285 lesen
- [ ] `<style>`-Block (Zeilen 8–278) ersetzen
- [ ] Inline-Farben ersetzen
- [ ] Gleiches für `components/buttons-demo.html`
- [ ] Browser-Check: Button-Matrix und Event-Log korrekt dargestellt
- [ ] Commit:
```bash
git add components/buttons.html components/buttons-demo.html
git commit -m "fix(buttons-demo): replace inline style blocks with CSS file links"
```

---

## Task 6: `cards.html` und `code-viewer.html`

**Files:**
- Modify: `components/cards.html`
- Modify: `components/code-viewer.html`

### cards.html

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/topbar.css">
<link rel="stylesheet" href="../css/cards.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:** Alle `.card-*`-Klassen sind in `cards.css`. Topbar in `topbar.css`. Lesen und prüfen: `awk '/<style>/,/<\/style>/' components/cards.html | grep -E '^\.[a-z]'` — alle Klassen müssen in `cards.css`, `topbar.css` oder `demo.css` vorhanden sein. Falls eine Klasse fehlt, in Trimmed-Block übernehmen.

Erwartung: Kein oder minimaler verbleibender `<style>`-Block.

**Inline-Farben** (0 Vorkommen — kein Handlungsbedarf).

### code-viewer.html

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/page.css">
<link rel="stylesheet" href="../css/typography.css">
<link rel="stylesheet" href="../css/forms.css">
<link rel="stylesheet" href="../css/code-viewer.css">
<link rel="stylesheet" href="../css/demo.css">
```

Hinweis: `.panel` ist in `page.css` definiert. `.mono` und `.ci-label` sind in `typography.css`.

**Verbleibender `<style>`-Block:**

```html
<style>
.demo-body { padding: 32px 40px; display: flex; flex-direction: column; gap: 32px; max-width: 860px; }
.demo-section-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; color: var(--subtle); margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid #1e1e1e; }
</style>
```

**Inline-Farben** (0 Vorkommen — kein Handlungsbedarf).

- [ ] `components/cards.html` Zeilen 1–420 lesen
- [ ] `<style>`-Block ersetzen, Klassen gegen CSS-Files prüfen
- [ ] `components/code-viewer.html` Zeilen 1–120 lesen
- [ ] `<style>`-Block (Zeilen 8–117) durch Links + Trimmed-Block ersetzen
- [ ] Browser-Check: Card-Grid und Code-Viewer korrekt dargestellt
- [ ] Commit:
```bash
git add components/cards.html components/code-viewer.html
git commit -m "fix(cards-code-demo): replace inline style blocks with CSS file links"
```

---

## Task 7: `context-menu.html` und `forms.html`

**Files:**
- Modify: `components/context-menu.html`
- Modify: `components/forms.html`

### context-menu.html

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/modal.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

Entfernen: `:root`, reset, body, `.topbar`, `.brand`, `.page-content`, `.demo-section*` (alle in demo.css), `.ctx-menu*` (alle in modal.css), `.fake-map` und `.fake-map-label` (in demo.css).

Behalten:

```html
<style>
.annotation { font-size: 0.8rem; color: var(--subtle); margin-top: 10px; line-height: 1.6; }
.annotation code { background: #1e1e1e; padding: 1px 5px; border-radius: 3px; font-family: monospace; font-size: 0.75rem; color: #7ba8d4; }
.action-menu-btn { display: inline-flex; align-items: center; gap: 6px; height: 30px; padding: 0 12px; border: 1px solid var(--border); border-radius: 4px; font-size: 0.8rem; font-weight: 600; font-family: inherit; cursor: pointer; background: var(--panel); color: var(--muted); transition: all var(--transition-fast); }
.action-menu-btn:hover { background: var(--accent-subtle-md); color: var(--accent); }
.action-menu-wrap { position: relative; display: inline-block; }
.action-menu-wrap .ctx-menu { top: 36px; left: 0; }
.fake-map-hint { position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); font-size: 0.7rem; color: rgba(255,255,255,0.25); pointer-events: none; white-space: nowrap; }
.ci-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; background: var(--panel); }
.ci-table thead tr { border-bottom: 1px solid var(--border); }
.ci-table th { padding: 8px 14px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; color: var(--subtle); text-align: left; }
.ci-table tbody tr { border-bottom: 1px solid rgba(255,255,255,0.03); transition: background var(--transition-fast); }
.ci-table tbody tr:last-child { border-bottom: none; }
.ci-table tbody tr:hover { background: rgba(255,255,255,0.025); }
.ci-table td { padding: 8px 14px; vertical-align: middle; }
</style>
```

**Inline-Farben** (0 Vorkommen — kein Handlungsbedarf).

### forms.html

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/topbar.css">
<link rel="stylesheet" href="../css/forms.css">
<link rel="stylesheet" href="../css/sidebar.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Style-Blöcke** (forms.html hat zwei — Zeilen 8–424 und 815–826):

Block 1 (Zeilen 8–424): Entfernen: `:root`, reset, body, `.topbar`, `.brand`. Den Rest des Blocks lesen und alle Klassen prüfen, die in `forms.css`, `sidebar.css` oder `demo.css` definiert sind — diese entfernen. Verbleibende datei-spezifische Demo-Klassen (wie `.service-selector`, `.segmented`, `.geocoder-results` etc.) in einem Trimmed-Block behalten.

Block 2 (Zeilen 815–826): Komplett entfernen — `.form-submit` ist in `forms.css` (Zeile 328) definiert.

Prüf-Befehl für Block 1 Klassen:
```bash
awk '/^<style>/,/^<\/style>/' components/forms.html | grep -E '^\.[a-z]' | head -40
```
Dann für jede Klasse prüfen: `grep -n "^<Klassenname>" css/forms.css css/sidebar.css css/demo.css`

**Inline-Farben** (0 Vorkommen — kein Handlungsbedarf).

- [ ] `components/context-menu.html` Zeilen 1–140 lesen
- [ ] `<style>`-Block ersetzen
- [ ] `components/forms.html` Zeilen 1–430 und 810–830 lesen
- [ ] Beiden Style-Blöcke bearbeiten
- [ ] Browser-Check: Context-Menu und Formular korrekt dargestellt, Sidebar-Ctx sichtbar
- [ ] Commit:
```bash
git add components/context-menu.html components/forms.html
git commit -m "fix(context-forms-demo): replace inline style blocks with CSS file links"
```

---

## Task 8: `sidebar.html` und `sidebar-types.html`

**Files:**
- Modify: `components/sidebar.html`
- Modify: `components/sidebar-types.html`

### sidebar.html

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/topbar.css">
<link rel="stylesheet" href="../css/sidebar.css">
<link rel="stylesheet" href="../css/badges.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

Entfernen: `:root`, reset, body, `.topbar`, `.brand`, alle Sidebar-Klassen (in `sidebar.css`), badge-Klassen (in `badges.css`). Demo-Layout-Klassen aus `demo.css` entfernen (`.page-content`, `.ref-title`, `.ref-desc`, `.ref-section`, `.ref-section-title`, `.element-grid`, `.element-card*`, `.type-switcher`, `.type-btn`, `.type-info` — sind alle in demo.css).

Behalten:

```html
<style>
.layout { display: flex; height: calc(100vh - var(--topbar-height)); }
.nav-icon { width: 16px; text-align: center; font-size: 0.85em; flex-shrink: 0; opacity: 0.7; }
.external-icon { font-size: 0.65em; margin-left: auto; opacity: 0.5; flex-shrink: 0; }
.accordion { display: flex; flex-direction: column; gap: 2px; }
</style>
```

**Inline-Farben** (6 Vorkommen):
```
background:#3b82f6  → background:var(--accent)    (acc-dot Zeilen 386, 566)
background:#22c55e  → background:var(--success)   (acc-dot Zeile 408)
background:#ef4444  → background:var(--danger)    (acc-dot Zeile 439)
background:#555     → background:var(--subtle)    (acc-dot Zeilen 601, 617, 633)
```

### sidebar-types.html

**Neue `<head>`-Section** (Zeilen 7–10 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/sidebar.css">
<link rel="stylesheet" href="../css/badges.css">
<link rel="stylesheet" href="../css/forms.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

Entfernen: `:root`, reset, body, alle Sidebar/Badge/Forms-Klassen. `.page-title`, `.page-desc`, `.section-label`, `.section-desc`, `.annotation` — diese sind NICHT in demo.css → behalten.

Behalten:

```html
<style>
.page-title { font-size: 1.6rem; font-weight: 300; color: var(--white); margin-bottom: 6px; }
.page-title strong { font-weight: 700; color: var(--accent); }
.page-desc { font-size: 0.85rem; color: var(--muted); margin-bottom: 48px; max-width: 640px; line-height: 1.6; }
.section-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: var(--subtle); margin-bottom: 6px; padding-bottom: 8px; border-bottom: 1px solid #222; }
.section-desc { font-size: 0.82rem; color: #444; margin-bottom: 16px; line-height: 1.6; }
.annotation { font-size: 0.8rem; color: var(--subtle); margin-top: 10px; line-height: 1.6; max-width: 860px; }
.annotation code { background: #1e1e1e; padding: 1px 5px; border-radius: 3px; font-family: monospace; font-size: 0.75rem; color: #7ba8d4; }
.annotation strong { color: var(--muted); font-weight: 600; }
.screen { background: var(--bg); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; max-width: 860px; margin-bottom: 16px; }
.m-tb { background: var(--card-bg); height: 44px; border-bottom: 2px solid var(--accent); display: flex; align-items: center; padding: 0 12px; gap: 10px; }
.m-brand { color: var(--white); font-weight: 700; font-size: 1.1rem; letter-spacing: 1.2px; display: flex; align-items: center; gap: 7px; }
.m-brand img { width: 20px; height: 20px; }
.m-nav { margin-left: auto; display: flex; gap: 10px; }
.m-nav a { font-size: 0.72rem; color: var(--muted); text-decoration: none; }
.m-nav a.active { color: var(--accent); }
.m-layout { display: flex; }
.m-map-bg { flex: 1; background: #2d3a2d; display: flex; align-items: center; justify-content: center; }
.m-map-label { font-size: 0.62rem; color: rgba(255,255,255,0.15); }
.sb-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: var(--subtle); padding: 10px 8px 4px; }
</style>
```

**Inline-Farben** (8 Vorkommen):
```
color:#fff          → color:var(--white)     (Zeilen 531, 773, 830, 859)
background:#eab308  → background:var(--warning)  (Zeile 540)
background:#22c55e  → background:var(--success)  (Zeile 548)
background:#3b82f6  → background:var(--accent)   (Zeile 566)
background:#a78bfa  → background:var(--auth)     (Zeile 574)
```

- [ ] `components/sidebar.html` Zeilen 1–340 lesen
- [ ] `<style>`-Block (Zeilen 8–336) durch Links + Trimmed-Block ersetzen
- [ ] Inline-Farben ersetzen
- [ ] `components/sidebar-types.html` Zeilen 1–475 lesen
- [ ] `<style>`-Block (Zeilen 10–469) durch Links + Trimmed-Block ersetzen
- [ ] Inline-Farben ersetzen
- [ ] Browser-Check: Beide Sidebar-Referenzseiten vollständig dargestellt
- [ ] Commit:
```bash
git add components/sidebar.html components/sidebar-types.html
git commit -m "fix(sidebar-demo): replace inline style blocks with CSS file links"
```

---

## Task 9: `modal.html` und `topbar.html`

**Files:**
- Modify: `components/modal.html`
- Modify: `components/topbar.html`

### modal.html

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/topbar.css">
<link rel="stylesheet" href="../css/modal.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

Entfernen: `:root`, reset, body, `.topbar`, `.brand`, alle Modal-Klassen (in `modal.css`), `.ctx-menu*` (in `modal.css`), `.map-legend*` (in `modal.css`).

Behalten: Alle Demo-spezifischen Map-Popup-Klassen. Den Style-Block lesen und prüfen, welche Klassen NICHT in `modal.css` oder `demo.css` sind:
```bash
awk '/<style>/,/<\/style>/' components/modal.html | grep -E '^\.[a-z]' | grep -v '\.topbar\|\.brand\|\.modal\|\.ctx-\|\.map-legend'
```
Diese Klassen in einem Trimmed-Block behalten.

**Inline-Farben** (3 Vorkommen):
```
background:#22c55e  → background:var(--success)  (map-legend-dot, Zeile 601)
background:#3b82f6  → background:var(--accent)   (map-legend-line, Zeile 605)
background:#f59e0b  → bleibt (kein Token)         (map-legend-area, Zeile 609)
```

### topbar.html

**Neue `<head>`-Section** (Zeile 7 `<style>` ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/topbar.css">
<link rel="stylesheet" href="../css/sidebar.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

Entfernen: `:root`, reset, body, alle Topbar-Klassen (in `topbar.css`), alle Sidebar-Klassen (in `sidebar.css`). 

Den Rest prüfen:
```bash
awk '/<style>/,/<\/style>/' components/topbar.html | grep -E '^\.[a-z]' | grep -v '\.topbar\|\.brand\|\.sidebar\|\.nav-icon\|\.acc-\|\.tab-\|\.footer\|\.dropdown'
```

Aus der vorherigen Analyse sind folgende Demo-Klassen zu behalten:

```html
<style>
.layout { display: flex; height: calc(100vh - var(--topbar-height)); overflow: hidden; }
.page-content { flex: 1; padding: 32px 40px; overflow-y: auto; max-width: 860px; }
.controls-panel { background: var(--panel); border-left: 1px solid var(--border); width: 280px; display: flex; flex-direction: column; overflow-y: auto; }
.controls-toggle { display: flex; align-items: center; gap: 8px; padding: 12px 16px; font-size: 0.78rem; font-weight: 600; color: var(--muted); cursor: pointer; border-bottom: 1px solid var(--border); user-select: none; }
.controls-overlay { position: fixed; inset: 0; z-index: 900; display: none; flex-direction: column; }
.controls-overlay.open { display: flex; }
.controls-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.5); opacity: 0; transition: opacity 0.2s; z-index: 900; }
.controls-backdrop.visible { opacity: 1; }
.slider-icon { width: 18px; height: 14px; display: flex; flex-direction: column; gap: 3px; }
.slider-icon span { display: block; height: 2px; background: var(--muted); border-radius: 2px; }
.slider-icon span:nth-child(2) { width: 65%; }
.demo-content { padding: 32px 40px; }
.demo-title { font-size: 1.6rem; font-weight: 300; color: var(--white); margin-bottom: 8px; }
.demo-title strong { font-weight: 700; color: var(--accent); }
.demo-desc { font-size: 0.85rem; color: var(--muted); margin-bottom: 40px; max-width: 600px; line-height: 1.6; }
.event-log { background: #0d0d0d; border: 1px solid #222; border-radius: 6px; padding: 12px 14px; font-family: var(--font-mono); font-size: 0.78rem; color: var(--code-text); min-height: 80px; max-height: 160px; overflow-y: auto; line-height: 1.9; }
.event-log .log-muted { color: #444; }
.bp-indicator { display: inline-flex; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 4px; background: var(--accent-subtle-md); border: 1px solid var(--accent-border); color: var(--accent); margin-bottom: 20px; }
</style>
```

**Inline-Farben** (2 Vorkommen in JS template strings, Zeilen 1076 + 1117):
```
background:#2a2a2a  → background:var(--code-inline-bg)
color:#e0e0e0       → color:var(--text)
```
Hinweis: `#4b5563` und `#d1d5db` bleiben (kein Token).

- [ ] `components/modal.html` Zeilen 1–430 lesen
- [ ] `<style>`-Block (Zeilen 8–427) ersetzen
- [ ] Inline-Farben ersetzen (Zeilen 601, 605)
- [ ] `components/topbar.html` Zeilen 1–690 lesen
- [ ] `<style>`-Block (Zeilen 7–683) durch Links + Trimmed-Block ersetzen
- [ ] Inline-Farben in JS-Template-Strings ersetzen (Zeilen 1076, 1117)
- [ ] Browser-Check: Alle Modal-Typen öffnen, Topbar-Controls funktionieren
- [ ] Commit:
```bash
git add components/modal.html components/topbar.html
git commit -m "fix(modal-topbar-demo): replace inline style blocks with CSS file links"
```

---

## Task 10: `page-types.html`

**Files:**
- Modify: `components/page-types.html`

**Neue `<head>`-Section** (Zeilen 7–8 ersetzen):

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/demo.css">
```

**Verbleibender `<style>`-Block:**

Entfernen: `:root`, reset, body. Alle Mini-Mockup-Klassen (`.m-tb`, `.m-brand`, `.m-layout`, `.m-sb*`, `.m-panel*`, `.m-card-grid*`, `.m-btn`, `.m-input`, `.ph`, `.w-*`, `.screen`, `.page-title-main`, `.page-desc`, `.section-label`, `.section-desc`, `.ext`) sind datei-spezifisch und NICHT in demo.css → vollständig behalten.

Den `<style>`-Block lesen:
```bash
awk 'NR>=8 && NR<=262' components/page-types.html
```

Daraus den Trimmed-Block erstellen: Alles nach dem `body { }` Block behalten, `:root`, `*`, `body` entfernen.

**Inline-Farben** (10 Vorkommen):
```
color:#666        → bleibt (kein Token)
background:#e0e0e0 → background:var(--text)  (Zeile 380 — Platzhalter-Balken)
background:#444   → background:var(--border-strong)  (Zeile 646 m-btn disabled)
color:#666        → bleibt (Zeile 646)
color:#fff        → color:var(--white)  (Zeile 690)
background:#eab308 → background:var(--warning)  (Zeile 696)
color:#555        → color:var(--subtle)  (Zeile 698)
background:#2a2a2a → background:var(--code-inline-bg)  (Zeile 698 border)
color:#fff        → color:var(--white)  (Zeile 713 — Checkmark-Icon)
background:#3b82f6 → background:var(--accent)  (Zeile 729)
```

- [ ] `components/page-types.html` Zeilen 1–270 lesen
- [ ] `:root`, `*`, `body` aus `<style>`-Block entfernen, Links davor einfügen
- [ ] Inline-Farben ersetzen
- [ ] Browser-Check: Alle Seitentyp-Mockups korrekt dargestellt
- [ ] Commit:
```bash
git add components/page-types.html
git commit -m "fix(page-types-demo): replace inline token definitions with CSS file links"
```

---

## Abschluss-Notiz

`toast.html` wurde absichtlich nicht verändert — sie verwendet bereits die korrekte Struktur mit `<link>`-Tags und dient als Referenzimplementierung für alle anderen Dateien.

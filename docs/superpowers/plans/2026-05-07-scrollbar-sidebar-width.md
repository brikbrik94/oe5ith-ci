# Scrollbar-Stilisierung + Sidebar-Breite 300px — Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** CI-konformen dunklen Scrollbar global einführen und `--sidebar-width` auf 300px erhöhen.

**Architecture:** Ausschließlich `css/common.css` (Tokens + globale Scrollbar-Regeln) und Doku-Updates (`docs/tokens.md`, `CHANGELOG.md`). Keine Änderungen an anderen CSS-Dateien oder HTML-Komponenten — alle verwenden `--sidebar-width` via Token.

**Tech Stack:** CSS Custom Properties, CSS Scrollbar API (scrollbar-width/color + ::-webkit-scrollbar)

---

## Dateikarte

| Datei | Aktion | Was ändert sich |
|---|---|---|
| `css/common.css` | Modify | `--sidebar-width` 260→300px; neuer Scrollbar-Block nach `@media`-Reset |
| `docs/tokens.md` | Modify | `--sidebar-width` in Tabelle + in der `common.css`-Codeblock-Kopie aktualisieren; Änderungshistorie ergänzen |
| `CHANGELOG.md` | Modify | `v1.6.0`-Eintrag anlegen |

---

## Task 1: `--sidebar-width` von 260px auf 300px setzen

**Files:**
- Modify: `css/common.css:66`

- [ ] **Schritt 1: Token in `css/common.css` ändern**

Zeile 66 — ersetzen:
```css
  --sidebar-width:        260px;
```
durch:
```css
  --sidebar-width:        300px;
```

- [ ] **Schritt 2: Visuell prüfen**

`components/sidebar-types.html` im Browser öffnen. Alle 7 Sidebar-Typen müssen 300px breit sein. Typ 7 (Koordinaten-Umrechner, ganz unten): DMS-Zeilen (Lat./Lon. mit 3 schmalen Feldern) dürfen nicht mehr an den rechten Rand drängen.

- [ ] **Schritt 3: Commit**

```bash
git add css/common.css
git commit -m "fix: increase --sidebar-width to 300px"
```

---

## Task 2: Globale Scrollbar-Stilisierung in `css/common.css`

**Files:**
- Modify: `css/common.css` — nach dem `@media`-Block (nach Zeile 151, am Dateiende)

- [ ] **Schritt 1: Scrollbar-Block an das Ende von `css/common.css` anhängen**

Nach dem `@media (max-width: 768px)`-Block (derzeit letzter Block der Datei) einfügen:

```css

/* ── SCROLLBAR ── */
html {
  scrollbar-width: thin;
  scrollbar-color: var(--border-strong) transparent;
}

::-webkit-scrollbar        { width: 6px; height: 6px; }
::-webkit-scrollbar-track  { background: transparent; }
::-webkit-scrollbar-thumb  { background: var(--border-strong); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--subtle); }
```

- [ ] **Schritt 2: Visuell prüfen — Sidebar**

`components/sidebar-types.html` im Browser öffnen. Die Browserfenster-Höhe so verkleinern, dass in einem Sidebar-Mock ein Scrollbalken erscheint (z.B. Typ 7 bei kleiner Fensterhöhe). Der Scrollbalken muss:
- 6px breit sein (schmal, nicht der fette System-Standard)
- Dunkelgrauer Thumb (`#444444`) auf transparentem Track
- Beim Hover etwas heller (`#555555`)
- Kein weißer/grauer System-Scrollbalken sichtbar

- [ ] **Schritt 3: Visuell prüfen — Page Content**

`components/typography.html` oder `components/cards.html` im Browser öffnen, Fenster verkleinern bis ein Seitenscrollbalken erscheint. Gleiche Kriterien wie oben.

- [ ] **Schritt 4: Commit**

```bash
git add css/common.css
git commit -m "feat: add global CI scrollbar styling to common.css"
```

---

## Task 3: `docs/tokens.md` aktualisieren

**Files:**
- Modify: `docs/tokens.md`

- [ ] **Schritt 1: Tabelleneintrag `--sidebar-width` aktualisieren**

In der Tabelle „Spacing & Layout Tokens" (ca. Zeile 91) — ersetzen:
```markdown
| `--sidebar-width` | `260px` | Sidebar, alle Breakpoints |
```
durch:
```markdown
| `--sidebar-width` | `300px` | Sidebar, alle Breakpoints |
```

- [ ] **Schritt 2: `common.css`-Codeblock-Kopie aktualisieren**

Weiter unten in `tokens.md` gibt es einen vollständigen `common.css`-Codeblock (Abschnitt „Vollständige common.css"). Dort ebenfalls:
```css
  --sidebar-width:        260px;
```
durch:
```css
  --sidebar-width:        300px;
```
ersetzen. Und den Scrollbar-Block anhängen (nach `--shadow-toast`):

```css
/* ── Scrollbar ── */
html {
  scrollbar-width: thin;
  scrollbar-color: var(--border-strong) transparent;
}
::-webkit-scrollbar        { width: 6px; height: 6px; }
::-webkit-scrollbar-track  { background: transparent; }
::-webkit-scrollbar-thumb  { background: var(--border-strong); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--subtle); }
```

- [ ] **Schritt 3: Änderungshistorie ergänzen**

In der Tabelle „Änderungshistorie" am Ende von `tokens.md` eine neue Zeile ganz oben in der Tabelle einfügen:
```markdown
| 2026-05-07 | `--sidebar-width` von 260px auf 300px erhöht. Globale Scrollbar-Stilisierung (`scrollbar-width: thin`, `--border-strong`/transparent) ergänzt. |
```

- [ ] **Schritt 4: Commit**

```bash
git add docs/tokens.md
git commit -m "docs: update --sidebar-width to 300px and document scrollbar styling"
```

---

## Task 4: `CHANGELOG.md` — v1.6.0 anlegen

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Schritt 1: Neuen v1.6.0-Block einfügen**

Nach dem bestehenden `## v1.5.0`-Block (oder dem jeweils letzten Block) einen neuen Block einfügen:

```markdown
## v1.6.0 - 2026-05-07

### Added

- `css/common.css`: Globale Scrollbar-Stilisierung. 6px breiter Thumb in `--border-strong`
  auf transparentem Track. Hover-State `--subtle`. Unterstützt Firefox (`scrollbar-width`/
  `scrollbar-color`) und Chrome/Safari/Edge (`::-webkit-scrollbar`).

### Changed

- `css/common.css`: `--sidebar-width` von 260px auf 300px erhöht. Verbessert die Lesbarkeit
  von Formularen mit mehreren nebeneinanderstehenden Feldern (z.B. DMS-Zeilen im
  Koordinaten-Umrechner). Auf aktuellen Displays (≥1366px Breite) unproblematisch.
- `docs/tokens.md`: `--sidebar-width` und Änderungshistorie aktualisiert.

---
```

- [ ] **Schritt 2: Prüfen ob Versionsnummer korrekt**

Letzten Git-Tag prüfen:
```bash
git tag --sort=-version:refname | head -5
```
Wenn der letzte Tag `v1.5.x` ist, ist `v1.6.0` korrekt. Falls bereits `v1.6.x` existiert entsprechend anpassen.

- [ ] **Schritt 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "chore: update CHANGELOG.md for v1.6.0"
```

# Disclosure (Single-Panel) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eine generische, wiederverwendbare CI-Komponente `.disclosure` bauen — ein einzelnes, nativ auf `<details>`/`<summary>` basierendes auf-/zuklappbares Panel ohne Auswahlzustand, für Turn-by-Turn-Wegbeschreibungen und künftige Detail-Listen.

**Architecture:** Neue `css/disclosure.css`, ausschließlich Reuse bestehender Tokens und der `.badge`-Komponente — kein neuer Token nötig. Kein JS für Auf-/Zu (nativ über `<details>`), im Unterschied zu `.accordion`. Doku als neuer Abschnitt in `docs/sidebar.md` (kein eigenes Doc-File), Registry-Eintrag erweitert den bestehenden `sidebar`-Eintrag.

**Tech Stack:** Reines CSS + HTML. Kein Build, kein Test-Framework. Verifikation: `python3 scripts/cli/check_consistency.py`, Struktur-Greps, visuelle Kontrolle der Referenzseite im Browser.

## Global Constraints

- Keine hardcodierten Werte — nur Tokens aus `css/common.css` für Farben, Backgrounds, Borders, Radien, Schatten, Z-Index, Transitions.
- Keine neuen Komponentenklassen, wo bestehende passen. `.disclosure-count` **muss** `.badge` (aus `badges.css`) wiederverwenden — keine neue Badge-Variante.
- Hover-Hintergrund von `.disclosure-header` nutzt den bestehenden Token `--surface-hover` (rgba 0.05) — **nicht** den hardcodierten `.acc-header`-Wert (0.03) kopieren, keinen neuen Token einführen.
- Kein JS-Höhen-Contract: `.disclosure-body` bekommt keine `max-height`-Transition — `<details>` blendet nativ ein/aus. Das ist der zentrale Unterschied zu `.accordion`.
- `css/demo.css` ausschließlich in `components/disclosure.html`, nie produktiv.
- Jede produktive CSS muss in `css/index.css` importiert und in `docs/registry.json` registriert sein; `python3 scripts/cli/check_consistency.py` muss fehlerfrei sein.
- Version: additiv → MINOR `v1.19.0`. Filenames ohne Versionsnummer.
- Spec: `docs/superpowers/specs/2026-07-06-disclosure-component-design.md`.

---

### Task 1: `css/disclosure.css` (Komponenten-CSS + Import)

**Files:**
- Create: `css/disclosure.css`
- Modify: `css/index.css` (Import direkt nach `sidebar.css`)

**Interfaces:**
- Consumes: bestehende Tokens `--text`, `--muted`, `--border`, `--transition-base`, `--surface-hover`; bestehende Klasse `.badge` (`badges.css`).
- Produces: Klassen `.disclosure`, `.disclosure-header`, `.disclosure-title`, `.disclosure-count`, `.disclosure-chevron`, `.disclosure-body`, `.disclosure-item`, `.disclosure-item-text`, `.disclosure-item-meta` — von Task 2 (Referenz-HTML) konsumiert.

- [ ] **Step 1: `css/disclosure.css` schreiben**

```css
/*
 * OE5ITH CI — disclosure.css
 * Disclosure (Single-Panel): ein einzelnes auf-/zuklappbares Panel
 * ohne Auswahlzustand, nativ auf <details>/<summary> aufgebaut.
 * Kein JS für Auf-/Zu nötig (Unterschied zu .accordion in sidebar.css).
 *
 * Voraussetzung: css/common.css, css/badges.css (für .disclosure-count)
 */

/* ═══════════════════════════════════════
   WRAPPER
   ═══════════════════════════════════════ */
.disclosure {
  /* Kein eigener Rahmen zwingend — fügt sich in .panel/.panel-body ein */
}

/* ═══════════════════════════════════════
   HEADER (<summary>)
   ═══════════════════════════════════════ */
.disclosure-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  cursor: pointer;
  user-select: none;
  list-style: none;
  transition: background var(--transition-base);
}
.disclosure-header::-webkit-details-marker {
  display: none;
}
.disclosure-header:hover {
  background: var(--surface-hover);
}
.disclosure-header:focus-visible {
  outline: 2px solid var(--accent-border);
  outline-offset: -2px;
}

.disclosure-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* .disclosure-count erbt Optik vollständig von .badge (badges.css) */

.disclosure-chevron {
  font-size: 0.65rem;
  color: var(--muted);
  transition: transform var(--transition-base);
  flex-shrink: 0;
}
details.disclosure[open] .disclosure-chevron {
  transform: rotate(180deg);
}

/* ═══════════════════════════════════════
   BODY
   Kein max-height-Hack: <details> übernimmt
   Ein-/Ausblenden nativ.
   ═══════════════════════════════════════ */
.disclosure-body {
  padding: 4px 10px 8px;
}

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

/* ═══════════════════════════════════════
   REDUCED MOTION
   ═══════════════════════════════════════ */
@media (prefers-reduced-motion: reduce) {
  .disclosure-header,
  .disclosure-chevron {
    transition: none;
  }
}
```

- [ ] **Step 2: Import in `css/index.css` ergänzen**

Öffne `css/index.css`. Finde die Zeile `@import "sidebar.css";` (Block „Navigation", Zeile ~27). Füge direkt danach eine neue Zeile ein:

```css
@import "disclosure.css";
```

- [ ] **Step 3: Keine Rohwerte, Tokens verwendet — verifizieren**

Run: `grep -nE "#[0-9a-fA-F]{3,6}|rgba?\(|z-index" css/disclosure.css`
Expected: keine Treffer (keine hardcodierten Farben oder Z-Index).

Run: `grep -c "var(--" css/disclosure.css`
Expected: Zahl > 5 (Tokens werden mehrfach verwendet).

Run: `grep -n "disclosure.css" css/index.css`
Expected: 1 Treffer, direkt nach `sidebar.css`.

- [ ] **Step 4: Commit**

```bash
git add css/disclosure.css css/index.css
git commit -m "feat(disclosure): add disclosure.css (single-panel component)"
```

---

### Task 2: Referenz-HTML `components/disclosure.html`

**Files:**
- Create: `components/disclosure.html`

**Interfaces:**
- Consumes: Klassen aus Task 1 (`disclosure.css`), bestehende `.badge`, `.panel`/`.panel-header`/`.panel-title`/`.panel-body` (`page.css`).

- [ ] **Step 1: Struktur einer bestehenden Referenzseite als Vorlage ansehen**

Run: `sed -n '1,30p' components/split-view.html`
Ziel: `<head>`-Block (eingebundene CSS inkl. `demo.css` + FontAwesome) exakt übernehmen — analoges Muster für `components/disclosure.html` (einfache Demo-Seite ohne Sidebar/Topbar, wie `components/status-msg.html`; prüfen mit `sed -n '1,20p' components/status-msg.html` welches der beiden Muster näher passt — Disclosure braucht keine App-Sidebar, ein einfacher `demo-section`-Aufbau reicht).

- [ ] **Step 2: `components/disclosure.html` schreiben**

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Disclosure</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/badges.css">
<link rel="stylesheet" href="../css/page.css">
<link rel="stylesheet" href="../css/disclosure.css">
<link rel="stylesheet" href="../css/demo.css">
</head>
<body>

<div class="page-content">

  <!-- ═══ GESCHLOSSEN / OFFEN NEBENEINANDER ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Disclosure — Geschlossen / Offen</div>
    <div class="demo-section-desc">
      Einzelnes auf-/zuklappbares Panel ohne Auswahlzustand, nativ auf
      <code>&lt;details&gt;</code>/<code>&lt;summary&gt;</code> aufgebaut.
      Kein JS für Auf-/Zu nötig — Unterschied zum Accordion.
    </div>
    <div class="demo-row" style="align-items:flex-start; gap:16px;">

      <div class="panel" style="width:320px;">
        <div class="panel-body">
          <details class="disclosure">
            <summary class="disclosure-header">
              <span class="disclosure-title">Wegbeschreibung</span>
              <span class="disclosure-count badge">18 Schritte</span>
              <i class="fa-solid fa-chevron-down disclosure-chevron"></i>
            </summary>
            <div class="disclosure-body">
              <div class="disclosure-item">
                <span class="disclosure-item-text">Head northeast on Untere Donauländer, B129</span>
                <span class="disclosure-item-meta mono">280 m</span>
              </div>
              <div class="disclosure-item">
                <span class="disclosure-item-text">Turn right onto Welser Straße</span>
                <span class="disclosure-item-meta mono">1.2 km</span>
              </div>
            </div>
          </details>
        </div>
      </div>

      <div class="panel" style="width:320px;">
        <div class="panel-body">
          <details class="disclosure" open>
            <summary class="disclosure-header">
              <span class="disclosure-title">Wegbeschreibung</span>
              <span class="disclosure-count badge">18 Schritte</span>
              <i class="fa-solid fa-chevron-down disclosure-chevron"></i>
            </summary>
            <div class="disclosure-body">
              <div class="disclosure-item">
                <span class="disclosure-item-text">Head northeast on Untere Donauländer, B129</span>
                <span class="disclosure-item-meta mono">280 m</span>
              </div>
              <div class="disclosure-item">
                <span class="disclosure-item-text">Turn right onto Welser Straße, ein sehr langer Straßenname zum Testen der Ellipsis-Abschneidung im schmalen Panel</span>
                <span class="disclosure-item-meta mono">1.2 km</span>
              </div>
              <div class="disclosure-item">
                <span class="disclosure-item-text">Continue onto Kaiser-Josef-Platz</span>
                <span class="disclosure-item-meta mono">340 m</span>
              </div>
            </div>
          </details>
        </div>
      </div>

    </div>
  </div>

</div>

</body>
</html>
```

- [ ] **Step 3: Klassen-Existenz verifizieren**

Run: `grep -oE "class=\"[^\"]*\"" components/disclosure.html | grep -oE "badge[a-z-]*|panel[a-z-]*|disclosure[a-z-]*|demo-[a-z-]*" | sort -u`
Dann je Nicht-`disclosure-*`-Klasse prüfen: `grep -rn "<klasse>" css/badges.css css/page.css css/demo.css`
Expected: `.badge`, `.panel`, `.panel-body`, `.demo-section`, `.demo-section-title`, `.demo-section-desc`, `.demo-row` existieren jeweils in der referenzierten CSS-Datei.

- [ ] **Step 4: Visuell kontrollieren**

Öffne `components/disclosure.html` im Browser. Prüfe:
- Zwei Panels nebeneinander: linkes geschlossen (nur Header sichtbar), rechtes offen (Header + Items sichtbar).
- Chevron im offenen Zustand um 180° gedreht.
- Langer Item-Text im rechten Panel wird nicht umgebrochen, sondern bricht normal um (kein `white-space:nowrap` auf `.disclosure-item-text` — nur bei `.disclosure-title` Ellipsis vorgesehen). Falls das Layout dadurch unschön wirkt, im CSS (Task 1) prüfen ob Ellipsis auf `.disclosure-item-text` sinnvoller ist, und ggf. nachziehen.
- Klick auf Header klappt auf/zu (nativ, kein JS-Fehler in der Konsole).
- Tab-Taste: Header fokussierbar mit sichtbarem Fokusrahmen; Enter/Space klappt auf/zu (native `<summary>`-Semantik).
- `prefers-reduced-motion` in den Browser-DevTools simulieren: Chevron dreht ohne Transition (sofort).

- [ ] **Step 5: Commit**

```bash
git add components/disclosure.html
git commit -m "docs(disclosure): add components/disclosure.html reference page"
```

---

### Task 3: Doku `docs/sidebar.md` — Abschnitt „Disclosure (Single-Panel)"

**Files:**
- Modify: `docs/sidebar.md`

**Interfaces:**
- Consumes: Klassen aus Task 1 (für Element-Tabelle).

- [ ] **Step 1: Einfügeposition bestimmen**

Der neue Abschnitt gehört fachlich neben „Accordion-Gruppen" (aktuell Zeile 189–310 in `docs/sidebar.md`, endet vor „## Sidebar Footer"). Run: `grep -n "^## " docs/sidebar.md` um die exakte aktuelle Zeilennummer von „## Sidebar Footer" zu finden (kann sich durch frühere Änderungen verschoben haben).

- [ ] **Step 2: Abschnitt vor „## Sidebar Footer" einfügen**

```markdown
## Disclosure (Single-Panel)

Einzelnes auf-/zuklappbares Panel ohne Auswahlzustand. Nativ auf
`<details>`/`<summary>` aufgebaut — **kein JS** für Auf-/Zuklappen nötig,
im Unterschied zum Accordion.

### Wann Accordion, wann Disclosure

| Situation | Komponente |
|---|---|
| Mehrere gleichartige, unabhängig togglebare Kategorien mit Status pro Kategorie (z.B. Layer-Gruppen) | `.accordion` |
| Einzelne Kopfzeile klappt einen Inhaltsbereich auf/zu, kein Auswahlzustand, keine Checkbox-Liste (z.B. Turn-by-Turn-Wegbeschreibung) | `.disclosure` |

### Struktur

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

### Klassen

| Klasse | Zweck |
|---|---|
| `.disclosure` | Wrapper (`<details>`). Kein eigener Rahmen nötig — in `.panel`/`.panel-body` einbetten. |
| `.disclosure-header` | `<summary>`. Klickbar, Hover-BG `--surface-hover`, nativer Marker entfernt. |
| `.disclosure-title` | Primärtext. |
| `.disclosure-count` | Zähler/Badge — reuse `.badge`, **keine** neue Badge-Variante. |
| `.disclosure-chevron` | Rotiert bei `details[open]`, analog `.acc-chevron`. |
| `.disclosure-body` | Inhaltscontainer. Kein JS-Höhen-Contract — `<details>` blendet nativ ein/aus. |
| `.disclosure-item` | Einzelner Eintrag: Text · Meta. |
| `.disclosure-item-text` | Primärtext. |
| `.disclosure-item-meta` | Sekundärtext rechts, `--muted`. |

### Beispiel

```html
<details class="disclosure">
  <summary class="disclosure-header">
    <span class="disclosure-title">Wegbeschreibung</span>
    <span class="disclosure-count badge">18 Schritte</span>
    <i class="fa-solid fa-chevron-down disclosure-chevron"></i>
  </summary>
  <div class="disclosure-body">
    <div class="disclosure-item">
      <span class="disclosure-item-text">Head northeast on Untere Donauländer, B129</span>
      <span class="disclosure-item-meta">280 m</span>
    </div>
  </div>
</details>
```

### Regeln

1. Kein JS für Auf-/Zuklappen — `<details>`/`<summary>` übernimmt das nativ.
2. `.disclosure-count` reuse `.badge` — keine neue Badge-Variante anlegen.
3. Hover-Hintergrund immer `--surface-hover`, nie hardcodiert.
4. Für Gruppen mit Auswahlzustand/Checkboxen/Status-Badge weiterhin `.accordion` verwenden, nicht `.disclosure`.
```

- [ ] **Step 3: Änderungshistorie ergänzen**

Am Ende der Tabelle „## Änderungshistorie" (Zeile ~382 in der alten Version — Position mit `grep -n "^## Änderungshistorie"` neu bestimmen) eine Zeile hinzufügen:

```markdown
| 2026-07-06 | Disclosure (Single-Panel) ergänzt — `.disclosure`, Abgrenzung zu Accordion. |
```

- [ ] **Step 4: Verifizieren**

Run: `grep -n "Disclosure\|disclosure-" docs/sidebar.md`
Expected: neuer Abschnitt, alle 8 Klassen aus Task 1 kommen in der Tabelle vor, Änderungshistorie-Zeile vorhanden.

- [ ] **Step 5: Commit**

```bash
git add docs/sidebar.md
git commit -m "docs(sidebar): add Disclosure (Single-Panel) section"
```

---

### Task 4: Registry, Consistency-Check, Changelog, Version

**Files:**
- Modify: `docs/registry.json`
- Modify: `CHANGELOG.md`
- Modify: `README.md` (auto-generiert durch check_consistency)

**Interfaces:**
- Consumes: alle Artefakte aus Task 1–3.

- [ ] **Step 1: Bestehenden `sidebar`-Registry-Eintrag erweitern**

In `docs/registry.json` den bestehenden Eintrag mit `"id": "sidebar"` finden (aktuell):

```json
    { "id": "sidebar", "title": "Sidebar + Accordion", "category": "component",
      "css": ["sidebar.css"], "doc": ["sidebar.md", "sidebar-types.md"],
      "html": ["sidebar.html", "sidebar-types.html"] },
```

Ersetzen durch:

```json
    { "id": "sidebar", "title": "Sidebar + Accordion + Disclosure", "category": "component",
      "css": ["sidebar.css", "disclosure.css"], "doc": ["sidebar.md", "sidebar-types.md"],
      "html": ["sidebar.html", "sidebar-types.html", "disclosure.html"] },
```

Auf gültiges JSON achten (Komma-Platzierung unverändert lassen, nur die vier Arrays anpassen).

- [ ] **Step 2: Consistency-Check (Gate)**

Run: `python3 scripts/cli/check_consistency.py`
Expected: keine Fehler.

- [ ] **Step 3: README regenerieren**

Run: `python3 scripts/cli/check_consistency.py --write`
Expected: README-Blöcke aktualisiert, weiterhin keine Fehler.

- [ ] **Step 4: CHANGELOG ergänzen**

Der aktuelle oberste Eintrag in `CHANGELOG.md` ist (Stand dieses Plans)
`## v1.18.1 - 2026-07-06` (Modal-Backdrop-Fix). Finde diese Zeile mit
`grep -n "^## v" CHANGELOG.md | head -3` — falls sich der oberste Eintrag
inzwischen geändert hat, den neuen Block **darüber** einfügen, sonst direkt
über `## v1.18.1 - 2026-07-06`:

```markdown
## v1.19.0 - 2026-07-06

### Added
- **Disclosure (Single-Panel)** — generische Komponente für ein einzelnes auf-/zuklappbares Panel ohne Auswahlzustand, nativ auf `<details>`/`<summary>` aufgebaut, kein JS nötig. Neue `css/disclosure.css`, Referenz `components/disclosure.html`, Doku-Abschnitt in `docs/sidebar.md` (Abgrenzung zu `.accordion`). Keine neuen Tokens — reuse `.badge`, `--surface-hover`.

---
```

Halte dich exakt an das bestehende CHANGELOG-Format (`## vX.Y.Z - YYYY-MM-DD`, Kategorien `Added`/`Changed`/`Fixed`, Trennlinie `---` danach).

- [ ] **Step 5: Finale Verifikation**

Run: `python3 scripts/cli/check_consistency.py`
Expected: keine Fehler.

Run: `grep -n "disclosure" docs/registry.json README.md CHANGELOG.md`
Expected: in allen drei Dateien vorhanden.

- [ ] **Step 6: Commit**

```bash
git add docs/registry.json README.md CHANGELOG.md
git commit -m "docs(disclosure): register component, changelog v1.19.0"
```

---

## Hinweis zur Versionierung (nach Plan-Abschluss, nicht Teil der Tasks)

Tag erst nach Freigabe durch den User setzen:

```bash
git tag -a v1.19.0 -m "Release v1.19.0 — Disclosure (Single-Panel)"
git push origin main --tags
```

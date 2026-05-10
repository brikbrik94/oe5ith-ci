# Topbar-Verbesserungen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Drei Topbar-Verbesserungen: Dropdown-Menü-Breite fixieren, Icon-only Toggle-Modifier einführen, Rechts-Nav-Dropdown als neue Komponente hinzufügen.

**Architecture:** Reine CSS/HTML-Erweiterungen ohne Build-Step. Alle CSS-Änderungen in `css/topbar.css`, Demo-Updates in `components/topbar.html`, Dokumentation in `docs/topbar.md`. Keine neuen Dateien, keine Breaking Changes.

**Tech Stack:** CSS Custom Properties (aus `css/common.css`), Vanilla JS (Demo-only), HTML5

**Design-Spec:** `docs/superpowers/specs/2026-05-10-topbar-improvements-design.md`

---

## Dateien

| Datei | Änderung |
|---|---|
| `css/topbar.css` | min-width Fix · `.topbar-toggle--icon-only` · `.topbar-nav-dropdown` |
| `components/topbar.html` | Icon-only Demo-Button · Nav-Dropdown Demo + JS |
| `docs/topbar.md` | Drei neue Regelabschnitte |

---

## Task 1: Dropdown min-width Fix

**Files:**
- Modify: `css/topbar.css`

- [ ] **Step 1: CSS ändern**

In `css/topbar.css` die Zeile `min-width: 180px;` im Block `.topbar-dropdown-menu` auf `min-width: 100%;` setzen:

```css
/* ALT: */
.topbar-dropdown-menu {
  display: none;
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  background: #1f1f1f;
  border: 1px solid #4b5563;
  border-radius: 6px;
  min-width: 180px;
  z-index: var(--z-dropdown);
  padding: 4px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}

/* NEU: */
.topbar-dropdown-menu {
  display: none;
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  background: #1f1f1f;
  border: 1px solid #4b5563;
  border-radius: 6px;
  min-width: 100%;
  z-index: var(--z-dropdown);
  padding: 4px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}
```

- [ ] **Step 2: Visuell prüfen**

`components/topbar.html` im Browser öffnen.  
Dropdown aufklappen → Menü darf nicht breiter als der Toggle-Button (140px) sein.  
Erwartetes Ergebnis: Toggle-Button und aufgeklapptes Menü haben identische Breite.

- [ ] **Step 3: Commit**

```bash
git add css/topbar.css
git commit -m "fix: align topbar dropdown menu width to toggle button (min-width: 100%)"
```

---

## Task 2: Modifier `.topbar-toggle--icon-only`

**Files:**
- Modify: `css/topbar.css`
- Modify: `components/topbar.html`

- [ ] **Step 1: CSS einfügen**

In `css/topbar.css` direkt nach dem Block `.topbar-toggle.active .topbar-toggle-indicator { ... }` (Ende des TOGGLE BUTTON Abschnitts) folgenden Block einfügen:

```css
/* ═══════════════════════════════════════
   TOGGLE — ICON-ONLY MODIFIER
   ═══════════════════════════════════════ */

/* Desktop: Label verbergen */
.controls-panel .topbar-toggle--icon-only .topbar-toggle-label {
  display: none;
}

/* Desktop: Tooltip via CSS */
.controls-panel .topbar-toggle--icon-only[data-tooltip] {
  position: relative;
}

.controls-panel .topbar-toggle--icon-only[data-tooltip]:hover::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 0.75rem;
  color: var(--text);
  white-space: nowrap;
  z-index: var(--z-tooltip);
  pointer-events: none;
}

/* Overlay: Label immer sichtbar */
.controls-overlay .topbar-toggle--icon-only .topbar-toggle-label {
  display: inline;
}
```

- [ ] **Step 2: Demo-Button in topbar.html einfügen**

In `components/topbar.html` nach dem Button `id="btn1"` (Ende: `</button>`) einen neuen Icon-only Button einfügen:

```html
<!-- Icon-Only Toggle Button -->
<button class="topbar-toggle topbar-toggle--icon-only"
        data-tooltip="Hillshade"
        aria-pressed="false"
        id="btn-hillshade">
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.3">
    <circle cx="7" cy="7" r="3"/>
    <line x1="7" y1="1" x2="7" y2="3"/>
    <line x1="7" y1="11" x2="7" y2="13"/>
    <line x1="1" y1="7" x2="3" y2="7"/>
    <line x1="11" y1="7" x2="13" y2="7"/>
  </svg>
  <span class="topbar-toggle-label">Hillshade</span>
</button>
```

- [ ] **Step 3: Icon-only Clone in buildControlsOverlay() ergänzen**

In `components/topbar.html` in der Funktion `buildControlsOverlay()` nach dem Toggle-Clone (`overlay.appendChild(tClone);`) folgenden Block einfügen:

```js
  // Icon-only Toggle clone (Label im Overlay immer sichtbar)
  const icClone = document.createElement('button');
  icClone.className = 'topbar-toggle';
  icClone.style.cssText = 'width:100%;justify-content:center;gap:8px';
  icClone.innerHTML = `<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.3"><circle cx="7" cy="7" r="3"/><line x1="7" y1="1" x2="7" y2="3"/><line x1="7" y1="11" x2="7" y2="13"/><line x1="1" y1="7" x2="3" y2="7"/><line x1="11" y1="7" x2="13" y2="7"/></svg><span>Hillshade</span>`;
  let hillshadeActive = false;
  icClone.addEventListener('click', () => {
    hillshadeActive = !hillshadeActive;
    icClone.classList.toggle('active', hillshadeActive);
    const desktopBtn = document.getElementById('btn-hillshade');
    if (desktopBtn) desktopBtn.classList.toggle('active', hillshadeActive);
    log(`Hillshade → ${hillshadeActive ? 'aktiviert' : 'deaktiviert'}`);
  });
  overlay.appendChild(icClone);
```

- [ ] **Step 4: JS für btn-hillshade Demo ergänzen**

In `components/topbar.html` in der JS-Sektion (beim NAV LINKS Block) folgenden Block hinzufügen:

```js
/* ═══════════════════════════════════════
   ICON-ONLY TOGGLE (Hillshade Demo)
   ═══════════════════════════════════════ */
let hillshadeOn = false;
$('btn-hillshade').addEventListener('click', () => {
  hillshadeOn = !hillshadeOn;
  $('btn-hillshade').classList.toggle('active', hillshadeOn);
  $('btn-hillshade').setAttribute('aria-pressed', hillshadeOn);
  log(`Hillshade → ${hillshadeOn ? 'aktiviert' : 'deaktiviert'}`);
});
```

- [ ] **Step 5: Visuell prüfen**

`components/topbar.html` im Browser öffnen.

Desktop (≥1025px):
- Hillshade-Button zeigt nur das Icon (kein Text)
- Hover über den Button → Tooltip "Hillshade" erscheint oberhalb
- Klick → Button wechselt in aktiven Zustand (blauer Hintergrund)

Tablet/Mobile (Fenster auf <1025px verkleinern):
- Controls-Panel öffnen → Hillshade-Button zeigt Icon + Text "Hillshade" nebeneinander

- [ ] **Step 6: Commit**

```bash
git add css/topbar.css components/topbar.html
git commit -m "feat: add .topbar-toggle--icon-only modifier with CSS tooltip and overlay label"
```

---

## Task 3: Komponente `.topbar-nav-dropdown`

**Files:**
- Modify: `css/topbar.css`
- Modify: `components/topbar.html`

- [ ] **Step 1: CSS einfügen**

In `css/topbar.css` direkt nach dem Block `.topbar-nav-link.active { ... }` (Ende des NAV LINKS Abschnitts) folgenden Block einfügen:

```css
/* ═══════════════════════════════════════
   RIGHT — NAV DROPDOWN
   ═══════════════════════════════════════ */
.topbar-nav-dropdown {
  position: relative;
}

.topbar-nav-dropdown-toggle {
  background: none;
  border: none;
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  height: 36px;
  white-space: nowrap;
  font-family: inherit;
  transition: color var(--transition-fast), background var(--transition-fast);
}

.topbar-nav-dropdown-toggle:hover,
.topbar-nav-dropdown-toggle.open {
  color: var(--text);
  background: rgba(255, 255, 255, 0.05);
}

.topbar-nav-dropdown-toggle .chevron {
  font-size: 0.65rem;
  transition: transform 0.2s;
  flex-shrink: 0;
}

.topbar-nav-dropdown-toggle.open .chevron {
  transform: rotate(180deg);
}

.topbar-nav-dropdown-menu {
  display: none;
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 6px;
  min-width: 160px;
  z-index: var(--z-dropdown);
  padding: 4px;
  box-shadow: var(--shadow-dropdown);
}

.topbar-nav-dropdown-menu.open {
  display: block;
}

.topbar-nav-dropdown-item {
  display: flex;
  align-items: center;
  padding: 8px 10px;
  border-radius: 4px;
  font-size: 0.82rem;
  color: var(--text);
  text-decoration: none;
  transition: background 0.1s;
}

.topbar-nav-dropdown-item:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #fff;
}

.topbar-nav-dropdown-item.active {
  color: var(--accent);
}
```

- [ ] **Step 2: Mobile Breakpoint einfügen**

In `css/topbar.css` im bestehenden Block `@media (max-width: 768px) { .topbar-nav-link { display: none !important; } ... }` (ganz unten in der Datei) eine Zeile ergänzen:

```css
@media (max-width: 768px) {
  .topbar-nav-link { display: none !important; }
  .topbar .nav-list { display: none !important; }
  .topbar-nav-dropdown { display: none !important; }
}
```

- [ ] **Step 3: HTML in topbar.html ersetzen**

In `components/topbar.html` den Block `<div class="topbar-right">` mit den drei `topbar-nav-link`-Einträgen durch folgendes ersetzen:

```html
  <!-- RECHTS: Nav Dropdown -->
  <div class="topbar-right">
    <div class="topbar-nav-dropdown" id="nav-dropdown-wrap">
      <button class="topbar-nav-dropdown-toggle" id="nav-dropdown-toggle"
              aria-haspopup="true" aria-expanded="false">
        Portale
        <span class="chevron">▾</span>
      </button>
      <div class="topbar-nav-dropdown-menu" id="nav-dropdown-menu">
        <a href="#" class="topbar-nav-dropdown-item" data-link="1">Portal 1</a>
        <a href="#" class="topbar-nav-dropdown-item" data-link="2">Portal 2</a>
        <a href="#" class="topbar-nav-dropdown-item active" data-link="3">Portal 3</a>
      </div>
    </div>
  </div>
```

- [ ] **Step 4: JS-Block NAV LINKS ersetzen**

In `components/topbar.html` den bestehenden JS-Block `/* NAV LINKS */` (mit den `querySelectorAll('.topbar-nav-link')`) durch folgenden Block ersetzen:

```js
/* ═══════════════════════════════════════
   NAV DROPDOWN
   ═══════════════════════════════════════ */
let navDropdownOpen = false;

function setNavDropdown(open) {
  navDropdownOpen = open;
  $('nav-dropdown-menu').classList.toggle('open', open);
  $('nav-dropdown-toggle').classList.toggle('open', open);
  $('nav-dropdown-toggle').setAttribute('aria-expanded', open);
}

$('nav-dropdown-toggle').addEventListener('click', e => {
  e.stopPropagation();
  setNavDropdown(!navDropdownOpen);
  log(`Portale-Dropdown → ${navDropdownOpen ? 'geöffnet' : 'geschlossen'}`);
});

document.querySelectorAll('.topbar-nav-dropdown-item').forEach(item => {
  item.addEventListener('click', e => {
    e.preventDefault();
    document.querySelectorAll('.topbar-nav-dropdown-item').forEach(i => i.classList.remove('active'));
    item.classList.add('active');
    log(`Portal → "Portal ${item.dataset.link}" geklickt`);
    setNavDropdown(false);
  });
});

document.addEventListener('click', e => {
  if (navDropdownOpen && !$('nav-dropdown-wrap').contains(e.target)) {
    setNavDropdown(false);
  }
});
```

- [ ] **Step 5: Escape-Handler erweitern**

In `components/topbar.html` im bestehenden `keydown`-Listener (Escape-Block) den Nav-Dropdown schließen ergänzen:

```js
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    if (controlsOpen) setControls(false);
    if (sidebarOpen && window.innerWidth <= 768) setSidebar(false);
    if (dropdownOpen) setDropdown(false);
    if (navDropdownOpen) setNavDropdown(false);
  }
});
```

- [ ] **Step 6: Visuell prüfen**

`components/topbar.html` im Browser öffnen.

Desktop (≥1025px):
- Rechts oben: Button "Portale ▾" sichtbar (keine separaten Links)
- Klick → Dropdown öffnet sich rechts ausgerichtet mit drei Portal-Links
- Klick auf einen Link → Link wird aktiv, Dropdown schließt
- Klick außerhalb oder Escape → Dropdown schließt

Mobile (Fenster auf ≤768px verkleinern):
- "Portale ▾" Button ist ausgeblendet

- [ ] **Step 7: Commit**

```bash
git add css/topbar.css components/topbar.html
git commit -m "feat: add .topbar-nav-dropdown component for right-side navigation"
```

---

## Task 4: Dokumentation `docs/topbar.md`

**Files:**
- Modify: `docs/topbar.md`

- [ ] **Step 1: Dropdown-Menü-Breite dokumentieren**

In `docs/topbar.md` im Abschnitt `### Dropdown — Fixe Breite (Pflicht)` nach dem Toggle-Breite-Codeblock folgenden Abschnitt einfügen:

```markdown
**Menü-Breite:**
```css
.topbar-dropdown-menu {
  min-width: 100%;  /* mindestens so breit wie der Toggle */
}
```
Das Menü ist immer mindestens so breit wie sein Toggle-Button — nie schmaler.  
Wenn einzelne Einträge länger sind als der Toggle, darf das Menü breiter werden.
```

- [ ] **Step 2: Modifier `.topbar-toggle--icon-only` dokumentieren**

In `docs/topbar.md` direkt vor dem Abschnitt `## Zone: Rechts` einen neuen Abschnitt einfügen:

```markdown
### Schaltflächen: Icon-only Modifier

Toggle-Schaltflächen können mit `.topbar-toggle--icon-only` als reine Icon-Buttons dargestellt werden.

| Kontext | Darstellung |
|---|---|
| Desktop (`controls-panel`) | Nur Icon — Text als Tooltip bei Hover |
| Tablet/Mobile (`controls-overlay`) | Icon + Text immer sichtbar |

**HTML (Pflichtfelder):**
```html
<button class="topbar-toggle topbar-toggle--icon-only"
        data-tooltip="Hillshade"
        aria-pressed="false">
  <svg>…</svg>
  <span class="topbar-toggle-label">Hillshade</span>
</button>
```

Regeln:
- `data-tooltip` und der Text im `.topbar-toggle-label`-Span müssen identisch sein.
- Ohne `data-tooltip` und `.topbar-toggle-label` ist der Modifier nicht erlaubt.
- Der Tooltip erscheint mittig oberhalb des Buttons via CSS `::after`.
```

- [ ] **Step 3: `.topbar-nav-dropdown` in Zone: Rechts dokumentieren**

In `docs/topbar.md` im Abschnitt `## Zone: Rechts` nach der bestehenden Tabelle (Breakpoint-Verhalten der Links) folgenden Abschnitt anhängen:

```markdown
### Nav Dropdown (`.topbar-nav-dropdown`)

Ersetzt mehrere einzelne `.topbar-nav-link`-Einträge wenn mehr als 2–3 Links benötigt werden.

> **Regel:** `.topbar-nav-dropdown` und `.topbar-nav-link` nie gleichzeitig in `topbar-right` verwenden.

**HTML:**
```html
<div class="topbar-nav-dropdown">
  <button class="topbar-nav-dropdown-toggle"
          aria-haspopup="true" aria-expanded="false">
    Portale
    <span class="chevron">▾</span>
  </button>
  <div class="topbar-nav-dropdown-menu">
    <a href="#" class="topbar-nav-dropdown-item">Link 1</a>
    <a href="#" class="topbar-nav-dropdown-item active">Link 2</a>
    <a href="#" class="topbar-nav-dropdown-item">Link 3</a>
  </div>
</div>
```

- Label ("Portale") ist frei wählbar im HTML — keine CSS-Änderung nötig.
- Menü öffnet sich **rechts ausgerichtet** (`right: 0`).

**Breakpoints:**

| Breakpoint | Verhalten |
|---|---|
| Desktop ≥1025px | Vollständig sichtbar |
| Tablet 769–1024px | Vollständig sichtbar |
| Mobile ≤768px | Ausgeblendet (`display: none !important`) |
```

- [ ] **Step 4: Änderungshistorie ergänzen**

In `docs/topbar.md` am Ende in der Tabelle `## Änderungshistorie` eine Zeile hinzufügen:

```markdown
| 2026-05-10 | Dropdown min-width Fix · `.topbar-toggle--icon-only` Modifier · `.topbar-nav-dropdown` Komponente |
```

- [ ] **Step 5: Commit**

```bash
git add docs/topbar.md
git commit -m "docs: update topbar.md with dropdown width rule, icon-only modifier, nav dropdown"
```

---

## Task 5: Push

- [ ] **Push to main**

```bash
git push origin main
```

Erwartetes Ergebnis: Alle Commits aus Tasks 1–4 sind auf `origin/main`.

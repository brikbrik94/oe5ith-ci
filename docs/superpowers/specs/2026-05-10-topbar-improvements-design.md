# Design: Topbar-Verbesserungen

**Datum:** 2026-05-10  
**Scope:** `css/topbar.css`, `components/topbar.html`, `docs/topbar.md`  
**Version:** MINOR (neue Komponente + neue Modifier-Klasse)

---

## Überblick

Drei unabhängige, dokumentierte Verbesserungen der Topbar-Komponente:

1. **Dropdown-Breite** — Menü-Breite korrigiert (war: 180px Minimum, soll: mindestens so breit wie Toggle-Button)
2. **Schaltflächen-Darstellung** — Neuer Modifier `.topbar-toggle--icon-only` mit kontextsensitivem Tooltip/Label
3. **Rechts-Navigation** — Neue Komponente `.topbar-nav-dropdown` für platzsparende Link-Gruppen

---

## 1. Dropdown-Breite

### Problem

`.topbar-dropdown-toggle` hat eine fixe Breite (Standard: `140px`).  
`.topbar-dropdown-menu` hatte `min-width: 180px` — das Menü öffnete sich stets breiter als der Button.

### Lösung

`min-width: 180px` wird ersetzt durch `min-width: 100%` (relativ zum `.topbar-dropdown`-Container).

```css
.topbar-dropdown-menu {
  min-width: 100%;  /* war: 180px */
}
```

### Regel

Das Dropdown-Menü ist immer mindestens so breit wie sein Toggle-Button.  
Wenn einzelne Einträge länger sind als der Toggle, darf das Menü natürlich breiter werden — aber nie schmaler.

---

## 2. Schaltflächen-Darstellung: `.topbar-toggle--icon-only`

### Ziel

Toggle-Schaltflächen in der Topbar-Mitte können kompakt als Icon-only dargestellt werden.  
Der beschreibende Text erscheint kontextsensitiv:

| Kontext | Darstellung |
|---|---|
| Desktop (`controls-panel`) | Nur Icon — Text erscheint als Tooltip bei Hover |
| Tablet/Mobile (`controls-overlay`) | Icon + Text immer sichtbar |

### HTML-Struktur

```html
<button class="topbar-toggle topbar-toggle--icon-only"
        data-tooltip="Hillshade"
        aria-pressed="false">
  <svg>…</svg>
  <span class="topbar-toggle-label">Hillshade</span>
</button>
```

**Pflichtfelder beim Einsatz von `.topbar-toggle--icon-only`:**
- `data-tooltip="…"` — Text für den Desktop-Tooltip
- `.topbar-toggle-label`-Span — Text für das Overlay

`data-tooltip` und der Text im `.topbar-toggle-label`-Span müssen identisch sein.  
Ohne beide Felder ist der Modifier nicht erlaubt.

### CSS

```css
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

---

## 3. Rechts-Navigation: `.topbar-nav-dropdown`

### Ziel

Ersetzt mehrere einzelne `.topbar-nav-link`-Einträge in `topbar-right` durch ein aufklappbares Menü mit frei wählbarem Label (z.B. "Portale", "Websites").

**Regel:** `.topbar-nav-dropdown` und `.topbar-nav-link` nie gleichzeitig in `topbar-right` verwenden, wenn mehr als 2 Ziele vorhanden sind.

### HTML-Struktur

```html
<div class="topbar-nav-dropdown">
  <button class="topbar-nav-dropdown-toggle"
          aria-haspopup="true"
          aria-expanded="false">
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

Das Label ("Portale") ist frei wählbar im HTML — keine CSS-Änderung erforderlich.

### Optik

Der Toggle sieht aus wie ein `topbar-nav-link` mit Chevron — kein Rahmen, kein Hintergrund im Ruhezustand. Hover: subtiler Hintergrund identisch zu `.topbar-nav-link:hover`.

Das Menü öffnet sich **rechts ausgerichtet** (`right: 0`), da die Komponente am rechten Bildschirmrand sitzt.

### CSS

```css
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

### Breakpoints

| Breakpoint | Verhalten |
|---|---|
| Desktop ≥1025px | Vollständig sichtbar |
| Tablet 769–1024px | Vollständig sichtbar — ersetzt bisher ausgeblendete Links ab dem 3. |
| Mobile ≤768px | Ausgeblendet (`display: none !important`) |

```css
@media (max-width: 768px) {
  .topbar-nav-dropdown { display: none !important; }
}
```

### JavaScript (minimal)

```js
const navDropdownToggle = document.querySelector('.topbar-nav-dropdown-toggle');
const navDropdownMenu   = document.querySelector('.topbar-nav-dropdown-menu');

if (navDropdownToggle && navDropdownMenu) {
  navDropdownToggle.addEventListener('click', () => {
    const open = navDropdownMenu.classList.toggle('open');
    navDropdownToggle.classList.toggle('open', open);
    navDropdownToggle.setAttribute('aria-expanded', open);
  });

  document.addEventListener('click', e => {
    if (!navDropdownToggle.closest('.topbar-nav-dropdown').contains(e.target)) {
      navDropdownMenu.classList.remove('open');
      navDropdownToggle.classList.remove('open');
      navDropdownToggle.setAttribute('aria-expanded', false);
    }
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      navDropdownMenu.classList.remove('open');
      navDropdownToggle.classList.remove('open');
      navDropdownToggle.setAttribute('aria-expanded', false);
    }
  });
}
```

---

## Änderungen im Überblick

| Datei | Änderung |
|---|---|
| `css/topbar.css` | `min-width` Fix · `.topbar-toggle--icon-only` · `.topbar-nav-dropdown` |
| `components/topbar.html` | Neue Demo-Sektionen für alle drei Änderungen |
| `docs/topbar.md` | Dokumentation der neuen Regeln und Komponente |

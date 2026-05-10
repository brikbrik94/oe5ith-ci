# Topbar

**Referenz-Datei:** `components/topbar.html`  
**Status:** definiert · v1.0

---

## Überblick

Die Topbar ist das markanteste Element jeder Seite. Sie ist auf allen Seiten und Breakpoints
strukturell identisch — Inhalt und Verhalten variieren je nach Seitentyp.

**Drei Zonen:** `topbar-left` · `topbar-center` · `topbar-right`

---

## Abmessungen

| Breakpoint | Höhe | Padding |
|---|---|---|
| Desktop ≥1025px | `60px` | `0 20px` |
| Tablet 769–1024px | `60px` | `0 20px` |
| Mobile ≤768px | `52px` | `0 14px` |

**Hintergrund:** `--card-bg` (#252525)  
**Unterstrich:** `2px solid --accent` — immer, auf allen Seiten

---

## Zone: Links (`topbar-left`)

Enthält immer: **Logo** + **Seitenname**

### Desktop + Tablet (≥769px)
- SVG-Logo links, monochrom blau (`--accent`)
- Seitenname: CAPS, `font-size: 1.2rem`, `font-weight: 700`, `letter-spacing: 1px`
- Zusammen als klickbarer Link → Homepage der jeweiligen Site

### Mobile (≤768px)
- **Kein Logo** — nur kurzer Seitenname (1 Wort), kein Icon
- `font-size: 1rem`, `letter-spacing: 0.5px`
- Klickbar → Homepage

```css
.brand { display: flex; align-items: center; gap: 9px; color: #fff;
         font-weight: 700; font-size: 1.2rem; letter-spacing: 1px; }

@media (max-width: 768px) {
  .brand-logo { display: none; }
  .brand { font-size: 1rem; letter-spacing: 0.5px; }
}
```

---

## Zone: Mitte (`topbar-center`)

Nur auf **Tool-Seiten** (z.B. Karte) befüllt. Auf allen anderen Seiten leer.

### Mögliche Elemente (in `topbar.html` als Referenz definiert)

| Element | ID/Klasse | Beschreibung |
|---|---|---|
| Dropdown | `#dropdown-wrap` | Auswahlmenü, öffnet nach unten. Fixe Breite — springt nie. |
| Toggle Button | `#btn1` / `.topbar-toggle` | Ein/Aus-Schalter mit Zustandsindikator |
| Searchbar | `#search-wrap` | Texteingabe + Such-Icon-Button, Ergebnis als kurzes Overlay |

### Dropdown — Fixe Breite (Pflicht)

Der Toggle-Button eines Dropdowns muss eine **fest definierte Breite** haben.
Die Breite darf sich beim Wechsel der Auswahl **nicht** ändern — die Topbar darf nicht springen.

**Regel:**
```css
.topbar-dropdown-toggle {
  width: 140px;  /* fix — immer explizit setzen */
}
```

Die Breite wird **einmalig** beim Anlegen des Dropdowns festgelegt, orientiert am längsten Options-Text:

| Faustformel | Wert |
|---|---|
| Zeichenbreite bei `font-size: 0.82rem` | ~7px pro Zeichen |
| Padding links + rechts | 24px |
| Chevron + Gap | ~20px |
| **Beispiel: „Option 1" (8 Zeichen)** | `8 × 7 + 44 = ~100px` → auf `120px` aufrunden |

> **Für dynamische Dropdowns** (Optionen kommen aus einer API oder ändern sich):  
> Die Breite muss trotzdem fix sein. Entweder einen konservativen Maximalwert hardcoden,
> oder beim Laden einmalig die längste Option messen und die Breite programmatisch setzen —
> danach nicht mehr ändern.

```js
// Einmaliges Messen beim Laden (optional, für dynamische Optionen)
const longest = options.reduce((a, b) => a.length >= b.length ? a : b, '');
const measured = longest.length * 7 + 44;
toggle.style.width = Math.ceil(measured / 10) * 10 + 'px'; // auf 10px runden
```

**Nicht erlaubt:** `width: auto`, `min-width`, oder Breite durch Inhalt bestimmen lassen.

**Menü-Breite:**
```css
.topbar-dropdown-menu {
  min-width: 100%;  /* mindestens so breit wie der Toggle */
}
```
Das Menü ist immer mindestens so breit wie sein Toggle-Button — nie schmaler.  
Wenn einzelne Einträge länger sind als der Toggle, darf das Menü breiter werden.

### Verhalten nach Breakpoint

| Breakpoint | Verhalten |
|---|---|
| Desktop ≥1025px | Alle Controls inline sichtbar in `topbar-center` |
| Tablet 769–1024px | Controls ausgeblendet; stattdessen **„Tools"-Button** mit Slider-Icon + Text → öffnet `controls-overlay` |
| Mobile ≤768px | `topbar-center` komplett ausgeblendet; Tools-Button wandert in `topbar-right`, **nur Slider-Icon** (kein Text) |

### Controls Overlay (Tablet + Mobile)

Öffnet sich unter der Topbar, volle Breite, `background: #202020`.  
Wird per Klick außerhalb oder `Escape` geschlossen.

---

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

---

## Zone: Rechts (`topbar-right`)

Enthält bis zu **3 Navigationslinks** zu anderen Sites.  
Links je nach Seite zu definieren (siehe Seiten-spezifische Doku).

### Verhalten nach Breakpoint

| Breakpoint | Links sichtbar |
|---|---|
| Desktop ≥1025px | Alle 3 |
| Tablet 769–1024px | Max. 2 |
| Mobile ≤768px | Keine |

```css
.topbar-nav-link {
  color: var(--muted); font-size: 0.82rem; font-weight: 600;
  padding: 6px 10px; border-radius: 5px; text-decoration: none;
  height: 36px;
}
.topbar-nav-link.active { color: var(--accent); }
.topbar-nav-link:hover  { color: var(--text); background: rgba(255,255,255,0.05); }

@media (max-width: 768px)  { .topbar-nav-link { display: none; } }
@media (max-width: 1024px) { .topbar-nav-link:nth-child(n+3) { display: none; } }
```

### Nav Dropdown (`.topbar-nav-dropdown`)

Ersetzt mehrere einzelne `.topbar-nav-link`-Einträge wenn mehr als 2–3 Links benötigt werden.

> **Regel:** `.topbar-nav-dropdown` und `.topbar-nav-link` nie gleichzeitig in `topbar-right` verwenden.

**HTML:**
```html
<div class="topbar-nav-dropdown">
  <button class="topbar-nav-dropdown-toggle"
          aria-haspopup="menu" aria-expanded="false">
    Portale
    <span class="chevron">▾</span>
  </button>
  <div class="topbar-nav-dropdown-menu" role="menu">
    <a href="#" class="topbar-nav-dropdown-item" role="menuitem">Link 1</a>
    <a href="#" class="topbar-nav-dropdown-item active" role="menuitem">Link 2</a>
    <a href="#" class="topbar-nav-dropdown-item" role="menuitem">Link 3</a>
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

---

## Sidebar-Toggle

**Kein Hamburger-Button in der Topbar** — auf keinem Breakpoint.

Stattdessen: Halbkreis-Tab an der rechten Kante der Sidebar.

### Aussehen

| Token | Wert |
|---|---|
| Hintergrund | `rgba(59,130,246, 0.07)` |
| Border | `rgba(59,130,246, 0.25)`, rechts + oben/unten (links offen) |
| Border-Radius | `0 7px 7px 0` |
| Breite × Höhe | `13px × 36px` |
| Symbol offen | `‹` |
| Symbol geschlossen | `›` |
| Hover | `background: --accent`, Pfeil weiß |

### Standard-Zustand

| Breakpoint | Standard |
|---|---|
| Desktop ≥769px | Sidebar **offen** |
| Tablet 769–1024px | Sidebar **offen** |
| Mobile ≤768px | Sidebar **geschlossen** (Overlay + Backdrop) |

```css
.sidebar-tab {
  position: absolute; right: -13px; top: 50%; transform: translateY(-50%);
  width: 13px; height: 36px;
  background: rgba(59,130,246, 0.07);
  border: 1px solid rgba(59,130,246, 0.25); border-left: none;
  border-radius: 0 7px 7px 0;
  color: var(--accent); font-size: 10px; font-weight: 700;
}
.sidebar-tab:hover { background: var(--accent); color: #fff; }
```

---

## Seitentypen-Matrix

| Seite | Links-Zone | Mitte-Zone | Rechts-Zone | Sidebar |
|---|---|---|---|---|
| Landing (cloud) | Logo + Name | leer | leer | nein |
| Internal | Logo + Name | leer | max. 3 Links | ja |
| Tiles | Logo + Name | leer | max. 3 Links | ja |
| Karte | Logo + Name | Controls | max. 3 Links | nein |

---

## Accessibility

- `brand`-Link: `title="Zur Startseite"`
- Dropdown: `aria-haspopup="listbox"`, `aria-expanded`
- Toggle Button: `aria-pressed`
- Searchbar: `aria-label="Suchfeld"`
- Sidebar-Tab: `role="button"`, `aria-label`, `tabindex="0"`, Enter/Space bedienbar
- Nav Dropdown Toggle: `aria-haspopup="menu"`, `aria-expanded`, `Escape` schließt Menü
- Controls-Toggle: `aria-expanded`, `aria-controls`
- `Escape` schließt Dropdown, Sidebar (Mobile), Controls-Overlay

---

## Controls-Panel — Verhalten nach Breakpoint

Das Controls-Panel enthält die Werkzeuge einer Tool-Seite (Dropdowns, Toggles, Suche).
Es verhält sich je nach Breakpoint anders:

| Breakpoint | Controls-Panel | Toggle-Button | Overlay |
|---|---|---|---|
| Desktop ≥1025px | Inline in `.topbar-center` | ausgeblendet | — |
| Tablet 769–1024px | ausgeblendet | Icon + Text | öffnet sich unter Topbar |
| Mobile ≤768px | ausgeblendet | nur Icon | öffnet sich unter Topbar |

### HTML-Struktur

```html
<!-- Toggle-Button — wird auf Tablet/Mobile eingeblendet -->
<button class="controls-toggle tablet-only" id="controls-toggle">
  <div class="slider-icon">
    <span></span><span></span><span></span>
  </div>
  <span class="controls-toggle-text">Tools</span>  <!-- Mobile: display:none -->
</button>

<!-- Overlay — öffnet sich unter der Topbar, volle Breite -->
<div class="controls-overlay" id="controls-overlay">
  <!-- Kopie / Variante der Controls für Tablet/Mobile -->
  <!-- Alle Elemente hier: volle Breite, vertikal gestapelt -->
  <div class="form-field">
    <label class="form-label">Hintergrundkarte</label>
    <select class="form-select">...</select>
  </div>
  <button class="topbar-toggle">Labels</button>
</div>

<!-- Backdrop — schließt Overlay bei Klick außerhalb -->
<div class="controls-backdrop" id="controls-backdrop"></div>
```

### Controls im Overlay — Layout-Regeln

| Inhalt | Regel |
|---|---|
| Dropdown / Select | Volle Breite, immer oben |
| Eingabefeld (Geocoder, Suche) | Volle Breite, mit oder ohne Icon |
| 1 Button | Volle Breite |
| 2+ Buttons | 2er Grid (2 Spalten) |
| Trenner | `.controls-sep` zwischen jeder inhaltlichen Gruppe |

#### HTML-Struktur

```html
<div class="controls-overlay" id="controls-overlay">

  <!-- 1. Dropdowns/Selects: volle Breite, oben -->
  <div class="form-field">
    <label class="form-label">Hintergrundkarte</label>
    <select class="form-select">
      <option>OSM Standard</option>
      <option>OSM DE</option>
    </select>
  </div>

  <!-- Trenner -->
  <div class="controls-sep"></div>

  <!-- Eingabefeld (Geocoder / Suche): volle Breite -->
  <div class="form-field">
    <div class="form-input-wrap">
      <i class="fa-solid fa-magnifying-glass form-input-icon"></i>
      <input class="form-input" type="text" placeholder="Ort oder Adresse suchen…">
    </div>
  </div>

  <!-- Trenner -->
  <div class="controls-sep"></div>

  <!-- Buttons: ab 2 Stück im 2er-Grid -->
  <div class="controls-btn-group">
    <button class="topbar-toggle">Zoom</button>
    <button class="topbar-toggle active">Legende</button>
    <button class="topbar-toggle">Labels: an</button>
    <button class="topbar-toggle">Info</button>
  </div>

  <!-- 1 Button allein: .single für volle Breite -->
  <!-- <div class="controls-btn-group single">
    <button class="topbar-toggle">Zoom</button>
  </div> -->

</div>
```

#### Beispiele nach Anzahl

| Buttons | Ergebnis |
|---|---|
| 1 | `.controls-btn-group.single` → volle Breite |
| 2 | 2er Grid → 2 nebeneinander |
| 3 | 2er Grid → 2 + 1 (letzte Zeile links) |
| 4 | 2er Grid → 2 × 2 |
| 5+ | 2er Grid → mehrere Zeilen |

### Slider-Icon (Tools-Button)

Das Icon für den Controls-Toggle besteht aus drei CSS-Linien:

```html
<div class="slider-icon">
  <span></span>  <!-- volle Breite -->
  <span></span>  <!-- 65% Breite — signalisiert "Filter/Einstellungen" -->
  <span></span>  <!-- volle Breite -->
</div>
```

```css
.slider-icon { display: flex; flex-direction: column; gap: 3px; width: 14px; }
.slider-icon span { display: block; height: 2px; background: currentColor; border-radius: 1px; }
.slider-icon span:nth-child(2) { width: 65%; }
```

### JavaScript

```js
let controlsOpen = false;

function setControls(open) {
  controlsOpen = open;
  document.getElementById('controls-overlay').classList.toggle('open', open);
  document.getElementById('controls-backdrop').classList.toggle('visible', open);
  document.getElementById('controls-toggle').setAttribute('aria-expanded', open);
}

document.getElementById('controls-toggle').addEventListener('click', () => setControls(!controlsOpen));
document.getElementById('controls-backdrop').addEventListener('click', () => setControls(false));
document.addEventListener('keydown', e => { if (e.key === 'Escape') setControls(false); });

// Bei Resize auf Desktop: Overlay schließen
window.addEventListener('resize', () => {
  if (window.innerWidth > 1024 && controlsOpen) setControls(false);
});
```

#### Sidebar-Zustand für Overlay-Position

Damit das Overlay auf Tablet korrekt neben der Sidebar startet,
muss `body.sidebar-collapsed` beim Sidebar-Toggle gesetzt werden:

```js
function setSidebar(open) {
  // ... bestehende Sidebar-Logik ...

  // body-Klasse für Overlay-Positionierung auf Tablet
  document.body.classList.toggle('sidebar-collapsed', !open);
}
```

**Verhalten nach Zustand:**

| Breakpoint | Sidebar offen | Sidebar eingeklappt |
|---|---|---|
| Desktop ≥1025px | Overlay nicht vorhanden | Overlay nicht vorhanden |
| Tablet 769–1024px | `left: var(--sidebar-width)` | `left: 0` |
| Mobile ≤768px | Sidebar als Overlay, nicht relevant | `left: 0` |


---

## Breakpoint-Hilfsklassen

Für Elemente die nur auf einem bestimmten Breakpoint sichtbar sein sollen.
Verhindert dass z.B. ein Tablet-Button gleichzeitig mit einem Mobile-Button angezeigt wird.

```html
<!-- Nur auf Tablet -->
<button class="tablet-only controls-toggle">Tools</button>

<!-- Nur auf Mobile -->
<button class="mobile-only controls-toggle">
  <div class="slider-icon">...</div>
</button>

<!-- Nur auf Desktop -->
<div class="desktop-only controls-panel">...</div>
```

```css
.tablet-only  { display: none; }
@media (min-width: 769px) and (max-width: 1024px) { .tablet-only  { display: flex; } }

.mobile-only  { display: none; }
@media (max-width: 768px)                         { .mobile-only  { display: flex; } }

.desktop-only { display: flex; }
@media (max-width: 1024px)                        { .desktop-only { display: none; } }
```

---

## Striktes Mobile Nav-Hiding

Nav-Links werden auf Mobile mit `!important` ausgeblendet um Layout-Konflikte
mit `display: flex` aus anderen Regeln zu verhindern.

```css
@media (max-width: 768px) {
  .topbar-nav-link { display: none !important; }
  .topbar .nav-list { display: none !important; }
}
```

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-05-10 | Dropdown min-width Fix · `.topbar-toggle--icon-only` Modifier · `.topbar-nav-dropdown` Komponente |
| 2026-04-21 | Initiale Definition. Hamburger durch Sidebar-Tab ersetzt. Mobile 52px. Brand ohne Icon auf Mobile. |

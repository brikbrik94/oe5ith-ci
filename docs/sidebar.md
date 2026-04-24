# Sidebar & Navigation

**Referenz-Datei:** `components/sidebar.html`  
**Status:** definiert · v1.1

---

## Überblick

Die Sidebar ist die primäre Navigation auf Seiten mit mehreren Bereichen.
Sie fasst alle Navigationselemente zusammen: Nav-Items, Accordion-Gruppen,
externe Links, Trenner und Section-Labels.

---

## Verfügbare Elemente

| Element | Klasse | Verwendung |
|---|---|---|
| Nav-Item | `.sidebar-nav-item` | Interne Navigation, aktiver Zustand |
| Externer Link | `.sidebar-nav-item.external` | Links zu anderen Diensten |
| Accordion-Gruppe | `.acc-group` | Layer-Steuerung, aufklappbare Kategorien |
| Filter-Feld | `.acc-filter` | Suche über Accordion-Gruppen |
| Section-Label | `.sidebar-section-label` | Gruppenüberschrift zwischen Bereichen |
| Trenner | `.sidebar-sep` | 1px Linie zwischen logischen Gruppen |
| Status-Dot (Nav) | `.sidebar-status-dot` | Service-Health rechts im Nav-Item |
| Footer | `.sidebar-footer` | Version + optionaler Status ganz unten |

---

## Abmessungen & Tokens

| Token | Wert |
|---|---|
| `--sidebar-width` | `260px` — fix auf allen Breakpoints |
| Hintergrund | `--panel` (#202020) |
| `--nav-active-bg` | `--accent-subtle` (rgba 59,130,246, 0.07) |
| `--nav-active-border` | `--accent` |
| Tab Background | `rgba(59,130,246, 0.07)` |
| Tab Border | `rgba(59,130,246, 0.25)` |

---

## Höhe & Scroll-Verhalten

Die Sidebar ist immer exakt so hoch wie der sichtbare Viewport unter der Topbar.
Der Footer klebt immer am unteren Rand — unabhängig davon wie viel Inhalt in `.sidebar-inner` steht.

```
Viewport
├── Topbar (60px, sticky)
└── .layout (height: 100vh - 60px, overflow: hidden)
    ├── .sidebar (height: 100%, flex-column)
    │   ├── .sidebar-inner (flex: 1, overflow-y: auto)  ← scrollt
    │   └── .sidebar-footer (flex-shrink: 0)            ← klebt unten
    └── .page-content (flex: 1, overflow-y: auto)       ← scrollt unabhängig
```

### Collapsed — Inhalt ausblenden

Bei `width: 0` muss der Inhalt explizit ausgeblendet werden.
Ohne `opacity: 0` "blutet" `.sidebar-inner` nach rechts aus dem 0px-Container heraus,
da `overflow: visible` für den sichtbaren Tab-Toggle benötigt wird.

```css
.sidebar.collapsed .sidebar-inner,
.sidebar.collapsed .sidebar-footer {
  opacity: 0;
  pointer-events: none;       /* verhindert Klicks auf unsichtbaren Inhalt */
  transition: opacity 0.15s ease;
}

/* sidebar-inner braucht opacity: 1 als Ausgangszustand für die Transition */
.sidebar-inner {
  opacity: 1;
  transition: opacity 0.15s ease;
}
```

---

```css
/* Layout-Container: feste Höhe, kein Scroll auf Seiten-Ebene */
.layout {
  display: flex;
  height: calc(100vh - var(--topbar-height));
  overflow: hidden;
}

/* Sidebar: füllt Layout exakt aus */
.sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* Inner: wächst, scrollt bei Overflow */
.sidebar-inner {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Footer: schrumpft nicht, bleibt immer sichtbar */
.sidebar-footer {
  flex-shrink: 0;
}

/* Page Content: scrollt unabhängig von Sidebar */
.page-content {
  flex: 1;
  overflow-y: auto;
  height: 100%;
}
```

> **Wichtig:** `min-height` für `.layout` funktioniert hier nicht — es muss `height` sein,
> damit der Container den Viewport nicht überwächst. `overflow: hidden` auf `.layout`
> verhindert zusätzlich einen Scroll auf Seiten-Ebene.

---

## Nav-Items

```css
.sidebar-nav-item {
  padding: 8px 10px;        /* → ca. 36px Gesamthöhe */
  border-radius: 5px;
  border-left: 2px solid transparent;
  font-size: 0.85rem; color: var(--muted);
  gap: 10px;
  transition: color 0.15s, background 0.15s, border-color 0.15s;
}
.sidebar-nav-item:hover { color: var(--text); background: rgba(255,255,255,0.03); }
.sidebar-nav-item.active { color: var(--accent); background: var(--accent-subtle); border-left-color: var(--accent); }
```

### Status-Dot im Nav-Item

Für Service-Health rechts im Item. `margin-left: auto` drückt ihn an den rechten Rand.

```html
<a class="sidebar-nav-item">
  <i class="fa-solid fa-server nav-icon"></i>
  Services
  <span class="sidebar-status-dot online"></span>
</a>
```

| Klasse | Farbe | Verwendung |
|---|---|---|
| `.online` | `--success` + Glow | Service erreichbar |
| `.offline` | `#ef4444` + Glow | Service nicht erreichbar |
| *(keine Klasse)* | `#444` | Unbekannt |

### Externe Links

Gleiche Struktur, aber `color: #666` und Pfeil-Icon rechts. Kein aktiver Zustand.

```html
<a class="sidebar-nav-item external" href="https://..." target="_blank">
  <i class="fa-brands fa-docker nav-icon"></i>
  Portainer
  <i class="fa-solid fa-arrow-up-right-from-square external-icon"></i>
</a>
```

---

## Section-Labels & Trenner

Section-Labels nur bei **mehreren Gruppen** anzeigen — nie für eine einzelne Gruppe.

```html
<div class="sidebar-section-label">NAVIGATION</div>
<!-- Nav-Items ... -->
<div class="sidebar-sep"></div>
<div class="sidebar-section-label">KATEGORIEN</div>
<!-- Accordion ... -->
```

```css
.sidebar-section-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: #555; }
.sidebar-sep { height: 1px; background: var(--border); margin: 10px 0; }
```

---

## Accordion-Gruppen

Aufklappbare Kategorien mit Dot, Titel, Status-Badge und Checkbox-Liste.
Eingesetzt für Layer-Steuerung auf Kartenseiten.

### Struktur

```
.accordion
└── .acc-group (.open)
    ├── .acc-header          ← immer sichtbar, klickbar
    │   ├── .acc-dot         ← site-spezifische Farbe, kein CI-Token
    │   ├── .acc-title
    │   ├── .acc-status      ← unloaded / partial / all-on
    │   └── .acc-chevron     ← rotiert bei .open
    ├── .acc-controls        ← nur bei .open sichtbar
    │   ├── "Alle an"
    │   └── "Alle aus"
    └── .acc-body            ← max-height Transition
        └── .acc-item (.checked)
            ├── .acc-checkbox
            └── .acc-item-label
```

### Dot-Farbe

Der Dot signalisiert die Kategorie der Gruppe. Die Farbe ist **frei und site-spezifisch** —
sie ist kein CI-Token und wird nicht zentral vorgegeben. Jede Site wählt ihre eigenen
Dot-Farben passend zu den dargestellten Inhalten.

```html
<!-- Farbe direkt als style, kein Token -->
<span class="acc-dot" style="background:#22c55e"></span>
```

### Status-Badge

| Klasse | Text | Farbe | Bedeutung |
|---|---|---|---|
| `.acc-status.unloaded` | `nicht geladen` | Grau | Keine Layer aktiv |
| `.acc-status.partial` | `n Layer` | Blau (--accent) | 1 bis n-1 Layer aktiv |
| `.acc-status.all-on` | `alle aktiv` | Grün (--success) | Alle Layer aktiviert |

Badge-Text-Regel: 0 aktiv → `nicht geladen` · 1–(n-1) aktiv → `n Layer` · alle aktiv → `alle aktiv`

### Filter-Feld

Optional, vor der Accordion-Liste. Nur bei mehr als 5 Gruppen sinnvoll.

```html
<div class="acc-filter">
  <i class="fa-solid fa-magnifying-glass acc-filter-icon"></i>
  <input type="text" placeholder="Layer filtern...">
</div>
```

### Dynamische Höhe (kein statisches max-height)

`max-height` für die Transition wird beim Öffnen per JS auf den tatsächlichen `scrollHeight` gesetzt.
Ein fester Wert (z.B. `600px`) würde lange Listen abschneiden.

```css
.acc-body { max-height: 0; overflow: hidden; transition: max-height 0.25s ease; }
.acc-group.open .acc-body { max-height: var(--acc-body-height, 9999px); }
```

```js
function toggleGroup(header) {
  const group = header.closest('.acc-group');
  const body = group.querySelector('.acc-body');
  const isOpen = group.classList.toggle('open');
  if (isOpen) {
    // Einmalig messen — nie statisch begrenzen
    body.style.setProperty('--acc-body-height', body.scrollHeight + 'px');
  }
  header.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
}
```

### Keyboard-Navigation & Accessibility

Accordion-Header und Items müssen per Tastatur bedienbar sein.

```html
<!-- Header: tabindex + role + aria-expanded -->
<div class="acc-header" tabindex="0" role="button" aria-expanded="false"
     onclick="toggleGroup(this)" onkeydown="handleAccKey(event, this)">

<!-- Item: tabindex + role + aria-checked -->
<div class="acc-item" tabindex="0" role="checkbox" aria-checked="false"
     onclick="toggleItem(this)" onkeydown="handleItemKey(event, this)">
```

```js
function handleAccKey(e, header) {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleGroup(header); }
}
function handleItemKey(e, item) {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleItem(item); }
}
```

> Items die per Maus oder Tastatur aktiviert werden, aktualisieren immer auch `aria-checked`.

---

## Sidebar Footer

Immer sichtbar wenn die Sidebar sichtbar ist.

| Typ | Inhalt |
|---|---|
| **Statisch** | Nur Versionsinfo. Kein Dot. |
| **Live** | Version + Dot: `online` (grün) / `offline` (rot) |
| **Auth** | Version + Dot: `logged in` (grün) / `logged out` (rot) |

---

## Tab-Toggle

Halbkreis-Tab an der rechten Kante. Kein Hamburger in der Topbar.

Symbol: `‹` (offen) / `›` (geschlossen)

```css
.sidebar-tab {
  position: absolute; right: -13px; top: 50%; transform: translateY(-50%);
  width: 13px; height: 36px;
  background: rgba(59,130,246, 0.07); border: 1px solid rgba(59,130,246, 0.25); border-left: none;
  border-radius: 0 7px 7px 0; color: var(--accent);
}
.sidebar-tab:hover { background: var(--accent); color: #fff; }
```

---

## Breakpoint-Verhalten

| Breakpoint | Standard | Mechanismus |
|---|---|---|
| Desktop ≥769px | Offen | `width` Transition |
| Tablet 769–1024px | Offen | Identisch zu Desktop |
| Mobile ≤768px | Geschlossen | `position: fixed`, `transform: translateX(-100%)` |

---

## Regeln

1. Section-Labels nur bei mehreren Gruppen — nie für eine einzige Gruppe
2. Dot-Farbe der Accordion-Gruppe ist frei und site-spezifisch — kein CI-Token
3. Status-Badge immer per JS aktualisieren — nie statisch hardcoden
4. Filter-Feld nur bei mehr als 5 Accordion-Gruppen
5. Externe Links: immer `color: #666`, immer Pfeil-Icon, immer neuer Tab

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | v1.0: Initiale Definition. |
| 2026-04-22 | v1.1: Accordion als Sidebar-Element integriert. Dot-Farben aus Accordion entfernt — site-spezifisch. Elementübersicht ergänzt. accordion.md aufgelöst. |
| 2026-04-22 | v1.2: Höhe & Scroll-Verhalten definiert. Layout `height` statt `min-height`. Sidebar `height: 100%`, inner `flex: 1 / overflow-y: auto`, Footer `flex-shrink: 0`. |

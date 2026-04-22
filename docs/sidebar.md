# Sidebar & Navigation

**Referenz-Datei:** `components/sidebar.html`  
**Status:** definiert · v1.0

---

## Überblick

Die Sidebar ist die primäre Navigation auf Seiten mit mehreren Bereichen.
Sie ist auf allen Breakpoints 260px breit und wird über einen Halbkreis-Tab
an ihrer rechten Kante ein- und ausgeklappt — nie über einen Hamburger in der Topbar.

---

## Abmessungen & Tokens

| Token | Wert |
|---|---|
| `--sidebar-width` | `260px` — fix auf allen Breakpoints |
| `--sidebar-bg` | `#202020` |
| `--nav-active-bg` | `rgba(59,130,246, 0.07)` |
| `--nav-active-border` | `--accent` (#3b82f6) |
| `--sidebar-tab-bg` | `rgba(59,130,246, 0.07)` |
| `--sidebar-tab-border` | `rgba(59,130,246, 0.25)` |

---

## Struktur

```
.sidebar
├── .sidebar-inner          (scrollbarer Navigationsbereich, flex: 1)
│   ├── .sidebar-section-label   (nur bei mehreren Gruppen)
│   ├── .sidebar-nav-item        (interne Links)
│   ├── .sidebar-nav-item.external (externe Links)
│   └── .sidebar-sep             (Trenner zwischen Gruppen)
├── .sidebar-footer         (immer sichtbar wenn Sidebar sichtbar)
└── .sidebar-tab            (Halbkreis-Toggle, position: absolute)
```

---

## Nav Items

### Interne Links

```css
.sidebar-nav-item {
  padding: 8px 10px;        /* → ca. 36px Gesamthöhe */
  border-radius: 5px;
  border-left: 2px solid transparent;
  font-size: 0.85rem;
  color: var(--muted);
  gap: 10px;
}

.sidebar-nav-item:hover {
  color: var(--text);
  background: rgba(255,255,255, 0.03);
}

.sidebar-nav-item.active {
  color: var(--accent);
  background: var(--nav-active-bg);
  border-left-color: var(--accent);
}
```

**Höhe:** durch Padding definiert (~36px) — kein `min-height`.

### Icons

Font Awesome bevorzugt, SVG inline erlaubt.

```html
<!-- Font Awesome (bevorzugt) -->
<a class="sidebar-nav-item active">
  <i class="fa-solid fa-gauge-high nav-icon"></i>
  Dashboard
</a>

<!-- SVG inline (erlaubt) -->
<a class="sidebar-nav-item">
  <svg class="nav-icon" ...></svg>
  Services
</a>
```

Icon-Größe: `font-size: 0.85em`, Breite: `16px`, `opacity: 0.7` (aktiv: `1.0`).

### Status-Dot im Nav-Item

Für Service-Health-Signale rechts im Nav-Item:

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
| *(keine Klasse)* | `#444` | Unbekannt / nicht geprüft |

### Externe Links

Gleiche HTML-Struktur wie interne Links, aber:
- `color: #666` (dunkler als `--muted`) — signalisiert "sekundär"
- Pfeil-Icon `fa-arrow-up-right-from-square` rechts außen
- Klasse `.external`

```html
<a href="https://..." class="sidebar-nav-item external" target="_blank">
  <i class="fa-brands fa-docker nav-icon"></i>
  Portainer
  <i class="fa-solid fa-arrow-up-right-from-square external-icon"></i>
</a>
```

---

## Section Labels

Nur anzeigen wenn **mehrere Gruppen** vorhanden sind.
Bei einer einzigen Gruppe weglassen — ein Trenner reicht.

```html
<!-- Mehrere Gruppen → Labels anzeigen -->
<div class="sidebar-section-label">SYSTEM</div>
<!-- ... Nav Items ... -->
<div class="sidebar-sep"></div>
<div class="sidebar-section-label">TOOLS</div>
```

```css
.sidebar-section-label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #555;
}
```

---

## Sidebar Footer

Immer sichtbar wenn die Sidebar sichtbar ist.
Anordnung: **Links Version — Rechts Status**

```html
<div class="sidebar-footer" data-type="static|live|auth">
  <span class="sidebar-footer-version">v1.0.0</span>
  <span class="sidebar-footer-status">
    <span class="footer-dot green|red"></span>
    <span class="footer-status-text green|red">online|offline|logged in|logged out</span>
  </span>
</div>
```

### Drei Varianten je nach Seitentyp

| Typ | Wann | Footer-Inhalt |
|---|---|---|
| **Statisch** | Einmaliger Seitenaufruf — kein aktiver Datenabruf (Landing, Tiles, Docs) | Nur Versionsinfo. Kein Status-Dot. |
| **Live** | Aktiver Datenabruf ohne Login (Karte, ADS-B, AIS-Tracking) | Version + Dot: `online` (grün) / `offline` (rot) |
| **Auth** | Login erforderlich, Session überwacht (Internal Dashboard) | Version + Dot: `logged in` (grün) / `logged out` (rot) |

### CSS Footer-Status

```css
.sidebar-footer {
  border-top: 1px solid var(--border);
  padding: 9px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-footer-version {
  font-size: 0.65rem;
  font-family: monospace;
  color: #444;
}

.footer-dot        { width: 7px; height: 7px; border-radius: 50%; }
.footer-dot.green  { background: var(--success); box-shadow: 0 0 4px var(--success); }
.footer-dot.red    { background: #ef4444; box-shadow: 0 0 4px rgba(239,68,68,0.5); }

.footer-status-text.green { color: #4a7c59; }
.footer-status-text.red   { color: #7c4a4a; }
```

> **Implementierungshinweis:** Der Status muss vom jeweiligen Seiten-JS geprüft und
> gesetzt werden — die CI definiert nur die Darstellung, nicht die Abfrage-Logik.

---

## Tab-Toggle

Identisch zur Topbar-Spezifikation — hier zur Vollständigkeit:

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

Symbol: `‹` (offen) / `›` (geschlossen)

---

## Breakpoint-Verhalten

| Breakpoint | Standard | Mechanismus |
|---|---|---|
| Desktop ≥769px | **Offen** | `width` Transition 0–260px, `overflow: visible` für Tab |
| Tablet 769–1024px | **Offen** | Identisch zu Desktop |
| Mobile ≤768px | **Geschlossen** | `position: fixed`, `transform: translateX(-100%)` → `translateX(0)` |

**Mobile-Overlay:** Sidebar legt sich über den Content. Backdrop (halbtransparent) schließt bei Tap.

```css
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: var(--topbar-height);
    left: 0;
    height: calc(100vh - var(--topbar-height));
    z-index: 50;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
  }
  .sidebar.mobile-open {
    transform: translateX(0);
    box-shadow: 4px 0 20px rgba(0,0,0,0.5);
  }
}
```

---

## Accessibility

- `<nav aria-label="Hauptnavigation">` am Sidebar-Element
- Tab-Toggle: `role="button"`, `tabindex="0"`, `aria-label` wechselt mit Zustand
- Tab-Toggle: Enter + Space bedienbar
- Escape schließt Sidebar auf Mobile
- Backdrop: Klick schließt Sidebar auf Mobile
- `title`-Attribut auf Status-Dots (z.B. `title="Online"`)

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | Initiale Definition. 260px fix auf allen Breakpoints. Section-Labels nur bei mehreren Gruppen. Externe Links in #666. Footer mit drei Seitentyp-Varianten. |

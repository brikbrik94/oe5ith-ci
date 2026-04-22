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
- Controls-Toggle: `aria-expanded`, `aria-controls`
- `Escape` schließt Dropdown, Sidebar (Mobile), Controls-Overlay

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-21 | Initiale Definition. Hamburger durch Sidebar-Tab ersetzt. Mobile 52px. Brand ohne Icon auf Mobile. |

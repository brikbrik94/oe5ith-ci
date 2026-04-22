# Farben & Tokens

**Referenz-Datei:** `components/tokens.html`  
**Master-Datei:** `shared/assets/common.css`  
**Status:** definiert · v1.0

---

## Überblick

Alle Design Tokens sind als CSS Custom Properties in `shared/assets/common.css`
definiert und werden per Deploy-Script in jede Site kopiert.
Dies ist die einzige Quelle der Wahrheit — nie Werte duplizieren oder hardcoden.

---

## Basis-Farben

| Token | Wert | Verwendung |
|---|---|---|
| `--bg` | `#1a1a1a` | Haupt-Hintergrund aller Seiten |
| `--card-bg` | `#252525` | Cards, Topbar, Sidebar-Footer |
| `--panel` | `#202020` | Sidebar, tiefere Panels |
| `--panel-deep` | `#161616` | Tiefstes Panel, Code-Block-Hintergrund |
| `--text` | `#e0e0e0` | Primärtext — Headings, Labels |
| `--muted` | `#888888` | Sekundärtext — Beschreibungen, Body |
| `--subtle` | `#555555` | Labels, Section-Titles, Metadaten |
| `--border` | `#333333` | Alle Borders |
| `--border-strong` | `#444444` | Hover-Borders, aktive Elemente |

---

## Akzent-Farben

| Token | Wert | Verwendung |
|---|---|---|
| `--accent` | `#3b82f6` | Buttons, Icons, aktive Links, Topbar-Unterstrich |
| `--accent-hover` | `#2563eb` | Hover-State für Accent-Buttons |
| `--accent-subtle` | `rgba(59,130,246, 0.07)` | Aktive Nav-Items, Sidebar-Tab-Toggle |
| `--accent-subtle-md` | `rgba(59,130,246, 0.10)` | Badge-Hintergrund, Button-Secondary |
| `--accent-border` | `rgba(59,130,246, 0.25)` | Badge-Border, Tab-Toggle-Border |

---

## Semantische Farben

Jede semantische Farbe hat drei Varianten: Vollton, Subtle (10%), Border (25%).

| Token | Vollton | Subtle | Border | Bedeutung |
|---|---|---|---|---|
| `--success` | `#22c55e` | `rgba(34,197,94, 0.10)` | `rgba(34,197,94, 0.25)` | Online, OK, Aktiv |
| `--warning` | `#eab308` | `rgba(234,179,8, 0.10)` | `rgba(234,179,8, 0.25)` | Warnung, Auth required |
| `--danger` | `#ef4444` | `rgba(239,68,68, 0.10)` | `rgba(239,68,68, 0.25)` | Fehler, Offline, Destruktiv |
| `--auth` | `#a78bfa` | `rgba(139,92,246, 0.10)` | `rgba(139,92,246, 0.25)` | Auth/Security, Authentik, SSO |

---

## Code / Terminal Farben

| Token | Wert | Verwendung |
|---|---|---|
| `--code-bg` | `#000000` | Code Block Hintergrund |
| `--code-text` | `#4ade80` | Terminal-Output, Code Block Text |
| `--code-inline-bg` | `#2a2a2a` | Inline Code Hintergrund |
| `--code-inline-text` | `#e6e6e6` | Inline Code Text |
| `--url-bg` | `#0d0d0d` | URL / Pfad Felder in Cards |
| `--url-text` | `#4ade80` | URL / Pfad Text |

---

## Typografie Tokens

| Token | Wert |
|---|---|
| `--font-sans` | `'Segoe UI', system-ui, sans-serif` |
| `--font-mono` | `'JetBrains Mono', 'Consolas', 'Monaco', monospace` |

---

## Spacing & Layout Tokens

| Token | Wert | Verwendung |
|---|---|---|
| `--topbar-height` | `60px` | Topbar Desktop + Tablet |
| `--topbar-height-mobile` | `52px` | Topbar Mobile ≤768px |
| `--sidebar-width` | `260px` | Sidebar, alle Breakpoints |
| `--container-max` | `1000px` | Max-width Content-Container |
| `--card-radius` | `12px` | Cards, Modals |
| `--card-padding` | `20px` | Innenabstand Cards |
| `--card-gap` | `20px` | Grid-Gap zwischen Cards |
| `--btn-radius` | `6px` | Buttons |
| `--badge-radius` | `4px` | Badges — eckig |

---

## Z-Index Tokens

Z-Index Werte sind gestaffelt und dürfen nie manuell überschrieben werden.

| Token | Wert | Element |
|---|---|---|
| `--z-content` | `1` | Normaler Seiteninhalt |
| `--z-sidebar-tab` | `10` | Sidebar Tab-Toggle |
| `--z-backdrop` | `40` | Sidebar + Controls Backdrop |
| `--z-sidebar` | `50` | Sidebar Mobile Overlay |
| `--z-overlay` | `90` | Controls Overlay Panel |
| `--z-topbar` | `100` | Topbar (sticky) |
| `--z-dropdown` | `200` | Dropdowns, Menus |
| `--z-modal` | `500` | Modals |

---

## Transition Tokens

| Token | Wert | Verwendung |
|---|---|---|
| `--transition-fast` | `0.15s ease` | Buttons, Badges, Hover-Farben |
| `--transition-base` | `0.20s ease` | Card Hover (transform), Nav-Items |
| `--transition-slow` | `0.25s ease` | Sidebar ein/ausklappen |

---

## Shadow Tokens

| Token | Wert | Verwendung |
|---|---|---|
| `--shadow-topbar` | `0 2px 10px rgba(0,0,0,0.20)` | Topbar |
| `--shadow-card` | `0 10px 20px rgba(0,0,0,0.30)` | Card Hover-Zustand |
| `--shadow-dropdown` | `0 8px 20px rgba(0,0,0,0.40)` | Dropdowns, Overlay-Menus |
| `--shadow-sidebar` | `4px 0 20px rgba(0,0,0,0.50)` | Sidebar Mobile Overlay |

---

## Vollständige common.css

```css
:root {
  /* Basis */
  --bg:               #1a1a1a;
  --card-bg:          #252525;
  --panel:            #202020;
  --panel-deep:       #161616;
  --text:             #e0e0e0;
  --muted:            #888888;
  --subtle:           #555555;
  --border:           #333333;
  --border-strong:    #444444;

  /* Akzent */
  --accent:           #3b82f6;
  --accent-hover:     #2563eb;
  --accent-subtle:    rgba(59,130,246,0.07);
  --accent-subtle-md: rgba(59,130,246,0.10);
  --accent-border:    rgba(59,130,246,0.25);

  /* Semantisch */
  --success:          #22c55e;
  --success-subtle:   rgba(34,197,94,0.10);
  --success-border:   rgba(34,197,94,0.25);
  --warning:          #eab308;
  --warning-subtle:   rgba(234,179,8,0.10);
  --warning-border:   rgba(234,179,8,0.25);
  --danger:           #ef4444;
  --danger-subtle:    rgba(239,68,68,0.10);
  --danger-border:    rgba(239,68,68,0.25);
  --auth:             #a78bfa;
  --auth-subtle:      rgba(139,92,246,0.10);
  --auth-border:      rgba(139,92,246,0.25);

  /* Code */
  --code-bg:          #000000;
  --code-text:        #4ade80;
  --code-inline-bg:   #2a2a2a;
  --code-inline-text: #e6e6e6;
  --url-bg:           #0d0d0d;
  --url-text:         #4ade80;

  /* Typografie */
  --font-sans:        'Segoe UI', system-ui, sans-serif;
  --font-mono:        'JetBrains Mono', 'Consolas', 'Monaco', monospace;

  /* Spacing */
  --topbar-height:        60px;
  --topbar-height-mobile: 52px;
  --sidebar-width:        260px;
  --container-max:        1000px;
  --card-radius:          12px;
  --card-padding:         20px;
  --card-gap:             20px;
  --btn-radius:           6px;
  --badge-radius:         4px;

  /* Z-Index */
  --z-content:        1;
  --z-sidebar-tab:    10;
  --z-backdrop:       40;
  --z-sidebar:        50;
  --z-overlay:        90;
  --z-topbar:         100;
  --z-dropdown:       200;
  --z-modal:          500;

  /* Transitions */
  --transition-fast:  0.15s ease;
  --transition-base:  0.20s ease;
  --transition-slow:  0.25s ease;

  /* Shadows */
  --shadow-topbar:    0 2px 10px rgba(0,0,0,0.20);
  --shadow-card:      0 10px 20px rgba(0,0,0,0.30);
  --shadow-dropdown:  0 8px 20px rgba(0,0,0,0.40);
  --shadow-sidebar:   4px 0 20px rgba(0,0,0,0.50);
}
```

---

## Regeln

1. **Nie hardcoden** — immer Token verwenden, nie `#3b82f6` direkt im CSS
2. **Nie duplizieren** — `common.css` ist die einzige Quelle, nie kopieren
3. **Semantic gilt** — `--success` nur für wirklich positive Zustände, nie dekorativ
4. **Subtle-Varianten** für Hintergründe — Vollton nur für Text und Icons
5. **Z-Index nur via Token** — `z-index: 999` ist verboten

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | Initiale vollständige Token-Definition. Alle Farben aus Badges/Buttons als Tokens. Z-Index, Transitions, Shadows ergänzt. |

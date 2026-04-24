# OE5ITH CI Repository

Design System für das OE5ITH Cloud Portal.

## Struktur

```
oe5ith-ci/
├── css/                        # Produktions-CSS (in Sites einbinden)
│   ├── index.css               # Master-Import (alle Komponenten)
│   ├── common.css              # Tokens & Reset — immer zuerst einbinden
│   ├── topbar.css
│   ├── sidebar.css             # inkl. Accordion
│   ├── cards.css
│   ├── buttons.css
│   ├── badges.css
│   ├── page.css             # Page-Header, Content-Body, Panel, Tabelle, Column-Groups
│   ├── forms.css               # Input, Select, Service-Selector, Segmented
│   ├── modal.css               # Modal + Karten-Popup + Leaflet/MapLibre Overrides
│   ├── typography.css
│   └── tokens.css
├── assets/
│   └── logo.svg
├── components/                 # Interaktive Referenz-HTMLs (live testbar)
│   ├── topbar.html
│   ├── sidebar.html
│   ├── cards.html
│   ├── buttons.html
│   ├── buttons-demo.html
│   ├── badges.html
│   ├── forms.html
│   ├── modal.html
│   ├── typography.html
│   ├── typography-preview.html
│   └── tokens.html
├── docs/                       # Spezifikationen
│   ├── topbar.md
│   ├── sidebar.md
│   ├── cards.md
│   ├── buttons.md
│   ├── badges.md
│   ├── page.md
│   ├── page-types.md       # Entscheidungshilfe: welchen Seitentyp verwenden?
│   ├── forms.md
│   ├── modal.md
│   ├── typography.md
│   ├── tokens.md
│   └── cli.md
└── scripts/cli/
    ├── utils.sh
    └── utils.py
```

## CSS einbinden

### Alle Komponenten auf einmal
```html
<link rel="stylesheet" href="css/index.css">
```

### Selektiv — nur was gebraucht wird
```html
<!-- Tokens zuerst — immer Pflicht -->
<link rel="stylesheet" href="css/common.css">

<!-- Dann die benötigten Komponenten -->
<link rel="stylesheet" href="css/topbar.css">
<link rel="stylesheet" href="css/sidebar.css">
<link rel="stylesheet" href="css/buttons.css">
```

### Empfohlene Reihenfolge
1. `common.css` — Tokens & Reset
2. `typography.css`, `badges.css`, `buttons.css`, `cards.css`
3. `topbar.css`, `sidebar.css`
4. `forms.css`, `modal.css`

## Status

| Element | Spec | Referenz-HTML | CSS |
|---|---|---|---|
| Topbar | ✅ | ✅ | ✅ |
| Sidebar + Accordion | ✅ | ✅ | ✅ |
| Cards | ✅ | ✅ | ✅ |
| Buttons | ✅ | ✅ | ✅ |
| Badges | ✅ | ✅ | ✅ |
| Seitenstruktur (Page-Header, Panel, Tabelle) | ✅ | — | ✅ |
| Forms | ✅ | ✅ | ✅ |
| Modal + Karten-Popup | ✅ | ✅ | ✅ |
| Typografie | ✅ | ✅ | ✅ |
| Farben/Tokens | ✅ | ✅ | ✅ |
| CLI Terminal | ✅ | — | — |

## Token-Regeln

1. **Nie hardcoden** — immer Token verwenden
2. **Nie duplizieren** — `css/common.css` ist die einzige Quelle
3. **Semantic gilt** — `--success` nur für positive Zustände
4. **Subtle für Hintergründe** — Vollton nur für Text und Icons
5. **Z-Index nur via Token** — `z-index: 999` ist verboten

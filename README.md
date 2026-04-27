# OE5ITH CI Repository

Zentrales CI-, Design-System- und CSS-Repository für die OE5ITH-Webseiten.

Dieses Repository enthält die gestalterischen Grundlagen, wiederverwendbare UI-Komponenten,
CSS-Dateien für den produktiven Einsatz sowie Dokumentation für neue Seiten und Coding-Agenten.

---

## Zweck

`oe5ith-ci` ist die gemeinsame Grundlage für alle OE5ITH-Webseiten und Portale.

Es regelt:

- Farben und Design Tokens
- Typografie
- Layout-Grundstruktur
- wiederverwendbare Komponenten
- Seitentypen und Navigationsmuster
- Brand-, Naming-, Logo- und Favicon-Regeln
- Copyright- und Quellenhinweise
- CSS-Einbindung in produktiven Webseiten
- Regeln für Coding-Agenten und automatisierte Änderungen

Ziel ist, dass neue Seiten konsistent aussehen und bestehende Seiten nicht durch individuell
hardcodierte Styles auseinanderlaufen.

---

## Struktur

```text
oe5ith-ci/
├── README.md                   # Einstieg und Übersicht
├── CHANGELOG.md                # zentrale Änderungshistorie
├── css/                        # Produktions-CSS und Demo-CSS
│   ├── index.css               # Master-Import für alle produktiven Komponenten
│   ├── common.css              # Tokens, Reset, Basislayout — immer zuerst einbinden
│   ├── topbar.css              # Topbar / Header
│   ├── sidebar.css             # Sidebar inkl. Accordion
│   ├── cards.css               # Cards und Card-Grids
│   ├── buttons.css             # Buttons und Button-Varianten
│   ├── badges.css              # Status- und Info-Badges
│   ├── page.css                # Page-Header, Content-Body, Panels, Tabellen, Column-Groups
│   ├── forms.css               # Input, Select, Service-Selector, Segmented Controls
│   ├── modal.css               # Modal + Karten-Popup + Leaflet/MapLibre Overrides
│   ├── typography.css          # Typografie-Klassen
│   ├── tokens.css              # Token-Darstellung / Token-spezifische Styles
│   └── demo.css                # Nur für Komponenten-Demos und Referenzseiten
├── assets/
│   ├── logo.svg                # OE5ITH Logo
│   ├── favicon.svg             # CI-konformes SVG-Favicon
│   ├── favicon.ico             # ICO 16+32+48px für Browser-Kompatibilität
│   ├── favicon-32.png          # PNG 32×32
│   └── favicon-16.png          # PNG 16×16
├── components/                 # Interaktive Referenz-HTMLs, live testbar
│   ├── topbar.html
│   ├── sidebar.html
│   ├── cards.html
│   ├── buttons.html
│   ├── buttons-demo.html
│   ├── badges.html
│   ├── context-menu.html       # Context-Menu (Rechtsklick) + Action-Menu (⋮)
│   ├── forms.html
│   ├── modal.html
│   ├── page-types.html         # Visuelle Mockups aller Seitentypen
│   ├── sidebar-types.html      # Visuelle Mockups aller Sidebar-Typen
│   ├── typography.html
│   ├── typography-preview.html
│   └── tokens.html
├── docs/                       # Spezifikationen und Regeln
│   ├── concepts.md             # Begriffe: CI, Brand, Design System, CSS Library
│   ├── brand.md                # Brand-Grundregeln
│   ├── naming.md               # Dienstnamen, Schreibweisen und UI-Begriffe
│   ├── logo.md                 # Logo- und Favicon-Regeln
│   ├── usage.md                # CSS-Einbindung und Nutzungsregeln
│   ├── for-coding-agents.md    # Regeln für Coding-Agenten
│   ├── versioning.md           # Versionierung, Releases, Git-Tags
│   ├── tokens.md               # Farben, Tokens, Z-Index, Shadows, Transitions
│   ├── typography.md
│   ├── topbar.md
│   ├── sidebar.md
│   ├── sidebar-types.md        # Entscheidungshilfe: welchen Sidebar-Typ verwenden?
│   ├── page.md
│   ├── page-types.md           # Entscheidungshilfe: welchen Seitentyp verwenden?
│   ├── cards.md
│   ├── buttons.md
│   ├── badges.md
│   ├── forms.md
│   ├── modal.md
│   ├── context-menu.md         # Context-Menu + Action-Menu Spec
│   ├── resources.md            # Self-Hosting Anleitung für externe Ressourcen
│   ├── copyright.md            # Lizenzen aller verwendeten Ressourcen
│   ├── copyright-display.md    # Wo und wie Copyright auf Webseiten darstellen
│   └── cli.md
└── scripts/cli/
    ├── utils.sh
    └── utils.py
```

---

## Bereiche

### `css/`

Enthält die produktiv einbindbaren CSS-Dateien.

`css/common.css` ist die wichtigste Datei. Sie enthält die Design Tokens, den Reset
und das grundlegende Layout. Diese Datei muss immer vor allen anderen Komponenten
geladen werden.

`css/demo.css` ist nur für Demo- und Referenzseiten gedacht und sollte nicht in
produktive Webseiten eingebunden werden.

### `components/`

Enthält visuelle, testbare HTML-Referenzen für einzelne Komponenten und Seitentypen.

Diese Dateien sind keine produktiven Seiten, sondern dienen als Vorschau und
Referenz für die Umsetzung.

### `docs/`

Enthält Spezifikationen, Regeln und Entscheidungshilfen.

Wenn unklar ist, wie ein Element verwendet werden soll, gilt die Dokumentation in
`docs/` als fachliche Grundlage.

### `assets/`

Enthält Logo, Favicons und weitere CI-relevante statische Dateien.

---

## CSS einbinden

### Alle produktiven Komponenten auf einmal

```html
<link rel="stylesheet" href="css/index.css">
```

### Selektiv — nur was gebraucht wird

```html
<!-- Tokens, Reset und Basislayout zuerst — immer Pflicht -->
<link rel="stylesheet" href="css/common.css">

<!-- Danach die benötigten Komponenten -->
<link rel="stylesheet" href="css/topbar.css">
<link rel="stylesheet" href="css/sidebar.css">
<link rel="stylesheet" href="css/buttons.css">
```

### Empfohlene Reihenfolge

1. `common.css` — Tokens, Reset und Basislayout
2. `typography.css`, `badges.css`, `buttons.css`, `cards.css`
3. `topbar.css`, `sidebar.css`
4. `page.css`, `forms.css`, `modal.css`

Weitere Details stehen in:

```text
docs/usage.md
```

---

## Wichtige Einstiegsdokumente

| Dokument | Zweck |
|---|---|
| `docs/concepts.md` | Begriffsklärung: CI, Brand, Design System, CSS Library |
| `docs/brand.md` | Brand-Grundregeln und visueller Grundcharakter |
| `docs/naming.md` | Dienstnamen, Schreibweisen, Domains und UI-Begriffe |
| `docs/logo.md` | Logo- und Favicon-Regeln |
| `docs/usage.md` | CSS-Einbindung, Reihenfolge und Nutzungsregeln |
| `docs/for-coding-agents.md` | Verbindliche Regeln für Coding-Agenten |
| `docs/versioning.md` | Versionierung, Releases, Git-Tags und Changelog-Regeln |
| `docs/tokens.md` | Farben, Tokens, Z-Index, Shadows, Transitions |
| `docs/page-types.md` | Entscheidungshilfe für Seitentypen |
| `docs/sidebar-types.md` | Entscheidungshilfe für Sidebar-Varianten |
| `docs/resources.md` | Self-Hosting externer Ressourcen |
| `docs/copyright.md` | Quellen und Lizenzen verwendeter Ressourcen |
| `docs/copyright-display.md` | Darstellung von Copyright-Hinweisen auf Webseiten |
| `CHANGELOG.md` | zentrale Änderungshistorie |

---

## Status

| Element | Spec | Referenz-HTML | CSS |
|---|---|---|---|
| Brand / CI-Grundregeln | ✅ | — | — |
| Naming | ✅ | — | — |
| Logo / Favicons | ✅ | — | — |
| Versionierung | ✅ | — | — |
| Usage / Einbindung | ✅ | — | — |
| Coding-Agent-Regeln | ✅ | — | — |
| Topbar | ✅ | ✅ | ✅ |
| Sidebar + Accordion | ✅ | ✅ | ✅ |
| Cards | ✅ | ✅ | ✅ |
| Buttons | ✅ | ✅ | ✅ |
| Badges | ✅ | ✅ | ✅ |
| Seitenstruktur (Page-Header, Panel, Tabelle) | ✅ | ✅ | ✅ |
| Forms | ✅ | ✅ | ✅ |
| Modal + Karten-Popup | ✅ | ✅ | ✅ |
| Context-Menu + Action-Menu | ✅ | ✅ | ✅ |
| Typografie | ✅ | ✅ | ✅ |
| Farben/Tokens | ✅ | ✅ | ✅ |
| CLI Terminal | ✅ | — | — |
| Demo-/Preview-Styles | — | ✅ | ✅ |

---

## Grundregeln

1. **Keine Werte hardcoden** — Farben, Abstände, Radien, Shadows und Z-Index immer über Tokens verwenden.
2. **`css/common.css` ist die Quelle der Wahrheit** — Tokens nicht in einzelnen Webseiten duplizieren.
3. **Semantische Farben korrekt verwenden** — `--success` nur für positive Zustände, nicht dekorativ.
4. **Subtle-Varianten für Hintergründe verwenden** — Volltonfarben primär für Text, Icons und klare Statuspunkte.
5. **Z-Index nur via Token verwenden** — Werte wie `z-index: 999` sind verboten.
6. **Neue Muster dokumentieren** — Wenn ein neuer Seitentyp oder eine neue Komponente nötig ist, zuerst in `docs/` beschreiben.
7. **Demo-CSS nicht produktiv verwenden** — `css/demo.css` ist nur für Komponenten- und Referenzseiten gedacht.
8. **Brand- und Naming-Regeln beachten** — sichtbare Namen und Logos nach `docs/brand.md`, `docs/naming.md` und `docs/logo.md` verwenden.
9. **Coding-Agenten folgen `docs/for-coding-agents.md`** — automatisierte Änderungen müssen diese Regeln beachten.

---

## Empfohlener Ablauf für neue Webseiten

1. Passenden Seitentyp in `docs/page-types.md` auswählen.
2. Falls nötig, passenden Sidebar-Typ in `docs/sidebar-types.md` auswählen.
3. Benötigte Komponenten in `components/` ansehen.
4. CSS-Dateien nach `docs/usage.md` einbinden.
5. Bestehende Klassen und Tokens verwenden.
6. Sichtbaren Namen nach `docs/naming.md` wählen.
7. Logo/Favicon nach `docs/logo.md` einbinden.
8. Copyright-/Quellenhinweise nach `docs/copyright-display.md` prüfen.
9. Keine lokalen Sonderstyles anlegen, solange ein bestehendes Pattern passt.
10. Bei neuen UI-Patterns zuerst Dokumentation und Referenz-HTML im CI-Repo ergänzen.

---

## Begriffsklärung

Dieses Repository deckt mehrere Ebenen ab:

| Begriff | Bedeutung in diesem Repo |
|---|---|
| CI / Corporate Identity | Grundlegende visuelle und organisatorische Identität |
| Brand | Name, Tonalität, Logo, Wiedererkennbarkeit |
| Design System | Tokens, Komponenten, Layouts, Seitentypen und Nutzungsregeln |
| CSS Library | Produktive CSS-Dateien, die in Webseiten eingebunden werden |
| Komponenten-Referenz | HTML-Demos in `components/` zur visuellen Prüfung |
| Dokumentation | Spezifikation, Regeln und Entscheidungshilfen in `docs/` |

Details stehen in:

```text
docs/concepts.md
```

---

## Versionierung

Versionierung erfolgt über Git-Tags und `CHANGELOG.md`, nicht über Dateinamen.

Beispiele:

```text
v1.0.0
v1.1.0
v1.1.1
v2.0.0
```

Dateinamen bleiben stabil:

```text
README.md
docs/tokens.md
docs/usage.md
```

Details stehen in:

```text
docs/versioning.md
```

---

## Änderungshistorie

Die zentrale Änderungshistorie steht in:

```text
CHANGELOG.md
```

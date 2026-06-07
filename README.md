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

<!-- AUTOGEN:structure START -->
```text
css/badges.css
css/buttons.css
css/calendar.css
css/cards.css
css/code-viewer.css
css/common.css
css/coords.css
css/demo.css
css/forms.css
css/index.css
css/modal.css
css/page.css
css/service-dashboard.css
css/sidebar.css
css/toast.css
css/topbar.css
css/typography.css
css/utils.css
components/badges.html
components/buttons-demo.html
components/buttons.html
components/calendar.html
components/cards.html
components/code-viewer.html
components/context-menu.html
components/forms.html
components/modal.html
components/page-types.html
components/service-dashboard-config.html
components/service-dashboard-detail.html
components/service-dashboard-overview.html
components/sidebar-types.html
components/sidebar.html
components/toast.html
components/tokens.html
components/topbar.html
components/typography-preview.html
components/typography.html
components/utils.html
docs/badges.md
docs/brand.md
docs/buttons.md
docs/calendar.md
docs/cards.md
docs/cli.md
docs/code-viewer.md
docs/concepts.md
docs/context-menu.md
docs/copyright-display.md
docs/copyright.md
docs/for-coding-agents.md
docs/forms.md
docs/geocoder-dropdown.md
docs/logo.md
docs/map-legend.md
docs/map-routes.md
docs/modal.md
docs/naming.md
docs/page-types.md
docs/page.md
docs/resources.md
docs/roadmap.md
docs/service-dashboard.md
docs/sidebar-types.md
docs/sidebar.md
docs/toast.md
docs/tokens.md
docs/topbar.md
docs/typography.md
docs/usage.md
docs/versioning.md
```
<!-- AUTOGEN:structure END -->

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

<!-- AUTOGEN:status START -->
| Element | Spec | Referenz-HTML | CSS |
|---|---|---|---|
| Topbar | ✅ | ✅ | ✅ |
| Sidebar + Accordion | ✅ | ✅ | ✅ |
| Cards | ✅ | ✅ | ✅ |
| Buttons | ✅ | ✅ | ✅ |
| Badges | ✅ | ✅ | ✅ |
| Seitenstruktur | ✅ | ✅ | ✅ |
| Forms | ✅ | ✅ | ✅ |
| Modal + Karten-Popup | ✅ | ✅ | ✅ |
| Context-Menu + Action-Menu | ✅ | ✅ | — |
| Typografie | ✅ | ✅ | ✅ |
| Kalender | ✅ | ✅ | ✅ |
| Code-Viewer | ✅ | ✅ | ✅ |
| Toast | ✅ | ✅ | ✅ |
| Koordinaten-Umrechner (Sidebar Typ 7) | — | — | ✅ |
| Utility-Klassen | — | ✅ | ✅ |
| Service-Dashboard | ✅ | ✅ | ✅ |
<!-- AUTOGEN:status END -->

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

# Begriffe & Ebenen

Diese Datei definiert, wie zentrale Begriffe im `oe5ith-ci` Repository verwendet werden.

Ziel ist, dass Dokumentation, CSS, Komponenten und spätere Coding-Agenten dieselben Begriffe
gleich verstehen.

---

## Überblick

`oe5ith-ci` deckt mehrere Ebenen ab:

| Begriff | Bedeutung |
|---|---|
| CI / Corporate Identity | Grundlegende visuelle und organisatorische Identität der OE5ITH-Webseiten |
| Brand | Markennahe Regeln wie Logo, Name, Tonalität und Wiedererkennbarkeit |
| Design System | System aus Tokens, Komponenten, Layouts, Seitentypen und Nutzungsregeln |
| CSS Library | Produktive CSS-Dateien, die in Webseiten eingebunden werden |
| Komponenten-Referenz | HTML-Demos zur visuellen Prüfung einzelner Komponenten |
| Dokumentation | Spezifikation, Regeln und Entscheidungshilfen für Umsetzung und Pflege |

---

## CI / Corporate Identity

Die Corporate Identity beschreibt die übergeordnete Identität der OE5ITH-Webseiten.

Dazu gehören:

- Name und Schreibweise
- Logo und Favicons
- Grundfarben
- allgemeiner visueller Stil
- Copyright- und Quellenhinweise
- Wiedererkennbarkeit über verschiedene Webseiten hinweg

Die CI beantwortet die Frage:

> Woran erkennt man, dass eine Webseite zum OE5ITH-System gehört?

In diesem Repository liegen CI-relevante Inhalte vor allem in:

- `assets/`
- `docs/copyright.md`
- `docs/copyright-display.md`
- `docs/resources.md`
- `docs/tokens.md`

---

## Brand

Der Begriff Brand wird hier für markennahe Regeln verwendet.

Dazu gehören zum Beispiel:

- wie `OE5ITH` geschrieben wird
- wann welches Logo oder Favicon verwendet wird
- welche Bezeichnungen für Dienste genutzt werden
- wie neutral, technisch oder erklärend Texte formuliert werden sollen

Brand-Regeln sind nicht zwingend CSS-Regeln. Sie betreffen auch Inhalte, Namen und Darstellung.

Beispiele:

- `OE5ITH Cloud Portal`
- `OE5ITH Tiles`
- `OE5ITH Routing`
- `OE5ITH SDR`
- `OE5ITH Monitoring`

---

## Design System

Das Design System ist die praktische Umsetzung der visuellen Regeln.

Es besteht aus:

- Design Tokens
- Komponenten
- Layout-Regeln
- Seitentypen
- Sidebar-Typen
- Interaktionsmustern
- Accessibility-Regeln
- Dokumentation zur korrekten Verwendung

Das Design System beantwortet die Frage:

> Wie baue ich eine neue OE5ITH-Webseite konsistent auf?

Wichtige Dateien:

- `docs/tokens.md`
- `docs/page-types.md`
- `docs/sidebar-types.md`
- `docs/topbar.md`
- `docs/sidebar.md`
- `docs/cards.md`
- `docs/buttons.md`
- `docs/forms.md`
- `docs/modal.md`
- `docs/typography.md`

---

## CSS Library

Die CSS Library ist der produktive Teil des Repositories.

Sie besteht aus den Dateien in `css/`, die direkt in Webseiten eingebunden werden können.

Wichtig:

- `css/common.css` ist immer zuerst einzubinden.
- `css/index.css` bündelt alle produktiven Komponenten.
- `css/demo.css` ist nur für Referenzseiten gedacht und nicht für produktive Webseiten.

Die CSS Library beantwortet die Frage:

> Welche CSS-Dateien muss eine Webseite einbinden, damit sie nach OE5ITH-CI aussieht?

---

## Komponenten-Referenz

Die Komponenten-Referenz besteht aus HTML-Dateien im Verzeichnis `components/`.

Diese Dateien sind live testbare Beispiele für:

- Topbar
- Sidebar
- Cards
- Buttons
- Badges
- Forms
- Modal
- Context-Menu
- Typografie
- Tokens
- Seitentypen
- Sidebar-Typen

Sie dienen als visuelle Kontrolle und Vorlage, sind aber keine produktiven Webseiten.

Die Komponenten-Referenz beantwortet die Frage:

> Wie sieht eine Komponente konkret aus und wie wird sie im HTML verwendet?

---

## Dokumentation

Die Dokumentation liegt in `docs/`.

Sie beschreibt:

- Zweck einer Komponente
- erlaubte Varianten
- HTML-Struktur
- CSS-Klassen
- Nutzungsregeln
- Entscheidungshilfen
- Abgrenzungen zu anderen Komponenten oder Seitentypen

Die Dokumentation beantwortet die Frage:

> Wann und wie soll ein Element verwendet werden?

---

## Abgrenzung

### CI ist nicht gleich CSS

Die CI beschreibt die übergeordnete Identität.
CSS ist nur ein technisches Mittel, um Teile davon umzusetzen.

### Design System ist nicht gleich Komponenten-Sammlung

Ein Design System enthält nicht nur Buttons und Cards, sondern auch Regeln,
wann welche Komponente oder welcher Seitentyp verwendet wird.

### Komponenten-Demos sind keine Produktivseiten

Dateien in `components/` dürfen als Vorlage dienen, sollen aber nicht direkt als
fertige produktive Webseiten kopiert werden.

### Demo-CSS ist nicht produktiv

`css/demo.css` ist nur für Referenz- und Vorschauseiten gedacht.

---

## Regeln für neue Inhalte

1. Neue Farben, Abstände oder Z-Index-Werte zuerst als Token definieren.
2. Neue Komponenten zuerst in `docs/` beschreiben.
3. Neue Komponenten danach als Referenz in `components/` visualisieren.
4. Produktive CSS-Regeln in `css/` ablegen.
5. Keine lokalen Sonderlösungen in einzelnen Webseiten einbauen, wenn ein bestehendes Pattern passt.
6. Wenn ein Pattern nicht passt, zuerst prüfen, ob ein neuer Seitentyp oder eine neue Komponente nötig ist.

---

## Empfohlene Reihenfolge bei neuen Webseiten

1. Passenden Seitentyp in `docs/page-types.md` auswählen.
2. Passenden Sidebar-Typ in `docs/sidebar-types.md` auswählen.
3. Komponenten in `components/` ansehen.
4. CSS aus `css/` einbinden.
5. Nur bestehende Tokens und Klassen verwenden.
6. Abweichungen dokumentieren, bevor sie umgesetzt werden.

---

## Kurzform

| Frage | Zuständiger Bereich |
|---|---|
| Wie heißt der Dienst? | Brand / Naming |
| Welche Farben und Abstände gibt es? | Tokens |
| Wie sieht ein Button aus? | Komponenten |
| Welche Seite passt für meinen Anwendungsfall? | Seitentypen |
| Welche CSS-Datei muss ich einbinden? | CSS Library |
| Wie wird Copyright angezeigt? | CI / Copyright-Doku |
| Wie soll ein Coding-Agent arbeiten? | Dokumentation und Regeln |

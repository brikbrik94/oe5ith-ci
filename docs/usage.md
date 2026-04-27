# Verwendung des OE5ITH CI

Diese Datei beschreibt, wie das `oe5ith-ci` Design System in Webseiten eingebunden und verwendet wird.

Ziel ist, dass alle OE5ITH-Webseiten dieselben Grundlagen, Tokens und Komponenten verwenden.

---

## Grundprinzip

Jede Webseite verwendet die CSS-Dateien aus dem Verzeichnis `css/`.

Die wichtigste Datei ist:

```text
css/common.css
```

Sie enthält:

- Design Tokens
- Basis-Reset
- grundlegendes Seitenlayout
- globale Farb- und Typografie-Regeln

`css/common.css` muss immer vor allen anderen CSS-Dateien eingebunden werden.

---

## Variante 1: Alle produktiven Komponenten einbinden

Für einfache Seiten oder neue Projekte kann die komplette produktive CSS-Bibliothek eingebunden werden:

```html
<link rel="stylesheet" href="css/index.css">
```

`css/index.css` importiert die produktiven CI-Komponenten zentral.

Diese Variante ist sinnvoll, wenn:

- die Seite mehrere CI-Komponenten verwendet
- die Dateigröße keine kritische Rolle spielt
- eine schnelle und konsistente Einbindung gewünscht ist
- die Seite ein klassisches OE5ITH-Portal oder Dashboard ist

---

## Variante 2: Nur benötigte Komponenten einbinden

Für schlankere Seiten können CSS-Dateien gezielt eingebunden werden.

Beispiel:

```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/typography.css">
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/cards.css">
<link rel="stylesheet" href="css/topbar.css">
<link rel="stylesheet" href="css/sidebar.css">
```

Diese Variante ist sinnvoll, wenn:

- eine Seite nur wenige Komponenten verwendet
- die Ladegröße reduziert werden soll
- eine Spezialseite nur einzelne CI-Elemente benötigt
- eine Karten-App eigene Layoutregeln verwendet

---

## Empfohlene Reihenfolge

Wenn CSS-Dateien einzeln eingebunden werden, gilt diese Reihenfolge:

1. `css/common.css`
2. `css/typography.css`
3. `css/badges.css`
4. `css/buttons.css`
5. `css/cards.css`
6. `css/topbar.css`
7. `css/sidebar.css`
8. `css/page.css`
9. `css/forms.css`
10. `css/modal.css`

Begründung:

- `css/common.css` definiert Tokens und Basisregeln.
- Typografie und kleine UI-Elemente kommen vor größeren Komponenten.
- Layout-Komponenten wie Topbar, Sidebar und Page-Strukturen kommen danach.
- Formulare und Modals hängen oft von den vorherigen Tokens und Komponenten ab.

---

## Demo-CSS nicht produktiv verwenden

Die Datei:

```text
css/demo.css
```

ist ausschließlich für Referenz- und Komponenten-Demos gedacht.

Sie darf nicht in produktive Webseiten eingebunden werden.

Produktive Webseiten verwenden entweder:

```html
<link rel="stylesheet" href="css/index.css">
```

oder eine gezielte Auswahl produktiver CSS-Dateien.

---

## Startpunkt für neue Webseiten

Für neue Webseiten gilt dieser Ablauf:

1. Passenden Seitentyp in `docs/page-types.md` auswählen.
2. Falls vorhanden, passenden Sidebar-Typ in `docs/sidebar-types.md` auswählen.
3. Passende Komponenten in `components/` ansehen.
4. CSS-Dateien nach dieser Datei einbinden.
5. Nur bestehende Tokens und Klassen verwenden.
6. Keine Farben, Abstände, Radien, Shadows oder Z-Index-Werte hardcoden.
7. Falls ein Pattern fehlt, zuerst im CI-Repo dokumentieren und dann umsetzen.

---

## Beispiel: Dashboard-Seite

```html
<link rel="stylesheet" href="css/index.css">
```

Typische Verwendung:

- Topbar
- Sidebar
- Card-Grid
- Status-Badges
- Buttons

Passender Seitentyp:

```text
docs/page-types.md → Typ 3 — Dashboard
```

---

## Beispiel: Detail-Seite

```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/typography.css">
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/badges.css">
<link rel="stylesheet" href="css/cards.css">
<link rel="stylesheet" href="css/topbar.css">
<link rel="stylesheet" href="css/sidebar.css">
<link rel="stylesheet" href="css/page.css">
<link rel="stylesheet" href="css/forms.css">
```

Typische Verwendung:

- Page-Header
- Panels
- Formularbereiche
- Statusanzeigen
- Codeblöcke
- Tabellen

Passender Seitentyp:

```text
docs/page-types.md → Typ 1 — Detail-Seite
```

---

## Beispiel: Karten-Seite

Karten-Seiten sind ein Sonderfall.

Sie verwenden meist:

```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/topbar.css">
<link rel="stylesheet" href="css/sidebar.css">
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/badges.css">
<link rel="stylesheet" href="css/modal.css">
```

Wichtig:

- `css/page.css` wird bei Vollbild-Karten meist nicht verwendet.
- Die Karte füllt den Hauptbereich direkt aus.
- Sidebar enthält meist Layer-Gruppen oder Accordions.
- MapLibre/Leaflet-spezifische Overrides liegen in `css/modal.css`.

Passender Seitentyp:

```text
docs/page-types.md → Karten-Seite (Sonderfall)
```

---

## Pfade

Die Beispiele verwenden relative Pfade:

```html
<link rel="stylesheet" href="css/index.css">
```

Je nach Deployment können die Pfade angepasst werden, zum Beispiel:

```html
<link rel="stylesheet" href="/assets/oe5ith-ci/css/index.css">
```

oder:

```html
<link rel="stylesheet" href="https://example.org/assets/oe5ith-ci/css/index.css">
```

Wichtig ist, dass die Reihenfolge der Dateien erhalten bleibt.

---

## Regeln für lokale Anpassungen

Lokale Anpassungen in einzelnen Webseiten sollen vermieden werden.

Erlaubt sind lokale Styles nur für:

- projektspezifische Inhalte
- einmalige Datenvisualisierungen
- Layouts, die im CI noch nicht existieren
- technische Sonderfälle

Nicht erlaubt sind lokale Duplikate von:

- Farben
- Buttons
- Cards
- Badges
- Topbar
- Sidebar
- Standardformularen
- Z-Index-Werten

Wenn ein wiederverwendbares Pattern fehlt, soll es zuerst im CI-Repo ergänzt werden.

---

## Mindest-Einbindung

Die kleinste sinnvolle CI-Einbindung ist:

```html
<link rel="stylesheet" href="css/common.css">
```

Damit sind Tokens, Reset und Basislayout verfügbar.

Für eine sichtbare OE5ITH-Optik sollten in der Regel zusätzlich mindestens verwendet werden:

```html
<link rel="stylesheet" href="css/typography.css">
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/cards.css">
```

---

## Prüfliste

Vor dem Veröffentlichen einer Seite prüfen:

- [ ] `css/common.css` ist eingebunden.
- [ ] CSS-Dateien sind in richtiger Reihenfolge eingebunden.
- [ ] Keine CI-Werte wurden lokal hardcodiert.
- [ ] Kein `css/demo.css` in produktiver Seite.
- [ ] Passender Seitentyp wurde verwendet.
- [ ] Buttons, Badges, Cards und Formulare verwenden CI-Klassen.
- [ ] Z-Index-Werte verwenden Tokens.
- [ ] Copyright-/Quellenhinweise sind korrekt eingebunden.

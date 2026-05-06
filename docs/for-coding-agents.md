# Regeln für Coding-Agenten

Diese Datei beschreibt, wie Coding-Agenten mit dem `oe5ith-ci` Repository und den darauf basierenden Webseiten arbeiten sollen.

Ziel ist, dass automatisierte Änderungen keine lokalen Sonderlösungen erzeugen und die bestehende CI-/Design-System-Struktur respektieren.

---

## Grundsatz

Ein Coding-Agent darf keine neue visuelle Logik erfinden, solange im CI-Repo bereits ein passendes Pattern existiert.

Vor jeder UI-Änderung ist zu prüfen:

1. Gibt es einen passenden Seitentyp?
2. Gibt es eine passende Komponente?
3. Gibt es bereits passende Tokens?
4. Gibt es eine bestehende Referenz in `components/`?
5. Gibt es eine Spezifikation in `docs/`?

Erst wenn kein bestehendes Pattern passt, darf ein neues Pattern vorgeschlagen werden.

---

## Wichtige Dateien

| Datei / Ordner | Bedeutung |
|---|---|
| `css/common.css` | Quelle der Wahrheit für Tokens, Reset und Basislayout |
| `css/index.css` | Master-Import für produktive CI-Komponenten |
| `css/demo.css` | Nur für Referenzseiten, nicht produktiv verwenden |
| `docs/tokens.md` | Dokumentation aller Tokens |
| `docs/page-types.md` | Entscheidungshilfe für Seitentypen |
| `docs/sidebar-types.md` | Entscheidungshilfe für Sidebar-Typen |
| `docs/usage.md` | Anleitung zur CSS-Einbindung |
| `components/` | Visuelle Referenzen und HTML-Beispiele |
| `assets/` | Logo, Favicons und CI-Assets |

---

## Pflichtregeln

### 1. Keine Werte hardcoden

Nicht erlaubt:

```css
color: #3b82f6;
background: #252525;
border-radius: 12px;
z-index: 999;
```

Stattdessen Tokens verwenden:

```css
color: var(--accent);
background: var(--card-bg);
border-radius: var(--card-radius);
z-index: var(--z-dropdown);
```

Diese Regel gilt für:

- Farben
- Hintergründe
- Borders
- Radien
- Shadows
- Z-Index
- Transitions
- wiederverwendbare Layoutwerte

---

### 2. `css/common.css` immer zuerst einbinden

Wenn CSS-Dateien einzeln eingebunden werden, muss `css/common.css` immer zuerst geladen werden.

Richtig:

```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/cards.css">
```

Falsch:

```html
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/common.css">
```

---

### 3. `css/demo.css` nicht produktiv verwenden

`css/demo.css` ist ausschließlich für Dateien in `components/` oder andere Referenzseiten gedacht.

Produktive Webseiten dürfen `css/demo.css` nicht einbinden.

---

### 4. Bestehende Komponenten verwenden

Wenn Buttons, Cards, Badges, Forms, Modals, Topbar oder Sidebar benötigt werden, müssen vorhandene Klassen und Patterns verwendet werden.

Keine neuen Klassen wie:

```css
.my-special-button
.custom-card-dark
.new-sidebar-item
```

anlegen, wenn ein bestehendes CI-Pattern passt.

---

### 5. Bestehende Seitentypen verwenden

Vor dem Erstellen oder Ändern einer Seite muss `docs/page-types.md` geprüft werden.

Aktuelle Seitentypen:

- Detail-Seite
- Listen-Seite
- Dashboard
- Karten-Grid
- Landing Page
- Karten-Seite als Sonderfall

Wenn keiner dieser Typen passt, muss zuerst ein neuer Seitentyp dokumentiert werden.

---

### 5a. API-Debugger / Code-Viewer

Seiten, die API-Antworten oder technische Rohdaten anzeigen, verwenden das `.panel-code` Pattern.

**Seitentyp:** Typ 1 — Detail-Seite.

**Zwei Panels:**

1. **Control Panel** — normales `.panel` mit `.form-row` für horizontal angeordnete Eingabefelder.
   Labels über Feldern: `.ci-label`. Mono-Inputs: `.form-input.mono`.

2. **Code Viewer** — `.panel.panel-code` mit:
   - `.panel-header`: Titel links, `badge-green`/`badge-red` + Latenz + Copy-Button rechts.
   - `<pre class="code-viewer-pre">`: scrollbarer Code-Block.

**Regeln:**
- Kein `background` hardcoden — `var(--code-bg)` verwenden.
- HTTP-Status immer als Badge darstellen: `badge-green` (2xx), `badge-red` (4xx/5xx), `badge-yellow` (3xx).
- Latenz als `<span class="panel-meta">42 ms</span>` neben dem Badge.
- Copy-Button: `.btn.btn-sm.btn-ghost`.
- Kein CSS-Grid, kein lokales Panel-Styling — nur `.panel.panel-code`.

**Referenz:** `components/code-viewer.html`, `docs/code-viewer.md`

---

### 6. Karten-Seiten sind Sonderfälle

Karten-Seiten mit Leaflet oder MapLibre verwenden eigene Layoutregeln.

Wichtig:

- `css/page.css` wird bei Vollbild-Karten meist nicht verwendet.
- Die Karte füllt den Hauptbereich direkt aus.
- Sidebar enthält meist Layer-Gruppen oder Accordions.
- MapLibre-/Leaflet-Overrides liegen in `css/modal.css`.
- Z-Index-Werte müssen mit den Karten-Engines kompatibel bleiben.

Keine pauschalen Page-Layouts auf Karten-Seiten anwenden.

---

### 7. Keine Pfade eigenmächtig ändern

Deployment-Pfade dürfen nicht ohne expliziten Auftrag geändert werden.

Nicht eigenmächtig ändern:

- CSS-Pfade
- Asset-Pfade
- Font-Pfade
- Sprite-Pfade
- Tile-/PMTiles-Pfade
- API-Endpunkte
- Domainnamen

Wenn ein Pfad unklar ist, muss die bestehende Struktur beibehalten und die Unsicherheit dokumentiert werden.

---

### 8. Keine Struktur ohne Grund umbauen

Nicht erlaubt ohne expliziten Auftrag:

- bestehende Dateien umbenennen
- Ordnerstruktur ändern
- Komponenten zusammenlegen
- CSS-Dateien aufteilen
- Klassen großflächig umbenennen
- bestehende Dokumentation entfernen

Änderungen sollen klein, nachvollziehbar und rückwärtskompatibel sein.

---

## Neue Komponenten

Wenn eine neue Komponente nötig ist, gilt dieser Ablauf:

1. Zweck und Anwendungsfall in `docs/<komponente>.md` beschreiben.
2. HTML-Struktur und Klassen definieren.
3. CSS-Datei in `css/` ergänzen oder bestehende passende Datei erweitern.
4. Referenz-HTML in `components/` erstellen.
5. Falls nötig, `README.md` und `docs/usage.md` aktualisieren.
6. Keine bestehenden Komponenten brechen.

---

## Neue Tokens

Neue Tokens dürfen nur ergänzt werden, wenn ein Wert mehrfach oder semantisch wiederverwendbar ist.

Beispiele für sinnvolle Tokens:

```css
--surface-map-control: ...
--space-4: ...
--radius-panel: ...
--z-toast: ...
```

Nicht sinnvoll:

```css
--special-padding-for-one-card: ...
--blue-from-test-page: ...
```

Neue Tokens müssen dokumentiert werden in:

```text
docs/tokens.md
```

und definiert werden in:

```text
css/common.css
```

---

## Lokale Styles in Webseiten

Lokale Styles sind nur erlaubt für:

- projektspezifische Datenvisualisierungen
- einmalige technische Sonderfälle
- Inhalte, die im CI noch nicht generalisiert sind
- externe Bibliotheken, die eigene Anpassungen benötigen

Lokale Styles dürfen nicht verwendet werden, um CI-Komponenten nachzubauen oder zu überschreiben.

---

## Änderung bestehender Webseiten

Bei Änderungen an bestehenden Webseiten gilt:

1. Bestehende Struktur lesen.
2. Verwendete CI-Dateien identifizieren.
3. Nur die betroffenen Dateien ändern.
4. Keine unbeteiligten Bereiche neu formatieren.
5. Keine fremden Stilkonzepte einführen.
6. Bestehende Pfade und Namen beibehalten.
7. Änderungen möglichst klein halten.

---

## HTML-Regeln

HTML soll semantisch und nachvollziehbar bleiben.

Empfehlungen:

- Buttons als `<button>` umsetzen, wenn eine Aktion ausgelöst wird.
- Links als `<a>` umsetzen, wenn navigiert wird.
- Tabellen nur für echte tabellarische Daten verwenden.
- Überschriftenhierarchie nicht überspringen.
- Formularelemente mit Labels versehen.
- Interaktive Elemente tastaturbedienbar halten.

---

## Accessibility-Regeln

Coding-Agenten sollen auf grundlegende Barrierefreiheit achten:

- ausreichender Farbkontrast
- sichtbare Fokuszustände
- sinnvolle `aria-label`, wenn Text fehlt
- keine reine Farbcodierung ohne Text/Icon
- Tastaturbedienbarkeit für Menüs, Modals und Buttons
- `prefers-reduced-motion` respektieren, wenn Animationen ergänzt werden

---

## CSS-Regeln

CSS soll wartbar und CI-konform bleiben.

Regeln:

- Tokens statt Rohwerte verwenden.
- Bestehende Klassennamen respektieren.
- Komponenten-CSS nicht mit Seiten-spezifischem CSS vermischen.
- Keine globalen Selektoren ergänzen, wenn eine Komponentenklasse reicht.
- Keine `!important` verwenden, außer zur bewussten Korrektur externer Bibliotheken.
- Z-Index nur über Tokens.
- Keine externen Fonts oder CDNs ohne Dokumentation in `docs/resources.md`.

---

## JavaScript-Regeln

Falls JavaScript ergänzt wird:

- UI-Zustände über Klassen steuern.
- Keine Inline-Styles setzen, wenn eine CSS-Klasse ausreicht.
- Kein `style="..."` in dynamisch erzeugten HTML-Strings im JS/TS-Code. Ausnahme: Werte die erst zur Laufzeit berechnet werden können (z.B. Pixel-Positionen aus JS-Events, dynamische Breiten/Höhen aus Messungen). Für alle anderen Fälle: CI-Klassen verwenden.
- Keine hart codierten Farben oder Layoutwerte in JavaScript.
- Bestehende IDs und Klassen nicht ohne Grund ändern.
- Event-Handler nachvollziehbar benennen.
- Karten-spezifische Logik von allgemeiner UI-Logik trennen.

---

## Umgang mit externen Ressourcen

Externe Ressourcen sollen bevorzugt selbst gehostet werden, wenn sie Teil der CI oder einer produktiven Seite sind.

Dazu gehören:

- Fonts
- Icons
- Sprites
- CSS-Bibliotheken
- JavaScript-Bibliotheken

Neue externe Ressourcen müssen in `docs/resources.md` dokumentiert werden.

Lizenz- oder Copyright-relevante Ressourcen müssen zusätzlich in `docs/copyright.md` dokumentiert werden.

---

## Prüfliste vor Abschluss einer Änderung

Vor Abschluss einer Änderung prüfen:

- [ ] `css/common.css` ist weiterhin Quelle der Wahrheit.
- [ ] Keine Farben oder Z-Index-Werte wurden hardcodiert.
- [ ] Keine produktive Seite verwendet `css/demo.css`.
- [ ] Bestehende Komponenten wurden wiederverwendet.
- [ ] Neue Komponenten wurden dokumentiert.
- [ ] Neue Tokens wurden in `css/common.css` und `docs/tokens.md` ergänzt.
- [ ] README oder Usage-Doku wurde aktualisiert, falls die Nutzung betroffen ist.
- [ ] Keine Pfade oder Deploy-Strukturen wurden unbeabsichtigt geändert.
- [ ] Änderungen sind klein und nachvollziehbar.
- [ ] Karten-Seiten wurden als Sonderfall behandelt.

---

## Kurzfassung für Agenten

Wenn du an OE5ITH-Webseiten arbeitest:

1. Lies zuerst `README.md`.
2. Lies danach `docs/usage.md`.
3. Prüfe `docs/page-types.md`.
4. Verwende vorhandene Tokens aus `css/common.css`.
5. Verwende vorhandene Komponenten aus `css/` und `components/`.
6. Erfinde keine lokalen Sonderstyles.
7. Ändere keine Pfade ohne Auftrag.
8. Dokumentiere neue Patterns zuerst im CI-Repo.

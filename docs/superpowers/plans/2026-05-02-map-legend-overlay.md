# Map Legend Overlay — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Karten-Legende als fixiertes Panel rechts unten mit Vanilla-JS-API (`MapLegend`), drei Eintragstypen (Punkt, Linie, Fläche) und beliebigen Farben, steuerbar über einen Topbar-Button.

**Architecture:** CSS-Klassen in `css/modal.css` (bestehende Heimat aller Map-Styles). Referenz-HTML + vollständige `MapLegend`-Klasse (Vanilla JS) in `components/modal.html`. Dokumentation in `docs/map-legend.md`. Keine neuen Tokens — alle verwendeten Tokens existieren bereits.

**Tech Stack:** CSS Custom Properties, Vanilla JS (ES6 class), kein Build-Schritt.

---

## Dateien

| Aktion | Pfad | Zweck |
|---|---|---|
| Modify | `css/modal.css` | Neuer Abschnitt `MAP LEGEND` am Ende der Datei |
| Modify | `components/modal.html` | Legend-Panel-HTML + Demo-Abschnitt + `MapLegend`-Klasse im `<script>` |
| Create | `docs/map-legend.md` | Komponenten-Dokumentation |

---

## Task 1: CSS — Map-Legend-Klassen

**Dateien:**
- Modify: `css/modal.css` (am Ende, nach Zeile 484)

- [ ] **Schritt 1: CSS-Block anfügen**

Folgendes an das Ende von `css/modal.css` anhängen (nach der letzten geschweiften Klammer):

```css

/* ═══════════════════════════════════════
   MAP LEGEND
   Fixiertes Info-Panel rechts unten über
   der Karte. Befüllung per MapLegend-API.
   ═══════════════════════════════════════ */
.map-legend {
  position: fixed;
  bottom: 16px;
  right: 16px;
  z-index: var(--z-overlay);
  background: var(--card-bg);
  border: 1px solid var(--border-strong);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-card);
  min-width: 160px;
  max-width: 260px;
  padding: 12px 14px;
}

.map-legend-title {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 8px;
}

.map-legend-entries {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.map-legend-entry {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 3px 0;
}

.map-legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.map-legend-line {
  width: 24px;
  height: 3px;
  border-radius: 2px;
  flex-shrink: 0;
}

.map-legend-area {
  width: 16px;
  height: 12px;
  border-radius: 3px;
  opacity: 0.8;
  flex-shrink: 0;
}

.map-legend-label {
  font-size: 0.8rem;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

- [ ] **Schritt 2: Visuell prüfen**

`components/modal.html` im Browser öffnen — Seite muss fehlerfrei laden (keine CSS-Fehler in DevTools). Das Panel ist noch nicht sichtbar, da es kein HTML-Element gibt — das kommt in Task 2.

- [ ] **Schritt 3: Commit**

```bash
git add css/modal.css
git commit -m "feat: add map-legend CSS classes to modal.css"
```

---

## Task 2: HTML — Panel-Struktur und Demo-Abschnitt

**Dateien:**
- Modify: `components/modal.html`

Das Panel-HTML wird an zwei Stellen eingefügt:
1. Das versteckte `<div class="map-legend">` am Anfang des `<body>` (wie das Modal-Backdrop)
2. Ein Demo-Abschnitt im Hauptinhalt, der die Legende live demonstriert

- [ ] **Schritt 1: Legend-Panel-HTML einfügen**

In `components/modal.html` nach dem bestehenden Block `<!-- ═══ MODAL (versteckt, wird per JS geöffnet) ═══ -->` (Zeile ~431) folgendes einfügen:

```html
<!-- ═══ MAP LEGEND ═══ -->
<div class="map-legend" id="demo-legend" style="display:none; position:fixed; bottom:16px; right:16px;">
  <div class="map-legend-title"></div>
  <div class="map-legend-entries"></div>
</div>
```

- [ ] **Schritt 2: Demo-Abschnitt einfügen**

In `components/modal.html` den letzten `<!-- ═══ ... ═══ -->` Demo-Abschnitt (Karten-Popup Detailliert, endet bei Zeile ~574) suchen. Direkt **danach**, vor dem schließenden `</div>` (Zeile 576) folgenden Block einfügen:

```html
  <!-- ═══ MAP LEGEND ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Karten-Legende</div>
    <div class="demo-section-desc">
      Fixiertes Panel rechts unten. Befüllung per <code>MapLegend</code>-API.
      Drei Eintragstypen: <code>dot</code>, <code>line</code>, <code>area</code>.
      Beliebige CSS-Farben. Ein-/Ausblenden über <code>legend.toggle()</code>.
    </div>
    <div class="demo-row">
      <button class="demo-trigger" onclick="demoLegendToggle()">Legende ein-/ausblenden</button>
      <button class="demo-trigger" onclick="demoLegendReset()">Demo-Einträge neu laden</button>
    </div>

    <!-- Statisches Markup-Beispiel (nicht live, nur Referenz) -->
    <div style="margin-top:24px; padding:12px 14px; background:var(--panel-deep); border:1px solid var(--border); border-radius:8px; display:inline-block;">
      <div class="map-legend" style="position:static; box-shadow:none; min-width:0;">
        <div class="map-legend-title">Kartenschlüssel</div>
        <div class="map-legend-entries">
          <div class="map-legend-entry">
            <div class="map-legend-dot" style="background:#22c55e;"></div>
            <span class="map-legend-label">Feuerwehr aktiv</span>
          </div>
          <div class="map-legend-entry">
            <div class="map-legend-line" style="background:#3b82f6;"></div>
            <span class="map-legend-label">Route</span>
          </div>
          <div class="map-legend-entry">
            <div class="map-legend-area" style="background:#f59e0b;"></div>
            <span class="map-legend-label">Sperrzone</span>
          </div>
        </div>
      </div>
    </div>
  </div>
```

- [ ] **Schritt 3: Visuell prüfen**

`components/modal.html` im Browser öffnen:
- Demo-Abschnitt "Karten-Legende" muss am Ende der Seite erscheinen
- Statisches Markup-Beispiel zeigt drei Einträge korrekt (grüner Punkt, blauer Strich, gelbes Rechteck)
- Buttons sind sichtbar (JS-Logik folgt in Task 3)

- [ ] **Schritt 4: Commit**

```bash
git add components/modal.html
git commit -m "feat: add map-legend HTML panel and demo section to modal.html"
```

---

## Task 3: JS — MapLegend-Klasse und Demo-Verdrahtung

**Dateien:**
- Modify: `components/modal.html` (im bestehenden `<script>`-Block, Zeile ~578)

- [ ] **Schritt 1: MapLegend-Klasse einfügen**

Im `<script>`-Block von `components/modal.html` (beginnt bei `<script>` vor `/* ── Modal ── */`) die Klasse **vor dem bestehenden Code** einfügen:

```js
/* ── MapLegend ── */
class MapLegend {
  constructor(selector) {
    this._el = typeof selector === 'string'
      ? document.querySelector(selector)
      : selector;
    this._titleEl = this._el.querySelector('.map-legend-title');
    this._entriesEl = this._el.querySelector('.map-legend-entries');
  }

  setTitle(text) {
    this._titleEl.textContent = text;
    this._titleEl.style.display = text ? '' : 'none';
  }

  addEntry({ type, color, label }) {
    const typeClass = { dot: 'map-legend-dot', line: 'map-legend-line', area: 'map-legend-area' }[type];
    const entry = document.createElement('div');
    entry.className = 'map-legend-entry';

    const indicator = document.createElement('div');
    indicator.className = typeClass;
    indicator.style.background = color;

    const labelEl = document.createElement('span');
    labelEl.className = 'map-legend-label';
    labelEl.textContent = label;

    entry.appendChild(indicator);
    entry.appendChild(labelEl);
    this._entriesEl.appendChild(entry);
  }

  clearEntries() {
    this._entriesEl.innerHTML = '';
  }

  show() {
    this._el.style.display = '';
  }

  hide() {
    this._el.style.display = 'none';
  }

  toggle() {
    this.isVisible() ? this.hide() : this.show();
  }

  isVisible() {
    return this._el.style.display !== 'none';
  }

  destroy() {
    this._el.remove();
  }
}
```

- [ ] **Schritt 2: Demo-Funktionen und Initialisierung einfügen**

Direkt nach der Klasse (noch vor `/* ── Modal ── */`) einfügen:

```js
/* ── MapLegend Demo ── */
const demoLegend = new MapLegend('#demo-legend');

function demoLegendReset() {
  demoLegend.clearEntries();
  demoLegend.setTitle('Kartenschlüssel');
  demoLegend.addEntry({ type: 'dot',  color: '#22c55e', label: 'Feuerwehr aktiv' });
  demoLegend.addEntry({ type: 'dot',  color: '#ef4444', label: 'Feuerwehr inaktiv' });
  demoLegend.addEntry({ type: 'line', color: '#3b82f6', label: 'Anfahrtsroute' });
  demoLegend.addEntry({ type: 'area', color: '#f59e0b', label: 'Sperrzone' });
  demoLegend.addEntry({ type: 'area', color: '#8b5cf6', label: 'Einsatzgebiet' });
  demoLegend.show();
}

function demoLegendToggle() {
  demoLegend.toggle();
}

demoLegendReset();
```

- [ ] **Schritt 3: Visuell prüfen**

`components/modal.html` im Browser öffnen und testen:

1. Beim Laden erscheint die Legende rechts unten mit 5 Einträgen und Titel "Kartenschlüssel"
2. Button "Legende ein-/ausblenden" → Panel verschwindet; nochmals klicken → erscheint wieder
3. Button "Demo-Einträge neu laden" → Einträge werden geleert und neu befüllt
4. Alle drei Typen korrekt dargestellt:
   - `dot`: Kreis 10×10px
   - `line`: Flache Linie 24×3px
   - `area`: Rechteck 16×12px mit leichter Transparenz
5. DevTools zeigen keine JS-Fehler

- [ ] **Schritt 4: Commit**

```bash
git add components/modal.html
git commit -m "feat: add MapLegend JS class and demo wiring to modal.html"
```

---

## Task 4: Dokumentation

**Dateien:**
- Create: `docs/map-legend.md`

- [ ] **Schritt 1: Dokumentationsdatei anlegen**

`docs/map-legend.md` erstellen. Inhalt (äußere `~~~`-Fence wird nicht in die Datei geschrieben):

~~~markdown
# Map Legend

Fixiertes Overlay-Panel rechts unten über der Karte. Zeigt eine Legende mit
farbkodierten Einträgen. Gesteuert über die `MapLegend`-JS-Klasse.

## Voraussetzungen

- `css/modal.css` geladen (enthält `.map-legend`-Klassen)
- `MapLegend`-Klasse eingebunden (aus `components/modal.html` kopieren oder eigenem Bundle)

## HTML-Grundstruktur

```html
<div class="map-legend" id="map-legend" style="display:none;">
  <div class="map-legend-title"></div>
  <div class="map-legend-entries"></div>
</div>
```

Das Panel startet mit `display:none` — `MapLegend.show()` macht es sichtbar.

## JS-API

```js
const legend = new MapLegend('#map-legend');

legend.setTitle('Kartenschlüssel');

legend.addEntry({ type: 'dot',  color: '#22c55e', label: 'Aktiv' });
legend.addEntry({ type: 'line', color: '#3b82f6', label: 'Route' });
legend.addEntry({ type: 'area', color: '#f59e0b', label: 'Sperrzone' });

legend.clearEntries();
legend.show();
legend.hide();
legend.toggle();
legend.isVisible(); // boolean
legend.destroy();   // entfernt Panel aus DOM
```

## Eintragstypen

| `type` | Indikator | Verwendung |
|---|---|---|
| `dot` | Kreis 10×10px | Punktmarker, Stationen |
| `line` | Linie 24×3px | Routen, Grenzen, Verbindungen |
| `area` | Rechteck 16×12px | Zonen, Flächen, Polygone |

`color` akzeptiert jeden gültigen CSS-Farbwert (`#hex`, `rgb()`, Farbnamen).

## Topbar-Button

Standard `.topbar-toggle` ohne neues Styling:

```html
<button class="topbar-toggle" id="legend-toggle" title="Legende">
  <i class="fa-solid fa-list"></i>
</button>
```

```js
const btn = document.getElementById('legend-toggle');
btn.addEventListener('click', () => {
  legend.toggle();
  btn.classList.toggle('active', legend.isVisible());
});
```

## TypeScript

```ts
interface LegendEntry {
  type: 'dot' | 'line' | 'area';
  color: string;
  label: string;
}
```

Die `MapLegend`-Klasse kann direkt in TS importiert oder mit Typen annotiert werden.

## Referenz

Lebende Demo: `components/modal.html` — Abschnitt "Karten-Legende"
~~~

- [ ] **Schritt 2: Visuell prüfen**

Datei öffnen und sicherstellen dass:
- Kein "TBD" oder Platzhalter enthalten ist
- Alle Code-Blöcke vollständig sind
- TypeScript-Interface mit der JS-API übereinstimmt

- [ ] **Schritt 3: Commit**

```bash
git add docs/map-legend.md
git commit -m "docs: add map-legend component documentation"
```

---

## Abschluss-Check

- [ ] `css/modal.css` enthält alle `.map-legend*`-Klassen, keine hardcodierten Farben oder z-Index-Werte
- [ ] `components/modal.html` zeigt Demo mit allen drei Eintragstypen
- [ ] `MapLegend`-Klasse deckt alle API-Methoden aus dem Spec ab: `setTitle`, `addEntry`, `clearEntries`, `show`, `hide`, `toggle`, `isVisible`, `destroy`
- [ ] `docs/map-legend.md` existiert und ist vollständig
- [ ] Kein `display:none` im CSS (Sichtbarkeit wird ausschließlich per JS gesteuert)
- [ ] Keine neuen Tokens in `css/common.css` nötig (alle Token existieren bereits)

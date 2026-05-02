# Map Route Styles — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Visuelle Linienstile für Kartenrouten und Luftlinien dokumentieren und als JS-Referenzkonstante mit SVG-Demo in das CI einbetten.

**Architecture:** Kein neues CSS und keine neuen Tokens — Kartenlinien werden von Leaflet/MapLibre als SVG/Canvas gerendert, nicht per CSS gestylt. Das CI liefert ein dokumentiertes JS-Konstantenobjekt (`MAP_ROUTE_STYLES`) das Projekte direkt kopieren. Zwei semantische Zustände: `active` (accent-blau, durchgehend) und `background` (gedimmt-grau, für Vergleichsrouten und Luftlinien). Dokumentation in `docs/map-routes.md`, SVG-Vorschau + Konstante in `components/modal.html`, Zukunfts-Notiz in `docs/roadmap.md`.

**Tech Stack:** Vanilla JS, SVG (inline), Leaflet-kompatible Polyline-Options, MapLibre GL paint-Properties.

---

## Dateien

| Aktion | Pfad | Zweck |
|---|---|---|
| Create | `docs/map-routes.md` | Vollständige Komponentendokumentation |
| Modify | `components/modal.html` | Neuer Demo-Abschnitt "Kartenlinienstile" mit SVG-Vorschau und Konstantenreferenz |
| Modify | `docs/roadmap.md` | Roadmap-Eintrag: Variante C bei Erweiterung |

---

## Task 1: Dokumentation — docs/map-routes.md

**Dateien:**
- Create: `docs/map-routes.md`

- [ ] **Schritt 1: Datei erstellen**

`docs/map-routes.md` erstellen. Inhalt (äußere `~~~`-Fence nicht in die Datei schreiben):

~~~markdown
# Map Route Styles

Visuelle Linienstile für Routen und Luftlinien auf Karten. Zwei semantische
Zustände: `active` (hervorgehobene Route) und `background` (Vergleichsrouten,
Luftlinien). Bereitgestellt als JS-Konstantenobjekt — kein CSS, da
Leaflet/MapLibre Linien als SVG/Canvas rendern.

## Linienzustände

| Zustand | Zweck | Farbe | Stärke | Deckkraft |
|---|---|---|---|---|
| `active` | Hervorgehobene/aktive Route | `#3b82f6` (`--accent`) | 5px | 1.0 |
| `background` | Vergleichsrouten, Luftlinien zu NAH-Stützpunkten | `#888888` (`--muted`) | 3px | 0.6 |

`background` deckt beide Anwendungsfälle ab — die geometrische Form (Straße vs.
gerade Linie) liefert auf der Karte ausreichend visuelle Unterscheidung.

## JS-Konstante

In TypeScript-Projekten kopieren oder importieren:

```js
const MAP_ROUTE_STYLES = {
  active: {
    color:   '#3b82f6',   /* --accent */
    weight:  5,
    opacity: 1.0,
  },
  background: {
    color:   '#888888',   /* --muted */
    weight:  3,
    opacity: 0.6,
  },
};
```

## Leaflet

```js
// Hervorgehobene Route
L.polyline(latlngs, MAP_ROUTE_STYLES.active).addTo(map);

// Vergleichsroute oder Luftlinie
L.polyline(latlngs, MAP_ROUTE_STYLES.background).addTo(map);
```

## MapLibre GL

```js
map.addLayer({
  id: 'route-active',
  type: 'line',
  source: 'route-source',
  paint: {
    'line-color':   MAP_ROUTE_STYLES.active.color,
    'line-width':   MAP_ROUTE_STYLES.active.weight,
    'line-opacity': MAP_ROUTE_STYLES.active.opacity,
  },
});

map.addLayer({
  id: 'route-background',
  type: 'line',
  source: 'background-source',
  paint: {
    'line-color':   MAP_ROUTE_STYLES.background.color,
    'line-width':   MAP_ROUTE_STYLES.background.weight,
    'line-opacity': MAP_ROUTE_STYLES.background.opacity,
  },
});
```

## MapLegend-Integration

Zusammen mit der `MapLegend`-Komponente (`docs/map-legend.md`):

```js
legend.addEntry({ type: 'line', color: MAP_ROUTE_STYLES.active.color,     label: 'Aktive Route' });
legend.addEntry({ type: 'line', color: MAP_ROUTE_STYLES.background.color, label: 'Vergleichsroute' });
```

## TypeScript

```ts
type RouteStyleKey = 'active' | 'background';

interface RouteStyle {
  color:   string;
  weight:  number;
  opacity: number;
}

const MAP_ROUTE_STYLES: Record<RouteStyleKey, RouteStyle> = { /* ... */ };
```

## Referenz

Lebende Demo: `components/modal.html` — Abschnitt "Kartenlinienstile"
~~~

- [ ] **Schritt 2: Prüfen**

Datei lesen und sicherstellen:
- Alle Abschnitte vorhanden (Linienzustände, JS-Konstante, Leaflet, MapLibre, MapLegend, TypeScript, Referenz)
- Keine `TBD`-Platzhalter
- TypeScript-Interface stimmt mit der JS-Konstante überein

- [ ] **Schritt 3: Commit**

```bash
git add docs/map-routes.md
git commit -m "docs: add map-routes component documentation"
```

---

## Task 2: Demo-Abschnitt in components/modal.html

**Dateien:**
- Modify: `components/modal.html` (nach dem `<!-- ═══ MAP LEGEND ═══ -->` Demo-Abschnitt, vor dem schließenden `</div>` des Hauptinhalts, ca. Zeile 616)

- [ ] **Schritt 1: Demo-Abschnitt einfügen**

In `components/modal.html` den Block suchen der mit `  </div>\n\n</div>` endet (das Ende des Karten-Legende-Abschnitts gefolgt vom schließenden Haupt-`</div>`). Direkt **vor** dem `\n</div>` (dem Haupt-Content-Schließtag) einfügen:

```html
  <!-- ═══ KARTENLINIENSTILE ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Kartenlinienstile</div>
    <div class="demo-section-desc">
      JS-Konstantenobjekt für Routen und Luftlinien. Kompatibel mit Leaflet und MapLibre GL.
      Zwei Zustände: <code>active</code> (hervorgehobene Route) und
      <code>background</code> (Vergleichsrouten, Luftlinien).
    </div>

    <!-- SVG-Vorschau -->
    <div style="display:inline-block; margin-bottom:16px; background:var(--panel-deep); border:1px solid var(--border); border-radius:8px; padding:12px 16px;">
      <svg width="228" height="68">
        <line x1="0" y1="16" x2="228" y2="16" stroke="#3b82f6" stroke-width="5" stroke-linecap="round"/>
        <text x="0" y="30" fill="#888888" font-size="10" font-family="system-ui,sans-serif">active — #3b82f6, 5px, opacity 1.0</text>
        <line x1="0" y1="50" x2="228" y2="50" stroke="#888888" stroke-width="3" stroke-linecap="round" opacity="0.6"/>
        <text x="0" y="64" fill="#888888" font-size="10" font-family="system-ui,sans-serif">background — #888888, 3px, opacity 0.6</text>
      </svg>
    </div>

    <!-- Konstantenreferenz -->
    <pre style="background:var(--panel-deep); border:1px solid var(--border); border-radius:8px; padding:12px 14px; font-size:0.78rem; color:var(--text); overflow-x:auto; margin:0;">const MAP_ROUTE_STYLES = {
  active:     { color: '#3b82f6', weight: 5, opacity: 1.0 },
  background: { color: '#888888', weight: 3, opacity: 0.6 },
};</pre>
  </div>
```

- [ ] **Schritt 2: Prüfen**

Relevanten Bereich von `components/modal.html` lesen und sicherstellen:
- Demo-Abschnitt "Kartenlinienstile" ist nach dem "Karten-Legende"-Abschnitt vorhanden
- SVG-Element mit zwei `<line>`-Elementen (blau + grau) korrekt eingebettet
- `<pre>`-Block mit der Konstante vollständig
- HTML korrekt geschachtelt (kein fehlendes closing tag)

- [ ] **Schritt 3: Commit**

```bash
git add components/modal.html
git commit -m "feat: add map route styles demo section to modal.html"
```

---

## Task 3: Roadmap-Eintrag — Variante C

**Dateien:**
- Modify: `docs/roadmap.md`

- [ ] **Schritt 1: Roadmap-Eintrag einfügen**

In `docs/roadmap.md` den Abschnitt `## Spätere mögliche Releases` suchen (ca. Zeile 333). Direkt **nach** der Zeile `## Spätere mögliche Releases` und **vor** `### v1.3.0` folgendes einfügen:

```markdown
### Kartenstile — Erweiterung auf Variante C

Aktuell: `MAP_ROUTE_STYLES` als dokumentiertes JS-Inline-Objekt zum Kopieren (Variante A).

Sobald weitere Linienzustände hinzukommen (z.B. gesperrt, alternativ, geplant,
Rückweg), soll das Objekt in eine dedizierte TypeScript-Referenzdatei ausgelagert
werden:

```text
scripts/map-styles.ts
```

Diese Datei würde alle Kartenstil-Konstanten (Routen, Marker, Polygone) zentral
bündeln und direkt importierbar machen. Dokumentation in `docs/map-routes.md`
entsprechend aktualisieren.

---

```

- [ ] **Schritt 2: Prüfen**

Abschnitt in `docs/roadmap.md` lesen und sicherstellen:
- Eintrag steht unter `## Spätere mögliche Releases`, vor `### v1.3.0`
- Pfad `scripts/map-styles.ts` ist angegeben
- Kein `TBD`

- [ ] **Schritt 3: Commit**

```bash
git add docs/roadmap.md
git commit -m "docs: add map-styles Variante C roadmap entry"
```

---

## Abschluss-Check

- [ ] `docs/map-routes.md` existiert mit allen 7 Abschnitten
- [ ] `MAP_ROUTE_STYLES` enthält exakt `active` und `background` mit `color`, `weight`, `opacity`
- [ ] SVG in `components/modal.html` zeigt blau (active) und gedimmt-grau (background)
- [ ] `<pre>`-Block in `components/modal.html` enthält die Konstante korrekt
- [ ] Roadmap-Eintrag nennt `scripts/map-styles.ts` als Zielpfad
- [ ] Kein neues CSS, keine neuen Tokens in `css/common.css`

# Map Route Styles — Design Spec

**Datum:** 2026-05-02  
**Status:** Approved

## Überblick

Visuelle Spezifikation für Linien auf Karten (Routen und Luftlinien). Zwei semantische Zustände: `active` (hervorgehobene Route) und `background` (Vergleichsrouten, Luftlinien). Implementiert als dokumentiertes JS-Konstantenobjekt (Variante A) — kein neues CSS, keine neuen Tokens.

---

## 1. Linienzustände

| Zustand | Zweck | Farbe | Stärke | Deckkraft | Strich |
|---|---|---|---|---|---|
| `active` | Hervorgehobene/aktive Route | `#3b82f6` (`--accent`) | 5px | 1.0 | durchgehend |
| `background` | Vergleichsrouten, Luftlinien zu NAH-Stützpunkten | `#888888` (`--muted`) | 3px | 0.6 | durchgehend |

**Abgrenzung:** `background` deckt sowohl Straßenrouten (z.B. Vergleich von Anfahrtswegen verschiedener Dienststellen zum EO) als auch Luftlinien (gerade Verbindungen zu NAH-Stützpunkten) ab. Die geometrische Form (Straßenführung vs. gerade Linie) liefert auf der Karte bereits ausreichend visuelle Unterscheidung.

---

## 2. JS-Referenzobjekt

**Verwendung:** In TypeScript-Projekten kopieren oder importieren.

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

### Leaflet-Verwendung

```js
// Hervorgehobene Route
L.polyline(latlngs, MAP_ROUTE_STYLES.active).addTo(map);

// Vergleichsroute oder Luftlinie
L.polyline(latlngs, MAP_ROUTE_STYLES.background).addTo(map);
```

### MapLibre GL-Verwendung

```js
map.addLayer({
  id: 'route-active',
  type: 'line',
  source: 'route',
  paint: {
    'line-color':   MAP_ROUTE_STYLES.active.color,
    'line-width':   MAP_ROUTE_STYLES.active.weight,
    'line-opacity': MAP_ROUTE_STYLES.active.opacity,
  },
});
```

---

## 3. Legende-Integration

`background`-Linien sollen in der `MapLegend`-Komponente mit dem `line`-Typ und der Farbe aus `MAP_ROUTE_STYLES.background.color` dargestellt werden:

```js
legend.addEntry({ type: 'line', color: MAP_ROUTE_STYLES.background.color, label: 'Vergleichsroute' });
legend.addEntry({ type: 'line', color: MAP_ROUTE_STYLES.active.color,     label: 'Aktive Route' });
```

---

## 4. Dokumentation & Referenz

| Artefakt | Pfad |
|---|---|
| Dokumentation | `docs/map-routes.md` |
| Demo-Abschnitt | `components/modal.html` — Abschnitt "Kartenlinienstile" |
| Roadmap-Eintrag | `docs/roadmap.md` — Migration auf Variante C bei Erweiterung |

---

## 5. Zukünftige Erweiterung (Variante C)

Sobald weitere Linienzustände hinzukommen (z.B. gesperrt, alternativ, geplant), wird `MAP_ROUTE_STYLES` in eine dedizierte TypeScript-Referenzdatei ausgelagert:

```text
css/map-styles.ts   (oder scripts/map-styles.ts)
```

Der Roadmap-Eintrag hält diese Entscheidung fest. Bis dahin bleibt Variante A (dokumentiertes Inline-Objekt zum Kopieren).

---

## 6. Abgrenzung

- Keine neuen CSS-Klassen (Kartenlinien sind SVG/Canvas — kein CSS-Styling)
- Keine neuen Tokens in `css/common.css`
- Keine Behandlung von Sonderzuständen wie "gesperrt" oder "alternativ" (YAGNI)
- Keine automatische Synchronisation mit `css/common.css`-Token-Werten — Werte werden als Kommentar dokumentiert

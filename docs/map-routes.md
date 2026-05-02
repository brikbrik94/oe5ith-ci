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

const MAP_ROUTE_STYLES: Record<RouteStyleKey, RouteStyle> = {
  active:     { color: '#3b82f6', weight: 5, opacity: 1.0 },
  background: { color: '#888888', weight: 3, opacity: 0.6 },
};
```

## Referenz

Lebende Demo: `components/modal.html` — Abschnitt "Kartenlinienstile"

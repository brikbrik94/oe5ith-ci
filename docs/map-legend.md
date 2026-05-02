# Map Legend

Fixiertes Overlay-Panel rechts unten über der Karte. Zeigt eine Legende mit farbkodierten Einträgen. Gesteuert über die `MapLegend`-JS-Klasse.

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

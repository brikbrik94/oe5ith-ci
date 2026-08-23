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

Das Panel startet mit `display:none` — `MapLegend.show()` macht es sichtbar. Die Kindelemente `.map-legend-title` und `.map-legend-entries` müssen im HTML vorhanden sein. `isVisible()` prüft ausschließlich den Inline-Style — CSS-Klassen-basiertes Ausblenden wird nicht erkannt.

## JS-API

```js
const legend = new MapLegend('#map-legend');

legend.setTitle('Kartenschlüssel');

legend.addEntry({ type: 'dot',  color: '#22c55e', label: 'Aktiv' });
legend.addEntry({ type: 'line', color: '#3b82f6', label: 'Route' });
legend.addEntry({ type: 'line', color: '#3b82f6', width: 5, label: 'Skiroute (breit)' });
legend.addEntry({ type: 'line', color: '#3b82f6', dasharray: [2, 1], label: 'Wanderweg (gestrichelt)' });
legend.addEntry({ type: 'area', color: '#f59e0b', label: 'Sperrzone' });
legend.addEntry({ type: 'area', color: '#3b82f6', outline_color: '#1d4ed8', outline_width: 1, label: 'Bezirksgrenze' });
legend.addEntry({ type: 'icon', icon: 'fa-solid fa-helicopter', color: '#22c55e', label: 'Aktiv' });
legend.addEntry({ type: 'line-cased', color: '#3b82f6', width: 3, outline_color: '#ffffff', outline_width: 5, label: 'Skilift (Casing)' });

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
| `line` | Linie 24px lang, Höhe 3px (Default) oder `width`-geclampt 1–6px; optional `dasharray` | Routen, Grenzen, Verbindungen |
| `area` | Rechteck 16×12px, optional Rand via `outline_color`/`outline_width` (geclampt 1–3px) | Zonen, Flächen, Polygone |
| `icon` | FontAwesome-Glyph 12×12px | Symbol-Marker mit Formsemantik (z.B. Fahrzeuge, Stationen) |
| `line-cased` | Linie mit Umrandung — Innenfarbe/-breite (`width`, geclampt 1–6px, zusätzlich gedeckelt auf geclampte `outline_width` − 1) + Außenfarbe/-breite (`outline_width`, geclampt 2–8px) | Straßen-/Liftsymbole mit Casing (z.B. Skilifte) |

Hinweis: `.map-legend-area` hat `opacity: 0.8` — ein per `outline_color` gesetzter Rand erscheint
dadurch leicht abgeschwächt, nicht in Reinfarbe.

`color` akzeptiert jeden gültigen CSS-Farbwert (`#hex`, `rgb()`, Farbnamen).

Bei `type: 'icon'` wird `color` als `style.color` (statt `style.background`) auf das Glyph
angewendet; `icon` ist dann erforderlich und enthält die vollständigen FontAwesome-Klassen
(z.B. `'fa-solid fa-helicopter'`).

## Line-Cased — Struktur

`type: 'line-cased'` erzeugt statt eines einzelnen Indikator-Elements einen Wrapper mit zwei
gestapelten Balken (Outline zuerst im DOM, Inner darüber — die DOM-Reihenfolge reicht für die
Stapelung, kein `z-index` nötig):

Layer-Objekte, die mit `type: 'line'` sowie `outline_color`/`outline_width` ankommen (wie
`geodata-plugin-standard`-Layer, z.B. `ski-lifts`), müssen vom Aufrufer explizit auf
`type: 'line-cased'` gemappt werden — bei `type: 'line'` werden `outline_color`/`outline_width`
vollständig ignoriert (kein Fehler, keine Casing-Darstellung).

```
.map-legend-line-cased
├── .map-legend-line-cased-outline   (Außenfarbe, Höhe = outline_width, geclampt 2–8px)
└── .map-legend-line-cased-inner     (Innenfarbe, Höhe = width, geclampt 1–6px, zusätzlich gedeckelt auf geclampte outline_width − 1)
```

| Element / Klasse | Zweck | Pflicht/Optional |
|---|---|---|
| `.map-legend-line-cased` | Wrapper, `position:relative`, Breite 24px, Höhe = geclampte `outline_width` | Pflicht |
| `.map-legend-line-cased-outline` | Äußerer Balken, `position:absolute`, vertikal zentriert | Pflicht |
| `.map-legend-line-cased-inner` | Innerer Balken, `position:absolute`, vertikal zentriert, liegt über der Outline (DOM-Reihenfolge) | Pflicht |

Alle vier Felder (`color`, `width`, `outline_color`, `outline_width`) sind bei
`type: 'line-cased'` Pflicht — fehlt eines, wirft `addEntry()` einen Fehler.

---

## Modifier: `.map-legend--wide`

Das Panel hat standardmäßig `max-width: var(--sidebar-width)` (300px) — ausreichend für die
Standard-Eintragstypen mit kurzem Label. Enthält ein Panel Einträge mit breiterem Inhalt (z.B.
mehrere Farb-/Formvarianten pro Zeile, längere Labels), reicht 300px oft nicht aus.

```html
<div class="map-legend map-legend--wide" id="map-legend" style="display:none;">
  <div class="map-legend-title"></div>
  <div class="map-legend-entries"></div>
</div>
```

`.map-legend--wide` setzt `max-width: var(--legend-width-wide)` (340px). Rein deklarativ im
HTML gesetzt — keine JS-API dafür, `MapLegend` kennt die Klasse nicht. Die Darstellung von
Mehrfach-Chip-/Varianten-Zeilen selbst (z.B. mehrere farbige Streifen in einem Eintrag) ist
nicht Teil dieser Komponente — nur die Panel-Breite als Rahmen dafür.

---

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
  type: 'dot' | 'line' | 'area' | 'icon' | 'line-cased';
  color: string;
  label: string;
  icon?: string;                 // nur type:'icon', vollständige FontAwesome-Klassen
  width?: number;                // type:'line' (Höhe, geclampt 1–6px) | type:'line-cased' (Pflicht, Innenbreite)
  dasharray?: [number, number];  // type:'line' — [Strich, Lücke], proportional normalisiert auf 8px-Zyklus
  outline_color?: string;        // type:'area' (mit outline_width) | type:'line-cased' (Pflicht)
  outline_width?: number;        // type:'area' (geclampt 1–3px, mit outline_color) | type:'line-cased' (Pflicht, geclampt 2–8px)
}
```

Die `MapLegend`-Klasse kann direkt in TS importiert oder mit Typen annotiert werden.

## Validierung

`addEntry()` wirft einen Fehler in folgenden Fällen:

| Fall | Fehlermeldung |
|---|---|
| `type` unbekannt (und nicht `line-cased`) | `MapLegend.addEntry: unknown type "<type>"` |
| `type:'area'` — nur eines von `outline_color`/`outline_width` gesetzt | `MapLegend.addEntry: 'area' benötigt outline_color UND outline_width zusammen` |
| `type:'line'` — `dasharray` hat nicht genau 2 Werte | `MapLegend.addEntry: dasharray muss genau 2 Werte [dash, gap] enthalten` |
| `type:'line-cased'` — eines der 4 Pflichtfelder (`color`, `width`, `outline_color`, `outline_width`) fehlt | `MapLegend.addEntry: type 'line-cased' benötigt color, width, outline_color, outline_width` |

---

## Referenz

Lebende Demo: `components/modal.html` — Abschnitt "Karten-Legende"

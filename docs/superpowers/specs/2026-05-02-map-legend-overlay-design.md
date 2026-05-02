# Map Legend Overlay — Design Spec

**Datum:** 2026-05-02  
**Status:** Approved

## Überblick

Eine wiederverwendbare Karten-Legende als fixiertes Panel rechts unten über der Karte. Unterstützt drei Eintragstypen (Punkt, Linie, Fläche) mit beliebigen Farben, einen optionalen Titel und eine Vanilla-JS-API, die direkt in TypeScript adaptierbar ist. Ein- und Ausblenden erfolgt über einen Topbar-Button.

---

## 1. HTML-Struktur

```html
<div class="map-legend" id="map-legend">
  <div class="map-legend-title">Kartenschlüssel</div>
  <div class="map-legend-entries">
    <!-- wird per JS befüllt -->
  </div>
</div>
```

Das Panel wird initial leer gerendert; Titel und Einträge werden per JS gesetzt.

---

## 2. CSS

**Datei:** `css/modal.css` (bereits Heimat aller Map-Styles)

**Panel `.map-legend`:**
- `position: fixed; bottom: 16px; right: 16px`
- `z-index: var(--z-overlay)` (1090 — über Karte, unter Topbar)
- `background: var(--card-bg)`
- `border: 1px solid var(--border-strong)`
- `border-radius: var(--card-radius)` (12px)
- `box-shadow: var(--shadow-card)`
- `min-width: 160px; max-width: 260px`
- `padding: 12px 14px`
- Ausgeblendet: `display: none` (JS setzt/entfernt direkt)

**Titel `.map-legend-title`:**
- Uppercase, `font-size: 0.65rem`, `font-weight: 700`, `letter-spacing: 1.2px`
- `color: var(--muted)` — identisch zu `.sidebar-section-label`
- `margin-bottom: 8px`
- Wird nicht gerendert wenn leer

**Eintrags-Zeile `.map-legend-entry`:**
- `display: flex; align-items: center; gap: 8px`
- `padding: 3px 0`

**Indikator-Typen** — Farbe immer per `style="background: <color>"`:

| Klasse | Größe | Radius | Besonderheit |
|---|---|---|---|
| `.map-legend-dot` | 10×10px | 50% | — |
| `.map-legend-line` | 24×3px | 2px | — |
| `.map-legend-area` | 16×12px | 3px | `opacity: 0.8` |

**Label `.map-legend-label`:**
- `font-size: 0.8rem; color: var(--text)`
- `white-space: nowrap; overflow: hidden; text-overflow: ellipsis`

Keine neuen Tokens erforderlich — alle verwendeten Tokens existieren bereits in `css/common.css`.

---

## 3. JS-API

**Datei:** Referenzimplementierung in `components/modal.html` (als `<script>`-Block)

```js
class MapLegend {
  constructor(selector)          // bindet sich an ein bestehendes DOM-Element (Selector oder Element-Referenz); erstellt kein neues Element
  setTitle(text)                 // Titel setzen; leerer String → .map-legend-title bekommt display:none
  addEntry({ type, color, label }) // type: 'dot' | 'line' | 'area'; hängt Eintrag an .map-legend-entries an
  clearEntries()                 // alle Einträge aus .map-legend-entries entfernen
  show()                         // setzt display auf ursprünglichen Wert (block)
  hide()                         // setzt display: none auf dem Panel
  toggle()                       // wechselt zwischen show() und hide()
  isVisible()                    // gibt true zurück wenn Panel nicht display:none
  destroy()                      // entfernt Panel vollständig aus dem DOM
}
```

**TypeScript-Interface (zur Dokumentation):**
```ts
interface LegendEntry {
  type: 'dot' | 'line' | 'area';
  color: string;   // beliebiger CSS-Farbwert
  label: string;
}
```

Die Klasse hat keine externen Abhängigkeiten und braucht keinen Build-Schritt.

---

## 4. Topbar-Integration

**Button** — verwendet bestehende `.topbar-toggle`-Klasse, kein neues Styling:

```html
<button class="topbar-toggle" id="legend-toggle" title="Legende">
  <i class="fa-solid fa-list"></i>
</button>
```

**Logik:**
```js
const btn = document.getElementById('legend-toggle');
btn.addEventListener('click', () => {
  legend.toggle();
  btn.classList.toggle('active', legend.isVisible());
});
```

`.active` auf dem Button folgt dem bestehenden Topbar-Toggle-Muster.

---

## 5. Dokumentation & Referenz

| Artefakt | Pfad |
|---|---|
| CSS | `css/modal.css` — Abschnitt `MAP LEGEND` |
| Referenz-HTML + JS | `components/modal.html` |
| Dokumentation | `docs/map-legend.md` |

---

## 6. Abgrenzung

- Keine Gruppierung / Sections innerhalb der Legende (YAGNI)
- Keine Animations-Übergänge beim Ein-/Ausblenden (kann später ergänzt werden)
- Keine automatische Positionierung relativ zur Karte — immer `fixed` bottom-right
- Die TS-Implementierung lebt in der Konsumenten-App, nicht im CI-Repo

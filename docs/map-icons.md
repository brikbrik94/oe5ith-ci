# Map-Icons (SDF-Form-Quellen)

**Assets:** `assets/map-icons/`  
**Referenz:** `components/map-icons.html`  
**Status:** definiert · v1.17.0

---

## Zweck & Abgrenzung

`assets/map-icons/` ist die **Source of Truth für generische, einfarbige SDF-Form-Quellen** (Pins, Label-Bubbles, neutrale Marker und Symbole), die CI-konsistent und über MapLibres `icon-color` zur Laufzeit umfärbbar sind.

**Bewusst nicht hier:**

- **Keine Build-Logik.** Das Sprite-Sheet wird in einem separaten Build-Repo erzeugt, das dieses Repo (und weitere) als Submodul einbindet und *ein* gemeinsames Sheet baut.
- **Keine org-/einsatzspezifischen Vollfarb-Icons** (z. B. `nef-*`, `rd-*`, `nah-*` aus `oe5ith-markers`). Diese sind mehrfarbiges Organisations-Branding, **nicht SDF-fähig** — SDF ist single-channel, beschränkt auf eine umfärbbare Farbe — und bleiben im Domänen-Repo.

Die SDF-Beschränkung zieht die Trennlinie: nur monochrome, umfärbbare Formen gehören hierher. Nur MapLibre wird unterstützt (alle aktuellen Projekte).

---

## Verzeichnis

```
assets/map-icons/
├── ci-pin.svg
├── ci-pin-hole.svg
├── ci-pin-fallback.svg          (geplant)
├── ci-bubble-label.svg
├── ci-bubble-tail.svg           (geplant)
├── ci-marker-dot.svg
├── ci-marker-ring.svg
├── ci-marker-square.svg         (geplant)
├── ci-marker-diamond.svg        (geplant)
├── ci-symbol-location.svg
├── ci-symbol-warning.svg
├── ci-symbol-info.svg           (geplant)
├── ci-symbol-star.svg           (geplant)
├── ci-symbol-flag.svg           (geplant)
└── icons.json                   ← Manifest = die nach-außen-API
```

Das Verzeichnis wird vom Konsistenz-Check **nicht** erfasst (er prüft nur `css/`, `components/`, `docs/`) — daher entstehen keine Orphan-/Dangling-Fehler für SVGs und Manifest. Die SVGs werden **nicht** einzeln in `registry.json` gelistet; `icons.json` ist ihre Registry.

---

## Katalog

Alle 14 vorgesehenen Icons, 7 davon im initialen Release `v1.17.0` ausgeliefert:

| Kategorie | Icon-ID | Zweck | Release |
|---|---|---|---|
| pin | `ci-pin` | Standard-Tropfen-Pin (Standort) | **v1.17.0** |
| pin | `ci-pin-hole` | Pin mit Loch — farbiger Punkt/Symbol dahinter sichtbar | **v1.17.0** |
| pin | `ci-pin-fallback` | Generischer Fallback-Pin | geplant |
| bubble | `ci-bubble-label` | Dehnbarer Hintergrund für Straßen-/Ortslabels | **v1.17.0** |
| bubble | `ci-bubble-tail` | Dito mit Zeiger/Tail (Callout) | geplant |
| marker | `ci-marker-dot` | Gefüllter Kreis (Punktmarker, Stationen) | **v1.17.0** |
| marker | `ci-marker-ring` | Kreis-Outline (Auswahl/Position) | **v1.17.0** |
| marker | `ci-marker-square` | Gerundetes Quadrat | geplant |
| marker | `ci-marker-diamond` | Raute | geplant |
| symbol | `ci-symbol-location` | Fadenkreuz / aktuelle Position | **v1.17.0** |
| symbol | `ci-symbol-warning` | Neutrales Warndreieck (generische Gefahr) | **v1.17.0** |
| symbol | `ci-symbol-info` | Info-Kreis | geplant |
| symbol | `ci-symbol-star` | POI / Favorit | geplant |
| symbol | `ci-symbol-flag` | Start-/Zielmarker | geplant |

„Geplant"-Icons sind dokumentiert, aber noch nicht als SVG enthalten. Sie werden ohne Breaking Change als MINOR-Releases ergänzt.

---

## Namensschema

- **Icon-ID im Sprite:** `ci-<kategorie>-<name>` bzw. `ci-<name>` — fester `ci-`-Präfix, der diesem Repo gehört und Kollisionen im gemeinsamen Sprite-Sheet ausschließt.
- **Dateiname:** identisch zur ID, also `<id>.svg` (z. B. `ci-pin.svg`).
- Beispiele: `ci-pin`, `ci-pin-hole`, `ci-bubble-label`, `ci-marker-dot`, `ci-symbol-location`.
- Neue Icons: immer `ci-`-Präfix; keine Unterverzeichnisse.

---

## Größensystem

Raster wie das bestehende `oe5ith-markers`-Sheet (pixelRatio 1; `@2x` erzeugt der externe Builder):

| Kategorie | viewBox | Pixel | Anker |
|---|---|---|---|
| marker | `0 0 64 64` | 64×64 | center |
| bubble | `0 0 64 64` | 64×64 | center |
| pin | `0 0 64 80` | 64×80 | bottom |

```
Pin (64×80)               Marker/Bubble (64×64)
  ┌────┐                     ┌────┐
  │    │                     │ ●  │  anchor: center
  └─▽──┘  anchor: bottom     └────┘
```

Der **Anker** bestimmt, wo MapLibre das Icon an der Koordinate ausrichtet:
- `bottom` — Pin-Spitze zeigt auf die Koordinate (Standardfall für Pins).
- `center` — Mittelpunkt des Icons liegt auf der Koordinate (Marker, Bubbles, Symbole).

---

## SDF-Authoring-Regeln

Diese Regeln sind **verbindlich** für alle SVGs in `assets/map-icons/`:

- **Monochrom, gefüllte Flächen.** Keine reinen Striche (Strokes) — SDF degradiert dünne Linien. Strokes immer in Pfade umwandeln (Outline → Fill). `ci-marker-ring` ist korrekt als Donut-Pfad (Fill-Rule `evenodd`) realisiert, nicht als `stroke`.
- **`fill="currentColor"`** im SVG. Für SDF zählt nur die Form/Alpha; `currentColor` lässt außerdem die HTML-Referenzgalerie per CSS umfärben.
- **Exakte `viewBox`** = Raster aus dem Größensystem (§ oben). Kein Whitespace außerhalb.
- **Safe-Area-Puffer ≥ 4 px** (im 64er-Raster) zum Rand, damit Distanzfeld und optionales `icon-halo` Platz haben.
- **Eine Pfad-/Gruppenebene** — kein eingebettetes Raster, keine `<filter>`-Elemente, keine `<text>`-Elemente, keine `<image>`-Elemente.

---

## Manifest-Schema (`icons.json`)

`icons.json` ist die maschinenlesbare API für **Builder** (welche Dateien, SDF, Stretch-Zonen) und **Konsumenten/Legende** (Anker, empfohlene Farbe).

```json
{
  "version": 1,
  "grid": { "marker": [64, 64], "bubble": [64, 64], "pin": [64, 80] },
  "icons": [
    {
      "name": "ci-pin",
      "category": "pin",
      "file": "ci-pin.svg",
      "viewBox": [64, 80],
      "anchor": "bottom",
      "sdf": true,
      "recommendedColor": "--accent"
    },
    {
      "name": "ci-bubble-label",
      "category": "bubble",
      "file": "ci-bubble-label.svg",
      "viewBox": [64, 64],
      "anchor": "center",
      "sdf": true,
      "recommendedColor": "--panel",
      "stretchX": [[20, 44]],
      "stretchY": [[28, 36]],
      "content": [12, 24, 52, 40]
    }
  ]
}
```

Felddefinitionen:

| Feld | Pflicht | Typ | Bedeutung |
|---|---|---|---|
| `name` | ja | string | Icon-ID im Sprite (`ci-`-präfixt, siehe Namensschema) |
| `category` | ja | string | `pin` \| `bubble` \| `marker` \| `symbol` |
| `file` | ja | string | Dateiname relativ zu `assets/map-icons/` |
| `viewBox` | ja | `[w, h]` | Exakt das Raster aus dem Größensystem |
| `anchor` | ja | string | MapLibre `icon-anchor`: `bottom` (Pins) \| `center` (alle anderen) |
| `sdf` | ja | boolean | Immer `true` in diesem Repo |
| `recommendedColor` | ja | string | Empfohlener CI-Token-Name für `icon-color`, ohne `var()` |
| `stretchX` | nur bubble | `[[from, to], …]` | Dehnbare Pixelbereiche auf der X-Achse (MapLibre-Sprite-Spec) |
| `stretchY` | nur bubble | `[[from, to], …]` | Dehnbare Pixelbereiche auf der Y-Achse |
| `content` | nur bubble | `[left, top, right, bottom]` | Text-Content-Box für `icon-text-fit: both` |

**Regel:** `stretchX`, `stretchY` und `content` dürfen **nur** bei Bubbles vorkommen. Bei allen anderen Kategorien (pin, marker, symbol) sind diese Felder wegzulassen.

---

## Recoloring

SDF-Icons werden zur Laufzeit ausschließlich über die MapLibre-Paint-Property **`icon-color`** eingefärbt — im SVG selbst wird keine Farbe kodiert (nur die Form/Alpha-Maske zählt).

`icons.json` trägt pro Icon das Feld `recommendedColor` mit dem empfohlenen CI-Token-Namen (z. B. `--accent`, `--warning`, `--panel`). Der Konsument löst den Token in seinen tatsächlichen Hex-Wert auf und setzt diesen als `icon-color`:

```js
// Token aus dem CI-Stylesheet auslesen:
const accent = getComputedStyle(document.documentElement)
  .getPropertyValue('--accent').trim();  // → z. B. "#3b82f6"

// Als icon-color verwenden:
paint: { 'icon-color': accent }
```

Eigene Farbwahl ist jederzeit möglich — `recommendedColor` ist eine Empfehlung, keine Einschränkung. Für Status-Semantiken (warn, off) die entsprechenden `--warning`- bzw. `--error`-Tokens verwenden.

---

## Builder-Vertrag

Ein externer Builder (separates Sprite-Build-Repo), der `assets/map-icons/` als Quelle einbindet, **muss** folgendes beachten:

1. **Alle SVGs scannen:** `assets/map-icons/*.svg` — jede Datei im Verzeichnis ist ein Icon.
2. **Alle Icons sind SDF:** `sdf: true` im Manifest und als `sdf: true` im erzeugten `sprite.json` übernehmen.
3. **Namen bereits `ci-`-präfixt:** Die Dateinamen (`ci-pin.svg`) entsprechen direkt der Sprite-ID — keine Umbennung nötig.
4. **`stretchX`/`stretchY`/`content` aus `icons.json` ins `sprite.json` übernehmen:** Diese Felder sind für MapLibres dehnbare Icons zwingend erforderlich und dürfen nicht verloren gehen. Der Builder liest sie aus dem Manifest und trägt sie 1:1 in den jeweiligen Sprite-Eintrag ein.
5. **`@2x`-Variante erzeugen:** Der Builder liefert pixelRatio 1 und pixelRatio 2 (`@2x`) — die SVGs selbst sind pixelRatio-unabhängig.

---

## Konsumenten-Snippets (MapLibre)

### Einfacher Pin

```js
map.addLayer({
  id: 'stations',
  type: 'symbol',
  source: 'stations',
  layout: {
    'icon-image': 'ci-pin',
    'icon-anchor': 'bottom',
    'icon-size': 0.5
  },
  paint: {
    'icon-color': '#3b82f6'   // SDF-Recoloring: beliebiger Hex-Wert (z. B. --accent aufgelöst)
  }
});
```

### Dehnbarer Label-Hintergrund (`ci-bubble-label`)

```js
map.addLayer({
  id: 'street-labels',
  type: 'symbol',
  source: 'streets',
  layout: {
    'icon-image': 'ci-bubble-label',
    'icon-text-fit': 'both',         // dehnt die Bubble an stretchX/stretchY auf Textbreite
    'text-field': ['get', 'name']
  },
  paint: {
    'icon-color': '#ffffff'   // z. B. --panel aufgelöst
  }
});
```

`icon-text-fit: both` funktioniert nur korrekt, wenn der Builder `stretchX`, `stretchY` und `content` aus `icons.json` ins `sprite.json` übernommen hat (siehe Builder-Vertrag).

---

## Regeln

1. **Neues Icon:** SVG nach Authoring-Regeln erstellen → in `assets/map-icons/` ablegen → Eintrag in `icons.json` ergänzen (alle Pflichtfelder; Bubble: auch Stretch-Felder) → Galerie `components/map-icons.html` um eine Karte erweitern.
2. **Kein produktiver CSS-Code.** Keine CI-Klassen, keine neuen Tokens — Recoloring läuft ausschließlich über MapLibre `icon-color`.
3. **Keine Build-Logik** in diesem Repo. SVGs und Manifest sind reine Quellen; der Builder liegt extern.
4. **Konsistenz-Check** erfasst `assets/map-icons/` nicht — Änderungen am Verzeichnis lösen keinen Check-Fehler aus. Der Check prüft aber `docs/map-icons.md` als registrierte Dokumentation.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-22 | Initiale Definition. 7 SDF-Icons (`v1.17.0`), Manifest, Builder-Vertrag, Konsumenten-Snippet. |

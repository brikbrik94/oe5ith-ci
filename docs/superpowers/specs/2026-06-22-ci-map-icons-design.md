# CI Map-Icons (SDF-Form-Quellen) — Design / Spec

**Datum:** 2026-06-22
**Status:** Freigegeben · zur Umsetzung
**Angefragt von:** OE5ITH-Webmapping (MapLibre) — CI-konsistente Marker-Formen
**Version:** additiv → MINOR `v1.17.0`

Freigegebene, technisch geklärte Design-Spec für eine neue Asset-Kategorie im
CI-Repo: einfarbige, umfärbbare **SDF-Form-Quellen** für MapLibre-Karten.

---

## 1. Zweck & Abgrenzung

Dieses Repo wird **Source of Truth für generische, einfarbige SDF-Form-Quellen**
(Pins, Label-Bubbles, neutrale Marker/Symbole), die CI-konsistent und über
MapLibres `icon-color` umfärbbar sind.

**Bewusst nicht hier:**
- **Keine Build-Logik.** Das Sprite-Sheet wird in einem separaten Build-Repo
  erzeugt, das dieses Repo (und weitere) als Submodul einbindet und *ein*
  gemeinsames Sheet baut.
- **Keine org-/einsatzspezifischen Vollfarb-Icons** (z. B. `nef-*`, `rd-*`,
  `nah-*` aus dem bestehenden `oe5ith-markers`-Sheet). Diese sind mehrfarbiges
  reales Organisations-Branding, **nicht SDF-fähig** (SDF ist single-channel,
  auf *eine* umfärbbare Farbe beschränkt) und bleiben im Domänen-Repo.

Die SDF-Beschränkung zieht die Trennlinie: nur monochrome, umfärbbare
Marken-Formen gehören hierher.

Nur MapLibre wird unterstützt (alle aktuellen Projekte) → ausschließlich SDF,
keine Vollfarb-Raster-Varianten in diesem Repo.

---

## 2. Verzeichnis & Schnittstelle

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

`assets/map-icons/` wird vom Konsistenz-Check **nicht** erfasst (er prüft nur
`css/`, `components/`, `docs/`) — daher keine Orphan-/Dangling-Fehler für SVGs
und Manifest. Die SVGs/Manifest werden **nicht** in `registry.json` einzeln
gelistet; das Manifest selbst ist ihre Registry.

---

## 3. Manifest `icons.json`

Maschinenlesbare API für **Builder** (welche Dateien, SDF, Stretch-Zonen) *und*
**Konsumenten/Legende** (Anker, empfohlene Farbe).

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
      "stretchX": [[16, 48]],
      "stretchY": [[16, 48]],
      "content": [12, 12, 52, 52]
    }
  ]
}
```

Feld-Definitionen:

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `name` | ja | Icon-ID im Sheet (`ci-`-präfixt, siehe §4) |
| `category` | ja | `pin` \| `bubble` \| `marker` \| `symbol` |
| `file` | ja | Dateiname relativ zu `assets/map-icons/` |
| `viewBox` | ja | `[w, h]` — exakt das Raster (§5) |
| `anchor` | ja | MapLibre `icon-anchor`: `bottom` (Pins) \| `center` (Rest) |
| `sdf` | ja | immer `true` in diesem Repo |
| `recommendedColor` | ja | empfohlener CI-Token-Name für `icon-color` (ohne `var()`) |
| `stretchX` / `stretchY` | nur bubble | dehnbare Achsenbereiche `[[from, to], …]` (MapLibre-Sprite-Spec) |
| `content` | nur bubble | Text-Content-Box `[left, top, right, bottom]` für `icon-text-fit` |

Der externe Builder MUSS `stretchX`/`stretchY`/`content` (falls vorhanden) ins
generierte `sprite.json` übernehmen.

---

## 4. Namensschema

- IDs: **`ci-<kategorie>-<name>`** bzw. `ci-<name>` — fester `ci-`-Präfix, der
  diesem Repo gehört und Kollisionen im gemeinsamen Sheet ausschließt.
- Beispiele: `ci-pin`, `ci-pin-hole`, `ci-bubble-label`, `ci-marker-dot`,
  `ci-symbol-location`.
- Dateiname = `<name>.svg` (identisch zur ID).

---

## 5. Größensystem

Raster wie das bestehende `oe5ith-markers`-Sheet (pixelRatio 1; `@2x` erzeugt der
externe Builder):

| Kategorie | viewBox | Verhältnis | Anker |
|---|---|---|---|
| marker | `0 0 64 64` | 1:1 | center |
| bubble | `0 0 64 64` | 1:1 | center |
| pin | `0 0 64 80` | 4:5 | bottom |

```
Pin (64×80)            Marker/Bubble (64×64)
  ┌────┐                  ┌────┐
  │    │                  │ ●  │  anchor: center
  └─▽──┘  anchor: bottom  └────┘
```

---

## 6. SDF-Authoring-Regeln (verbindlich, in Doku)

- **Monochrom, gefüllte Flächen.** Keine reinen dünnen Striche — SDF
  degradiert dünne Linien. Strokes ggf. in Pfade umwandeln (Outline → Fill).
- **`fill="currentColor"`** im SVG. Für SDF ist die Quellfarbe egal (nur die
  Form/Alpha zählt); `currentColor` lässt zugleich die HTML-Referenz-Galerie
  per CSS umfärben.
- **Exakte `viewBox`** = Raster aus §5.
- **Safe-Area-Puffer** ≥ 4 px (im 64er-Raster) zum Rand, damit Distanzfeld und
  optionales `icon-halo` Platz haben.
- Eine Pfad-/Gruppenebene, **kein** eingebettetes Raster, **keine** Filter,
  **keine** `<text>`-Elemente.

---

## 7. Farbe / Recoloring

SDF-Icons werden zur Laufzeit über die MapLibre-Paint-Property `icon-color`
eingefärbt. Die Doku empfiehlt CI-Tokens je Semantik (Anlehnung an
`docs/map-legend.md`): z. B. `--accent` (neutral/aktiv), Status-Tokens für
warn/off. Das Manifest trägt pro Icon `recommendedColor` als Token-Name; der
Konsument löst den Token zu seinem Hex-Wert auf und setzt ihn als `icon-color`.

Konsumenten-Snippet (Doku):

```js
map.addLayer({
  id: 'stations', type: 'symbol', source: 'stations',
  layout: {
    'icon-image': 'ci-pin',
    'icon-anchor': 'bottom',
    'icon-size': 0.5
  },
  paint: { 'icon-color': '#<token-wert>' }   // SDF-Recoloring
});

// Dehnbarer Label-Hintergrund:
map.addLayer({
  id: 'street-labels', type: 'symbol', source: 'streets',
  layout: {
    'icon-image': 'ci-bubble-label',
    'icon-text-fit': 'both',
    'text-field': ['get', 'name']
  },
  paint: { 'icon-color': '#<token-wert>' }
});
```

---

## 8. Icon-Katalog

| Kategorie | Icon-ID | Zweck | Release |
|---|---|---|---|
| pin | `ci-pin` | Standard-Tropfen-Pin (Standort) | v1.17.0 |
| pin | `ci-pin-hole` | Pin mit Loch — farbiger Punkt/Symbol dahinter | v1.17.0 |
| pin | `ci-pin-fallback` | Generischer Fallback-Pin | geplant |
| bubble | `ci-bubble-label` | Dehnbarer Hintergrund für Straßen-/Ortslabels | v1.17.0 |
| bubble | `ci-bubble-tail` | dito mit Zeiger/Tail (Callout) | geplant |
| marker | `ci-marker-dot` | Gefüllter Kreis (Punktmarker, Stationen) | v1.17.0 |
| marker | `ci-marker-ring` | Kreis-Outline (Auswahl/Position) | v1.17.0 |
| marker | `ci-marker-square` | Gerundetes Quadrat | geplant |
| marker | `ci-marker-diamond` | Raute | geplant |
| symbol | `ci-symbol-location` | Fadenkreuz / aktuelle Position | v1.17.0 |
| symbol | `ci-symbol-warning` | Neutrales Warndreieck (generische Gefahr) | v1.17.0 |
| symbol | `ci-symbol-info` | Info-Kreis | geplant |
| symbol | `ci-symbol-star` | POI / Favorit | geplant |
| symbol | `ci-symbol-flag` | Start-/Zielmarker | geplant |

**Initialer Release `v1.17.0`:** `ci-pin`, `ci-pin-hole`, `ci-bubble-label`,
`ci-marker-dot`, `ci-marker-ring`, `ci-symbol-location`, `ci-symbol-warning`.
„Geplant"-Icons sind dokumentiert, aber noch nicht als SVG enthalten.

---

## 9. Referenz-Galerie

`components/map-icons.html` (mit `css/demo.css` wie andere Referenzseiten):

1. Jedes ausgelieferte SVG inline eingebettet, dargestellt im echten Raster.
2. **Recoloring-Demo:** jedes Icon in mehreren CI-Token-Farben (über CSS
   `color:` auf den `currentColor`-SVGs) — zeigt die SDF-Umfärbung visuell.
3. Pro Icon: ID, Kategorie, viewBox, Anker; bei Bubbles die Stretch-/Content-Box
   visualisiert (z. B. Overlay-Rahmen) mit kurzer Text-Fit-Erklärung.

Demo-only: Breitenbegrenzung von `demo.css` ggf. überschreiben, falls für die
Darstellung nötig.

---

## 10. Doku, Registry, Versionierung

- `assets/map-icons/*.svg` — neue SVG-Quellen (initialer Katalog, §8).
- `assets/map-icons/icons.json` — Manifest (§3).
- `docs/map-icons.md` — Komponenten-/Asset-Doku: Zweck/Abgrenzung,
  Verzeichnis, Manifest-Schema, Namensschema, Größensystem, SDF-Authoring-Regeln,
  Anker, Recoloring, **Builder-Vertrag** (scanne `assets/map-icons/*.svg`, alle
  SDF, Namen schon `ci-`-präfixt, Stretch-Zonen aus Manifest übernehmen),
  Konsumenten-Snippet. Doku-Standard sinngemäß (Element-/Katalog-Tabelle,
  Struktur, Regeln, Zustände).
- `docs/registry.json` — **ein** Eintrag, Kategorie **`asset`**, der nur
  `html: ["map-icons.html"]` und `doc: ["map-icons.md"]` beansprucht
  (kein `css`). `category != "component"` → keine Doku-Warnung, kein
  Eintrag in der README-Komponenten-Statustabelle. **Keine** Script-Änderung
  an `check_consistency.py` nötig.
- `CHANGELOG.md` — `Added`-Eintrag für `v1.17.0`.
- Keine neuen CSS-Tokens; Recoloring nutzt bestehende Tokens.
- Version: MINOR `v1.17.0`.

---

## 11. Akzeptanzkriterien

- [ ] `assets/map-icons/` enthält die 7 Initial-SVGs (§8) + `icons.json`.
- [ ] Alle SVGs: korrekte `viewBox` je Kategorie (§5), `fill="currentColor"`,
      gefüllte Flächen, Safe-Area-Puffer, keine `<text>`/Filter/Raster.
- [ ] IDs/Dateinamen folgen `ci-<…>` (§4); keine Kollision mit bestehenden Namen.
- [ ] `icons.json` validiert gegen das Schema in §3; Bubble-Einträge tragen
      `stretchX`/`stretchY`/`content`, fixe Icons nicht.
- [ ] Jeder Manifest-Eintrag verweist auf eine existierende Datei; jede
      ausgelieferte SVG hat einen Manifest-Eintrag.
- [ ] `components/map-icons.html` zeigt alle Icons inkl. Recoloring-Demo und
      Bubble-Stretch-Visualisierung; nutzt `css/demo.css` (nicht produktiv).
- [ ] `docs/map-icons.md` vollständig (inkl. Builder-Vertrag + Konsumenten-Snippet);
      ein Agent könnte ein Icon ergänzen, ohne die HTML zu öffnen.
- [ ] `docs/registry.json`: `asset`-Eintrag (nur html+doc); `CHANGELOG.md`
      `v1.17.0`-`Added`.
- [ ] `python3 scripts/cli/check_consistency.py` endet mit „✔ … konsistent",
      keine neue Warnung/kein neuer Fehler durch diesen Eintrag.
- [ ] Keine neuen Tokens; keine Build-Logik in diesem Repo.

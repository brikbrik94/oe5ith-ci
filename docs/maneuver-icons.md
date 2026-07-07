# Maneuver-Icons (Turn-by-Turn Richtungssymbole)

**Assets:** `assets/maneuver-icons/`
**Referenz:** `components/maneuver-icons.html`
**Status:** definiert · v1.20.0

---

## Zweck & Abgrenzung

`assets/maneuver-icons/` ist die **Source of Truth für Turn-by-Turn-Richtungssymbole**,
1:1 zu den Manöver-Codes von **OpenRouteService (ORS)**. FontAwesome Free deckt
Navigations-Pfeile (Slight/Sharp-Varianten, Kreisverkehr, Gabelung-Halten) nicht
ausreichend ab — dieses Set schließt die Lücke mit eigenen, monochromen SVGs.

**Bewusst nicht hier:**
- **Kein SDF/MapLibre-Bezug.** Diese Icons sind reine UI-Icons für die
  Sidebar-Liste (inline `<svg>`, `stroke="currentColor"`), keine Karten-Marker.
  Für Karten-Symbole gilt `assets/map-icons/` (`docs/map-icons.md`).
- **Keine Rotation/Spiegelung zur Laufzeit.** Jeder Manöver-Typ ist eine
  eigenständige SVG-Datei.
- **Kein Exit-Nummern-Rendering für Kreisverkehr.** Die Icons zeigen nur
  „rein"/„raus", keine Zahlen-Overlays — Exit-Nummern liefert ORS als Text.

---

## Verzeichnis

```
assets/maneuver-icons/
├── ci-maneuver-turn-left.svg
├── ci-maneuver-turn-right.svg
├── ci-maneuver-sharp-left.svg
├── ci-maneuver-sharp-right.svg
├── ci-maneuver-slight-left.svg
├── ci-maneuver-slight-right.svg
├── ci-maneuver-straight.svg
├── ci-maneuver-roundabout-enter.svg
├── ci-maneuver-roundabout-exit.svg
├── ci-maneuver-uturn.svg
├── ci-maneuver-goal.svg
├── ci-maneuver-depart.svg
├── ci-maneuver-keep-left.svg
├── ci-maneuver-keep-right.svg
└── icons.json                   ← Manifest = ORS-Code-Mapping
```

Das Verzeichnis wird vom Konsistenz-Check **nicht** erfasst (er prüft nur
`css/`, `components/`, `docs/`) — keine Orphan-/Dangling-Fehler für SVGs und
Manifest. Die SVGs werden **nicht** einzeln in `registry.json` gelistet;
`icons.json` ist ihre Registry.

---

## ORS-Code-Katalog

| Code | ORS-Manöver | Icon-ID | Form |
|---|---|---|---|
| 0 | Left | `ci-maneuver-turn-left` | 90°-Pfeil nach links |
| 1 | Right | `ci-maneuver-turn-right` | 90°-Pfeil nach rechts |
| 2 | Sharp left | `ci-maneuver-sharp-left` | ~135°-Pfeil nach links |
| 3 | Sharp right | `ci-maneuver-sharp-right` | ~135°-Pfeil nach rechts |
| 4 | Slight left | `ci-maneuver-slight-left` | ~30–45°-Pfeil nach links |
| 5 | Slight right | `ci-maneuver-slight-right` | ~30–45°-Pfeil nach rechts |
| 6 | Straight | `ci-maneuver-straight` | gerader Pfeil nach oben |
| 7 | Enter roundabout | `ci-maneuver-roundabout-enter` | Kreis, Pfeil von außen hinein |
| 8 | Exit roundabout | `ci-maneuver-roundabout-exit` | Kreis, Pfeil von innen hinaus |
| 9 | U-turn | `ci-maneuver-uturn` | 180°-Haarnadel-Pfeil |
| 10 | Goal | `ci-maneuver-goal` | Ziel-Symbol (Flagge) |
| 11 | Depart | `ci-maneuver-depart` | Start-Symbol (Punkt) |
| 12 | Keep left | `ci-maneuver-keep-left` | Y-Gabelung, linker Ast betont |
| 13 | Keep right | `ci-maneuver-keep-right` | Y-Gabelung, rechter Ast betont |

**Slight vs. Keep:** „Slight" (4/5) ist eine leichte Abbiegung auf eine neue
Straße. „Keep" (12/13) ist eine Gabelung, bei der man auf der aktuellen Spur
bleibt — visuell bewusst unterschiedliche Formen (gebogener Pfeil vs.
Y-Gabelung mit betontem Ast).

---

## Namensschema

- **Icon-ID:** `ci-maneuver-<name>` — fester Präfix, Kollisionsschutz.
- **Dateiname:** identisch zur ID, also `<id>.svg`.
- Neue Icons: immer `ci-maneuver-`-Präfix, keine Unterverzeichnisse.

---

## Stil-Regeln (verbindlich)

Line-Art-Stil, identisch zu bestehenden Custom-Icons in
`topbar.html`/`modal.html` (nicht der SDF-Stil aus `map-icons`):

- **`viewBox="0 0 16 16"`** — festes Raster für alle 14 Icons.
- **`fill="none"`, `stroke="currentColor"`, `stroke-width="1.5"`,
  `stroke-linecap="round"`, `stroke-linejoin="round"`**.
- Ausnahmen mit `fill="currentColor"` nur wo zur Lesbarkeit nötig
  (`ci-maneuver-goal`: Flaggenfläche; `ci-maneuver-depart`: Mittelpunkt).
- Kein eingebettetes Raster, keine `<filter>`, keine `<text>`.
- Jede Datei ist eigenständig — keine Rotation/Spiegelung zur Laufzeit.

---

## Manifest-Schema (`icons.json`)

```json
{
  "version": 1,
  "grid": [16, 16],
  "icons": [
    { "orsCode": 0, "name": "ci-maneuver-turn-left", "file": "ci-maneuver-turn-left.svg", "label": "Left" }
  ]
}
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `orsCode` | ja | Numerischer ORS-Manöver-Code (0–13) — Kopplungsschlüssel |
| `name` | ja | Icon-ID, `ci-maneuver-`-präfixt |
| `file` | ja | Dateiname relativ zu `assets/maneuver-icons/` |
| `label` | ja | Kurzbezeichnung (Englisch, wie ORS-Doku) für Tooltip/Alt-Text |

---

## Einbindung (Konsumenten-Snippet)

```js
const manifest = await fetch('/assets/maneuver-icons/icons.json').then(r => r.json());
const byCode = Object.fromEntries(manifest.icons.map(i => [i.orsCode, i]));

async function iconMarkupFor(orsCode) {
  const icon = byCode[orsCode];
  const svgText = await fetch(`/assets/maneuver-icons/${icon.file}`).then(r => r.text());
  return svgText; // inline einsetzen, NICHT <img src> (sonst kein currentColor-Erben)
}
```

In der Disclosure-Liste (`disclosure.css`):

```html
<div class="disclosure-item">
  <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none"
       stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <!-- ci-maneuver-turn-right Pfad -->
  </svg>
  <span class="disclosure-item-text">Turn right onto Welser Straße</span>
  <span class="disclosure-item-meta mono">1.2 km</span>
</div>
```

`.disclosure-item-icon` setzt `color: var(--text)` — gleiche Gewichtung wie
`.disclosure-item-text`, da das Richtungssymbol navigatorisch relevant ist.

---

## Regeln

1. **Neues Icon:** SVG nach den Stil-Regeln erstellen → in
   `assets/maneuver-icons/` ablegen → Eintrag in `icons.json` ergänzen →
   Galerie `components/maneuver-icons.html` um eine Karte erweitern.
2. **Kein produktiver CSS-Code** außer `.disclosure-item-icon` in
   `disclosure.css` — keine neuen Tokens.
3. **Konsistenz-Check** erfasst `assets/maneuver-icons/` nicht — Änderungen am
   Verzeichnis lösen keinen Check-Fehler aus. Der Check prüft aber
   `docs/maneuver-icons.md` als registrierte Dokumentation.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-07-07 | Initiale Definition. 14 Icons (`v1.20.0`), Manifest mit ORS-Code-Mapping, `.disclosure-item-icon`-Slot. |

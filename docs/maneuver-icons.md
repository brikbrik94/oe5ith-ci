# Maneuver-Icons (Turn-by-Turn Richtungssymbole)

**Assets:** `assets/maneuver-icons/`
**Referenz:** `components/maneuver-icons.html`
**Status:** definiert · v2.0.0

---

## Zweck & Abgrenzung

`assets/maneuver-icons/` ist die **Source of Truth für Turn-by-Turn-Richtungssymbole**.
14 Icons sind 1:1 zu den Manöver-Codes von **OpenRouteService (ORS)** gekoppelt
(`orsCode`); seit `v1.26.0` kommen 16 weitere Icons für **Valhalla**-Konzepte hinzu, die
keine ORS-Entsprechung haben (`valhallaType`, siehe „Valhalla-Only-Konzepte" unten).
FontAwesome Free deckt Navigations-Pfeile (Slight/Sharp-Varianten, Kreisverkehr,
Gabelung-Halten, Ramp/Exit, gerichtete Depart/Goal/U-Turn) nicht ausreichend ab — dieses
Set schließt die Lücke mit eigenen, monochromen SVGs.

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
├── ci-maneuver-uturn-left.svg
├── ci-maneuver-uturn-right.svg
├── ci-maneuver-ramp-right.svg
├── ci-maneuver-ramp-left.svg
├── ci-maneuver-ramp-straight.svg
├── ci-maneuver-exit-right.svg
├── ci-maneuver-exit-left.svg
├── ci-maneuver-stay-straight.svg
├── ci-maneuver-merge.svg
├── ci-maneuver-ferry-enter.svg
├── ci-maneuver-ferry-exit.svg
├── ci-maneuver-depart-right.svg
├── ci-maneuver-depart-left.svg
├── ci-maneuver-goal-right.svg
├── ci-maneuver-goal-left.svg
├── ci-maneuver-becomes.svg
└── icons.json                   ← Manifest = ORS-/Valhalla-Kopplung
```

Das Verzeichnis wird vom Konsistenz-Check **nicht** erfasst (er prüft nur
`css/`, `components/`, `docs/`) — keine Orphan-/Dangling-Fehler für SVGs und
Manifest. Die SVGs werden **nicht** einzeln in `registry.json` gelistet;
`icons.json` ist ihre Registry.

---

## ORS-Code-Katalog (14 Icons)

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

## Valhalla-Only-Konzepte (16 Icons)

Diese 16 Icons haben **keinen** ORS-Code — sie decken Valhalla-Manöver-Typen ab, für die
der 14er-ORS-Katalog kein Äquivalent hat. Kopplung über `valhallaType` (symbolischer
Valhalla-Manöver-Typname, nicht der numerische Ordinal-Wert — siehe Manifest-Schema unten).

| Icon-ID | Valhalla-Typ | Form |
|---|---|---|
| `ci-maneuver-uturn-left` | `kUturnLeft` | 180°-Haarnadel-Pfeil, gerichtet nach links |
| `ci-maneuver-uturn-right` | `kUturnRight` | 180°-Haarnadel-Pfeil, gerichtet nach rechts |
| `ci-maneuver-ramp-right` | `kRampRight` | Pfeil rechts abzweigend, gedimmte Gerade im Hintergrund (Auffahrt) |
| `ci-maneuver-ramp-left` | `kRampLeft` | Pfeil links abzweigend, gedimmte Gerade im Hintergrund (Auffahrt) |
| `ci-maneuver-ramp-straight` | `kRampStraight` | Gerader Pfeil, gedimmter Seitenast (Auffahrt geradeaus) |
| `ci-maneuver-exit-right` | `kExitRight` | Pfeil rechts abzweigend, gedimmte Gerade im Hintergrund (Ausfahrt) |
| `ci-maneuver-exit-left` | `kExitLeft` | Pfeil links abzweigend, gedimmte Gerade im Hintergrund (Ausfahrt) |
| `ci-maneuver-stay-straight` | `kStayStraight` | Gerader Pfeil, zwei gedimmte Gabelungsäste im Hintergrund |
| `ci-maneuver-merge` | `kMerge` | Zwei Linien laufen zu einem Pfeil zusammen |
| `ci-maneuver-ferry-enter` | `kFerryEnter` | Pfeil nach unten auf gedimmte Wasserlinie |
| `ci-maneuver-ferry-exit` | `kFerryExit` | Pfeil nach oben von gedimmter Wasserlinie |
| `ci-maneuver-depart-right` | `kStartRight` | Start-Symbol (Punkt), Pfeil nach rechts versetzt |
| `ci-maneuver-depart-left` | `kStartLeft` | Start-Symbol (Punkt), Pfeil nach links versetzt |
| `ci-maneuver-goal-right` | `kDestinationRight` | Ziel-Symbol (Flagge) rechts versetzt |
| `ci-maneuver-goal-left` | `kDestinationLeft` | Ziel-Symbol (Flagge) links versetzt |
| `ci-maneuver-becomes` | `kBecomes` | Gerader Pfeil, gedimmte Querlinie (Straßenwechsel ohne Richtungsänderung) |

**Abgrenzung Stay-straight vs. Slight/Keep:** „Stay straight" ist eine Gabelung, bei der
man geradeaus bleibt — der ORS-Katalog kennt nur Keep-left/-right (Gabelung mit
Seitenpräferenz), keine Geradeaus-Variante. Eigenständiges Icon statt Wiederverwendung von
`ci-maneuver-straight`, da der Gabelungskontext (zwei sich trennende, gedimmte Äste im
Hintergrund) visuell mitgeliefert werden muss.

**Bewusst nicht abgedeckt:** die 7 Valhalla-Transit-Manöver-Typen (kein OE5ITH-Konsument
kann sie mangels GTFS-Daten aktuell liefern).

---

## Namensschema

- **Icon-ID:** `ci-maneuver-<name>` — fester Präfix, Kollisionsschutz.
- **Dateiname:** identisch zur ID, also `<id>.svg`.
- Neue Icons: immer `ci-maneuver-`-Präfix, keine Unterverzeichnisse.

---

## Stil-Regeln (verbindlich)

Line-Art-Stil, identisch zu bestehenden Custom-Icons in
`topbar.html`/`modal.html` (nicht der SDF-Stil aus `map-icons`):

- **`viewBox="0 0 16 24"`** — festes, hochformatiges Raster für alle 30 Icons (seit
  `v2.0.0`; zuvor `0 0 16 16`). Gerichtete Pfeile nutzen die zusätzliche Höhe für einen
  längeren Pfeilschaft/-bogen; rotationssymmetrische/flächige Icons (Kreisverkehr, Goal,
  Depart) behalten ihre native Proportion und sind im neuen Raster vertikal zentriert statt
  gestreckt.
- **`fill="none"`, `stroke="currentColor"`, `stroke-width="1.5"`,
  `stroke-linecap="round"`, `stroke-linejoin="round"`**.
- Ausnahmen mit `fill="currentColor"` nur wo zur Lesbarkeit nötig
  (`ci-maneuver-goal`/`-goal-right`/`-goal-left`: Flaggenfläche;
  `ci-maneuver-depart`/`-depart-right`/`-depart-left`: Mittelpunkt).
- **Kontext-Pfad-Konvention** (seit v1.26.0): Icons, die einen ungenommenen
  Straßen-/Gabelungsast oder eine Wasserlinie im Hintergrund zeigen müssen
  (`ramp-*`, `exit-*`, `stay-straight`, `becomes`, `ferry-enter`, `ferry-exit`), dimmen
  diesen Kontext-Pfad statt ihn wegzulassen: gestrichelt via `stroke-dasharray`
  (Icon-abhängig, z. B. `1.5 1.5` oder `1 1.5`) mit `opacity` 0.4–0.5 für fortlaufenden
  Straßenverlauf (Ramp/Exit/Becomes), reines `opacity` (Icon-abhängiger Wert zwischen
  0.35 und 0.6, kein Dasharray) für durchgezogene, aber nachrangige Linien (Gabelungsäste
  bei Stay-straight — bereits seit `v1.20.0` bei Keep-left/-right in gleicher Weise
  verwendet —, Wasserlinie bei den Fähre-Icons). Der eigentliche Manöver-Pfad bleibt immer
  durchgezogen und voll deckend — die Konvention ist ein Zusatz, keine Ersetzung der
  übrigen Stil-Regeln; die genauen Dasharray-/Opacity-Werte sind pro Icon zu wählen, keine
  einzelne feste Zahl ist über alle Icons hinweg bindend.
- Kein eingebettetes Raster, keine `<filter>`, keine `<text>`.
- Jede Datei ist eigenständig — keine Rotation/Spiegelung zur Laufzeit.

---

## Manifest-Schema (`icons.json`)

```json
{
  "version": 1,
  "grid": [16, 24],
  "icons": [
    { "orsCode": 0, "name": "ci-maneuver-turn-left", "file": "ci-maneuver-turn-left.svg", "label": "Left" },
    { "name": "ci-maneuver-ramp-right", "valhallaType": "kRampRight", "file": "ci-maneuver-ramp-right.svg", "label": "Ramp right" }
  ]
}
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `name` | ja | Icon-ID, `ci-maneuver-`-präfixt. Einziger providerneutraler Schlüssel — kein separates `id`-Feld. |
| `orsCode` | optional | Numerischer ORS-Manöver-Code (0–13) — Kopplungsschlüssel. Nur vorhanden, wenn das Icon ORS-gekoppelt ist. |
| `valhallaType` | optional | Symbolischer Valhalla-Manöver-Typ (String, z. B. `"kRampRight"`) — **nicht** der numerische Ordinal-Wert, da nur die Namen über Valhalla-Versionen hinweg stabil dokumentiert sind. Nur vorhanden, wenn das Icon ein Valhalla-Only-Konzept ist. |
| `file` | ja | Dateiname relativ zu `assets/maneuver-icons/` |
| `label` | ja | Kurzbezeichnung (Englisch, wie ORS-/Valhalla-Doku) für Tooltip/Alt-Text |

**Feld-Absenz:** Nicht zutreffende Felder werden **weggelassen**, nicht auf `null`
gesetzt — die 14 ORS-Icons haben kein `valhallaType`-Feld, die 16 Valhalla-Only-Icons
haben kein `orsCode`-Feld.

**Verantwortungsteilung:** `icons.json` liefert nur die Kopplungsdaten. Das tatsächliche
Lookup/Mapping von einem Provider-Manöver-Code auf einen Icon-Eintrag bleibt Aufgabe der
konsumierenden App — identisch zum bestehenden `byCode`-Muster im Konsumenten-Snippet unten.

---

## Einbindung (Konsumenten-Snippet)

```js
const manifest = await fetch('/assets/maneuver-icons/icons.json').then(r => r.json());
const byCode = Object.fromEntries(
  manifest.icons.filter(i => i.orsCode !== undefined).map(i => [i.orsCode, i])
);

async function iconMarkupFor(orsCode) {
  const icon = byCode[orsCode];
  const svgText = await fetch(`/assets/maneuver-icons/${icon.file}`).then(r => r.text());
  return svgText; // inline einsetzen, NICHT <img src> (sonst kein currentColor-Erben)
}
```

Der Filter ist notwendig: 16 Einträge haben kein `orsCode`-Feld, `i.orsCode` wäre dort
`undefined` und würde ohne Filter alle unter dem Schlüssel `"undefined"` kollabieren
(Last-Write-Wins). `!== undefined` statt eines Truthy-Checks, weil `orsCode: 0` (Left)
sonst fälschlich herausgefiltert würde.

Für Valhalla-Konsumenten identisch, nur nach `valhallaType` statt `orsCode` indiziert:

```js
const byValhallaType = Object.fromEntries(
  manifest.icons.filter(i => i.valhallaType !== undefined).map(i => [i.valhallaType, i])
);
```

## Turn-by-Turn-Liste (`.maneuver-item`)

Eigene Zeilen-Definition für Turn-by-Turn-Listen — ersetzt `.disclosure-item` nur für
diesen Spezialfall. Die generische `.disclosure`-Hülle (Header, Collapse, `<details>`/
`<summary>`) wird unverändert weiterverwendet, siehe `docs/sidebar.md` Abschnitt
„Disclosure (Single-Panel)".

### Struktur

```
.disclosure-body
└── .maneuver-item              (mehrfach, ersetzt .disclosure-item)
    ├── .maneuver-item-icon     (Pflicht — inline <svg>, 16×24)
    ├── .maneuver-item-text     (Pflicht — Anweisungstext)
    └── .maneuver-item-meta     (Optional — Distanz, mono)
```

### Elemente

| Element / Klasse | Zweck | Pflicht/Optional | Modifier |
|---|---|---|---|
| `.maneuver-item` | Zeilen-Wrapper: Flex-Row, Trennlinie unten (`--border`) | Pflicht | keine |
| `.maneuver-item-icon` | Icon-Slot, 16×24px, `color: var(--text)` | Pflicht | keine |
| `.maneuver-item-text` | Anweisungstext, `flex:1`, `--text` | Pflicht | keine |
| `.maneuver-item-meta` | Distanz/Meta rechts, `--muted`, meist `.mono` | Optional | keine |

### Reihenfolge

Icon → Text → Meta, in dieser Reihenfolge als direkte Kinder von `.maneuver-item`. Kein
Meta-Element, wenn keine Distanzangabe vorhanden ist (kein leerer Platzhalter).

### Zustände/Varianten

| Zustand | Klasse | Wann verwenden |
|---|---|---|
| Standard | `.maneuver-item` | Jede Zeile — kein Auswahlzustand, keine Varianten |
| Letzte Zeile | `.maneuver-item:last-child` | Automatisch (kein manuelles Setzen) — entfernt die untere Trennlinie |

### Einbindung (Konsumenten-Snippet)

Manifest-Lookup (`byCode`/`byValhallaType`) siehe oben, Abschnitt „Einbindung
(Konsumenten-Snippet)".

Markup:

```html
<div class="maneuver-item">
  <svg class="maneuver-item-icon" viewBox="0 0 16 24" fill="none"
       stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <!-- ci-maneuver-turn-right Pfad -->
  </svg>
  <span class="maneuver-item-text">Turn right onto Welser Straße</span>
  <span class="maneuver-item-meta mono">1.2 km</span>
</div>
```

---

## Regeln

1. **Neues Icon:** SVG nach den Stil-Regeln erstellen → in
   `assets/maneuver-icons/` ablegen → Eintrag in `icons.json` ergänzen (genau eines von
   `orsCode`/`valhallaType` setzen, nie beide, nie keins) →
   Galerie `components/maneuver-icons.html` um eine Karte erweitern.
2. **Kein produktiver CSS-Code** außer `.disclosure-item-icon`/`.maneuver-item-icon` in
   `disclosure.css` — keine neuen Tokens.
3. **Konsistenz-Check** erfasst `assets/maneuver-icons/` nicht — Änderungen am
   Verzeichnis lösen keinen Check-Fehler aus. Der Check prüft aber
   `docs/maneuver-icons.md` als registrierte Dokumentation.
4. **Turn-by-Turn-Listen** verwenden `.maneuver-item` (siehe oben), nicht das generische
   `.disclosure-item` — eigene Zeilen-Definition für diesen Spezialfall, siehe
   `docs/sidebar.md`.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-07-07 | Initiale Definition. 14 Icons (`v1.20.0`), Manifest mit ORS-Code-Mapping, `.disclosure-item-icon`-Slot. |
| 2026-08-22 | +16 Icons (`v1.26.0`) für Valhalla-Only-Konzepte (Ramp/Exit/Merge/Ferry/gerichtete Uturn+Depart+Goal/Becomes). Schema: `orsCode` optional, neues optionales Feld `valhallaType`. Kontext-Pfad-Stilkonvention (`stroke-dasharray`/`opacity`) eingeführt. |
| 2026-08-23 | **v2.0.0 (Breaking).** Alle 30 Icons auf `viewBox="0 0 16 24"` umgezeichnet (war `0 0 16 16`). Neue Komponente `.maneuver-item` (`disclosure.css`) ersetzt `.disclosure-item` für Turn-by-Turn-Listen. `icons.json`: `"grid"` von `[16,16]` auf `[16,24]`. Migration: `docs/migration-v2.md`. |

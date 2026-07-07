# Maneuver-Icons (Turn-by-Turn Richtungssymbole) — Design / Spec

**Datum:** 2026-07-07
**Status:** Freigegeben · zur Umsetzung
**Angefragt von:** OE5ITH-Routing-Sidebar — Icons für die Turn-by-Turn-Wegbeschreibung
  (`.disclosure`-Liste, siehe `docs/sidebar.md`, Beispiel „Wegbeschreibung“)
**Version:** additiv → MINOR `v1.20.0`

---

## 1. Zweck & Abgrenzung

Am 2026-07-06 wurde die Disclosure-Komponente (`css/disclosure.css`) u. a. für
Turn-by-Turn-Wegbeschreibungen eingeführt (`.disclosure-item` mit Text + Meta).
Ein Icon-Slot für das Abbiege-/Richtungssymbol pro Schritt fehlte bisher.

FontAwesome Free deckt Navigations-Pfeile (leicht/scharf abbiegen, Kreisverkehr
rein/raus, Gabelung halten) nicht ausreichend ab. Dieses Repo wird daher
**Source of Truth für einen eigenen, kleinen Line-Art-Icon-Satz**, der 1:1 den
Manöver-Codes von **OpenRouteService (ORS)** entspricht.

**Bewusst nicht hier:**
- **Kein SDF/MapLibre-Bezug.** Diese Icons sind reine UI-Icons für die
  Sidebar-Liste (inline `<svg>`, `stroke="currentColor"`), keine Karten-Marker.
  Für Karten-Symbole gilt weiterhin `assets/map-icons/` (`docs/map-icons.md`).
- **Keine Rotation/Spiegelung zur Laufzeit.** Jeder Manöver-Typ ist eine
  eigenständige SVG-Datei — kein CSS-`transform`-Trick, damit auch
  Nicht-CSS-Konsumenten (z. B. native Wrapper) die Dateien direkt verwenden
  können.
- **Kein Exit-Nummern-Rendering für Kreisverkehr.** ORS liefert Exit-Zahlen
  separat als Text; die Icons zeigen nur „rein“/„raus“, keine Zahlen-Overlays.

---

## 2. Verzeichnis & Schnittstelle

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

Analog zu `assets/map-icons/`: Der Konsistenz-Check erfasst
`assets/maneuver-icons/` **nicht** (prüft nur `css/`, `components/`, `docs/`) —
keine Orphan-/Dangling-Fehler für SVGs und Manifest. Die SVGs/Manifest werden
**nicht** einzeln in `registry.json` gelistet; das Manifest ist ihre Registry.

---

## 3. Manifest `icons.json`

```json
{
  "version": 1,
  "grid": [16, 16],
  "icons": [
    { "orsCode": 0,  "name": "ci-maneuver-turn-left",        "file": "ci-maneuver-turn-left.svg",        "label": "Left" },
    { "orsCode": 1,  "name": "ci-maneuver-turn-right",       "file": "ci-maneuver-turn-right.svg",       "label": "Right" },
    { "orsCode": 2,  "name": "ci-maneuver-sharp-left",       "file": "ci-maneuver-sharp-left.svg",       "label": "Sharp left" },
    { "orsCode": 3,  "name": "ci-maneuver-sharp-right",      "file": "ci-maneuver-sharp-right.svg",      "label": "Sharp right" },
    { "orsCode": 4,  "name": "ci-maneuver-slight-left",      "file": "ci-maneuver-slight-left.svg",      "label": "Slight left" },
    { "orsCode": 5,  "name": "ci-maneuver-slight-right",     "file": "ci-maneuver-slight-right.svg",     "label": "Slight right" },
    { "orsCode": 6,  "name": "ci-maneuver-straight",         "file": "ci-maneuver-straight.svg",         "label": "Straight" },
    { "orsCode": 7,  "name": "ci-maneuver-roundabout-enter", "file": "ci-maneuver-roundabout-enter.svg", "label": "Enter roundabout" },
    { "orsCode": 8,  "name": "ci-maneuver-roundabout-exit",  "file": "ci-maneuver-roundabout-exit.svg",  "label": "Exit roundabout" },
    { "orsCode": 9,  "name": "ci-maneuver-uturn",            "file": "ci-maneuver-uturn.svg",            "label": "U-turn" },
    { "orsCode": 10, "name": "ci-maneuver-goal",             "file": "ci-maneuver-goal.svg",             "label": "Goal" },
    { "orsCode": 11, "name": "ci-maneuver-depart",           "file": "ci-maneuver-depart.svg",           "label": "Depart" },
    { "orsCode": 12, "name": "ci-maneuver-keep-left",        "file": "ci-maneuver-keep-left.svg",        "label": "Keep left" },
    { "orsCode": 13, "name": "ci-maneuver-keep-right",       "file": "ci-maneuver-keep-right.svg",       "label": "Keep right" }
  ]
}
```

Feld-Definitionen:

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `orsCode` | ja | Numerischer ORS-Manöver-Code (0–13, siehe §4) — Kopplungsschlüssel |
| `name` | ja | Icon-ID, `ci-maneuver-`-präfixt |
| `file` | ja | Dateiname relativ zu `assets/maneuver-icons/` |
| `label` | ja | Kurzbezeichnung (Englisch, wie ORS-Doku) für Tooltip/Alt-Text |

---

## 4. ORS-Code-Katalog

| Code | ORS-Manöver | Icon-ID | Form |
|---|---|---|---|
| 0 | Left | `ci-maneuver-turn-left` | 90°-Pfeil nach links |
| 1 | Right | `ci-maneuver-turn-right` | 90°-Pfeil nach rechts |
| 2 | Sharp left | `ci-maneuver-sharp-left` | ~135°-Pfeil nach links |
| 3 | Sharp right | `ci-maneuver-sharp-right` | ~135°-Pfeil nach rechts |
| 4 | Slight left | `ci-maneuver-slight-left` | ~30–45°-Pfeil nach links (sanfte Biegung) |
| 5 | Slight right | `ci-maneuver-slight-right` | ~30–45°-Pfeil nach rechts (sanfte Biegung) |
| 6 | Straight | `ci-maneuver-straight` | gerader Pfeil nach oben |
| 7 | Enter roundabout | `ci-maneuver-roundabout-enter` | Kreis mit Pfeil, der von außen hineinzeigt |
| 8 | Exit roundabout | `ci-maneuver-roundabout-exit` | Kreis mit Pfeil, der von innen nach außen zeigt |
| 9 | U-turn | `ci-maneuver-uturn` | 180°-Haarnadel-Pfeil |
| 10 | Goal | `ci-maneuver-goal` | Ziel-Symbol (Flagge) |
| 11 | Depart | `ci-maneuver-depart` | Start-Symbol (gefüllter Punkt) |
| 12 | Keep left | `ci-maneuver-keep-left` | Y-Gabelung, linker Ast betont |
| 13 | Keep right | `ci-maneuver-keep-right` | Y-Gabelung, rechter Ast betont |

**Slight vs. Keep — bewusst unterschiedliche Formen:** „Slight" (4/5) ist eine
leichte Abbiegung auf eine neue Straße (gebogener Pfeil, kleiner Winkel).
„Keep" (12/13) ist eine Gabelung, bei der man auf der aktuellen Spur bleibt
(Y-Form mit einem betonten Ast). Visuell verwechselbare, aber semantisch
unterschiedliche Manöver bekommen unterschiedliche Icon-Formen.

---

## 5. Größensystem & Stil (verbindlich)

Line-Art-Stil, identisch zu bestehenden Custom-Icons in `topbar.html`/`modal.html`
(nicht der SDF-Stil aus `map-icons`):

- **`viewBox="0 0 16 16"`** — festes Raster für alle 14 Icons.
- **`fill="none"`**, **`stroke="currentColor"`**, **`stroke-width="1.5"`**,
  **`stroke-linecap="round"`**.
- Keine gefüllten Flächen außer wo zur Lesbarkeit nötig (z. B. `ci-maneuver-depart`
  als gefüllter Punkt, `ci-maneuver-goal` als gefüllte Flagge) — dann ebenfalls
  `fill="currentColor"`.
- Kein eingebettetes Raster, keine Filter, keine `<text>`-Elemente.
- Jede Datei ist eigenständig (siehe §1 — keine Rotation/Spiegelung zur Laufzeit).

---

## 6. Integration in Disclosure (`disclosure.css`)

Neuer optionaler Icon-Slot als erstes Kind in `.disclosure-item`:

```css
.disclosure-item-icon {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  color: var(--text);
}
```

Verwendung (Beispiel):

```html
<div class="disclosure-item">
  <svg class="disclosure-item-icon" viewBox="0 0 16 16" fill="none"
       stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
    <!-- ci-maneuver-turn-right Pfad -->
  </svg>
  <span class="disclosure-item-text">Turn right onto Welser Straße</span>
  <span class="disclosure-item-meta mono">1.2 km</span>
</div>
```

`color: var(--text)` — gleiche visuelle Gewichtung wie `.disclosure-item-text`,
da das Richtungssymbol navigatorisch relevant ist, nicht rein dekorativ (im
Unterschied zu `.disclosure-item-meta`, das bewusst `var(--muted)` bleibt).

Kein neuer Token nötig — reuse `--text`.

---

## 7. Referenz-Galerie

`components/maneuver-icons.html` (mit `css/demo.css`, wie andere Referenzseiten):

1. Alle 14 Icons inline eingebettet, im 16×16-Raster, mit ORS-Code + Label
   beschriftet.
2. Ein Disclosure-Beispiel („Wegbeschreibung" analog zu `disclosure.html`),
   aber mit `.disclosure-item-icon` pro Zeile befüllt, um die reale Kombination
   Icon + Text + Meta zu zeigen.

---

## 8. Doku, Registry, Versionierung

- `assets/maneuver-icons/*.svg` — 14 SVG-Quellen (§4).
- `assets/maneuver-icons/icons.json` — Manifest (§3).
- `docs/maneuver-icons.md` — Katalogtabelle mit ORS-Code (§4), Stil-Regeln (§5),
  Einbindungs-Snippet (§6), Verweis auf Abgrenzung zu `map-icons` (§1).
- `css/disclosure.css` — neue `.disclosure-item-icon`-Regel (§6).
- `components/maneuver-icons.html` — Referenz-Galerie (§7).
- `components/disclosure.html` — bestehendes Wegbeschreibungs-Beispiel um Icons
  ergänzen.
- `docs/registry.json` — ein neuer Eintrag, Kategorie **`asset`** (wie
  `map-icons`), `doc: ["maneuver-icons.md"]`, `html: ["maneuver-icons.html"]`,
  `note` auf die Erweiterung von `disclosure.css`/`disclosure.html`. Der
  bestehende `sidebar`-Eintrag (`css: ["sidebar.css", "disclosure.css"]`)
  bleibt unverändert (disclosure.css wird nur erweitert, nicht neu erstellt).
- `docs/sidebar.md` — Hinweis im Turn-by-Turn-Beispielsatz auf die neuen Icons
  ergänzen.
- `CHANGELOG.md` — `Added`-Eintrag für `v1.20.0`.
- Keine neuen CSS-Tokens; `.disclosure-item-icon` nutzt `--text`.
- Version: MINOR `v1.20.0`.

---

## 9. Akzeptanzkriterien

- [ ] `assets/maneuver-icons/` enthält alle 14 SVGs (§4) + `icons.json`.
- [ ] Alle SVGs: `viewBox="0 0 16 16"`, `stroke="currentColor"`,
      `stroke-width="1.5"`, `stroke-linecap="round"`, `fill="none"` (außer
      begründete Ausnahmen laut §5), keine `<text>`/Filter/Raster.
- [ ] IDs/Dateinamen folgen `ci-maneuver-<…>` (§4); jeder ORS-Code 0–13 hat
      genau einen Manifest-Eintrag.
- [ ] `icons.json` validiert gegen Schema §3; jeder Eintrag verweist auf eine
      existierende Datei; jede SVG hat einen Manifest-Eintrag.
- [ ] `.disclosure-item-icon` in `disclosure.css` ergänzt (§6), kein neuer
      Token, `color: var(--text)`.
- [ ] `components/maneuver-icons.html` zeigt alle 14 Icons mit ORS-Code/Label
      sowie ein Disclosure-Beispiel mit befüllten Icons; nutzt `css/demo.css`.
- [ ] `components/disclosure.html` — Wegbeschreibungs-Beispiel nutzt die neuen
      Icons.
- [ ] `docs/maneuver-icons.md` vollständig (Katalog, Stil-Regeln, Snippet,
      Abgrenzung zu map-icons).
- [ ] `docs/registry.json`: neuer `asset`-Eintrag; `CHANGELOG.md` `v1.20.0`
      `Added`.
- [ ] `python3 scripts/cli/check_consistency.py` endet mit „✔ … konsistent",
      keine neue Warnung/kein neuer Fehler.
- [ ] Keine neuen Tokens; keine SDF-/MapLibre-Logik in diesem Set.

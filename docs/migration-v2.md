# Migration v1 → v2

## Turn-by-Turn-Icons: `viewBox` 16×16 → 16×24

Alle 30 Icons in `assets/maneuver-icons/` haben ein neues, hochformatiges
`viewBox="0 0 16 24"` (vorher `0 0 16 16`) — gleiche Dateinamen/IDs, gleiches
`icons.json`-Schema, nur andere Bildproportionen.

### Wer ist betroffen?

Jeder Konsument, der die SVGs in einem **fest quadratischen** Container rendert (z.B. die
bisherige `.disclosure-item-icon { width:16px; height:16px }`). Das Icon wird dort per
`preserveAspectRatio`-Default (`xMidYMid meet`) klein und zentriert mit Leerraum
dargestellt statt im vorgesehenen Hochformat.

### Was tun?

1. `assets/maneuver-icons/icons.json` neu laden — `"grid"` ist jetzt `[16, 24]`.
2. Den Container, der die Icons rendert, von 16×16 auf 16×24 (oder ein proportionales
   Vielfaches, z.B. 20×30) umstellen. In `oe5ith-ci` selbst: neue Klasse
   `.maneuver-item-icon` (`css/disclosure.css`) statt `.disclosure-item-icon` — siehe
   `docs/maneuver-icons.md` Abschnitt „Turn-by-Turn-Liste".
3. Kein Schema-Bruch bei den einzelnen `icons.json`-Einträgen (`name`/`orsCode`/
   `valhallaType`/`file`/`label` unverändert) — nur Grid + SVG-Bildinhalt.

### Nicht betroffen

- `assets/map-icons/` (SDF/Karten-Icons) — unverändert.
- Icon-IDs, Dateinamen, `icons.json`-Feldnamen — unverändert.

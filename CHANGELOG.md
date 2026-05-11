# Changelog

Alle relevanten Änderungen am `oe5ith-ci` Repository werden in dieser Datei dokumentiert.

Das Format orientiert sich an semantischer Versionierung:

```text
vMAJOR.MINOR.PATCH
```

Siehe auch:

```text
docs/versioning.md
```

## [2.2.0] - 2026-05-11

### Added

- Geocoder Dropdown: `.geocoder-results`, `.geocoder-item`, `.geocoder-icon`, `.geocoder-content`, `.geocoder-title`, `.geocoder-subtitle` in `css/forms.css`
- `docs/geocoder-dropdown.md`: Dokumentation mit HTML-Struktur, Icon-Referenz und Regeln
- Demo-Abschnitt in `components/forms.html`

---

## [Unreleased]

### Added

- Sidebar Typ 8 — Objekt-Detail: neues Panel für Tracking-/Monitoring-Seiten. Zeigt bei Klick auf ein Kartenobjekt Details (Callsign/Name, Höhe/Speed/Kurs, MMSI/SOG/COG, RSSI). Klassen: `.object-detail`, `.object-detail-header`, `.object-detail-icon`, `.object-detail-name`.
- `components/sidebar-types.html`: Typ 8 Demo-Sektion mit Leerzustand, ADSB-Objekt, AIS-Objekt und Kombinations-Beispiel (Typ 6 + Typ 8).

### Changed

- `css/sidebar.css`: `result-kv`, `status-panel`, `status-row*`, `status-dot` aus Inline-Style von `components/sidebar-types.html` extrahiert — jetzt für alle Produktionsseiten im gemeinsamen CSS verfügbar.
- `docs/sidebar-types.md`: Typ 8 dokumentiert, Entscheidungsbaum und Stapel-Tabelle ergänzt.

---

## v2.1.0 - 2026-05-10

### Added

- `css/topbar.css`: `.topbar-toggle--icon-only` Modifier — Icon-only Toggle-Schaltflächen
  mit CSS-Tooltip auf Desktop (`data-tooltip` via `::after`) und Icon + Label im
  Controls-Overlay (Tablet/Mobile). Pflichtfelder: `data-tooltip` + `.topbar-toggle-label`.
- `css/topbar.css`: `.topbar-nav-dropdown` Komponente — Platzsparendes Navigations-Dropdown
  für `topbar-right`. Ersetzt einzelne `.topbar-nav-link`-Einträge bei mehr als 2–3 Links.
  Label frei wählbar im HTML. Menü rechts ausgerichtet. Auf Mobile ausgeblendet.
- `css/common.css`: `--surface-hover` Token — `rgba(255,255,255,0.05)` für subtile
  Hover-Hintergründe auf dunklen Oberflächen.

### Fixed

- `css/topbar.css`: `.topbar-dropdown-menu` — `min-width: 180px` korrigiert auf
  `min-width: 100%`. Dropdown-Menü öffnet sich nicht mehr breiter als der Toggle-Button.
- `css/topbar.css`: `.topbar-nav-link:hover` — Hardcoded `rgba(255,255,255,0.05)`
  durch `var(--surface-hover)` ersetzt.

---

## v2.0.0 - 2026-05-07

### Breaking

- `css/page.css`: `.map-attribution`, `.map-attribution-sep`, `.map-attribution-info`
  entfernt. Sites die diese Klassen verwenden müssen das `.map-attribution`-HTML-Element
  entfernen und native MapLibre/Leaflet-Attribution aktivieren.
- `css/page.css`: Hide-Regeln `.leaflet-control-attribution` und `.maplibregl-ctrl-attrib`
  entfernt. Native Attribution wird jetzt im Standard-Stil der jeweiligen Bibliothek
  angezeigt.

### Added

- `css/page.css`: `.page-footer`, `.page-footer-version`, `.page-footer-copy`,
  `.page-footer-links` — Fußzeilen-Komponente für Typ-5-Startseiten (ohne Sidebar).
  Enthält Version, Copyright-Text und Linkliste (Impressum, Datenschutz etc.).

---

## v1.6.1 - 2026-05-07

### Fixed

- `css/topbar.css`: `.controls-panel` erhält `gap: 8px` als Fallback. Wenn `display: contents`
  durch eine Utility-Klasse (z.B. `.desktop-only`) überschrieben wird, kleben die Kind-Elemente
  nicht mehr zusammen. Gemeldet via `CI_FIXES_REPORT.md` aus `website-v3`.

---

## v1.4.0 - 2026-05-05

### Added

- `css/coords.css` (neu): Sidebar Typ 7 — Koordinaten-Umrechner Pattern.
  - `.coord-block` / `.coord-block.active` — Container mit Accent-Border-Links für aktives System.
  - `.coord-block-header`, `.coord-block-title`, `.coord-copy` — Titelzeile mit Copy-Button.
  - `.coord-row`, `.coord-label`, `.coord-input` — Standard-Zeile für 2-Feld-Systeme (WGS84 Dezimalgrad, UTM, BMN).
  - `.coord-row-dms`, `.coord-input-dms`, `.coord-suffix` — DMS-Zeile mit 3 schmalen Feldern + N/S, E/W Suffix.
  - `.coord-row-inline`, `.coord-input-short` — Inline-Zeile für 2 Feld-Paare nebeneinander (MGRS GZD + 100km-Square).
  - `.coord-input-full` — Volles Feld ohne Label (Maidenhead Grid).
  - `.coord-input-error` — Fehler-State (rote Border).
  - `.coord-select` — Dropdown für Meridianstreifen (BMN M28/M31/M34).
- `css/sidebar.css`: `.tool-sep` ergänzt (war bisher nur in Komponenten-Inline-Style definiert).
- `components/sidebar-types.html`: Typ 7 Demo-Sektion mit allen 6 Koordinatensystemen.
- `docs/sidebar-types.md`: Typ 7 Beschreibung, Entscheidungsbaum-Erweiterung.

---

## v1.6.0 - 2026-05-07

### Added

- `css/common.css`: Globale Scrollbar-Stilisierung. 6px breiter Thumb in `--border-strong`
  auf transparentem Track. Hover-State `--subtle`. Unterstützt Firefox (`scrollbar-width`/
  `scrollbar-color`) und Chrome/Safari/Edge (`::-webkit-scrollbar`).

### Changed

- `css/common.css`: `--sidebar-width` von 260px auf 300px erhöht. Verbessert die Lesbarkeit
  von Formularen mit mehreren nebeneinanderstehenden Feldern (z.B. DMS-Zeilen im
  Koordinaten-Umrechner). Auf aktuellen Displays (≥1366px Breite) unproblematisch.
- `docs/tokens.md`: `--sidebar-width` und Änderungshistorie aktualisiert.

---

## v1.5.0 - 2026-05-05

### Added

- `css/utils.css` (neu): Utility-Klassen ohne Komponenten-Kontext.
  - `.full-map` — vollflächiger MapLibre/Leaflet-Container (`flex:1`, `height:100%`, `min-height:0`, `position:relative`).
  - `.m-gap` / `.mb-gap` — Abstände via `var(--card-gap)`.
  - `.flex-col` / `.flex-center` — grundlegende Flex-Steuerung.
- `css/common.css`: `--sidebar-tab-width: 16px` und `--sidebar-tab-height: 44px` ergänzt.
- `css/sidebar.css`: `.overlay-section-label` — Variante von `.sidebar-section-label` für schwebende Overlays.
- `components/utils.html` — Referenzseite für alle Utils.
- `components/sidebar-types.html`: `.overlay-section-label` Demo-Sektion.
- `docs/tokens.md`: Z-Index-Bereichstabelle (0–999 App, 1000+ CI) und Tab-Maß-Token-Dokumentation.
- `docs/for-coding-agents.md`: No-Inline-Style-Regel für dynamisch erzeugte HTML-Strings im JS/TS.

---

## v1.3.0 - 2026-05-02

### Added

- `css/code-viewer.css` (neu): Code-Viewer / API-Debugger Pattern.
  - `.panel-code` Modifier auf `.panel` — Terminal-Charakter (schwarzer Hintergrund, starke Border).
  - `.code-viewer-pre` — scrollbarer Code-Block (`max-height: 600px`, `pre-wrap`, Mono-Font, grüne Schrift).
  - `.form-row` — horizontales Flex-Layout für Control-Panel-Inputs (`flex-end` ausgerichtet).
- `css/typography.css`: Utility-Klassen ergänzt.
  - `.mono` — wendet `var(--font-mono)` auf beliebige Elemente an.
  - `.ci-label` — kleines Uppercase-Label außerhalb von `.form-field` Kontexten.
- `components/code-viewer.html` — Referenz-Seite mit allen Badge-Varianten (200 OK, 302 Found, 404 Not Found) und `.mono` Demo.
- `docs/code-viewer.md` — vollständige Komponentendokumentation.
- `docs/for-coding-agents.md`: Abschnitt 5a API-Debugger / Code-Viewer ergänzt.
- `docs/tokens.md`: Verwendungshinweise für `--code-bg` und `--code-text` auf `.panel-code` ergänzt.
- `.gitignore` hinzugefügt.

---

## v1.2.0 - 2026-04-29

### Changed

- `css/page.css`: `.result-action` (Auge-Button) überarbeitet.
  - Neuer unabhängiger Toggle-State: `.result-action.active` = Route sichtbar (Success-Grün).
  - Kaputte Regel `result-item.active .result-action { color: accent }` entfernt (blau auf blau).
  - Default-Farbe von `--subtle` auf `--muted` angehoben (dezent sichtbarer).
- `css/page.css`: `.result-item-simple` (Typ 5) auf Card-Stil von `.result-item` angehoben.
  - Gleicher Rahmen, Hover und Active-State wie Typ 4.
  - `.result-simple-org` und `.result-simple-meta` mit `padding-left: 25px` (fluchtet mit Titel nach Badge).
- `docs/sidebar-types.md`: Typ 4 und Typ 5 aktualisiert.
- `components/sidebar-types.html`: Typ 4 zeigt alle Auge-Zustände; Typ 5 mit Card-Stil und Nummer-Badge.

---

## v1.1.0 - 2026-04-27

### Added

- `docs/concepts.md` ergänzt.
  - Begriffe und Ebenen wie CI, Brand, Design System, CSS Library und Komponenten-Referenz definiert.
- `docs/usage.md` ergänzt.
  - CSS-Einbindung, Reihenfolge, Demo-CSS-Regel und Beispiele für Seitentypen dokumentiert.
- `docs/for-coding-agents.md` ergänzt.
  - Regeln für automatisierte Änderungen, Coding-Agenten und CI-konforme Umsetzung dokumentiert.
- `docs/versioning.md` ergänzt.
  - Semantische Versionierung, Release-Regeln, Git-Tags und Deprecation-Regeln dokumentiert.

### Changed

- `README.md` überarbeitet.
  - Zweck des Repositories klarer beschrieben.
  - Repo-Struktur aktualisiert.
  - Bereiche `css/`, `components/`, `docs/` und `assets/` erklärt.
  - wichtige Einstiegsdokumente ergänzt.
  - Begriffsklärung zu CI, Design System, CSS Library und Komponenten-Referenz ergänzt.
- `docs/tokens.md` überarbeitet.
  - Master-Datei auf `css/common.css` vereinheitlicht.
  - Sidebar-Tab-Tokens in die Akzent-Tabelle aufgenommen.
  - eingebettete `common.css` mit den aktuellen Token-Werten synchronisiert.

### Fixed

- Widerspruch zwischen `shared/assets/common.css` und `css/common.css` in der Token-Dokumentation korrigiert.
- Veraltete Z-Index-Werte im eingebetteten `common.css`-Block von `docs/tokens.md` korrigiert.
- Beispiel für `.layout` in `docs/tokens.md` auf `var(--topbar-height)` korrigiert.

### Notes

- Diese Version enthält nur Dokumentations- und Strukturverbesserungen.
- Es wurden keine produktiven CSS-Klassen entfernt.
- Bestehende Webseiten sollten mit dieser Version kompatibel bleiben.

---

## v1.0.0 - 2026-04-22

### Added

- Initiale vollständige Token-Definition.
- Basisfarben, Akzentfarben und semantische Farben definiert.
- Typografie-, Spacing-, Z-Index-, Transition- und Shadow-Tokens ergänzt.
- Komponentenstruktur für Topbar, Sidebar, Cards, Buttons, Badges, Forms, Modal und Typografie aufgebaut.
- Referenz-HTMLs in `components/` ergänzt.
- Spezifikationen in `docs/` ergänzt.
- Logo und Favicons in `assets/` ergänzt.

### Notes

- Erste konsolidierte Version des OE5ITH CI / Design Systems.

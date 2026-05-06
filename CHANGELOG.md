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

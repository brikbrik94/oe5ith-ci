# Changelog

Alle relevanten Änderungen am `oe5ith-ci` Repository werden in dieser Datei dokumentiert.
Format: `## vX.Y.Z - YYYY-MM-DD` · Neueste Version zuerst · Siehe `docs/versioning.md`

---

## [Unreleased]

### Fixed
- `coords.css`: in `.coord-vals`-Zeilen (`.coord-row-wgs`) bekommen Nicht-Dezimal-Felder (Grad,
  ganzzahlige Minuten) jetzt eine feste, schmale Breite (36px) statt sich die Zeile gleichmäßig
  mit dem Dezimalfeld zu teilen; das Dezimalfeld (`inputmode="decimal"`, immer das letzte in der
  Zeile) bekommt dadurch den verbleibenden Platz. Additiv zur bestehenden `flex: 1`-Regel, DD-Format
  (ein Dezimalfeld pro Zeile) bleibt optisch unverändert. Angefragt aus `website-v3`
  (Koordinaten-Umrechner, `Wgs84Block.ts`).

---

## v1.21.0 - 2026-07-18

### Added
- `badges.css`: `.badge-wrap` Modifier-Klasse — erlaubt internen Zeilenumbruch für Badges mit
  langem/variablem Text (z.B. Warnungen in schmalen Sidebars), ohne das `nowrap`-Standardverhalten
  für kurze Status-Badges zu ändern. Behebt Meldung aus `website-v3` (Routing-Sidebar-Warn-Badges).
- `common.css`: neuer Token `--map-bg` (Default `#ffffff`) für den Karten-Container-Hintergrund;
  `utils.css`: `.full-map` nutzt `background: var(--map-bg)`. Übernahme aus `website-v3`
  (Koordinaten-Umrechner-Karte), vorher nur als lokaler App-Override vorhanden.
- `coords.css`: neue Klassen `.coord-row-wgs` / `.coord-vals` — einheitliche Gesamtbreite für
  WGS84-Koordinatenzeilen unabhängig von der Feldanzahl (DD/DDM/DMS), baut auf `.coord-input-dms`
  auf. Übernahme aus `website-v3` (Koordinaten-Umrechner), vorher nur lokal in der App vorhanden.
- `modal.css` / `MapLegend`: neuer Eintragstyp `icon` (`.map-legend-icon`, 12×12px) für
  Legenden-Einträge mit Formsemantik (z.B. Fahrzeug-/Stations-Icons statt reiner Farbfläche).
  Additiv — bestehende `dot`/`line`/`area`-Konsumenten bleiben unverändert funktionsfähig.
  Angefragt aus `website-v3` (NAH-Luftrettungs-Legende).

---

## v1.20.0 - 2026-07-07

### Added
- **Maneuver-Icons (Turn-by-Turn)** — 14 line-art SVG-Richtungssymbole (`ci-maneuver-*`), 1:1 zu OpenRouteService-Manöver-Codes 0–13 (Left/Right/Sharp/Slight/Straight/Roundabout Enter+Exit/U-turn/Goal/Depart/Keep Left+Right). Neues Asset-Verzeichnis `assets/maneuver-icons/` mit `icons.json`-Manifest (ORS-Code-Mapping), Referenz `components/maneuver-icons.html`, Doku `docs/maneuver-icons.md`. Neuer `.disclosure-item-icon`-Slot in `css/disclosure.css` für die Turn-by-Turn-Sidebar-Liste — keine neuen Tokens, reuse `--text`.

---

## v1.19.0 - 2026-07-06

### Added
- **Disclosure (Single-Panel)** — generische Komponente für ein einzelnes auf-/zuklappbares Panel ohne Auswahlzustand, nativ auf `<details>`/`<summary>` aufgebaut, kein JS nötig. Neue `css/disclosure.css`, Referenz `components/disclosure.html`, Doku-Abschnitt in `docs/sidebar.md` (Abgrenzung zu `.accordion`). Keine neuen Tokens — reuse `.badge`, `--surface-hover`.

---

## v1.18.1 - 2026-07-06

### Fixed
- `modal.css`: `.modal-backdrop` setzte `z-index: var(--z-backdrop)` (1040) statt `var(--z-modal)` (1500) — durch den eigenen Stacking-Context von `position: fixed` + `z-index` rendert das gesamte Modal (inkl. `.modal`) dadurch unter einer stickyen `.topbar` (`--z-topbar`: 1100), unabhängig vom `z-index` von `.modal` selbst. Betrifft jedes Portal, das `modal.css` mit stickyer Topbar kombiniert. `--z-backdrop` bleibt unverändert (weiterhin für `sidebar-backdrop`/`controls-backdrop`, die bewusst unter der Topbar bleiben sollen).

---

## v1.18.0 - 2026-06-24

### Added
- `page.css`: `.status-msg` Komponente mit Modifier-Klassen `.info`, `.warn`, `.error` — Inline-Statusmeldungen für Aktions-Feedback, Fehlerzustände und Leer-Zustände; behebt gleichzeitig unstyled usage in bestehenden Portal-Views (`logs.html`, `pocsag.html`)
- `utils.css`: `.max-w-150`, `.max-w-200` — Max-Width-Utilities für kurze Formularfelder
- `utils.css`: `.text-right` — Text-Alignment-Utility, ergänzt `.text-center` und `.text-left`
- `components/status-msg.html` — Referenz-Demo für alle drei `.status-msg`-Varianten

---

## v1.17.0 - 2026-06-22

### Added
- **Map-Icons (SDF)** — Neue Asset-Kategorie `assets/map-icons/`: einfarbige, über MapLibre `icon-color` umfärbbare SDF-Form-Quellen für Karten. Initialer Katalog (7): `ci-pin`, `ci-pin-hole`, `ci-bubble-label` (dehnbar), `ci-marker-dot`, `ci-marker-ring`, `ci-symbol-location`, `ci-symbol-warning`. Manifest `icons.json` (Builder- + Konsumenten-API inkl. Stretch-Zonen), Referenz `components/map-icons.html`, Doku `docs/map-icons.md`. Der Sprite-Build erfolgt extern (Submodul-Repo); keine neuen Tokens.

---

## v1.16.0 - 2026-06-22

### Added
- Seitentyp **Typ 7 — Statistik-Explorer**: fixiertes Steuer-Feld (Tabellen-Auswahl, Zeitraum-Presets + Von–Bis, Filter, Aktionen) über einer in sich scrollbaren, sortierbaren `ci-table` mit Sticky-Header. Neue Datei `css/stats.css`, Referenz `components/stats-explorer.html`, Doku `docs/page-stats.md`. Keine neuen Tokens. (`docs/page-types.md` Typ 7 ergänzt.)

---

## v1.15.3 - 2026-06-19

### Added
- **split.css** — Optionaler zweizeiliger Master-Eintrag: `.split-item-text` (umschließt Label + Unterzeile) und `.split-item-sub` (gedämpfte, einzeilige Unterzeile mit Ellipsis) für eine sekundäre Info pro Quelle (z. B. letzte Meldung). Rückwärtskompatibel — bestehende einzeilige `.split-item-label`-Nutzung bleibt unverändert. Beispiel in `components/split-view.html`.

---

## v1.15.2 - 2026-06-19

### Fixed
- **split.css** — Detail-Spalte (`.split-detail`) staucht ihre Kinder nicht mehr zusammen. Da `.split-detail` ein `flex`-`column` mit `overflow-y:auto` ist, schrumpften die Panels per Default-`flex-shrink:1` (z. B. wurde das Filter-Panel über der Ergebnis-Tabelle unsichtbar gequetscht) statt dass die Spalte scrollte. `.split-detail > * { flex-shrink: 0 }` lässt jedes Kind seine natürliche Höhe behalten, sodass das Detail bei Überlänge wie vorgesehen als Ganzes scrollt.

---

## v1.15.1 - 2026-06-19

### Fixed
- **split.css** — Fixed-Height-Modus funktioniert jetzt auch, wenn zwischen `.page-content` und `.content-body` ein eigener Wrapper liegt (z. B. SPA-View-Container wie `.view-section`). Bisher setzte die Aktivierung voraus, dass `.content-body` direktes Kind von `.page-content` ist; ein Zwischen-Wrapper unterbrach die Flex-Höhenkette, wodurch die Seite über die Viewport-Höhe hinaus wuchs und abgeschnitten wurde (kein Scroll) statt Master/Detail separat scrollen zu lassen. Neue Regel reicht den Wrapper, der den Split enthält, als flex-füllendes Element durch.

---

## v1.15.0 - 2026-06-19

### Added
- **utils.css** — Breiten-Utilities: `.col-w-80`, `.col-w-100`, `.col-w-120`, `.col-w-180` (feste Spaltenbreiten für Tabellen-`<th>`) und `.max-w-300` (Max-Breite für Container/Select). Referenz-Demo in `components/utils.html`. Behebt zuvor wirkungslose No-op-Klassen in den website-v3-Views (logs, POCSAG).

---

## v1.14.0 - 2026-06-18

### Added
- **Split-View (Typ 6)** — generische Master-Detail-Komponente: schmale scrollbare Auswahlliste links, Detailbereich rechts, beide unabhängig scrollbar. Neue `css/split.css`, Tokens `--split-master-width`/`--split-master-max-h`, Doku `docs/split-view.md`, Referenz `components/split-view.html`, Seitentyp Typ 6 in `docs/page-types.md`.

---

## v1.13.1 - 2026-06-11

### Fixed
- **Kalender**: Wochenzeilen sind jetzt einheitlich hoch. Bisher richtete sich jede
  Zeile nach ihrem Inhalt (`grid-auto-rows` ungesetzt → `auto`), wodurch Wochen mit
  mehreren Einträgen pro Tag höher wurden als spärliche Wochen. Über
  `grid-template-rows: auto` (kompakter Wochentag-Header) + `grid-auto-rows: 1fr`
  werden alle Wochenzeilen auf die höchste angeglichen. In der einspaltigen
  Mobilansicht (≤768px) bleibt `grid-auto-rows: auto`.

---

## v1.13.0 - 2026-06-11

### Added
- **Chart-Komponente** (`css/chart.css`, `docs/chart.md`, `components/chart.html`, neu):
  datengetriebene Verlaufsdarstellung per Inline-SVG. Typen: Linie, Fläche (`chart-area`),
  Balken (`chart-bar`), Sparkline (`chart-sparkline`). Serien- und Schwellwert-Färbung,
  Achsen, Grid, Legende, Tooltip, Empty-State.
- **Chart-Token** in `common.css`: `--chart-1`–`--chart-4`, `--chart-grid`, `--chart-axis`,
  `--chart-area-opacity` (dokumentiert in `docs/tokens.md`).
- **service-dashboard**: neuer Panel-Typ „Verlauf / Historie"; Sparkline als optionales
  letztes Kind in `.svc-data-cell` und in Übersichts-Kacheln.

---

## v1.12.3 - 2026-06-08

### Added
- **docs/service-dashboard.md** — Abschnitt „Inhalt & Semantik" für Detail- und Config-Seite:
  - **Detail:** Ein-Endpunkt-Regel (eine Detailseite zeigt genau einen Dienst/Endpunkt);
    festes Set erlaubter Panel-Typen (Live-Status [Pflicht], Verbindung/Endpoint,
    Konfiguration read-only, Diagnose/Fehler); Zellen-Regel (ein Wert = eine `.svc-data-cell`).
  - **Config:** Kategorien-Gruppierung als offenes Prinzip (Beispiele: Allgemein, Verbindung,
    Authentifizierung, Erweitert); Pflicht-Überschrift je Panel.

### Changed
- `.panel-title` auf der Config-Seite von „bestehende Klasse" zu **Pflicht je Panel** hochgestuft.

---

## v1.12.2 - 2026-06-07

### Added
- **docs/doc-standard.md** (neu): verbindlicher Doku-Standard für `category: component`-Docs.
  Vier Pflicht-Garantien — G1 vollständige Element-Tabelle, G2 Verschachtelungs-Baum,
  G3 Reihenfolge/Platzierung, G4 Zustände/Varianten — damit Coding-Agenten Komponenten allein
  aus der Doc bauen können, ohne die `components/*.html` zu interpretieren. Registriert in
  `docs/registry.json` (concept). Verankert in `docs/for-coding-agents.md` (neuer Abschnitt +
  Prüflisten-Punkt).
- **service-dashboard.css**: neue Layout-Klassen `.svc-page-title-row`, `.svc-field-grid`
  (+ `.svc-field-grid--cols-3`), `.svc-label-type`, `.svc-field-code` sowie Regel
  `.svc-toggle.warn .svc-toggle-sublabel`.

### Changed
- `docs/service-dashboard.md` auf den Doku-Standard gehoben (interpretationsfrei, G1–G4 für alle
  drei Seiten: vollständige Element-Tabellen, Verschachtelungs-Bäume, Button-/Header-Platzierung,
  Zustände-Tabelle).

### Fixed
- `service-dashboard-*.html`: Layout-Inline-Styles durch CI-Klassen ersetzt; hartcodierte Farbe
  `#4ade80` der JSON-Textarea durch `var(--code-text)` ersetzt.

---

## v1.12.1 - 2026-06-07

### Added
- **scripts/cli/check_consistency.py** (neu): Manifest-getriebener Konsistenz-Check. Prüft `docs/registry.json` gegen die realen Dateien — Dangling-Verweise, verwaiste Dateien, fehlende `css/index.css`-Imports und den Dreiklang Spec→Referenz→CSS. Exit-Code-basiert (CI-tauglich), inkl. `unittest`-Tests.
- **docs/registry.json** (neu): deklaratives Manifest als Single Source of Truth dafür, welche Dateien zu welchem Feature gehören (Kategorien `component`/`concept`/`infra`).
- `docs/for-coding-agents.md`: Abschnitt „Neue Komponente registrieren"; CLAUDE.md Regel 8 verweist darauf.
- `README.md`: Datei-Baum und Status-Tabelle werden via `check_consistency.py --write` zwischen AUTOGEN-Markern generiert und können nicht mehr veralten.

### Changed
- `README.md`: veraltete Übersicht korrigiert — `calendar.css`, `code-viewer.css`, `coords.css`, `service-dashboard.css`, `toast.css`, `utils.css` ergänzt; nicht existierende `tokens.css` entfernt.
- `CLAUDE.md`: „CSS loading order" an die reale Reihenfolge in `css/index.css` angeglichen.

### Removed
- `CI_FIXES_REPORT.md`: obsolet — die beschriebenen Z-Index-Tokens und `--topbar-height-mobile` sind vollständig umgesetzt.

---

## v1.12.0 - 2026-06-07

### Added
- **service-dashboard.css** (neu): CI-Baustein für lokale Raspberry-Pi-Dienst-Überwachung.
  - `.svc-card-icon`, `.svc-info-line`, `.svc-status-line.online/offline/unknown` — Kachel-Elemente für die Übersichtsseite
  - `.svc-page-icon` — FA-Icon im Page-Header der Detail-Seite
  - `.svc-data-grid`, `.svc-data-cell`, `.svc-data-label`, `.svc-data-value`, `.svc-data-sub` — Live-Status-Datenpanel
  - `.svc-back-link` — Zurück-Navigation auf der Config-Seite
  - `.svc-field`, `.svc-field-readonly`, `.svc-field-hint` — Formular-Feld-Wrapper
  - `.svc-input-prefix`, `.svc-input-prefix-label` — URL-Felder mit Protokoll-Prefix
  - `.svc-secret`, `.svc-secret-toggle` — Passwort-Felder mit Auge-Toggle
  - `.svc-toggle`, `.svc-toggle.warn`, `.svc-toggle-track`, `.svc-toggle-thumb`, `.svc-toggle-label`, `.svc-toggle-sublabel` — Toggle-Switch für Boolean-Config-Felder
  - `.svc-form-actions`, `.svc-form-hint` — Aktionsleiste auf der Config-Seite
  - `.sidebar-status-dot.unknown` — fehlende unknown-Variante für Sidebar-Dots ergänzt
- Drei neue Referenz-HTML-Seiten: `components/service-dashboard-overview.html`, `components/service-dashboard-detail.html`, `components/service-dashboard-config.html`
- Dokumentation: `docs/service-dashboard.md`

### Fixed
- `cards.css`: `.card-status-dot.unknown` verwendet jetzt `var(--warning)` und `var(--warning-subtle)` statt hardcodierten Amber-Werten

---

## v1.11.2 - 2026-06-06

### Added
- Breitengrenze auf `.calendar` (`max-width: 100%`, `overflow: hidden`), `.calendar-day` (`min-width: 0`, `overflow: hidden`) und `.calendar-entry` (`max-width: 100%`)
- `.calendar-entry--multiline` Modifier: Zeit auf Zeile 1, Titel umbricht ab Zeile 2

---

## v1.11.1 - 2026-06-06

### Added
- `.calendar--show-all` Modifier-Klasse für Mobile: zeigt alle Tageszellen inkl. leerer
- Tablet-Breakpoint (769px–1024px) mit komprimierter Eintragsdarstellung in `css/calendar.css`

---

## v1.11.0 - 2026-06-06

### Added

- 10 generische Kalender-Farbslots (`--cal-color-1` bis `--cal-color-10`) mit Subtle- und Border-Varianten in `css/common.css`
- `.calendar-entry--color-1` bis `.calendar-entry--color-10` Modifier-Klassen in `css/calendar.css`
- `.calendar-entry--continues-left` und `.calendar-entry--continues-right` für mehrtägige Events
- Rückwärtskompatible Aliase (`.calendar-entry--early`, `.--late`, `.--night`, `.--default`) auf die neuen Slots

---

## v1.10.0 - 2026-06-03

### Added

- **calendar.css** (neu): Monatskalender-Komponente für Dienstplan-Darstellung aus ICS-Backend.
  - `.calendar`, `.calendar-header`, `.calendar-title`, `.calendar-nav-btn` — Navigation mit Zurück/Vor-Pfeilen und Heute-Button.
  - `.calendar-grid`, `.calendar-weekday` — 7-Spalten-Raster mit Wochentag-Köpfen.
  - `.calendar-day`, `.calendar-day--today`, `.calendar-day--outside` — Tageszellen mit Heute-Indikator (Accent-Kreis) und gedimmten Außerhalb-Tagen (opacity: 0.35).
  - `.calendar-entry`, `.calendar-entry-time`, `.calendar-entry-title`, `.calendar-entry-changed` — Eintragszeilen mit Uhrzeit, Titel und optionalem Änderungsindikator (`--warning`, fa-circle-exclamation).
  - `.calendar-entry--early`, `.calendar-entry--late`, `.calendar-entry--night`, `.calendar-entry--default` — Diensttyp-Farbcodierung via bestehende semantische Tokens.
  - `.cal-modal-*` — Modal-Inhalt-Klassen für Detailansicht (wiederverwendet `.modal-backdrop` aus `modal.css`).
  - Mobile (≤768px): Grid kollabiert zu einspaltiger Liste, leere Tage ausgeblendet.
- `components/calendar.html` — Referenzseite mit allen Zuständen: Heute, Außerhalb-Tage, 2 Einträge pro Tag, Änderungsindikator, funktionales Detail-Modal.
- `docs/calendar.md` — vollständige Komponentendokumentation.
- **Sidebar Typ 8 — Tracking-Liste**: scrollbare Liste aller empfangenen ADSB/AIS-Objekte mit Mode-Switch (Alle / ADS-B / AIS) und Expand-Verhalten. Klassen: `.tracking-list`, `.tracking-item`, `.tracking-item-header`, `.tracking-item-body`, `.tracking-item-icon`, `.tracking-item-name`, `.tracking-item-chevron`.
- **utils.css** — Text/Visibility: `.text-center`, `.text-left`, `.opacity-50`, `.hidden`
- **utils.css** — Flex: `.flex-1`, `.flex-2`, `.w-full`, `.flex-align-center`, `.justify-between`, `.gap-4`
- **utils.css** — Table: `.table-wrapper`, `.table-col-25`, `.border-collapse`
- **utils.css** — Spacing: `.m-0`, `.mt-0`, `.mt-8`, `.mt-12`, `.mb-8`, `.pb-0`, `.p-double-gap`, `.mb-1-5-gap`, `.p-2rem`
- **utils.css** — Misc: `.pos-relative`, `.cursor-pointer`, `.border-none`, `.no-dot-bg`
- **typography.css** — Font-Weights: `.font-medium`, `.font-semibold`
- **typography.css** — Text-Utilities: `.t-success`, `.t-danger`, `.t-muted`, `.t-subtle`, `.t-white`, `.t-tiny`
- **sidebar.css** — `.acc-item.loading-state`, `.acc-item.error-state` für asynchrone Layer-Zustände
- **cards.css** — `.sprite-preview-img` für Icon-/Asset-Vorschauen in Cards
- **coords.css** — `.coord-header-status` für Zusatz-Text im Koordinaten-Block-Header
- **sidebar.css** — `.acc-dot` erhält `background: var(--accent)` als CI-Default
- **common.css / tokens.md** — Token `--white: #ffffff`
- Referenz-Demos in `components/utils.html`, `components/typography.html`, `components/sidebar.html`, `components/cards.html` aktualisiert

### Changed

- `docs/sidebar.md`: `.acc-dot` Dokumentation aktualisiert. Async-Zustände `.loading-state` / `.error-state` dokumentiert.
- `docs/sidebar-types.md`: Typ 8 vollständig neu definiert (Tracking-Liste ersetzt Objekt-Detail).
- `docs/topbar.md`: Regel ergänzt dass `.topbar-nav-dropdown-toggle` keine feste Breite benötigt (Label zur Laufzeit unveränderlich).

### Removed

- `.object-detail`, `.object-detail-header`, `.object-detail-icon`, `.object-detail-name` aus `css/sidebar.css` — kein Produktionseinsatz, ersetzt durch `.tracking-*`.

---

## v1.9.0 - 2026-05-11

### Added

- Geocoder Dropdown: `.geocoder-results`, `.geocoder-item`, `.geocoder-icon`, `.geocoder-content`, `.geocoder-title`, `.geocoder-subtitle` in `css/forms.css`
- `docs/geocoder-dropdown.md`: Dokumentation mit HTML-Struktur, Icon-Referenz und Regeln
- Demo-Abschnitt in `components/forms.html`

---

## v1.8.0 - 2026-05-10

### Added

- `css/topbar.css`: `.topbar-toggle--icon-only` Modifier — Icon-only Toggle-Schaltflächen mit CSS-Tooltip auf Desktop (`data-tooltip` via `::after`) und Icon + Label im Controls-Overlay (Tablet/Mobile).
- `css/topbar.css`: `.topbar-nav-dropdown` Komponente — Navigations-Dropdown für `topbar-right`. Ersetzt einzelne `.topbar-nav-link`-Einträge bei mehr als 2–3 Links. Menü rechts ausgerichtet. Auf Mobile ausgeblendet.
- `css/common.css`: Token `--surface-hover: rgba(255,255,255,0.05)` für subtile Hover-Hintergründe.

### Fixed

- `css/topbar.css`: `.topbar-dropdown-menu` — `min-width` korrigiert auf `min-width: 100%`.
- `css/topbar.css`: `.topbar-nav-link:hover` — Hardcoded Wert durch `var(--surface-hover)` ersetzt.

---

## v1.7.0 - 2026-05-07

### Added

- `css/page.css`: `.page-footer`, `.page-footer-version`, `.page-footer-copy`, `.page-footer-links` — Fußzeilen-Komponente für Typ-5-Startseiten.

### Removed

- `css/page.css`: `.map-attribution`, `.map-attribution-sep`, `.map-attribution-info` entfernt — kein Produktionseinsatz, native MapLibre/Leaflet-Attribution wird verwendet.
- `css/page.css`: Hide-Regeln `.leaflet-control-attribution` und `.maplibregl-ctrl-attrib` entfernt.

---

## v1.6.1 - 2026-05-07

### Fixed

- `css/topbar.css`: `.controls-panel` erhält `gap: 8px` als Fallback für Utility-Klassen-Konflikte.

---

## v1.6.0 - 2026-05-07

### Added

- `css/common.css`: Globale Scrollbar-Stilisierung. 6px breiter Thumb in `--border-strong` auf transparentem Track.

### Changed

- `css/common.css`: `--sidebar-width` von 260px auf 300px erhöht.
- `docs/tokens.md`: `--sidebar-width` Änderungshistorie aktualisiert.

---

## v1.5.0 - 2026-05-05

### Added

- `css/utils.css` (neu): `.full-map`, `.m-gap`, `.mb-gap`, `.flex-col`, `.flex-center`
- `css/common.css`: `--sidebar-tab-width: 18px`, `--sidebar-tab-height: 44px`
- `css/sidebar.css`: `.overlay-section-label`
- `components/utils.html` — Referenzseite
- `docs/tokens.md`: Z-Index-Bereichstabelle und Tab-Maß-Token-Dokumentation
- `docs/for-coding-agents.md`: No-Inline-Style-Regel für dynamisch erzeugte HTML-Strings

---

## v1.4.0 - 2026-05-05

### Added

- `css/coords.css` (neu): Sidebar Typ 7 — Koordinaten-Umrechner Pattern mit allen Eingabezeilen-Varianten (WGS84, UTM, BMN, DMS, MGRS, Maidenhead).
- `css/sidebar.css`: `.tool-sep`
- `components/sidebar-types.html`: Typ 7 Demo
- `docs/sidebar-types.md`: Typ 7 Beschreibung

---

## v1.3.0 - 2026-05-02

### Added

- `css/code-viewer.css` (neu): `.panel-code`, `.code-viewer-pre`, `.form-row`
- `css/typography.css`: `.mono`, `.ci-label`
- `components/code-viewer.html` — Referenzseite
- `docs/code-viewer.md` — Dokumentation
- `.gitignore`

---

## v1.2.0 - 2026-04-29

### Changed

- `css/page.css`: `.result-action` überarbeitet — neuer Toggle-State `.result-action.active`.
- `css/page.css`: `.result-item-simple` auf Card-Stil angehoben.
- `docs/sidebar-types.md`: Typ 4 und Typ 5 aktualisiert.

---

## v1.1.0 - 2026-04-27

### Added

- `docs/concepts.md`, `docs/usage.md`, `docs/for-coding-agents.md`, `docs/versioning.md`

### Changed

- `README.md` überarbeitet.
- `docs/tokens.md` überarbeitet und mit `css/common.css` synchronisiert.

### Fixed

- Widerspruch zwischen Token-Dokumentation und `css/common.css` korrigiert.

---

## v1.0.0 - 2026-04-22

### Added

- Initiale vollständige Token-Definition, Komponentenstruktur, Referenz-HTMLs, Spezifikationen, Logo und Favicons.

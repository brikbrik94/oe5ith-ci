# Changelog

Alle relevanten Änderungen am `oe5ith-ci` Repository werden in dieser Datei dokumentiert.
Format: `## vX.Y.Z - YYYY-MM-DD` · Neueste Version zuerst · Siehe `docs/versioning.md`

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

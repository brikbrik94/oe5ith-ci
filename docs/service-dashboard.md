# Service Dashboard

**Referenz-Dateien:** `components/service-dashboard-overview.html` · `components/service-dashboard-detail.html` · `components/service-dashboard-config.html`
**CSS:** `css/service-dashboard.css`
**Status:** definiert · v1.12.2

> Diese Doc folgt `docs/doc-standard.md` (interpretationsfrei). Die Beispiel-HTML in
> `components/` ist Verifikation, nicht Quelle — alles Nötige steht hier im Text.

---

## Überblick

Drei-Seiten-Muster für lokale Raspberry-Pi-Dienst-Überwachung. Basiert auf bestehenden
CI-Klassen; `service-dashboard.css` ergänzt nur was kein bestehendes Muster abdeckt.

### Ladereihenfolge

```css
css/common.css
css/cards.css        /* card-dashboard, card-grid, card-status-dot */
css/badges.css       /* badge-green/red/yellow */
css/buttons.css      /* btn, btn-danger, btn-secondary, btn-ghost, btn-primary */
css/page.css         /* page-header, panel, content-body */
css/sidebar.css      /* sidebar-nav-item, sidebar-status-dot */
css/service-dashboard.css  /* svc-* Klassen — immer zuletzt */
```

---

## Seite 1 — Übersicht (Seitentyp 3: Dashboard)

Zeigt alle Dienste eines Pi als klickbare Kacheln im Card-Grid.

### Verschachtelung (G2)

```text
.card-grid
└── a.card.card-dashboard.card-dashboard-link
    ├── div.card-status-dot[.online|.offline|.unknown]   (Pflicht)
    ├── h3
    │   ├── i.svc-card-icon                               (Optional)
    │   └── span (Titel-Text)                             (Pflicht)
    ├── p.svc-info-line                                   (Optional)
    ├── span.svc-status-line[.online|.offline|.unknown]   (Pflicht)
    └── i.card-dashboard-arrow                            (Pflicht)
```

### Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.card-grid` | Grid-Container der Kacheln (aus `cards.css`) | Pflicht | — |
| `.card.card-dashboard.card-dashboard-link` | Klickbare Dienst-Kachel (aus `cards.css`) | Pflicht | — |
| `.card-status-dot` | Status-Punkt oben in der Kachel (aus `cards.css`) | Pflicht | `.online`, `.offline`, `.unknown` |
| `.svc-card-icon` | FA-Icon inline im h3-Titel (accent, 0.85rem, flex-shrink:0) | Optional | — |
| `.svc-info-line` | Kurzbeschreibung unter Titel (0.75rem, muted) | Optional | — |
| `.svc-status-line` | Statuszeile unten (0.7rem) | Pflicht | `.online`, `.offline`, `.unknown` |
| `.card-dashboard-arrow` | Pfeil-Icon rechts (aus `cards.css`) | Pflicht | — |

### Reihenfolge & Platzierung (G3)

- Reihenfolge in der Kachel: Status-Dot → h3 (Icon, dann Titel) → Info-Zeile → Status-Zeile → Pfeil.
- Wenn `.svc-card-icon` im h3 verwendet wird, MUSS der Textteil in `<span>` stehen, damit
  Truncation korrekt funktioniert.

---

## Seite 2 — Detail (Seitentyp 1: Detail-Seite)

### Verschachtelung (G2)

```text
.page-header
├── .page-header-left
│   ├── (Titelzeile: i.svc-page-icon + h1.page-title + span.badge.badge-*)   (Pflicht)
│   └── p.page-subtitle                                                      (Optional)
└── .page-header-right
    ├── button.btn.btn-danger     (destruktive Aktion, z. B. Neustart)       (Optional)
    └── a.btn.btn-secondary       (Navigation, z. B. Config)                 (Optional)

.svc-data-grid
└── .svc-data-cell                                                          (Pflicht, n×)
    ├── span.svc-data-label                                                 (Pflicht)
    ├── span.svc-data-value[.success|.danger]                              (Pflicht)
    └── span.svc-data-sub                                                   (Optional)
```

### Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.svc-page-icon` | FA-Icon im Page-Header der Detailseite | Pflicht | — |
| `.svc-data-grid` | Responsive Grid: 3/2/1 Spalten (Desktop/Tablet/Mobile) | Pflicht | — |
| `.svc-data-cell` | Einzelne Zelle: panel-deep Hintergrund, 8px Radius | Pflicht | — |
| `.svc-data-label` | Bezeichnung (0.68rem, uppercase, `--subtle`) | Pflicht | — |
| `.svc-data-value` | Wert (0.95rem, 600, `--text`) | Pflicht | `.success`, `.danger` |
| `.svc-data-sub` | Subtext (0.72rem, `--muted`) | Optional | — |

Bestehende Klassen: `.page-header`, `.page-header-left`, `.page-header-right`,
`.page-title`, `.page-subtitle`, `.badge.badge-green/red/yellow`, `.btn.btn-danger`,
`.btn.btn-secondary`.

### Reihenfolge & Platzierung (G3)

- **Header links:** Icon → Titel → Status-Badge in einer Zeile; Subtitle darunter.
- **Header rechts:** Aktions-Buttons. Destruktive Aktionen (Restart) als `btn-danger`,
  Navigation (Config) als `btn-secondary`. Destruktive Aktion zuerst, Navigation danach.
- Nur API-Endpunkte/Aktionen einblenden, die tatsächlich vorhanden sind. Destruktive
  Aktionen immer mit `confirm()` absichern.

---

## Seite 3 — Config (Seitentyp 1: Detail-Seite)

### Verschachtelung (G2)

```text
a.svc-back-link                                              (Pflicht)

(Formularfeld je Typ — siehe Feldtypen-Tabelle)

.svc-form-actions                                            (Pflicht)
├── button.btn.btn-primary   (Speichern, fa-floppy-disk)    (Pflicht)
├── a.btn.btn-ghost          (Abbrechen)                    (Pflicht)
└── span.svc-form-hint       (Hinweis, z. B. Neustart)      (Optional)

.svc-toggle[.on|.warn]                                       (Toggle-Feldtyp)
├── .svc-toggle-track
│   └── .svc-toggle-thumb
├── .svc-toggle-label
└── .svc-toggle-sublabel                                     (Optional)
```

### Feldtypen / Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.svc-back-link` | Zurück-Navigation oben (mit `fa-arrow-left`) | Pflicht | — |
| `.svc-field` | Standard-Feld: `<input text/number>`, `<select>`, `<textarea>` | Pflicht (je Feld) | — |
| `.svc-field-readonly` | Read-only-Wert als `<div>` statt Input | Optional | — |
| `.svc-field-hint` | Hilfstext unter einem Feld (`<span>`) | Optional | — |
| `.svc-secret` | Wrapper für Passwort-Feld mit Auge-Toggle | Optional | — |
| `.svc-secret-toggle` | Sichtbarkeits-Umschalter im Secret-Feld | Optional | — |
| `.svc-input-prefix` | Wrapper für Input mit Protokoll-Prefix | Optional | — |
| `.svc-input-prefix-label` | Prefix-Label (z. B. `https://`) | Optional | — |
| `.svc-toggle` | Toggle-Switch für Boolean-Config | Optional | `.on` (aktiv), `.warn` (Warnfarbe wenn aktiv) |
| `.svc-toggle-track` | Schiene des Toggles | Pflicht (im Toggle) | — |
| `.svc-toggle-thumb` | Beweglicher Knopf im Track | Pflicht (im Toggle) | — |
| `.svc-toggle-label` | Beschriftung des Toggles | Pflicht (im Toggle) | — |
| `.svc-toggle-sublabel` | Zusatz-/Hilfstext unter dem Toggle-Label | Optional | — |
| `.svc-form-actions` | Aktionsleiste am Formular-Ende | Pflicht | — |
| `.svc-form-hint` | Hinweis in der Aktionsleiste | Optional | — |

### Reihenfolge & Platzierung (G3)

- Zurück-Link steht oben, vor dem Formular.
- **Aktionsleiste (`.svc-form-actions`):** Speichern zuerst als `btn btn-primary`
  (Disketten-Icon `fa-floppy-disk`), direkt daneben Abbrechen als `btn btn-ghost`. Ein
  optionaler `.svc-form-hint` folgt rechts. (Projektweite Konvention: primär zuerst,
  sekundär als Ghost daneben.)

---

## Zustände & Varianten (G4)

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Dienst online | `.card-status-dot.online`, `.svc-status-line.online`, `.badge-green` | Dienst erreichbar/läuft |
| Dienst offline | `.card-status-dot.offline`, `.svc-status-line.offline`, `.badge-red` | Dienst nicht erreichbar |
| Dienst unbekannt | `.card-status-dot.unknown`, `.svc-status-line.unknown`, `.sidebar-status-dot.unknown`, `.badge-yellow` | Status nicht ermittelbar |
| Datenwert positiv | `.svc-data-value.success` | Wert ist im Soll-Zustand (z. B. „Gültig") |
| Datenwert negativ | `.svc-data-value.danger` | Wert signalisiert Fehler/Ausfall |
| Toggle aktiv | `.svc-toggle.on` | Boolean-Config ist eingeschaltet |
| Toggle aktiv mit Warnung | `.svc-toggle.warn` | Eingeschalteter Zustand ist riskant (Warnfarbe) |
| Feld schreibgeschützt | `.svc-field-readonly` | Wert anzeigen, aber nicht editierbar |

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-07 | Auf `docs/doc-standard.md` gehoben (G1–G4, interpretationsfrei). Toggle-Teile inkl. `.svc-toggle-sublabel` ergänzt, Button-Platzierung und Zustände-Tabelle ausformuliert. |
| 2026-06-07 | Initiale Definition. 3 Seiten. svc-* Klassen. Feldtypen-Palette. |

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

Zeigt alle Dienste eines Pi als Kacheln im Card-Grid. Kacheln existieren in zwei Varianten:
**klickbar** (Link zur Detail-Seite) und **nicht klickbar** (kein Link, keine Detail-Seite vorhanden).

### Verschachtelung (G2)

```text
.card-grid
├── a.card.card-dashboard.card-dashboard-link        (klickbare Variante — Optional)
│   ├── div.card-status-dot[.online|.offline|.unknown]   (Pflicht)
│   ├── h3
│   │   ├── i.svc-card-icon                               (Optional)
│   │   └── span (Titel-Text)                             (Pflicht)
│   ├── p.svc-info-line                                   (Optional)
│   ├── span.svc-status-line[.online|.offline|.unknown]   (Pflicht)
│   └── i.card-dashboard-arrow                            (Optional, nur klickbare Variante)
└── div.card.card-dashboard                          (nicht klickbare Variante — Optional)
    ├── div.card-status-dot[.online|.offline|.unknown]   (Pflicht)
    ├── h3
    │   ├── i.svc-card-icon                               (Optional)
    │   └── span (Titel-Text)                             (Pflicht)
    ├── p.svc-info-line                                   (Optional)
    └── span.svc-status-line[.online|.offline|.unknown]   (Pflicht)
```

### Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.card-grid` | Grid-Container der Kacheln (aus `cards.css`) | Pflicht | — |
| `.card.card-dashboard` | Dienst-Kachel (aus `cards.css`); Basis für beide Varianten | Pflicht | — |
| `.card-dashboard-link` | Zusatzklasse auf `<a>` für klickbare Variante (aus `cards.css`) | Optional | — |
| `.card-status-dot` | Status-Punkt oben in der Kachel (aus `cards.css`) | Pflicht | `.online`, `.offline`, `.unknown` |
| `.svc-card-icon` | FA-Icon inline im h3-Titel (accent, 0.85rem, flex-shrink:0) | Optional | — |
| `.svc-info-line` | Kurzbeschreibung unter Titel (0.75rem, muted) | Optional | — |
| `.svc-status-line` | Statuszeile unten (0.7rem) | Pflicht | `.online`, `.offline`, `.unknown` |
| `.card-dashboard-arrow` | Pfeil-Icon rechts — nur in klickbarer Variante (aus `cards.css`) | Optional | — |

### Reihenfolge & Platzierung (G3)

- **Klickbare Variante** (`<a>` als Wurzel): Reihenfolge Status-Dot → h3 (Icon, dann Titel) →
  Info-Zeile → Status-Zeile → Pfeil-Icon. Das Pfeil-Icon (`.card-dashboard-arrow`) ist das letzte
  Kind; es zeigt visuell an, dass die Kachel zu einer Detail-Seite führt.
- **Nicht klickbare Variante** (`<div>` als Wurzel): gleiche Reihenfolge ohne `.card-dashboard-link`
  und ohne `.card-dashboard-arrow`. Verwenden, wenn für diesen Dienst keine Detail-Seite existiert.
- Wenn `.svc-card-icon` im h3 verwendet wird, MUSS der Textteil in `<span>` stehen, damit
  Truncation korrekt funktioniert.

---

## Seite 2 — Detail (Seitentyp 1: Detail-Seite)

### Verschachtelung (G2)

```text
.page-header
├── .page-header-left
│   ├── .svc-page-title-row      (Icon + Titel + Badge auf einer Linie)      (Pflicht)
│   │   ├── i.svc-page-icon                                                  (Pflicht)
│   │   ├── h1.page-title                                                    (Pflicht)
│   │   └── span.badge.badge-*   (Statusbadge, z. B. badge-green)           (Optional)
│   └── p.page-subtitle          (Subtitle, Geschwister von .svc-page-title-row) (Optional)
└── .page-header-right
    ├── button.btn.btn-danger     (destruktive Aktion, z. B. Neustart)       (Optional)
    └── a.btn.btn-secondary       (Navigation, z. B. Config)                 (Optional)

.content-body
├── .panel                                                                   (Pflicht, n×)
│   ├── .panel-header
│   │   ├── .panel-title         (Icon + Bezeichnung)
│   │   └── .panel-header-right
│   │       └── span.panel-meta  (z. B. Zeitstempel, Badge)                 (Optional)
│   └── .panel-body
│       └── .svc-data-grid
│           └── .svc-data-cell                                               (Pflicht, n×)
│               ├── span.svc-data-label                                      (Pflicht)
│               ├── span.svc-data-value[.success|.danger]                   (Pflicht)
│               └── span.svc-data-sub                                        (Optional)
└── div.card-warn                (Hinweis bei destruktiven Aktionen)         (Optional)
```

### Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.svc-page-title-row` | Flex-Wrapper für Icon, Titel und Badge im Page-Header; setzt auch die Größe von `.page-title` (1.2rem, 600) | Pflicht | — |
| `.svc-page-icon` | FA-Icon im Page-Header der Detailseite | Pflicht | — |
| `.svc-data-grid` | Responsive Grid: 3/2/1 Spalten (Desktop/Tablet/Mobile) | Pflicht | — |
| `.svc-data-cell` | Einzelne Zelle: panel-deep Hintergrund, 8px Radius | Pflicht | — |
| `.svc-data-label` | Bezeichnung (0.68rem, uppercase, `--subtle`) | Pflicht | — |
| `.svc-data-value` | Wert (0.95rem, 600, `--text`) | Pflicht | `.success`, `.danger` |
| `.svc-data-sub` | Subtext (0.72rem, `--muted`) | Optional | — |
| `.card-warn` | Warnbox für destruktive Aktionen (gelber Warn-Hinweis) | Optional | — |

Bestehende Klassen (aus `page.css`): `.page-header`, `.page-header-left`, `.page-header-right`,
`.page-title`, `.page-subtitle`, `.panel`, `.panel-header`, `.panel-title`,
`.panel-header-right`, `.panel-body`, `.panel-meta`.
Weitere bestehende Klassen: `.badge.badge-green/red/yellow`, `.btn.btn-danger`,
`.btn.btn-secondary`.

### Reihenfolge & Platzierung (G3)

- **Header links:** Icon, Titel und Status-Badge sitzen gemeinsam in `.svc-page-title-row`
  (erste Ebene unterhalb `.page-header-left`). Diese Klasse sorgt dafür, dass Icon, `h1` und Badge
  auf einer horizontalen Linie ausgerichtet sind und setzt gleichzeitig die Schriftgröße von
  `.page-title` auf 1.2rem/600. Die optionale Subtitle (`p.page-subtitle`) ist ein
  Geschwisterelement von `.svc-page-title-row`, also ein zweites direktes Kind von `.page-header-left`.
- **Header rechts:** Aktions-Buttons. Destruktive Aktionen (Restart) als `btn-danger`,
  Navigation (Config) als `btn-secondary`. Destruktive Aktion zuerst, Navigation danach.
- Nur API-Endpunkte/Aktionen einblenden, die tatsächlich vorhanden sind. Destruktive
  Aktionen immer mit `confirm()` absichern.
- `.card-warn` folgt unmittelbar nach dem Panel mit den Daten und dient als Hinweis,
  dass die destruktive Aktion (z. B. Neustart) Konsequenzen hat.

### Inhalt & Semantik

**Ein Endpunkt pro Seite:** Eine Detailseite zeigt **genau einen Dienst/Endpunkt**.
Alle Panels der Seite beziehen sich auf diesen einen Endpunkt; mehrere Dienste werden
**nie** auf einer Detailseite gemischt — jeder Dienst hat seine eigene Detailseite,
der Wechsel erfolgt über die Sidebar. (Die „Variante – Dienst offline" in
`components/service-dashboard-detail.html` ist eine Zustands-Demo, kein zweiter Dienst.)

**Festes Set an Panel-Typen:** Jede Kachel (`.panel`) muss **genau einem** der
folgenden Typen entsprechen — andere Panel-Typen sind nicht zulässig:

| Panel-Typ | Inhalt | Pflicht/Optional |
|---|---|---|
| **Live-Status** | Echtzeit-Laufzeitwerte, per JS aktualisiert (z. B. GPS-Fix, Geschwindigkeit, nächste TX, Payload, Dienst aktiv) | Pflicht (mind. 1 pro Seite) |
| **Verbindung / Endpoint** | Statische Verbindungsdaten: Host, Port, Protokoll, URL, letzter Kontakt | Optional |
| **Konfiguration (read-only)** | Aktuell geladene Einstellungen nur zur Anzeige; Ändern erfolgt über die Config-Seite | Optional |
| **Diagnose / Fehler** | Letzte Fehler, Warnungen, Diagnosehinweise | Optional |

**Zellen-Regel:** Ein Wert = eine `.svc-data-cell` (Label / Wert / optional Subtext).
Eine Zelle enthält keinen zusammengesetzten oder mehrwertigen Inhalt — mehrere Werte
werden auf mehrere Zellen aufgeteilt.

---

## Seite 3 — Config (Seitentyp 1: Detail-Seite)

Der Page-Header enthält auf der Config-Seite `.svc-page-title-row` (erste Ebene unter
`.page-header-left`) mit Icon und h1, aber kein Badge (da kein Live-Status gezeigt wird).

### Verschachtelung (G2)

```text
.content-body
├── a.svc-back-link                                                          (Pflicht)
├── .panel                                 (ein oder mehrere Panels)        (Pflicht, n×)
│   ├── .panel-header
│   │   ├── .panel-title                   (Icon + Bezeichnung)
│   │   └── span.panel-meta               (Typ-Hinweis, z. B. „Text · Zahl") (Optional)
│   └── .panel-body
│       └── .svc-field-grid[.svc-field-grid--cols-3]  (Grid-Wrapper bei ≥2 Feldern)  (s. Hinweis)
│           └── .svc-field                                                   (Pflicht, n×)
│               ├── label
│               ├── input | select | textarea | .svc-field-readonly
│               │   (oder .svc-secret | .svc-input-prefix als Wrapper)
│               └── span.svc-field-hint                                      (Optional)
└── .svc-form-actions                                                        (Pflicht)
    ├── button.btn.btn-primary   (Speichern, fa-floppy-disk)                 (Pflicht)
    ├── a.btn.btn-ghost          (Abbrechen)                                 (Pflicht)
    └── span.svc-form-hint       (Hinweis, z. B. Neustart-Erfordernis)      (Optional)
```

**Hinweis (Einzelfeld):** Enthält ein Panel nur ein einzelnes, volle Breite nutzendes Feld
(z. B. eine JSON-Textarea), entfällt der `.svc-field-grid`-Wrapper — die `.svc-field` sitzt dann
direkt im `.panel-body`. Der Grid-Wrapper ist nur ab zwei Feldern erforderlich.

Toggle-Struktur (innerhalb von `.svc-field-grid` im Panel-Body, als Alternative zu `.svc-field`):

```text
.svc-toggle[.on][.warn]
├── .svc-toggle-track                                                        (Pflicht)
│   └── .svc-toggle-thumb                                                    (Pflicht)
└── div  (Beschriftungs-Wrapper-div, Geschwister von .svc-toggle-track)      (Pflicht)
    ├── .svc-toggle-label                                                    (Pflicht)
    └── .svc-toggle-sublabel                                                  (Optional)
```

### Feldtypen / Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.svc-back-link` | Zurück-Navigation oben (mit `fa-arrow-left`) | Pflicht | — |
| `.svc-field-grid` | Grid-Wrapper für Feldgruppen im Panel-Body (2-Spalten-Grid); Struktur: `.panel-body > .svc-field-grid > .svc-field`. Bei einzelnem volle-Breite-Feld entfällt der Wrapper. | Pflicht ab ≥2 Feldern | `.svc-field-grid--cols-3` |
| `.svc-field-grid--cols-3` | Modifier: 3-Spalten-Grid statt 2 (z. B. für Toggle-Felder) | Optional | — |
| `.svc-label-type` | Typ-Hinweis im Label (z. B. „(Text)", „(Zahl)"); schriftgewicht 400, Farbe `--subtle` | Optional | — |
| `.svc-field-code` | Code/JSON-Textarea: Monospace-Font (`--font-mono`), 0.8rem, Farbe `--code-text`, vertikal resizable | Optional | — |
| `.svc-field` | Standard-Feld: `<input text/number>`, `<select>`, `<textarea>` | Pflicht (je Feld) | — |
| `.svc-field-readonly` | Read-only-Wert als `<div>` statt Input | Optional | — |
| `.svc-field-hint` | Hilfstext unter einem Feld (`<span>`) | Optional | — |
| `.svc-secret` | Wrapper für Passwort-Feld mit Auge-Toggle | Optional | — |
| `.svc-secret-toggle` | Sichtbarkeits-Umschalter im Secret-Feld | Optional | — |
| `.svc-input-prefix` | Wrapper für Input mit Protokoll-Prefix; der innere `<input>` erhält `.mono` (Monospace, aus `typography.css`) | Optional | — |
| `.svc-input-prefix-label` | Prefix-Label (z. B. `https://`) | Optional | — |
| `.svc-toggle` | Toggle-Switch für Boolean-Config | Optional | `.on` (aktiv, Track grün), `.warn` (Sublabel in Warnfarbe; Track-Warnfarbe nur zusammen mit `.on`) |
| `.svc-toggle-track` | Schiene des Toggles | Pflicht (im Toggle) | — |
| `.svc-toggle-thumb` | Beweglicher Knopf im Track | Pflicht (im Toggle) | — |
| `.svc-toggle-label` | Beschriftung des Toggles | Pflicht (im Toggle) | — |
| `.svc-toggle-sublabel` | Zusatz-/Hilfstext unter dem Toggle-Label | Optional | — |
| `.svc-form-actions` | Aktionsleiste am Formular-Ende | Pflicht | — |
| `.svc-form-hint` | Hinweis in der Aktionsleiste | Optional | — |

Bestehende Klassen (aus `page.css`): `.panel`, `.panel-header`, `.panel-title`, `.panel-body`,
`.panel-meta`. (`.panel-header-right` wird auf der Config-Seite nicht verwendet — dort steht
`span.panel-meta` direkt im `.panel-header` als Geschwister von `.panel-title`.)
`.panel-title` (Icon + Bezeichnung) ist auf der Config-Seite **Pflicht je Panel** — auch
bei einem Panel mit nur einem Feld (siehe „Inhalt & Semantik").

### Reihenfolge & Platzierung (G3)

- Zurück-Link steht als erstes Kind von `.content-body`, vor allen Panels.
- Felder sind in Panels gruppiert. Innerhalb von `.panel-body` sitzt `.svc-field-grid`, der alle
  `.svc-field`-Elemente (oder Toggle-Elemente) des jeweiligen Panels enthält. Toggle-Felder
  verwenden `.svc-field-grid.svc-field-grid--cols-3` (3-Spalten-Variante).
- In jedem `.svc-toggle` folgt auf `.svc-toggle-track` ein namenloser `div`, der
  `.svc-toggle-label` und optional `.svc-toggle-sublabel` enthält. Diese Labels sind damit NICHT
  direkte Kinder von `.svc-toggle`, sondern Enkel.
- **Aktionsleiste (`.svc-form-actions`):** Speichern zuerst als `btn btn-primary`
  (Disketten-Icon `fa-floppy-disk`), direkt daneben Abbrechen als `btn btn-ghost`. Ein
  optionaler `.svc-form-hint` folgt rechts. (Projektweite Konvention: primär zuerst,
  sekundär als Ghost daneben.)
- `.svc-form-actions` ist letztes Kind von `.content-body`, nach allen Panels.

### Inhalt & Semantik

**Gruppierung nach Kategorien (offenes Prinzip):** Einstellungen werden thematisch in
Panels („Kategorien") gruppiert. Dienste wählen die passenden Kategorien selbst — es gibt
keine geschlossene Liste. Empfohlene Beispiel-Kategorien: **Allgemein, Verbindung,
Authentifizierung, Erweitert**. Reihenfolge: allgemeine/häufig genutzte Kategorien zuerst,
„Erweitert" bzw. riskante Einstellungen zuletzt.

**Pflicht-Überschrift je Panel:** Jedes Config-Panel **muss** eine Überschrift
(`.panel-title` mit Icon + Bezeichnung) enthalten — auch wenn das Panel nur ein einzelnes
Feld hat.

---

## Zustände & Varianten (G4)

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Dienst online | `.card-status-dot.online`, `.svc-status-line.online`, `.sidebar-status-dot.online`, `.badge-green` | Dienst erreichbar/läuft |
| Dienst offline | `.card-status-dot.offline`, `.svc-status-line.offline`, `.sidebar-status-dot.offline`, `.badge-red` | Dienst nicht erreichbar |
| Dienst unbekannt | `.card-status-dot.unknown`, `.svc-status-line.unknown`, `.sidebar-status-dot.unknown`, `.badge-yellow` | Status nicht ermittelbar |
| Datenwert positiv | `.svc-data-value.success` | Wert ist im Soll-Zustand (z. B. „Gültig") |
| Datenwert negativ | `.svc-data-value.danger` | Wert signalisiert Fehler/Ausfall |
| Toggle inaktiv | kein Modifier (Default-/Aus-Zustand) | Boolean-Config ist ausgeschaltet |
| Toggle aktiv | `.svc-toggle.on` | Boolean-Config ist eingeschaltet |
| Toggle aktiv mit Warnung | `.svc-toggle.warn.on` | Eingeschalteter Zustand ist riskant (Warnfarbe) |
| Feld schreibgeschützt | `.svc-field-readonly` | Wert anzeigen, aber nicht editierbar |

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-08 | Inhaltlich-semantische Regeln ergänzt: Detail-Seite „Inhalt & Semantik" (Ein-Endpunkt-Regel, festes Panel-Typen-Set, Zellen-Regel); Config-Seite „Inhalt & Semantik" (Kategorien-Gruppierung als offenes Prinzip, `.panel-title` als Pflicht je Panel). |
| 2026-06-07 | Layout-Inline-Styles durch CI-Klassen ersetzt: `.svc-page-title-row` (Detail+Config Page-Header), `.svc-field-grid` + `.svc-field-grid--cols-3` (Config Panel-Body), `.svc-label-type` (Label-Typ-Hinweise), `.svc-field-code` (JSON-Textarea); G2-Bäume und G3-Text aktualisiert. |
| 2026-06-07 | Strukturkorrekturen: Panel-Verschachtelung für svc-data-grid dokumentiert; Flex-Wrapper-div in page-header-left für Detail+Config; Toggle-Beschriftungs-Wrapper-div; nicht-klickbare Kachel-Variante (div.card.card-dashboard); card-dashboard-link/arrow als Optional; card-warn ergänzt; 2-Spalten-Grid-div in Panel-Body; panel-Klassen in G1-Hinweis; G4 um sidebar-status-dot.online/offline und Toggle-inaktiv-Zeile ergänzt. |
| 2026-06-07 | Auf `docs/doc-standard.md` gehoben (G1–G4, interpretationsfrei). Toggle-Teile inkl. `.svc-toggle-sublabel` ergänzt, Button-Platzierung und Zustände-Tabelle ausformuliert. |
| 2026-06-07 | Initiale Definition. 3 Seiten. svc-* Klassen. Feldtypen-Palette. |

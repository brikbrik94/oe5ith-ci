# Seitentypen — Entscheidungshilfe

**CSS:** `css/page.css`  
**Status:** definiert · v1.0

---

## Überblick

Fünf definierte Seitentypen. Jeder Typ hat eine klare Struktur und einen
bestimmten Anwendungsfall. Wenn keine der fünf Varianten passt, ist ein
neues Design erforderlich.

---

## Entscheidungsbaum

```
Hat die Seite eine Sidebar?
│
├── NEIN → Typ 5: Landing
│
└── JA
    │
    ├── Ist der Hauptinhalt eine Karte (Leaflet/MapLibre)?
    │   └── JA → Karten-Seite (eigene Regeln, kein page.css)
    │
    ├── Gibt es mehrere thematische Spalten nebeneinander?
    │   └── JA → Typ 4: Karten-Grid
    │
    ├── Ist der Hauptinhalt eine Datentabelle oder Feed?
    │   └── JA → Typ 2: Listen-Seite
    │
    ├── Gibt es nur einen Titel und dann direkt Cards?
    │   └── JA → Typ 3: Dashboard
    │
    └── Gibt es strukturierte Panels mit Formular/Code/Status?
        └── JA → Typ 1: Detail-Seite
```

---

## Typ 1 — Detail-Seite

**Beispiele:** Geocoding API, SDR Spectrum, SDR POCSAG (Eingabe + Inhalt), Routing API

**Wann verwenden:**
Die Seite zeigt detaillierte Informationen zu einem einzelnen Dienst oder Thema.
Es gibt mehrere inhaltliche Abschnitte (Panels) mit unterschiedlichem Inhalt:
Eingabefelder, Code-Blöcke, Status-Anzeigen, Live-Daten.

**Struktur:**
```
Topbar
└── Layout
    ├── Sidebar
    └── page-content
        ├── page-header          ← Titel + Untertitel + optionale Meta/Action
        └── content-body
            ├── Panel 1          ← z.B. Service Information / Eingabe
            ├── Panel 2          ← z.B. Code-Beispiele / Endpoints
            └── Panel 3          ← z.B. Live-Status / Ergebnisse
```

**Merkmale:**
- Page-Header mit Titel **und** Untertitel (kurze Beschreibung des Dienstes)
- Meta-Info rechts (z.B. letzter Refresh, Version)
- Optionaler `page-action` Button rechts (z.B. "Aktualisieren")
- Panels mit eigenem Header + Icon
- Panels können Formulare, Code-Blöcke, Tabellen, Status-Indikatoren enthalten

**Nicht geeignet wenn:**
- Der Inhalt hauptsächlich eine große Datentabelle ist → Typ 2
- Es keine strukturierten Abschnitte gibt → Typ 3

---

## Typ 2 — Listen-Seite

**Beispiele:** POCSAG Feed (Nachrichtenliste), zukünftige Log-Seiten, Ereignis-Listen

**Wann verwenden:**
Der Hauptinhalt ist eine scrollbare Datentabelle oder Liste mit vielen gleichartigen
Einträgen. Es gibt optional ein Eingabe-Panel oben (Filter, Frequenz etc.) und dann
direkt die Tabelle.

**Struktur:**
```
Topbar
└── Layout
    ├── Sidebar
    └── page-content
        ├── page-header          ← Titel + Untertitel + Zeitstempel rechts
        └── content-body
            ├── Panel (optional) ← Filter / Eingabe / Konfiguration
            └── Panel            ← Tabelle (panel-body-flush + ci-table)
```

**Merkmale:**
- Page-Header mit Zeitstempel rechts (wann zuletzt aktualisiert)
- Optionaler `page-action` Button "Aktualisieren" / "Exportieren"
- Tabelle nimmt den meisten Platz ein
- Tabelle in `.panel-body-flush` (kein inneres Padding)
- Erste Spalte ist Primärwert (`--text`), restliche Spalten in `--muted`
- Mono-Spalten für Timestamps, IDs, Frequenzen

**Nicht geeignet wenn:**
- Die Tabelle sehr wenige Spalten hat und es viel anderen Inhalt gibt → Typ 1
- Es keine Tabelle gibt, sondern Cards → Typ 3 oder 4

---

## Typ 3 — Dashboard

**Beispiele:** System Overview (internal.oe5ith.at), Service-Status-Übersicht

**Wann verwenden:**
Die Seite gibt einen schnellen Überblick über den Systemzustand.
Der Inhalt sind primär Cards in einem Grid — jede Card repräsentiert
einen Dienst, eine Ressource oder einen Status.

**Struktur:**
```
Topbar
└── Layout
    ├── Sidebar
    └── page-content
        ├── page-header          ← Nur Titel, kein Untertitel
        └── content-body
            └── Card-Grid        ← Dashboard-Cards (Typ 2 aus cards.css)
```

**Merkmale:**
- Page-Header nur mit Titel — kein Untertitel, keine Meta-Info
- Cards direkt ohne Panel-Wrapper (kein extra Container-Kasten)
- Cards haben Status-Dot (online/offline)
- Klickbare Cards verlinken auf Detail-Seiten (Typ 1)
- Kein Panel-Header nötig

**Nicht geeignet wenn:**
- Es neben den Cards noch andere strukturierte Inhalte gibt → Typ 1
- Die Cards thematisch in Gruppen unterteilt sind → Typ 4

---

## Typ 4 — Karten-Grid (Column-Groups)

**Beispiele:** Tiles Registry (Vektorkarten), Font-Galerie, Sprites-Übersicht

**Wann verwenden:**
Der Inhalt lässt sich in 2–4 thematische Spalten aufteilen, die nebeneinander
angezeigt werden. Jede Spalte hat eine eigene Überschrift und enthält Cards
des gleichen Typs.

**Struktur:**
```
Topbar
└── Layout
    ├── Sidebar
    └── page-content
        ├── page-header          ← Titel, kein Untertitel
        └── content-body
            └── col-groups col-groups-3
                ├── col-group    ← Überschrift "Basemap" + Cards
                ├── col-group    ← Überschrift "Overlay" + Cards
                └── col-group    ← Überschrift "Elevation" + Cards
```

**Merkmale:**
- Spaltenüberschriften (`.col-group-label`) als H2-Equivalent
- Cards in jeder Spalte sind gleichartig (gleicher Typ)
- Breite Spalten (`col-groups-3` für 3 Kategorien)
- Auf Tablet: 2 Spalten, auf Mobile: 1 Spalte (automatisch)

**Nicht geeignet wenn:**
- Die Spalten unterschiedlich viele oder unterschiedliche Card-Typen haben
- Es mehr als 4 Kategorien gibt → lieber Tabs oder Filter überlegen

---

## Typ 5 — Landing Page

**Beispiele:** cloud.oe5ith.at Portal-Übersicht

**Wann verwenden:**
Einstiegsseite ohne Sidebar. Zeigt die verfügbaren Bereiche/Dienste als
Navigation-Cards. Zentrierter Inhalt, maximale Breite begrenzt.

**Struktur:**
```
Topbar
└── landing-body (zentriert)
    ├── landing-title            ← "Willkommen im Cloud Portal"
    ├── card-grid                ← Navigation-Cards (Typ 1 aus cards.css)
    └── Footer (optional)        ← Versioninfo, Copyright
```

**Merkmale:**
- Kein `.layout`, keine Sidebar
- Inhalt zentriert mit `max-width: 860px`
- `padding-top: 60px` — mehr Luft nach der Topbar als bei anderen Typen
- Nav-Cards mit Icon + Titel + Beschreibung + Button
- Disabled-Cards für noch nicht verfügbare Bereiche

**Nicht geeignet wenn:**
- Es nach dem Login weitere Navigation gibt → Typ 3 (Dashboard)

---

## Karten-Seite (Sonderfall)

**Beispiele:** karte.oe5ith.at, vector-map-test, Routing-Karte

**Wann verwenden:**
Die Karte (Leaflet/MapLibre) ist der Hauptinhalt und füllt den gesamten
verfügbaren Bereich. Die Sidebar enthält Layer-Controls (Accordion).

**Besonderheiten:**
- `page.css` wird **nicht** verwendet — kein Page-Header, kein Content-Body
- Die Karte füllt `flex: 1` im Layout direkt aus
- Sidebar enthält Accordion-Gruppen statt Nav-Items
- Topbar enthält Controls-Panel (Dropdown, Toggles)
- Leaflet/MapLibre CSS-Overrides aus `modal.css` aktivieren

**Struktur:**
```
Topbar (mit Controls-Panel: Kartentyp, Zoom, Legende, Labels)
└── Layout
    ├── Sidebar (Accordion-Layer-Steuerung)
    └── Karten-Container (height: 100%, width: 100%)
```

---

## Schnellreferenz

| Ich brauche... | Typ |
|---|---|
| Übersicht aller Dienste beim Login | 5 — Landing |
| Status aller Services auf einen Blick | 3 — Dashboard |
| Details zu einem einzelnen Dienst/Tool | 1 — Detail |
| Lange Liste von Einträgen / Feed | 2 — Listen |
| Katalog mit thematischen Gruppen | 4 — Karten-Grid |
| Interaktive Karte als Hauptinhalt | Karten-Sonderfall |
| Keines davon passt | Neues Design erforderlich |

---

## Neues Design erforderlich wenn...

- Der Inhalt in zwei gleichwertige Hälften aufgeteilt ist (Split-View)
- Es eine Step-by-Step Wizard-Logik gibt
- Der Inhalt primär aus Diagrammen / Charts besteht
- Es eine vollständige Einstellungsseite mit Kategorien ist (Settings-Pattern)
- Die Seite einen eigenen Login/Auth-Flow hat

In diesen Fällen: neuen Seitentyp als `docs/page-<name>.md` anlegen und
das bestehende Basis-CSS (`common.css`, `topbar.css`, `sidebar.css`) wiederverwenden.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-24 | Initiale Definition. 5 Typen + Karten-Sonderfall. Entscheidungsbaum. Schnellreferenz. |

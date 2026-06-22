# Seitentypen — Entscheidungshilfe

**CSS:** `css/page.css`  
**Status:** definiert · v1.0

---

## Überblick

Sieben definierte Seitentypen. Jeder Typ hat eine klare Struktur und einen
bestimmten Anwendungsfall. Wenn keine der sieben Varianten passt, ist ein
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
    ├── Ist der Hauptinhalt eine konfigurierbare Statistik-Tabelle mit Steuer-Feld
    │   (Tabellenwahl + Zeitraum)?
    │   └── JA → Typ 7: Statistik-Explorer
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
    └── page-footer              ← Version · Copyright · Links (Pflicht)
        ├── page-footer-version  ← CI-Version, z.B. "CI v2.0.0"
        ├── page-footer-copy     ← "© 2026 OE5ITH"
        └── page-footer-links    ← Impressum, Datenschutz
```

**Merkmale:**
- Kein `.layout`, keine Sidebar
- Inhalt zentriert mit `max-width: 860px`
- `padding-top: 60px` — mehr Luft nach der Topbar als bei anderen Typen
- Nav-Cards mit Icon + Titel + Beschreibung + Button
- Disabled-Cards für noch nicht verfügbare Bereiche
- `.page-footer` mit Version, Copyright-Text und Links ist **Pflicht** — kein optionaler Baustein

**Nicht geeignet wenn:**
- Es nach dem Login weitere Navigation gibt → Typ 3 (Dashboard)

---

## Typ 6 — Split-View (Master-Detail)

**Beispiele:** Log-Explorer, Alarm-/Event-Listen, Geräteverwaltung, Ressourcenlisten mit Detailansicht

**Wann verwenden:**
Der Inhalt besteht aus einer scrollbaren Auswahlliste (Master) und einem abhängigen
Detailbereich (Detail), die nebeneinander angezeigt werden. Der Nutzer wählt aus der
Master-Liste einen Eintrag aus und sieht das Ergebnis sofort im Detailbereich —
ohne Seitenneuladen. Beide Spalten scrollen unabhängig voneinander.

**Struktur:**
```
Topbar
└── Layout
    ├── Sidebar
    └── page-content
        ├── page-header          ← Titel + Untertitel + optionale Aktion
        └── content-body
            └── split-view       ← einziges direktes Kind von content-body
                ├── split-master ← linke Spalte: scrollbare Auswahlliste
                │   ├── split-master-header  (Optional — Titel, Aktions-Buttons)
                │   └── split-master-body
                │       └── split-item [.active]
                │           ├── status-dot [.on|.warn|.off]  (Optional)
                │           ├── split-item-label
                │           └── split-item-meta              (Optional)
                └── split-detail ← rechte Spalte: Panels, Tabellen, etc.
```

**Merkmale:**
- Der Fixed-Height-Modus aktiviert sich **automatisch** sobald `.split-view` im DOM vorhanden ist — kein zusätzliches Klassen-Markup am Seiten-Wrapper nötig.
- `css/split.css` zusätzlich zu `css/page.css` einbinden.
- `.split-view` ist das **einzige direkte Kind** von `.content-body`.
- Auf Mobile (≤ 768 px) werden Master und Detail automatisch gestapelt.
- Komponenten-Doku: `docs/split-view.md`

**Nicht geeignet wenn:**
- Es keine persistente Auswahlliste gibt → Typ 1 (Panel-Stapel)
- Der Hauptinhalt nur eine einzelne Tabelle ohne Selektion ist → Typ 2

---

## Typ 7 — Statistik-Explorer

**Beispiele:** Alarmierungsstatistik, Empfangsstatistik, Nutzungsauswertung

**Wann verwenden:**
Der Hauptinhalt ist eine einzelne, sortierbare Datentabelle, die über ein fixiertes
Steuer-Feld konfiguriert wird (Tabellenwahl, Zeitraum-Preset, optionaler Freitext-Filter).
Das Steuer-Feld bleibt stets sichtbar am oberen Rand; nur die Tabelle scrollt in sich.

**Struktur:**
```
Topbar
└── Layout
    ├── Sidebar
    └── page-content
        ├── page-header          ← Titel + Untertitel
        └── content-body
            └── stats-explorer   ← einziges direktes Kind von content-body
                ├── stats-controls          ← Steuer-Feld (fix oben)
                │   ├── stats-control-group ← Tabellenwahl (form-select)
                │   ├── stats-control-group ← Zeitraum (segmented + date inputs)
                │   ├── stats-control-group.stats-search  ← Filter (form-input)
                │   └── stats-actions       ← Aktions-Buttons (Aktualisieren, Export)
                └── section.panel.stats-table-panel
                    └── panel-body-flush--scroll
                        └── table.ci-table.ci-table--sortable   (oder .stats-empty)
```

**Merkmale:**
- Der Fixed-Height-Modus aktiviert sich **automatisch**, sobald `.stats-explorer` im DOM vorhanden ist — kein zusätzliches Klassen-Markup am Seiten-Wrapper nötig.
- `css/stats.css` zusätzlich zu `css/page.css`, `css/forms.css` und `css/buttons.css` einbinden.
- `.stats-explorer` ist das **einzige direkte Kind** von `.content-body`.
- Sortierung, Filterung und Datenwechsel liegen vollständig in der Verantwortung des seiteneigenen JavaScript.
- Auf Mobile (≤ 768 px) wechselt `.stats-controls` auf `flex-direction: column`.
- Komponenten-Doku: `docs/page-stats.md`

**Nicht geeignet wenn:**
- Die Tabelle keine Steuerfeld-Konfiguration benötigt → Typ 2 (Listen-Seite)
- Es mehrere unabhängige Tabellen nebeneinander gibt → Typ 4 oder Typ 1
- Ein Master-Detail-Pattern benötigt wird → Typ 6 (Split-View)

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
- Native MapLibre/Leaflet-Attribution bleibt aktiv (kein CSS-Override nötig)
- `.sidebar-footer-copyright`-Button für weiterführende Lizenzinfos nutzen

**Struktur:**
```
Topbar (mit Controls-Panel: Kartentyp, Zoom, Legende, Labels)
└── Layout
    ├── Sidebar (Accordion-Layer-Steuerung)
    └── Karten-Container (height: 100%, width: 100%)
```

---

## Footer- und Copyright-Regeln

| Seitentyp | Sidebar | Copyright-Anzeige |
|---|---|---|
| Typ 1–4, Typ 6–7 | Pflicht | Sidebar-Footer: Version + `.sidebar-footer-copyright`-Button |
| Typ 5 — Startseite | Nicht vorhanden | `.page-footer` mit Version, Copyright-Text, Links |
| Karten-Sonderfall | Pflicht (auch wenn leer) | Sidebar-Footer + native MapLibre/Leaflet-Attribution |

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
| Master-Detail / Split-View | Typ 6 |
| Konfigurierbare Statistik-Tabelle (Wahl + Zeitraum) | 7 |
| Keines davon passt | Neues Design erforderlich |

---

## Neues Design erforderlich wenn...

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
| 2026-06-22 | Typ 7 — Statistik-Explorer ergänzt. Entscheidungsbaum + Schnellreferenz aktualisiert. |
| 2026-06-18 | Typ 6 — Split-View (Master-Detail) ergänzt. Schnellreferenz + „Neues Design"-Punkt aktualisiert. |
| 2026-05-07 | `.map-attribution`-Verweis entfernt (Breaking: v2.0.0). `.page-footer` als Pflichtbaustein für Typ 5 dokumentiert. Footer/Copyright-Regeltabelle ergänzt. |
| 2026-04-24 | Initiale Definition. 5 Typen + Karten-Sonderfall. Entscheidungsbaum. Schnellreferenz. |

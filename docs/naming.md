# Naming

Diese Datei definiert die bevorzugten Namen, Schreibweisen und Bezeichnungen für OE5ITH-Webseiten und Dienste.

Ziel ist, dass sichtbare Namen in UI, Dokumentation, Navigation und Footer einheitlich verwendet werden.

---

## Grundregel

Im sichtbaren UI-Kontext wird die Marke immer als `OE5ITH` geschrieben.

```text
OE5ITH
```

Technische Namen wie Domains, Repository-Namen, Pfade oder CSS-Klassen dürfen kleingeschrieben sein.

Beispiele:

| Kontext | Schreibweise |
|---|---|
| sichtbarer Seitenname | `OE5ITH Tiles` |
| Domain | `tiles.oe5ith.at` |
| Repository | `oe5ith-ci` |
| CSS-Klasse | `.oe5ith-card` oder projektspezifisch |
| Pfad | `/assets/oe5ith-ci/` |

---

## Grundschema für Dienstnamen

Sichtbare Dienstnamen folgen grundsätzlich diesem Schema:

```text
OE5ITH <Dienstname>
```

Beispiele:

```text
OE5ITH Cloud Portal
OE5ITH Tiles
OE5ITH Karte
OE5ITH Routing
OE5ITH SDR
OE5ITH Monitoring
```

Der Dienstname soll kurz, verständlich und sprechend sein.

---

## Empfohlene Dienstnamen

| Bereich | Sichtbarer Name | Technischer Bezug / Domain | Verwendung |
|---|---|---|---|
| Zentrales Portal | `OE5ITH Cloud Portal` | `cloud.oe5ith.at` oder Portal-Startseite | Landing Page / Einstieg |
| Interne Übersicht | `OE5ITH Internal` | `internal.oe5ith.at` | interne Service-Übersicht |
| Kartenserver / Tiles | `OE5ITH Tiles` | `tiles.oe5ith.at` | PMTiles, Styles, Fonts, Sprites |
| Kartenanwendung | `OE5ITH Karte` | `karte.oe5ith.at` | interaktive Karte |
| Routing | `OE5ITH Routing` | Routing-/ORS-Endpunkte | Routing-App oder API-Seite |
| SDR | `OE5ITH SDR` | SDR-/OpenWebRX-/SDR++-Dienste | Funk-/SDR-Webseiten |
| Monitoring | `OE5ITH Monitoring` | Grafana, Netdata, Metriken | Status- und Monitoringseiten |
| Auth / SSO | `OE5ITH Login` oder `OE5ITH Auth` | Authentik / Authelia / SSO | Login-/Auth-Kontext |
| NetBird | `OE5ITH NetBird` | `netbird.oe5ith.at` | NetBird-Webinterface |
| CI Repository | `OE5ITH CI` | `oe5ith-ci` | Design-System-/CI-Doku |

---

## Deutsche und englische Begriffe

Die UI darf deutsche und etablierte englische Fachbegriffe mischen, wenn das im technischen Kontext verständlicher ist.

Bevorzugt deutsch:

```text
Karte
Dienste
Status
Einstellungen
Aktualisieren
Letzter Refresh
Keine Daten verfügbar
```

Akzeptierte englische Begriffe:

```text
Dashboard
Sidebar
Topbar
Token
Modal
API
Endpoint
Routing
Monitoring
Login
```

Wichtig ist Konsistenz innerhalb einer Seite.

Nicht innerhalb derselben Seite mischen:

```text
Karte / Map
Dienste / Services
Status / State
Einstellungen / Settings
```

Eine Variante wählen und durchziehen.

---

## Seitentitel

Seitentitel sollen sprechend sein und nicht nur aus Domains bestehen.

Richtig:

```text
OE5ITH Tiles
OE5ITH Karte
OE5ITH Routing
OE5ITH Monitoring
```

Nur technische Domain als Titel vermeiden:

```text
tiles.oe5ith.at
karte.oe5ith.at
ors.oe5ith.at
```

Ausnahme:

Wenn eine Seite explizit einen Endpoint, eine Domain oder einen technischen Pfad dokumentiert, darf dieser sichtbar im Inhalt stehen.

---

## Navigation

In Navigationen sollen kurze Namen verwendet werden.

Beispiele:

```text
Portal
Dienste
Karte
Tiles
Routing
SDR
Monitoring
Login
```

Wenn der OE5ITH-Kontext durch Topbar oder Seitenrahmen klar ist, muss nicht jeder Navigationspunkt mit `OE5ITH` beginnen.

Beispiel:

```text
Topbar: OE5ITH Cloud Portal
Sidebar:
- Übersicht
- Karte
- Tiles
- Routing
- SDR
- Monitoring
```

---

## Technische Bezeichnungen

Technische Namen dürfen sachlich und exakt sein.

Beispiele:

```text
PMTiles
MapLibre
Leaflet
OpenRouteService
OpenWebRX+
SDR++
NetBird
InfluxDB
Grafana
Nginx
```

Diese Namen sollen korrekt geschrieben werden und nicht künstlich eingedeutscht werden.

---

## Domains

Domains werden kleingeschrieben.

Beispiele:

```text
oe5ith.at
tiles.oe5ith.at
karte.oe5ith.at
netbird.oe5ith.at
minecraft.oe5ith.at
```

Domains dürfen in technischen Tabellen, Endpoint-Listen und Codeblöcken direkt angezeigt werden.

Im normalen UI-Titel soll stattdessen ein sprechender Name stehen.

---

## Repository- und Dateinamen

Repository- und Dateinamen bleiben technisch und kleingeschrieben.

Beispiele:

```text
oe5ith-ci
hiking-overlay
README.md
docs/tokens.md
css/common.css
```

Keine Versionen in Dateinamen verwenden.

Richtig:

```text
README.md
docs/usage.md
docs/versioning.md
```

Falsch:

```text
README_v2.md
usage_final.md
tokens_neu.md
```

Versionierung erfolgt über Git-Tags und `CHANGELOG.md`.

---

## Schreibweisen

| Begriff | Korrekt | Nicht verwenden |
|---|---|---|
| OE5ITH | `OE5ITH` | `oe5ith`, `Oe5ith`, `OE5ith` |
| CI | `OE5ITH CI` | `oe5ith ci`, `CI System` ohne Kontext |
| Cloud Portal | `OE5ITH Cloud Portal` | `Cloudportal`, `cloud portal` |
| Tiles | `OE5ITH Tiles` | `Tile Server` als sichtbarer Hauptname |
| Karte | `OE5ITH Karte` | `Map` und `Karte` gemischt |
| Routing | `OE5ITH Routing` | `ORS Seite` als sichtbarer Hauptname |
| SDR | `OE5ITH SDR` | `sdr page` |
| Monitoring | `OE5ITH Monitoring` | `monitoring page` |

---

## Status-Begriffe

Status-Begriffe sollen klar und kurz sein.

Bevorzugt:

```text
Online
Offline
Aktiv
Inaktiv
Warnung
Fehler
Unbekannt
Auth erforderlich
Eingeschränkt
```

Nicht verwenden:

```text
läuft eh
kaputt
geht nicht
okay-ish
vielleicht online
```

Für Farben gelten die semantischen Tokens aus `docs/tokens.md`.

---

## Aktionen

Aktionen sollen als Verben formuliert sein.

Beispiele:

```text
Aktualisieren
Speichern
Abbrechen
Öffnen
Schließen
Kopieren
Exportieren
Zurücksetzen
Anmelden
Abmelden
```

Nicht ideal:

```text
OK
Los
Weiter
Hier klicken
Mach
```

`OK` ist nur für einfache Bestätigungsdialoge sinnvoll.

---

## Tabellen- und Kartenbegriffe

Für Karten- und Geodaten-Kontext bevorzugt:

```text
Karte
Layer
Overlay
Basiskarte
Stil
Quelle
Attribution
Zoom
Koordinate
Route
Profil
```

Für Tiles-/PMTiles-Kontext bevorzugt:

```text
Tiles
PMTiles
Style
Glyphs
Sprites
Fonts
Vector Tiles
Raster Tiles
Terrain
```

---

## API-Begriffe

Für API-Seiten bevorzugt:

```text
API
Endpoint
Request
Response
Parameter
Beispiel
Status
Fehlercode
JSON
```

Diese Begriffe können auf Deutsch erklärt werden, müssen aber technisch korrekt bleiben.

---

## Kurzfassung

- Sichtbare Namen beginnen bei zentralen Diensten mit `OE5ITH`.
- `OE5ITH` wird groß geschrieben.
- Domains und technische Pfade bleiben kleingeschrieben.
- URLs sind keine guten Seitentitel.
- Navigation darf kurze Namen verwenden, wenn der OE5ITH-Kontext klar ist.
- Begriffe innerhalb einer Seite konsistent verwenden.
- Versionierung nicht in Dateinamen abbilden.

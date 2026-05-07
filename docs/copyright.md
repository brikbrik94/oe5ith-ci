# Copyright & Lizenzen

Dieses Dokument listet alle externen Ressourcen (Schriftarten, Icons, Bibliotheken)
die im OE5ITH CI und auf den zugehörigen Webseiten verwendet werden,
sowie deren Lizenzanforderungen für die Darstellung auf Webseiten.

---

## Schriftarten

### JetBrains Mono

| | |
|---|---|
| **Verwendung** | Monospace — Code-Blöcke, URLs, Koordinaten, Terminal-Ausgaben |
| **Hersteller** | JetBrains s.r.o. |
| **Lizenz** | SIL Open Font License 1.1 (OFL-1.1) |
| **Quelle** | https://www.jetbrains.com/lp/mono/ |
| **GitHub** | https://github.com/JetBrains/JetBrains-Mono |

**OFL-1.1 Anforderungen:**
- Kostenlose Nutzung, Einbettung und Weitergabe erlaubt
- Schriftart darf nicht unter einem anderen Namen verkauft werden
- Ableitende Werke müssen ebenfalls unter OFL lizenziert werden
- Copyright-Vermerk muss in Ableitungen erhalten bleiben

**Copyright-Vermerk:**
```
Copyright 2020 The JetBrains Mono Project Authors
(https://github.com/JetBrains/JetBrains-Mono)
```

**Pflichtangabe auf Webseiten:** Nein — OFL erfordert keinen sichtbaren
Copyright-Vermerk auf der Webseite selbst, nur in mitgelieferten Schriftdateien.

---

### Segoe UI

| | |
|---|---|
| **Verwendung** | Sans-Serif — alle UI-Texte, Überschriften, Labels |
| **Hersteller** | Microsoft Corporation |
| **Lizenz** | System-Schrift (Windows) — keine Einbettung |
| **Einbindung** | Systemfont-Stack, kein Download |

**Wichtig:** Segoe UI darf **nicht** auf Webservern gehostet werden.
Sie ist eine lizenzierte Microsoft-Schrift die nur über den System-Font-Stack
(`font-family: 'Segoe UI', system-ui, sans-serif`) genutzt werden darf.
Auf Nicht-Windows-Systemen greift automatisch `system-ui` (San Francisco auf macOS/iOS,
Roboto auf Android).

**Pflichtangabe auf Webseiten:** Nein.

---

## Icons

### Font Awesome 6 Free

| | |
|---|---|
| **Verwendung** | UI-Icons in Topbar, Sidebar, Buttons, Badges, Panels |
| **Version** | 6.5.1 |
| **Lizenz Icons** | CC BY 4.0 — Creative Commons Attribution 4.0 |
| **Lizenz Code** | MIT License |
| **Hersteller** | Fonticons, Inc. |
| **Webseite** | https://fontawesome.com |
| **GitHub** | https://github.com/FortAwesome/Font-Awesome |

**CC BY 4.0 Anforderungen für Icons:**
- Namensnennung erforderlich wenn Icons direkt in einem Werk verwendet werden
- Für Webseiten gilt: Attribution empfohlen aber nicht zwingend für die
  Free-Variante bei normaler Nutzung im UI-Kontext
- Icons dürfen modifiziert werden

**Empfohlene Attribution (z.B. im Footer oder Impressum):**
```
Icons: Font Awesome Free (https://fontawesome.com) — CC BY 4.0
```

**MIT License (Code/CSS):**
```
Copyright (c) Fonticons, Inc.
```

**Selbst-Hosting:** Font Awesome Free darf vollständig selbst gehostet werden.
Alle benötigten Dateien (CSS + Webfonts) sind in der Free-Version enthalten.

---

## Karten-Bibliotheken

### Leaflet

| | |
|---|---|
| **Verwendung** | Interaktive Karten (karte.oe5ith.at, NAH, Routing) |
| **Version** | aktuell |
| **Lizenz** | BSD 2-Clause License |
| **Hersteller** | Vladimir Agafonkin |
| **Webseite** | https://leafletjs.com |
| **GitHub** | https://github.com/Leaflet/Leaflet |

**BSD 2-Clause Anforderungen:**
- Copyright-Vermerk und Lizenzbedingungen müssen in der Software erhalten bleiben
- Namensnennung bei öffentlicher Verwendung empfohlen

**Pflichtangabe auf Webseiten:**
Leaflet fügt automatisch einen `© Leaflet` Link in die Karte ein.
Dieser **darf nicht entfernt werden** — er ist Teil der Lizenzbedingungen.

```
© Leaflet (https://leafletjs.com)
```

---

### MapLibre GL JS

| | |
|---|---|
| **Verwendung** | Vektor-Kartendarstellung (vector-map-test, zukünftige Karten) |
| **Version** | aktuell |
| **Lizenz** | BSD 3-Clause License |
| **Hersteller** | MapLibre contributors |
| **Webseite** | https://maplibre.org |
| **GitHub** | https://github.com/maplibre/maplibre-gl-js |

**BSD 3-Clause Anforderungen:**
- Copyright-Vermerk in der Software erhalten
- Weder Name des Projekts noch der Beitragenden zur Bewerbung verwenden

**Pflichtangabe auf Webseiten:** Keine zwingend, Attribution empfohlen.

---

## Kartendaten

### OpenStreetMap

| | |
|---|---|
| **Verwendung** | Kartendaten für alle Karten-Seiten |
| **Lizenz** | Open Database License (ODbL) 1.0 |
| **Hersteller** | OpenStreetMap contributors |
| **Webseite** | https://www.openstreetmap.org |

**ODbL Anforderungen — PFLICHT auf Webseiten:**
Der folgende Copyright-Vermerk **muss** auf jeder Seite mit OSM-Kartendaten
sichtbar dargestellt werden (üblicherweise in der Karte selbst):

```
© OpenStreetMap contributors (https://www.openstreetmap.org/copyright)
```

Leaflet und MapLibre fügen diesen Vermerk automatisch hinzu wenn der
Attribution-Layer korrekt konfiguriert ist. **Nicht entfernen.**

---

### basemap.at

| | |
|---|---|
| **Verwendung** | Österreich-spezifische Basiskarte |
| **Lizenz** | Creative Commons Attribution 4.0 (CC BY 4.0) |
| **Hersteller** | Bundesamt für Eich- und Vermessungswesen (BEV) |
| **Webseite** | https://basemap.at |

**CC BY 4.0 Anforderungen — PFLICHT:**
```
© basemap.at (https://basemap.at) — CC BY 4.0
```

---

## Pflicht-Attributions-Übersicht

Folgende Vermerke **müssen** auf Kartenseiten sichtbar sein:

```
© OpenStreetMap contributors | © Leaflet | © basemap.at
```

> **Hinweis:** `.map-attribution` wurde in v2.0.0 entfernt. Karten-Seiten verwenden die native
> MapLibre/Leaflet-Attribution. Weiterführende Copyright-Infos über `.sidebar-footer-copyright`.

---

## Webseiten-Impressum Empfehlung

Für das Impressum / die Datenschutzseite empfohlener Abschnitt:

```
Verwendete Open-Source-Bibliotheken und Ressourcen:
- Font Awesome Free (https://fontawesome.com) — Icons — CC BY 4.0 / MIT
- JetBrains Mono (https://www.jetbrains.com/lp/mono/) — Schriftart — OFL 1.1
- Leaflet (https://leafletjs.com) — Kartenbibliothek — BSD 2-Clause
- MapLibre GL JS (https://maplibre.org) — Vektorkarten — BSD 3-Clause
- OpenStreetMap (https://www.openstreetmap.org) — Kartendaten — ODbL 1.0
- basemap.at (https://basemap.at) — Österreich-Basiskarte — CC BY 4.0
```

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-24 | Initiale Erstellung. JetBrains Mono, Font Awesome, Leaflet, MapLibre, OSM, basemap.at. |

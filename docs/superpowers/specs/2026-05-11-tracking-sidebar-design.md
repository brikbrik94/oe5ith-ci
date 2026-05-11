# Design: Tracking-Sidebar (ADSB/AIS)

**Datum:** 2026-05-11  
**Seite:** map.oe5ith.at/tracking  
**Status:** genehmigt

---

## Kontext

Die Tracking-Seite empfängt ADSB- (Flugzeuge) und AIS- (Schiffe) Pakete und stellt sie auf einer Karte dar. Die Sidebar zeigt Live-Statistiken zum Empfang und Details zum angeklickten Objekt.

---

## Gesamtstruktur

Zwei gestapelte Panels in einer gemeinsamen `.sidebar-inner`:

```
.sidebar-inner
├── [Typ 6] Stats-Panel
│     ├── status-row: ADS-B Flugzeuge
│     ├── status-row: AIS Schiffe
│     ├── status-row: Receiver
│     └── status-row: Pakete/min
├── .tool-sep
└── [Typ 8] Objekt-Detail-Panel
      ├── Leerzustand: .result-empty
      └── Gefüllt: .object-detail
            ├── .object-detail-header
            └── .result-kv (Zeilen)
.sidebar-footer (Version · © — Standard)
```

Sidebar-Typ laut `sidebar-types.md`: **Kombination Typ 6 + Typ 8**.

---

## Abschnitt 1: Stats-Panel (Typ 6)

Vier `status-row`-Zeilen, live per JS aktualisiert.

| Zeile | Icon | Label | Wert | Dot-Logik |
|---|---|---|---|---|
| 1 | `fa-plane` | ADS-B Flugzeuge | Anzahl empfangene Flugzeuge | `.on` wenn >0 · `.off` wenn 0 |
| 2 | `fa-ship` | AIS Schiffe | Anzahl empfangene Schiffe | `.on` wenn >0 · `.off` wenn 0 |
| 3 | `fa-tower-broadcast` | Receiver | `online` / `offline` | `.on` online · `.warn` erreichbar aber keine Pakete · `.off` nicht erreichbar |
| 4 | `fa-arrow-right-arrow-left` | Pakete/min | Durchsatz | kein Dot |

**HTML-Beispiel:**

```html
<div class="status-row">
  <div class="status-row-left">
    <i class="fa-solid fa-plane status-row-icon"></i>
    <span class="status-row-name">ADS-B Flugzeuge</span>
  </div>
  <div class="status-row-right">
    <span class="status-row-value" id="stat-adsb-count">0</span>
    <span class="status-dot off" id="stat-adsb-dot"></span>
  </div>
</div>
```

---

## Abschnitt 2: Objekt-Detail-Panel (Typ 8)

Neuer Sidebar-Typ: **Typ 8 — Objekt-Detail**. Für Tracking-Seiten mit Klick auf Kartenobjekt.

### Leerzustand

Solange kein Objekt ausgewählt ist:

```html
<div class="result-empty">
  <i class="fa-solid fa-satellite-dish"></i>
  Klicke auf ein Flugzeug oder Schiff auf der Karte für Details.
</div>
```

Kein Hover, kein Klick — rein informativ. Pattern identisch zu Typ 5 `.result-empty`.

### Gefüllt — ADSB

```html
<div class="object-detail">
  <div class="object-detail-header">
    <i class="fa-solid fa-plane object-detail-icon"></i>
    <span class="object-detail-name">AUA123</span>
    <span class="badge badge-accent">ADS-B</span>
  </div>
  <div class="result-kv">
    <div class="result-kv-item">
      <span class="result-kv-label">Höhe</span>
      <span class="result-kv-value">8.450 ft</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">Speed</span>
      <span class="result-kv-value">485 kt</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">Kurs</span>
      <span class="result-kv-value">247°</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">RSSI</span>
      <span class="result-kv-value">−82 dBm</span>
    </div>
  </div>
</div>
```

**ADSB-Felder:** Callsign, Höhe (ft), Speed (kt), Kurs (°), RSSI (dBm)

### Gefüllt — AIS

```html
<div class="object-detail">
  <div class="object-detail-header">
    <i class="fa-solid fa-ship object-detail-icon"></i>
    <span class="object-detail-name">NORDIC ODEN</span>
    <span class="badge badge-surface">AIS</span>
  </div>
  <div class="result-kv">
    <div class="result-kv-item">
      <span class="result-kv-label">MMSI</span>
      <span class="result-kv-value">230084000</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">SOG</span>
      <span class="result-kv-value">12,4 kt</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">COG</span>
      <span class="result-kv-value">184°</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">RSSI</span>
      <span class="result-kv-value">−91 dBm</span>
    </div>
  </div>
</div>
```

**AIS-Felder:** Schiffsname, MMSI, SOG (kt), COG (°), RSSI (dBm)

### Badge-Unterscheidung

| Typ | Badge-Klasse | Farbe |
|---|---|---|
| ADSB | `.badge.badge-accent` | `--accent` (blau) |
| AIS | `.badge.badge-surface` | `--surface` / neutral grau |

Unterschiedliche Badge-Farben machen ADSB und AIS auf einen Blick unterscheidbar.

---

## Neue CSS-Klassen

| Klasse | Beschreibung |
|---|---|
| `.object-detail` | Container für das gefüllte Detail-Panel |
| `.object-detail-header` | Zeile mit Icon + Name + Badge; flexbox, gap, align-center |
| `.object-detail-icon` | FA-Icon links, gleiche Breite wie `status-row-icon` (14px, opacity 0.7) |
| `.object-detail-name` | Name/Callsign, font-weight bold, flex: 1 |
| `.badge-surface` | Badge in neutraler Oberflächenfarbe (für AIS) |

`.result-kv` und `.result-kv-item` / `.result-kv-label` / `.result-kv-value` werden **unverändert aus Typ 4 wiederverwendet** — keine neuen Klassen nötig.

---

## Sidebar-Types-Eintrag (Typ 8)

In `docs/sidebar-types.md` ergänzen:

**Typ 8 — Objekt-Detail**

Für Tracking-/Monitoring-Seiten wo ein Klick auf ein Kartenobjekt Details in der Sidebar zeigt. Immer kombiniert mit einem anderen Panel-Typ (z.B. Typ 6) über `tool-sep` getrennt.

Elemente:
- Leerzustand: `.result-empty` (Icon + Hinweistext)
- Gefüllt: `.object-detail` mit Header (Icon + Name + Badge) + `.result-kv`-Zeilen
- Badge-Farbe unterscheidet den Objekttyp (ADSB: accent / AIS: surface)

---

## Tokens & Wiederverwendung

Alle Farben, Abstände und Schatten verwenden bestehende CI-Tokens aus `css/common.css`. Keine neuen Tokens erforderlich — `.object-detail-header` nutzt dieselben Flex/Gap/Opacity-Werte wie `status-row`.

---

## Abgrenzung

- Kein Formular, keine Eingabe in der Sidebar (Map-Seite, Karte ist primär)
- Keine Layer-Steuerung (Typ 2) — ADSB/AIS sind immer aktiv, kein Toggle nötig
- Kein Auge-Icon (Typ 4) — kein Routing, nur Objekt-Detail
- `css/demo.css` wird nicht auf der Produktionsseite geladen

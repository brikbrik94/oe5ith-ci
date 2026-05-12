# Design: Typ 8 — Tracking-Liste (ADSB/AIS)

**Datum:** 2026-05-12  
**Seite:** map.oe5ith.at/tracking  
**Status:** genehmigt  
**Ersetzt:** `2026-05-11-tracking-sidebar-design.md` (Typ 8 Objekt-Detail → Tracking-Liste)

---

## Kontext

Typ 8 wird vollständig neu definiert. Die bisherige Single-Detail-Ansicht (`.object-detail` — zeigt Details des angeklickten Kartenobjekts) wird ersetzt durch eine **scrollbare Tracking-Liste** aller empfangenen Objekte. Ein Mode-Switch filtert die Liste nach Typ (Alle / ADS-B / AIS). Klick auf ein Item klappt es auf und hebt das Objekt auf der Karte hervor.

Die alten Klassen `.object-detail`, `.object-detail-header`, `.object-detail-icon`, `.object-detail-name` werden entfernt.

---

## Gesamtstruktur

```
.sidebar-inner
├── [Typ 6] Stats-Panel  (unverändert)
├── .tool-sep
└── [Typ 8] Tracking-Liste
      ├── .segmented          ← Mode-Switch: Alle / ADS-B / AIS
      │     ├── .segmented-btn.active  "Alle"
      │     ├── .segmented-btn         "ADS-B"
      │     └── .segmented-btn         "AIS"
      ├── .tracking-list
      │     ├── .tracking-item           (collapsed)
      │     │     └── .tracking-item-header
      │     ├── .tracking-item.active    (aufgeklappt + ausgewählt)
      │     │     ├── .tracking-item-header
      │     │     └── .tracking-item-body
      │     └── ...weitere Items
      └── .result-empty   (wenn Filter kein Ergebnis liefert)
.sidebar-footer
```

---

## HTML — Mode-Switch

```html
<div class="segmented">
  <button class="segmented-btn active">Alle</button>
  <button class="segmented-btn">ADS-B</button>
  <button class="segmented-btn">AIS</button>
</div>
```

Wiederverwendung von `.segmented` / `.segmented-btn` aus `forms.css` — keine neuen Klassen.

---

## HTML — Tracking-Liste

```html
<div class="tracking-list">

  <!-- Item collapsed -->
  <div class="tracking-item" data-type="adsb">
    <div class="tracking-item-header">
      <i class="fa-solid fa-plane tracking-item-icon"></i>
      <span class="tracking-item-name">AUA123</span>
      <span class="badge badge-blue">ADS-B</span>
      <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
    </div>
  </div>

  <!-- Item aufgeklappt + aktiv -->
  <div class="tracking-item active" data-type="adsb">
    <div class="tracking-item-header">
      <i class="fa-solid fa-plane tracking-item-icon"></i>
      <span class="tracking-item-name">OE-LXA</span>
      <span class="badge badge-blue">ADS-B</span>
      <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
    </div>
    <div class="tracking-item-body">
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
  </div>

  <!-- AIS-Item collapsed -->
  <div class="tracking-item" data-type="ais">
    <div class="tracking-item-header">
      <i class="fa-solid fa-ship tracking-item-icon"></i>
      <span class="tracking-item-name">NORDIC ODEN</span>
      <span class="badge badge-gray">AIS</span>
      <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
    </div>
  </div>

</div>
```

**AIS-Felder in `.tracking-item-body`:** MMSI, SOG (kt), COG (°), RSSI (dBm)

---

## HTML — Leerzustand

Wenn der aktive Filter keine Ergebnisse liefert (z.B. AIS-Filter aber noch keine Schiffe empfangen):

```html
<div class="result-empty">
  <i class="fa-solid fa-satellite-dish"></i>
  Keine AIS-Schiffe empfangen.
</div>
```

Text ist app-spezifisch je nach aktivem Filter.

---

## CSS — Neue Klassen (css/sidebar.css)

| Klasse | Beschreibung |
|---|---|
| `.tracking-list` | `display: flex; flex-direction: column; gap: 4px` |
| `.tracking-item` | Card: `border: 1px solid var(--border); border-radius: 4px; background: var(--panel-deep); cursor: pointer; overflow: hidden` |
| `.tracking-item.active` | `border-left: 2px solid var(--accent)` |
| `.tracking-item-header` | `display: flex; align-items: center; gap: 8px; padding: 6px 8px` |
| `.tracking-item-icon` | `font-size: 0.72rem; color: var(--muted); width: 14px; text-align: center; flex-shrink: 0` |
| `.tracking-item-name` | `font-size: 0.82rem; font-weight: 600; color: var(--text); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap` |
| `.tracking-item-chevron` | `font-size: 0.65rem; color: var(--muted); flex-shrink: 0; transition: transform var(--transition-fast)` |
| `.tracking-item.active .tracking-item-chevron` | `transform: rotate(180deg)` |
| `.tracking-item-body` | `display: none; padding: 0 8px 8px` |
| `.tracking-item.active .tracking-item-body` | `display: block` |

## CSS — Entfernte Klassen (css/sidebar.css)

- `.object-detail`
- `.object-detail-header`
- `.object-detail-icon`
- `.object-detail-name`

## CSS — Wiederverwendet ohne Änderung

- `.segmented` / `.segmented-btn` aus `forms.css`
- `.result-kv`, `.result-kv-item`, `.result-kv-label`, `.result-kv-value` aus `sidebar.css`
- `.result-empty` aus `sidebar.css`

---

## JS-Zuständigkeiten (App-Grenze)

| Aktion | JS-Aufgabe |
|---|---|
| Klick auf `.tracking-item-header` | `.active` am Parent-Item toggeln, alle anderen Items deaktivieren; entsprechendes Kartenobjekt highlighten |
| Kartenklick auf Objekt | Passendes `.tracking-item` per `data-id` oder Callsign/MMSI finden, `.active` setzen, `scrollIntoView()` |
| Mode-Switch `.segmented-btn` klicken | `.active` auf geklicktem Button; `.tracking-item` per `data-type` filtern |
| Neues Objekt empfangen | `.tracking-item` in `.tracking-list` einfügen |
| Objekt-Werte aktualisieren | Werte in `.result-kv-value` des entsprechenden Items aktualisieren |

`data-type="adsb"` / `data-type="ais"` ist die einzige CI-relevante JS-Schnittstelle.

---

## Betroffene Dateien

| Datei | Aktion |
|---|---|
| `css/sidebar.css` | `.object-detail*` entfernen; `.tracking-list`, `.tracking-item*` hinzufügen |
| `docs/sidebar-types.md` | Typ 8 vollständig neu schreiben |
| `components/sidebar-types.html` | Typ 8 Demo-Sektion neu aufbauen |
| `CHANGELOG.md` | Änderung dokumentieren |

---

## Badge-Unterscheidung

| Typ | Badge-Klasse | Bedeutung |
|---|---|---|
| ADS-B | `.badge.badge-blue` | Flugzeug (bestehende Klasse) |
| AIS | `.badge.badge-gray` | Schiff (bestehende Klasse) |

# Sidebar-Typen — Entscheidungshilfe

**Referenz-Datei:** `components/sidebar-types.html`  
**Status:** definiert · v1.0

---

## Überblick

Acht definierte Sidebar-Panel-Typen. Panels können **gestapelt** werden —
z.B. Tool-Panel + Ergebnis-Liste in einer gemeinsam scrollenden `.sidebar-inner`.

| Typ | Name | Beispiel |
|---|---|---|
| 1 | Nav-Liste | internal.oe5ith.at |
| 2 | Layer-Steuerung | karte.oe5ith.at |
| 3 | Tool-Panel | Routing A→B |
| 4 | Tool-Panel + Ergebnis-Liste | Routing SEW/NEF |
| 5 | Ergebnis-Liste einfach | NAH-Stützpunkte |
| 6 | Status-Panel | ADS-B/AIS Live-Stats |
| 7 | Koordinaten-Umrechner | coord.oe5ith.at |
| 8 | Tracking-Liste | map.oe5ith.at/tracking |

> **Sidebar-Footer:** Jede Sidebar benötigt ein `.sidebar-footer` am unteren Rand (Version, optionaler Status, `©`-Button).
> Vollständige Struktur und HTML: → [`docs/sidebar.md` — Abschnitt „Sidebar Footer"](sidebar.md#sidebar-footer)

---

## Entscheidungsbaum

```
Navigiert der Nutzer zwischen Seiten?
│
└── JA → Typ 1: Nav-Liste

Steuert der Nutzer Karten-Layer?
│
└── JA → Typ 2: Layer-Steuerung (Accordion)

Gibt der Nutzer Daten ein und bekommt Ergebnisse?
│
├── Ergebnisse in der Sidebar anzeigen?
│   ├── JA, mit Formular oben → Typ 4: Tool + Ergebnis-Liste
│   └── JA, nur Ergebnisse   → Typ 5: Ergebnis-Liste einfach
│
└── Nur Formular, Ergebnis auf der Karte → Typ 3: Tool-Panel

Zeigt die Sidebar nur Live-Daten (read-only)?
│
└── JA → Typ 6: Status-Panel

Zeigt die Sidebar alle empfangenen Tracking-Objekte (Flugzeuge, Schiffe) in einer Liste?
│
└── JA → Typ 8: Tracking-Liste (kombiniert mit Typ 6)

Gibt der Nutzer Koordinaten ein und will zwischen Systemen umrechnen?
│
└── JA → Typ 7: Koordinaten-Umrechner

Kombinationen nötig?
└── Panels stapeln — z.B. Typ 2 + Typ 6
```

---

## Typ 1 — Nav-Liste

**Beispiel:** internal.oe5ith.at, tiles.oe5ith.at

**Wann verwenden:**
Seiten mit fester Navigation zwischen mehreren Bereichen.
Die Sidebar ist primär ein Navigations-Element, kein Tool.

**Elemente:**
- Section-Labels (nur bei mehreren Gruppen)
- Nav-Items mit Icon + Label + optionalem Status-Dot
- Externe Links in eigener Gruppe am Ende (`color: #666`, Pfeil-Icon)
- Trenner (`sidebar-sep`) zwischen Gruppen

**Regeln:**
- Status-Dot rechts: `online` (grün) / `offline` (rot) für Live-Services
- Externe Links immer als letzte Gruppe, nie gemischt mit internen
- Max. 3 Hierarchie-Ebenen (Section → Item, keine Sub-Items)

---

## Typ 2 — Layer-Steuerung (Accordion)

**Beispiel:** karte.oe5ith.at, vector-map-test

**Wann verwenden:**
Karten-Seiten mit ein-/ausschaltbaren Layern.
Nutzer soll Layer-Gruppen auf- und zuklappen können.

**Elemente:**
- Optionales Filter-Feld (nur bei >5 Gruppen)
- Accordion-Gruppen mit Dot, Titel, Status-Badge
- Checkboxen pro Layer
- Schnellzugriff "Alle an / Alle aus" (nur bei geöffneter Gruppe)

**Regeln:**
- Dot-Farbe ist site-spezifisch — kein CI-Token
- Badge automatisch per JS: `nicht geladen` / `n Layer` / `alle aktiv`
- Accordion-Höhe dynamisch (`scrollHeight`) — nie statisch begrenzen
- Keyboard-Navigation: Enter/Space für Header und Items

---

## Typ 3 — Tool-Panel (Formular)

**Beispiel:** Routing A→B, zukünftige Analyse-Tools

**Wann verwenden:**
Karten-Seiten mit Berechnungs-Tool. Das Ergebnis erscheint
direkt auf der Karte — keine Liste in der Sidebar nötig.

**Elemente (typische Reihenfolge):**
1. Titel (H1-Equivalent der Sidebar)
2. Service-Selector (wenn mehrere Endpunkte verfügbar)
3. Trenner
4. Profil / Kategorie (Select)
5. Modus (Segmented Control)
6. Trenner
7. Eingabefelder (Koordinaten, Geocoder)
8. Submit-Button (volle Breite, ganz unten)

**Regeln:**
- Submit-Button immer letztes Element, volle Breite
- Trenner zwischen logischen Gruppen (nicht nach jedem Feld)
- Formular-Elemente aus `forms.css`

---

## Typ 4 — Tool-Panel + Ergebnis-Liste (gestapelt)

**Beispiel:** Routing SEW/NEF (5 nächste Dienststellen)

**Wann verwenden:**
Karten-Seiten wo nach einer Berechnung eine Liste von Ergebnissen
in der Sidebar erscheint. Formular und Ergebnisse scrollen gemeinsam.

**Struktur:**

```html
<div class="sidebar-inner">

  <!-- Tool-Panel (Formular) -->
  <div class="tool-panel-title">Routing</div>
  <!-- Felder... -->
  <button class="btn-primary">Start</button>

  <!-- Trenner -->
  <div class="tool-sep"></div>

  <!-- Ergebnis-Header -->
  <div class="result-header">
    <span class="result-count">5 Standorte gefunden</span>
  </div>
  <div class="result-label">Nächste RD-Dienststellen (SEW)</div>

  <!-- Ergebnis-Liste -->
  <div class="result-list">
    <div class="result-item active">
      <div class="result-item-header">
        <span class="result-num">1</span>
        <span class="result-item-title">Rotes Kreuz Ortsstelle Leonding</span>
      </div>
      <div class="result-item-sub">0620</div>
      <div class="result-kv">
        <div class="result-kv-item">
          <span class="result-kv-label">Dauer</span>
          <span class="result-kv-value">3 min</span>
        </div>
        <div class="result-kv-item">
          <span class="result-kv-label">Distanz</span>
          <span class="result-kv-value">4.4 km</span>
        </div>
      </div>
      <!-- Auge-Icon: Route anzeigen -->
      <button class="result-action" title="Route anzeigen">
        <i class="fa-solid fa-eye"></i>
      </button>
    </div>
    <!-- weitere Items... -->
  </div>

</div>
```

**Zwei unabhängige Aktionen pro Item:**

| Aktion | Element | Verhalten |
|---|---|---|
| Klick auf Auge | `.result-action` | Route ein-/ausblenden (Toggle) — mehrere gleichzeitig möglich |
| Klick auf Item | `.result-item` | Bereits sichtbare Route auf Karte hervorheben (highlight), Item wird `.active` |

**Auge-Button Zustände (`result-action`):**

| Zustand | CSS | Bedeutung |
|---|---|---|
| Aus (default) | — | Route nicht sichtbar, Auge dezent (muted) |
| Hover | — | Accent-Hint — zeigt Interaktivität |
| An | `.result-action.active` | Route sichtbar — Success-Grün, sichtbar auf dunklem und blauem Hintergrund |

**Regeln:**
- Auge-State ist unabhängig vom Item-Auswahlzustand — kein `color: accent` auf aktivem Item
- Mehrere Augen können gleichzeitig `.active` sein
- Klick auf Item ohne aktives Auge: zeigt die Route zuerst (setzt Auge auf `.active`), dann highlight
- Nummer-Badge wird bei `.active` Item mit Accent gefüllt
- `tool-sep` zwischen Formular und Ergebnis-Block
- Ergebnis-Header zeigt Anzahl (grün) + Label der Kategorie
- Wenn keine Ergebnisse: `result-count` in `--danger`

---

## Typ 5 — Ergebnis-Liste einfach

**Beispiel:** NAH-Stützpunkte (nur Ergebnisliste, kein Formular)

**Wann verwenden:**
Die Sidebar zeigt nur Ergebnisse — kein Formular, keine Eingabe.
Kein Auge-Icon (keine Routing-Funktion). Ganzes Item ist klickbar.

**Elemente:**
- Titel (H2-Equivalent der Sidebar)
- Items mit: Nummer-Badge + Titel (fett) + Organisation (accent) + Meta (Distanz/Zeit)
- Gleicher Card-Stil wie Typ 4 (Rahmen, Hover, Active-State)

```html
<div class="result-item-simple active">
  <div class="result-item-header">
    <span class="result-num">1</span>
    <span class="result-simple-title">ÖAMTC Luftrettungsstation Hörsching</span>
  </div>
  <div class="result-simple-org">Christophorus Flugrettungsverein</div>
  <div class="result-simple-meta">5.06 km · Anflugzeit ca. 3 min · Ankunft ca. 14:49</div>
</div>
```

**Regeln:**
- Kein Auge-Icon — Typ 5 hat keine Route-Toggle-Funktion
- Nummer-Badge wie in Typ 4 (wird bei `.active` mit Accent gefüllt)
- Org-Name in `--accent` Farbe, fluchtet mit Titel-Text (padding-left: 25px)
- Klick auf ganzes Item → Zoom auf Karte, Item wird `.active`

**Leerzustand:**

Wenn noch keine Ergebnisse vorliegen, `.result-empty` anstelle der `.result-list` anzeigen:

```html
<div class="result-empty">
  <i class="fa-solid fa-arrow-pointer"></i>
  Klicke auf einen Punkt in der Karte, um die 5 nächsten NAH-Stützpunkte zu berechnen.
</div>
```

- Icon optional — FontAwesome, Auswahl site-spezifisch (z.B. `fa-arrow-pointer` für Desktop-Hinweis)
- Kein Hover, kein Klick — rein informativer Zustand
- Text frei wählbar je nach Anwendungsfall

---

## Typ 6 — Status-Panel (read-only)

**Beispiel:** ADS-B/AIS Live-Zähler, Server-Health-Anzeige

**Wann verwenden:**
Live-Daten die nur angezeigt werden — keine Eingabe, keine Navigation.
Aktualisierung per JS im Hintergrund.

**Struktur pro Zeile:**

```html
<div class="status-row">
  <div class="status-row-left">
    <i class="fa-solid fa-plane status-row-icon"></i>
    <span class="status-row-name">ADS-B Flugzeuge</span>
  </div>
  <div class="status-row-right">
    <span class="status-row-value">42</span>
    <span class="status-dot on"></span>
  </div>
</div>
```

**Status-Dot:**

| Klasse | Farbe | Bedeutung |
|---|---|---|
| `.on` | `--success` | Dienst aktiv / Wert normal |
| `.warn` | `--warning` | Warnung / Schwellwert überschritten |
| `.off` | `--danger` | Offline / Fehler |

**Regeln:**
- Kein Hover, kein Klick — rein read-only
- Wert-Spalte rechts: Zahl, Einheit oder Status-Text
- Icon links: immer gleiche Breite (14px), opacity 0.7

---

## Typ 7 — Koordinaten-Umrechner

**Beispiel:** coord.oe5ith.at

**Wann verwenden:**
Karten-Seiten mit bidirektionalem Koordinaten-Umrechner. Nutzer gibt Koordinaten
in einem beliebigen System ein — alle anderen Systeme werden live umgerechnet
und der Punkt auf der Karte gesetzt.

**Elemente:**
- `.coord-block` je Koordinatensystem (aktiv oder inaktiv)
- `.coord-block-header`: Systemname + Copy-Button (`.coord-copy`)
- `.coord-row`: Standard-Zeile mit `.coord-label` + `.coord-input`
- `.coord-row-dms`: DMS-Zeile mit 3 × `.coord-input-dms` + `.coord-suffix` (N/S, E/W)
- `.coord-row-inline`: 2 Feld-Paare nebeneinander (MGRS: GZD + 100km-Square)
- `.coord-input-full`: Volles Feld ohne Label (Maidenhead)
- `.coord-select`: Dropdown für Meridianstreifen (BMN: M28/M31/M34)
- `tool-sep` zwischen Blöcken

**Zustände:**

| Zustand | CSS | Felder |
|---|---|---|
| Aktiver Block (Eingabe) | `.coord-block.active` | Border links `--accent`, Titel `--accent`, editierbar |
| Inaktiver Block (Ausgabe) | `.coord-block` | Kein Rand, `readonly`, Farbe `--muted` |
| Feld-Fehler | `.coord-input-error` | Border `--danger` |

**Regeln:**
- Exakt ein Block ist zur Zeit aktiv — Klick auf inaktiven Block wechselt die Aktivierung
- Copy-Button immer sichtbar (aktiv + inaktiv) — Format ist App-spezifisch
- Kein Submit-Button — Umrechnung erfolgt live per App-JS
- Karten-Punkt wird automatisch gesetzt sobald gültige Koordinaten vorliegen
- Umrechnungslogik, Zone-Defaults und Copy-Format sind nicht Teil des CI

---

## Typ 8 — Tracking-Liste

**Beispiel:** map.oe5ith.at/tracking

**Wann verwenden:**
Tracking-/Monitoring-Karten die alle empfangenen Objekte (Flugzeuge, Schiffe)
in einer scrollbaren Liste zeigen. Mode-Switch filtert nach Typ.
Klick auf ein Item klappt Details auf und hebt das Objekt auf der Karte hervor.
Immer in Kombination mit Typ 6 (Stats-Panel), getrennt durch `tool-sep`.

**Zustände:**

| Zustand | Anzeige |
|---|---|
| Keine Objekte empfangen | `.result-empty` mit Icon + Hinweistext |
| Objekte vorhanden | `.tracking-list` mit `.tracking-item`-Items |
| Item ausgewählt | `.tracking-item.active` — aufgeklappt + Karte highlighted |

**HTML — Mode-Switch:**

```html
<div class="segmented">
  <button class="segmented-btn active">Alle</button>
  <button class="segmented-btn">ADS-B</button>
  <button class="segmented-btn">AIS</button>
</div>
```

**HTML — Tracking-Liste (ein collapsed, ein aktiv aufgeklappt):**

```html
<div class="tracking-list">

  <!-- collapsed -->
  <div class="tracking-item" data-type="adsb" data-id="AUA123">
    <div class="tracking-item-header">
      <i class="fa-solid fa-plane tracking-item-icon"></i>
      <span class="tracking-item-name">AUA123</span>
      <span class="badge badge-blue">ADS-B</span>
      <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
    </div>
  </div>

  <!-- aufgeklappt + aktiv (ADS-B) -->
  <div class="tracking-item active" data-type="adsb" data-id="OE-LXA">
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

  <!-- AIS collapsed -->
  <div class="tracking-item" data-type="ais" data-id="230084000">
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

**HTML — Leerzustand:**

```html
<div class="result-empty">
  <i class="fa-solid fa-satellite-dish"></i>
  Warte auf Empfang…
</div>
```

**Regeln:**
- `data-type="adsb"` / `data-type="ais"` für JS-Filterung via Mode-Switch
- `data-id` = Callsign für ADS-B, MMSI für AIS — wird von JS für Kartenklick-Zuordnung genutzt
- Badge-Farbe: `.badge-blue` für ADS-B, `.badge-gray` für AIS
- `.result-kv` aus Typ 4 wird unverändert wiederverwendet
- `.result-empty` aus Typ 5 wird wiederverwendet
- `.segmented` / `.segmented-btn` aus `forms.css` wird wiederverwendet
- Immer genau ein Item kann `.active` sein (oder keines)
- JS-Zuständigkeit: Klick auf `.tracking-item-header` → `.active` toggeln + Karte highlighten; Kartenklick → Item per `data-type`/`data-id` finden, `.active` setzen, `scrollIntoView()`; Mode-Switch → Items per `data-type` filtern

---

## Panels stapeln

Mehrere Panel-Typen können in einer `.sidebar-inner` kombiniert werden.
Reihenfolge: Tool/Eingabe oben, Ergebnisse unten.

| Kombination | Verwendung |
|---|---|
| Typ 1 + Typ 6 | Nav-Liste + Live-Stats am Ende |
| Typ 2 + Typ 6 | Layer-Steuerung + Status-Anzeige |
| Typ 3 + (→ Typ 4) | Tool-Panel, nach Berechnung Ergebnisse einblenden |
| Typ 6 + Typ 8 | Live-Stats + Tracking-Liste (Tracking-Seite) |

**Trenner zwischen gestapelten Panels:**
```html
<div class="tool-sep"></div>
```

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-24 | Initiale Definition. 6 Typen. Gestapelte Panels. Ergebnis-Liste mit Auge-Icon. |
| 2026-04-30 | Typ 5: `.result-empty` Leerzustand ergänzt |
| 2026-05-05 | Typ 7: Koordinaten-Umrechner ergänzt (`coords.css`, `.coord-block` Pattern) |
| 2026-05-11 | Typ 8: Objekt-Detail ergänzt; `result-kv`, `status-panel/row/dot` nach `sidebar.css` extrahiert |
| 2026-05-12 | Typ 8: Objekt-Detail → Tracking-Liste; Mode-Switch, Expand-Verhalten, `data-type`-Filter |

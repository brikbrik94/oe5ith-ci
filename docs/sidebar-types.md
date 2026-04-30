# Sidebar-Typen — Entscheidungshilfe

**Referenz-Datei:** `components/sidebar-types.html`  
**Status:** definiert · v1.0

---

## Überblick

Sechs definierte Sidebar-Panel-Typen. Panels können **gestapelt** werden —
z.B. Tool-Panel + Ergebnis-Liste in einer gemeinsam scrollenden `.sidebar-inner`.

| Typ | Name | Beispiel |
|---|---|---|
| 1 | Nav-Liste | internal.oe5ith.at |
| 2 | Layer-Steuerung | karte.oe5ith.at |
| 3 | Tool-Panel | Routing A→B |
| 4 | Tool-Panel + Ergebnis-Liste | Routing SEW/NEF |
| 5 | Ergebnis-Liste einfach | NAH-Stützpunkte |
| 6 | Status-Panel | ADS-B/AIS Live-Stats |

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

## Panels stapeln

Mehrere Panel-Typen können in einer `.sidebar-inner` kombiniert werden.
Reihenfolge: Tool/Eingabe oben, Ergebnisse unten.

| Kombination | Verwendung |
|---|---|
| Typ 1 + Typ 6 | Nav-Liste + Live-Stats am Ende |
| Typ 2 + Typ 6 | Layer-Steuerung + Status-Anzeige |
| Typ 3 + (→ Typ 4) | Tool-Panel, nach Berechnung Ergebnisse einblenden |

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

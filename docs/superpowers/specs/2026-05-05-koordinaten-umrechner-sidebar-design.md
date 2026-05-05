# Sidebar Typ 7 — Koordinaten-Umrechner

**Datum:** 2026-05-05  
**Status:** Entwurf  
**Scope:** CI-Definition — HTML-Struktur, CSS-Klassen, Zustände. Umrechnungslogik und Zone-Defaults sind Sache der jeweiligen App.

---

## Übersicht

Neuer Sidebar-Typ für Koordinaten-Umrechner-Seiten. Der Nutzer gibt Koordinaten in einem beliebigen System ein — alle anderen Systeme werden live umgerechnet und der Punkt auf der Karte gesetzt. Jedes System kann durch Klick zum aktiven Eingabe-System werden (bidirektional).

---

## Unterstützte Koordinatensysteme

| System | Felder | Besonderheit |
|---|---|---|
| WGS84 Dezimalgrad | 2 | Lat. / Lon. |
| WGS84 DMS | 6 (3 × 2) | Grad / Min / Sek je Koordinate + N/S, E/W Suffix |
| UTM | 3 | Zone / Easting / Northing |
| BMN | 3 | Meridianstreifen-Dropdown (M28/M31/M34) + HW / RW |
| MGRS | 4 | GZD + 100km-Square inline, E + N darunter |
| Maidenhead | 1 | Einzelnes Locator-Feld |

---

## Block-Struktur

Jedes Koordinatensystem wird als `.coord-block` dargestellt.

```html
<div class="coord-block active">
  <div class="coord-block-header">
    <span class="coord-block-title">WGS84 Dezimalgrad</span>
    <button class="coord-copy" title="Koordinate kopieren">
      <i class="fa-solid fa-copy"></i>
    </button>
  </div>
  <div class="coord-row">
    <span class="coord-label">Lat.</span>
    <input class="coord-input" type="text" inputmode="decimal" placeholder="48.123456">
  </div>
  <div class="coord-row">
    <span class="coord-label">Lon.</span>
    <input class="coord-input" type="text" inputmode="decimal" placeholder="14.654321">
  </div>
</div>
```

Zwischen Blöcken: `<div class="tool-sep"></div>`

### Feld-Layouts je System

**WGS84 Dezimalgrad**
```
Lat.  [  48.123456        ]
Lon.  [  14.654321        ]
```

**WGS84 DMS**
```
Lat.  [ 48° ] [ 23' ] [ 15.4" ]  N
Lon.  [ 14° ] [ 38' ] [ 46.2" ]  E
```
DMS-Zeile: `.coord-row-dms` mit 3 × `.coord-input-dms` (schmaler) + `.coord-suffix` (N/S bzw. E/W)

**UTM**
```
Zone  [ 33U             ]
E     [  411234         ]
N     [ 5332100         ]
```

**BMN**
```
M     [ M31 ▾ ]   ← <select class="coord-select">
HW    [  5332100  ]
RW    [   411234  ]
```

**MGRS**
```
GZD [ 33U ]  100km [ VP ]    ← inline, .coord-row-inline
E   [  41123  ]
N   [  33210  ]
```
Inline-Zeile: `.coord-row-inline` mit je einem `.coord-label` + `.coord-input-short`

**Maidenhead**
```
     [  JN77TX          ]
```
Kein Label — einzelnes `.coord-input-full`

---

## Zustände

### Aktiver Block (Eingabe)

- Border links: 3px solid `var(--accent)` — wie aktives Nav-Item
- `.coord-block-title` Farbe: `var(--accent)`
- Felder: heller Hintergrund, editierbar, Fokus-Ring bei Keyboard-Navigation
- Klasse: `.coord-block.active`

### Inaktiver Block (Ausgabe)

- Kein farbiger Rand
- `.coord-block-title` Farbe: `var(--text)`
- Felder: `var(--surface-2)` Hintergrund, `readonly`-Attribut, `cursor: default`
- Hover auf Block: leichte Hervorhebung zeigt Klickbarkeit
- Klick auf beliebige Stelle im Block → Block wird aktiv, alle anderen inaktiv

### Ungültige Eingabe

- Betroffenes Feld erhält `.coord-input-error` (Border: `var(--danger)`)
- Letzter gültiger Punkt bleibt auf der Karte

### Leerzustand

- Alle Felder leer, erster Block (WGS84 Dezimalgrad) ist aktiv und hat Fokus

---

## Karten-Interaktion

- Automatisch, kein Button — sobald ein vollständiger gültiger Koordinatensatz vorliegt, wird der Punkt auf der Karte gesetzt
- Bei ungültiger oder unvollständiger Eingabe: letzter gültiger Punkt bleibt

---

## Copy-Button

- `.coord-copy` immer sichtbar (aktiv und inaktiv)
- Kopiert die vollständige Koordinate als formatierten String in die Zwischenablage
- Format ist systemspezifisch (App-Logik), CI definiert nur den Button

---

## Sidebar-Gesamtstruktur

```html
<div class="sidebar-inner">

  <div class="coord-block active"> <!-- WGS84 Dezimalgrad --> </div>
  <div class="tool-sep"></div>

  <div class="coord-block"> <!-- WGS84 DMS --> </div>
  <div class="tool-sep"></div>

  <div class="coord-block"> <!-- UTM --> </div>
  <div class="tool-sep"></div>

  <div class="coord-block"> <!-- BMN --> </div>
  <div class="tool-sep"></div>

  <div class="coord-block"> <!-- MGRS --> </div>
  <div class="tool-sep"></div>

  <div class="coord-block"> <!-- Maidenhead --> </div>

</div>
```

Kein Submit-Button — die Sidebar ist ein reines Tool-Panel mit Live-Umrechnung.

---

## Entscheidungsbaum-Ergänzung für `sidebar-types.md`

```
Gibt der Nutzer Koordinaten ein und will zwischen Systemen umrechnen?
│
└── JA → Typ 7: Koordinaten-Umrechner
```

---

## Neue CSS-Klassen

| Klasse | Beschreibung |
|---|---|
| `.coord-block` | Container eines Koordinatensystems |
| `.coord-block.active` | Aktiver Eingabe-Block |
| `.coord-block-header` | Titelzeile mit Systemname + Copy-Button |
| `.coord-block-title` | Systemname-Label |
| `.coord-copy` | Copy-Button (Icon) |
| `.coord-row` | Zeile mit Label + Eingabefeld |
| `.coord-row-dms` | DMS-Zeile mit 3 Feldern + Suffix |
| `.coord-row-inline` | Zeile mit 2 Feld-Paaren nebeneinander (MGRS) |
| `.coord-label` | Kurzbezeichnung (Lat./Lon./E/N/HW/RW/Zone/GZD) |
| `.coord-suffix` | N/S, E/W Suffix bei DMS |
| `.coord-input` | Standard-Eingabefeld |
| `.coord-input-dms` | Schmales Feld für Grad/Min/Sek |
| `.coord-input-short` | Kurzes Feld für GZD/100km-Square |
| `.coord-input-full` | Volles Feld ohne Label (Maidenhead) |
| `.coord-input-error` | Fehler-Zustand eines Felds |
| `.coord-select` | Dropdown für Meridianstreifen (BMN) |

---

## Abgrenzung

- **CI definiert:** HTML-Struktur, CSS-Klassen, visuelle Zustände, Copy-Button-Element
- **App definiert:** Umrechnungslogik, Zone-Defaults, Copy-Text-Format, Karten-Bibliothek

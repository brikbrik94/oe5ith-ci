# Cards

**Referenz-Datei:** `components/cards.html`  
**Status:** definiert · v1.0

---

## Überblick

Cards sind das zentrale Layout-Element für Inhalte. Alle vier Typen teilen
dieselbe CSS-Basis (`--card-bg`, `--border`, `--card-radius`, `--card-padding`).
Hover-Verhalten, Status-Dots und Badges werden je nach Typ und Kontext definiert.

---

## Basis-Tokens

| Token | Wert |
|---|---|
| `--card-bg` | `#252525` |
| `--card-radius` | `12px` |
| `--card-padding` | `20px` |
| `--card-gap` | `20px` (Abstand zwischen Cards im Grid) |
| Border | `1px solid --border` (#333) |

```css
.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--card-radius);  /* 12px */
  padding: var(--card-padding);       /* 20px */
  position: relative;
  overflow: hidden;    /* Inhalt darf nie herausstehen */
  min-width: 0;        /* verhindert Grid-Overflow */
}
```

---

## Card Grid

| Breakpoint | Spalten |
|---|---|
| Desktop ≥1025px | 3 |
| Tablet 769–1024px | 2 |
| Mobile ≤768px | 1 |

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--card-gap);
}

@media (max-width: 1024px) {
  .card-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 768px) {
  .card-grid { grid-template-columns: 1fr; }
}
```

> **Wichtig:** `minmax(0, 1fr)` statt `1fr` — verhindert dass Cards durch langen
> Inhalt (URLs, lange Strings) breiter als die Spalte werden.

---

## Text-Overflow Regel (Pflicht)

Inhalt darf **nie** über den Card-Rand hinausstehen. Gilt für alle Card-Typen.

```css
/* Titel: einzeilig abschneiden */
.card h2, .card h3, .card h4 {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Beschreibungstext: max. 3 Zeilen */
.card p {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

/* URLs, Pfade, Code: einzeilig abschneiden */
.card-truncate, .card-url {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
}
```

---

## Typ 1 — Navigation Card

**Verwendet auf:** Landing Page  
**Klickbar:** ja — gesamte Card ist ein `<a>`-Link  
**Hover:** `translateY(-5px)` + `box-shadow` + `border-color: --accent`  
**Status-Dot:** nur auf auth-geschützten Seiten sinnvoll, nicht auf öffentlichen

### Struktur

```html
<a href="/ziel" class="card card-nav">
  <div class="card-nav-icon">
    <i class="fa-solid fa-map-location-dot"></i>
  </div>
  <h3>Tileserver Registry</h3>
  <p>Vektorkarten, Styles und Fonts.</p>
  <span class="card-nav-btn">
    <i class="fa-solid fa-arrow-right"></i>
    Öffnen
  </span>
</a>
```

### Disabled-Variante (zukünftige Features)

```html
<a class="card card-nav disabled">
  ...
  <span class="card-nav-btn">Demnächst</span>
</a>
```

```css
.card-nav.disabled { opacity: 0.55; pointer-events: none; }
.card-nav.disabled .card-nav-btn { background: #444; color: #666; }
```

---

## Typ 2 — Dashboard Card (Kachel)

**Verwendet auf:** Internal Dashboard  
**Zwei Varianten:** klickbar (Verlinkung zu Detail-View) oder nicht klickbar (reine Info)

### Klickbare Kachel — `.card-dashboard-link`

Hover identisch zu Nav-Card: `translateY(-5px)` + `box-shadow` + `border-color: --accent`.  
Pfeil-Icon (`→`) erscheint zusätzlich on hover, bottom-right — signalisiert Klickbarkeit.

```html
<a href="/detail/nginx" class="card card-dashboard card-dashboard-link">
  <div class="card-status-dot online" title="Online"></div>
  <h3>Reverse Proxy</h3>
  <p>Nginx · SSL Termination</p>
  <i class="fa-solid fa-arrow-right card-dashboard-arrow"></i>
</a>
```

### Nicht klickbare Kachel — reine Infoanzeige

Kein Hover, kein Pfeil, kein `.card-dashboard-link`.

```html
<div class="card card-dashboard">
  <div class="card-status-dot unknown" title="Unbekannt"></div>
  <h3>Nominatim</h3>
  <p>Geocoding · Status unbekannt</p>
</div>
```

### CSS — Hover + Pfeil

```css
.card-dashboard-link {
  cursor: pointer; text-decoration: none; color: inherit; display: block;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}
.card-dashboard-link:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.3);
  border-color: var(--accent);
}

/* Pfeil — nur on hover sichtbar */
.card-dashboard-arrow {
  position: absolute; bottom: 12px; right: 14px;
  font-size: 0.72rem; color: var(--accent);
  opacity: 0; transform: translateX(-4px);
  transition: opacity 0.15s, transform 0.15s;
}
.card-dashboard-link:hover .card-dashboard-arrow {
  opacity: 1; transform: translateX(0);
}
```

### Status-Dot

Position immer `top: 14px; right: 14px`.

| Klasse | Farbe | Bedeutung |
|---|---|---|
| `.online` | `--success` + Glow | Dienst erreichbar |
| `.offline` | `#ef4444` + Glow | Dienst nicht erreichbar |
| `.unknown` | `#f59e0b` + Glow | Status unbekannt |

```css
.card-status-dot { position: absolute; top: 14px; right: 14px;
                   width: 10px; height: 10px; border-radius: 50%; }
.card-status-dot.online  { background: var(--success); box-shadow: 0 0 5px var(--success); }
.card-status-dot.offline { background: #ef4444; box-shadow: 0 0 5px rgba(239,68,68,0.5); }
.card-status-dot.unknown { background: #f59e0b; box-shadow: 0 0 5px rgba(245,158,11,0.5); }
```

---

## Typ 3 — Content Card

**Verwendet auf:** Tiles Registry, API-Dokumentation  
**Klickbar:** optional  
**Hover:** Entwickler entscheidet je nach Kontext  
**Badge:** immer grau (`color: #666`) — nur Info, keine Semantik

### Struktur

```html
<div class="card">
  <div class="card-content-header">
    <h3>Basemap Austria</h3>
    <span class="card-badge">Basemap</span>
  </div>
  <p>Vektorkarte Österreich im PMTiles-Format.</p>
  <span class="card-url">pmtiles://tiles.oe5ith.at/...</span>
</div>
```

### Badge-Regel

Badges in Content Cards sind **immer grau** — sie tragen keine semantische Bedeutung
(kein Grün für "gut", kein Rot für "schlecht"). Nur Typ-Info.

```css
.card-badge {
  background: rgba(255,255,255,0.04);
  color: #666;
  border: 1px solid #2a2a2a;
  font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
}
```

### URL-Feld

```css
.card-url {
  font-family: monospace; font-size: 0.72rem;
  color: #4ade80; background: #0d0d0d;
  border-radius: 4px; padding: 6px 10px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  display: block; min-width: 0;
}
```

---

## Typ 4 — Info / Hinweis Card

**Verwendet für:** Warnungen, Hinweise, kontextuelle Informationen  
**Position:** Standalone, volle Breite — **nicht** im `.card-grid`  
**border-radius:** rechte Seite 12px, linke Seite 0 (wegen border-left)

```html
<!-- Info (blau) -->
<div class="card-info">
  <strong>Info:</strong> Text hier.
</div>

<!-- Warnung (gelb) -->
<div class="card-warn">
  <strong>Hinweis:</strong> Text hier.
</div>
```

```css
.card-info {
  border-left: 3px solid var(--accent);
  background: rgba(59,130,246, 0.05);
  border-radius: 0 12px 12px 0;
  padding: 12px 16px;
  color: #b8d4f8;
}

.card-warn {
  border-left: 3px solid #eab308;
  background: rgba(234,179,8, 0.05);
  border-radius: 0 12px 12px 0;
  color: #fcd34d;
}
```

---

## Hover-Verhalten

Der Hover-Effekt ist **nicht automatisch** — der Entwickler setzt ihn gezielt je nach Kontext.

| Situation | Hover |
|---|---|
| Card ist klickbarer Link/Button | Ja — `.card-hover` Klasse hinzufügen |
| Card ist reine Infoanzeige | Nein |
| Card öffnet ein Detail / Modal | Ja |

```css
.card-hover {
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  cursor: pointer;
}
.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.3);
  border-color: var(--accent);
}
```

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | Initiale Definition. 4 Typen. 12px Radius. 3/2/1 Grid. Ellipsis für alle Texte. Badge immer grau. Hover kontextabhängig. |

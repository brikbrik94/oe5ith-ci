# Service Dashboard

**Referenz-Dateien:** `components/service-dashboard-overview.html` · `components/service-dashboard-detail.html` · `components/service-dashboard-config.html`
**CSS:** `css/service-dashboard.css`
**Status:** definiert · v1.12.0

---

## Überblick

Drei-Seiten-Muster für lokale Raspberry-Pi-Dienst-Überwachung. Basiert auf bestehenden
CI-Klassen; `service-dashboard.css` ergänzt nur was kein bestehendes Muster abdeckt.

### Ladereihenfolge

```css
css/common.css
css/cards.css        /* card-dashboard, card-grid, card-status-dot */
css/badges.css       /* badge-green/red/yellow */
css/buttons.css      /* btn, btn-danger, btn-secondary, btn-ghost */
css/page.css         /* page-header, panel, content-body */
css/sidebar.css      /* sidebar-nav-item, sidebar-status-dot */
css/service-dashboard.css  /* svc-* Klassen — immer zuletzt */
```

---

## Seite 1 — Übersicht (Seitentyp 3: Dashboard)

Zeigt alle Dienste eines Pi als klickbare Kacheln im Card-Grid.

### HTML-Struktur (Kachel)

```html
<a href="/lora-tracker" class="card card-dashboard card-dashboard-link">
  <div class="card-status-dot online"></div>
  <h3>
    <i class="fa-solid fa-satellite-dish svc-card-icon"></i>
    <span>LoRa-Tracker</span>
  </h3>
  <p class="svc-info-line">GPS Fix · 0.0 km/h</p>
  <span class="svc-status-line online">● Online · TX in 4:58</span>
  <i class="fa-solid fa-arrow-right card-dashboard-arrow"></i>
</a>
```

**Wichtig:** Wenn `.svc-card-icon` im h3 verwendet wird, den Textteil in `<span>` wrappen
damit Truncation korrekt funktioniert.

### Neue Klassen

| Klasse | Zweck |
|---|---|
| `.svc-card-icon` | FA-Icon inline im h3-Titel (accent, 0.85rem, flex-shrink:0) |
| `.svc-info-line` | Kurzbeschreibung unter Titel (0.75rem, muted) |
| `.svc-status-line` | Statuszeile unten (0.7rem) |
| `.svc-status-line.online` | Farbe `--success` |
| `.svc-status-line.offline` | Farbe `--danger` |
| `.svc-status-line.unknown` | Farbe `--warning` |

Bestehende Klassen: `.card-grid`, `.card`, `.card-dashboard`, `.card-dashboard-link`,
`.card-status-dot.online/offline/unknown`, `.card-dashboard-arrow` — alle aus `cards.css`.

---

## Seite 2 — Detail (Seitentyp 1: Detail-Seite)

### Page-Header

```html
<div class="page-header">
  <div class="page-header-left">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
      <i class="fa-solid fa-satellite-dish svc-page-icon"></i>
      <h1 class="page-title" style="font-size:1.2rem;font-weight:600;">LoRa-Tracker</h1>
      <span class="badge badge-green">ONLINE</span>
    </div>
    <p class="page-subtitle">GPS-Tracking · LoRaWAN · TTN</p>
  </div>
  <div class="page-header-right">
    <button class="btn btn-danger">
      <i class="fa-solid fa-rotate-right"></i> Neustart
    </button>
    <a href="/config" class="btn btn-secondary">
      <i class="fa-solid fa-sliders"></i> Config
    </a>
  </div>
</div>
```

Status-Badge: `badge badge-green` (online), `badge badge-red` (offline), `badge badge-yellow` (unknown) — aus `badges.css`.

Aktions-Buttons: `btn btn-danger` (destruktive Aktionen), `btn btn-secondary` (Navigation) — aus `buttons.css`.

### Data Grid

```html
<div class="svc-data-grid">
  <div class="svc-data-cell">
    <span class="svc-data-label">GPS Fix</span>
    <span class="svc-data-value success">Gültig</span>
    <span class="svc-data-sub">48.2643° / 14.2649°</span>
  </div>
</div>
```

| Klasse | Zweck |
|---|---|
| `.svc-data-grid` | Responsive Grid: 3/2/1 Spalten (Desktop/Tablet/Mobile) |
| `.svc-data-cell` | Einzelne Zelle: panel-deep Hintergrund, 8px Radius |
| `.svc-data-label` | Bezeichnung (0.68rem, uppercase, `--subtle`) |
| `.svc-data-value` | Wert (0.95rem, 600, `--text`) |
| `.svc-data-value.success` | Wert in `--success` |
| `.svc-data-value.danger` | Wert in `--danger` |
| `.svc-data-sub` | Subtext (0.72rem, `--muted`) |

### Dynamische Aktionen

Nur API-Endpunkte einblenden, die tatsächlich vorhanden sind. Destruktive Aktionen
(Restart) immer mit `confirm()` absichern.

---

## Seite 3 — Config (Seitentyp 1: Detail-Seite)

### Zurück-Link

```html
<a href="/dienst" class="svc-back-link">
  <i class="fa-solid fa-arrow-left"></i> Zurück
</a>
```

### Feldtypen

| Typ | HTML | Klassen |
|---|---|---|
| Text | `<input type="text">` | `.svc-field` |
| Zahl | `<input type="number">` | `.svc-field` |
| Auswahl | `<select>` | `.svc-field` |
| Read-only | `<div class="svc-field-readonly">` | — |
| Secret | `.svc-secret` + Input + `.svc-secret-toggle` | — |
| URL-Prefix | `.svc-input-prefix` + `.svc-input-prefix-label` + Input | — |
| Toggle | `.svc-toggle` + `.svc-toggle-track` + `.svc-toggle-thumb` + `.svc-toggle-label` | `.on` (aktiv), `.warn` (Warnung wenn aktiv) |
| Textarea | `<textarea>` | `.svc-field` |
| Hilfstext | `<span class="svc-field-hint">` | — |

### Aktionsleiste

```html
<div class="svc-form-actions">
  <button class="btn btn-primary">
    <i class="fa-solid fa-floppy-disk"></i> Speichern
  </button>
  <a href="/dienst" class="btn btn-ghost">Abbrechen</a>
  <!-- Optional -->
  <span class="svc-form-hint">
    <i class="fa-solid fa-rotate"></i> Neustart erforderlich nach Speichern
  </span>
</div>
```

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-07 | Initiale Definition. 3 Seiten. svc-* Klassen. Feldtypen-Palette. |

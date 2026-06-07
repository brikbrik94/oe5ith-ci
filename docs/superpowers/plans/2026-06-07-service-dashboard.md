# Service Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Neuen CI-Baustein `service-dashboard` erstellen — CSS, drei Referenz-HTML-Seiten und Dokumentation für lokale Raspberry-Pi-Dienst-Überwachung.

**Architecture:** Minimale Erweiterung: eine neue `css/service-dashboard.css` enthält nur Klassen die kein bestehendes CI-Muster abdecken. Alle anderen Bausteine (Card-Grid, Panels, Buttons, Badges, Formulare) kommen aus vorhandenen CI-Dateien. Drei neue Referenz-HTML-Seiten dokumentieren Übersicht, Detail und Config. Kein JavaScript.

**Tech Stack:** Vanilla CSS (Custom Properties), HTML5, Font Awesome 6.5, bestehende CI-Klassen aus `cards.css`, `buttons.css`, `badges.css`, `page.css`, `sidebar.css`, `forms.css`.

---

## Datei-Übersicht

| Datei | Aktion | Inhalt |
|---|---|---|
| `css/service-dashboard.css` | Erstellen | Alle neuen `svc-*` Klassen |
| `css/index.css` | Ergänzen | `@import "service-dashboard.css"` am Ende |
| `components/service-dashboard-overview.html` | Erstellen | Referenz: Übersichtsseite (Seitentyp 3) |
| `components/service-dashboard-detail.html` | Erstellen | Referenz: Detail-Seite (Seitentyp 1) |
| `components/service-dashboard-config.html` | Erstellen | Referenz: Config-Seite (Seitentyp 1) |
| `docs/service-dashboard.md` | Erstellen | Dokumentation des Bausteins |
| `CHANGELOG.md` | Ergänzen | v1.12.0 Eintrag |

---

## Task 1: CSS-Datei anlegen und in index.css einbinden

**Files:**
- Create: `css/service-dashboard.css`
- Modify: `css/index.css`

- [ ] **Schritt 1: CSS-Datei erstellen**

Datei `css/service-dashboard.css` mit folgendem vollständigen Inhalt anlegen:

```css
/*
 * OE5ITH CI — service-dashboard.css
 * Service-Monitoring-Baustein für lokale Pi-Dashboards.
 *
 * Abhängigkeiten (müssen vorher geladen sein):
 *   common.css, cards.css, badges.css, buttons.css,
 *   page.css, sidebar.css, forms.css
 *
 * <link rel="stylesheet" href="shared/css/service-dashboard.css">
 */

/* ═══════════════════════════════════════
   SERVICE CARD — Übersicht-Kachel
   ═══════════════════════════════════════ */

/* h3 mit Icon: flex-Layout für Icon + Text */
.card-dashboard h3:has(.svc-card-icon) {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Textspan im h3 mit Icon: korrekte Truncation */
.card-dashboard h3:has(.svc-card-icon) > span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* FA-Icon inline im Titel */
.svc-card-icon {
  color: var(--accent);
  font-size: 0.85rem;
  flex-shrink: 0;
}

/* Kurzbeschreibung unter dem Titel */
.svc-info-line {
  font-size: 0.75rem;
  color: var(--muted);
  margin-bottom: 10px;
  /* .card p setzt -webkit-box — hier überschreiben */
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  -webkit-line-clamp: unset;
}

/* Statuszeile unten in der Kachel */
.svc-status-line {
  font-size: 0.7rem;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.svc-status-line.online  { color: var(--success); }
.svc-status-line.offline { color: var(--danger); }
.svc-status-line.unknown { color: var(--warning); }

/* ═══════════════════════════════════════
   SIDEBAR — fehlende unknown-Variante
   ═══════════════════════════════════════ */

.sidebar-status-dot.unknown {
  background: var(--warning);
  box-shadow: 0 0 4px var(--warning);
}

/* ═══════════════════════════════════════
   DETAIL-SEITE — Page-Header Icon
   ═══════════════════════════════════════ */

.svc-page-icon {
  color: var(--accent);
  font-size: 1.1rem;
  flex-shrink: 0;
  margin-right: 4px;
}

/* ═══════════════════════════════════════
   DATA GRID — Live-Status-Panel
   Desktop: 3 Spalten · Tablet: 2 · Mobile: 1
   ═══════════════════════════════════════ */

.svc-data-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

@media (max-width: 1024px) {
  .svc-data-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 768px) {
  .svc-data-grid { grid-template-columns: 1fr; }
}

.svc-data-cell {
  background: var(--panel-deep);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.svc-data-label {
  font-size: 0.68rem;
  color: var(--subtle);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin-bottom: 4px;
}

.svc-data-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.svc-data-value.success { color: var(--success); }
.svc-data-value.danger  { color: var(--danger); }

.svc-data-sub {
  font-size: 0.72rem;
  color: var(--muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ═══════════════════════════════════════
   CONFIG — Zurück-Link
   ═══════════════════════════════════════ */

.svc-back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--muted);
  text-decoration: none;
  margin-bottom: 20px;
  transition: color var(--transition-fast);
}

.svc-back-link:hover { color: var(--text); }

/* ═══════════════════════════════════════
   CONFIG — Formular-Felder
   ═══════════════════════════════════════ */

/* Wrapper: Label + Input + Hilfstext */
.svc-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.svc-field > label {
  font-size: 0.75rem;
  color: var(--muted);
  font-weight: 500;
}

.svc-field > input,
.svc-field > select,
.svc-field > textarea {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 10px;
  color: var(--text);
  font-size: 0.85rem;
  font-family: inherit;
  width: 100%;
  box-sizing: border-box;
  transition: border-color var(--transition-fast);
}

.svc-field > input:focus,
.svc-field > select:focus,
.svc-field > textarea:focus {
  outline: none;
  border-color: var(--accent);
}

/* Hilfstext unter dem Feld */
.svc-field-hint {
  font-size: 0.72rem;
  color: var(--subtle);
}

/* Read-only Anzeige — kein Fokus-Ring, kein Edit-Cursor */
.svc-field-readonly {
  background: var(--panel-deep);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 10px;
  color: var(--subtle);
  font-size: 0.85rem;
  font-family: var(--font-mono);
  user-select: all;
}

/* URL-Prefix (z.B. "https://") vor einem Input */
.svc-input-prefix {
  display: flex;
  align-items: stretch;
}

.svc-input-prefix-label {
  background: var(--panel-deep);
  border: 1px solid var(--border);
  border-right: none;
  border-radius: 6px 0 0 6px;
  padding: 8px 10px;
  color: var(--subtle);
  font-size: 0.8rem;
  white-space: nowrap;
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.svc-input-prefix > input {
  border-radius: 0 6px 6px 0;
  flex: 1;
  min-width: 0;
  /* Basis-Styling — .svc-field > input greift nicht für verschachtelte Inputs */
  background: var(--card-bg);
  border: 1px solid var(--border);
  padding: 8px 10px;
  color: var(--text);
  font-size: 0.85rem;
  font-family: inherit;
  box-sizing: border-box;
  transition: border-color var(--transition-fast);
}

.svc-input-prefix > input:focus {
  outline: none;
  border-color: var(--accent);
}

/* Secret / Password mit Auge-Toggle */
.svc-secret {
  display: flex;
  align-items: stretch;
}

.svc-secret > input {
  border-radius: 6px 0 0 6px;
  flex: 1;
  min-width: 0;
  /* Basis-Styling — .svc-field > input greift nicht für verschachtelte Inputs */
  background: var(--card-bg);
  border: 1px solid var(--border);
  padding: 8px 10px;
  color: var(--text);
  font-size: 0.85rem;
  font-family: inherit;
  box-sizing: border-box;
  transition: border-color var(--transition-fast);
}

.svc-secret > input:focus {
  outline: none;
  border-color: var(--accent);
}

.svc-secret-toggle {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-left: none;
  border-radius: 0 6px 6px 0;
  padding: 0 12px;
  color: var(--subtle);
  cursor: pointer;
  font-size: 0.82rem;
  display: flex;
  align-items: center;
  transition: color var(--transition-fast);
}

.svc-secret-toggle:hover { color: var(--text); }

/* Toggle-Switch (on = grün, off = grau) */
.svc-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.svc-toggle-track {
  width: 36px;
  height: 20px;
  background: var(--border-strong);
  border-radius: 10px;
  position: relative;
  flex-shrink: 0;
  transition: background var(--transition-fast);
}

.svc-toggle-thumb {
  position: absolute;
  left: 3px;
  top: 3px;
  width: 14px;
  height: 14px;
  background: var(--subtle);
  border-radius: 50%;
  transition: left var(--transition-fast), background var(--transition-fast);
}

.svc-toggle.on .svc-toggle-track { background: var(--success); }
.svc-toggle.on .svc-toggle-thumb { left: 19px; background: #fff; }

/* Warn-Variante: on = gelb */
.svc-toggle.warn.on .svc-toggle-track { background: var(--warning); }

.svc-toggle-label {
  font-size: 0.82rem;
  color: var(--text);
}

.svc-toggle-sublabel {
  font-size: 0.7rem;
  color: var(--subtle);
}

/* Form-Aktionsleiste */
.svc-form-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-top: 8px;
  flex-wrap: wrap;
}

.svc-form-hint {
  margin-left: auto;
  font-size: 0.72rem;
  color: var(--subtle);
  display: flex;
  align-items: center;
  gap: 6px;
}

@media (max-width: 768px) {
  .svc-form-hint { margin-left: 0; }
}
```

- [ ] **Schritt 2: In index.css einbinden**

In `css/index.css` am Ende (nach `@import "toast.css";`) folgende Zeile ergänzen:

```css
/* 6. Service-Dashboard */
@import "service-dashboard.css";
```

- [ ] **Schritt 3: Commit**

```bash
git add css/service-dashboard.css css/index.css
git commit -m "feat(service-dashboard): add service-dashboard.css with svc-* classes"
```

---

## Task 2: Referenz-HTML — Übersichtsseite

**Files:**
- Create: `components/service-dashboard-overview.html`

Diese Seite zeigt das Kachelgrid mit vier Diensten (online, offline, unknown, nicht-klickbar). Sie demonstriert `.svc-card-icon`, `.svc-info-line`, `.svc-status-line` sowie `.sidebar-status-dot.unknown`.

- [ ] **Schritt 1: HTML-Datei erstellen**

Datei `components/service-dashboard-overview.html` mit folgendem Inhalt:

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Service Dashboard: Übersicht</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/topbar.css">
<link rel="stylesheet" href="../css/sidebar.css">
<link rel="stylesheet" href="../css/page.css">
<link rel="stylesheet" href="../css/cards.css">
<link rel="stylesheet" href="../css/badges.css">
<link rel="stylesheet" href="../css/service-dashboard.css">
<link rel="stylesheet" href="../css/demo.css">
</head>
<body>

<div class="sidebar-backdrop" id="sidebar-backdrop"></div>

<header class="topbar">
  <a href="#" class="brand">
    <img src="assets/logo.svg" alt="Logo" width="26" height="26">
    <span>Pi Dashboard</span>
  </a>
  <button class="topbar-menu-btn" id="sidebar-toggle" aria-label="Menü öffnen">
    <i class="fa-solid fa-bars"></i>
  </button>
</header>

<div class="layout">

  <nav class="sidebar" id="sidebar" aria-label="Dienste-Navigation">
    <div class="sidebar-inner">
      <div class="sidebar-section-label">Dienste</div>

      <a href="#" class="sidebar-nav-item active">
        <i class="fa-solid fa-grid-2 nav-icon"></i>
        Übersicht
        <div class="sidebar-status-dot online" style="margin-left:auto" title="3 von 4 online"></div>
      </a>
      <a href="service-dashboard-detail.html" class="sidebar-nav-item">
        <i class="fa-solid fa-satellite-dish nav-icon"></i>
        LoRa-Tracker
        <div class="sidebar-status-dot online"></div>
      </a>
      <a href="#" class="sidebar-nav-item">
        <i class="fa-solid fa-tower-broadcast nav-icon"></i>
        APRS-Gate
        <div class="sidebar-status-dot offline"></div>
      </a>
      <a href="#" class="sidebar-nav-item">
        <i class="fa-solid fa-cloud-sun nav-icon"></i>
        Wetterdienst
        <div class="sidebar-status-dot unknown"></div>
      </a>
      <a href="#" class="sidebar-nav-item">
        <i class="fa-solid fa-location-dot nav-icon"></i>
        GPS-Logger
        <div class="sidebar-status-dot online"></div>
      </a>
    </div>
    <div class="sidebar-footer">
      <span class="sidebar-footer-version">CI v1.12.0</span>
      <button class="sidebar-footer-copyright">© 2026 OE5ITH</button>
    </div>
  </nav>

  <div class="page-content">

    <div class="page-header">
      <div class="page-header-left">
        <h1 class="page-title">System-Übersicht</h1>
      </div>
    </div>

    <div class="content-body">

      <div class="demo-section">
        <div class="demo-section-title">Kacheln — klickbar (.card-dashboard-link)</div>
        <div class="demo-section-desc">
          Jede Kachel verlinkt auf eine Detail-Seite. Icon inline im h3 mit <code>.svc-card-icon</code>,
          Info-Zeile mit <code>.svc-info-line</code>, Statuszeile mit <code>.svc-status-line.online/offline/unknown</code>.
          Status-Dot kommt aus <code>cards.css .card-status-dot</code>.
        </div>

        <div class="card-grid">

          <!-- Online + klickbar -->
          <a href="service-dashboard-detail.html" class="card card-dashboard card-dashboard-link">
            <div class="card-status-dot online" title="Online"></div>
            <h3>
              <i class="fa-solid fa-satellite-dish svc-card-icon"></i>
              <span>LoRa-Tracker</span>
            </h3>
            <p class="svc-info-line">GPS Fix · 0.0 km/h</p>
            <span class="svc-status-line online">● Online · nächste TX in 4:58</span>
            <i class="fa-solid fa-arrow-right card-dashboard-arrow"></i>
          </a>

          <!-- Offline + klickbar -->
          <a href="#" class="card card-dashboard card-dashboard-link">
            <div class="card-status-dot offline" title="Offline"></div>
            <h3>
              <i class="fa-solid fa-tower-broadcast svc-card-icon"></i>
              <span>APRS-Gate</span>
            </h3>
            <p class="svc-info-line">aprs.fi · Port 14580</p>
            <span class="svc-status-line offline">● Offline · zuletzt gesehen vor 2h</span>
            <i class="fa-solid fa-arrow-right card-dashboard-arrow"></i>
          </a>

          <!-- Unknown + klickbar -->
          <a href="#" class="card card-dashboard card-dashboard-link">
            <div class="card-status-dot unknown" title="Status unbekannt"></div>
            <h3>
              <i class="fa-solid fa-cloud-sun svc-card-icon"></i>
              <span>Wetterdienst</span>
            </h3>
            <p class="svc-info-line">BME280 · I²C</p>
            <span class="svc-status-line unknown">● Unbekannt · API nicht erreichbar</span>
            <i class="fa-solid fa-arrow-right card-dashboard-arrow"></i>
          </a>

          <!-- Online + nicht klickbar (kein Link, keine Detail-Seite) -->
          <div class="card card-dashboard">
            <div class="card-status-dot online" title="Online"></div>
            <h3>
              <i class="fa-solid fa-location-dot svc-card-icon"></i>
              <span>GPS-Logger</span>
            </h3>
            <p class="svc-info-line">NMEA · /dev/ttyAMA0</p>
            <span class="svc-status-line online">● Online · 8 Satelliten</span>
          </div>

        </div>
      </div>

    </div>
  </div>
</div>

<script>
const toggle = document.getElementById('sidebar-toggle');
const sidebar = document.getElementById('sidebar');
const backdrop = document.getElementById('sidebar-backdrop');
if (toggle) {
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    backdrop.classList.toggle('visible');
  });
  backdrop.addEventListener('click', () => {
    sidebar.classList.remove('open');
    backdrop.classList.remove('visible');
  });
}
</script>

</body>
</html>
```

- [ ] **Schritt 2: Im Browser öffnen und prüfen**

Datei im Browser öffnen: `components/service-dashboard-overview.html`

Prüfpunkte:
- Vier Kacheln im 3-Spalten-Grid (Desktop)
- Icon inline neben dem Dienst-Namen, in `--accent` (blau)
- Status-Dots oben rechts: grün / rot / gelb / grün
- Statuszeile in korrekter Farbe: grün / rot / gelb / grün
- Hover auf klickbaren Kacheln: `translateY(-5px)` + blauer Rahmen + Pfeil rechts unten
- Auf Tablet (≤1024px): 2 Spalten; auf Mobile (≤768px): 1 Spalte
- Sidebar: Status-Dots inkl. gelbem Dot für "Wetterdienst" (`.sidebar-status-dot.unknown`)

- [ ] **Schritt 3: Commit**

```bash
git add components/service-dashboard-overview.html
git commit -m "feat(service-dashboard): add overview reference HTML"
```

---

## Task 3: Referenz-HTML — Detail-Seite

**Files:**
- Create: `components/service-dashboard-detail.html`

Diese Seite zeigt einen einzelnen Dienst mit Page-Header (Icon + Titel + Badge + Aktions-Buttons), Live-Status-Panel mit `.svc-data-grid` und den Hinweis zur Neustart-Bestätigung.

- [ ] **Schritt 1: HTML-Datei erstellen**

Datei `components/service-dashboard-detail.html` mit folgendem Inhalt:

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Service Dashboard: Detail</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/topbar.css">
<link rel="stylesheet" href="../css/sidebar.css">
<link rel="stylesheet" href="../css/page.css">
<link rel="stylesheet" href="../css/cards.css">
<link rel="stylesheet" href="../css/badges.css">
<link rel="stylesheet" href="../css/buttons.css">
<link rel="stylesheet" href="../css/service-dashboard.css">
<link rel="stylesheet" href="../css/demo.css">
</head>
<body>

<div class="sidebar-backdrop" id="sidebar-backdrop"></div>

<header class="topbar">
  <a href="#" class="brand">
    <img src="assets/logo.svg" alt="Logo" width="26" height="26">
    <span>Pi Dashboard</span>
  </a>
  <button class="topbar-menu-btn" id="sidebar-toggle" aria-label="Menü öffnen">
    <i class="fa-solid fa-bars"></i>
  </button>
</header>

<div class="layout">

  <nav class="sidebar" id="sidebar" aria-label="Dienste-Navigation">
    <div class="sidebar-inner">
      <div class="sidebar-section-label">Dienste</div>
      <a href="service-dashboard-overview.html" class="sidebar-nav-item">
        <i class="fa-solid fa-grid-2 nav-icon"></i>
        Übersicht
      </a>
      <a href="#" class="sidebar-nav-item active">
        <i class="fa-solid fa-satellite-dish nav-icon"></i>
        LoRa-Tracker
        <div class="sidebar-status-dot online"></div>
      </a>
      <a href="#" class="sidebar-nav-item">
        <i class="fa-solid fa-tower-broadcast nav-icon"></i>
        APRS-Gate
        <div class="sidebar-status-dot offline"></div>
      </a>
      <a href="#" class="sidebar-nav-item">
        <i class="fa-solid fa-cloud-sun nav-icon"></i>
        Wetterdienst
        <div class="sidebar-status-dot unknown"></div>
      </a>
    </div>
    <div class="sidebar-footer">
      <span class="sidebar-footer-version">CI v1.12.0</span>
      <button class="sidebar-footer-copyright">© 2026 OE5ITH</button>
    </div>
  </nav>

  <div class="page-content">

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
        <!-- Nur Aktionen einblenden, die die API anbietet (hier: restart) -->
        <button class="btn btn-danger" onclick="confirmRestart()">
          <i class="fa-solid fa-rotate-right"></i> Neustart
        </button>
        <a href="service-dashboard-config.html" class="btn btn-secondary">
          <i class="fa-solid fa-sliders"></i> Config
        </a>
      </div>
    </div>

    <div class="content-body">

      <!-- Live-Status-Panel -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <i class="fa-solid fa-chart-line"></i>
            Live-Status
          </div>
          <div class="panel-header-right">
            <span class="panel-meta">aktualisiert vor 12s</span>
          </div>
        </div>
        <div class="panel-body">
          <div class="svc-data-grid">

            <div class="svc-data-cell">
              <span class="svc-data-label">GPS Fix</span>
              <span class="svc-data-value success">Gültig</span>
              <span class="svc-data-sub">48.2643° / 14.2649°</span>
            </div>

            <div class="svc-data-cell">
              <span class="svc-data-label">Geschwindigkeit</span>
              <span class="svc-data-value">0.018 km/h</span>
              <span class="svc-data-sub">stationär</span>
            </div>

            <div class="svc-data-cell">
              <span class="svc-data-label">Nächste TX</span>
              <span class="svc-data-value">4:58</span>
              <span class="svc-data-sub">300s Intervall · fixed</span>
            </div>

            <div class="svc-data-cell">
              <span class="svc-data-label">Payload</span>
              <span class="svc-data-value">31 Bytes</span>
              <span class="svc-data-sub">GPS + Telemetrie</span>
            </div>

            <div class="svc-data-cell">
              <span class="svc-data-label">Strategie</span>
              <span class="svc-data-value">fixed</span>
              <span class="svc-data-sub">festes Intervall</span>
            </div>

            <div class="svc-data-cell">
              <span class="svc-data-label">Dienst</span>
              <span class="svc-data-value success">Aktiv</span>
              <span class="svc-data-sub">service_active: true</span>
            </div>

          </div>
        </div>
      </div>

      <!-- Hinweis: Neustart-Bestätigung -->
      <div class="card-warn">
        <i class="fa-solid fa-triangle-exclamation" style="margin-right:6px;"></i>
        Neustart unterbricht die TX-Sequenz. Der Button öffnet eine Bestätigungsabfrage vor der Ausführung.
      </div>

      <!-- Demo-Variante: Dienst offline -->
      <div class="demo-section">
        <div class="demo-section-title">Variante — Dienst offline</div>
        <div class="demo-section-desc">
          Bei Offline-Dienst: Badge <code>.badge-red</code>, Datenzellen zeigen letzten bekannten Wert in <code>--muted</code>.
        </div>
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">
              <i class="fa-solid fa-tower-broadcast"></i>
              APRS-Gate
            </div>
            <div class="panel-header-right">
              <span class="badge badge-red">OFFLINE</span>
            </div>
          </div>
          <div class="panel-body">
            <div class="svc-data-grid">
              <div class="svc-data-cell">
                <span class="svc-data-label">Status</span>
                <span class="svc-data-value danger">Nicht erreichbar</span>
                <span class="svc-data-sub">Letzter Kontakt vor 2h</span>
              </div>
              <div class="svc-data-cell">
                <span class="svc-data-label">Port</span>
                <span class="svc-data-value">14580</span>
                <span class="svc-data-sub">aprs.fi</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</div>

<script>
const toggle = document.getElementById('sidebar-toggle');
const sidebar = document.getElementById('sidebar');
const backdrop = document.getElementById('sidebar-backdrop');
if (toggle) {
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    backdrop.classList.toggle('visible');
  });
  backdrop.addEventListener('click', () => {
    sidebar.classList.remove('open');
    backdrop.classList.remove('visible');
  });
}

function confirmRestart() {
  if (confirm('LoRa-Tracker wirklich neu starten?\nDie laufende TX-Sequenz wird unterbrochen.')) {
    alert('POST /api/service/restart würde hier ausgeführt.');
  }
}
</script>

</body>
</html>
```

- [ ] **Schritt 2: Im Browser öffnen und prüfen**

Datei `components/service-dashboard-detail.html` im Browser öffnen.

Prüfpunkte:
- Page-Header: Icon blau, Titel, grünes ONLINE-Badge, zwei Buttons (roter Neustart, blauer Config)
- Neustart-Button: Klick öffnet `confirm()`-Dialog
- Data-Grid: 6 Zellen in 3 Spalten, Label uppercase grau, Wert fett, Subtext klein
- "GPS Fix" und "Dienst" Werte in grün (`svc-data-value.success`)
- Warn-Box (gelber linker Rand) unter dem Panel
- Offline-Variante unten: rotes OFFLINE-Badge, `svc-data-value.danger` rot
- Tablet/Mobile: Grid bricht auf 2/1 Spalten um

- [ ] **Schritt 3: Commit**

```bash
git add components/service-dashboard-detail.html
git commit -m "feat(service-dashboard): add detail reference HTML"
```

---

## Task 4: Referenz-HTML — Config-Seite

**Files:**
- Create: `components/service-dashboard-config.html`

Diese Seite demonstriert alle Config-Feldtypen: Text, Zahl, Select, Read-only, Secret, URL-Prefix, Toggle (normal + warn), Textarea. Zurück-Link zur Detail-Seite, Speichern/Abbrechen-Leiste unten.

- [ ] **Schritt 1: HTML-Datei erstellen**

Datei `components/service-dashboard-config.html` mit folgendem Inhalt:

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Service Dashboard: Config</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/topbar.css">
<link rel="stylesheet" href="../css/sidebar.css">
<link rel="stylesheet" href="../css/page.css">
<link rel="stylesheet" href="../css/badges.css">
<link rel="stylesheet" href="../css/buttons.css">
<link rel="stylesheet" href="../css/service-dashboard.css">
<link rel="stylesheet" href="../css/demo.css">
</head>
<body>

<div class="sidebar-backdrop" id="sidebar-backdrop"></div>

<header class="topbar">
  <a href="#" class="brand">
    <img src="assets/logo.svg" alt="Logo" width="26" height="26">
    <span>Pi Dashboard</span>
  </a>
  <button class="topbar-menu-btn" id="sidebar-toggle" aria-label="Menü öffnen">
    <i class="fa-solid fa-bars"></i>
  </button>
</header>

<div class="layout">

  <nav class="sidebar" id="sidebar" aria-label="Dienste-Navigation">
    <div class="sidebar-inner">
      <div class="sidebar-section-label">Dienste</div>
      <a href="service-dashboard-overview.html" class="sidebar-nav-item">
        <i class="fa-solid fa-grid-2 nav-icon"></i>
        Übersicht
      </a>
      <a href="service-dashboard-detail.html" class="sidebar-nav-item active">
        <i class="fa-solid fa-satellite-dish nav-icon"></i>
        LoRa-Tracker
        <div class="sidebar-status-dot online"></div>
      </a>
      <a href="#" class="sidebar-nav-item">
        <i class="fa-solid fa-tower-broadcast nav-icon"></i>
        APRS-Gate
        <div class="sidebar-status-dot offline"></div>
      </a>
    </div>
    <div class="sidebar-footer">
      <span class="sidebar-footer-version">CI v1.12.0</span>
      <button class="sidebar-footer-copyright">© 2026 OE5ITH</button>
    </div>
  </nav>

  <div class="page-content">

    <div class="page-header">
      <div class="page-header-left">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
          <i class="fa-solid fa-sliders svc-page-icon"></i>
          <h1 class="page-title" style="font-size:1.2rem;font-weight:600;">Konfiguration — LoRa-Tracker</h1>
        </div>
      </div>
    </div>

    <div class="content-body">

      <a href="service-dashboard-detail.html" class="svc-back-link">
        <i class="fa-solid fa-arrow-left"></i> Zurück zur Detail-Seite
      </a>

      <!-- Panel: Text / Zahl / Select / Read-only -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <i class="fa-solid fa-pen-to-square"></i>
            Einfache Felder
          </div>
          <span class="panel-meta">Text · Zahl · Auswahl · Read-only</span>
        </div>
        <div class="panel-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">

            <div class="svc-field">
              <label for="cfg-host">API-Host <span style="font-weight:400;color:var(--subtle)">(Text)</span></label>
              <input type="text" id="cfg-host" value="0.0.0.0">
              <span class="svc-field-hint">Bind-Adresse des API-Servers</span>
            </div>

            <div class="svc-field">
              <label for="cfg-port">API-Port <span style="font-weight:400;color:var(--subtle)">(Zahl)</span></label>
              <input type="number" id="cfg-port" value="8000" min="1024" max="65535">
              <span class="svc-field-hint">1024–65535</span>
            </div>

            <div class="svc-field">
              <label for="cfg-strategy">Beacon-Strategie <span style="font-weight:400;color:var(--subtle)">(Auswahl)</span></label>
              <select id="cfg-strategy">
                <option selected>fixed</option>
                <option>adaptive</option>
                <option>on-movement</option>
              </select>
              <span class="svc-field-hint">Bestimmt wann gesendet wird</span>
            </div>

            <div class="svc-field">
              <label>Firmware-Version <span style="font-weight:400;color:var(--subtle)">(Read-only)</span></label>
              <div class="svc-field-readonly">v2.3.1-stable</div>
              <span class="svc-field-hint">Kann nicht über die API geändert werden</span>
            </div>

            <div class="svc-field">
              <label for="cfg-tx">TX-Intervall <span style="font-weight:400;color:var(--subtle)">(Sekunden)</span></label>
              <input type="number" id="cfg-tx" value="300" min="60">
              <span class="svc-field-hint">Mindestens 60s empfohlen (Fair Use)</span>
            </div>

            <div class="svc-field">
              <label for="cfg-gps-timeout">GPS-Timeout <span style="font-weight:400;color:var(--subtle)">(Sekunden)</span></label>
              <input type="number" id="cfg-gps-timeout" value="30" min="5">
              <span class="svc-field-hint">Wartezeit auf gültigen GPS-Fix</span>
            </div>

          </div>
        </div>
      </div>

      <!-- Panel: Secret / URL-Prefix -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <i class="fa-solid fa-key"></i>
            Zugangsdaten &amp; Verbindungen
          </div>
          <span class="panel-meta">Secret · URL</span>
        </div>
        <div class="panel-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">

            <div class="svc-field">
              <label>API-Key <span style="font-weight:400;color:var(--subtle)">(Secret)</span></label>
              <div class="svc-secret">
                <input type="password" id="cfg-apikey" value="sk-abc123xyz">
                <button class="svc-secret-toggle" onclick="toggleSecret('cfg-apikey', this)" type="button">
                  <i class="fa-solid fa-eye"></i>
                </button>
              </div>
              <span class="svc-field-hint">Wird maskiert gespeichert</span>
            </div>

            <div class="svc-field">
              <label>Network-Server <span style="font-weight:400;color:var(--subtle)">(URL)</span></label>
              <div class="svc-input-prefix">
                <span class="svc-input-prefix-label">https://</span>
                <input type="text" value="router.oe5ith.at:1700" style="font-family:var(--font-mono);">
              </div>
              <span class="svc-field-hint">LoRaWAN Network Server</span>
            </div>

          </div>
        </div>
      </div>

      <!-- Panel: Toggles -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <i class="fa-solid fa-toggle-on"></i>
            Schalter
          </div>
          <span class="panel-meta">Boolean-Felder</span>
        </div>
        <div class="panel-body">
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">

            <div class="svc-toggle on" onclick="toggleSwitch(this)">
              <div class="svc-toggle-track">
                <div class="svc-toggle-thumb"></div>
              </div>
              <div>
                <div class="svc-toggle-label">GPS aktiviert</div>
                <div class="svc-toggle-sublabel">payload_gps</div>
              </div>
            </div>

            <div class="svc-toggle" onclick="toggleSwitch(this)">
              <div class="svc-toggle-track">
                <div class="svc-toggle-thumb"></div>
              </div>
              <div>
                <div class="svc-toggle-label">Debug-Logging</div>
                <div class="svc-toggle-sublabel">debug_mode</div>
              </div>
            </div>

            <div class="svc-toggle on" onclick="toggleSwitch(this)">
              <div class="svc-toggle-track">
                <div class="svc-toggle-thumb"></div>
              </div>
              <div>
                <div class="svc-toggle-label">CPU-Temperatur</div>
                <div class="svc-toggle-sublabel">payload_cpu_temp</div>
              </div>
            </div>

            <div class="svc-toggle on" onclick="toggleSwitch(this)">
              <div class="svc-toggle-track">
                <div class="svc-toggle-thumb"></div>
              </div>
              <div>
                <div class="svc-toggle-label">WiFi-RSSI</div>
                <div class="svc-toggle-sublabel">payload_wifi_rssi</div>
              </div>
            </div>

            <div class="svc-toggle on" onclick="toggleSwitch(this)">
              <div class="svc-toggle-track">
                <div class="svc-toggle-thumb"></div>
              </div>
              <div>
                <div class="svc-toggle-label">RAM</div>
                <div class="svc-toggle-sublabel">payload_ram</div>
              </div>
            </div>

            <!-- warn-Variante: gelb wenn aktiv -->
            <div class="svc-toggle warn on" onclick="toggleSwitch(this)">
              <div class="svc-toggle-track">
                <div class="svc-toggle-thumb"></div>
              </div>
              <div>
                <div class="svc-toggle-label">Senden ohne Fix</div>
                <div class="svc-toggle-sublabel" style="color:var(--warning);">⚠ sendet ungültige Pos.</div>
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- Panel: Textarea -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <i class="fa-solid fa-align-left"></i>
            Mehrzeilig
          </div>
          <span class="panel-meta">Freitext · JSON</span>
        </div>
        <div class="panel-body">
          <div class="svc-field">
            <label for="cfg-meta">Zusatz-Metadaten <span style="font-weight:400;color:var(--subtle)">(JSON)</span></label>
            <textarea id="cfg-meta" rows="4" style="font-family:var(--font-mono);font-size:.8rem;color:#4ade80;resize:vertical;">{"comment": "Test-Pi OE5ITH-3",
  "location": "Linz/AUT"}</textarea>
            <span class="svc-field-hint">Optional · wird unverändert weitergegeben</span>
          </div>
        </div>
      </div>

      <!-- Aktionsleiste -->
      <div class="svc-form-actions">
        <button class="btn btn-primary" type="button" onclick="alert('POST /api/config würde hier ausgeführt.')">
          <i class="fa-solid fa-floppy-disk"></i> Speichern
        </button>
        <a href="service-dashboard-detail.html" class="btn btn-ghost">Abbrechen</a>
        <span class="svc-form-hint">
          <i class="fa-solid fa-rotate"></i> Neustart erforderlich nach Speichern
        </span>
      </div>

    </div>
  </div>
</div>

<script>
const toggle = document.getElementById('sidebar-toggle');
const sidebar = document.getElementById('sidebar');
const backdrop = document.getElementById('sidebar-backdrop');
if (toggle) {
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    backdrop.classList.toggle('visible');
  });
  backdrop.addEventListener('click', () => {
    sidebar.classList.remove('open');
    backdrop.classList.remove('visible');
  });
}

function toggleSecret(id, btn) {
  const input = document.getElementById(id);
  const isHidden = input.type === 'password';
  input.type = isHidden ? 'text' : 'password';
  btn.innerHTML = isHidden
    ? '<i class="fa-solid fa-eye-slash"></i>'
    : '<i class="fa-solid fa-eye"></i>';
}

function toggleSwitch(el) {
  el.classList.toggle('on');
}
</script>

</body>
</html>
```

- [ ] **Schritt 2: Im Browser öffnen und prüfen**

Datei `components/service-dashboard-config.html` im Browser öffnen.

Prüfpunkte:
- Zurück-Link oben in `--muted`, hover in `--text`
- Alle vier Panels mit Trennlinie Header/Body
- Text/Zahl/Select-Felder: dark background, focus ergibt blauen Rahmen
- Read-only-Feld: dunkler, mono, kein Fokusring
- Secret-Feld: Passwort maskiert, Auge-Button schaltet um
- URL-Prefix: grau-blauer Prefix-Block bündig an Input
- Toggles: aktive grün, `warn on` gelb, Klick schaltet um
- Textarea: monospace, grüne Schrift auf dunklem Grund
- Aktionsleiste: Speichern blau, Abbrechen ghost, Hinweis rechts

- [ ] **Schritt 3: Commit**

```bash
git add components/service-dashboard-config.html
git commit -m "feat(service-dashboard): add config reference HTML"
```

---

## Task 5: Dokumentation

**Files:**
- Create: `docs/service-dashboard.md`

- [ ] **Schritt 1: Dokumentationsdatei erstellen**

Datei `docs/service-dashboard.md` anlegen:

```markdown
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
```

- [ ] **Schritt 2: Commit**

```bash
git add docs/service-dashboard.md
git commit -m "docs(service-dashboard): add component documentation"
```

---

## Task 6: CHANGELOG und Release v1.12.0

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Schritt 1: CHANGELOG-Eintrag ergänzen**

In `CHANGELOG.md` nach der Titelzeile und vor dem ersten bestehenden Eintrag (`## v1.11.2`) folgendes einfügen:

```markdown
## v1.12.0 - 2026-06-07

### Added
- **service-dashboard.css** (neu): CI-Baustein für lokale Raspberry-Pi-Dienst-Überwachung.
  - `.svc-card-icon`, `.svc-info-line`, `.svc-status-line.online/offline/unknown` — Kachel-Elemente für die Übersichtsseite
  - `.svc-page-icon` — FA-Icon im Page-Header der Detail-Seite
  - `.svc-data-grid`, `.svc-data-cell`, `.svc-data-label`, `.svc-data-value`, `.svc-data-sub` — Live-Status-Datenpanel
  - `.svc-back-link` — Zurück-Navigation auf der Config-Seite
  - `.svc-field`, `.svc-field-readonly`, `.svc-field-hint` — Formular-Feld-Wrapper
  - `.svc-input-prefix`, `.svc-input-prefix-label` — URL-Felder mit Protokoll-Prefix
  - `.svc-secret`, `.svc-secret-toggle` — Passwort-Felder mit Auge-Toggle
  - `.svc-toggle`, `.svc-toggle.warn`, `.svc-toggle-track`, `.svc-toggle-thumb`, `.svc-toggle-label`, `.svc-toggle-sublabel` — Toggle-Switch für Boolean-Config-Felder
  - `.svc-form-actions`, `.svc-form-hint` — Aktionsleiste auf der Config-Seite
  - `.sidebar-status-dot.unknown` — fehlende unknown-Variante für Sidebar-Dots ergänzt
- Drei neue Referenz-HTML-Seiten: `components/service-dashboard-overview.html`, `components/service-dashboard-detail.html`, `components/service-dashboard-config.html`
- Dokumentation: `docs/service-dashboard.md`

---
```

- [ ] **Schritt 2: Commit und Tag**

```bash
git add CHANGELOG.md
git commit -m "chore(release): v1.12.0 — service-dashboard CI component"
git tag -a v1.12.0 -m "Release v1.12.0 — service-dashboard CI component"
```

- [ ] **Schritt 3: Tag pushen (nach Review)**

```bash
git push origin main
git push origin v1.12.0
```

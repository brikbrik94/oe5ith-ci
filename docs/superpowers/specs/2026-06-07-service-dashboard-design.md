# Service Dashboard — Design-Spec

**Datum:** 2026-06-07  
**Status:** genehmigt  
**Scope:** Neuer CI-Baustein für lokale Raspberry-Pi-Dienst-Überwachung

---

## Überblick

Ein neuer CI-Baustein `service-dashboard` ermöglicht eine lokale Webseite pro Raspberry Pi, die alle darauf laufenden Dienste überwacht und verwaltet. Die Startseite zeigt Dienst-Kacheln mit Status; ein Klick führt zur Detail-Seite mit Live-Daten und Aktionen; eine separate Config-Seite erlaubt die Konfiguration des Dienstes.

---

## Architektur

### Ansatz: Minimale Erweiterung

Eine neue Datei `css/service-dashboard.css` ergänzt das CI mit ausschließlich den Klassen, die kein bestehendes Muster abdecken. Alles andere (Card-Grid, Panels, Buttons, Formulare) kommt aus vorhandenen CI-Dateien.

### Neue Dateien

| Datei | Zweck |
|---|---|
| `css/service-dashboard.css` | Neue Klassen für Dienst-Überwachung |
| `docs/service-dashboard.md` | Dokumentation des Bausteins |
| `components/service-dashboard-overview.html` | Referenz: Übersichtsseite |
| `components/service-dashboard-detail.html` | Referenz: Detail-Seite |
| `components/service-dashboard-config.html` | Referenz: Config-Seite |

### CSS-Ladereihenfolge

```
css/common.css
css/typography.css
css/cards.css
css/buttons.css
css/forms.css
css/page.css
css/sidebar.css
css/topbar.css
css/service-dashboard.css   ← nach allen anderen
```

### Kein JavaScript

`service-dashboard.css` enthält kein JS. API-Polling, Status-Updates und Button-Handling implementiert der Entwickler selbst.

---

## Seite 1 — Übersicht (Seitentyp 3: Dashboard)

### Funktion

Startseite des Pi-Dashboards. Zeigt alle konfigurierten Dienste als klickbare Kacheln mit Status-Dot und Info-Zeile.

### HTML-Struktur

```html
<div class="card-grid">
  <a href="/lora-tracker" class="card card-dashboard card-dashboard-link">
    <div class="card-status-dot online"></div>
    <h3>
      <i class="fa-solid fa-satellite-dish svc-card-icon"></i>
      LoRa-Tracker
    </h3>
    <p class="svc-info-line">GPS Fix · 0.0 km/h</p>
    <span class="svc-status-line online">● Online · TX in 4:58</span>
    <i class="fa-solid fa-arrow-right card-dashboard-arrow"></i>
  </a>
</div>
```

### Responsive Grid

| Breakpoint | Spalten |
|---|---|
| Desktop ≥1025px | 3 |
| Tablet 769–1024px | 2 |
| Mobile ≤768px | 1 |

Kommt aus bestehendem `.card-grid` — kein neues CSS.

### Neue Klassen (Übersicht)

| Klasse | Zweck |
|---|---|
| `.svc-card-icon` | FA-Icon inline im Titel; Farbe `--accent`, Größe 0.85rem, flex-shrink 0 |
| `.svc-info-line` | Kurzbeschreibung unter dem Titel (font-size 0.75rem, color `--muted`) |
| `.svc-status-line` | Statuszeile unten in der Kachel (font-size 0.7rem) |
| `.svc-status-line.online` | Farbe `--success` |
| `.svc-status-line.offline` | Farbe `--danger` |
| `.svc-status-line.unknown` | Farbe `--warning` |

---

## Seite 2 — Detail (Seitentyp 1: Detail-Seite)

### Funktion

Zeigt Live-Status-Daten eines einzelnen Dienstes und bietet dynamische Aktions-Buttons basierend auf den von der API angebotenen Endpunkten.

### Page-Header

```html
<div class="page-header">
  <div class="page-header-title">
    <i class="fa-solid fa-satellite-dish svc-page-icon"></i>
    <h1>LoRa-Tracker</h1>
    <span class="badge badge-green">ONLINE</span>
  </div>
  <div class="page-header-meta">GPS-Tracking · LoRaWAN · TTN</div>
  <div class="page-action">
    <!-- Nur Endpunkte einblenden, die die API anbietet -->
    <button class="btn btn-danger">
      <i class="fa-solid fa-rotate-right"></i> Neustart
    </button>
    <a href="/lora-tracker/config" class="btn btn-secondary">
      <i class="fa-solid fa-sliders"></i> Config
    </a>
  </div>
</div>
```

### Live-Status-Panel

```html
<div class="panel">
  <div class="panel-header">
    <i class="fa-solid fa-chart-line"></i> Live-Status
    <span class="panel-meta">aktualisiert vor 12s</span>
  </div>
  <div class="panel-body">
    <div class="svc-data-grid">
      <div class="svc-data-cell">
        <span class="svc-data-label">GPS Fix</span>
        <span class="svc-data-value success">Gültig</span>
        <span class="svc-data-sub">48.2643° / 14.2649°</span>
      </div>
      <!-- weitere Cells … -->
    </div>
  </div>
</div>
```

### Dynamische Aktionen

Die Aktions-Buttons werden clientseitig gerendert basierend auf den verfügbaren API-Endpunkten. Nur was die API anbietet erscheint. Der Restart-Button öffnet eine Bestätigungsabfrage bevor er feuert.

### Neue Klassen (Detail)

| Klasse | Zweck |
|---|---|
| `.svc-page-icon` | FA-Icon im Page-Header neben dem Titel |
| `badge badge-green` | ONLINE-Badge — bestehend aus `badges.css` |
| `badge badge-red` | OFFLINE-Badge — bestehend aus `badges.css` |
| `badge badge-yellow` | UNKNOWN-Badge — bestehend aus `badges.css` |
| `btn btn-danger` | Destruktive Aktion (Restart) — bestehend aus `buttons.css` |
| `btn btn-secondary` | Navigation/Config — bestehend aus `buttons.css` |
| `.svc-data-grid` | Responsive Grid für Key-Value-Datenzellen (3/2/1 Spalten) |
| `.svc-data-cell` | Einzelne Datenzelle: Label + Wert + Subtext |
| `.svc-data-label` | Feldbezeichnung (0.68rem, uppercase, `--subtle`) |
| `.svc-data-value` | Hauptwert (0.95rem, fett, `--text`) |
| `.svc-data-value.success` | Wert in `--success` |
| `.svc-data-value.danger` | Wert in `--danger` |
| `.svc-data-sub` | Subtext unter dem Wert (0.72rem, `--muted`) |

---

## Seite 3 — Config (Seitentyp 1: Detail-Seite)

### Funktion

Separate Seite zum Bearbeiten der Dienstkonfiguration via `POST /api/config`. Felder werden in thematischen Panels gruppiert. Speichern schickt alle geänderten Felder als JSON-Objekt.

### Zurück-Link

```html
<a href="/lora-tracker" class="svc-back-link">
  <i class="fa-solid fa-arrow-left"></i> Zurück
</a>
```

### Feldtypen

| Typ | Klasse / Element | Zweck |
|---|---|---|
| Text | `<input type="text">` + `.svc-field` | Strings, Hostnamen |
| Zahl | `<input type="number">` + `.svc-field` | Ports, Intervalle, Timeouts |
| Auswahl | `<select>` + `.svc-field` | Enum-Felder (z.B. Strategie) |
| Read-only | `.svc-field-readonly` | Nicht editierbare Werte (z.B. Firmware-Version) |
| Secret | `.svc-secret` | Passwörter/API-Keys mit Auge-Toggle |
| URL | `.svc-input-prefix` + `<input>` | URL-Felder mit Protokoll-Prefix |
| Toggle | `.svc-toggle` | Boolean-Felder (on = grün, off = grau) |
| Toggle Warnung | `.svc-toggle.warn` | Boolean mit Risiko (on = gelb) |
| Textarea | `<textarea>` | Freitext, JSON, Scripts |
| Hilfstext | `.svc-field-hint` | Erläuterung unter dem Feld |

### Aktionsleiste (Speichern)

```html
<div class="svc-form-actions">
  <button class="btn btn-primary">
    <i class="fa-solid fa-floppy-disk"></i> Speichern
  </button>
  <a href="/lora-tracker" class="btn btn-secondary">Abbrechen</a>
  <!-- Optional: -->
  <span class="svc-form-hint">
    <i class="fa-solid fa-rotate"></i> Neustart erforderlich nach Speichern
  </span>
</div>
```

### Neue Klassen (Config)

| Klasse | Zweck |
|---|---|
| `.svc-back-link` | Zurück-Link mit Pfeil oben links |
| `.svc-field` | Wrapper für Label + Input + Hint |
| `.svc-field-readonly` | Read-only Anzeige (dunkelgrau, kein Fokus-Ring) |
| `.svc-input-prefix` | Prefix-Block vor Input (z.B. "https://") |
| `.svc-secret` | Password-Feld-Wrapper mit Auge-Toggle-Button |
| `.svc-toggle` | Toggle-Switch-Element |
| `.svc-toggle.warn` | Toggle in Warnfarbe wenn aktiv |
| `.svc-field-hint` | Hilfstext unter Feld (0.72rem, `--subtle`) |
| `.svc-form-actions` | Aktionsleiste: Speichern + Abbrechen + optionaler Hinweis |
| `.svc-form-hint` | Hinweistext in der Aktionsleiste |

---

## Versionierung

Dieser Baustein ist eine **MINOR**-Ergänzung (neues CSS, neue Docs, neue Referenz-HTML — keine Breaking Changes).  
Version nach Fertigstellung: **v1.12.0**

---

## Erweiterbarkeit

Die Feldtypen-Palette (`svc-field`, `svc-toggle`, `svc-secret` etc.) ist generisch gehalten und nicht LoRa-spezifisch. Neue Feldtypen können jederzeit in `css/service-dashboard.css` ergänzt werden ohne Breaking Changes.

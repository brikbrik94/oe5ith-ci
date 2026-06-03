# Design-Spec: Kalender-Komponente

**Datum:** 2026-06-03  
**Status:** Spec — bereit zur Implementierung  
**Kontext:** Monatskalender für den Dienstplan im Internal Dashboard, gespeist aus einem ICS-Backend

---

## Ziel

Eine read-only Monatsübersicht die Dienstplan-Einträge aus einem ICS-Backend darstellt. Pro Tag bis zu 2 Einträge mit Titel und Uhrzeit, farblich nach Diensttyp codiert. Detailansicht per Modal. Navigation zwischen Monaten mit Zurück/Vor-Pfeilen und "Heute"-Button.

---

## Dateien

| Datei | Rolle |
|---|---|
| `css/calendar.css` | Neue CSS-Komponente |
| `components/calendar.html` | Referenzseite |
| `docs/calendar.md` | Dokumentation |
| `css/index.css` | Import ergänzen |

---

## HTML-Struktur

```html
<div class="calendar">

  <!-- Kopfzeile: Navigation -->
  <div class="calendar-header">
    <button class="calendar-nav-btn calendar-prev" aria-label="Vorheriger Monat">
      <i class="fa-solid fa-chevron-left"></i>
    </button>
    <span class="calendar-title">Juni 2026</span>
    <button class="calendar-nav-btn calendar-next" aria-label="Nächster Monat">
      <i class="fa-solid fa-chevron-right"></i>
    </button>
    <button class="calendar-today-btn">Heute</button>
  </div>

  <!-- Raster -->
  <div class="calendar-grid">

    <!-- Wochentag-Header (fest, 7 Spalten) -->
    <div class="calendar-weekday">Mo</div>
    <div class="calendar-weekday">Di</div>
    <div class="calendar-weekday">Mi</div>
    <div class="calendar-weekday">Do</div>
    <div class="calendar-weekday">Fr</div>
    <div class="calendar-weekday">Sa</div>
    <div class="calendar-weekday">So</div>

    <!-- Tageszelle — aktueller Monat -->
    <div class="calendar-day">
      <span class="calendar-day-number">3</span>
      <div class="calendar-entry calendar-entry--early"
           data-id="123" role="button" tabindex="0"
           aria-label="Frühdienst, 06:00–14:00, Details öffnen">
        <span class="calendar-entry-time">06:00–14:00</span>
        <span class="calendar-entry-title">Frühdienst</span>
      </div>
    </div>

    <!-- Tageszelle — heute -->
    <div class="calendar-day calendar-day--today">
      <span class="calendar-day-number">4</span>
      <div class="calendar-entry calendar-entry--night"
           data-id="124" role="button" tabindex="0"
           aria-label="Nachtdienst, 20:00–08:00, geändert, Details öffnen">
        <span class="calendar-entry-time">20:00–08:00</span>
        <span class="calendar-entry-title">Nachtdienst</span>
        <i class="fa-solid fa-circle-exclamation calendar-entry-changed"
           title="Zuletzt geändert: 01.06.2026"></i>
      </div>
    </div>

    <!-- Tageszelle — 2 Einträge -->
    <div class="calendar-day">
      <span class="calendar-day-number">5</span>
      <div class="calendar-entry calendar-entry--early" data-id="125" role="button" tabindex="0">
        <span class="calendar-entry-time">06:00–10:00</span>
        <span class="calendar-entry-title">Frühdienst A</span>
      </div>
      <div class="calendar-entry calendar-entry--night" data-id="126" role="button" tabindex="0">
        <span class="calendar-entry-time">22:00–06:00</span>
        <span class="calendar-entry-title">Nachtdienst B</span>
      </div>
    </div>

    <!-- Tageszelle — außerhalb des Monats -->
    <div class="calendar-day calendar-day--outside">
      <span class="calendar-day-number">30</span>
      <div class="calendar-entry calendar-entry--late" data-id="120" role="button" tabindex="0">
        <span class="calendar-entry-time">14:00–22:00</span>
        <span class="calendar-entry-title">Spätdienst</span>
      </div>
    </div>

    <!-- Leere Tageszelle -->
    <div class="calendar-day">
      <span class="calendar-day-number">6</span>
    </div>

  </div>
</div>

<!-- Detail-Modal (bestehende .modal-Komponente) -->
<div class="modal" id="calendar-modal" role="dialog" aria-modal="true" aria-labelledby="cal-modal-title">
  <div class="modal-content">
    <div class="modal-header">
      <h2 class="modal-title" id="cal-modal-title">Nachtdienst</h2>
      <span class="badge badge--auth">Nacht</span>
      <button class="modal-close" aria-label="Schließen">×</button>
    </div>
    <div class="modal-body">
      <p class="cal-modal-date">Dienstag, 03. Juni 2026</p>
      <p class="cal-modal-time">20:00 – 08:00</p>
      <p class="cal-modal-description">Beschreibung / Notizen vom Backend</p>
      <p class="cal-modal-location">Ort (falls vorhanden)</p>
      <!-- Nur sichtbar wenn Änderung vorhanden -->
      <div class="cal-modal-changed">
        <i class="fa-solid fa-circle-exclamation"></i>
        <span>Zuletzt geändert: 01.06.2026</span>
        <p class="cal-modal-changed-note">Änderungsnotiz vom Backend (optional)</p>
      </div>
    </div>
  </div>
</div>
```

---

## CSS-Konzept

### Layout

```css
.calendar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.calendar-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.calendar-title {
  flex: 1;
  text-align: center;
  font-size: 1.1rem;
  font-weight: 700;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}
```

### Wochentag-Header

```css
.calendar-weekday {
  background: var(--panel-deep);
  color: var(--muted);
  font-size: 0.75rem;
  font-weight: 600;
  text-align: center;
  padding: 6px 0;
  border-radius: 4px;
}
```

### Tageszelle

```css
.calendar-day {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.calendar-day--outside {
  opacity: 0.35;
}

.calendar-day--today .calendar-day-number {
  background: var(--accent);
  color: #fff;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.78rem;
  font-weight: 700;
}

.calendar-day-number {
  font-size: 0.78rem;
  color: var(--muted);
  font-weight: 600;
  margin-bottom: 2px;
}
```

### Einträge

```css
.calendar-entry {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 6px;
  border-radius: 4px;
  border-left: 3px solid;
  font-size: 0.72rem;
  cursor: pointer;
  transition: filter var(--transition-fast);
  position: relative;
}

.calendar-entry:hover { filter: brightness(1.15); }

.calendar-entry-time {
  color: var(--muted);
  white-space: nowrap;
  flex-shrink: 0;
}

.calendar-entry-title {
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.calendar-entry-changed {
  color: var(--warning);
  font-size: 0.7rem;
  flex-shrink: 0;
  margin-left: auto;
}
```

### Diensttyp-Modifier

```css
.calendar-entry--early {
  background: var(--success-subtle);
  border-color: var(--success);
}
.calendar-entry--late {
  background: var(--warning-subtle);
  border-color: var(--warning);
}
.calendar-entry--night {
  background: var(--auth-subtle);
  border-color: var(--auth);
}
.calendar-entry--default {
  background: var(--accent-subtle);
  border-color: var(--accent);
}
```

### Navigations-Buttons

```css
.calendar-nav-btn {
  background: none;
  border: none;
  color: var(--muted);
  padding: 6px 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: color var(--transition-fast), background var(--transition-fast);
}
.calendar-nav-btn:hover {
  color: var(--text);
  background: var(--surface-hover);
}

/* .calendar-today-btn verwendet .btn.btn--secondary aus buttons.css — keine eigene Regel */
```

### Mobile (≤768px)

```css
@media (max-width: 768px) {
  .calendar-grid {
    grid-template-columns: 1fr;
  }
  .calendar-weekday {
    display: none;
  }
  .calendar-day:not(:has(.calendar-entry)) {
    display: none;
  }
  .calendar-day {
    min-height: unset;
  }
  .calendar-day-number {
    font-size: 0.85rem;
  }
}
```

---

## Farbcodierung — Diensttypen

| Modifier-Klasse | Bedeutung | Tokens |
|---|---|---|
| `.calendar-entry--early` | Frühdienst | `--success-subtle` / `--success` |
| `.calendar-entry--late` | Spätdienst | `--warning-subtle` / `--warning` |
| `.calendar-entry--night` | Nachtdienst | `--auth-subtle` / `--auth` |
| `.calendar-entry--default` | Sonstiges / Fallback | `--accent-subtle` / `--accent` |

Der Diensttyp wird vom Backend als Klasse geliefert. Neue Typen können durch neue Modifier-Klassen ergänzt werden ohne bestehende Klassen zu ändern.

---

## Änderungsindikator

```html
<i class="fa-solid fa-circle-exclamation calendar-entry-changed"
   title="Zuletzt geändert: 01.06.2026"></i>
```

- Position: rechts in der Eintragszeile (`margin-left: auto`)
- Farbe: `--warning`
- Größe: `0.7rem`
- Nur im DOM wenn vom Backend gesetzt
- `title`-Attribut trägt das Änderungsdatum — kein eigener Tooltip-Mechanismus

---

## Detail-Modal

Wiederverwendung der bestehenden `.modal`-Komponente aus `css/modal.css`. Kein neues Modal-CSS.

**Inhalt:**
- Diensttyp-Badge (`.badge` mit passendem Modifier)
- Datum ausgeschrieben
- Uhrzeit Von–Bis
- Titel / Beschreibung
- Ort (optional, nur wenn Backend-Daten vorhanden)
- Änderungsblock (optional, nur wenn geändert): Icon + Datum + Notiz

**Öffnen:** Klick auf `.calendar-entry` (auch per Enter/Space da `role="button"` + `tabindex="0"`)  
**Schließen:** Klick auf `.modal-close`, Klick außerhalb, `Escape`

---

## Accessibility

| Element | Attribut |
|---|---|
| `.calendar-nav-btn` | `aria-label="Vorheriger/Nächster Monat"` |
| `.calendar-entry` | `role="button"`, `tabindex="0"`, `aria-label` mit Titel + Zeit + "geändert" falls zutreffend |
| `.modal` | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` |
| Escape | schließt Modal |

---

## Neue Tokens

Keine. Alle verwendeten Tokens sind in `css/common.css` bereits vorhanden.

---

## Nicht in dieser Spec

- Interaktive Tagauswahl / Datepicker
- Wochenansicht oder Tagesansicht
- Wiederholende Ereignisse (werden vom Backend bereits aufgelöst)
- Synchronisations-Status-Anzeige (separates Thema)

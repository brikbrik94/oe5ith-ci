# Kalender

**Referenz-Datei:** `components/calendar.html`  
**CSS:** `css/calendar.css`  
**Status:** definiert · v1.0

---

## Überblick

Monatskalender für die Darstellung von Dienstplan-Einträgen aus einem ICS-Backend.
Read-only. Einträge sind farblich nach Diensttyp codiert. Detailansicht per Modal.

**Struktur:** Freistehender Content-Block ohne Card-Wrapper — füllt `page-content` direkt.

---

## Ladereihenfolge

```
common.css → buttons.css → modal.css → calendar.css
```

---

## HTML-Struktur

```html
<div class="calendar">
  <div class="calendar-header">
    <button class="calendar-nav-btn calendar-prev" aria-label="Vorheriger Monat">
      <i class="fa-solid fa-chevron-left"></i>
    </button>
    <span class="calendar-title">Juni 2026</span>
    <button class="calendar-nav-btn calendar-next" aria-label="Nächster Monat">
      <i class="fa-solid fa-chevron-right"></i>
    </button>
    <button class="btn btn-secondary">Heute</button>
  </div>

  <div class="calendar-grid">
    <!-- 7 Wochentag-Header -->
    <div class="calendar-weekday">Mo</div>
    ...

    <!-- Tageszellen -->
    <div class="calendar-day">
      <span class="calendar-day-number">3</span>
      <div class="calendar-entry calendar-entry--night"
           role="button" tabindex="0"
           aria-label="Nachtdienst, 20:00–08:00, geändert, Details öffnen">
        <span class="calendar-entry-time">20:00</span>
        <span class="calendar-entry-title">Nachtdienst</span>
        <i class="fa-solid fa-circle-exclamation calendar-entry-changed"
           title="Zuletzt geändert: 01.06.2026"></i>
      </div>
    </div>
  </div>
</div>
```

---

## Tageszell-Modifier

| Klasse | Bedeutung |
|---|---|
| `.calendar-day--today` | Aktueller Tag — Tageszahl mit `--accent`-Kreis |
| `.calendar-day--outside` | Tag aus Vor-/Folgemonat — `opacity: 0.35` |

---

## Eintragstypen

| Modifier-Klasse | Diensttyp | Tokens |
|---|---|---|
| `.calendar-entry--early` | Frühdienst | `--success-subtle` / `--success` |
| `.calendar-entry--late` | Spätdienst | `--warning-subtle` / `--warning` |
| `.calendar-entry--night` | Nachtdienst | `--auth-subtle` / `--auth` |
| `.calendar-entry--default` | Sonstiges / Fallback | `--accent-subtle` / `--accent` |

Neue Diensttypen als neue Modifier-Klasse ergänzen — bestehende Klassen nicht ändern.

---

## Änderungsindikator

```html
<i class="fa-solid fa-circle-exclamation calendar-entry-changed"
   title="Zuletzt geändert: 01.06.2026"></i>
```

- Position: rechts in der Eintragszeile (`margin-left: auto`)
- Farbe: `--warning`
- Nur im DOM wenn vom Backend gesetzt
- Änderungsdatum im `title`-Attribut

---

## Bis zu 2 Einträge pro Tag

Beide Einträge werden als separate `.calendar-entry`-Elemente untereinander in der
`.calendar-day`-Zelle platziert. Die Zelle wächst mit dem Inhalt — keine feste Höhe.

---

## Detail-Modal

Wiederverwendung der bestehenden `.modal-backdrop` / `.modal`-Komponente aus `modal.css`.

**Inhalt:**
- Diensttyp-Badge (`.badge` mit passendem Modifier)
- Datum ausgeschrieben
- Uhrzeit Von–Bis
- Titel / Beschreibung
- Ort (optional)
- Änderungsblock (nur wenn geändert): `--warning`-Box mit Datum + optionaler Notiz

**Öffnen/Schließen:**
- Klick auf `.calendar-entry` öffnet Modal
- Klick auf `.modal-close`, Klick auf Backdrop, `Escape` schließt Modal

---

## Mobile (≤768px)

Das 7-Spalten-Grid kollabiert zu einer einspaltigen Liste.
Wochentag-Header werden ausgeblendet.
Leere Tageszellen (keine Einträge) werden ausgeblendet.

Hinweis: Mobile-Collapse verwendet `:has()` — benötigt einen modernen Browser (Baseline 2023).

---

## Außerhalb-Tage

Tage aus dem Vor- oder Folgemonat erhalten `.calendar-day--outside` (opacity: 0.35).
Einträge werden weiterhin angezeigt (mit reduzierter Sichtbarkeit).

---

## Neue Tokens

Keine. Alle Tokens kommen aus `css/common.css`.

---

## Accessibility

| Element | Attribut |
|---|---|
| `.calendar-nav-btn` | `aria-label="Vorheriger/Nächster Monat"` |
| `.calendar-entry` | `role="button"`, `tabindex="0"`, `aria-label` mit Titel + Zeit |
| `.modal-backdrop` | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` |
| Tastatur | Enter/Space öffnet Modal, Escape schließt |

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-03 | Initiale Definition. Vier Diensttypen, Änderungsindikator, Mobile-Collapse. |

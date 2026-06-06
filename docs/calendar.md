# Kalender

**Referenz-Datei:** `components/calendar.html`  
**CSS:** `css/calendar.css`  
**Status:** definiert · v1.2

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

## Generische Farbslots

| Modifier-Klasse | Token-Paar |
|---|---|
| `.calendar-entry--color-1` | `--cal-color-1-subtle` / `--cal-color-1` |
| `.calendar-entry--color-2` | `--cal-color-2-subtle` / `--cal-color-2` |
| `.calendar-entry--color-3` | `--cal-color-3-subtle` / `--cal-color-3` |
| `.calendar-entry--color-4` | `--cal-color-4-subtle` / `--cal-color-4` |
| `.calendar-entry--color-5` | `--cal-color-5-subtle` / `--cal-color-5` |
| `.calendar-entry--color-6` | `--cal-color-6-subtle` / `--cal-color-6` |
| `.calendar-entry--color-7` | `--cal-color-7-subtle` / `--cal-color-7` |
| `.calendar-entry--color-8` | `--cal-color-8-subtle` / `--cal-color-8` |
| `.calendar-entry--color-9` | `--cal-color-9-subtle` / `--cal-color-9` |
| `.calendar-entry--color-10` | `--cal-color-10-subtle` / `--cal-color-10` |

Die Standardfarben (grün, gelb, violett, blau, orange, rot, cyan, pink, limette, grau)
können pro Website überschrieben werden — siehe `docs/tokens.md`.

### Aliase (rückwärtskompatibel)

| Alias-Klasse | Entspricht |
|---|---|
| `.calendar-entry--early` | `--color-1` (grün) |
| `.calendar-entry--late` | `--color-2` (gelb) |
| `.calendar-entry--night` | `--color-3` (violett) |
| `.calendar-entry--default` | `--color-4` (blau) |

Neue Diensttypen als `--color-N`-Klasse ergänzen — Aliase nicht für neue Typen verwenden.

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

## Mehrtägige Events

Events die sich über mehrere Tage erstrecken, erscheinen in jeder Tageszelle einzeln.
Zwei Modifier-Klassen steuern die Fortsetzungsmarkierungen:

| Klasse | Bedeutung | Visuell |
|---|---|---|
| `.calendar-entry--continues-right` | Event geht am Folgetag weiter | `›` rechts via `::after` |
| `.calendar-entry--continues-left` | Event kommt vom Vortag | `‹` links via `::before`, `border-left` transparent |

Kombinierbar: Ein mittlerer Tag trägt beide Klassen.

```html
<!-- Tag 1: Starttag — zeigt Uhrzeit -->
<div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-right"
     role="button" tabindex="0"
     aria-label="Konferenz, 08:00, läuft weiter, Details öffnen">
  <span class="calendar-entry-time">08:00</span>
  <span class="calendar-entry-title">Konferenz</span>
</div>

<!-- Tag 2: Mitteltag — keine Uhrzeit -->
<div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-left calendar-entry--continues-right"
     role="button" tabindex="0"
     aria-label="Konferenz, Fortsetzung, Details öffnen">
  <span class="calendar-entry-title">Konferenz</span>
</div>

<!-- Tag 3: Endtag — keine Uhrzeit -->
<div class="calendar-entry calendar-entry--color-5 calendar-entry--continues-left"
     role="button" tabindex="0"
     aria-label="Konferenz, Fortsetzung, Details öffnen">
  <span class="calendar-entry-title">Konferenz</span>
</div>
```

**Uhrzeit-Regel:** Nur der Starttag enthält `.calendar-entry-time` im DOM.
Folgetage lassen das Element weg.

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

### Leere Tageszellen — Toggle

Standardmäßig werden leere Tageszellen (keine Einträge) ausgeblendet. Mit dem Modifier
`.calendar--show-all` auf `.calendar` werden alle Tageszellen angezeigt.

| Zustand | Klasse | Leere Tage |
|---|---|---|
| Kompakt (Standard) | _(kein Modifier)_ | ausgeblendet |
| Alle anzeigen | `.calendar--show-all` | sichtbar |

Die CI definiert die CSS-Klasse. Die Website setzt/entfernt sie per JavaScript nach eigenem Ermessen.

```html
<!-- Alle Tage anzeigen -->
<div class="calendar calendar--show-all">…</div>

<!-- Nur Tage mit Einträgen (Standard) -->
<div class="calendar">…</div>
```

Hinweis: Mobile-Collapse verwendet `:has()` — benötigt einen modernen Browser (Baseline 2023).

---

## Tablet (769px–1024px)

Das 7-Spalten-Grid bleibt erhalten. Eintragsinhalt wird automatisch komprimiert — kein
JavaScript, keine zusätzlichen Klassen erforderlich.

| Element | Desktop | Tablet |
|---|---|---|
| Tageszell-Padding | 6px | 4px |
| Min-Height Zelle | 80px | 64px |
| Entry-Schriftgröße | 0.72rem | 0.68rem |
| Uhrzeit | vollständig | nur Startzeit (max. 36px, abgeschnitten) |

Für Detailinformationen (vollständige Zeit, Beschreibung, Ort) öffnet der Nutzer das Modal.

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
| 2026-06-06 | Generische Farbslots `--color-1` bis `--color-10`. Aliase für bestehende Diensttypen. Mehrtägige Events mit `--continues-left` / `--continues-right`. |
| 2026-06-06 | Mobile Show-All-Toggle (`.calendar--show-all`). Tablet-Breakpoint 769px–1024px mit komprimierter Darstellung. |

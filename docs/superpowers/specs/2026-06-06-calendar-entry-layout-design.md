# Design-Spec: Kalender — Eintrags-Layout & Breitengrenze

**Datum:** 2026-06-06  
**Status:** Spec — bereit zur Implementierung  
**Kontext:** Kalender-Einträge dürfen den verfügbaren Platz nicht überschreiten. Websites sollen per Modifier-Klasse zwischen einzeiligem (Truncate) und mehrzeiligem (Wrap) Layout wählen können.

---

## Ziel

1. **Harte Breitengrenze** — Der Kalender darf nie breiter werden als sein Container. Sichergestellt durch `max-width: 100%` und `overflow: hidden` auf den relevanten Elementen.
2. **Mehrzeilen-Modifier** — `.calendar-entry--multiline` ermöglicht ein gestapeltes Layout: Zeit auf Zeile 1, Titel ab Zeile 2. Die Website entscheidet welchen Modus sie verwendet.

---

## Dateien

| Datei | Änderung |
|---|---|
| `css/calendar.css` | Breitengrenze auf `.calendar`, `.calendar-day`, `.calendar-entry` + neuer `--multiline` Modifier |
| `docs/calendar.md` | Neue Sektion „Eintrags-Layout", Änderungshistorie |
| `components/calendar.html` | Demo-Sektion für `--multiline` |

---

## Teil 1 — Harte Breitengrenze

Drei Ergänzungen an bestehenden Regeln — keine neuen Klassen:

```css
/* .calendar — bereits vorhanden, ergänzen */
.calendar {
  max-width: 100%;
  overflow: hidden;   /* NEU */
}

/* .calendar-day — bereits vorhanden, ergänzen */
.calendar-day {
  min-width: 0;       /* NEU — verhindert Flex-Overflow */
  overflow: hidden;   /* NEU */
}

/* .calendar-entry — bereits vorhanden, ergänzen */
.calendar-entry {
  max-width: 100%;    /* NEU */
}
```

Diese Regeln gelten immer, unabhängig vom gewählten Layout-Modifier.

---

## Teil 2 — `.calendar-entry--multiline` Modifier

### CSS

```css
/* ─── Mehrzeilen-Layout ─── */

.calendar-entry--multiline {
  flex-wrap: wrap;
  align-items: flex-start;
}

.calendar-entry--multiline .calendar-entry-time {
  flex-basis: 100%;
}

.calendar-entry--multiline .calendar-entry-title {
  white-space: normal;
  text-overflow: unset;
  overflow: visible;
}
```

### Visuelles Ergebnis

**Mit `--multiline`:**
```
┌──────────────────────┐
│ 08:00                │  ← Zeit (volle Breite, Zeile 1)
│ Frühdienst Station 1 │  ← Titel (umbricht bei Bedarf, Zeile 2+)
└──────────────────────┘
```

**Default (kein Modifier):**
```
┌──────────────────────┐
│ 08:00  Frühdienst… ⚠ │  ← einzeilig, Ellipsis bei Überlauf
└──────────────────────┘
```

### Änderungs-Icon

`.calendar-entry-changed` bleibt auf der Titelzeile rechts — `margin-left: auto` funktioniert weiterhin in beiden Modi.

### Einschränkung

Die Kombination von `.calendar-entry--multiline` mit `.calendar-entry--continues-left` / `--continues-right` wird nicht explizit gestylt. Websites sollen diese Kombinationen vermeiden.

### HTML-Beispiel

```html
<!-- Mehrzeilen-Eintrag -->
<div class="calendar-entry calendar-entry--color-1 calendar-entry--multiline"
     role="button" tabindex="0"
     aria-label="Frühdienst, 08:00, Details öffnen">
  <span class="calendar-entry-time">08:00</span>
  <span class="calendar-entry-title">Frühdienst Station 1</span>
</div>

<!-- Einzeiler (Default) -->
<div class="calendar-entry calendar-entry--color-1"
     role="button" tabindex="0"
     aria-label="Frühdienst, 08:00, Details öffnen">
  <span class="calendar-entry-time">08:00</span>
  <span class="calendar-entry-title">Frühdienst Station 1</span>
</div>
```

---

## Neue Tokens

Keine.

---

## Nicht in dieser Spec

- Kombination von `--multiline` und `--continues-left/right`
- Automatischer Wrap ohne Modifier (kein YAGNI)
- Zeilenzahl-Begrenzung via `line-clamp`

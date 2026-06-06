# Design-Spec: Kalender — Mobile Toggle & Tablet-Darstellung

**Datum:** 2026-06-06  
**Status:** Spec — bereit zur Implementierung  
**Kontext:** Erweiterung der bestehenden Kalender-Komponente um einen Mobile-Show-All-Toggle und eine optimierte Tablet-Darstellung.

---

## Ziel

1. **Mobile Toggle** — Auf Mobile (≤768px) kann die Website zwischen zwei Ansichten wechseln: nur Tage mit Einträgen, oder alle Tage. Die CI definiert die CSS-Klasse; die Website setzt sie per JS nach eigenem Ermessen.
2. **Tablet-Darstellung** — Auf Tablet (769px–1024px) bleibt das 7-Spalten-Grid, aber Eintragsinhalt wird komprimiert. Funktioniert automatisch ohne Klassen oder JS.

---

## Dateien

| Datei | Änderung |
|---|---|
| `css/calendar.css` | Mobile: `.calendar--show-all` Modifier + angepasster `:has()`-Selektor. Tablet: neuer `@media`-Block |
| `docs/calendar.md` | Dokumentation beider neuen Features |
| `components/calendar.html` | Demo-Beispiel für `.calendar--show-all` mit Toggle-Button |

---

## Teil 1 — Mobile Show-All-Toggle (≤768px)

### Konzept

Die CI definiert das Verhalten zweier Zustände über CSS. **Die Website** ist verantwortlich für:
- Den Toggle-Button (Platzierung, Label, Styling)
- Das Setzen/Entfernen der Klasse per JavaScript

### CSS-Logik

**Default (kein Modifier):** Leere Tageszellen werden ausgeblendet — bestehende Regel.

```css
@media (max-width: 768px) {
  .calendar-day:not(:has(.calendar-entry)) {
    display: none;
  }
}
```

**`.calendar--show-all`:** Alle Tageszellen werden angezeigt, auch leere.

```css
@media (max-width: 768px) {
  .calendar.calendar--show-all .calendar-day:not(:has(.calendar-entry)) {
    display: flex;
  }
}
```

Die höhere Spezifizität (`.calendar.calendar--show-all .calendar-day`) überschreibt die `:not(:has())` Regel.

### HTML-Struktur

```html
<!-- Kalender mit Show-All-Toggle aktiv -->
<div class="calendar calendar--show-all">
  ...
</div>

<!-- Kalender im Default (nur Tage mit Einträgen) -->
<div class="calendar">
  ...
</div>
```

### Referenzseite (`components/calendar.html`)

Die Referenzseite zeigt einen minimalen JS-Toggle als Beispiel:

```html
<button onclick="document.querySelector('.calendar').classList.toggle('calendar--show-all')">
  Alle Tage / Nur mit Termin
</button>
```

Dieser Button dient ausschließlich der Demonstration — kein Teil der CI-Klassen.

### Dokumentation

In `docs/calendar.md`: Neue Sektion „Mobile — Show-All-Toggle" mit:
- Erklärung der Klasse
- Hinweis dass die Website den Toggle selbst implementiert
- HTML-Beispiel

---

## Teil 2 — Tablet-Darstellung (769px–1024px)

### Konzept

Rein CSS-seitig via `@media (min-width: 769px) and (max-width: 1024px)`. Keine neuen Klassen, kein JavaScript. Websites müssen nichts tun.

### CSS-Regeln

```css
@media (min-width: 769px) and (max-width: 1024px) {
  .calendar-day {
    padding: 4px;
    min-height: 64px;
  }

  .calendar-day-number {
    font-size: 0.72rem;
  }

  .calendar-entry {
    padding: 2px 4px;
    font-size: 0.68rem;
    gap: 2px;
  }

  .calendar-entry-time {
    max-width: 36px;
    overflow: hidden;
    text-overflow: clip;
    white-space: nowrap;
  }

  .calendar-entry-title {
    font-size: 0.68rem;
  }
}
```

**Begründung der Werte:**
- `padding: 4px` (von 6px) — mehr Platz für Inhalt in engen Zellen
- `min-height: 64px` (von 80px) — kompaktere Zellen
- `font-size: 0.68rem` — eine Stufe kleiner als Desktop (0.72rem)
- `.calendar-entry-time` auf `max-width: 36px` — zeigt nur die Startzeit (z.B. „14:00"), Endzeit wird abgeschnitten
- `text-overflow: clip` statt `ellipsis` auf der Zeit — kein störendes `…` nach der Uhrzeit

### Verhalten

| Element | Desktop | Tablet | Mobile |
|---|---|---|---|
| Grid | 7 Spalten | 7 Spalten | 1 Spalte |
| Tageszell-Padding | 6px | 4px | 6px |
| Min-Height Zelle | 80px | 64px | unset |
| Entry-Font | 0.72rem | 0.68rem | 0.72rem |
| Uhrzeit | vollständig | nur Startzeit | vollständig |
| Leere Tage | sichtbar | sichtbar | ausgeblendet (toggle-bar) |

### Dokumentation

In `docs/calendar.md`: Neue Sektion „Tablet (769px–1024px)" mit:
- Beschreibung des automatischen Verhaltens
- Tabelle wie oben

---

## Neue Tokens

Keine. Alle Werte sind Größen-Anpassungen die keine Token-Würdigkeit erreichen (nicht semantisch, nicht wiederverwendet).

---

## Nicht in dieser Spec

- Eigener Toggle-Button als CI-Komponente (liegt in der Website)
- Wochenansicht oder Tagesansicht
- Swipe-Gesten auf Mobile

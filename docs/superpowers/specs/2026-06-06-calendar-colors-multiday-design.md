# Design-Spec: Kalender — Generische Farben & Mehrtägige Events

**Datum:** 2026-06-06  
**Status:** Spec — bereit zur Implementierung  
**Kontext:** Erweiterung der bestehenden Kalender-Komponente (`css/calendar.css`) um universell einsetzbare Farbslots und Unterstützung für mehrtägige Events.

---

## Ziel

1. **Generische Farb-Tokens** — 10 nummerierte Farbslots ersetzen die semantischen Diensttyp-Namen. Jede Website weist die Slots frei zu. Der Kalender wird damit universell einsetzbar (nicht nur Dienstplan).
2. **Mehrtägige Events** — Events die sich über mehrere Tage erstrecken, werden in jeder Tageszelle einzeln dargestellt, mit visuellen Fortsetzungsmarkierungen links/rechts.

---

## Dateien

| Datei | Änderung |
|---|---|
| `css/common.css` | 10 neue Token-Tripel (`--cal-color-N`, `-subtle`, `-border`) |
| `css/calendar.css` | 10 generische Modifier-Klassen + 4 Alias-Klassen + 2 Mehrtags-Modifier |
| `docs/tokens.md` | Neue Tokens dokumentieren |
| `docs/calendar.md` | Neue Klassen und Verwendung dokumentieren |
| `components/calendar.html` | Referenzbeispiele ergänzen |

---

## Teil 1 — Generische Farb-Tokens

### Neue Tokens in `css/common.css`

10 Token-Tripel (Hauptfarbe + subtle + border) im `:root`-Block:

```css
/* Kalender-Farbslots (pro Website frei belegbar) */
--cal-color-1:         #22c55e;
--cal-color-1-subtle:  rgba(34, 197, 94, 0.10);
--cal-color-1-border:  rgba(34, 197, 94, 0.25);

--cal-color-2:         #eab308;
--cal-color-2-subtle:  rgba(234, 179, 8, 0.10);
--cal-color-2-border:  rgba(234, 179, 8, 0.25);

--cal-color-3:         #a78bfa;
--cal-color-3-subtle:  rgba(167, 139, 250, 0.10);
--cal-color-3-border:  rgba(167, 139, 250, 0.25);

--cal-color-4:         #3b82f6;
--cal-color-4-subtle:  rgba(59, 130, 246, 0.07);
--cal-color-4-border:  rgba(59, 130, 246, 0.25);

--cal-color-5:         #f97316;
--cal-color-5-subtle:  rgba(249, 115, 22, 0.10);
--cal-color-5-border:  rgba(249, 115, 22, 0.25);

--cal-color-6:         #ef4444;
--cal-color-6-subtle:  rgba(239, 68, 68, 0.10);
--cal-color-6-border:  rgba(239, 68, 68, 0.25);

--cal-color-7:         #06b6d4;
--cal-color-7-subtle:  rgba(6, 182, 212, 0.10);
--cal-color-7-border:  rgba(6, 182, 212, 0.25);

--cal-color-8:         #ec4899;
--cal-color-8-subtle:  rgba(236, 72, 153, 0.10);
--cal-color-8-border:  rgba(236, 72, 153, 0.25);

--cal-color-9:         #84cc16;
--cal-color-9-subtle:  rgba(132, 204, 22, 0.10);
--cal-color-9-border:  rgba(132, 204, 22, 0.25);

--cal-color-10:        #94a3b8;
--cal-color-10-subtle: rgba(148, 163, 184, 0.10);
--cal-color-10-border: rgba(148, 163, 184, 0.25);
```

### Neue Modifier-Klassen in `calendar.css`

```css
.calendar-entry--color-1  { background: var(--cal-color-1-subtle);  border-color: var(--cal-color-1); }
.calendar-entry--color-2  { background: var(--cal-color-2-subtle);  border-color: var(--cal-color-2); }
/* ... bis --color-10 */
```

### Alias-Klassen (bestehende Namen, rückwärtskompatibel)

Die bisherigen semantischen Klassen bleiben als Aliase erhalten und können später entfernt werden:

```css
.calendar-entry--early   { background: var(--cal-color-1-subtle); border-color: var(--cal-color-1); }
.calendar-entry--late    { background: var(--cal-color-2-subtle); border-color: var(--cal-color-2); }
.calendar-entry--night   { background: var(--cal-color-3-subtle); border-color: var(--cal-color-3); }
.calendar-entry--default { background: var(--cal-color-4-subtle); border-color: var(--cal-color-4); }
```

### Website-seitige Überschreibung

Eine Website die Slot 1 für "Urlaub" (rot) nutzen will:

```css
:root {
  --cal-color-1:        #ef4444;
  --cal-color-1-subtle: rgba(239, 68, 68, 0.10);
  --cal-color-1-border: rgba(239, 68, 68, 0.25);
}
```

---

## Teil 2 — Mehrtägige Events

### Konzept

Jede Tageszelle zeigt den Eintrag des mehrtägigen Events einzeln. Zwei Modifier-Klassen steuern die Fortsetzungsmarkierungen:

| Klasse | Bedeutung |
|---|---|
| `.calendar-entry--continues-right` | Event geht am Folgetag weiter — `›` rechts |
| `.calendar-entry--continues-left` | Event kommt vom Vortag — `‹` links, `border-left` transparent |

Kombinierbar: Ein mittlerer Tag trägt beide Klassen.

### HTML-Beispiel (3-Tage-Event)

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

### CSS-Konzept

```css
/* Pfeil rechts via ::after */
.calendar-entry--continues-right::after {
  content: "›";
  margin-left: auto;
  flex-shrink: 0;
  color: var(--muted);
  font-size: 0.8rem;
  line-height: 1;
}

/* Pfeil links via ::before, border-left ausblenden */
.calendar-entry--continues-left {
  border-left-color: transparent;
}

.calendar-entry--continues-left::before {
  content: "‹";
  flex-shrink: 0;
  color: var(--muted);
  font-size: 0.8rem;
  line-height: 1;
}
```

### Uhrzeit-Regel

- Nur der **Starttag** zeigt `calendar-entry-time`
- Folgetage lassen das Element weg (nicht im DOM)

### Mobile

Die Wiederholungs-Strategie funktioniert auf Mobile ohne Änderung — jeder Tag wird einzeln in der einspaltigen Liste angezeigt, die Pfeile zeigen die Kontinuität an.

---

## Accessibility

Neue `aria-label`-Konventionen für Mehrtags-Events:

| Tag | aria-label |
|---|---|
| Starttag | `"Titel, HH:MM, läuft weiter, Details öffnen"` |
| Mitteltag | `"Titel, Fortsetzung, Details öffnen"` |
| Endtag | `"Titel, Fortsetzung, Details öffnen"` |

---

## Neue Tokens

| Token | Typ | Wert |
|---|---|---|
| `--cal-color-1` … `--cal-color-10` | Hauptfarbe | Konkrete Hex-Werte |
| `--cal-color-N-subtle` | Hintergrund | `rgba(…, 0.10)` |
| `--cal-color-N-border` | Rand | `rgba(…, 0.25)` |

Alle 30 Tokens in `css/common.css` definiert, in `docs/tokens.md` dokumentiert.

---

## Nicht in dieser Spec

- Spanning-Bars über mehrere Spalten (Option A wurde abgelehnt)
- Automatisches Mapping Backend-Kategorie → Farbslot (liegt in der jeweiligen Website)
- Entfernung der Alias-Klassen (separater Schritt zu einem späteren Zeitpunkt)

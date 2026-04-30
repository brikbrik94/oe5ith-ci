# Design-Spec: Typ 5 — Empty State (`.result-empty`)

**Datum:** 2026-04-30  
**Status:** Approved  
**Scope:** `sidebar.css`, `components/sidebar-types.html`, `docs/sidebar-types.md`

---

## Ziel

Typ 5 (Ergebnis-Liste einfach, z.B. NAH-Stützpunkte) soll einen definierten Leerzustand erhalten.
Wenn noch keine Ergebnisse vorliegen, wird ein informativer Hinweistext angezeigt — optional mit Icon.

---

## Komponente: `.result-empty`

### HTML

```html
<!-- Mit Icon (site-spezifisch, optional) -->
<div class="result-empty">
  <i class="fa-solid fa-arrow-pointer"></i>
  Klicke auf einen Punkt in der Karte, um die 5 nächsten NAH-Stützpunkte zu berechnen.
</div>

<!-- Ohne Icon -->
<div class="result-empty">
  Klicke auf einen Punkt in der Karte, um die 5 nächsten NAH-Stützpunkte zu berechnen.
</div>
```

### CSS (Ergänzung in `sidebar.css`, nach `.result-simple-meta`)

```css
.result-empty {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px 4px;
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.5;
}
.result-empty i {
  flex-shrink: 0;
  margin-top: 2px;
  opacity: 0.5;
  font-size: 0.85rem;
}
```

---

## Regeln

- `.result-empty` ersetzt die `.result-list` wenn keine Ergebnisse vorhanden sind
- Icon ist optional — immer FontAwesome, Auswahl site-spezifisch
- Kein Hover, kein Klick — rein informativer Zustand
- Text ist frei wählbar je nach Anwendungsfall
- Keine Hardcoded-Farben — nur `var(--muted)` und `opacity`

---

## Änderungen

| Datei | Änderung |
|---|---|
| `css/sidebar.css` | `.result-empty` + `.result-empty i` hinzufügen |
| `components/sidebar-types.html` | Empty-State-Beispiel in Typ-5-Sektion ergänzen |
| `docs/sidebar-types.md` | Typ-5-Abschnitt: `.result-empty` dokumentieren |

# Buttons

**Referenz-Datei:** `components/buttons.html`  
**Status:** definiert · v1.0

---

## Überblick

Alle Buttons teilen dieselbe Basis-Klasse `.btn`. Variante, Größe und Zustand
werden durch zusätzliche Klassen gesteuert. Font Awesome Icons werden links
vom Text platziert.

---

## Basis-Tokens

| Token | Wert |
|---|---|
| `height` | `36px` (Default) |
| `padding` | `0 16px` |
| `border-radius` | `6px` |
| `font-size` | `0.85rem` |
| `font-weight` | `700` |
| `gap` (Icon + Text) | `7px` |
| Icon `font-size` | `0.8rem` |

```css
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 7px; height: 36px; padding: 0 16px;
  border-radius: 6px; font-size: 0.85rem; font-weight: 600;
  font-family: inherit; cursor: pointer; border: none;
  white-space: nowrap; position: relative;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}
.btn:active { transform: scale(0.97); }
.btn i { font-size: 0.8rem; }
```

---

## Varianten

| Klasse | Verwendung |
|---|---|
| `.btn-primary` | Primäre Aktion — immer nur eine pro Bereich |
| `.btn-secondary` | Sekundäre Aktion, weniger Gewicht als Primary |
| `.btn-ghost` | Neutrale Aktion, Navigation, Abbrechen |
| `.btn-danger` | Destruktive Aktion (Löschen, Widerrufen) |

### Primary

```css
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: var(--accent-hover); }
```

### Secondary

```css
.btn-secondary {
  background: rgba(59,130,246, 0.10);
  color: var(--accent);
  border: 1px solid rgba(59,130,246, 0.25);
}
.btn-secondary:hover {
  background: rgba(59,130,246, 0.18);
  border-color: rgba(59,130,246, 0.40);
}
```

### Ghost

```css
.btn-ghost {
  background: transparent;
  color: var(--muted);
  border: 1px solid var(--border);
}
.btn-ghost:hover {
  color: var(--text);
  border-color: #555;
  background: rgba(255,255,255, 0.04);
}
```

### Danger

```css
.btn-danger {
  background: rgba(239,68,68, 0.10);
  color: #ef4444;
  border: 1px solid rgba(239,68,68, 0.20);
}
.btn-danger:hover {
  background: rgba(239,68,68, 0.20);
  border-color: rgba(239,68,68, 0.40);
}
```

---

## Größen

| Klasse | Höhe | Padding | Font-size | Verwendung |
|---|---|---|---|---|
| `.btn-sm` | `28px` | `0 10px` | `0.75rem` | Kompakte Bereiche, Tabellen |
| *(keine)* | `36px` | `0 16px` | `0.85rem` | Standard |
| `.btn-lg` | `44px` | `0 22px` | `0.95rem` | Mobile, primäre CTAs |

```css
.btn-sm { height: 28px; padding: 0 10px; font-size: 0.75rem; border-radius: 5px; }
.btn-lg { height: 44px; padding: 0 22px; font-size: 0.95rem; }
```

> **Regel:** Auf Mobile immer `.btn-lg` für Touch-Targets (min. 44px).

---

## Zustände

### Disabled

Gilt für alle vier Varianten — keine eigene Farbe nötig.

```css
.btn:disabled, .btn.disabled {
  opacity: 0.4;
  pointer-events: none;
  cursor: not-allowed;
}
```

```html
<button class="btn btn-primary" disabled>Gesperrt</button>
```

### Loading

Text wird unsichtbar (`color: transparent`), Spinner überlagert.
Spinner-Farbe passend zur Variante.

```css
.btn.loading { pointer-events: none; color: transparent; }

.btn.loading::after {
  content: ''; position: absolute;
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255, 0.25);
  border-top-color: #fff;
  border-radius: 50%;
  animation: btn-spin 0.6s linear infinite;
}

/* Spinner-Farbe für Secondary + Ghost */
.btn-secondary.loading::after,
.btn-ghost.loading::after {
  border-color: rgba(59,130,246, 0.20);
  border-top-color: var(--accent);
}

/* Spinner-Farbe für Danger */
.btn-danger.loading::after {
  border-color: rgba(239,68,68, 0.20);
  border-top-color: #ef4444;
}

@keyframes btn-spin { to { transform: rotate(360deg); } }
```

```js
// Loading aktivieren
btn.classList.add('loading');

// Loading beenden
btn.classList.remove('loading');
```

---

## Zustands-Matrix

| | Primary | Secondary | Ghost | Danger |
|---|---|---|---|---|
| **Default** | Blau gefüllt | Blau transparent | Transparent | Rot transparent |
| **Hover** | Dunkleres Blau | Mehr Opacity | Leichter Hintergrund | Mehr Opacity |
| **Disabled** | 40% Opacity | 40% Opacity | 40% Opacity | 40% Opacity |
| **Loading** | Weißer Spinner | Blauer Spinner | Blauer Spinner | Roter Spinner |

---

## Mit Icon

Icon immer links vom Text. Ausschließlich Font Awesome.

```html
<button class="btn btn-primary">
  <i class="fa-solid fa-eye"></i> Vorschau
</button>

<button class="btn btn-danger">
  <i class="fa-solid fa-trash"></i> Löschen
</button>
```

> Kein Icon-only Button ohne Text — immer mit Label für Accessibility.
> Ausnahme: Icons in der Topbar (dort eigene Regeln, siehe `topbar.md`).

---

## Verwendungsregeln

- **Primary** nur einmal pro sichtbarem Bereich — die wichtigste Aktion
- **Danger** nur für destruktive Aktionen — nie für "Abbrechen" (dafür Ghost)
- **Ghost** für Navigation und neutrale Aktionen (Zurück, Schließen, Abbrechen)
- **Secondary** für gleichwertige Alternativen zur Primary-Aktion
- Buttons nebeneinander: Primary rechts, Ghost/Secondary links

```html
<!-- Richtige Reihenfolge -->
<button class="btn btn-ghost">Abbrechen</button>
<button class="btn btn-primary">Speichern</button>
```

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | Initiale Definition. 4 Varianten. 3 Größen. Disabled + Loading Zustände. Icon-Regel. |

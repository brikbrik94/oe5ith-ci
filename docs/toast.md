# Toast

**CSS:** `css/toast.css`  
**TypeScript:** `scripts/ui/toast.ts`  
**Referenz:** `components/toast.html`  
**Status:** definiert · v1.0

---

## Überblick

Toasts sind kurze, nicht-blockierende Status-Meldungen. Sie erscheinen unten rechts, stapeln sich bei mehreren gleichzeitigen Meldungen, und verschwinden automatisch nach einer konfigurierbaren Dauer.

---

## Varianten

| Klasse | Verwendung |
|---|---|
| `.toast--success` | Aktion erfolgreich abgeschlossen |
| `.toast--warning` | Hinweis, Aktion läuft weiter |
| `.toast--danger` | Fehler, Aktion fehlgeschlagen |
| `.toast--info` | Neutrale Information |

---

## Modifier

### `.toast--rich`

Erweitert den Toast um einen Beschreibungstext (`.toast-body`) und einen optionalen Action-Button (`.toast-action`). Wird automatisch gesetzt wenn `body` oder `action` übergeben werden.

---

## HTML-Struktur

### Standard Toast

```html
<div class="toast-container">
  <div class="toast toast--success toast--visible" role="status" aria-live="polite" aria-atomic="true">
    <div class="toast-main">
      <span class="toast-icon" aria-hidden="true">✔</span>
      <span class="toast-text">Einstellungen gespeichert</span>
      <button class="toast-close" type="button" aria-label="Schließen">✕</button>
    </div>
  </div>
</div>
```

### Rich Toast

```html
<div class="toast toast--info toast--rich toast--visible" role="status" aria-live="polite" aria-atomic="true">
  <div class="toast-main">
    <span class="toast-icon" aria-hidden="true">ℹ</span>
    <span class="toast-text">Import abgeschlossen</span>
    <button class="toast-close" type="button" aria-label="Schließen">✕</button>
  </div>
  <p class="toast-body">142 Einträge wurden importiert.</p>
  <button class="toast-action" type="button">Details →</button>
</div>
```

---

## TypeScript API

```typescript
import { toast } from './scripts/ui/toast';

// Convenience-Methoden
toast.success('Gespeichert');
toast.warning('Verbindung instabil');
toast.danger('Import fehlgeschlagen');
toast.info('Update verfügbar');

// Mit Rich-Optionen
toast.success('Import abgeschlossen', {
  body: '142 Einträge wurden importiert.',
  action: {
    label: 'Details →',
    onClick: () => router.push('/import/log'),
  },
});

// Persistenter Toast (kein auto-dismiss)
const dismiss = toast.warning('Offline — Änderungen werden gespeichert', {
  duration: 0,
});
// Später manuell schließen:
dismiss();

// Explizite Dauer
toast.info('Clipboard kopiert', { duration: 2000 });
```

### `ToastOptions`

| Option | Typ | Default | Beschreibung |
|---|---|---|---|
| `type` | `'success' \| 'warning' \| 'danger' \| 'info'` | `'info'` | Variante |
| `text` | `string` | — | Pflicht: kurze Hauptmeldung |
| `body` | `string` | — | Beschreibungstext (aktiviert `.toast--rich`) |
| `action` | `{ label: string; onClick: () => void }` | — | Action-Button (aktiviert `.toast--rich`) |
| `duration` | `number` (ms) | `4000` | Auto-dismiss. `0` = persistent |

---

## CSS einbinden

```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/toast.css">
```

Oder via `css/index.css` (bereits enthalten).

---

## Neue Tokens

Zwei Tokens wurden in `css/common.css` ergänzt:

| Token | Wert | Verwendung |
|---|---|---|
| `--z-toast` | `1600` | Toast-Container — über Modals |
| `--shadow-toast` | `0 8px 24px rgba(0,0,0,0.50)` | Toast-Schatten |

---

## Regeln

- Toast nur für Feedback zu Nutzeraktionen oder wichtigen System-Ereignissen.
- Kein Toast für Informationen, die dauerhaft sichtbar sein müssen — dafür Badges oder Panels.
- `duration: 0` nur wenn der Nutzer die Meldung explizit bestätigen oder lesen muss.
- Mehrere gleichzeitige Toasts sind erlaubt, aber auf max. 3–4 begrenzen.
- Auf Karten-Seiten: Toast-Container liegt über der Karte (`--z-toast: 1600`), kein Konflikt mit Leaflet/MapLibre.

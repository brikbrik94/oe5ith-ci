# Design: Globale Scrollbar-Stilisierung + Sidebar-Breite 300px

**Datum:** 2026-05-07  
**Status:** Genehmigt  

---

## Ziel

1. Den Browser-Standard-Scrollbar durch einen CI-konformen dunklen Scrollbar ersetzen — gilt global für alle scrollbaren Bereiche (Sidebar, Page Content, etc.)
2. `--sidebar-width` von 260px auf 300px erhöhen, um mehr Platz für Formulare wie den Koordinaten-Umrechner zu schaffen (löst auch den DMS-Zeilen-Überlauf ohne Eingriff in `coords.css`)

---

## Begründung

- `.sidebar-inner` hat `overflow-y: auto`, rendert aber ohne CSS den System-Scrollbar (hell/grau) — wirkt inkonsistent im dunklen CI-Theme
- DMS-Zeile in Koordinaten-Umrechner braucht ~222px, verfügbar waren ~209px → bei sichtbarem Scrollbar Überlauf. Mit 300px Sidebar stehen ~249px zur Verfügung (passt auch mit CI-Scrollbar)
- 300px ist auf allen aktuellen Displays (1366px+) unproblematisch

---

## Änderungen

### 1. `css/common.css`

**Token-Änderung:**
```css
--sidebar-width: 300px;   /* war: 260px */
```

**Neuer Abschnitt „Scrollbar" nach dem Reset-Block:**
```css
/* ── Scrollbar ── */
html {
  scrollbar-width: thin;
  scrollbar-color: var(--border-strong) transparent;
}
::-webkit-scrollbar        { width: 6px; height: 6px; }
::-webkit-scrollbar-track  { background: transparent; }
::-webkit-scrollbar-thumb  { background: var(--border-strong); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--subtle); }
```

- `html`-Selektor: Firefox + Chrome 121+ (native `scrollbar-color`)
- `::-webkit-scrollbar`: Chrome/Safari/Edge (webkit-Präfix)
- Farben: `--border-strong` (#444) für Thumb, `transparent` für Track — kein Hardcode
- Breite 6px: schmal genug um nicht zu dominieren, breit genug für Touchpad-Nutzung

### 2. `docs/tokens.md`

- `--sidebar-width` in der Tabelle von 260px auf 300px aktualisieren
- Änderungshistorie ergänzen

### 3. `CHANGELOG.md`

Neuen Eintrag `v1.6.0` anlegen mit Kategorien `Added` (Scrollbar) und `Changed` (Sidebar-Breite).

---

## Nicht geändert

- `css/coords.css` — kein Eingriff nötig, Breitenerhöhung löst das DMS-Problem
- `css/sidebar.css` — Scrollbar-Regel kommt global in `common.css`
- Alle HTML-Referenzseiten in `components/` — nutzen `--sidebar-width` via Token

---

## Browserkompatibilität

| Browser | Mechanismus |
|---|---|
| Firefox | `scrollbar-width` + `scrollbar-color` auf `html` |
| Chrome 121+ | `scrollbar-width` + `scrollbar-color` auf `html` |
| Chrome < 121, Safari, Edge | `::-webkit-scrollbar` |

Beide Regelsätze koexistieren — kein Konflikt.

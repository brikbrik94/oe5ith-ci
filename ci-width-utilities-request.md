# CI-Erweiterung: Breiten-Utilities (max-w-* / w-*) — Anforderung

**Status:** Vorschlag · zur Umsetzung im `oe5ith-ci` Repo
**Angefragt von:** internal.oe5ith.at (System-Logs-View, betrifft auch bestehende POCSAG-View)
**Datum:** 2026-06-18

---

## Problem

Mehrere produktive Seiten referenzieren Breiten-Utility-Klassen, die im CI
**nicht existieren** — sie sind aktuell wirkungslose No-op-Klassen:

| Klasse | Verwendet in | Im CI definiert? |
|---|---|---|
| `max-w-300` | `site/internal/src/views/logs/logs.html`, `…/pocsag/pocsag.html` | ❌ nein |
| `w-180` | `…/pocsag/pocsag.html` (Tabellen-`<th>`) | ❌ nein |
| `w-120` | `…/pocsag/pocsag.html` | ❌ nein |
| `w-100` | `…/logs/logs.html`, `…/pocsag/pocsag.html` | ❌ nein |
| `w-80`  | `…/pocsag/pocsag.html` | ❌ nein |

`deps/oe5ith-ci/css/utils.css` definiert derzeit nur `.w-full` (und `.flex-1`,
`.flex-2`). Es gibt **keine** fixen Breiten-/Max-Breiten-Utilities. Die Klassen
werden also gerendert, haben aber keine CSS-Regel → Spalten/Felder fallen auf
Auto-Breite zurück.

**Auswirkung:** rein kosmetisch (Tabellenspalten und Formularfelder dimensionieren
sich automatisch statt mit fester Breite). Kein funktionaler Fehler. Aber: Verstoß
gegen die CI-Regel „nur existierende CI-Klassen verwenden" und irreführend für
spätere Entwickler.

---

## Zwei mögliche Lösungen (CI-Team entscheidet)

### Option A — Utilities ins CI aufnehmen (empfohlen)

In `css/utils.css` eine kleine, dokumentierte Gruppe fixer Breiten ergänzen,
passend zu den real verwendeten Werten. Werte als Tokens, wenn mehrfach genutzt.

Beispiel (Werte an die tatsächlich gebrauchten anpassen):

```css
/* ═══ WIDTH UTILITIES (feste Spalten-/Feldbreiten) ═══ */
.w-80   { width: 80px; }
.w-100  { width: 100px; }
.w-120  { width: 120px; }
.w-180  { width: 180px; }

/* ═══ MAX-WIDTH UTILITIES ═══ */
.max-w-300 { max-width: 300px; }
```

- In `docs/tokens.md` bzw. einer Utilities-Doku kurz dokumentieren.
- In `docs/registry.json` registrieren und `scripts/cli/check_consistency.py`
  laufen lassen (gemäß `for-coding-agents.md`).
- Additiv → MINOR-Release.

> Hinweis Tabellen: Für `<th>`-Breiten ist ggf. eine eigene, semantisch klarere
> Konvention sinnvoller (z.B. `.col-w-180`). Das CI-Team kann hier die bevorzugte
> Benennung festlegen — wichtig ist nur, dass die in den Seiten genutzten Namen
> existieren oder die Seiten auf die neuen Namen umgestellt werden.

### Option B — Klassen aus den Seiten entfernen

Falls das CI bewusst keine festen Breiten-Utilities möchte: die No-op-Klassen aus
`logs.html` und `pocsag.html` entfernen und Auto-Breite akzeptieren (bzw. wo nötig
über bestehende Patterns lösen). Dann ist nichts am CI zu tun, aber die Seiten
müssen angepasst werden.

---

## Empfehlung

Option A — die Werte werden offensichtlich gebraucht (Timestamp-/ID-/Baud-Spalten,
begrenzte Select-Breite). Eine kleine, dokumentierte Utility-Gruppe ist
CI-konform, wiederverwendbar und behebt die Lücke in beiden Views auf einmal.

Sobald das CI erweitert und das Submodul hier aktualisiert ist, sind die Klassen
in `logs.html`/`pocsag.html` automatisch wirksam — keine Frontend-Änderung nötig.

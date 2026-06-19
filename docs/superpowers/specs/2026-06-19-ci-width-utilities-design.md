# CI-Breiten-Utilities — Design

**Datum:** 2026-06-19
**Status:** Freigegeben · zur Umsetzung
**Quelle der Anforderung:** `ci-width-utilities-request.md` (internal.oe5ith.at — System-Logs-View, POCSAG-View)

---

## Problem

Produktive Seiten in website-v3 (`logs.html`, `pocsag.html`) referenzieren Breiten-Utility-Klassen, die im CI **nicht existieren** und damit wirkungslose No-op-Klassen sind. `css/utils.css` definiert bislang nur `.w-full`, `.flex-1`, `.flex-2` — keine fixen Breiten- oder Max-Breiten-Utilities. Folge: Tabellenspalten/Felder fallen auf Auto-Breite zurück (rein kosmetisch, kein funktionaler Fehler), und es liegt ein Verstoß gegen die CI-Regel „nur existierende Klassen verwenden" vor.

Gewählte Lösung: **Option A** — eine kleine, dokumentierte Utility-Gruppe ins CI aufnehmen.

---

## Entscheidungen

- **Semantische Benennung für Spaltenbreiten:** `.col-w-80 / .col-w-100 / .col-w-120 / .col-w-180` statt der ursprünglich verwendeten `.w-*`. Begründung: klarer Zweck (Spalten-/Zellbreite) und sauberere CI-Konvention. Kosten: die `<th>`-Klassen in website-v3 müssen umbenannt werden (siehe „Auswirkung außerhalb dieses Repos").
- **`.max-w-300` bleibt generisch:** Es begrenzt laut Anforderung einen Container/Select, ist also keine Spaltenbreite. Daher als allgemeine Max-Width-Utility mit unverändertem Namen.
- **Keine Tokens, harte px-Werte:** Es handelt sich um Einzelwerte ohne mehrfache/semantische Wiederverwendung. CLAUDE.md erlaubt Tokens nur für mehrfach genutzte oder semantisch klare Werte; es gibt bereits Präzedenz in `utils.css` (`.p-2rem { padding: 2rem; }`, „kein Token vorhanden").
- **Keine eigene Spec-Doc / kein G1–G4:** Der Registry-Eintrag `utils` ist als „Zweckgebundene Utilities ohne eigene Spec" (`doc: []`) geführt. Der Doku-Standard G1–G4 gilt nur für Kategorie `component`. Utility-Klassen werden — wie alle bestehenden — ausschließlich über die Referenz-Demo in `components/utils.html` dokumentiert.

---

## Änderungen (nur dieses Repo)

### 1. `css/utils.css`

Zwei neue Sektionen nach der bestehenden `FLEX EXTENSIONS`-Sektion:

```css
/* ═══════════════════════════════════════
   WIDTH UTILITIES (feste Spaltenbreiten)
   ═══════════════════════════════════════ */

.col-w-80  { width: 80px; }
.col-w-100 { width: 100px; }
.col-w-120 { width: 120px; }
.col-w-180 { width: 180px; }

/* ═══════════════════════════════════════
   MAX-WIDTH UTILITIES
   ═══════════════════════════════════════ */

.max-w-300 { max-width: 300px; }
```

### 2. `components/utils.html`

- Inline-`<style>`-Block um die neuen Klassen ergänzen (analog zu den bestehenden Utils, damit die Demo eigenständig rendert).
- Neue Demo-Sektion(en) vor `</body>`:
  - Eine Tabelle, die `.col-w-80/100/120/180` an `<th>` zeigt (feste vs. Auto-Spalte sichtbar).
  - Ein Container/Select mit `.max-w-300`.

### 3. `CHANGELOG.md`

Neue Sektion `## v1.15.0 - 2026-06-19` mit `### Added`-Eintrag für die Breiten-Utilities. Additiv → **MINOR** (von v1.14.0 → v1.15.0).

### 4. Consistency-Check

`python3 scripts/cli/check_consistency.py` muss grün bleiben. `utils.css` ist bereits in `docs/registry.json` registriert — keine Registry-Änderung nötig.

---

## Auswirkung außerhalb dieses Repos (nur Hinweis, kein Code hier)

In website-v3 müssen `logs.html` und `pocsag.html` ihre Spaltenklassen von `w-80/w-100/w-120/w-180` auf `col-w-*` umstellen. `max-w-300` bleibt unverändert.

**Zu verifizieren beim Umstellen:** `w-100` wird laut Anforderung auch in `logs.html` genutzt. Falls das dort **kein** Spalten-/`<th>`-Kontext ist, wäre `.col-w-100` ein Misnomer — in dem Fall dort eine passendere Klasse wählen.

---

## Nicht im Scope (YAGNI)

- Keine vollständige Skala an Breiten-Utilities (`w-1`…`w-n`) — nur die real gebrauchten Werte.
- Keine Tokens für Breiten.
- Keine Änderungen an website-v3 aus diesem Repo heraus.

# Service-Dashboard Inhaltsregeln Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Die inhaltlich-semantischen Regeln aus `docs/superpowers/specs/2026-06-08-service-dashboard-content-rules-design.md` in `docs/service-dashboard.md` ergänzen (Detail: Ein-Endpunkt + festes Panel-Set + Zellen-Regel; Config: Kategorien-Prinzip + Pflicht-Überschrift).

**Architecture:** Reines Doku-Update einer einzigen Datei (`docs/service-dashboard.md`). Pro Seite wird nach dem bestehenden `### Reihenfolge & Platzierung (G3)` eine neue Unterüberschrift `### Inhalt & Semantik` eingefügt. Keine neuen CSS-Klassen, keine Strukturänderung, keine Registry-Änderung. Verifikation über Grep + `check_consistency.py`.

**Tech Stack:** Markdown, `scripts/cli/check_consistency.py` (Python).

---

### Task 1: Detail-Seite — Abschnitt „Inhalt & Semantik"

**Files:**
- Modify: `docs/service-dashboard.md` (Seite 2 — Detail, nach G3)

- [ ] **Step 1: Neue Unterüberschrift nach dem G3-Block der Detail-Seite einfügen**

Suche in `docs/service-dashboard.md` das Ende des Detail-G3-Blocks. Der `old_string`
ist der letzte G3-Bullet der Detail-Seite gefolgt vom Trenner:

old_string:
```markdown
- `.card-warn` folgt unmittelbar nach dem Panel mit den Daten und dient als Hinweis,
  dass die destruktive Aktion (z. B. Neustart) Konsequenzen hat.

---

## Seite 3 — Config (Seitentyp 1: Detail-Seite)
```

new_string:
```markdown
- `.card-warn` folgt unmittelbar nach dem Panel mit den Daten und dient als Hinweis,
  dass die destruktive Aktion (z. B. Neustart) Konsequenzen hat.

### Inhalt & Semantik

**Ein Endpunkt pro Seite:** Eine Detailseite zeigt **genau einen Dienst/Endpunkt**.
Alle Panels der Seite beziehen sich auf diesen einen Endpunkt; mehrere Dienste werden
**nie** auf einer Detailseite gemischt — jeder Dienst hat seine eigene Detailseite,
der Wechsel erfolgt über die Sidebar. (Die „Variante – Dienst offline" in
`components/service-dashboard-detail.html` ist eine Zustands-Demo, kein zweiter Dienst.)

**Festes Set an Panel-Typen:** Jede Kachel (`.panel`) muss **genau einem** der
folgenden Typen entsprechen — andere Panel-Typen sind nicht zulässig:

| Panel-Typ | Inhalt | Pflicht/Optional |
|---|---|---|
| **Live-Status** | Echtzeit-Laufzeitwerte, per JS aktualisiert (z. B. GPS-Fix, Geschwindigkeit, nächste TX, Payload, Dienst aktiv) | Pflicht (mind. 1 pro Seite) |
| **Verbindung / Endpoint** | Statische Verbindungsdaten: Host, Port, Protokoll, URL, letzter Kontakt | Optional |
| **Konfiguration (read-only)** | Aktuell geladene Einstellungen nur zur Anzeige; Ändern erfolgt über die Config-Seite | Optional |
| **Diagnose / Fehler** | Letzte Fehler, Warnungen, Diagnosehinweise | Optional |

**Zellen-Regel:** Ein Wert = eine `.svc-data-cell` (Label / Wert / optional Subtext).
Eine Zelle enthält keinen zusammengesetzten oder mehrwertigen Inhalt — mehrere Werte
werden auf mehrere Zellen aufgeteilt.

---

## Seite 3 — Config (Seitentyp 1: Detail-Seite)
```

- [ ] **Step 2: Verifizieren, dass der Detail-Abschnitt vorhanden ist**

Run: `grep -n "Festes Set an Panel-Typen\|Ein Endpunkt pro Seite\|Zellen-Regel" docs/service-dashboard.md`
Expected: 3 Treffer.

- [ ] **Step 3: Verifizieren, dass die Detail-`### Inhalt & Semantik` vor „Seite 3" steht**

Run: `grep -n "### Inhalt & Semantik\|## Seite 3" docs/service-dashboard.md`
Expected: Mindestens eine `### Inhalt & Semantik`-Zeile mit kleinerer Zeilennummer als die `## Seite 3`-Zeile.

- [ ] **Step 4: Commit**

```bash
git add docs/service-dashboard.md
git commit -m "docs(service-dashboard): add detail content rules (one endpoint, fixed panel set, cell rule)"
```

---

### Task 2: Config-Seite — Abschnitt „Inhalt & Semantik" + `.panel-title` als Pflicht

**Files:**
- Modify: `docs/service-dashboard.md` (Seite 3 — Config: G1-Hinweis + nach G3)

- [ ] **Step 1: `.panel-title` im G1-„Bestehende Klassen"-Hinweis der Config-Seite als Pflicht kennzeichnen**

old_string:
```markdown
Bestehende Klassen (aus `page.css`): `.panel`, `.panel-header`, `.panel-title`, `.panel-body`,
`.panel-meta`. (`.panel-header-right` wird auf der Config-Seite nicht verwendet — dort steht
`span.panel-meta` direkt im `.panel-header` als Geschwister von `.panel-title`.)
```

new_string:
```markdown
Bestehende Klassen (aus `page.css`): `.panel`, `.panel-header`, `.panel-title`, `.panel-body`,
`.panel-meta`. (`.panel-header-right` wird auf der Config-Seite nicht verwendet — dort steht
`span.panel-meta` direkt im `.panel-header` als Geschwister von `.panel-title`.)
`.panel-title` (Icon + Bezeichnung) ist auf der Config-Seite **Pflicht je Panel** — auch
bei einem Panel mit nur einem Feld (siehe „Inhalt & Semantik").
```

- [ ] **Step 2: Neue Unterüberschrift nach dem G3-Block der Config-Seite einfügen**

old_string:
```markdown
- `.svc-form-actions` ist letztes Kind von `.content-body`, nach allen Panels.

---

## Zustände & Varianten (G4)
```

new_string:
```markdown
- `.svc-form-actions` ist letztes Kind von `.content-body`, nach allen Panels.

### Inhalt & Semantik

**Gruppierung nach Kategorien (offenes Prinzip):** Einstellungen werden thematisch in
Panels („Kategorien") gruppiert. Dienste wählen die passenden Kategorien selbst — es gibt
keine geschlossene Liste. Empfohlene Beispiel-Kategorien: **Allgemein, Verbindung,
Authentifizierung, Erweitert**. Reihenfolge: allgemeine/häufig genutzte Kategorien zuerst,
„Erweitert" bzw. riskante Einstellungen zuletzt.

**Pflicht-Überschrift je Panel:** Jedes Config-Panel **muss** eine Überschrift
(`.panel-title` mit Icon + Bezeichnung) enthalten — auch wenn das Panel nur ein einzelnes
Feld hat.

---

## Zustände & Varianten (G4)
```

- [ ] **Step 3: Verifizieren, dass der Config-Abschnitt und die Pflicht-Kennzeichnung vorhanden sind**

Run: `grep -n "Gruppierung nach Kategorien\|Pflicht-Überschrift je Panel\|Pflicht je Panel" docs/service-dashboard.md`
Expected: 3 Treffer.

- [ ] **Step 4: Verifizieren, dass jetzt genau zwei `### Inhalt & Semantik`-Abschnitte existieren (Detail + Config)**

Run: `grep -c "### Inhalt & Semantik" docs/service-dashboard.md`
Expected: `2`

- [ ] **Step 5: Commit**

```bash
git add docs/service-dashboard.md
git commit -m "docs(service-dashboard): add config category grouping and mandatory panel heading"
```

---

### Task 3: Änderungshistorie + Gesamt-Verifikation

**Files:**
- Modify: `docs/service-dashboard.md` (Abschnitt „Änderungshistorie")

- [ ] **Step 1: Neuen Historien-Eintrag oben in die Tabelle einfügen**

old_string:
```markdown
| Datum | Änderung |
|---|---|
| 2026-06-07 | Layout-Inline-Styles durch CI-Klassen ersetzt: `.svc-page-title-row` (Detail+Config Page-Header), `.svc-field-grid` + `.svc-field-grid--cols-3` (Config Panel-Body), `.svc-label-type` (Label-Typ-Hinweise), `.svc-field-code` (JSON-Textarea); G2-Bäume und G3-Text aktualisiert. |
```

new_string:
```markdown
| Datum | Änderung |
|---|---|
| 2026-06-08 | Inhaltlich-semantische Regeln ergänzt: Detail-Seite „Inhalt & Semantik" (Ein-Endpunkt-Regel, festes Panel-Typen-Set, Zellen-Regel); Config-Seite „Inhalt & Semantik" (Kategorien-Gruppierung als offenes Prinzip, `.panel-title` als Pflicht je Panel). |
| 2026-06-07 | Layout-Inline-Styles durch CI-Klassen ersetzt: `.svc-page-title-row` (Detail+Config Page-Header), `.svc-field-grid` + `.svc-field-grid--cols-3` (Config Panel-Body), `.svc-label-type` (Label-Typ-Hinweise), `.svc-field-code` (JSON-Textarea); G2-Bäume und G3-Text aktualisiert. |
```

- [ ] **Step 2: Konsistenz-Check ausführen**

Run: `python3 scripts/cli/check_consistency.py`
Expected: Endet mit `✔ Manifest und Dateien sind konsistent` (Exit-Code 0). Die vorbestehenden Warnungen zu `coords`/`utils` sind erwartbar und kein Fehler.

- [ ] **Step 3: Verifizieren, dass keine CSS-/Komponenten-Dateien geändert wurden**

Run: `git status --porcelain css/ components/`
Expected: Keine Ausgabe (diese Verzeichnisse bleiben unverändert — reines Doku-Vorhaben).

- [ ] **Step 4: Commit**

```bash
git add docs/service-dashboard.md
git commit -m "docs(service-dashboard): changelog entry for content rules"
```

---

## Self-Review

**Spec-Coverage:**
- ✅ A1 Ein-Endpunkt-Regel → Task 1, Step 1 („Ein Endpunkt pro Seite")
- ✅ A2 Festes Panel-Typen-Set (Tabelle) → Task 1, Step 1
- ✅ A3 Zellen-Regel → Task 1, Step 1
- ✅ B1 Kategorien-Gruppierung (offenes Prinzip + Beispiele) → Task 2, Step 2
- ✅ B2 Pflicht-Überschrift je Panel → Task 2, Step 1 (G1-Hinweis) + Step 2 (Inhalt & Semantik)
- ✅ Platzierung: je Seite `### Inhalt & Semantik` nach G3 → Tasks 1 & 2
- ✅ Änderungshistorie 2026-06-08 → Task 3
- ✅ Verifikation `check_consistency.py` grün, keine Registry-Änderung → Task 3

**Nicht-Ziele eingehalten:** Keine neuen CSS-Klassen, keine G2-Strukturänderung, keine geschlossene Config-Kategorienliste, keine Änderung an Seite 1 (Übersicht) — durch Task 3, Step 3 (`git status` auf css/components leer) abgesichert.

**Placeholder-Scan:** Keine TBD/TODO; alle Einfügungen als vollständige `old_string`/`new_string`-Blöcke vorhanden.

**Typ-/Namenskonsistenz:** Verwendete Klassennamen (`.panel`, `.panel-title`, `.svc-data-cell`) entsprechen exakt der bestehenden Doku und CSS.

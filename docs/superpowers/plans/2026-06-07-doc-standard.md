# Doku-Standard für Komponenten-Docs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Einen verbindlichen, interpretationsfreien Doku-Standard (`docs/doc-standard.md`) einführen und `docs/service-dashboard.md` als kanonisches Muster vollständig darauf heben.

**Architecture:** Reine Doku-Arbeit. `docs/doc-standard.md` definiert vier Pflicht-Garantien (G1 Element-Tabelle, G2 Verschachtelung, G3 Reihenfolge/Platzierung, G4 Zustände). `service-dashboard.md` wird zur Referenzumsetzung. Verankerung in `for-coding-agents.md` und `docs/registry.json`. „Verifikation" = `check_consistency.py` bleibt grün + jede `svc-*`-CSS-Klasse erscheint in der Doc.

**Tech Stack:** Markdown, `docs/registry.json`, `scripts/cli/check_consistency.py` (Python 3 — nur `python3` vorhanden).

---

## Datei-Struktur

- Create: `docs/doc-standard.md` — der Doku-Standard (Definition + G1–G4 + Format-Vorlagen).
- Modify: `docs/registry.json` — neuer `concept`-Eintrag für `doc-standard.md` (sonst Orphan).
- Modify: `docs/service-dashboard.md` — vollständiger Umbau auf G1–G4.
- Modify: `docs/for-coding-agents.md` — Verweis-Abschnitt + Prüflisten-Punkt.

Reihenfolge wichtig: Task 1 legt die Datei **und** den Registry-Eintrag gemeinsam an, damit `check_consistency.py` nach jeder Task grün ist (eine neue Datei ohne Registry-Eintrag wäre ein Orphan-Fehler).

---

### Task 1: `docs/doc-standard.md` erstellen + registrieren

**Files:**
- Create: `docs/doc-standard.md`
- Modify: `docs/registry.json`

- [ ] **Step 1: Datei `docs/doc-standard.md` mit exakt diesem Inhalt anlegen**

````markdown
# Doku-Standard für Komponenten-Docs

Dieser Standard legt fest, wie beschreibende Komponenten-Docs in `docs/` geschrieben
werden, damit ein Coding-Agent eine Komponente **allein aus der Doc** korrekt umsetzen
kann — ohne die Beispiel-HTML in `components/*.html` interpretieren zu müssen.

**Grundregel:** Die Doc ist die Quelle. Das HTML in `components/` ist nur **Verifikation**,
nicht die Spezifikation. Was nur im Beispiel-HTML steht, aber nicht in der Doc, gilt als
nicht spezifiziert.

---

## Geltungsbereich

Der Standard gilt für Docs der Registry-Kategorie **`component`** (siehe
`docs/registry.json`). Konzept-Docs (`concept`, z. B. brand, naming, versioning) und
Infrastruktur (`infra`) sind ausgenommen — sie beschreiben keine zusammensetzbaren
UI-Elemente.

Der Standard schreibt Pflicht-**Informationen** vor, keine starre identische
Abschnittsreihenfolge. Bestehende vollständige Docs erfüllen ihn ggf. bereits;
komponenten-spezifische Zusatzabschnitte bleiben erlaubt.

---

## Die vier Pflicht-Garantien

Jede `component`-Doc MUSS diese vier Informationen vollständig im Text enthalten.

### G1 — Vollständige Element-Tabelle

Jede verwendbare Klasse/jedes Element der Komponente steht in einer Tabelle. **Keine
Klasse darf nur im Beispiel-HTML auftauchen.** Format:

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.beispiel` | Was es tut | Pflicht | `.aktiv`, `.warn` |

### G2 — Struktur / Verschachtelung

Ein expliziter Baum der Eltern-Kind-Hierarchie, sodass die DOM-Verschachtelung ohne
Lesen der `components/*.html` klar ist. Format:

```text
.wrapper
├── .kind-a            (Pflicht)
└── .kind-b            (Optional)
```

### G3 — Reihenfolge & Platzierung

Explizite Prosa-Regeln zur Anordnung/Position — nicht nur aus dem Beispiel ablesbar.

**Projektweite Button-Konvention:** primärer Button zuerst/links, sekundärer als
`btn-ghost` daneben.

### G4 — Zustände & Varianten

Eine Tabelle aller Zustände/Varianten mit der Bedingung „wann verwenden". Format:

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Aktiv | `.aktiv` | Wenn der Dienst läuft |

---

## Prüffrage

Bevor eine Komponenten-Doc als fertig gilt: *Könnte ein Agent die Komponente bauen, ohne
die `components/*.html` zu öffnen?* Wenn nein, fehlt eine der Garantien G1–G4.
````

- [ ] **Step 2: Registry-Eintrag ergänzen**

In `docs/registry.json` in das `components`-Array bei den `concept`-Einträgen einen neuen
Eintrag ergänzen (z. B. direkt nach dem `for-coding-agents`-Eintrag):

```json
    { "id": "doc-standard", "title": "Doku-Standard", "category": "concept",
      "css": [], "doc": ["doc-standard.md"], "html": [] },
```

Auf gültiges JSON achten (Komma zwischen den Einträgen korrekt setzen).

- [ ] **Step 3: Konsistenz-Check grün verifizieren**

Run: `python3 scripts/cli/check_consistency.py`
Expected: Exit 0, „Manifest und Dateien sind konsistent" (Warnungen für `coords`/`utils`
unverändert). KEIN Orphan-Fehler für `doc-standard.md`.

- [ ] **Step 4: JSON-Gültigkeit verifizieren**

Run: `python3 -c "import json; json.load(open('docs/registry.json')); print('json ok')"`
Expected: `json ok`

- [ ] **Step 5: README-Struktur regenerieren**

Da `doc-standard.md` neu im Manifest ist, muss der README-Struktur-Block aktualisiert werden:

Run: `python3 scripts/cli/check_consistency.py --write`
Expected: Exit 0, „README.md AUTOGEN-Abschnitte aktualisiert".
Run: `git diff README.md` — der Diff darf NUR die Zeile `docs/doc-standard.md` im
Struktur-Block hinzufügen (doc-standard ist `concept`, taucht NICHT in der Status-Tabelle auf).

- [ ] **Step 6: Commit**

```bash
git add docs/doc-standard.md docs/registry.json README.md
git commit -m "docs(standard): add interpretation-free doc standard + register it"
```

---

### Task 2: `service-dashboard.md` auf den Standard heben

**Files:**
- Modify: `docs/service-dashboard.md` (vollständiger Ersatz des Inhalts)

Ziel: Alle 31 `svc-*`/`sidebar-status-dot`-Klassen aus `css/service-dashboard.css` erscheinen
in Element-Tabellen (G1); jede der drei Seiten hat einen Verschachtelungs-Baum (G2);
Button-/Header-Platzierung ist als Regel ausformuliert (G3); es gibt eine Zustände-Tabelle (G4).

- [ ] **Step 1: `docs/service-dashboard.md` vollständig durch diesen Inhalt ersetzen**

````markdown
# Service Dashboard

**Referenz-Dateien:** `components/service-dashboard-overview.html` · `components/service-dashboard-detail.html` · `components/service-dashboard-config.html`
**CSS:** `css/service-dashboard.css`
**Status:** definiert · v1.12.2

> Diese Doc folgt `docs/doc-standard.md` (interpretationsfrei). Die Beispiel-HTML in
> `components/` ist Verifikation, nicht Quelle — alles Nötige steht hier im Text.

---

## Überblick

Drei-Seiten-Muster für lokale Raspberry-Pi-Dienst-Überwachung. Basiert auf bestehenden
CI-Klassen; `service-dashboard.css` ergänzt nur was kein bestehendes Muster abdeckt.

### Ladereihenfolge

```css
css/common.css
css/cards.css        /* card-dashboard, card-grid, card-status-dot */
css/badges.css       /* badge-green/red/yellow */
css/buttons.css      /* btn, btn-danger, btn-secondary, btn-ghost, btn-primary */
css/page.css         /* page-header, panel, content-body */
css/sidebar.css      /* sidebar-nav-item, sidebar-status-dot */
css/service-dashboard.css  /* svc-* Klassen — immer zuletzt */
```

---

## Seite 1 — Übersicht (Seitentyp 3: Dashboard)

Zeigt alle Dienste eines Pi als klickbare Kacheln im Card-Grid.

### Verschachtelung (G2)

```text
.card-grid
└── a.card.card-dashboard.card-dashboard-link
    ├── div.card-status-dot[.online|.offline|.unknown]   (Pflicht)
    ├── h3
    │   ├── i.svc-card-icon                               (Optional)
    │   └── span (Titel-Text)                             (Pflicht)
    ├── p.svc-info-line                                   (Optional)
    ├── span.svc-status-line[.online|.offline|.unknown]   (Pflicht)
    └── i.card-dashboard-arrow                            (Pflicht)
```

### Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.card-grid` | Grid-Container der Kacheln (aus `cards.css`) | Pflicht | — |
| `.card.card-dashboard.card-dashboard-link` | Klickbare Dienst-Kachel (aus `cards.css`) | Pflicht | — |
| `.card-status-dot` | Status-Punkt oben in der Kachel (aus `cards.css`) | Pflicht | `.online`, `.offline`, `.unknown` |
| `.svc-card-icon` | FA-Icon inline im h3-Titel (accent, 0.85rem, flex-shrink:0) | Optional | — |
| `.svc-info-line` | Kurzbeschreibung unter Titel (0.75rem, muted) | Optional | — |
| `.svc-status-line` | Statuszeile unten (0.7rem) | Pflicht | `.online`, `.offline`, `.unknown` |
| `.card-dashboard-arrow` | Pfeil-Icon rechts (aus `cards.css`) | Pflicht | — |

### Reihenfolge & Platzierung (G3)

- Reihenfolge in der Kachel: Status-Dot → h3 (Icon, dann Titel) → Info-Zeile → Status-Zeile → Pfeil.
- Wenn `.svc-card-icon` im h3 verwendet wird, MUSS der Textteil in `<span>` stehen, damit
  Truncation korrekt funktioniert.

---

## Seite 2 — Detail (Seitentyp 1: Detail-Seite)

### Verschachtelung (G2)

```text
.page-header
├── .page-header-left
│   ├── (Titelzeile: i.svc-page-icon + h1.page-title + span.badge.badge-*)   (Pflicht)
│   └── p.page-subtitle                                                      (Optional)
└── .page-header-right
    ├── button.btn.btn-danger     (destruktive Aktion, z. B. Neustart)       (Optional)
    └── a.btn.btn-secondary       (Navigation, z. B. Config)                 (Optional)

.svc-data-grid
└── .svc-data-cell                                                          (Pflicht, n×)
    ├── span.svc-data-label                                                 (Pflicht)
    ├── span.svc-data-value[.success|.danger]                              (Pflicht)
    └── span.svc-data-sub                                                   (Optional)
```

### Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.svc-page-icon` | FA-Icon im Page-Header der Detailseite | Pflicht | — |
| `.svc-data-grid` | Responsive Grid: 3/2/1 Spalten (Desktop/Tablet/Mobile) | Pflicht | — |
| `.svc-data-cell` | Einzelne Zelle: panel-deep Hintergrund, 8px Radius | Pflicht | — |
| `.svc-data-label` | Bezeichnung (0.68rem, uppercase, `--subtle`) | Pflicht | — |
| `.svc-data-value` | Wert (0.95rem, 600, `--text`) | Pflicht | `.success`, `.danger` |
| `.svc-data-sub` | Subtext (0.72rem, `--muted`) | Optional | — |

Bestehende Klassen: `.page-header`, `.page-header-left`, `.page-header-right`,
`.page-title`, `.page-subtitle`, `.badge.badge-green/red/yellow`, `.btn.btn-danger`,
`.btn.btn-secondary`.

### Reihenfolge & Platzierung (G3)

- **Header links:** Icon → Titel → Status-Badge in einer Zeile; Subtitle darunter.
- **Header rechts:** Aktions-Buttons. Destruktive Aktionen (Restart) als `btn-danger`,
  Navigation (Config) als `btn-secondary`. Destruktive Aktion zuerst, Navigation danach.
- Nur API-Endpunkte/Aktionen einblenden, die tatsächlich vorhanden sind. Destruktive
  Aktionen immer mit `confirm()` absichern.

---

## Seite 3 — Config (Seitentyp 1: Detail-Seite)

### Verschachtelung (G2)

```text
a.svc-back-link                                              (Pflicht)

(Formularfeld je Typ — siehe Feldtypen-Tabelle)

.svc-form-actions                                            (Pflicht)
├── button.btn.btn-primary   (Speichern, fa-floppy-disk)    (Pflicht)
├── a.btn.btn-ghost          (Abbrechen)                    (Pflicht)
└── span.svc-form-hint       (Hinweis, z. B. Neustart)      (Optional)

.svc-toggle[.on|.warn]                                       (Toggle-Feldtyp)
├── .svc-toggle-track
│   └── .svc-toggle-thumb
├── .svc-toggle-label
└── .svc-toggle-sublabel                                     (Optional)
```

### Feldtypen / Elemente (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.svc-back-link` | Zurück-Navigation oben (mit `fa-arrow-left`) | Pflicht | — |
| `.svc-field` | Standard-Feld: `<input text/number>`, `<select>`, `<textarea>` | Pflicht (je Feld) | — |
| `.svc-field-readonly` | Read-only-Wert als `<div>` statt Input | Optional | — |
| `.svc-field-hint` | Hilfstext unter einem Feld (`<span>`) | Optional | — |
| `.svc-secret` | Wrapper für Passwort-Feld mit Auge-Toggle | Optional | — |
| `.svc-secret-toggle` | Sichtbarkeits-Umschalter im Secret-Feld | Optional | — |
| `.svc-input-prefix` | Wrapper für Input mit Protokoll-Prefix | Optional | — |
| `.svc-input-prefix-label` | Prefix-Label (z. B. `https://`) | Optional | — |
| `.svc-toggle` | Toggle-Switch für Boolean-Config | Optional | `.on` (aktiv), `.warn` (Warnfarbe wenn aktiv) |
| `.svc-toggle-track` | Schiene des Toggles | Pflicht (im Toggle) | — |
| `.svc-toggle-thumb` | Beweglicher Knopf im Track | Pflicht (im Toggle) | — |
| `.svc-toggle-label` | Beschriftung des Toggles | Pflicht (im Toggle) | — |
| `.svc-toggle-sublabel` | Zusatz-/Hilfstext unter dem Toggle-Label | Optional | — |
| `.svc-form-actions` | Aktionsleiste am Formular-Ende | Pflicht | — |
| `.svc-form-hint` | Hinweis in der Aktionsleiste | Optional | — |

### Reihenfolge & Platzierung (G3)

- Zurück-Link steht oben, vor dem Formular.
- **Aktionsleiste (`.svc-form-actions`):** Speichern zuerst als `btn btn-primary`
  (Disketten-Icon `fa-floppy-disk`), direkt daneben Abbrechen als `btn btn-ghost`. Ein
  optionaler `.svc-form-hint` folgt rechts. (Projektweite Konvention: primär zuerst,
  sekundär als Ghost daneben.)

---

## Zustände & Varianten (G4)

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Dienst online | `.card-status-dot.online`, `.svc-status-line.online`, `.badge-green` | Dienst erreichbar/läuft |
| Dienst offline | `.card-status-dot.offline`, `.svc-status-line.offline`, `.badge-red` | Dienst nicht erreichbar |
| Dienst unbekannt | `.card-status-dot.unknown`, `.svc-status-line.unknown`, `.sidebar-status-dot.unknown`, `.badge-yellow` | Status nicht ermittelbar |
| Datenwert positiv | `.svc-data-value.success` | Wert ist im Soll-Zustand (z. B. „Gültig") |
| Datenwert negativ | `.svc-data-value.danger` | Wert signalisiert Fehler/Ausfall |
| Toggle aktiv | `.svc-toggle.on` | Boolean-Config ist eingeschaltet |
| Toggle aktiv mit Warnung | `.svc-toggle.warn` | Eingeschalteter Zustand ist riskant (Warnfarbe) |
| Feld schreibgeschützt | `.svc-field-readonly` | Wert anzeigen, aber nicht editierbar |

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-07 | Auf `docs/doc-standard.md` gehoben (G1–G4, interpretationsfrei). Toggle-Teile inkl. `.svc-toggle-sublabel` ergänzt, Button-Platzierung und Zustände-Tabelle ausformuliert. |
| 2026-06-07 | Initiale Definition. 3 Seiten. svc-* Klassen. Feldtypen-Palette. |
````

- [ ] **Step 2: Verifizieren, dass jede `svc-*`/`sidebar-status-dot`-CSS-Klasse in der Doc vorkommt**

Run:
```bash
cd /root/git/oe5ith-ci
missing=0
for c in $(grep -oE '\.(svc-[a-z-]+|sidebar-status-dot)' css/service-dashboard.css | sed 's/^\.//' | sort -u); do
  grep -q "$c" docs/service-dashboard.md || { echo "FEHLT in Doc: $c"; missing=1; }
done
[ "$missing" = 0 ] && echo "ALLE Klassen dokumentiert"
```
Expected: `ALLE Klassen dokumentiert` (keine `FEHLT`-Zeile).

- [ ] **Step 3: Konsistenz-Check grün verifizieren**

Run: `python3 scripts/cli/check_consistency.py`
Expected: Exit 0 (service-dashboard.md ist bereits registriert; nur Inhalt änderte sich).

- [ ] **Step 4: Commit**

```bash
git add docs/service-dashboard.md
git commit -m "docs(service-dashboard): make interpretation-free per doc-standard (G1-G4)"
```

---

### Task 3: Verankerung in `for-coding-agents.md`

**Files:**
- Modify: `docs/for-coding-agents.md`

- [ ] **Step 1: Verweis-Abschnitt einfügen**

In `docs/for-coding-agents.md` direkt NACH dem Abschnitt `## Neue Komponente registrieren`
(am Ende der Datei) diesen Abschnitt anhängen:

```markdown
## Komponenten-Docs schreiben

Beschreibende Docs für `category: component` folgen `docs/doc-standard.md` und müssen
**interpretationsfrei** sein: Ein Agent muss die Komponente allein aus der Doc bauen können,
ohne die Beispiel-HTML in `components/*.html` zu interpretieren. Pflicht sind die vier
Garantien:

1. **G1** — vollständige Element-Tabelle (jede Klasse mit Zweck, Pflicht/Optional, Modifier).
2. **G2** — Verschachtelungs-Baum (Eltern-Kind-Hierarchie).
3. **G3** — Reihenfolge & Platzierung als Text-Regel (z. B. Speichern primär zuerst,
   Abbrechen als `btn-ghost` daneben).
4. **G4** — Zustände-/Varianten-Tabelle mit „wann verwenden".

`docs/service-dashboard.md` ist das Referenz-Beispiel.
```

- [ ] **Step 2: Prüflisten-Punkt ergänzen**

Im Abschnitt `## Prüfliste vor Abschluss einer Änderung` einen neuen Punkt am Ende der
Checkliste anfügen:

```markdown
- [ ] Geänderte/neue Komponenten-Docs erfüllen `docs/doc-standard.md` (G1–G4, interpretationsfrei).
```

- [ ] **Step 3: Konsistenz-Check grün verifizieren**

Run: `python3 scripts/cli/check_consistency.py`
Expected: Exit 0.

- [ ] **Step 4: Commit**

```bash
git add docs/for-coding-agents.md
git commit -m "docs(agents): require doc-standard for component docs"
```

---

### Task 4: Abschluss-Verifikation

- [ ] **Step 1: Voller Check + Tests**

Run:
```bash
cd /root/git/oe5ith-ci
python3 -m unittest discover -s scripts/cli -p 'test_*.py' 2>&1 | tail -2
python3 scripts/cli/check_consistency.py; echo "exit=$?"
```
Expected: Tests OK (unverändert 10), Check exit 0.

- [ ] **Step 2: README-Idempotenz**

Run: `python3 scripts/cli/check_consistency.py --write && git diff --stat README.md`
Expected: Kein Diff an README.md (Task 1 hat den Struktur-Block bereits regeneriert; doc-standard
ist `concept` → nicht in der component-Status-Tabelle). Falls doch ein Diff: inspizieren und
committen.

---

## Hinweis zum Abschluss (nicht Teil der Tasks)

Reine Doku → **PATCH v1.12.2**. Nach Abschluss: `CHANGELOG.md` unter `Added` (doc-standard)
und `Changed` (service-dashboard interpretationsfrei) ergänzen, taggen, pushen. Das übernimmt
die finishing-a-development-branch-Phase.

---

## Addendum (Task 2b): Layout-Inline-Styles durch CI-Klassen ersetzen

Beim Review von Task 2 zeigte sich: Die `service-dashboard-*.html` nutzen Inline-Styles für
Layout (ohne CI-Klasse) — zugleich Interpretations-Lücke UND CI-Regelverstoß. Damit die Doc
wirklich interpretationsfrei via G1 sein kann, werden CI-Klassen eingeführt. Geht über die
ursprüngliche Doku-Scope hinaus (berührt CSS + 3 HTML), vom Nutzer freigegeben.

**Neue Klassen in `css/service-dashboard.css`:**
- `.svc-page-title-row` — `display:flex; align-items:center; gap:10px; margin-bottom:4px;`
  (Header-Titelzeile Detail/Config). Plus `.svc-page-title-row .page-title { font-size:1.2rem;
  font-weight:600; }` (ersetzt die h1-Inline-Override).
- `.svc-field-grid` — `display:grid; grid-template-columns:1fr 1fr; gap:16px;`
  Modifier `.svc-field-grid--cols-3` → `grid-template-columns:repeat(3,1fr);`.
- `.svc-label-type` — `font-weight:400; color:var(--subtle);` (Typ-Hinweis im Label, „(Text)").
- `.svc-field-code` — `font-family:var(--font-mono); font-size:.8rem; color:var(--code-text);
  resize:vertical;` (JSON-Textarea; ersetzt hardcodiertes `#4ade80` durch Token).
- CSS-Regel `.svc-toggle.warn .svc-toggle-sublabel { color: var(--warning); }` (ersetzt Inline).
- Mono-Inputs nutzen bestehendes `.mono` (typography.css) statt `style="font-family:..."`.

**HTML-Refactor (3 Dateien):** alle o. g. Inline-Styles durch diese Klassen ersetzen.

**Out of scope (andere Komponenten):** `card-warn`-Icon-Abstand (cards.css) und
`sidebar-status-dot` `margin-left:auto` (sidebar.css) bleiben — gehören nicht zum svc-Bauteil.

**Verifikation:** Keine `style="`-Layout-Attribute mehr in den 3 HTML außer den zwei Out-of-scope-
Fällen; `python3 scripts/cli/check_consistency.py` grün; Doc (Task 2-Finale) dokumentiert die
neuen Klassen in den G1-Tabellen.

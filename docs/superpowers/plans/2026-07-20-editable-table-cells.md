# Editierbare Tabellenzellen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zwei neue Zellen-Varianten für `.ci-table` bauen — `.cell-select` (Dropdown mit festem Wertebereich) und `.cell-text` (einzeiliger Freitext) — mit einem gemeinsamen CSS-Zustands-Kontrakt für Inline-Bearbeitung (Ruhezustand, Editing, Saving, Saved, Error).

**Architecture:** Dual-Markup pro Zelle: `<td class="cell-editable cell-select|cell-text">` enthält gleichzeitig ein `.cell-value`-Anzeigeelement und ein natives `.form-select`/`.form-input`. Zustände werden ausschließlich über CSS-Klassen auf dem `<td>` gesteuert (kein DOM-Swap), analog zum bestehenden Sortable Contract in `docs/page.md`. Erweiterung von `css/page.css` (kein neues CSS-File) und `docs/page.md` (kein neues Doc-File) — der bestehende `page`-Registry-Eintrag wird um `components/table-editable.html` ergänzt.

**Tech Stack:** Reines CSS + HTML + Vanilla-JS (nur in der Referenzseite zur Demonstration des Zustands-Kontrakts). Kein Build, kein Test-Framework. Verifikation: `python3 scripts/cli/check_consistency.py`, Struktur-Greps, visuelle Kontrolle der Referenzseite im Browser.

## Global Constraints

- Keine hardcodierten Werte — nur Tokens aus `css/common.css` (Farben, Backgrounds, Borders, Radien, Z-Index, Transitions).
- Keine neuen Tokens. Wiederverwendet: `--accent-subtle`, `--accent-subtle-md`, `--danger`, `--danger-subtle`, `--panel-deep`, `--border-strong`, `--z-tooltip`, `--transition-slow`, `--transition-fast`.
- `.cell-select` nutzt unverändert `.form-select`, `.cell-text` nutzt unverändert `.form-input` (`css/forms.css`) — keine Duplizierung von Input-Styling, kein neues Select/Input-Styling in `page.css`.
- Kein DOM-Swap per `innerHTML` — beide Elemente (`.cell-value` + Eingabeelement) liegen gleichzeitig im DOM, Zustandswechsel ausschließlich über Klassen-Toggle auf `<td>`.
- `.cell-text` ist bewusst einzeilig (kein `<textarea>`, kein Multiline-Modifier — außerhalb des Scopes dieses Plans).
- Keine Persistenz-/API-Logik in CSS oder Referenz-Doku — nur simuliertes Commit im Demo-JS von `components/table-editable.html`.
- `css/demo.css` ausschließlich in `components/table-editable.html`, nie produktiv.
- Jede produktive CSS muss in `css/index.css` importiert sein (bereits erfüllt — `page.css` ist dort bereits importiert) und in `docs/registry.json` registriert sein; `python3 scripts/cli/check_consistency.py` muss fehlerfrei sein.
- Version: additiv → MINOR `v1.23.0`. Filenames ohne Versionsnummer.
- Spec: `docs/superpowers/specs/2026-07-20-editable-table-cells-design.md`.

---

### Task 1: `css/page.css` — Zustands-Kontrakt für editierbare Zellen

**Files:**
- Modify: `css/page.css:281` (direkt nach `.ci-table td.empty { color: var(--subtle); }`, vor dem Kommentarblock `COLUMN GROUPS` in Zeile 283)

**Interfaces:**
- Consumes: Tokens `--accent-subtle`, `--accent-subtle-md`, `--danger`, `--danger-subtle`, `--panel-deep`, `--border-strong`, `--z-tooltip`, `--transition-slow`, `--transition-fast`, `--accent-border` (alle aus `css/common.css`); Klassen `.form-select`, `.form-input` (aus `css/forms.css`, wird von Task 2 im HTML referenziert).
- Produces: Klassen `.cell-editable`, `.cell-select`, `.cell-text`, `.cell-value`, `.is-editing`, `.is-saving`, `.is-saved`, `.is-error`, `.cell-error-tip` — von Task 2 (Referenz-HTML) und Task 3 (Doku) konsumiert.

- [ ] **Step 1: Bestehenden Einfügepunkt verifizieren**

Run: `sed -n '278,284p' css/page.css`
Expected:
```
/* Highlighted Row */
.ci-table tbody tr.highlight td { color: var(--text); }

/* Leere Zelle */
.ci-table td.empty { color: var(--subtle); }

/* ═══════════════════════════════════════
   COLUMN GROUPS
```

Falls die Zeilennummer abweicht (frühere Änderungen an der Datei), den Block anhand des Textes `.ci-table td.empty` lokalisieren — dort wird eingefügt, nicht nach absoluter Zeilennummer.

- [ ] **Step 2: CSS-Block einfügen**

Füge direkt nach `.ci-table td.empty { color: var(--subtle); }` und vor dem `COLUMN GROUPS`-Kommentarblock folgenden Block ein:

```css

/* ═══════════════════════════════════════
   EDITIERBARE ZELLEN (.cell-editable)
   Dual-Markup: .cell-value (Anzeige) +
   .form-select/.form-input (Eingabe) liegen
   gleichzeitig im DOM. Zustand ausschließlich
   über Klassen auf <td>, kein DOM-Swap.
   Voraussetzung: css/forms.css
   ═══════════════════════════════════════ */
.cell-editable {
  position: relative;
  background: var(--accent-subtle);
  cursor: pointer;
}

.cell-editable .form-select,
.cell-editable .form-input {
  display: none;
}

.cell-editable .cell-value {
  cursor: pointer;
}
.cell-editable .cell-value:focus-visible {
  outline: 2px solid var(--accent-border);
  outline-offset: -2px;
}

/* Editing: Eingabeelement sichtbar, Anzeige versteckt */
.cell-editable.is-editing {
  background: transparent;
  cursor: default;
}
.cell-editable.is-editing .cell-value {
  display: none;
}
.cell-editable.is-editing .form-select,
.cell-editable.is-editing .form-input {
  display: block;
}

/* Saving: transiente Sperre während Commit läuft */
.cell-editable.is-saving .form-select,
.cell-editable.is-saving .form-input {
  opacity: 0.6;
  pointer-events: none;
}

/* Saved: kurzes Erfolgs-Feedback (JS entfernt Klasse nach eigenem Timeout) */
.cell-editable.is-saved {
  background: var(--accent-subtle-md);
  transition: background var(--transition-slow);
}

/* Error: Commit fehlgeschlagen / Validierung fehlgeschlagen */
.cell-editable.is-error {
  border: 1px solid var(--danger);
  background: var(--danger-subtle);
}

.cell-error-tip {
  position: absolute;
  z-index: var(--z-tooltip);
  bottom: 100%;
  left: 0;
  margin-bottom: 4px;
  background: var(--panel-deep);
  border: 1px solid var(--border-strong);
  border-radius: 6px;
  padding: 6px 9px;
  font-size: 0.72rem;
  color: var(--danger);
  white-space: nowrap;
}
```

- [ ] **Step 3: Keine hardcodierten Werte verifizieren**

Run: `sed -n '/EDITIERBARE ZELLEN/,/^\/\* ═.*COLUMN GROUPS/p' css/page.css | grep -E '#[0-9a-fA-F]{3,6}|rgba\(|[0-9]+px.*z-index|z-index:\s*[0-9]'`
Expected: kein Treffer (alle Farben/Z-Index laufen über `var(--...)`, `px`-Werte sind nur Radien/Spacing, keine Farb-/Z-Index-Hardcodes).

- [ ] **Step 4: Commit**

```bash
git add css/page.css
git commit -m "feat(page): add .cell-editable state contract for inline table editing"
```

---

### Task 2: Referenz-HTML `components/table-editable.html`

**Files:**
- Create: `components/table-editable.html`

**Interfaces:**
- Consumes: Klassen aus Task 1 (`.cell-editable`, `.cell-select`, `.cell-text`, `.cell-value`, `.is-editing`, `.is-saving`, `.is-saved`, `.is-error`, `.cell-error-tip`), bestehende `.ci-table`/`.panel`/`.panel-header`/`.panel-title`/`.panel-body-flush`/`.panel-body-flush--scroll` (`page.css`), `.form-select`/`.form-input` (`forms.css`).

- [ ] **Step 1: Bestehende Referenzseite mit Tabelle als Vorlage ansehen**

Run: `sed -n '1,20p' components/status-msg.html`
Ziel: identisches `<head>`-Muster übernehmen (kein Build-Tool, direkte `<link>`-Einbindung inkl. FontAwesome-CDN + `css/demo.css`).

- [ ] **Step 2: `components/table-editable.html` schreiben**

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI Reference — Editierbare Tabellenzellen</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="../css/common.css">
<link rel="stylesheet" href="../css/forms.css">
<link rel="stylesheet" href="../css/page.css">
<link rel="stylesheet" href="../css/demo.css">
</head>
<body>

<div class="page-content">

  <!-- ═══ LIVE-DEMO: Klick-Interaktion mit vollem Zustands-Kontrakt ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Editierbare Tabellenzellen — Live-Demo</div>
    <div class="demo-section-desc">
      Klick auf eine Zelle mit blauem Hintergrund öffnet den Bearbeitungsmodus.
      Dropdown-Zelle (Status): Auswahl committet sofort. Freitext-Zelle (Notiz):
      <code>Enter</code>/Blur committet, <code>Escape</code> verwirft. Commit wird
      simuliert (kein echter API-Call) — nach ~600&nbsp;ms erfolgreich, bei Eingabe
      des Worts <code>fehler</code> in der Notiz-Zelle schlägt der Commit absichtlich fehl.
    </div>
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">Nachrichten-Übersicht</div>
      </div>
      <div class="panel-body-flush panel-body-flush--scroll">
        <table class="ci-table" id="demo-table">
          <thead>
            <tr>
              <th class="mono">Zeitstempel</th>
              <th>Status</th>
              <th>Notiz</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="mono">24.4.2026 13:46</td>
              <td class="cell-editable cell-select">
                <span class="cell-value" tabindex="0" role="button">Aktiv</span>
                <select class="form-select" aria-label="Status">
                  <option value="active" selected>Aktiv</option>
                  <option value="inactive">Inaktiv</option>
                  <option value="pending">Ausstehend</option>
                </select>
              </td>
              <td class="cell-editable cell-text">
                <span class="cell-value" tabindex="0" role="button">BH Jurist benötigt 4020 Linz…</span>
                <input class="form-input" type="text" aria-label="Notiz" value="BH Jurist benötigt 4020 Linz…">
              </td>
            </tr>
            <tr>
              <td class="mono">24.4.2026 13:38</td>
              <td class="cell-editable cell-select">
                <span class="cell-value" tabindex="0" role="button">Ausstehend</span>
                <select class="form-select" aria-label="Status">
                  <option value="active">Aktiv</option>
                  <option value="inactive">Inaktiv</option>
                  <option value="pending" selected>Ausstehend</option>
                </select>
              </td>
              <td class="cell-editable cell-text">
                <span class="cell-value" tabindex="0" role="button">–</span>
                <input class="form-input" type="text" aria-label="Notiz" value="">
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ═══ STATISCHE ZUSTÄNDE (ohne JS nachvollziehbar) ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Zustands-Kontrakt (statisch)</div>
    <div class="demo-section-desc">
      Alle fünf Zustände einer <code>.cell-text</code>-Zelle nebeneinander, jeweils
      mit der Klasse fest im HTML gesetzt (kein Klick nötig).
    </div>
    <table class="ci-table" style="max-width: 720px;">
      <thead>
        <tr>
          <th>Zustand</th>
          <th>Notiz</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Ruhezustand</td>
          <td class="cell-editable cell-text">
            <span class="cell-value" tabindex="0" role="button">BH Jurist benötigt 4020 Linz…</span>
            <input class="form-input" type="text" value="BH Jurist benötigt 4020 Linz…">
          </td>
        </tr>
        <tr>
          <td>is-editing</td>
          <td class="cell-editable cell-text is-editing">
            <span class="cell-value" tabindex="0" role="button">BH Jurist benötigt 4020 Linz…</span>
            <input class="form-input" type="text" value="BH Jurist benötigt 4020 Linz…">
          </td>
        </tr>
        <tr>
          <td>is-saving</td>
          <td class="cell-editable cell-text is-editing is-saving">
            <span class="cell-value" tabindex="0" role="button">BH Jurist benötigt 4020 Linz…</span>
            <input class="form-input" type="text" value="BH Jurist benötigt 4020 Linz…">
          </td>
        </tr>
        <tr>
          <td>is-saved</td>
          <td class="cell-editable cell-text is-saved">
            <span class="cell-value" tabindex="0" role="button">BH Jurist benötigt 4020 Linz…</span>
            <input class="form-input" type="text" value="BH Jurist benötigt 4020 Linz…">
          </td>
        </tr>
        <tr>
          <td>is-error</td>
          <td class="cell-editable cell-text is-error">
            <span class="cell-value" tabindex="0" role="button">BH Jurist benötigt 4020 Linz…</span>
            <input class="form-input" type="text" value="BH Jurist benötigt 4020 Linz…" aria-describedby="static-err-tip">
            <div class="cell-error-tip" id="static-err-tip" role="alert">Speichern fehlgeschlagen</div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

</div>

<script>
(function () {
  var activeCell = null;

  var errTipSeq = 0;

  function commitCell(cell, valueEl, inputEl, newValue) {
    cell.classList.remove('is-editing');
    cell.classList.add('is-saving');

    setTimeout(function () {
      cell.classList.remove('is-saving');

      if (newValue.toLowerCase().indexOf('fehler') !== -1) {
        cell.classList.add('is-error');
        var tip = cell.querySelector('.cell-error-tip');
        if (!tip) {
          tip = document.createElement('div');
          tip.className = 'cell-error-tip';
          tip.setAttribute('role', 'alert');
          tip.id = 'demo-err-tip-' + (++errTipSeq);
          cell.appendChild(tip);
          if (inputEl) inputEl.setAttribute('aria-describedby', tip.id);
        }
        tip.textContent = 'Speichern fehlgeschlagen';
        return;
      }

      valueEl.textContent = newValue;
      cell.classList.add('is-saved');
      setTimeout(function () { cell.classList.remove('is-saved'); }, 1200);
    }, 600);
  }

  function openEditing(cell) {
    if (activeCell && activeCell !== cell) {
      activeCell.classList.remove('is-editing');
    }
    cell.classList.remove('is-error');
    var tip = cell.querySelector('.cell-error-tip');
    if (tip) {
      tip.remove();
      var describedInput = cell.querySelector('.form-select, .form-input');
      if (describedInput) describedInput.removeAttribute('aria-describedby');
    }

    cell.classList.add('is-editing');
    activeCell = cell;

    var input = cell.querySelector('.form-select, .form-input');
    if (input) input.focus();
  }

  document.querySelectorAll('#demo-table .cell-editable').forEach(function (cell) {
    var valueEl = cell.querySelector('.cell-value');
    var selectEl = cell.querySelector('.form-select');
    var inputEl = cell.querySelector('.form-input');

    valueEl.addEventListener('click', function () { openEditing(cell); });
    valueEl.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openEditing(cell);
      }
    });

    if (selectEl) {
      selectEl.addEventListener('change', function () {
        var label = selectEl.options[selectEl.selectedIndex].text;
        commitCell(cell, valueEl, selectEl, label);
      });
    }

    if (inputEl) {
      inputEl.addEventListener('blur', function () {
        if (cell.classList.contains('is-editing')) {
          commitCell(cell, valueEl, inputEl, inputEl.value);
        }
      });
      inputEl.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          inputEl.blur();
        } else if (e.key === 'Escape') {
          inputEl.value = valueEl.textContent;
          cell.classList.remove('is-editing');
          activeCell = null;
        }
      });
    }
  });
})();
</script>

</body>
</html>
```

- [ ] **Step 3: Klassen-Existenz verifizieren**

Run: `grep -oE "class=\"[^\"]*\"" components/table-editable.html | grep -oE "cell-[a-z-]*|ci-table[a-z-]*|form-[a-z-]*|panel[a-z-]*|demo-[a-z-]*|is-[a-z]*" | sort -u`
Dann je Klasse prüfen, dass sie in `css/page.css`, `css/forms.css` oder `css/demo.css` definiert ist:
`grep -rn "\.cell-editable\|\.cell-select\|\.cell-text\|\.cell-value\|\.cell-error-tip\|\.is-editing\|\.is-saving\|\.is-saved\|\.is-error" css/page.css`
Expected: alle acht Klassen aus Task 1 kommen vor.

- [ ] **Step 4: Visuell und interaktiv kontrollieren**

Öffne `components/table-editable.html` im Browser. Prüfe:
- Live-Demo-Tabelle: Status-Zelle und Notiz-Zelle haben dezent blauen Hintergrund (`--accent-subtle`) im Ruhezustand.
- Klick auf Status-Zelle öffnet `<select>`, Auswahl committet sofort (kurzes `is-saving`, dann Text aktualisiert, kurzer grünlich-blauer Flash durch `is-saved`).
- Klick auf Notiz-Zelle öffnet `<input>`, fokussiert automatisch. `Escape` verwirft Änderung und schließt. `Enter` oder Klick außerhalb (Blur) committet.
- Notiz-Text mit dem Wort „fehler" eingeben und committen → Zelle bekommt roten Rahmen (`is-error`) + Tooltip „Speichern fehlgeschlagen" oberhalb der Zelle.
- Tab-Taste erreicht `.cell-value` mit sichtbarem Fokusrahmen; `Enter`/`Space` öffnet den Bearbeitungsmodus auch ohne Maus.
- Statische Zustands-Tabelle zeigt alle fünf Zustände optisch unterscheidbar, ohne Interaktion nötig.
- Keine Fehler in der Browser-Konsole.

- [ ] **Step 5: Commit**

```bash
git add components/table-editable.html
git commit -m "docs(table-editable): add components/table-editable.html reference page"
```

---

### Task 3: Doku `docs/page.md` — Abschnitt „Editierbare Tabellenzellen"

**Files:**
- Modify: `docs/page.md` (neuer Abschnitt nach „## Tabelle", vor „## Column-Groups" — aktuell Zeile 210/212, mit `grep -n "^## " docs/page.md` neu verifizieren)

**Interfaces:**
- Consumes: Klassen aus Task 1 (für Element-Tabelle G1), JS-Kontrakt aus Spec §4.

- [ ] **Step 1: Einfügeposition verifizieren**

Run: `grep -n "^## " docs/page.md`
Expected: `## Tabelle` gefolgt von `## Column-Groups` — der neue Abschnitt kommt dazwischen, direkt vor der `## Column-Groups`-Zeile (nach der abschließenden `---`-Trennlinie des Tabellen-Abschnitts).

- [ ] **Step 2: Abschnitt vor „## Column-Groups" einfügen**

```markdown
## Editierbare Tabellenzellen

Erweiterung von `.ci-table` um zwei inline-bearbeitbare Zellen-Varianten: fester
Wertebereich per Dropdown (`.cell-select`) oder einzeiliger Freitext
(`.cell-text`). Dual-Markup pro Zelle — Anzeige- und Eingabeelement liegen
gleichzeitig im DOM, der Zustand wird ausschließlich über CSS-Klassen auf dem
`<td>` gesteuert (kein DOM-Swap per `innerHTML`).

**Keine Persistenz-Logik in der CI.** Wie ein Commit gespeichert wird
(API-Call, Optimistic Update, Fehlerbehandlung), ist Sache der Website —
analog zum Sortable Contract oben: CSS liefert die Zustände, JS-Pflicht ist
die eigentliche Logik.

### Struktur

```text
<td class="cell-editable cell-select|cell-text">
├── .cell-value                    (Pflicht — Anzeige, role="button", tabindex="0")
├── <select class="form-select">   (Pflicht bei .cell-select)
├── <input class="form-input">     (Pflicht bei .cell-text)
└── .cell-error-tip                (Optional — nur bei is-error, role="alert")
```

### Elemente

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.cell-editable` | Basis-Klasse auf `<td>` — aktiviert den Zustands-Kontrakt | Pflicht | `.cell-select`, `.cell-text` |
| `.cell-select` | Variante: Dropdown mit festem Wertebereich | Pflicht (genau eine der beiden Varianten) | — |
| `.cell-text` | Variante: einzeiliger Freitext | Pflicht (genau eine der beiden Varianten) | — |
| `.cell-value` | Anzeigeelement im Ruhezustand, `role="button" tabindex="0"` | Pflicht | — |
| `<select class="form-select">` | Eingabeelement der `.cell-select`-Variante, unverändert aus `docs/forms.md` | Pflicht bei `.cell-select` | — |
| `<input class="form-input" type="text">` | Eingabeelement der `.cell-text`-Variante, unverändert aus `docs/forms.md` | Pflicht bei `.cell-text` | — |
| `.cell-error-tip` | Fehlermeldung, `role="alert"`, per `aria-describedby` mit dem Eingabeelement verknüpft | Optional (nur bei `.is-error`) | — |

### Reihenfolge & Platzierung

- `.cell-value` steht immer als **erstes** Kind im `<td>`, direkt gefolgt vom Eingabeelement (`<select class="form-select">` oder `<input class="form-input">`). `.cell-error-tip` ist immer das **letzte** Kind, wenn vorhanden.
- `.cell-error-tip` wird **erst bei Eintritt in `.is-error`** ins DOM eingefügt (bzw. sichtbar) — nicht vorab unsichtbar mitgerendert. Position: `position: absolute; bottom: 100%; left: 0;` — der Tooltip öffnet **oberhalb** der Zelle, linksbündig zur Zellkante, nie nach rechts oder unten (Tabellenzeilen darunter dürfen nicht verdeckt werden).
- Beim Verlassen des Fehlerzustands (erneuter Klick auf `.cell-value`) wird `.cell-error-tip` aus dem DOM entfernt und `aria-describedby` vom Eingabeelement wieder entfernt — kein verwaistes `aria-describedby` auf ein nicht mehr existierendes Element.
- Innerhalb einer Tabellenzeile ist die Reihenfolge der Spalten frei wählbar — `.cell-editable`-Spalten dürfen beliebig mit normalen, nicht editierbaren `<td>`-Spalten gemischt werden (siehe Beispiel `components/table-editable.html`).

### Zustände (auf `<td class="cell-editable …">`)

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Ruhezustand | *(kein Modifier)* | Zelle ist editierbar, aber nicht aktiv in Bearbeitung. `.cell-value` sichtbar, Eingabeelement `display:none`, Hintergrund `--accent-subtle` als Discoverability-Hinweis. |
| Editing | `.is-editing` | Nutzer hat die Zelle aktiviert (Klick/Enter/Space auf `.cell-value`). Eingabeelement sichtbar + fokussiert, `.cell-value` versteckt. |
| Saving | `.is-saving` | Commit-Request läuft (transient). Eingabeelement `opacity:0.6`, nicht interagierbar. |
| Saved | `.is-saved` | Commit war erfolgreich (transient, JS entfernt die Klasse nach eigenem Timeout, empfohlen ~1200 ms). Kurzer Hintergrund-Flash `--accent-subtle-md`. |
| Error | `.is-error` | Commit oder Validierung ist fehlgeschlagen und bleibt bestehen, bis erneut editiert wird. Rahmen `--danger`, Hintergrund `--danger-subtle`, `.cell-error-tip` sichtbar. |

**Zustandsübergänge (Text-Regel):**

```
Ruhezustand ──Klick/Enter/Space──▶ is-editing
is-editing ──Blur/Change/Enter──▶ is-saving
is-editing ──Escape (nur .cell-text)──▶ Ruhezustand (kein Commit, Wert zurückgesetzt)
is-saving ──Commit OK──▶ is-saved ──Timeout──▶ Ruhezustand
is-saving ──Commit fehlgeschlagen──▶ is-error
is-error ──erneuter Klick──▶ is-editing
```

Der Zustands-Satz ist für `.cell-select` und `.cell-text` identisch.

### JS-Verantwortlichkeiten (Pflicht)

- Klick oder `Enter`/`Space` auf `.cell-value`: `.is-editing` auf dem `<td>` setzen, Eingabeelement fokussieren.
- `change` (Select) / `blur` oder `Enter` (Input): `.is-editing` entfernen, `.is-saving` setzen, Commit auslösen.
- `Escape` nur bei `.cell-text`: Eingabewert auf zuletzt committeten Wert zurücksetzen, `.is-editing` entfernen, kein Commit.
- Commit erfolgreich: `.is-saving` entfernen, `.cell-value`-Text aktualisieren, `.is-saved` setzen und nach ~1200 ms wieder entfernen.
- Commit fehlgeschlagen: `.is-saving` entfernen, `.is-error` setzen, Fehlertext in `.cell-error-tip` schreiben.
- Klick auf `.cell-value` im `.is-error`-Zustand: `.is-error` entfernen, zurück in `.is-editing`.

### Beispiel

```html
<td class="cell-editable cell-select">
  <span class="cell-value" tabindex="0" role="button">Aktiv</span>
  <select class="form-select" aria-label="Status">
    <option value="active" selected>Aktiv</option>
    <option value="inactive">Inaktiv</option>
  </select>
</td>
```

### Regeln

1. Dual-Markup ist Pflicht — kein `innerHTML`-Ersatz des Zellinhalts beim Zustandswechsel (Fokus-Erhalt, Barrierefreiheit).
2. `.cell-select`/`.cell-text` nutzen unverändert `.form-select`/`.form-input` (`docs/forms.md`) — kein eigenes Input-Styling in `page.css`.
3. `.cell-text` ist bewusst einzeilig. Für mehrzeilige Werte ist dies nicht das passende Pattern.
4. Persistenz (API-Call, Fehlerbehandlung bei Netzwerkfehlern) ist Sache der Website, nicht der CI.
5. `.form-select`/`.form-input` in editierbaren Zellen bekommen `aria-label` aus dem Spalten-Header-Kontext.
```

- [ ] **Step 3: Änderungshistorie ergänzen**

Run: `grep -n "^## Änderungshistorie" docs/page.md`
Füge am Ende der zugehörigen Tabelle eine neue Zeile hinzu:

```markdown
| 2026-07-20 | Editierbare Tabellenzellen ergänzt — `.cell-select`, `.cell-text`, Zustands-Kontrakt (is-editing/is-saving/is-saved/is-error). |
```

- [ ] **Step 4: Verifizieren**

Run: `grep -n "cell-editable\|cell-select\|cell-text\|cell-value\|is-editing\|is-saving\|is-saved\|is-error\|cell-error-tip" docs/page.md`
Expected: neuer Abschnitt vorhanden, alle acht Klassen aus Task 1 kommen mindestens einmal in der Element- oder Zustandstabelle vor.

- [ ] **Step 5: Commit**

```bash
git add docs/page.md
git commit -m "docs(page): add Editierbare Tabellenzellen section (G1-G4)"
```

---

### Task 4: Registry, Consistency-Check, Changelog, Version

**Files:**
- Modify: `docs/registry.json`
- Modify: `CHANGELOG.md`
- Modify: `README.md` (auto-generiert durch `check_consistency.py --write`)

**Interfaces:**
- Consumes: alle Artefakte aus Task 1–3.

- [ ] **Step 1: Bestehenden `page`-Registry-Eintrag erweitern**

In `docs/registry.json` den bestehenden Eintrag mit `"id": "page"` finden (aktuell, verifizieren mit `grep -n -A3 '"id": "page"' docs/registry.json`):

```json
    { "id": "page", "title": "Seitenstruktur", "category": "component",
      "css": ["page.css"], "doc": ["page.md", "page-types.md"],
      "html": ["page-types.html", "status-msg.html"] },
```

Ersetzen durch (nur das `html`-Array ändert sich, Formatierung/Zeilenumbrüche identisch beibehalten):

```json
    { "id": "page", "title": "Seitenstruktur", "category": "component",
      "css": ["page.css"], "doc": ["page.md", "page-types.md"],
      "html": ["page-types.html", "status-msg.html", "table-editable.html"] },
```

Auf gültiges JSON achten (Komma-Platzierung unverändert lassen, nur das `html`-Array anpassen). Falls sich die tatsächliche Formatierung im Repo inzwischen unterscheidet (andere Einrückung/Zeilenumbrüche), diese beibehalten und nur das `html`-Array-Element ergänzen.

- [ ] **Step 2: Consistency-Check (Gate)**

Run: `python3 scripts/cli/check_consistency.py`
Expected: keine Fehler.

- [ ] **Step 3: README regenerieren**

Run: `python3 scripts/cli/check_consistency.py --write`
Expected: README-Blöcke (zwischen den AUTOGEN-Markern) aktualisiert, weiterhin keine Fehler.

- [ ] **Step 4: CHANGELOG ergänzen**

Aktuellen obersten Versions-Eintrag bestimmen:

Run: `grep -n "^## v" CHANGELOG.md | head -3`
Stand dieses Plans ist das `## v1.22.0 - 2026-07-19`. Falls sich der oberste Eintrag inzwischen geändert hat, den neuen Block **darüber** einfügen, sonst direkt über `## v1.22.0 - 2026-07-19`:

```markdown
## v1.23.0 - 2026-07-20

### Added
- **Editierbare Tabellenzellen** — Erweiterung von `.ci-table` um `.cell-select` (Dropdown mit festem Wertebereich) und `.cell-text` (einzeiliger Freitext) für Inline-Bearbeitung. Gemeinsamer Zustands-Kontrakt (`is-editing`/`is-saving`/`is-saved`/`is-error`) in `css/page.css`, Referenz `components/table-editable.html`, Doku-Abschnitt in `docs/page.md`. Keine neuen Tokens — reuse `--accent-subtle`, `--accent-subtle-md`, `--danger`, `--danger-subtle`, `.form-select`/`.form-input`.

---
```

Halte dich exakt an das bestehende CHANGELOG-Format (`## vX.Y.Z - YYYY-MM-DD`, Kategorie `Added`, Trennlinie `---` danach).

- [ ] **Step 5: Finale Verifikation**

Run: `python3 scripts/cli/check_consistency.py`
Expected: keine Fehler.

Run: `grep -n "table-editable" docs/registry.json README.md CHANGELOG.md`
Expected: in allen drei Dateien vorhanden.

- [ ] **Step 6: Commit**

```bash
git add docs/registry.json README.md CHANGELOG.md
git commit -m "chore(registry): register table-editable.html, update changelog for v1.23.0"
```

---

### Task 5: Release-Tag

**Files:** keine (Git-Tag-Operation)

**Interfaces:**
- Consumes: finalen Stand aus Task 1–4.

- [ ] **Step 1: Sicherstellen, dass alle vorherigen Commits vorhanden sind**

Run: `git log --oneline -6`
Expected: Commits aus Task 1–4 sichtbar (page.css, table-editable.html, page.md, registry/changelog).

- [ ] **Step 2: Tag setzen**

```bash
git tag -a v1.23.0 -m "Release v1.23.0"
```

- [ ] **Step 3: Verifizieren**

Run: `git tag -l "v1.23.0" -n1`
Expected: `v1.23.0          Release v1.23.0`

Tag-Push (`git push origin v1.23.0`) und Commit-Push liegen außerhalb dieses Plans — dafür explizit beim Nutzer nachfragen, nicht automatisch pushen.

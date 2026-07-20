# Editierbare Tabellenzellen (`.cell-editable`) — Design / Spec

**Datum:** 2026-07-20
**Status:** Freigegeben · zur Umsetzung
**Angefragt von:** Daniel Herbrik — Tabellen mit Daten aus einer Datenbank, bei
  denen einzelne Felder inline bearbeitbar sein sollen: entweder mit fest
  begrenztem Wertebereich (Dropdown) oder als Freitext.
**Version:** additiv → MINOR `v1.23.0`

---

## 1. Zweck & Abgrenzung

`docs/page.md` definiert bereits `.ci-table` als CI-konforme Tabelle inkl.
`.ci-table--sortable`-Contract (CSS liefert visuelle States, JS-Pflicht ist die
eigentliche Logik). Für Anwendungsfälle, in denen Tabellenwerte direkt in der
Zelle bearbeitet werden sollen (z. B. Status-Feld mit fixem Wertebereich,
Freitext-Notiz), fehlt bisher ein Pattern.

Dieses Spec erweitert `.ci-table` um zwei Zellen-Varianten:

- **`.cell-select`** — Wertebereich ist auf eine feste Menge X begrenzt,
  Bearbeitung über natives `<select class="form-select">`.
- **`.cell-text`** — freie, einzeilige Texteingabe über
  `<input class="form-input" type="text">`.

Beide teilen sich einen gemeinsamen visuellen Zustands-Kontrakt (§3).

**Bewusst nicht hier:**

- **Keine Persistenz-Logik.** Wie ein Commit tatsächlich gespeichert wird
  (API-Call, Optimistic Update, Retry, Offline-Handling) ist Sache der
  jeweiligen Website — analog zum Sortable Contract, bei dem die CI nur
  CSS-Zustände liefert und die Sortierlogik JS-Pflicht der Website ist. Die CI
  definiert ausschließlich, **welche Zustände es gibt und wie sie aussehen**,
  nicht wie sie befüllt werden.
- **Kein mehrzeiliger Freitext.** `.cell-text` ist bewusst auf einzeilige
  Werte beschränkt (kurze DB-Felder wie Namen, IDs, Status-Notizen). Für
  längere Texte (Kommentare, Beschreibungen) ist dies nicht das passende
  Pattern — dafür müsste ein eigenes `.cell-text--multiline`-Pattern separat
  spezifiziert werden, wenn der Bedarf entsteht (YAGNI, hier nicht Teil des
  Scopes).
- **Keine Zeilen-weise Mehrfachbearbeitung.** Jede Zelle wird unabhängig
  bearbeitet und committed (Auto-Commit on Blur/Change), kein gemeinsamer
  Save/Cancel-Zustand über mehrere Zellen einer Zeile hinweg.
- **Keine Datenquelle für Dropdown-Optionen.** Woher die erlaubten Werte einer
  `.cell-select`-Spalte kommen (statisch im HTML oder dynamisch aus der DB
  nachgeladen), ist Sache der Website. Die CI definiert nur die Darstellung
  des `<select>` selbst (bestehende `.form-select`-Klasse, siehe
  `docs/forms.md`).

---

## 2. HTML-Struktur

Dual-Markup-Ansatz: Jede editierbare `<td>` enthält **beide** Elemente
(Anzeige + Eingabe) gleichzeitig im DOM. JS toggelt nur eine Klasse, es wird
kein DOM per `innerHTML` ersetzt (robuster, Fokus bleibt erhalten,
barrierefreier als DOM-Swap).

```html
<table class="ci-table">
  <thead>
    <tr>
      <th>Zeitstempel</th>
      <th>Status</th>
      <th>Notiz</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="mono">24.4.2026 13:46</td>

      <!-- Dropdown-Variante: fester Wertebereich -->
      <td class="cell-editable cell-select">
        <span class="cell-value" tabindex="0" role="button">Aktiv</span>
        <select class="form-select" aria-label="Status">
          <option value="active" selected>Aktiv</option>
          <option value="inactive">Inaktiv</option>
          <option value="pending">Ausstehend</option>
        </select>
      </td>

      <!-- Freitext-Variante: einzeilig -->
      <td class="cell-editable cell-text">
        <span class="cell-value" tabindex="0" role="button">BH Jurist benötigt 4020 Linz…</span>
        <input class="form-input" type="text" aria-label="Notiz"
               value="BH Jurist benötigt 4020 Linz…">
      </td>
    </tr>
  </tbody>
</table>
```

Bei Fehlerzustand (§3) zusätzlich ein Tooltip-Element im Ruhezustand-Teil der
Zelle:

```html
<td class="cell-editable cell-text is-error">
  <span class="cell-value" tabindex="0" role="button">…</span>
  <input class="form-input" type="text" aria-describedby="err-1234" …>
  <div class="cell-error-tip" id="err-1234" role="alert">Speichern fehlgeschlagen</div>
</td>
```

**Regeln:**

- `.cell-value` = Anzeigeelement, `role="button"` + `tabindex="0"` für
  Tastatur-Trigger im Ruhezustand.
- `.form-select` / `.form-input` bekommt `aria-label` aus dem
  Spalten-Header-Text (kein sichtbares Label pro Zelle nötig, da der
  `<th>`-Kontext bereits die Bedeutung liefert).
- Nicht editierbare Spalten in derselben Tabelle bleiben normale `<td>` ohne
  `.cell-editable` — Mischung aus editierbaren und reinen Anzeige-Spalten ist
  der Standardfall.

---

## 3. Zustands-Kontrakt (CSS-Klassen auf `<td class="cell-editable …">`)

| Klasse | Bedeutung | Visuelle Umsetzung |
|---|---|---|
| *(kein Modifier)* | Ruhezustand, editierbar | `.cell-value` sichtbar, Eingabeelement `display: none`; `background: var(--accent-subtle)`, `cursor: pointer` |
| `.is-editing` | Aktiv in Bearbeitung | `.cell-value` `display: none`, Eingabeelement sichtbar + fokussiert |
| `.is-saving` | Commit läuft (transient) | Eingabeelement `opacity: 0.6`, `pointer-events: none` |
| `.is-saved` | Kurzzeitiges Erfolgs-Feedback (transient, JS entfernt Klasse nach eigenem Timeout) | `background: var(--accent-subtle-md)` mit `transition`, kein Loop-`@keyframes` |
| `.is-error` | Commit fehlgeschlagen / Validierung fehlgeschlagen | `border-color: var(--danger)`, `background: var(--danger-subtle)`; `.cell-error-tip` sichtbar |

**Zustandsübergänge:**

```
Ruhezustand ──Klick/Enter/Space──▶ is-editing
is-editing ──Blur/Change/Enter──▶ is-saving
is-editing ──Escape (nur .cell-text)──▶ Ruhezustand (Wert zurückgesetzt, kein Commit)
is-saving ──Commit OK──▶ is-saved ──Timeout──▶ Ruhezustand
is-saving ──Commit fehlgeschlagen──▶ is-error
is-error ──erneuter Klick──▶ is-editing
```

Der Zustands-Satz ist für `.cell-select` und `.cell-text` identisch — kein
separater State-Satz pro Variante.

---

## 4. JS-Kontrakt (Pflicht)

Analog zum Sortable Contract in `docs/page.md`: CSS liefert ausschließlich die
visuellen Zustände. Persistenz und Datenfluss sind Sache der Website.

| Ereignis | JS-Verantwortung |
|---|---|
| Klick oder `Enter`/`Space` auf `.cell-value` im Ruhezustand | `.is-editing` auf `<td>` setzen, Eingabeelement fokussieren |
| `change` (Select) / `blur` oder `Enter` (Input) | `.is-editing` entfernen, `.is-saving` setzen, Commit auslösen |
| `Escape` (nur `.cell-text`) | Eingabewert auf zuletzt committeten Wert zurücksetzen, `.is-editing` entfernen, kein Commit |
| Commit erfolgreich | `.is-saving` entfernen, `.cell-value`-Text aktualisieren, `.is-saved` setzen, nach ~1200 ms wieder entfernen |
| Commit fehlgeschlagen | `.is-saving` entfernen, `.is-error` setzen, Fehlertext in `.cell-error-tip` schreiben |
| Klick auf `.cell-value` im `.is-error`-Zustand | `.is-error` entfernen, zurück in `.is-editing` |

Die Website ist zusätzlich dafür verantwortlich, `Escape` bei `.cell-select`
sinnvoll zu behandeln (natives `<select>`-Verhalten schließt das Dropdown
bereits ohne Auswahl — kein zusätzlicher Reset nötig, da `change` nur bei
tatsächlicher Auswahl feuert).

---

## 5. Tokens

Keine neuen Tokens. Wiederverwendet:

| Token | Verwendung |
|---|---|
| `--accent-subtle` | Ruhezustand-Hintergrund (Discoverability) |
| `--accent-subtle-md` | `.is-saved`-Hintergrund |
| `--danger`, `--danger-subtle` | `.is-error`-Rahmen/Hintergrund, analog `.form-input.error` |
| `--panel-deep`, `--border-strong` | `.cell-error-tip`-Hintergrund/Rahmen, analog `.chart-tooltip` |
| `--z-tooltip` | `.cell-error-tip`-Stapelung |
| `.form-select`, `.form-input` | unverändert übernommen aus `docs/forms.md` |

---

## 6. Accessibility

- `.cell-value` (Ruhezustand-Trigger): `role="button"`, `tabindex="0"`,
  reagiert auf Klick, `Enter`, `Space`.
- `.form-select` / `.form-input`: `aria-label` aus Spalten-Header-Text.
- `.cell-error-tip`: `role="alert"`, per `aria-describedby` mit dem
  Eingabeelement verknüpft.
- Fokus bleibt beim Zustandswechsel immer auf demselben DOM-Knoten oder wird
  bewusst auf das neu sichtbare Element gesetzt (kein Fokusverlust durch
  DOM-Konstruktion, da kein DOM-Swap stattfindet).
- Farbe ist nie alleiniger Träger einer Bedeutung: `.is-error` hat zusätzlich
  den Tooltip-Text, `.is-saved` ist rein dekorativ-transient und trägt keine
  eigenständige Information, die nicht auch im aktualisierten `.cell-value`
  steht.

---

## 7. Referenz-Galerie

`components/table-editable.html` (mit `css/demo.css`, wie andere
Referenzseiten):

1. Eine `.ci-table` mit gemischten Spalten: normale Anzeige-Spalte,
   `.cell-select`-Spalte, `.cell-text`-Spalte.
2. Statische Darstellung aller fünf Zustände (Ruhezustand, `.is-editing`,
   `.is-saving`, `.is-saved`, `.is-error`) als eigene Beispielzeilen, damit der
   visuelle Kontrakt ohne JS nachvollziehbar ist.
3. Minimales Vanilla-JS, das den Zustands-Kontrakt aus §4 demonstriert
   (Commit wird simuliert, kein echter API-Call).

---

## 8. Doku, Registry, Versionierung

- `docs/page.md` — neuer Abschnitt „Editierbare Tabellenzellen" direkt nach
  dem bestehenden Tabellen-Abschnitt (inkl. Sortable Contract), mit
  vollständiger Element-Tabelle (G1), Verschachtelungs-Baum `<td>` →
  `.cell-value` + `.form-select`/`.form-input` (G2), Zustandsreihenfolge aus
  §3 als Text-Regel (G3) sowie Zustände-Tabelle mit „wann verwenden" (G4) —
  gemäß `docs/doc-standard.md`.
- `css/page.css` — neue Regeln für `.cell-editable`, `.cell-select`,
  `.cell-text`, State-Modifier (§3), `.cell-error-tip`. Keine neue CSS-Datei,
  da Erweiterung des bestehenden Tabellen-Patterns in `page.css`.
- `components/table-editable.html` — neue Referenzdatei (§7).
- `docs/registry.json` — bestehender `page`-Eintrag (`id: "page"`) wird um
  `components/table-editable.html` im `html`-Array erweitert; kein neuer
  Registry-Eintrag, da Erweiterung der bestehenden `page`-Komponente.
- `CHANGELOG.md` — `Added`-Eintrag für `v1.23.0`.
- Version: MINOR `v1.23.0` (rein additiv, keine Breaking Changes an
  `.ci-table`).

---

## 9. Akzeptanzkriterien

- [ ] `css/page.css`: `.cell-editable`, `.cell-select`, `.cell-text`,
      `.is-editing`, `.is-saving`, `.is-saved`, `.is-error`, `.cell-error-tip`
      definiert, ausschließlich mit bestehenden Tokens (§5), keine
      hardcodierten Farben/Radien/Z-Index.
- [ ] Beide Varianten nutzen unverändert `.form-select` / `.form-input` aus
      `css/forms.css` — keine Duplizierung von Input-Styling.
- [ ] `docs/page.md`: neuer Abschnitt erfüllt G1–G4 (`docs/doc-standard.md`),
      interpretationsfrei ohne Rückgriff auf `components/table-editable.html`.
- [ ] `components/table-editable.html`: gemischte Tabelle mit allen fünf
      Zuständen sichtbar + funktionierendes Demo-JS gemäß §4; nutzt
      `css/demo.css`.
- [ ] `docs/registry.json`: `page`-Eintrag um `table-editable.html` ergänzt;
      `python3 scripts/cli/check_consistency.py` endet ohne neuen
      Fehler/Warnung.
- [ ] `CHANGELOG.md`: `Added`-Eintrag `v1.23.0`.
- [ ] Accessibility-Kriterien aus §6 erfüllt (Tastaturbedienbarkeit,
      `role="alert"` auf Fehler-Tooltip, `aria-label` auf Eingabeelementen).
- [ ] Keine neuen Tokens; keine Persistenz-/API-Logik in CSS oder
      Referenz-Doku (nur simuliertes Commit im Demo-JS).

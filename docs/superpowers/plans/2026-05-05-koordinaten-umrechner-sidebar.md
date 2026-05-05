# Sidebar Typ 7 — Koordinaten-Umrechner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Neuen Sidebar-Typ 7 (Koordinaten-Umrechner) als wiederverwendbare CI-Komponente definieren — CSS-Klassen, HTML-Referenz und Dokumentation.

**Architecture:** `css/coords.css` enthält alle `.coord-*` Klassen. Die Datei wird über `css/index.css` importiert. `components/sidebar-types.html` erhält eine Typ-7-Demo-Sektion. `docs/sidebar-types.md` wird um den neuen Typ erweitert.

**Tech Stack:** Vanilla CSS (CSS Custom Properties / Tokens aus `css/common.css`), HTML5

---

## Datei-Übersicht

| Datei | Aktion | Zweck |
|---|---|---|
| `css/sidebar.css` | Modify | `.tool-sep` ergänzen (fehlt bisher in der CSS-Datei, nur in Komponenten-Inline-Style) |
| `css/coords.css` | Create | Alle `.coord-*` Klassen für Typ 7 |
| `css/index.css` | Modify | `@import "coords.css"` ergänzen |
| `components/sidebar-types.html` | Modify | CSS für Typ 7 in `<style>`-Block + HTML-Demo-Sektion |
| `docs/sidebar-types.md` | Modify | Typ 7 in Tabelle, Entscheidungsbaum, Beschreibung, Änderungshistorie |
| `CHANGELOG.md` | Modify | v1.4.0 Added-Eintrag |

---

## Task 1: `.tool-sep` in `css/sidebar.css` ergänzen

`.tool-sep` ist aktuell nur im Inline-Style von `components/sidebar-types.html` definiert — fehlt als echte CI-Klasse. Da sie in Typen 3, 4 und 7 gebraucht wird, gehört sie in `sidebar.css`.

**Files:**
- Modify: `css/sidebar.css` — nach Zeile 41 (`.sidebar-sep`)

- [ ] **Step 1: Einfügen**

  In `css/sidebar.css` nach der Zeile `.sidebar-sep { ... }` (aktuell Zeile 41) einfügen:

  ```css
  .tool-sep { height: 1px; background: var(--border); margin: 10px 0; }
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep -n "tool-sep" css/sidebar.css
  ```
  Erwartete Ausgabe: eine Zeile mit der neuen Regel.

- [ ] **Step 3: Commit**

  ```bash
  git add css/sidebar.css
  git commit -m "feat: add .tool-sep to sidebar.css"
  ```

---

## Task 2: `css/coords.css` erstellen

Neue Datei mit allen CSS-Klassen für den Koordinaten-Umrechner-Block.

**Files:**
- Create: `css/coords.css`

- [ ] **Step 1: Datei anlegen**

  Erstelle `css/coords.css` mit folgendem Inhalt:

  ```css
  /*
   * OE5ITH CI — coords.css
   * Sidebar Typ 7: Koordinaten-Umrechner
   *
   * Abhängigkeit: css/common.css (Tokens)
   * Einbinden: css/index.css (automatisch über @import)
   */

  /* ═══════════════════════════════════════
     COORD-BLOCK — Container je Koordinatensystem
     ═══════════════════════════════════════ */

  .coord-block {
    padding: 10px 12px;
    border-left: 3px solid transparent;
    cursor: pointer;
    transition: border-color var(--transition-fast), background var(--transition-fast);
  }
  .coord-block:hover:not(.active) {
    background: rgba(255,255,255,0.02);
  }
  .coord-block.active {
    border-left-color: var(--accent);
    cursor: default;
  }

  /* ═══════════════════════════════════════
     COORD-BLOCK-HEADER — Titel + Copy-Button
     ═══════════════════════════════════════ */

  .coord-block-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  .coord-block-title {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: var(--muted);
    transition: color var(--transition-fast);
  }
  .coord-block.active .coord-block-title {
    color: var(--accent);
  }
  .coord-copy {
    background: none;
    border: none;
    padding: 2px 4px;
    color: var(--subtle);
    font-size: 0.72rem;
    cursor: pointer;
    border-radius: 3px;
    line-height: 1;
    transition: color var(--transition-fast), background var(--transition-fast);
  }
  .coord-copy:hover {
    color: var(--text);
    background: rgba(255,255,255,0.06);
  }

  /* ═══════════════════════════════════════
     COORD-ROW — Standard-Zeile (Label + Feld)
     ═══════════════════════════════════════ */

  .coord-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 5px;
  }
  .coord-row:last-child { margin-bottom: 0; }

  .coord-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--muted);
    width: 32px;
    flex-shrink: 0;
    text-align: right;
  }

  /* ═══════════════════════════════════════
     COORD-INPUT — Basis-Eingabefeld
     ═══════════════════════════════════════ */

  .coord-input {
    flex: 1;
    background: var(--panel-deep);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 0.82rem;
    font-family: var(--font-mono);
    padding: 0 8px;
    height: 30px;
    outline: none;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-input::placeholder { color: var(--subtle); }
  .coord-input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
  }
  .coord-input[readonly] {
    background: var(--panel);
    border-color: transparent;
    color: var(--muted);
    cursor: default;
  }
  .coord-input[readonly]:focus {
    border-color: transparent;
    box-shadow: none;
  }
  .coord-input.coord-input-error {
    border-color: var(--danger);
    box-shadow: 0 0 0 2px rgba(239,68,68,0.12);
  }

  /* ═══════════════════════════════════════
     COORD-INPUT-FULL — Volles Feld ohne Label (Maidenhead)
     ═══════════════════════════════════════ */

  .coord-input-full {
    width: 100%;
    background: var(--panel-deep);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 0.82rem;
    font-family: var(--font-mono);
    padding: 0 8px;
    height: 30px;
    outline: none;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-input-full::placeholder { color: var(--subtle); }
  .coord-input-full:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
  }
  .coord-input-full[readonly] {
    background: var(--panel);
    border-color: transparent;
    color: var(--muted);
    cursor: default;
  }
  .coord-input-full[readonly]:focus {
    border-color: transparent;
    box-shadow: none;
  }

  /* ═══════════════════════════════════════
     COORD-ROW-DMS — DMS-Zeile (3 schmale Felder + Suffix)
     ═══════════════════════════════════════ */

  .coord-row-dms {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 5px;
  }
  .coord-row-dms:last-child { margin-bottom: 0; }
  .coord-row-dms .coord-label { margin-right: 4px; }

  .coord-input-dms {
    width: 52px;
    flex-shrink: 0;
    background: var(--panel-deep);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 0.82rem;
    font-family: var(--font-mono);
    padding: 0 6px;
    height: 30px;
    outline: none;
    text-align: center;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-input-dms::placeholder { color: var(--subtle); }
  .coord-input-dms:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
  }
  .coord-input-dms[readonly] {
    background: var(--panel);
    border-color: transparent;
    color: var(--muted);
    cursor: default;
  }
  .coord-input-dms[readonly]:focus {
    border-color: transparent;
    box-shadow: none;
  }

  .coord-suffix {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--muted);
    width: 14px;
    text-align: center;
    flex-shrink: 0;
  }

  /* ═══════════════════════════════════════
     COORD-ROW-INLINE — 2 Feld-Paare nebeneinander (MGRS GZD + 100km)
     ═══════════════════════════════════════ */

  .coord-row-inline {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 5px;
  }
  .coord-row-inline:last-child { margin-bottom: 0; }

  .coord-input-short {
    width: 52px;
    flex-shrink: 0;
    background: var(--panel-deep);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 0.82rem;
    font-family: var(--font-mono);
    padding: 0 6px;
    height: 30px;
    outline: none;
    text-align: center;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-input-short::placeholder { color: var(--subtle); }
  .coord-input-short:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
  }
  .coord-input-short[readonly] {
    background: var(--panel);
    border-color: transparent;
    color: var(--muted);
    cursor: default;
  }
  .coord-input-short[readonly]:focus {
    border-color: transparent;
    box-shadow: none;
  }

  /* ═══════════════════════════════════════
     COORD-SELECT — Dropdown (BMN Meridianstreifen)
     ═══════════════════════════════════════ */

  .coord-select {
    flex: 1;
    background: var(--panel-deep);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 0.82rem;
    font-family: inherit;
    padding: 0 24px 0 8px;
    height: 30px;
    outline: none;
    cursor: pointer;
    appearance: none;
    -webkit-appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23555' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 8px center;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-select:hover { border-color: var(--border-strong); }
  .coord-select:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
  }
  .coord-select option { background: var(--panel-deep); color: var(--text); }
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep -c "coord-" css/coords.css
  ```
  Erwartete Ausgabe: Zahl > 30 (alle Klassen vorhanden).

- [ ] **Step 3: Commit**

  ```bash
  git add css/coords.css
  git commit -m "feat: add css/coords.css — Sidebar Typ 7 Koordinaten-Umrechner"
  ```

---

## Task 3: `css/index.css` — Import ergänzen

**Files:**
- Modify: `css/index.css`

- [ ] **Step 1: Import einfügen**

  In `css/index.css` nach `@import "forms.css";` einfügen:

  ```css
  @import "coords.css";
  ```

  Der Abschnitt „5. Interaktion" sieht danach so aus:

  ```css
  /* 5. Interaktion */
  @import "forms.css";
  @import "coords.css";
  @import "modal.css";
  @import "toast.css";
  ```

- [ ] **Step 2: Prüfen**

  ```bash
  grep "coords" css/index.css
  ```
  Erwartete Ausgabe: `@import "coords.css";`

- [ ] **Step 3: Commit**

  ```bash
  git add css/index.css
  git commit -m "feat: register coords.css in index.css"
  ```

---

## Task 4: Typ 7 in `components/sidebar-types.html`

Zwei Änderungen an derselben Datei: CSS im `<style>`-Block ergänzen, dann HTML-Demo-Sektion vor `</body>` einfügen.

**Files:**
- Modify: `components/sidebar-types.html`

- [ ] **Step 1: CSS in `<style>`-Block einfügen**

  Nach dem `/* Tool Sep */`-Block (nach `.btn-primary:hover { ... }`, aktuell Zeile ~242) einfügen:

  ```css
  /* ══════════════════════════════════════
     COORD-BLOCK (Typ 7)
     ══════════════════════════════════════ */
  .coord-block {
    padding:10px 12px;
    border-left:3px solid transparent;
    cursor:pointer;
    transition:border-color var(--transition-fast), background var(--transition-fast);
  }
  .coord-block:hover:not(.active) { background:rgba(255,255,255,0.02); }
  .coord-block.active { border-left-color:var(--accent); cursor:default; }

  .coord-block-header {
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:8px;
  }
  .coord-block-title {
    font-size:0.65rem; font-weight:700; letter-spacing:0.8px;
    text-transform:uppercase; color:var(--muted);
    transition:color var(--transition-fast);
  }
  .coord-block.active .coord-block-title { color:var(--accent); }
  .coord-copy {
    background:none; border:none; padding:2px 4px;
    color:var(--subtle); font-size:0.72rem; cursor:pointer;
    border-radius:3px; line-height:1;
    transition:color var(--transition-fast), background var(--transition-fast);
  }
  .coord-copy:hover { color:var(--text); background:rgba(255,255,255,0.06); }

  .coord-row { display:flex; align-items:center; gap:8px; margin-bottom:5px; }
  .coord-row:last-child { margin-bottom:0; }
  .coord-label { font-size:0.68rem; font-weight:600; color:var(--muted); width:32px; flex-shrink:0; text-align:right; }

  .coord-input {
    flex:1; background:var(--panel-deep); border:1px solid var(--border);
    border-radius:4px; color:var(--text); font-size:0.82rem;
    font-family:var(--font-mono); padding:0 8px; height:30px; outline:none;
    transition:border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-input::placeholder { color:var(--subtle); }
  .coord-input:focus { border-color:var(--accent); box-shadow:0 0 0 2px rgba(59,130,246,0.15); }
  .coord-input[readonly] { background:var(--panel); border-color:transparent; color:var(--muted); cursor:default; }
  .coord-input[readonly]:focus { border-color:transparent; box-shadow:none; }
  .coord-input.coord-input-error { border-color:var(--danger); box-shadow:0 0 0 2px rgba(239,68,68,0.12); }

  .coord-input-full {
    width:100%; background:var(--panel-deep); border:1px solid var(--border);
    border-radius:4px; color:var(--text); font-size:0.82rem;
    font-family:var(--font-mono); padding:0 8px; height:30px; outline:none;
    transition:border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-input-full::placeholder { color:var(--subtle); }
  .coord-input-full:focus { border-color:var(--accent); box-shadow:0 0 0 2px rgba(59,130,246,0.15); }
  .coord-input-full[readonly] { background:var(--panel); border-color:transparent; color:var(--muted); cursor:default; }
  .coord-input-full[readonly]:focus { border-color:transparent; box-shadow:none; }

  .coord-row-dms { display:flex; align-items:center; gap:4px; margin-bottom:5px; }
  .coord-row-dms:last-child { margin-bottom:0; }
  .coord-row-dms .coord-label { margin-right:4px; }
  .coord-input-dms {
    width:52px; flex-shrink:0; background:var(--panel-deep); border:1px solid var(--border);
    border-radius:4px; color:var(--text); font-size:0.82rem; font-family:var(--font-mono);
    padding:0 6px; height:30px; outline:none; text-align:center;
    transition:border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-input-dms::placeholder { color:var(--subtle); }
  .coord-input-dms:focus { border-color:var(--accent); box-shadow:0 0 0 2px rgba(59,130,246,0.15); }
  .coord-input-dms[readonly] { background:var(--panel); border-color:transparent; color:var(--muted); cursor:default; }
  .coord-input-dms[readonly]:focus { border-color:transparent; box-shadow:none; }
  .coord-suffix { font-size:0.75rem; font-weight:700; color:var(--muted); width:14px; text-align:center; flex-shrink:0; }

  .coord-row-inline { display:flex; align-items:center; gap:8px; margin-bottom:5px; }
  .coord-row-inline:last-child { margin-bottom:0; }
  .coord-input-short {
    width:52px; flex-shrink:0; background:var(--panel-deep); border:1px solid var(--border);
    border-radius:4px; color:var(--text); font-size:0.82rem; font-family:var(--font-mono);
    padding:0 6px; height:30px; outline:none; text-align:center;
    transition:border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-input-short::placeholder { color:var(--subtle); }
  .coord-input-short:focus { border-color:var(--accent); box-shadow:0 0 0 2px rgba(59,130,246,0.15); }
  .coord-input-short[readonly] { background:var(--panel); border-color:transparent; color:var(--muted); cursor:default; }
  .coord-input-short[readonly]:focus { border-color:transparent; box-shadow:none; }

  .coord-select {
    flex:1; background:var(--panel-deep); border:1px solid var(--border);
    border-radius:4px; color:var(--text); font-size:0.82rem; font-family:inherit;
    padding:0 24px 0 8px; height:30px; outline:none; cursor:pointer;
    appearance:none; -webkit-appearance:none;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23555' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat:no-repeat; background-position:right 8px center;
    transition:border-color var(--transition-fast), box-shadow var(--transition-fast);
  }
  .coord-select:hover { border-color:var(--border-strong); }
  .coord-select:focus { border-color:var(--accent); box-shadow:0 0 0 2px rgba(59,130,246,0.15); }
  .coord-select option { background:var(--panel-deep); color:var(--text); }
  ```

- [ ] **Step 2: HTML-Demo-Sektion einfügen**

  Direkt vor `</body>` (aktuell Zeile 806) einfügen:

  ```html
  <!-- ═══ TYP 7: KOORDINATEN-UMRECHNER ═══ -->
  <div class="section">
    <div class="section-label">Typ 7 — Koordinaten-Umrechner</div>
    <div class="section-desc">
      Bidirektionaler Umrechner: Eingabe in beliebigem System, alle anderen werden live umgerechnet.
      Aktiver Block = Eingabe (Accent-Border links). Klick auf inaktiven Block aktiviert ihn.
    </div>
    <div class="screen">
      <div class="m-tb">
        <div class="m-brand"><img src="assets/logo.svg"> OESITH</div>
        <div class="m-nav"><a>Hintergrund ▾</a><a>Zoom</a></div>
      </div>
      <div class="m-layout">
        <div class="sidebar" style="height:640px">
          <div class="sidebar-inner">

            <!-- WGS84 Dezimalgrad — aktiv -->
            <div class="coord-block active">
              <div class="coord-block-header">
                <span class="coord-block-title">WGS84 Dezimalgrad</span>
                <button class="coord-copy" title="Kopieren"><i class="fa-solid fa-copy"></i></button>
              </div>
              <div class="coord-row">
                <span class="coord-label">Lat.</span>
                <input class="coord-input" type="text" inputmode="decimal" placeholder="48.123456" value="48.387564">
              </div>
              <div class="coord-row">
                <span class="coord-label">Lon.</span>
                <input class="coord-input" type="text" inputmode="decimal" placeholder="14.654321" value="14.514321">
              </div>
            </div>

            <div class="tool-sep"></div>

            <!-- WGS84 DMS — inaktiv -->
            <div class="coord-block">
              <div class="coord-block-header">
                <span class="coord-block-title">WGS84 DMS</span>
                <button class="coord-copy" title="Kopieren"><i class="fa-solid fa-copy"></i></button>
              </div>
              <div class="coord-row-dms">
                <span class="coord-label">Lat.</span>
                <input class="coord-input-dms" type="text" inputmode="numeric" placeholder="48" value="48" readonly>
                <input class="coord-input-dms" type="text" inputmode="numeric" placeholder="23" value="23" readonly>
                <input class="coord-input-dms" type="text" inputmode="decimal" placeholder="15.4" value="15.4" readonly>
                <span class="coord-suffix">N</span>
              </div>
              <div class="coord-row-dms">
                <span class="coord-label">Lon.</span>
                <input class="coord-input-dms" type="text" inputmode="numeric" placeholder="14" value="14" readonly>
                <input class="coord-input-dms" type="text" inputmode="numeric" placeholder="30" value="30" readonly>
                <input class="coord-input-dms" type="text" inputmode="decimal" placeholder="51.6" value="51.6" readonly>
                <span class="coord-suffix">E</span>
              </div>
            </div>

            <div class="tool-sep"></div>

            <!-- UTM — inaktiv -->
            <div class="coord-block">
              <div class="coord-block-header">
                <span class="coord-block-title">UTM</span>
                <button class="coord-copy" title="Kopieren"><i class="fa-solid fa-copy"></i></button>
              </div>
              <div class="coord-row">
                <span class="coord-label">Zone</span>
                <input class="coord-input" type="text" placeholder="33U" value="33U" readonly>
              </div>
              <div class="coord-row">
                <span class="coord-label">E</span>
                <input class="coord-input" type="text" inputmode="numeric" placeholder="411234" value="431421" readonly>
              </div>
              <div class="coord-row">
                <span class="coord-label">N</span>
                <input class="coord-input" type="text" inputmode="numeric" placeholder="5332100" value="5362145" readonly>
              </div>
            </div>

            <div class="tool-sep"></div>

            <!-- BMN — inaktiv -->
            <div class="coord-block">
              <div class="coord-block-header">
                <span class="coord-block-title">BMN</span>
                <button class="coord-copy" title="Kopieren"><i class="fa-solid fa-copy"></i></button>
              </div>
              <div class="coord-row">
                <span class="coord-label">M</span>
                <select class="coord-select">
                  <option value="M28">M28</option>
                  <option value="M31" selected>M31</option>
                  <option value="M34">M34</option>
                </select>
              </div>
              <div class="coord-row">
                <span class="coord-label">HW</span>
                <input class="coord-input" type="text" inputmode="numeric" placeholder="5332100" value="362145" readonly>
              </div>
              <div class="coord-row">
                <span class="coord-label">RW</span>
                <input class="coord-input" type="text" inputmode="numeric" placeholder="411234" value="131421" readonly>
              </div>
            </div>

            <div class="tool-sep"></div>

            <!-- MGRS — inaktiv -->
            <div class="coord-block">
              <div class="coord-block-header">
                <span class="coord-block-title">MGRS</span>
                <button class="coord-copy" title="Kopieren"><i class="fa-solid fa-copy"></i></button>
              </div>
              <div class="coord-row-inline">
                <span class="coord-label">GZD</span>
                <input class="coord-input-short" type="text" placeholder="33U" value="33U" readonly>
                <span class="coord-label">100km</span>
                <input class="coord-input-short" type="text" placeholder="VP" value="VP" readonly>
              </div>
              <div class="coord-row">
                <span class="coord-label">E</span>
                <input class="coord-input" type="text" inputmode="numeric" placeholder="41123" value="31421" readonly>
              </div>
              <div class="coord-row">
                <span class="coord-label">N</span>
                <input class="coord-input" type="text" inputmode="numeric" placeholder="33210" value="62145" readonly>
              </div>
            </div>

            <div class="tool-sep"></div>

            <!-- Maidenhead — inaktiv -->
            <div class="coord-block">
              <div class="coord-block-header">
                <span class="coord-block-title">Maidenhead</span>
                <button class="coord-copy" title="Kopieren"><i class="fa-solid fa-copy"></i></button>
              </div>
              <div class="coord-row">
                <input class="coord-input-full" type="text" placeholder="JN77TX" value="JN78AJ" readonly>
              </div>
            </div>

          </div>
          <div class="sidebar-footer"><span>v1.4.0</span><span class="sidebar-footer-dot"></span></div>
        </div>
        <div class="m-map-bg"><span class="m-map-label">Leaflet / MapLibre</span></div>
      </div>
    </div>
    <p class="annotation">
      <strong>Aktiver Block:</strong> Accent-Border links + Titel in <code>--accent</code>.
      Felder editierbar. <strong>Inaktive Blöcke:</strong> Kein Rand, Felder <code>readonly</code>
      (gedimmt). Klick auf Block macht ihn aktiv. <code>.coord-input-error</code>
      für Fehler-State (rote Border). Keine Umrechnungslogik im CI — App-Sache.
    </p>
  </div>
  ```

- [ ] **Step 3: Visuell prüfen**

  Datei im Browser öffnen:
  ```bash
  open components/sidebar-types.html
  # oder: xdg-open components/sidebar-types.html
  ```

  Prüfen:
  - Typ 7 Sektion am Ende sichtbar
  - WGS84 Dezimalgrad hat blaue Border links, Titel blau
  - Alle anderen Blöcke ohne Rand, Felder grau/readonly-Optik
  - DMS-Zeilen: 3 schmale Felder + N/E Suffix
  - MGRS erste Zeile: GZD + 100km nebeneinander
  - Maidenhead: volles Feld ohne Label
  - BMN: Dropdown für M28/M31/M34 sichtbar
  - Hover auf inaktivem Block: leichte Aufhellung

- [ ] **Step 4: Commit**

  ```bash
  git add components/sidebar-types.html
  git commit -m "feat: add Typ 7 Koordinaten-Umrechner to sidebar-types.html"
  ```

---

## Task 5: `docs/sidebar-types.md` aktualisieren

**Files:**
- Modify: `docs/sidebar-types.md`

- [ ] **Step 1: Typ 7 in Übersichtstabelle ergänzen**

  In der Tabelle nach Zeile `| 6 | Status-Panel | ADS-B/AIS Live-Stats |` einfügen:

  ```markdown
  | 7 | Koordinaten-Umrechner | coord.oe5ith.at |
  ```

- [ ] **Step 2: Entscheidungsbaum ergänzen**

  Nach dem Block `Zeigt die Sidebar nur Live-Daten (read-only)? ...` und vor `Kombinationen nötig?` einfügen:

  ```markdown
  Gibt der Nutzer Koordinaten ein und will zwischen Systemen umrechnen?
  │
  └── JA → Typ 7: Koordinaten-Umrechner
  ```

- [ ] **Step 3: Typ-7-Beschreibung vor `## Panels stapeln` einfügen**

  ```markdown
  ## Typ 7 — Koordinaten-Umrechner

  **Beispiel:** coord.oe5ith.at

  **Wann verwenden:**
  Karten-Seiten mit bidirektionalem Koordinaten-Umrechner. Nutzer gibt Koordinaten
  in einem beliebigen System ein — alle anderen Systeme werden live umgerechnet
  und der Punkt auf der Karte gesetzt.

  **Elemente:**
  - `.coord-block` je Koordinatensystem (aktiv oder inaktiv)
  - `.coord-block-header`: Systemname + Copy-Button (`.coord-copy`)
  - `.coord-row`: Standard-Zeile mit `.coord-label` + `.coord-input`
  - `.coord-row-dms`: DMS-Zeile mit 3 × `.coord-input-dms` + `.coord-suffix` (N/S, E/W)
  - `.coord-row-inline`: 2 Feld-Paare nebeneinander (MGRS: GZD + 100km-Square)
  - `.coord-input-full`: Volles Feld ohne Label (Maidenhead)
  - `.coord-select`: Dropdown für Meridianstreifen (BMN: M28/M31/M34)
  - `tool-sep` zwischen Blöcken

  **Zustände:**

  | Zustand | CSS | Felder |
  |---|---|---|
  | Aktiver Block (Eingabe) | `.coord-block.active` | Border links `--accent`, Titel `--accent`, editierbar |
  | Inaktiver Block (Ausgabe) | `.coord-block` | Kein Rand, `readonly`, Farbe `--muted` |
  | Feld-Fehler | `.coord-input-error` | Border `--danger` |

  **Regeln:**
  - Exakt ein Block ist zur Zeit aktiv — Klick auf inaktiven Block wechselt die Aktivierung
  - Copy-Button immer sichtbar (aktiv + inaktiv) — Format ist App-spezifisch
  - Kein Submit-Button — Umrechnung erfolgt live per App-JS
  - Karten-Punkt wird automatisch gesetzt sobald gültige Koordinaten vorliegen
  - Umrechnungslogik, Zone-Defaults und Copy-Format sind nicht Teil des CI
  ```

- [ ] **Step 4: Änderungshistorie ergänzen**

  In der Tabelle `## Änderungshistorie` eine neue Zeile einfügen:

  ```markdown
  | 2026-05-05 | Typ 7: Koordinaten-Umrechner ergänzt (`coords.css`, `.coord-block` Pattern) |
  ```

- [ ] **Step 5: Commit**

  ```bash
  git add docs/sidebar-types.md
  git commit -m "docs: add Typ 7 Koordinaten-Umrechner to sidebar-types.md"
  ```

---

## Task 6: `CHANGELOG.md` für v1.4.0

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Neuen Versionsblock einfügen**

  Nach der Trennlinie `---` (nach Zeile 17, vor `## v1.3.0`) einfügen:

  ```markdown
  ## v1.4.0 - 2026-05-05

  ### Added

  - `css/coords.css` (neu): Sidebar Typ 7 — Koordinaten-Umrechner Pattern.
    - `.coord-block` / `.coord-block.active` — Container mit Accent-Border-Links für aktives System.
    - `.coord-block-header`, `.coord-block-title`, `.coord-copy` — Titelzeile mit Copy-Button.
    - `.coord-row`, `.coord-label`, `.coord-input` — Standard-Zeile für 2-Feld-Systeme (WGS84 Dezimalgrad, UTM, BMN).
    - `.coord-row-dms`, `.coord-input-dms`, `.coord-suffix` — DMS-Zeile mit 3 schmalen Feldern + N/S, E/W Suffix.
    - `.coord-row-inline`, `.coord-input-short` — Inline-Zeile für 2 Feld-Paare nebeneinander (MGRS GZD + 100km-Square).
    - `.coord-input-full` — Volles Feld ohne Label (Maidenhead Grid).
    - `.coord-input-error` — Fehler-State (rote Border).
    - `.coord-select` — Dropdown für Meridianstreifen (BMN M28/M31/M34).
  - `css/sidebar.css`: `.tool-sep` ergänzt (war bisher nur in Komponenten-Inline-Style definiert).
  - `components/sidebar-types.html`: Typ 7 Demo-Sektion mit allen 6 Koordinatensystemen.
  - `docs/sidebar-types.md`: Typ 7 Beschreibung, Entscheidungsbaum-Erweiterung.

  ---
  ```

- [ ] **Step 2: Commit**

  ```bash
  git add CHANGELOG.md
  git commit -m "chore: update CHANGELOG.md for v1.4.0"
  ```

---

## Abschluss-Checkliste

- [ ] `css/coords.css` existiert, alle Klassen aus der Spec vorhanden
- [ ] `css/index.css` importiert `coords.css`
- [ ] `css/sidebar.css` hat `.tool-sep`
- [ ] `components/sidebar-types.html` zeigt alle 6 Koordinatensysteme korrekt (visuell geprüft)
- [ ] Aktiver Block hat Accent-Border links + Titel in Accent-Farbe
- [ ] Inaktive Blöcke: Felder grau, kein Rand
- [ ] `docs/sidebar-types.md` vollständig (Tabelle, Baum, Beschreibung, Historie)
- [ ] `CHANGELOG.md` v1.4.0 vorhanden
- [ ] 6 Commits, einer je Task

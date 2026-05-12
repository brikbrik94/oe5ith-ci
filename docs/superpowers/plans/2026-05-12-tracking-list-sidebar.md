# Tracking-Liste Sidebar (Typ 8 Redesign) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Typ 8 vollständig neu definieren: `.object-detail*`-Klassen entfernen, neue `.tracking-list`/`.tracking-item*`-Klassen für scrollbare Objekt-Liste mit Mode-Switch und Expand-Verhalten ergänzen.

**Architecture:** Drei Dateien werden angepasst — CSS (Klassen tauschen), HTML-Demo (Typ 8 Sektion neu), Docs (Typ 8 Eintrag neu). Kein Build-Schritt, direkte CSS/HTML-Änderungen. Neue Klassen reuten `.segmented` aus `forms.css` und `.result-kv`/`.result-empty` aus `sidebar.css` wiederverwendet — keine Abhängigkeiten auf diese Klassen ändern sich.

**Tech Stack:** CSS (Token-basiert, `css/common.css`), HTML, kein Build-Schritt.

**Spec:** `docs/superpowers/specs/2026-05-12-tracking-list-sidebar-design.md`

---

## Datei-Map

| Datei | Aktion | Inhalt |
|---|---|---|
| `css/sidebar.css` | Modify (Z. 337–368) | `.object-detail*` entfernen; `.tracking-*` Klassen einfügen |
| `components/sidebar-types.html` | Modify (Z. 1081–1225) | Typ 8 Demo-Sektion komplett ersetzen |
| `docs/sidebar-types.md` | Modify (Z. 337–428) | Typ 8 Abschnitt komplett ersetzen |
| `CHANGELOG.md` | Modify | Unreleased-Abschnitt ergänzen |

---

## Task 1: CSS — `.object-detail*` entfernen, `.tracking-*` einfügen

**Files:**
- Modify: `css/sidebar.css` (Zeilen 337–368)

- [ ] **Schritt 1: Datei lesen**

`css/sidebar.css` lesen. Den Block zwischen `/* ═══ TYP 8 — OBJEKT-DETAIL ═══ */` (Z. 337) und `/* ═══ MOBILE ═══ */` (Z. 370) identifizieren.

- [ ] **Schritt 2: Block ersetzen**

Den gesamten Block (Z. 337–369, also `/* ═══ TYP 8 … */` bis zur Leerzeile vor `/* ═══ MOBILE ═══ */`) ersetzen durch:

```css
/* ═══ TYP 8 — TRACKING-LISTE ═══ */
.tracking-list { display: flex; flex-direction: column; gap: 4px; }
.tracking-item {
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--panel-deep);
  cursor: pointer;
  overflow: hidden;
}
.tracking-item.active { border-left: 2px solid var(--accent); }
.tracking-item-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
}
.tracking-item-icon {
  font-size: 0.72rem;
  color: var(--muted);
  width: 14px;
  text-align: center;
  flex-shrink: 0;
}
.tracking-item-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.tracking-item-chevron {
  font-size: 0.65rem;
  color: var(--muted);
  flex-shrink: 0;
  transition: transform var(--transition-fast);
}
.tracking-item.active .tracking-item-chevron { transform: rotate(180deg); }
.tracking-item-body { display: none; padding: 0 8px 8px; }
.tracking-item.active .tracking-item-body { display: block; }
```

- [ ] **Schritt 3: Visuell prüfen**

`components/sidebar-types.html` im Browser öffnen. Alle anderen Typen (1–7, 9) müssen unverändert aussehen. Kein CSS-Fehler in der Dev-Console.

- [ ] **Schritt 4: Commit**

```bash
git add css/sidebar.css
git commit -m "feat: replace object-detail CSS with tracking-list for Typ 8"
```

---

## Task 2: HTML-Demo — Typ 8 Sektion in `components/sidebar-types.html` ersetzen

**Files:**
- Modify: `components/sidebar-types.html` (Zeilen 1081–1225)

- [ ] **Schritt 1: Datei lesen**

`components/sidebar-types.html` lesen. Den Block von Zeile 1081 (`<!-- ═══ TYP 8: OBJEKT-DETAIL ═══ -->`) bis Zeile 1225 (schließendes `</div>` der Sektion, unmittelbar vor `<!-- ═══ TYP 9: GEOCODER-SUCHE ═══ -->`) identifizieren.

- [ ] **Schritt 2: Sektion ersetzen**

Den gesamten Typ-8-Block (Z. 1081–1225) ersetzen durch:

```html
<!-- ═══ TYP 8: TRACKING-LISTE ═══ -->
<div class="section">
  <div class="section-label">Typ 8 — Tracking-Liste</div>
  <div class="section-desc">ADS-B / AIS Tracking-Sidebar. Zeigt alle empfangenen Objekte als scrollbare Liste. Mode-Switch filtert nach Typ. Klick auf Item klappt Details auf und hebt das Objekt auf der Karte hervor. Immer kombiniert mit Typ 6 (Status-Panel oben, <code>.tool-sep</code> als Trenner).</div>

  <!-- Hauptzustand: Liste mit Objekten, ein Item aufgeklappt -->
  <div class="screen">
    <div class="m-tb">
      <div class="m-brand"><img src="assets/logo.svg"> OESITH</div>
      <div class="m-nav"><a>OSM Standard ▾</a><a>Zoom</a></div>
    </div>
    <div class="m-layout">
      <div class="sidebar" style="height:460px">
        <div class="sidebar-inner">

          <!-- Status-Panel (Typ 6) -->
          <div class="status-panel">
            <div class="status-row">
              <div class="status-row-left">
                <i class="fa-solid fa-plane status-row-icon"></i>
                <span class="status-row-name">ADS-B Flugzeuge</span>
              </div>
              <div class="status-row-right">
                <span class="status-row-value">42</span>
                <span class="status-dot on"></span>
              </div>
            </div>
            <div class="status-row">
              <div class="status-row-left">
                <i class="fa-solid fa-ship status-row-icon"></i>
                <span class="status-row-name">AIS Schiffe</span>
              </div>
              <div class="status-row-right">
                <span class="status-row-value">7</span>
                <span class="status-dot on"></span>
              </div>
            </div>
            <div class="status-row">
              <div class="status-row-left">
                <i class="fa-solid fa-tower-broadcast status-row-icon"></i>
                <span class="status-row-name">Receiver</span>
              </div>
              <div class="status-row-right">
                <span class="status-row-value">online</span>
                <span class="status-dot on"></span>
              </div>
            </div>
            <div class="status-row">
              <div class="status-row-left">
                <i class="fa-solid fa-arrow-right-arrow-left status-row-icon"></i>
                <span class="status-row-name">Pakete/min</span>
              </div>
              <div class="status-row-right">
                <span class="status-row-value">284</span>
              </div>
            </div>
          </div>

          <div class="tool-sep"></div>

          <!-- Mode-Switch -->
          <div class="segmented">
            <button class="segmented-btn active">Alle</button>
            <button class="segmented-btn">ADS-B</button>
            <button class="segmented-btn">AIS</button>
          </div>

          <!-- Tracking-Liste -->
          <div class="tracking-list">

            <!-- Item collapsed -->
            <div class="tracking-item" data-type="adsb">
              <div class="tracking-item-header">
                <i class="fa-solid fa-plane tracking-item-icon"></i>
                <span class="tracking-item-name">AUA123</span>
                <span class="badge badge-blue">ADS-B</span>
                <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
              </div>
            </div>

            <!-- Item aufgeklappt + aktiv (ADS-B) -->
            <div class="tracking-item active" data-type="adsb">
              <div class="tracking-item-header">
                <i class="fa-solid fa-plane tracking-item-icon"></i>
                <span class="tracking-item-name">OE-LXA</span>
                <span class="badge badge-blue">ADS-B</span>
                <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
              </div>
              <div class="tracking-item-body">
                <div class="result-kv">
                  <div class="result-kv-item">
                    <span class="result-kv-label">Höhe</span>
                    <span class="result-kv-value">8.450 ft</span>
                  </div>
                  <div class="result-kv-item">
                    <span class="result-kv-label">Speed</span>
                    <span class="result-kv-value">485 kt</span>
                  </div>
                  <div class="result-kv-item">
                    <span class="result-kv-label">Kurs</span>
                    <span class="result-kv-value">247°</span>
                  </div>
                  <div class="result-kv-item">
                    <span class="result-kv-label">RSSI</span>
                    <span class="result-kv-value">−82 dBm</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- AIS-Item collapsed -->
            <div class="tracking-item" data-type="ais">
              <div class="tracking-item-header">
                <i class="fa-solid fa-ship tracking-item-icon"></i>
                <span class="tracking-item-name">NORDIC ODEN</span>
                <span class="badge badge-gray">AIS</span>
                <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
              </div>
            </div>

          </div>

        </div>
        <div class="sidebar-footer"><span>v2.3.0</span><span class="sidebar-footer-dot"></span></div>
      </div>
      <div class="m-map-bg"><span class="m-map-label">Leaflet / MapLibre</span></div>
    </div>
  </div>
  <p class="annotation">
    <strong>Struktur:</strong> Status-Panel (Typ 6) oben · <code>.tool-sep</code> · <code>.segmented</code> Mode-Switch (Alle / ADS-B / AIS) · <code>.tracking-list</code> mit <code>.tracking-item</code>-Items.<br>
    Aktives Item: <code>.tracking-item.active</code> — zeigt <code>.tracking-item-body</code>, dreht Chevron (180°), accent border-left.<br>
    ADS-B → <code>.badge-blue</code> + <code>fa-plane</code>, AIS → <code>.badge-gray</code> + <code>fa-ship</code>.<br>
    JS: Klick auf <code>.tracking-item-header</code> → <code>.active</code> toggeln + Karte highlighten. Kartenklick → passendes Item per <code>data-type</code>/<code>data-id</code> suchen, <code>.active</code> setzen, <code>scrollIntoView()</code>. Mode-Switch → Items per <code>data-type</code> filtern.
  </p>

  <!-- Leerzustand -->
  <div class="screen" style="max-width:320px;margin-top:16px">
    <div class="m-tb">
      <div class="m-brand"><img src="assets/logo.svg"> OESITH</div>
      <div class="m-nav"><a>OSM Standard ▾</a><a>Zoom</a></div>
    </div>
    <div class="m-layout">
      <div class="sidebar" style="height:240px">
        <div class="sidebar-inner">
          <div class="status-panel">
            <div class="status-row">
              <div class="status-row-left">
                <i class="fa-solid fa-plane status-row-icon"></i>
                <span class="status-row-name">ADS-B Flugzeuge</span>
              </div>
              <div class="status-row-right">
                <span class="status-row-value">0</span>
                <span class="status-dot off"></span>
              </div>
            </div>
            <div class="status-row">
              <div class="status-row-left">
                <i class="fa-solid fa-ship status-row-icon"></i>
                <span class="status-row-name">AIS Schiffe</span>
              </div>
              <div class="status-row-right">
                <span class="status-row-value">0</span>
                <span class="status-dot off"></span>
              </div>
            </div>
          </div>
          <div class="tool-sep"></div>
          <div class="segmented">
            <button class="segmented-btn active">Alle</button>
            <button class="segmented-btn">ADS-B</button>
            <button class="segmented-btn">AIS</button>
          </div>
          <div class="result-empty">
            <i class="fa-solid fa-satellite-dish"></i>
            Warte auf Empfang…
          </div>
        </div>
        <div class="sidebar-footer"><span>v2.3.0</span><span class="sidebar-footer-dot"></span></div>
      </div>
      <div class="m-map-bg"><span class="m-map-label">Leaflet / MapLibre</span></div>
    </div>
  </div>
  <p class="annotation">
    <strong>Leerzustand:</strong> <code>.result-empty</code> unterhalb des Mode-Switch solange keine Objekte empfangen wurden (oder der aktive Filter keine Treffer hat).
  </p>
</div>
```

- [ ] **Schritt 3: Visuell prüfen**

`components/sidebar-types.html` im Browser öffnen und prüfen:
- Typ 8 zeigt die neue Tracking-Liste mit Mode-Switch, zwei collapsed Items und einem aufgeklappten aktiven Item (OE-LXA)
- Das aktive Item hat accent-farbene linke Border und zeigt die result-kv Felder
- Der Chevron des aktiven Items ist um 180° gedreht
- Leerzustand zeigt `result-empty` mit Satellite-Icon
- Alle anderen Typen (1–7, 9) sind unverändert
- Keine Fehler in der Dev-Console

- [ ] **Schritt 4: Commit**

```bash
git add components/sidebar-types.html
git commit -m "feat: replace Typ 8 demo with tracking-list (mode-switch + expand)"
```

---

## Task 3: Docs — Typ 8 in `docs/sidebar-types.md` neu schreiben

**Files:**
- Modify: `docs/sidebar-types.md` (Zeilen 337–428)

- [ ] **Schritt 1: Datei lesen**

`docs/sidebar-types.md` lesen. Den Block `## Typ 8 — Objekt-Detail` (Z. 337) bis zum Ende des Abschnitts (Z. 428, vor `## Panels stapeln`) identifizieren.

- [ ] **Schritt 2: Typ 8 Abschnitt ersetzen**

Den gesamten Typ-8-Abschnitt (Z. 337–428) ersetzen durch:

```markdown
## Typ 8 — Tracking-Liste

**Beispiel:** map.oe5ith.at/tracking

**Wann verwenden:**
Tracking-/Monitoring-Karten die alle empfangenen Objekte (Flugzeuge, Schiffe)
in einer scrollbaren Liste zeigen. Mode-Switch filtert nach Typ.
Klick auf ein Item klappt Details auf und hebt das Objekt auf der Karte hervor.
Immer in Kombination mit Typ 6 (Stats-Panel), getrennt durch `tool-sep`.

**Zustände:**

| Zustand | Anzeige |
|---|---|
| Keine Objekte empfangen | `.result-empty` mit Icon + Hinweistext |
| Objekte vorhanden | `.tracking-list` mit `.tracking-item`-Items |
| Item ausgewählt | `.tracking-item.active` — aufgeklappt + Karte highlighted |

**HTML — Mode-Switch:**

```html
<div class="segmented">
  <button class="segmented-btn active">Alle</button>
  <button class="segmented-btn">ADS-B</button>
  <button class="segmented-btn">AIS</button>
</div>
```

**HTML — Tracking-Liste (ein collapsed, ein aktiv aufgeklappt):**

```html
<div class="tracking-list">

  <!-- collapsed -->
  <div class="tracking-item" data-type="adsb">
    <div class="tracking-item-header">
      <i class="fa-solid fa-plane tracking-item-icon"></i>
      <span class="tracking-item-name">AUA123</span>
      <span class="badge badge-blue">ADS-B</span>
      <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
    </div>
  </div>

  <!-- aufgeklappt + aktiv (ADS-B) -->
  <div class="tracking-item active" data-type="adsb">
    <div class="tracking-item-header">
      <i class="fa-solid fa-plane tracking-item-icon"></i>
      <span class="tracking-item-name">OE-LXA</span>
      <span class="badge badge-blue">ADS-B</span>
      <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
    </div>
    <div class="tracking-item-body">
      <div class="result-kv">
        <div class="result-kv-item">
          <span class="result-kv-label">Höhe</span>
          <span class="result-kv-value">8.450 ft</span>
        </div>
        <div class="result-kv-item">
          <span class="result-kv-label">Speed</span>
          <span class="result-kv-value">485 kt</span>
        </div>
        <div class="result-kv-item">
          <span class="result-kv-label">Kurs</span>
          <span class="result-kv-value">247°</span>
        </div>
        <div class="result-kv-item">
          <span class="result-kv-label">RSSI</span>
          <span class="result-kv-value">−82 dBm</span>
        </div>
      </div>
    </div>
  </div>

  <!-- AIS collapsed -->
  <div class="tracking-item" data-type="ais">
    <div class="tracking-item-header">
      <i class="fa-solid fa-ship tracking-item-icon"></i>
      <span class="tracking-item-name">NORDIC ODEN</span>
      <span class="badge badge-gray">AIS</span>
      <i class="fa-solid fa-chevron-down tracking-item-chevron"></i>
    </div>
  </div>

</div>
```

**AIS-Felder in `.tracking-item-body`:** MMSI, SOG (kt), COG (°), RSSI (dBm)

**HTML — Leerzustand:**

```html
<div class="result-empty">
  <i class="fa-solid fa-satellite-dish"></i>
  Warte auf Empfang…
</div>
```

**Regeln:**
- `data-type="adsb"` / `data-type="ais"` für JS-Filterung via Mode-Switch
- Badge-Farbe: `.badge-blue` für ADS-B, `.badge-gray` für AIS
- `.result-kv` aus Typ 4 wird unverändert wiederverwendet
- `.result-empty` aus Typ 5 wird wiederverwendet
- `.segmented` / `.segmented-btn` aus `forms.css` wird wiederverwendet
- Immer genau ein Item kann `.active` sein (oder keines)
- JS-Zuständigkeit: Klick auf `.tracking-item-header` → `.active` toggeln + Karte highlighten; Kartenklick → Item per `data-type`/`data-id` finden, `.active` setzen, `scrollIntoView()`; Mode-Switch → Items per `data-type` filtern
```

- [ ] **Schritt 3: Änderungshistorie aktualisieren**

In der Änderungshistorie-Tabelle am Ende der Datei eine neue Zeile ergänzen:

```markdown
| 2026-05-12 | Typ 8: Objekt-Detail → Tracking-Liste; Mode-Switch, Expand-Verhalten, `data-type`-Filter |
```

- [ ] **Schritt 4: Commit**

```bash
git add docs/sidebar-types.md
git commit -m "docs: rewrite Typ 8 as tracking-list with mode-switch and expand"
```

---

## Task 4: CHANGELOG aktualisieren

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Schritt 1: Datei lesen**

`CHANGELOG.md` lesen um das Format des letzten Eintrags `[2.2.0]` zu sehen.

- [ ] **Schritt 2: Unreleased-Abschnitt einfügen**

Direkt nach der Einleitung (nach dem `docs/versioning.md`-Block, vor `## [2.2.0]`) einfügen:

```markdown
## [Unreleased]

### Added
- Sidebar Typ 8 — Tracking-Liste: scrollbare Liste aller empfangenen ADSB/AIS-Objekte mit Mode-Switch (Alle / ADS-B / AIS) und Expand-Verhalten. Klassen: `.tracking-list`, `.tracking-item`, `.tracking-item-header`, `.tracking-item-body`, `.tracking-item-icon`, `.tracking-item-name`, `.tracking-item-chevron`.

### Changed
- `docs/sidebar-types.md`: Typ 8 vollständig neu definiert (Tracking-Liste ersetzt Objekt-Detail).

### Removed
- `.object-detail`, `.object-detail-header`, `.object-detail-icon`, `.object-detail-name` aus `css/sidebar.css` entfernt (ersetzt durch `.tracking-*`).

> **Hinweis Versioning:** Da `.object-detail*`-Klassen entfernt werden, ist das technisch ein MAJOR-Change (v3.0.0). Da diese Klassen erst mit v2.2.0 eingeführt wurden und noch keine Produktionsseite sie nutzt, kann auch v2.3.0 gewählt werden — Entscheidung liegt beim Maintainer.
```

- [ ] **Schritt 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for Typ 8 tracking-list redesign"
```

---

## Self-Review

**Spec-Abdeckung:**
- ✅ `.object-detail*` entfernen → Task 1
- ✅ `.tracking-list`, `.tracking-item*` CSS → Task 1
- ✅ Mode-Switch (`.segmented`) → Task 2 (Demo) + Task 3 (Docs)
- ✅ Item collapsed/expanded HTML → Task 2 + Task 3
- ✅ `.tracking-item.active` mit accent border-left + chevron-rotation + body-visible → Task 1
- ✅ ADS-B-Felder (Höhe, Speed, Kurs, RSSI) → Task 2 + Task 3
- ✅ AIS-Felder (MMSI, SOG, COG, RSSI) → Task 3
- ✅ `data-type` Attribut → Task 2 + Task 3
- ✅ Leerzustand `.result-empty` → Task 2 + Task 3
- ✅ JS-Zuständigkeiten dokumentiert → Task 3
- ✅ CHANGELOG → Task 4

**Placeholder-Scan:** Keine TBDs, kein "implement later", kein "similar to Task N".

**Typ-Konsistenz:** Klassennamen identisch in CSS (Task 1), HTML-Demo (Task 2) und Docs (Task 3):
`.tracking-list`, `.tracking-item`, `.tracking-item-header`, `.tracking-item-body`, `.tracking-item-icon`, `.tracking-item-name`, `.tracking-item-chevron` — durchgängig korrekt.

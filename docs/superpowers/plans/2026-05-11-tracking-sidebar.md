# Tracking Sidebar (ADSB/AIS) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sidebar-Definition für map.oe5ith.at/tracking: Live-Stats-Panel (Typ 6) + Objekt-Detail-Panel (Typ 8, neu) für ADSB-Flugzeuge und AIS-Schiffe.

**Architecture:** Zwei gestapelte Panels in `.sidebar-inner` getrennt durch `.tool-sep`. Stats-Panel (Typ 6, read-only Zähler) oben, Objekt-Detail-Panel (Typ 8, neu) unten. Klick auf Kartenobjekt füllt das Detail-Panel per JS. CSS-Klassen `result-kv`, `status-panel/row/dot` werden aus dem Inline-Style von `components/sidebar-types.html` nach `css/sidebar.css` extrahiert, da sie für Produktionsseiten im gemeinsamen CSS verfügbar sein müssen.

**Tech Stack:** CSS (Token-basiert, `css/common.css`), HTML, kein Build-Schritt.

**Spec:** `docs/superpowers/specs/2026-05-11-tracking-sidebar-design.md`

---

## Datei-Map

| Datei | Aktion | Inhalt |
|---|---|---|
| `css/sidebar.css` | Modify | `result-kv`, `status-panel/row/dot`, `object-detail*` hinzufügen |
| `components/sidebar-types.html` | Modify | Redundante Inline-CSS entfernen; Typ 8 Demo-Sektion hinzufügen |
| `docs/sidebar-types.md` | Modify | Typ 8 Eintrag + Änderungshistorie |
| `CHANGELOG.md` | Modify | Neuen Abschnitt für v2.2.0 dokumentieren |

---

## Task 1: `result-kv` aus Inline-Style nach `css/sidebar.css` extrahieren

**Files:**
- Modify: `css/sidebar.css`
- Modify: `components/sidebar-types.html` (Inline-CSS entfernen)

Diese Klassen existieren nur als Inline-Style in `components/sidebar-types.html` (Zeilen 389–392), nicht in `css/sidebar.css`. Produktionsseiten brauchen sie in der gemeinsamen CSS-Datei.

- [ ] **Schritt 1: Klassen in sidebar.css einfügen**

Datei lesen: `css/sidebar.css`

Nach dem Block `/* Typ 5: Leerzustand */` (nach `.result-empty > i { ... }`, vor dem `/* ═══ MOBILE ═══ */`-Kommentar) einfügen:

```css
/* ═══ TYP 4/6/8 — KEY-VALUE ZEILEN ═══ */
.result-kv { display: flex; gap: 12px; padding-left: 25px; margin-bottom: 5px; }
.result-kv-item { display: flex; flex-direction: column; gap: 1px; }
.result-kv-label { font-size: 0.58rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; color: var(--subtle); }
.result-kv-value { font-size: 0.78rem; font-weight: 600; color: var(--text); }
```

- [ ] **Schritt 2: Inline-CSS in sidebar-types.html entfernen**

Datei lesen: `components/sidebar-types.html`

Die vier Zeilen 389–392 in der `<style>`-Block entfernen:
```css
.result-kv { display:flex; gap:12px; padding-left:25px; margin-bottom:5px; }
.result-kv-item { display:flex; flex-direction:column; gap:1px; }
.result-kv-label { font-size:0.58rem; font-weight:700; letter-spacing:0.5px; text-transform:uppercase; color:var(--subtle); }
.result-kv-value { font-size:0.78rem; font-weight:600; color:var(--text); }
```

Sicherstellen dass `components/sidebar-types.html` `css/sidebar.css` per `<link>` einbindet — dann funktionieren die Klassen weiterhin aus der externen CSS-Datei.

- [ ] **Schritt 3: Visuell prüfen**

`components/sidebar-types.html` im Browser öffnen. Typ 4 (Routing SEW/NEF) muss unverändert aussehen — Key-Value-Zeilen „Dauer" und „Distanz" sichtbar und korrekt formatiert.

- [ ] **Schritt 4: Commit**

```bash
git add css/sidebar.css components/sidebar-types.html
git commit -m "refactor: extract result-kv styles from inline to sidebar.css"
```

---

## Task 2: `status-panel`, `status-row`, `status-dot` nach `css/sidebar.css` extrahieren

**Files:**
- Modify: `css/sidebar.css`
- Modify: `components/sidebar-types.html` (Inline-CSS entfernen)

Diese Klassen existieren nur als Inline-Style in `components/sidebar-types.html` (Zeilen 443–457), nicht in `css/sidebar.css`.

- [ ] **Schritt 1: Klassen in sidebar.css einfügen**

Nach dem neuen `result-kv`-Block aus Task 1, also vor `/* ═══ MOBILE ═══ */`, einfügen:

```css
/* ═══ TYP 6 — STATUS-PANEL ═══ */
.status-panel { display: flex; flex-direction: column; gap: 6px; }
.status-row {
  display: flex; align-items: center; justify-content: space-between;
  gap: 8px; padding: 6px 8px; border-radius: 4px;
  background: var(--panel-deep); border: 1px solid var(--border);
}
.status-row-left { display: flex; align-items: center; gap: 8px; min-width: 0; }
.status-row-icon { font-size: 0.72rem; color: var(--muted); width: 14px; text-align: center; flex-shrink: 0; }
.status-row-name { font-size: 0.78rem; color: var(--text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.status-row-right { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.status-row-value { font-size: 0.72rem; color: var(--muted); font-family: var(--font-mono); }
.status-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.status-dot.on   { background: var(--success); box-shadow: 0 0 4px var(--success); }
.status-dot.off  { background: var(--danger);  box-shadow: 0 0 4px rgba(239,68,68,0.5); }
.status-dot.warn { background: var(--warning); box-shadow: 0 0 4px rgba(234,179,8,0.5); }
```

- [ ] **Schritt 2: Inline-CSS in sidebar-types.html entfernen**

Die Zeilen 443–457 in der `<style>`-Block entfernen:
```css
.status-panel { display:flex; flex-direction:column; gap:6px; }
.status-row { ... }
.status-row-left { ... }
.status-row-icon { ... }
.status-row-name { ... }
.status-row-right { ... }
.status-row-value { ... }
.status-dot { ... }
.status-dot.on { ... }
.status-dot.off { ... }
.status-dot.warn { ... }
```

- [ ] **Schritt 3: Visuell prüfen**

`components/sidebar-types.html` im Browser öffnen. Typ 6 (ADS-B/AIS Live-Stats Demo) muss unverändert aussehen — status-rows mit Dots korrekt dargestellt.

- [ ] **Schritt 4: Commit**

```bash
git add css/sidebar.css components/sidebar-types.html
git commit -m "refactor: extract status-panel/row/dot styles from inline to sidebar.css"
```

---

## Task 3: Typ 8 CSS (`object-detail*`) in `css/sidebar.css` ergänzen

**Files:**
- Modify: `css/sidebar.css`

Neue Klassen für das Objekt-Detail-Panel (Typ 8). `.result-kv` und `.result-empty` werden wiederverwendet (bereits aus Task 1 bzw. vorhanden in sidebar.css).

- [ ] **Schritt 1: CSS einfügen**

Nach dem neuen `status-panel/row/dot`-Block (Task 2), vor `/* ═══ MOBILE ═══ */`, einfügen:

```css
/* ═══ TYP 8 — OBJEKT-DETAIL ═══ */
.object-detail { display: flex; flex-direction: column; gap: 8px; padding: 4px 0; }

.object-detail-header {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 8px; border-radius: 4px;
  background: var(--panel-deep); border: 1px solid var(--border);
}
.object-detail-icon {
  font-size: 0.72rem; color: var(--muted);
  width: 14px; text-align: center; flex-shrink: 0;
}
.object-detail-name {
  font-size: 0.82rem; font-weight: 600; color: var(--text);
  flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
```

- [ ] **Schritt 2: Visuell prüfen (Browser)**

`components/sidebar-types.html` im Browser öffnen. Die neuen Klassen sind noch nicht im HTML — kein visuelles Ergebnis zu erwarten. Sicherstellen dass keine CSS-Fehler in der Dev-Console erscheinen.

- [ ] **Schritt 3: Commit**

```bash
git add css/sidebar.css
git commit -m "feat: add object-detail CSS for sidebar Typ 8"
```

---

## Task 4: Typ 8 Demo in `components/sidebar-types.html` hinzufügen

**Files:**
- Modify: `components/sidebar-types.html`

Neue Sektion mit drei Zuständen: Leerzustand, ADSB-Objekt, AIS-Objekt. Badges: `.badge.badge-blue` für ADSB, `.badge.badge-gray` für AIS (bestehende Klassen aus `badges.css`).

- [ ] **Schritt 1: Datei lesen und Einfügestelle finden**

`components/sidebar-types.html` lesen. Letzte Typ-Sektion (Typ 7) finden — neue Sektion danach einfügen, vor dem schließenden `</main>` oder `</body>`.

- [ ] **Schritt 2: Typ 8 Demo-Sektion einfügen**

Nach der letzten Typ-Demo-Sektion einfügen:

```html
<!-- ═══ TYP 8 — OBJEKT-DETAIL ═══ -->
<section class="demo-section" id="typ8">
  <h2 class="demo-title">Typ 8 — Objekt-Detail</h2>
  <p class="demo-desc">Klick auf Kartenobjekt → Detail-Panel füllt sich. Kombiniert mit Typ 6 über <code>tool-sep</code>. Drei Zustände: leer, ADSB, AIS.</p>

  <div class="demo-row">

    <!-- Leerzustand -->
    <div class="demo-col">
      <div class="demo-label">Leerzustand</div>
      <div class="sidebar-preview">
        <div class="sidebar-inner">
          <div class="result-empty">
            <i class="fa-solid fa-satellite-dish"></i>
            Klicke auf ein Flugzeug oder Schiff auf der Karte für Details.
          </div>
        </div>
      </div>
    </div>

    <!-- ADSB-Objekt -->
    <div class="demo-col">
      <div class="demo-label">Gefüllt — ADS-B</div>
      <div class="sidebar-preview">
        <div class="sidebar-inner">
          <div class="object-detail">
            <div class="object-detail-header">
              <i class="fa-solid fa-plane object-detail-icon"></i>
              <span class="object-detail-name">AUA123</span>
              <span class="badge badge-blue">ADS-B</span>
            </div>
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
      </div>
    </div>

    <!-- AIS-Objekt -->
    <div class="demo-col">
      <div class="demo-label">Gefüllt — AIS</div>
      <div class="sidebar-preview">
        <div class="sidebar-inner">
          <div class="object-detail">
            <div class="object-detail-header">
              <i class="fa-solid fa-ship object-detail-icon"></i>
              <span class="object-detail-name">NORDIC ODEN</span>
              <span class="badge badge-gray">AIS</span>
            </div>
            <div class="result-kv">
              <div class="result-kv-item">
                <span class="result-kv-label">MMSI</span>
                <span class="result-kv-value">230084000</span>
              </div>
              <div class="result-kv-item">
                <span class="result-kv-label">SOG</span>
                <span class="result-kv-value">12,4 kt</span>
              </div>
              <div class="result-kv-item">
                <span class="result-kv-label">COG</span>
                <span class="result-kv-value">184°</span>
              </div>
              <div class="result-kv-item">
                <span class="result-kv-label">RSSI</span>
                <span class="result-kv-value">−91 dBm</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div><!-- /.demo-row -->

  <!-- Kombiniertes Beispiel: Typ 6 + Typ 8 -->
  <div class="demo-row">
    <div class="demo-col demo-col-wide">
      <div class="demo-label">Kombination Typ 6 + Typ 8 (Tracking-Sidebar)</div>
      <div class="sidebar-preview sidebar-preview-tall">
        <div class="sidebar-inner">

          <!-- Stats-Panel (Typ 6) -->
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

          <!-- Detail-Panel (Typ 8) — ADSB Objekt gewählt -->
          <div class="object-detail">
            <div class="object-detail-header">
              <i class="fa-solid fa-plane object-detail-icon"></i>
              <span class="object-detail-name">AUA123</span>
              <span class="badge badge-blue">ADS-B</span>
            </div>
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

        </div><!-- /.sidebar-inner -->
      </div><!-- /.sidebar-preview -->
    </div>
  </div><!-- /.demo-row -->

</section>
```

- [ ] **Schritt 3: Visuell prüfen**

`components/sidebar-types.html` im Browser öffnen. Drei neue Demo-Spalten für Typ 8 müssen sichtbar sein (Leer / ADSB / AIS). Kombiniertes Beispiel mit Typ 6 + Typ 8 muss korrekt dargestellt sein. Alle anderen Typen (1–7) müssen unverändert aussehen.

- [ ] **Schritt 4: Commit**

```bash
git add components/sidebar-types.html
git commit -m "feat: add Typ 8 object-detail demo to sidebar-types reference"
```

---

## Task 5: Typ 8 in `docs/sidebar-types.md` dokumentieren

**Files:**
- Modify: `docs/sidebar-types.md`

- [ ] **Schritt 1: Übersichtstabelle ergänzen**

In der Übersichtstabelle eine neue Zeile hinzufügen:

```markdown
| 8 | Objekt-Detail | map.oe5ith.at/tracking |
```

- [ ] **Schritt 2: Entscheidungsbaum ergänzen**

Im Entscheidungsbaum nach dem AIS/Status-Zweig einfügen:

```
Zeigt die Sidebar Details zu einem angeklickten Kartenobjekt (Flugzeug, Schiff)?
│
└── JA → Typ 8: Objekt-Detail (kombiniert mit Typ 6)
```

- [ ] **Schritt 3: Typ 8 Abschnitt ergänzen**

Am Ende der Typ-Abschnitte (nach Typ 7, vor „Panels stapeln") einfügen:

```markdown
## Typ 8 — Objekt-Detail

**Beispiel:** map.oe5ith.at/tracking

**Wann verwenden:**
Tracking-/Monitoring-Karten wo Klick auf ein Objekt (Flugzeug, Schiff, Fahrzeug)
Details in der Sidebar zeigt. Immer in Kombination mit einem anderen Panel-Typ (z.B. Typ 6),
getrennt durch `tool-sep`.

**Zustände:**

| Zustand | Anzeige |
|---|---|
| Kein Objekt gewählt | `.result-empty` mit Icon + Hinweistext |
| Objekt gewählt | `.object-detail` mit Header + Key-Value-Zeilen |

**HTML — Leerzustand:**

```html
<div class="result-empty">
  <i class="fa-solid fa-satellite-dish"></i>
  Klicke auf ein Flugzeug oder Schiff auf der Karte für Details.
</div>
```

**HTML — Gefüllt (ADSB):**

```html
<div class="object-detail">
  <div class="object-detail-header">
    <i class="fa-solid fa-plane object-detail-icon"></i>
    <span class="object-detail-name">AUA123</span>
    <span class="badge badge-blue">ADS-B</span>
  </div>
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
```

**HTML — Gefüllt (AIS):**

```html
<div class="object-detail">
  <div class="object-detail-header">
    <i class="fa-solid fa-ship object-detail-icon"></i>
    <span class="object-detail-name">NORDIC ODEN</span>
    <span class="badge badge-gray">AIS</span>
  </div>
  <div class="result-kv">
    <div class="result-kv-item">
      <span class="result-kv-label">MMSI</span>
      <span class="result-kv-value">230084000</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">SOG</span>
      <span class="result-kv-value">12,4 kt</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">COG</span>
      <span class="result-kv-value">184°</span>
    </div>
    <div class="result-kv-item">
      <span class="result-kv-label">RSSI</span>
      <span class="result-kv-value">−91 dBm</span>
    </div>
  </div>
</div>
```

**Regeln:**
- Badge-Farbe unterscheidet den Objekttyp: `.badge-blue` für ADSB, `.badge-gray` für AIS
- `.result-kv` aus Typ 4 wird unverändert wiederverwendet
- Leerzustand: `.result-empty` aus Typ 5 wird wiederverwendet
- JS-Zuständigkeit: Beim Klick auf ein Kartenobjekt `.result-empty` verstecken und `.object-detail` befüllen/zeigen; bei Klick auf leere Karte wieder Leerzustand zeigen
```

- [ ] **Schritt 4: Panels-stapeln-Tabelle ergänzen**

In der Tabelle „Panels stapeln" eine neue Zeile hinzufügen:

```markdown
| Typ 6 + Typ 8 | Live-Stats + Objekt-Detail (Tracking-Seite) |
```

- [ ] **Schritt 5: Änderungshistorie aktualisieren**

```markdown
| 2026-05-11 | Typ 8: Objekt-Detail ergänzt; `result-kv`, `status-panel/row/dot` nach `sidebar.css` extrahiert |
```

- [ ] **Schritt 6: Commit**

```bash
git add docs/sidebar-types.md
git commit -m "docs: add Typ 8 object-detail to sidebar-types documentation"
```

---

## Task 6: `CHANGELOG.md` aktualisieren

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Schritt 1: Datei lesen**

`CHANGELOG.md` lesen um das aktuelle Format zu verstehen und den letzten Eintrag zu sehen.

- [ ] **Schritt 2: Neuen Abschnitt einfügen**

Ganz oben (nach dem Header, vor dem letzten Release-Eintrag) einfügen:

```markdown
## [Unreleased]

### Added
- Sidebar Typ 8 — Objekt-Detail: neues Panel für Tracking-/Monitoring-Seiten. Zeigt bei Klick auf ein Kartenobjekt Details (Callsign/Name, Höhe/Speed/Kurs, MMSI/SOG/COG, RSSI). Klassen: `.object-detail`, `.object-detail-header`, `.object-detail-icon`, `.object-detail-name`.
- `components/sidebar-types.html`: Typ 8 Demo-Sektion mit Leerzustand, ADSB-Objekt, AIS-Objekt und Kombinations-Beispiel.

### Changed
- `css/sidebar.css`: `result-kv`, `status-panel`, `status-row*`, `status-dot` aus Inline-Style von `components/sidebar-types.html` extrahiert — ab sofort für alle Produktionsseiten im gemeinsamen CSS verfügbar.
- `docs/sidebar-types.md`: Typ 8 dokumentiert, Entscheidungsbaum und Stapel-Tabelle ergänzt.
```

- [ ] **Schritt 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for Typ 8 object-detail and CSS extraction"
```

---

## Self-Review

**Spec-Abdeckung:**
- ✅ Stats-Panel (Typ 6): vier status-rows (ADSB-Zähler, AIS-Zähler, Receiver, Pakete/min) → Task 2 + Task 4
- ✅ Leerzustand Detail-Panel: `.result-empty` mit Icon → Task 4
- ✅ ADSB-Felder (Callsign, Höhe, Speed, Kurs, RSSI) → Task 4
- ✅ AIS-Felder (Name, MMSI, SOG, COG, RSSI) → Task 4
- ✅ Badge-Unterscheidung ADSB vs AIS → Task 4 (`.badge-blue` / `.badge-gray`)
- ✅ CSS für neue Klassen → Task 3
- ✅ Dokumentation Typ 8 → Task 5
- ✅ CSS-Extraktion result-kv → Task 1
- ✅ CSS-Extraktion status-row/dot → Task 2

**Hinweis Badge-Klassen:** Der Spec nennt `.badge-accent` und `.badge-surface`. Im CI existieren diese nicht — stattdessen werden die bestehenden Klassen `.badge-blue` (Accent-Blau) und `.badge-gray` (neutral) verwendet. Das entspricht der CLAUDE.md-Regel "reuse existing CI classes".

**Placeholder-Scan:** Keine TBDs, keine offenen Punkte.

**Typ-Konsistenz:** Alle Klassennamen konsistent: `.object-detail`, `.object-detail-header`, `.object-detail-icon`, `.object-detail-name` — identisch in Task 3 (CSS), Task 4 (HTML) und Task 5 (Docs).

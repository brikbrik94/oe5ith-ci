# Geocoder Dropdown Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Geocoder Dropdown component to the CI — dokumentiert in `docs/`, mit CSS in `css/forms.css` und Live-Demo in `components/forms.html`.

**Architecture:** Drei aufeinander aufbauende Änderungen: zuerst Dokumentation, dann CSS, dann Demo-HTML. Alle CSS-Klassen nutzen ausschließlich bestehende Tokens aus `common.css`. Kein JavaScript, kein Open/Close-State im CI — der Consumer steuert Sichtbarkeit.

**Tech Stack:** CSS (Tokens aus `common.css`), HTML, Font Awesome 6 (bereits in `components/forms.html` eingebunden)

---

## Dateiübersicht

| Datei | Aktion | Inhalt |
|---|---|---|
| `docs/geocoder-dropdown.md` | Neu erstellen | Strukturbeispiel, Icon-Tabelle, Regeln |
| `css/forms.css` | Erweitern | 6 neue Klassen im Geocoder-Block |
| `components/forms.html` | Erweitern | Geocoder-CSS im `<style>`-Block + neuer Demo-Abschnitt |

---

### Task 1: Dokumentationsdatei erstellen

**Files:**
- Create: `docs/geocoder-dropdown.md`

- [ ] **Schritt 1: Datei anlegen**

Datei `docs/geocoder-dropdown.md` mit diesem Inhalt erstellen:

```markdown
# Geocoder Dropdown

**Referenz-Datei:** `components/forms.html`  
**Status:** definiert · v1.1

---

## Überblick

Das Geocoder Dropdown zeigt Suchergebnisse einer Nominatim-Abfrage unterhalb eines Text-Inputs.
Absolut positioniertes Panel mit einer Liste von Treffern — Icon, Primärtitel, Untertitel.

---

## Voraussetzung

Der umgebende `.form-field`-Container muss `position: relative` tragen:

```html
<div class="form-field" style="position: relative;">
```

---

## HTML-Struktur

```html
<div class="form-field" style="position: relative;">
  <label class="form-label" for="geocoder-input">Ort suchen</label>
  <div class="form-input-wrap">
    <i class="fa-solid fa-search form-input-icon"></i>
    <input class="form-input" id="geocoder-input" type="text" placeholder="Ort oder Adresse...">
  </div>

  <div class="geocoder-results">

    <div class="geocoder-item">
      <div class="geocoder-icon">
        <i class="fa-solid fa-city"></i>
      </div>
      <div class="geocoder-content">
        <div class="geocoder-title">Linz</div>
        <div class="geocoder-subtitle">Oberösterreich, Österreich</div>
      </div>
    </div>

  </div>
</div>
```

---

## Icon-Referenz

| Typ | Icon-Klasse |
|---|---|
| Stadt / Ort | `fa-city` oder `fa-location-dot` |
| Adresse | `fa-map-pin` |
| Berg / Gipfel | `fa-mountain` |
| Krankenhaus | `fa-hospital` |
| Gewässer | `fa-droplet` |
| POI / Allgemein | `fa-star` |

---

## Regeln

1. **Positionierung:** `.form-field` muss `position: relative` haben.
2. **Begrenzung:** `max-height: 280px` + `overflow-y: auto` — scrollt bei vielen Treffern.
3. **Hover:** Einträge reagieren mit `var(--surface-hover)` auf `:hover`.
4. **Z-Index:** `var(--z-dropdown)` — liegt über Karten-Elementen und Panels.
5. **Show/Hide:** Kein Open/Close-CSS im CI — der Consumer steuert Sichtbarkeit.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-05-11 | Initiale Definition. |
```

- [ ] **Schritt 2: Prüfen**

```bash
cat docs/geocoder-dropdown.md
```

Erwartung: Datei vollständig, keine leeren Abschnitte.

- [ ] **Schritt 3: Commit**

```bash
git add docs/geocoder-dropdown.md
git commit -m "docs: add geocoder-dropdown component documentation"
```

---

### Task 2: CSS zu `css/forms.css` hinzufügen

**Files:**
- Modify: `css/forms.css`

Der neue Geocoder-Block kommt direkt vor dem bestehenden `/* Einzelne Demos */`-Kommentar am Ende der Datei (aktuell Zeile ~251). Den Block dort einfügen.

- [ ] **Schritt 1: Geocoder-CSS-Block einfügen**

In `css/forms.css` den folgenden Block **vor** dem Kommentar `/* Einzelne Demos */` einfügen:

```css
/* ═══════════════════════════════════════
   GEOCODER DROPDOWN
   Für Suchergebnisse (Nominatim)
   ═══════════════════════════════════════ */
.geocoder-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--panel-deep);
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 5px 5px;
  box-shadow: var(--shadow-dropdown);
  z-index: var(--z-dropdown);
  max-height: 280px;
  overflow-y: auto;
}

.geocoder-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 12px;
  cursor: pointer;
  transition: background var(--transition-fast);
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.geocoder-item:last-child { border-bottom: none; }
.geocoder-item:hover { background: var(--surface-hover); }

.geocoder-icon {
  width: 16px;
  color: var(--accent);
  font-size: 0.9rem;
  text-align: center;
  margin-top: 2px;
  flex-shrink: 0;
}

.geocoder-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.geocoder-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.geocoder-subtitle {
  font-size: 0.72rem;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

- [ ] **Schritt 2: Keine hardcodierten Werte prüfen**

```bash
grep -n '#[0-9a-fA-F]\{3,6\}\b\|rgb(' css/forms.css | grep -v 'rgba(59,130,246\|rgba(239,68,68\|rgba(255,255,255,0.03\|rgba(255,255,255,0.04\|rgba(34,197,94\|rgba(239,68,68\|#555\|data:image'
```

Erwartung: Keine neuen hardcodierten Farbwerte in den Geocoder-Klassen.

- [ ] **Schritt 3: Commit**

```bash
git add css/forms.css
git commit -m "feat: add geocoder-dropdown CSS to forms.css"
```

---

### Task 3: Demo zu `components/forms.html` hinzufügen

**Files:**
- Modify: `components/forms.html`

Zwei Änderungen an `components/forms.html`:
1. Geocoder-CSS in den inline `<style>`-Block (vor dem `/* ═══ DEMO / REFERENZ STYLES ═══ */`-Kommentar)
2. Neuer Demo-Abschnitt im Body (vor dem `<div class="event-log"` Element)

- [ ] **Schritt 1: Geocoder-CSS in den `<style>`-Block einfügen**

In `components/forms.html` den folgenden Block **vor** den Kommentar `/* ═══ DEMO / REFERENZ STYLES ═══ */` einfügen (aktuell ab Zeile ~287):

```css
/* ═══════════════════════════════════════
   GEOCODER DROPDOWN
   Für Suchergebnisse (Nominatim)
   ═══════════════════════════════════════ */
.geocoder-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--panel-deep);
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 5px 5px;
  box-shadow: var(--shadow-dropdown);
  z-index: var(--z-dropdown);
  max-height: 280px;
  overflow-y: auto;
}

.geocoder-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 12px;
  cursor: pointer;
  transition: background var(--transition-fast);
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.geocoder-item:last-child { border-bottom: none; }
.geocoder-item:hover { background: var(--surface-hover); }

.geocoder-icon {
  width: 16px;
  color: var(--accent);
  font-size: 0.9rem;
  text-align: center;
  margin-top: 2px;
  flex-shrink: 0;
}

.geocoder-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.geocoder-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.geocoder-subtitle {
  font-size: 0.72rem;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

- [ ] **Schritt 2: Demo-Abschnitt in den Body einfügen**

In `components/forms.html` den folgenden Block **direkt vor** `<div class="event-log"` einfügen:

```html
  <!-- ═══ GEOCODER DROPDOWN ═══ -->
  <div class="demo-section">
    <div class="demo-section-title">Geocoder Dropdown — Suchergebnisse</div>
    <div class="demo-section-desc">
      Erscheint unterhalb eines <code>.form-input-wrap</code> bei aktiver Suche.
      Der übergeordnete <code>.form-field</code> muss <code>position: relative</code> haben.
      Show/Hide-Logik liegt beim Consumer.
    </div>

    <div class="demo-cols">

      <!-- Sidebar-Kontext mit sichtbarem Dropdown -->
      <div class="sidebar-ctx" style="position: relative; overflow: visible;">

        <div class="form-field" style="position: relative;">
          <label class="form-label" for="geocoder-demo">Ort suchen</label>
          <div class="form-input-wrap">
            <i class="fa-solid fa-search form-input-icon"></i>
            <input class="form-input" id="geocoder-demo" type="text" value="Linz">
          </div>

          <div class="geocoder-results">

            <div class="geocoder-item">
              <div class="geocoder-icon"><i class="fa-solid fa-city"></i></div>
              <div class="geocoder-content">
                <div class="geocoder-title">Linz</div>
                <div class="geocoder-subtitle">Oberösterreich, Österreich</div>
              </div>
            </div>

            <div class="geocoder-item">
              <div class="geocoder-icon"><i class="fa-solid fa-mountain"></i></div>
              <div class="geocoder-content">
                <div class="geocoder-title">Pöstlingberg</div>
                <div class="geocoder-subtitle">Berg in Linz</div>
              </div>
            </div>

            <div class="geocoder-item">
              <div class="geocoder-icon"><i class="fa-solid fa-map-pin"></i></div>
              <div class="geocoder-content">
                <div class="geocoder-title">Linzer Straße 42, Linz</div>
                <div class="geocoder-subtitle">Oberösterreich, Österreich</div>
              </div>
            </div>

          </div>
        </div>

      </div><!-- /sidebar-ctx -->

      <!-- Beschreibung -->
      <div style="font-size:.82rem;color:var(--muted);line-height:1.7">
        <p>Klassen:</p>
        <ul style="margin-top:6px;padding-left:16px;line-height:2">
          <li><code>.geocoder-results</code> — Container-Panel</li>
          <li><code>.geocoder-item</code> — Einzelner Treffer</li>
          <li><code>.geocoder-icon</code> — Icon-Spalte</li>
          <li><code>.geocoder-content</code> — Text-Spalte</li>
          <li><code>.geocoder-title</code> — Primärtext</li>
          <li><code>.geocoder-subtitle</code> — Sekundärtext</li>
        </ul>
      </div>

    </div>
  </div>
```

- [ ] **Schritt 3: Visuell prüfen**

`components/forms.html` im Browser öffnen (oder mit einem lokalen HTTP-Server). Prüfen:
- Dropdown erscheint direkt unterhalb des Inputs
- Drei Einträge sichtbar (Stadt, Berg, Adresse)
- Icons in Akzentfarbe
- Hover auf einem Eintrag zeigt den Surface-Hover-Hintergrund
- Kein Abschneiden durch `overflow: hidden` des Containers

- [ ] **Schritt 4: Commit**

```bash
git add components/forms.html
git commit -m "feat: add geocoder-dropdown demo to forms reference"
```

---

### Task 4: CHANGELOG aktualisieren und Version taggen

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Schritt 1: CHANGELOG-Eintrag hinzufügen**

In `CHANGELOG.md` einen neuen Abschnitt **ganz oben** (vor dem letzten Release-Eintrag) einfügen:

```markdown
## [1.1.1] - 2026-05-11

### Added
- Geocoder Dropdown: `.geocoder-results`, `.geocoder-item`, `.geocoder-icon`, `.geocoder-content`, `.geocoder-title`, `.geocoder-subtitle` in `css/forms.css`
- `docs/geocoder-dropdown.md`: Dokumentation mit HTML-Struktur, Icon-Referenz und Regeln
- Demo-Abschnitt in `components/forms.html`
```

- [ ] **Schritt 2: CHANGELOG prüfen**

```bash
head -20 CHANGELOG.md
```

Erwartung: Neuer `[1.1.1]`-Abschnitt ganz oben.

- [ ] **Schritt 3: Commit und Tag**

```bash
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for geocoder dropdown v1.1.1"
git tag -a v1.1.1 -m "Release v1.1.1 — Geocoder Dropdown"
```

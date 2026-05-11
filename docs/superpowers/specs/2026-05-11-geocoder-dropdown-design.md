# Design: Geocoder Dropdown

**Datum:** 2026-05-11  
**Status:** approved

---

## Ziel

Das Geocoder Dropdown ist ein Suchergebnis-Overlay für Nominatim-basierte Ortssuche. Es erscheint unterhalb eines `.form-input-wrap` und zeigt eine Liste von Treffern mit Icon, Titel und Untertitel.

---

## Scope

| Datei | Änderung |
|---|---|
| `docs/geocoder-dropdown.md` | Neue Dokumentationsdatei |
| `css/forms.css` | 6 neue Klassen am Ende des Geocoder-Blocks |
| `components/forms.html` | Neuer Demo-Abschnitt (statisches Dropdown, 2–3 Einträge) |

---

## HTML-Struktur

`.geocoder-results` ist ein Geschwister-Element von `.form-input-wrap`, beide innerhalb von `.form-field`. Das `.form-field` muss `position: relative` tragen (inline oder via eigener Klasse im Consumer).

```html
<div class="form-field" style="position: relative;">
  <label class="form-label">Ort suchen</label>
  <div class="form-input-wrap">
    <i class="fa-solid fa-search form-input-icon"></i>
    <input class="form-input" type="text" placeholder="Ort oder Adresse...">
  </div>

  <div class="geocoder-results">
    <div class="geocoder-item">
      <div class="geocoder-icon"><i class="fa-solid fa-city"></i></div>
      <div class="geocoder-content">
        <div class="geocoder-title">Linz</div>
        <div class="geocoder-subtitle">Oberösterreich, Österreich</div>
      </div>
    </div>
  </div>
</div>
```

---

## CSS

6 neue Klassen in `css/forms.css`, alle ausschließlich mit bestehenden Tokens:

| Klasse | Zweck |
|---|---|
| `.geocoder-results` | Absolut positioniertes Container-Panel |
| `.geocoder-item` | Einzelner Treffer (Flex-Zeile) |
| `.geocoder-icon` | Icon-Spalte (16px, `--accent`) |
| `.geocoder-content` | Text-Spalte (Flex-Column) |
| `.geocoder-title` | Primärtext (0.82rem, `--text`) |
| `.geocoder-subtitle` | Sekundärtext (0.72rem, `--muted`) |

**Token-Nutzung:** `--panel-deep`, `--border`, `--shadow-dropdown`, `--z-dropdown`, `--surface-hover`, `--accent`, `--text`, `--muted`, `--transition-fast`.

**Raw-RGBA:** `border-bottom: 1px solid rgba(255,255,255,0.03)` für den Trennstrich zwischen Einträgen — konsistent mit identischem Muster in bestehenden Komponenten.

**Kein Open-State:** Kein `.is-open`-Toggle, keine Radius-Änderung am Input beim Öffnen. Das Dropdown ist immer sichtbar wenn im DOM vorhanden — Show/Hide-Logik liegt beim Consumer.

---

## Dokumentation

Neue Datei `docs/geocoder-dropdown.md` mit:
- HTML-Strukturbeispiel
- Icon-Referenztabelle (Stadt, Adresse, Berg, Krankenhaus, Gewässer, POI)
- Regeln (position:relative, max-height, z-index, hover)

---

## Regeln

1. `.form-field` muss `position: relative` haben
2. Dropdown hat `max-height: 280px` + `overflow-y: auto`
3. Hover: `var(--surface-hover)`
4. Z-Index: `var(--z-dropdown)`
5. Kein Show/Hide-CSS — Consumer-Verantwortung

---

## Nicht im Scope

- Open/Close-Animation
- Keyboard-Navigation der Einträge (Consumer-Verantwortung)
- Loading/Empty-States

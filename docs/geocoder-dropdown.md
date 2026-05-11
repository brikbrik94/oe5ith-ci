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

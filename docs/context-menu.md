# Context-Menu & Action-Menu

**Referenz-Datei:** `components/context-menu.html`  
**CSS:** `css/modal.css` (am Ende)  
**Status:** definiert · v1.0

---

## Überblick

Zwei verwandte Menü-Komponenten — beide verwenden dieselbe `.ctx-menu` Struktur,
unterscheiden sich nur im Auslöser und der Positionierung.

| | Context-Menu | Action-Menu |
|---|---|---|
| **Auslöser** | Rechtsklick (`contextmenu` Event) | Klick auf `⋮` Button |
| **Position** | `fixed` an Mauskoordinaten | `absolute` relativ zum `⋮` Button |
| **Kontext** | Karte, beliebige Bereiche | Tabellen-Zeilen, Ergebnis-Items, Cards |
| **Flip** | Automatisch wenn Viewport-Rand erreicht | Öffnet nach links (`right: 0`) |

---

## HTML-Struktur

```html
<div class="ctx-menu" id="mein-menu" role="menu">

  <!-- Optionales Label (Koordinaten, Zeilen-ID etc.) -->
  <div class="ctx-label">48.3064, 14.2858</div>
  <div class="ctx-sep"></div>

  <!-- Standard-Item -->
  <div class="ctx-item" onclick="aktion()" role="menuitem">
    <i class="fa-solid fa-location-dot"></i> Route von hier
  </div>

  <!-- Item mit Wert rechts -->
  <div class="ctx-item" onclick="aktion()" role="menuitem">
    <i class="fa-regular fa-copy"></i> Koordinaten kopieren
    <span class="ctx-item-value">48.31, 14.29</span>
  </div>

  <!-- Trenner -->
  <div class="ctx-sep"></div>

  <!-- Disabled -->
  <div class="ctx-item disabled" role="menuitem" aria-disabled="true">
    <i class="fa-solid fa-draw-polygon"></i> Bereich messen
  </div>

  <!-- Danger -->
  <div class="ctx-item danger" onclick="aktion()" role="menuitem">
    <i class="fa-solid fa-trash"></i> Marker löschen
  </div>

</div>
```

### Item-Typen

| Klasse | Verwendung |
|---|---|
| `.ctx-item` | Standard-Aktion |
| `.ctx-item.danger` | Destruktive Aktion (Löschen) |
| `.ctx-item.disabled` | Nicht verfügbar |
| `.ctx-label` | Kontextinfo, nicht klickbar |
| `.ctx-sep` | Trenner zwischen Gruppen |
| `.ctx-item-value` | Wert rechts im Item (z.B. Koordinaten) |

---

## Context-Menu (Rechtsklick)

### HTML — Karte (Leaflet)

```js
// Leaflet Event
map.on('contextmenu', function(e) {
  const lat = e.latlng.lat.toFixed(4);
  const lng = e.latlng.lng.toFixed(4);

  // Label mit Koordinaten füllen
  document.getElementById('ctx-coords').textContent = `${lat}, ${lng}`;

  // Menü an Mausposition öffnen
  openCtxMenu(document.getElementById('map-ctx-menu'), e.originalEvent.clientX, e.originalEvent.clientY);
});
```

### HTML — MapLibre

```js
map.on('contextmenu', function(e) {
  const coords = e.lngLat;
  const lat = coords.lat.toFixed(4);
  const lng = coords.lng.toFixed(4);

  openCtxMenu(document.getElementById('map-ctx-menu'), e.point.x, e.point.y);
});
```

### Positionierung mit automatischem Viewport-Flip

```js
function openCtxMenu(menu, x, y) {
  closeAllMenus();

  menu.style.left = x + 'px';
  menu.style.top  = y + 'px';
  menu.classList.remove('flip-x', 'flip-y');

  // Rendern lassen, dann Größe messen
  menu.style.visibility = 'hidden';
  menu.classList.add('open');

  const rect = menu.getBoundingClientRect();

  // Zu nah am rechten Rand → nach links öffnen
  if (rect.right  > window.innerWidth  - 8) {
    menu.style.left = (x - rect.width)  + 'px';
    menu.classList.add('flip-x');
  }
  // Zu nah am unteren Rand → nach oben öffnen
  if (rect.bottom > window.innerHeight - 8) {
    menu.style.top  = (y - rect.height) + 'px';
    menu.classList.add('flip-y');
  }

  menu.style.visibility = '';
}
```

---

## Action-Menu (⋮ Button)

### HTML — Tabellen-Zeile

```html
<tr>
  <td>24.4.2026 13:46</td>
  <td>1056019</td>
  <td>BH Jurist benötigt…</td>
  <td class="actions">
    <!-- Wrapper ist der Anker für position: absolute -->
    <div class="action-menu-wrap">
      <button class="action-menu-btn"
              onclick="openRowMenu(event, '1056019')"
              title="Aktionen"
              aria-haspopup="true">
        <i class="fa-solid fa-ellipsis-vertical"></i>
      </button>
      <!-- Menü wird per JS in diesen Wrapper verschoben -->
    </div>
  </td>
</tr>
```

### JavaScript

```js
let activeMenu  = null;
let activeRowId = null;

function openRowMenu(e, rowId) {
  e.stopPropagation(); // verhindert sofortiges Schließen durch document-click

  const menu = document.getElementById('row-action-menu');

  // Toggle: zweiter Klick auf denselben Button schließt
  if (activeMenu === menu && activeRowId === rowId) {
    closeAllMenus(); return;
  }

  closeAllMenus();
  activeRowId = rowId;

  // Menü in den .action-menu-wrap des geklickten Buttons verschieben
  const wrap = e.currentTarget.closest('.action-menu-wrap');
  wrap.appendChild(menu);
  menu.classList.add('open');
  activeMenu = menu;
}
```

---

## Globales Schließen (Pflicht)

```js
function closeAllMenus() {
  document.querySelectorAll('.ctx-menu.open').forEach(m => m.classList.remove('open'));
  activeMenu  = null;
  activeRowId = null;
}

// Klick außerhalb → schließen
document.addEventListener('click', closeAllMenus);

// Escape → schließen
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeAllMenus();
});
```

---

## Regeln

1. **Immer `role="menu"`** auf `.ctx-menu`, `role="menuitem"` auf `.ctx-item`
2. **Globales Schließen** immer implementieren — Klick außerhalb + Escape
3. **Viewport-Flip** immer für Context-Menus — nie über den Rand
4. **`.ctx-item.danger`** nur für destruktive Aktionen (Löschen, Widerrufen) — nie für "Abbrechen"
5. **`.ctx-item.disabled`** mit `aria-disabled="true"` — kein `pointer-events: none` reicht nicht für Screenreader
6. **Karte:** Browser-Standard-Kontextmenü per `e.preventDefault()` unterdrücken
7. **Max. 8 Items** pro Menü — bei mehr Aktionen eine Unterstruktur mit Labels überlegen

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-24 | Initiale Definition. Context-Menu (Karte, Rechtsklick) + Action-Menu (⋮ Button, Tabellen). Viewport-Flip. |

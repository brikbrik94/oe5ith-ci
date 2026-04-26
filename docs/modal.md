# Modal & Karten-Popup

**Referenz-Datei:** `components/modal.html`  
**Status:** definiert · v1.0

---

## Überblick

| Element | Verwendung |
|---|---|
| Modal | Info-Dialog, zentriert im Viewport, mit Backdrop |
| Karten-Popup kompakt | Punkte mit wenig Attributen (Titel + 1–2 Zeilen) |
| Karten-Popup detailliert | Punkte mit mehreren Attributen (Key-Value + Icons) |

---

## Modal

### Struktur

```html
<div class="modal-backdrop" id="modal-backdrop"
     role="dialog" aria-modal="true" aria-labelledby="modal-title"
     onclick="handleBackdropClick(event)">
  <div class="modal">

    <div class="modal-header">
      <span class="modal-title" id="modal-title">Titel</span>
      <button class="modal-close" onclick="closeModal()" aria-label="Modal schließen">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>

    <div class="modal-body">
      <!-- Strukturierter Inhalt: h2, ul, p, code -->
    </div>

  </div>
</div>
```

### Tokens

| Eigenschaft | Wert |
|---|---|
| Hintergrund | `--card-bg` (#252525) |
| Border | `1px solid --border-strong` (#444) |
| Border-Radius | `--card-radius` (12px) |
| Max-Breite | `520px` |
| Max-Höhe | `calc(100vh - 80px)` — Body scrollt |
| Backdrop | `rgba(0,0,0, 0.65)` |
| Shadow | `0 24px 48px rgba(0,0,0,0.55)` |
| Z-Index | `--z-modal` (500) |

### CSS

```css
.modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.65);
  z-index: var(--z-modal);
  display: flex; align-items: center; justify-content: center;
  padding: 20px;
  opacity: 0; pointer-events: none;
  transition: opacity 0.20s ease;
}
.modal-backdrop.open { opacity: 1; pointer-events: all; }

.modal {
  background: var(--card-bg);
  border: 1px solid var(--border-strong);
  border-radius: var(--card-radius);
  box-shadow: 0 24px 48px rgba(0,0,0,0.55);
  width: 100%; max-width: 520px;
  max-height: calc(100vh - 80px);
  display: flex; flex-direction: column;
  /* Einfahren-Animation */
  transform: translateY(6px);
  transition: transform 0.20s ease;
}
.modal-backdrop.open .modal { transform: translateY(0); }

.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border); flex-shrink: 0;
}
.modal-title { font-size: 1.0rem; font-weight: 600; color: #fff; }

.modal-close {
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 5px; border: none; background: transparent;
  color: var(--subtle); cursor: pointer; font-size: 0.85rem;
  transition: background 0.15s, color 0.15s;
}
.modal-close:hover { background: rgba(255,255,255,0.06); color: var(--text); }
.modal-close:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }

.modal-body { flex: 1; overflow-y: auto; padding: 20px; }
```

### Inhalt — Typen

```css
/* Überschrift innerhalb des Modals */
.modal-body h2 { font-size: 0.88rem; font-weight: 600; color: #fff; margin-bottom: 8px; margin-top: 18px; }
.modal-body h2:first-child { margin-top: 0; }

/* Fließtext */
.modal-body p { font-size: 0.82rem; color: var(--muted); line-height: 1.6; margin-bottom: 10px; }

/* Liste mit Accent-Dot */
.modal-body ul li { font-size: 0.82rem; color: var(--muted); padding-left: 14px; position: relative; }
.modal-body ul li::before { content: '·'; position: absolute; left: 3px; color: var(--accent); font-weight: 700; }
.modal-body ul li strong { color: var(--text); font-weight: 600; }

/* Inline Code */
.modal-body code { font-family: var(--font-mono); font-size: 0.78rem; background: var(--panel-deep); color: #e6e6e6; padding: 1px 5px; border-radius: 3px; border: 1px solid #1a1a1a; }
```

### JavaScript

```js
function openModal() {
  const bd = document.getElementById('modal-backdrop');
  bd.classList.add('open');
  bd.querySelector('.modal-close').focus();   // Fokus auf Close setzen
}

function closeModal() {
  document.getElementById('modal-backdrop').classList.remove('open');
}

function handleBackdropClick(e) {
  if (e.target === document.getElementById('modal-backdrop')) closeModal();
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});
```

### Regeln

1. `role="dialog"` + `aria-modal="true"` + `aria-labelledby` — Pflicht
2. Beim Öffnen Fokus auf `.modal-close` setzen
3. Backdrop-Klick und Escape schließen
4. `.modal-body` scrollt — `max-height` bleibt immer `calc(100vh - 80px)`
5. Vorerst nur Info-Variante — kein Footer mit Buttons

---

## Karten-Popup

Identische HTML-Struktur für Leaflet und MapLibre.
Die Karten-Bibliothek gibt die äußere Hülle vor — wir überschreiben deren CSS
und schreiben unser Markup in `.leaflet-popup-content` bzw. `.maplibregl-popup-content`.

### Gemeinsame Basis-Tokens

| Eigenschaft | Wert |
|---|---|
| Hintergrund | `--card-bg` (#252525) |
| Border | `1px solid --border-strong` (#444) |
| Border-Radius | `8px` |
| Shadow | `--shadow-dropdown` |
| Min-Breite | `200px` |
| Max-Breite | `300px` |
| Pfeil/Tip | **immer ausgeblendet** |

### Variante 1 — Kompakt

Für Punkte mit wenig Attributen: Titel + 1–2 Zeilen + optionales Badge.

```html
<div class="map-popup">
  <button class="map-popup-close" aria-label="Popup schließen">
    <i class="fa-solid fa-xmark"></i>
  </button>
  <div class="map-popup-compact">
    <div class="popup-title">Rotes Kreuz BZS Eferding</div>
    <div class="popup-sub">Organisation: ÖRK</div>
    <!-- Badge optional -->
    <span class="popup-badge">RD-OO-SEW</span>
  </div>
</div>
```

### Variante 2 — Detailliert

Für Punkte mit mehreren Attributen: Header + optionale Icons-Zeile + Key-Value Tabelle.

```html
<div class="map-popup">
  <button class="map-popup-close" aria-label="Popup schließen">
    <i class="fa-solid fa-xmark"></i>
  </button>
  <div class="map-popup-detail">

    <div class="popup-header">
      <div class="popup-header-title">Rotes Kreuz BZS Ortsstelle Eferding</div>
      <div class="popup-header-id">0110</div>
      <div class="popup-header-org">Österreichisches Rotes Kreuz</div>
    </div>

    <!-- Icons-Zeile (optional, für Fahrzeugtypen etc.) -->
    <div class="popup-icons">
      <span class="popup-icon-tag"><i class="fa-solid fa-truck-medical"></i> RTW</span>
      <span class="popup-icon-tag"><i class="fa-solid fa-car-side"></i> NEF</span>
    </div>

    <table class="popup-kv">
      <tr><td>Adresse</td> <td>Vor dem Linzertor 10<br>4070 Eferding</td></tr>
      <tr><td>Betreiber</td><td>ÖRK Landesverband OÖ</td></tr>
      <tr><td>short_name</td><td>ÖRK</td></tr>
    </table>

  </div>
</div>
```

### Wann welche Variante

| Situation | Variante |
|---|---|
| Punkt hat Name + max. 2 Felder | Kompakt |
| Punkt hat ID, Betreiber, Adresse, Typ-Icons | Detailliert |
| Clustered Marker | Kompakt (Anzahl + Layer-Name) |

---

## Leaflet CSS Override

In `app.css` der jeweiligen Seite einfügen:

```css
.leaflet-popup-content-wrapper {
  background: var(--card-bg) !important;
  border: 1px solid var(--border-strong) !important;
  border-radius: 8px !important;
  box-shadow: var(--shadow-dropdown) !important;
  padding: 0 !important;
  color: var(--text) !important;
}
.leaflet-popup-content {
  margin: 0 !important;
  min-width: 200px !important;
  max-width: 300px !important;
}
/* Pfeil ausblenden */
.leaflet-popup-tip-container { display: none !important; }

.leaflet-popup-close-button {
  color: var(--subtle) !important;
  font-size: 16px !important;
  padding: 6px 8px !important;
  top: 4px !important;
  right: 4px !important;
}
.leaflet-popup-close-button:hover { color: var(--text) !important; }
```

---

## MapLibre CSS Override

```css
.maplibregl-popup-content {
  background: var(--card-bg) !important;
  border: 1px solid var(--border-strong) !important;
  border-radius: 8px !important;
  box-shadow: var(--shadow-dropdown) !important;
  padding: 0 !important;
  color: var(--text) !important;
}
/* Pfeil ausblenden */
.maplibregl-popup-tip { display: none !important; }

.maplibregl-popup-close-button {
  color: var(--subtle) !important;
  font-size: 16px !important;
  padding: 4px 8px !important;
  top: 4px !important;
  right: 4px !important;
  background: transparent !important;
  border: none !important;
}
.maplibregl-popup-close-button:hover { color: var(--text) !important; }
```

> **Wichtig:** Die Overrides mit `!important` sind notwendig, da beide Bibliotheken
> ihre Stile inline oder mit hoher Spezifität setzen. Die CSS-Variablen (`--card-bg` etc.)
> müssen im `:root` der Seite verfügbar sein — sichergestellt durch `common.css`.

---

## Copyright-Modal

Standard-Modal für Copyright/Lizenz-Informationen.
Wird über den `©`-Button im Sidebar-Footer und den `ⓘ`-Button
in der Karten-Attribution geöffnet.

### HTML

```html
<div class="modal-backdrop" id="copyright-modal-backdrop"
     role="dialog" aria-modal="true" aria-labelledby="copyright-modal-title"
     onclick="handleBackdropClick(event)">
  <div class="modal">

    <div class="modal-header">
      <span class="modal-title" id="copyright-modal-title">
        Copyright &amp; Lizenzen
      </span>
      <button class="modal-close" onclick="closeCopyrightModal()" aria-label="Schließen">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>

    <div class="modal-body">
      <h2>Kartendaten</h2>
      <ul>
        <li><strong>OpenStreetMap</strong>: © <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap contributors</a> — ODbL 1.0</li>
        <li><strong>basemap.at</strong>: © <a href="https://basemap.at" target="_blank">basemap.at</a> — CC BY 4.0</li>
      </ul>

      <h2>Karten-Bibliothek</h2>
      <ul>
        <li><strong>Leaflet</strong>: © <a href="https://leafletjs.com" target="_blank">Vladimir Agafonkin</a> — BSD 2-Clause</li>
        <li><strong>MapLibre GL JS</strong>: © <a href="https://maplibre.org" target="_blank">MapLibre contributors</a> — BSD 3-Clause</li>
      </ul>

      <h2>Icons &amp; Schriften</h2>
      <ul>
        <li><strong>Font Awesome Free</strong>: © <a href="https://fontawesome.com" target="_blank">Fonticons, Inc.</a> — Icons CC BY 4.0, Code MIT</li>
        <li><strong>JetBrains Mono</strong>: © <a href="https://www.jetbrains.com/lp/mono/" target="_blank">JetBrains s.r.o.</a> — OFL 1.1</li>
      </ul>
    </div>

  </div>
</div>
```

### JavaScript

```js
function openCopyrightModal() {
  const bd = document.getElementById('copyright-modal-backdrop');
  bd.classList.add('open');
  bd.querySelector('.modal-close').focus();
}

function closeCopyrightModal() {
  document.getElementById('copyright-modal-backdrop').classList.remove('open');
}

function handleBackdropClick(e) {
  if (e.target.id === 'copyright-modal-backdrop') closeCopyrightModal();
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeCopyrightModal();
});
```

### Auslöser

**Sidebar-Footer (alle Seiten mit Sidebar):**

```html
<div class="sidebar-footer">
  <span class="sidebar-footer-version">v1.0.0</span>
  <!-- Status-Dot (optional) -->
  <span class="sidebar-footer-status" id="footer-status">...</span>
  <!-- © Button — immer ganz rechts -->
  <button class="sidebar-footer-copyright"
          onclick="openCopyrightModal()"
          title="Copyright &amp; Lizenzen">©</button>
</div>
```

**Karten-Attribution (Karten-Seiten):**

```html
<!-- Ersetzt die native Leaflet/MapLibre Attribution -->
<div class="map-attribution">
  © <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>
  <span class="map-attribution-sep">|</span>
  © <a href="https://leafletjs.com" target="_blank">Leaflet</a>
  <span class="map-attribution-sep">|</span>
  © <a href="https://basemap.at" target="_blank">basemap.at</a>
  <button class="map-attribution-info"
          onclick="openCopyrightModal()"
          title="Alle Copyright-Informationen">ⓘ</button>
</div>
```

> **Wichtig:** `.leaflet-control-attribution` und `.maplibregl-ctrl-attrib` werden
> durch `page.css` ausgeblendet wenn `.map-attribution` verwendet wird —
> um doppelte Attribution zu vermeiden. OSM/Leaflet bleiben aber im
> `.map-attribution` Block sichtbar — die Lizenzpflicht bleibt erfüllt.


---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-24 | Copyright-Modal, Sidebar-Footer © Button, Karten-Attribution ⓘ Button. |
| 2026-04-22 | Initiale Definition. Modal (Info-Variante), Karten-Popup kompakt + detailliert. Leaflet + MapLibre Overrides. |

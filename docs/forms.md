# Forms & Eingabeelemente

**Referenz-Datei:** `components/forms.html`  
**Status:** definiert · v1.0

---

## Überblick

Vier Formular-Elemente für Eingaben und Auswahl.
Alle teilen dieselbe Label-Struktur und denselben Focus-Ring.

| Element | Klasse | Verwendung |
|---|---|---|
| Text-Input | `.form-input` | Freitext, Geocoder, Koordinaten |
| Select | `.form-select` | Profil-Auswahl, sortierte Listen |
| Service-Selector | `.service-selector` | Endpunkt-Auswahl mit Status |
| Segmented Control | `.segmented` | Modus-Auswahl, 2–5 Optionen |

---

## Field-Wrapper

Jedes Element wird in `.form-field` eingebettet:

```html
<div class="form-field">
  <label class="form-label" for="mein-feld">Label</label>
  <!-- Control hier -->
  <span class="form-hint">Optionaler Hinweis.</span>
</div>
```

```css
.form-field   { display: flex; flex-direction: column; gap: 5px; }
.form-label   { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; color: var(--subtle); }
.form-hint    { font-size: 0.72rem; color: var(--subtle); line-height: 1.4; }
.form-error   { font-size: 0.72rem; color: var(--danger); line-height: 1.4; }
```

---

## Text-Input

Für Geocoder-Suche, Koordinaten-Eingabe, Freitext.

```html
<!-- Standard -->
<input class="form-input" type="text" placeholder="Suche…">

<!-- Mit Icon links -->
<div class="form-input-wrap">
  <i class="fa-solid fa-location-dot form-input-icon"></i>
  <input class="form-input" type="text" placeholder="Ort oder Adresse">
</div>

<!-- Koordinaten (Mono) -->
<input class="form-input mono" type="text" placeholder="48.3064, 14.2858">

<!-- Fehler -->
<input class="form-input error" type="text" value="ungültig">
<span class="form-error">Kein gültiges Koordinatenformat.</span>

<!-- Disabled -->
<input class="form-input" type="text" disabled placeholder="—">
```

```css
.form-input {
  width: 100%; height: 34px; padding: 0 10px;
  background: var(--panel-deep); border: 1px solid var(--border);
  border-radius: 5px; color: var(--text); font-size: 0.82rem; font-family: inherit;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.form-input:hover  { border-color: var(--border-strong); }
.form-input:focus  { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(59,130,246,0.15); }
.form-input:disabled { opacity: 0.45; cursor: not-allowed; }
.form-input.error  { border-color: var(--danger); box-shadow: 0 0 0 2px rgba(239,68,68,0.12); }
.form-input.mono   { font-family: var(--font-mono); font-size: 0.78rem; letter-spacing: 0.3px; }

/* Input mit Icon */
.form-input-wrap { position: relative; display: flex; align-items: center; }
.form-input-wrap .form-input { padding-left: 30px; }
.form-input-icon { position: absolute; left: 10px; font-size: 0.75rem; color: var(--subtle); pointer-events: none; }
```

---

## Select / Dropdown

Natives `<select>` mit Custom-Styling. Volle Breite, Label darüber.
Für Profil-Auswahl und andere sortierte Listen.

```html
<div class="form-field">
  <label class="form-label" for="profil">Profil</label>
  <select class="form-select" id="profil">
    <option value="driving-car">driving-car (PKW)</option>
    <option value="foot-walking">foot-walking</option>
  </select>
</div>

<!-- Disabled mit Hinweis -->
<div class="form-field">
  <label class="form-label">Profil</label>
  <select class="form-select" disabled>
    <option>— kein Profil —</option>
  </select>
  <span class="form-hint">Wähle zuerst einen Dienst.</span>
</div>
```

```css
.form-select {
  width: 100%; height: 34px; padding: 0 30px 0 10px;
  background: var(--panel-deep); border: 1px solid var(--border);
  border-radius: 5px; color: var(--text); font-size: 0.82rem; font-family: inherit;
  appearance: none; -webkit-appearance: none; cursor: pointer; outline: none;
  /* Chevron als inline SVG */
  background-image: url("data:image/svg+xml,...");
  background-repeat: no-repeat; background-position: right 10px center;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.form-select:hover  { border-color: var(--border-strong); }
.form-select:focus  { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(59,130,246,0.15); }
.form-select:disabled { opacity: 0.45; cursor: not-allowed; }
```

> **Hinweis:** Der Chevron ist als Data-URI im `background-image` eingebettet.
> Den vollständigen Wert aus `components/forms.html` übernehmen.

---

## Service-Selector

Auswahl zwischen Dienst-Endpunkten mit Status-Dot.
Genau einer aktiv — Radio-Verhalten, aber kein natives `<input type="radio">`.

```html
<div class="form-field">
  <span class="form-label">Routing-Dienst</span>
  <div class="service-selector" role="radiogroup" aria-label="Routing-Dienst wählen">

    <div class="service-option active" tabindex="0" role="radio" aria-checked="true"
         data-service="ors-proxy" onclick="selectService(this)" onkeydown="handleServiceKey(event, this)">
      <span class="service-dot online" title="Online"></span>
      <div class="service-option-text">
        <div class="service-option-name">ORS-Proxy</div>
        <div class="service-option-desc">Standard-Endpunkt</div>
      </div>
    </div>

    <div class="service-option" tabindex="-1" role="radio" aria-checked="false"
         data-service="remote" onclick="selectService(this)" onkeydown="handleServiceKey(event, this)">
      <span class="service-dot online" title="Online"></span>
      <div class="service-option-text">
        <div class="service-option-name">Remote-Engine (Proxy)</div>
        <div class="service-option-desc">ors.oe5ith.at</div>
      </div>
    </div>

  </div>
</div>
```

### Status-Dot

| Klasse | Farbe | Bedeutung |
|---|---|---|
| `.service-dot.online` | `--success` + Glow | Endpunkt erreichbar |
| `.service-dot.offline` | `--danger` + Glow | Endpunkt nicht erreichbar |
| `.service-dot.unknown` | `#555` | Status unbekannt |

### Wichtig: `tabindex` Management

Beim Aktivieren einer Option: aktive bekommt `tabindex="0"`, alle anderen `tabindex="-1"`.
Das ist das Standard-Pattern für Radiogroups (Roving Tabindex).

```js
function selectService(el) {
  const selector = el.closest('.service-selector');
  selector.querySelectorAll('.service-option').forEach(o => {
    o.classList.remove('active');
    o.setAttribute('aria-checked', 'false');
    o.setAttribute('tabindex', '-1');
  });
  el.classList.add('active');
  el.setAttribute('aria-checked', 'true');
  el.setAttribute('tabindex', '0');
}

function handleServiceKey(e, el) {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectService(el); }
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    const opts = [...el.closest('.service-selector').querySelectorAll('.service-option')];
    const next = e.key === 'ArrowDown' ? opts[opts.indexOf(el) + 1] : opts[opts.indexOf(el) - 1];
    if (next) { next.focus(); selectService(next); }
  }
}
```

---

## Segmented Control

Modus-Auswahl mit 2–5 Optionen. Immer genau einer aktiv.
Bei mehr als 5 Optionen stattdessen Select verwenden.

```html
<div class="form-field">
  <span class="form-label">Modus</span>
  <div class="segmented" role="group" aria-label="Modus wählen">
    <button class="segmented-btn active" aria-pressed="true"  onclick="selectMode(this)">A → B</button>
    <button class="segmented-btn"        aria-pressed="false" onclick="selectMode(this)">SEW</button>
    <button class="segmented-btn"        aria-pressed="false" onclick="selectMode(this)">NEF</button>
  </div>
</div>
```

```css
.segmented {
  display: flex; background: var(--panel-deep); border: 1px solid var(--border);
  border-radius: 5px; padding: 2px; gap: 2px;
}
.segmented-btn {
  flex: 1; background: transparent; border: none; border-radius: 4px;
  color: var(--muted); font-size: 0.8rem; font-weight: 600; font-family: inherit;
  padding: 5px 8px; cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.segmented-btn:hover  { color: var(--text); background: rgba(255,255,255,0.04); }
.segmented-btn.active { background: var(--accent); color: #fff; }
.segmented-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
```

```js
function selectMode(btn) {
  btn.closest('.segmented').querySelectorAll('.segmented-btn').forEach(b => {
    b.classList.remove('active'); b.setAttribute('aria-pressed', 'false');
  });
  btn.classList.add('active'); btn.setAttribute('aria-pressed', 'true');
}

// Pfeiltasten-Navigation
document.querySelectorAll('.segmented').forEach(seg => {
  seg.querySelectorAll('.segmented-btn').forEach(btn => {
    btn.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        const btns = [...seg.querySelectorAll('.segmented-btn')];
        const next = e.key === 'ArrowRight' ? btns[btns.indexOf(btn) + 1] : btns[btns.indexOf(btn) - 1];
        if (next) { next.focus(); selectMode(next); }
      }
    });
  });
});
```

---

## Regeln

1. Jedes Control immer in `.form-field` mit `.form-label` — nie ohne Label
2. `<label for="id">` bei Text-Input und Select — verknüpft Label mit Control für Accessibility
3. `.form-label` bei Service-Selector und Segmented: `<span>` statt `<label>` (kein einzelnes fokussierbares Control)
4. Disabled-State: `opacity: 0.45` + `cursor: not-allowed` — keine eigene Farbe
5. Focus-Ring: immer `box-shadow: 0 0 0 2px rgba(59,130,246,0.15)` + `border-color: --accent`
6. Segmented Control: maximal 5 Optionen — bei mehr Select verwenden
7. Service-Selector: Roving Tabindex Pattern — aktive Option `tabindex="0"`, alle anderen `-1`
8. Koordinaten-Inputs: immer `.mono` Klasse

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | Initiale Definition. Text-Input, Select, Service-Selector, Segmented Control. Keyboard-Nav für alle Custom-Controls. |

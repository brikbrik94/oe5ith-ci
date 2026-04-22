# Badges

**Referenz-Datei:** `components/badges.html`  
**Status:** definiert · v1.0

---

## Überblick

Badges sind kleine Labels für Status, Typ und Kontext-Information.
Alle Badges teilen dieselbe Basis-Klasse `.badge` — Farbe und Inhalt
variieren je nach semantischer Bedeutung.

---

## Basis-Tokens

| Token | Wert |
|---|---|
| `font-size` | `0.68rem` |
| `font-weight` | `700` |
| `text-transform` | `uppercase` |
| `letter-spacing` | `0.4px` |
| `padding` | `3px 8px` |
| `border-radius` | `4px` — eckig, kein Pill |
| `border` | `1px solid` (farbspezifisch) |

```css
.badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.4px; text-transform: uppercase;
  padding: 3px 8px; border-radius: 4px;
  border: 1px solid; white-space: nowrap; line-height: 1;
}
```

---

## Farben — 6 Varianten

| Klasse | Farbe | Verwendung |
|---|---|---|
| `.badge-blue` | `#3b82f6` | Info, allgemeine Hinweise |
| `.badge-green` | `#22c55e` | OK, Online, Aktiv, Erfolgreich |
| `.badge-yellow` | `#eab308` | Warnung, Auth required, Pending |
| `.badge-red` | `#ef4444` | Fehler, Offline, Kritisch |
| `.badge-gray` | `#666` | Typ-Info ohne Semantik (Basemap, Version) |
| `.badge-purple` | `#a78bfa` | Auth / Security (Authentik, SSO, OIDC) |

```css
.badge-blue   { background: rgba(59,130,246,0.10); color: #3b82f6; border-color: rgba(59,130,246,0.25); }
.badge-green  { background: rgba(34,197,94,0.10);  color: #22c55e; border-color: rgba(34,197,94,0.25); }
.badge-yellow { background: rgba(234,179,8,0.10);  color: #eab308; border-color: rgba(234,179,8,0.25); }
.badge-red    { background: rgba(239,68,68,0.10);  color: #ef4444; border-color: rgba(239,68,68,0.25); }
.badge-gray   { background: rgba(255,255,255,0.04); color: #666;   border-color: #2a2a2a; }
.badge-purple { background: rgba(139,92,246,0.10); color: #a78bfa; border-color: rgba(139,92,246,0.25); }
```

> **Lila** ausschließlich für Auth/Security-Kontext. Nicht für allgemeine Info verwenden —
> dafür `.badge-blue`.

---

## Inhalt — Dot, Icon oder Text

Dot und Icon sind gleichwertig — je nach Kontext wählen. Beides in einem Badge vermeiden.

### Dot (CSS-only, kein Font Awesome)

Für Status-Anzeigen: Online/Offline, Service-Health.

```html
<span class="badge badge-green">
  <span class="badge-dot"></span> Online
</span>
```

```css
.badge-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: currentColor;   /* erbt Badge-Farbe automatisch */
  flex-shrink: 0;
}
```

### Icon (Font Awesome)

Für kontextuelle Labels: Auth-Hinweise, Service-Typ, Feature-Labels.

```html
<span class="badge badge-yellow">
  <i class="fa-solid fa-key"></i> API Key required
</span>

<span class="badge badge-purple">
  <i class="fa-solid fa-shield-halved"></i> Authentik
</span>
```

```css
.badge i { font-size: 0.65rem; flex-shrink: 0; }
```

### Nur Text

Für einfache Typ-Kennzeichnung ohne Semantik. **Immer `.badge-gray`.**

```html
<span class="badge badge-gray">Basemap</span>
<span class="badge badge-gray">v1.4.2</span>
```

---

## Verwendungsregeln

### In Content Cards (Typ 3)

Badge top-right in Content Cards ist **immer grau** — keine semantischen Farben.

```html
<div class="card-content-header">
  <h3>Basemap Austria</h3>
  <span class="badge badge-gray">Basemap</span>  <!-- immer gray -->
</div>
```

### In der Sidebar (Nav-Items)

Badges können rechts in Nav-Items eingesetzt werden für kompakte Status-Info.
Sehr kleine Variante: `padding: 2px 5px; font-size: 0.6rem`.

```html
<a class="sidebar-nav-item">
  <i class="fa-solid fa-route nav-icon"></i>
  Routing API
  <span class="badge badge-yellow" style="margin-left:auto; padding:2px 5px; font-size:.6rem">
    <i class="fa-solid fa-key"></i> Key
  </span>
</a>
```

### In der Topbar

Für Seiten-Typ-Hinweis oder Auth-Kontext direkt nach dem Brand-Text.

```html
<div class="brand">
  <img src="assets/logo.svg"> INTERNAL ADMIN
</div>
<span class="badge badge-purple">
  <i class="fa-solid fa-shield-halved"></i> Authentik
</span>
```

### Standalone (außerhalb von Cards)

Hier sind alle semantischen Farben erlaubt.

---

## Nicht erlaubt

- Semantische Farben (Grün/Rot/Gelb/Blau/Lila) als Typ-Badge in Content Cards
- Pill-Form (`border-radius > 4px`) — ausschließlich 4px
- Dot **und** Icon gleichzeitig in einem Badge
- Lila für nicht-Auth-Kontext

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | Initiale Definition. 6 Farben. Eckig (4px). Dot oder Icon erlaubt. Gray-Regel für Cards. Lila für Auth/Security. |

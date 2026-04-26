# Externe Ressourcen & Self-Hosting

Alle externen Ressourcen die im OE5ITH CI verwendet werden —
mit Download-Links und Anleitung zum Self-Hosting auf dem VPS.

Ziel: **keine Abhängigkeit von externen CDNs** im Produktivbetrieb.

---

## Übersicht

| Ressource | Typ | Aktuell | Self-Hosting |
|---|---|---|---|
| JetBrains Mono | Schriftart | Google Fonts CDN | ✅ Empfohlen |
| Font Awesome Free | Icons + CSS | cdnjs CDN | ✅ Empfohlen |
| Leaflet | JS + CSS | CDN | ✅ Empfohlen |
| MapLibre GL JS | JS + CSS | CDN | ✅ Empfohlen |

---

## JetBrains Mono

**Aktuelle Einbindung (CDN):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**Self-Hosting:**

1. Schriftdateien herunterladen:
   ```
   https://github.com/JetBrains/JetBrains-Mono/releases/latest
   → JetBrains-Mono-<version>.zip herunterladen
   ```
   Benötigte Gewichte: `Regular (400)`, `Medium (500)`
   Benötigte Formate: `woff2` (alle modernen Browser), optional `woff` als Fallback

2. Dateien auf den Server:
   ```
   /var/www/<site>/assets/fonts/
   ├── JetBrainsMono-Regular.woff2
   ├── JetBrainsMono-Regular.woff
   ├── JetBrainsMono-Medium.woff2
   └── JetBrainsMono-Medium.woff
   ```

3. CSS ersetzen (in `common.css` oder site-spezifischer CSS):
   ```css
   @font-face {
     font-family: 'JetBrains Mono';
     src: url('/assets/fonts/JetBrainsMono-Regular.woff2') format('woff2'),
          url('/assets/fonts/JetBrainsMono-Regular.woff') format('woff');
     font-weight: 400;
     font-style: normal;
     font-display: swap;
   }

   @font-face {
     font-family: 'JetBrains Mono';
     src: url('/assets/fonts/JetBrainsMono-Medium.woff2') format('woff2'),
          url('/assets/fonts/JetBrainsMono-Medium.woff') format('woff');
     font-weight: 500;
     font-style: normal;
     font-display: swap;
   }
   ```

4. Google Fonts Link-Tags aus allen HTML-Dateien entfernen.

**Nginx:** Schriftdateien werden mit Standard-Static-File-Handling ausgeliefert.
Cache-Header empfohlen:
```nginx
location ~* \.(woff2|woff)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## Font Awesome Free

**Aktuelle Einbindung (CDN):**
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
```

**Self-Hosting:**

1. Herunterladen:
   ```
   https://fontawesome.com/download
   → "Free for Web" herunterladen
   ```

2. Entpacken — nur diese Ordner werden benötigt:
   ```
   fontawesome-free-6.x.x-web/
   ├── css/
   │   └── all.min.css       ← Haupt-CSS
   └── webfonts/             ← alle Schriftdateien
       ├── fa-solid-900.woff2
       ├── fa-regular-400.woff2
       ├── fa-brands-400.woff2
       └── ...
   ```

3. Auf den Server kopieren:
   ```
   /var/www/<site>/assets/fontawesome/
   ├── css/all.min.css
   └── webfonts/...
   ```

   Oder zentral für alle Sites:
   ```
   /var/www/shared/fontawesome/
   ├── css/all.min.css
   └── webfonts/...
   ```

4. CSS anpassen — in `all.min.css` den Pfad zu `../webfonts/` prüfen.
   Bei korrekter Ordnerstruktur (css/ und webfonts/ nebeneinander) funktioniert
   der relative Pfad ohne Änderung.

5. Link-Tag ersetzen:
   ```html
   <!-- vorher: CDN -->
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/...">

   <!-- nachher: lokal -->
   <link rel="stylesheet" href="/assets/fontawesome/css/all.min.css">
   ```

**Nginx:**
```nginx
location /assets/fontawesome/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## Leaflet

**Aktuelle Einbindung (CDN):**
```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.x.x/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.x.x/dist/leaflet.js"></script>
```

**Self-Hosting:**

1. Herunterladen:
   ```
   https://leafletjs.com/download.html
   → "Download Leaflet" (neueste stabile Version)
   ```

2. Auf den Server:
   ```
   /var/www/<site>/assets/leaflet/
   ├── leaflet.css
   ├── leaflet.js
   └── images/          ← Marker-Icons etc. — zwingend nötig!
       ├── marker-icon.png
       ├── marker-icon-2x.png
       ├── marker-shadow.png
       └── layers.png
   ```

   **Wichtig:** Der `images/` Ordner muss im selben Verzeichnis wie `leaflet.css`
   liegen, da das CSS relative Pfade zu den Marker-Icons verwendet.

3. Einbindung:
   ```html
   <link rel="stylesheet" href="/assets/leaflet/leaflet.css">
   <script src="/assets/leaflet/leaflet.js"></script>
   ```

4. Wenn Marker-Icons nicht erscheinen (häufiges Problem bei Bundlern/Custom-Pfaden):
   ```js
   // Marker-Icon-Pfad explizit setzen
   delete L.Icon.Default.prototype._getIconUrl;
   L.Icon.Default.mergeOptions({
     iconRetinaUrl: '/assets/leaflet/images/marker-icon-2x.png',
     iconUrl:       '/assets/leaflet/images/marker-icon.png',
     shadowUrl:     '/assets/leaflet/images/marker-shadow.png',
   });
   ```

---

## MapLibre GL JS

**Aktuelle Einbindung (CDN):**
```html
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
```

**Self-Hosting:**

1. Herunterladen — zwei Möglichkeiten:

   **Option A: npm (empfohlen)**
   ```bash
   npm pack maplibre-gl
   # oder direkt aus releases:
   # https://github.com/maplibre/maplibre-gl-js/releases
   ```

   **Option B: Direkt von unpkg herunterladen**
   ```bash
   curl -o maplibre-gl.js  https://unpkg.com/maplibre-gl/dist/maplibre-gl.js
   curl -o maplibre-gl.css https://unpkg.com/maplibre-gl/dist/maplibre-gl.css
   ```

2. Auf den Server:
   ```
   /var/www/<site>/assets/maplibre/
   ├── maplibre-gl.js
   └── maplibre-gl.css
   ```

3. Einbindung:
   ```html
   <link rel="stylesheet" href="/assets/maplibre/maplibre-gl.css">
   <script src="/assets/maplibre/maplibre-gl.js"></script>
   ```

---

## Favicon

| Datei | Format | Verwendung |
|---|---|---|
| `assets/favicon.svg` | SVG | Moderne Browser (bevorzugt) |
| `assets/favicon.ico` | ICO 16+32+48px | Ältere Browser, Windows-Taskbar |
| `assets/favicon-32.png` | PNG 32×32 | Apple Touch, PWA |
| `assets/favicon-16.png` | PNG 16×16 | Fallback |

**Einbindung in HTML:**
```html
<head>
  <!-- SVG-Favicon (moderne Browser) -->
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <!-- PNG Fallback -->
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
  <!-- ICO Fallback (ältere Browser) -->
  <link rel="shortcut icon" href="/assets/favicon.ico">
</head>
```

**Nginx — Favicon direkt im Webroot:**
```bash
# Kopieren in den Webroot damit /favicon.ico automatisch gefunden wird
cp /var/www/<site>/assets/favicon.ico /var/www/<site>/favicon.ico
```

---

## Empfohlene Asset-Struktur auf dem VPS

Für Sites die das CI verwenden:

```
/var/www/<site>/
├── assets/
│   ├── fonts/
│   │   ├── JetBrainsMono-Regular.woff2
│   │   ├── JetBrainsMono-Regular.woff
│   │   ├── JetBrainsMono-Medium.woff2
│   │   └── JetBrainsMono-Medium.woff
│   ├── fontawesome/
│   │   ├── css/all.min.css
│   │   └── webfonts/...
│   ├── leaflet/          (nur Karten-Sites)
│   │   ├── leaflet.css
│   │   ├── leaflet.js
│   │   └── images/...
│   ├── maplibre/         (nur Vektor-Karten-Sites)
│   │   ├── maplibre-gl.css
│   │   └── maplibre-gl.js
│   ├── favicon.svg
│   ├── favicon.ico
│   ├── favicon-32.png
│   └── favicon-16.png
└── css/
    ├── common.css        ← CI-Tokens (mit @font-face für JetBrains Mono)
    ├── page.css
    └── ...
```

Wenn mehrere Sites auf dem gleichen VPS laufen: Fonts und Font Awesome
können in einem gemeinsamen Verzeichnis (`/var/www/shared/`) liegen
und per Nginx-Alias oder Symlink eingebunden werden.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-24 | Initiale Erstellung. JetBrains Mono, Font Awesome, Leaflet, MapLibre, Favicon. |

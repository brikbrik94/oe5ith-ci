# Design: Map-Attribution-Bereinigung + Startseite mit Fußzeile

**Datum:** 2026-05-07  
**Status:** Genehmigt  

---

## Ziel

1. Die custom `.map-attribution`-CSS-Schicht aus `page.css` entfernen und stattdessen die native MapLibre/Leaflet-Attribution im Standard-Stil verwenden.
2. Den bestehenden Typ 5 (Landing Page) in `page.css` durch eine definierte `.page-footer`-Komponente vervollständigen und die Regel in den Docs festschreiben.

---

## Teil 1: Map-Attribution-Bereinigung

### Entfernt aus `css/page.css`

Die folgenden Klassen und Regeln werden vollständig entfernt:

```css
/* entfernen: */
.map-attribution { ... }
.map-attribution a { ... }
.map-attribution a:hover { ... }
.map-attribution-sep { ... }
.map-attribution-info { ... }
.map-attribution-info:hover { ... }
.leaflet-control-attribution { display: none !important; }
.maplibregl-ctrl-attrib       { display: none !important; }
```

### Ergebnis

MapLibre und Leaflet rendern ihre native Attribution im Default-Stil (heller Hintergrund, schwarzer Text — passt auf dunklen Karten als visueller Kontrast-Anker). Die CI greift hier nicht ein.

### Copyright-Detail

Der `.sidebar-footer-copyright`-Button im Sidebar-Footer bleibt als App-seitiger Einstiegspunkt für vollständige Lizenz- und Quelleninfos. Das ist App-Logik, kein CI-Eingriff — der Button-Style ist in `sidebar.css` bereits definiert.

### Regel (in `docs/page-types.md` ergänzen)

Karten-Seiten haben immer eine Sidebar (auch wenn sie inhaltlich leer ist). Der Sidebar-Footer zeigt Version und Copyright-Button. Kein custom `.map-attribution`-Element mehr verwenden.

---

## Teil 2: Startseite (Typ 5) mit Fußzeile

### Struktur

```
body
└── Topbar
└── landing-body
    ├── landing-title             (bestehend)
    ├── card-grid mit Nav-Cards   (bestehende cards.css Klassen)
    └── page-footer               (NEU)
        ├── page-footer-version   CI-Version, z.B. "CI v1.6.1"
        ├── page-footer-copy      Copyright-Text + Jahr
        └── page-footer-links     Link-Liste (Impressum, Datenschutz etc.)
```

### CSS (neu in `css/page.css`, beim Landing-Block)

```css
/* ── PAGE FOOTER ── */
.page-footer {
  width: 100%;
  border-top: 1px solid var(--border);
  padding: 14px 0 0;
  margin-top: auto;          /* drückt Footer ans Ende von landing-body */
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  font-size: 0.72rem;
  color: var(--subtle);
}

.page-footer-version {
  font-family: var(--font-mono);
  color: var(--subtle);
}

.page-footer-copy {
  color: var(--subtle);
}

.page-footer-links {
  display: flex;
  gap: 12px;
}

.page-footer-links a {
  color: var(--muted);
  text-decoration: none;
  transition: color var(--transition-fast);
}
.page-footer-links a:hover { color: var(--text); }
```

### Regeln (in `docs/page-types.md` dokumentieren)

| Seitentyp | Sidebar | Footer |
|---|---|---|
| Typ 1–4 (alle mit Sidebar) | Pflicht | Keiner — Version/Copyright im Sidebar-Footer |
| Typ 5 Startseite | Nicht vorhanden | `.page-footer` ist Pflicht |
| Karten-Sonderfall | Pflicht (auch wenn leer) | Keiner — Version/Copyright im Sidebar-Footer |

### Komponenten-Demo

`components/page-types.html` bekommt einen neuen Abschnitt für Typ 5 mit Footer-Demo (`.page-footer` mit Platzhalter-Werten für Version, Copyright und zwei Links).

---

## Dateikarte

| Datei | Aktion |
|---|---|
| `css/page.css` | `.map-attribution*`-Block + Hide-Regeln entfernen; `.page-footer`-Block ergänzen |
| `docs/page-types.md` | Karten-Sonderfall-Beschreibung aktualisieren; Typ 5 Footer als Pflicht dokumentieren; Regeltabelle ergänzen |
| `components/page-types.html` | Typ-5-Demo mit `.page-footer` ergänzen |
| `CHANGELOG.md` | v2.0.0-Eintrag anlegen (Breaking: `.map-attribution*` entfernt) |

---

## Versionierung

Das Entfernen von `.map-attribution`, `.map-attribution-info`, `.map-attribution-sep` sowie der Hide-Regeln für native Attribution ist ein **Breaking Change** (Klassen aus dem Public API entfernt). Laut `CLAUDE.md`-Regeln → **v2.0.0**.

Sites die aktuell `.map-attribution` verwenden (z.B. `website-v3`) müssen:
- Das `.map-attribution`-HTML-Element entfernen
- Sicherstellen dass MapLibre/Leaflet Attribution nicht mehr via CSS ausgeblendet wird
- Den `.sidebar-footer-copyright`-Button für weiterführende Copyright-Infos nutzen

---

## Nicht geändert

- `css/sidebar.css` — `.sidebar-footer-copyright` bleibt unverändert
- `css/modal.css` — keine Maplibre/Leaflet-Attribution-Overrides einführen
- `css/modal.css` — bestehende Popup-Overrides bleiben
- Alle anderen CSS-Dateien

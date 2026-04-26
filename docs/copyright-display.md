# Copyright-Darstellung auf Webseiten

Dieses Dokument definiert **wo** und **wie** Copyright-Informationen
auf den OE5ITH-Webseiten dargestellt werden.

---

## Grundregel

Zwei Ebenen der Darstellung:

| Ebene | Wo | Was |
|---|---|---|
| **Pflicht-Attribution** | Sichtbar auf der Seite | OSM, Leaflet, basemap.at (nur Karten-Seiten) |
| **Vollständige Info** | Im Copyright-Modal | Alle Lizenzen, auf allen Seiten erreichbar |

---

## 1. Sidebar-Footer (alle Seiten mit Sidebar)

Der `©`-Button im Sidebar-Footer öffnet das Copyright-Modal.
Er ist auf **jeder** Seite mit Sidebar vorhanden — unabhängig vom Seitentyp.

```
┌─────────────────────────────────────┐
│ v1.0.0        ● logged in         © │  ← © Button ganz rechts
└─────────────────────────────────────┘
```

```html
<div class="sidebar-footer">
  <span class="sidebar-footer-version">v1.0.0</span>
  <span class="sidebar-footer-status"><!-- Status optional --></span>
  <button class="sidebar-footer-copyright"
          onclick="openCopyrightModal()"
          title="Copyright &amp; Lizenzen">©</button>
</div>
```

---

## 2. Karten-Attribution (nur Karten-Seiten)

Auf allen Seiten mit Leaflet oder MapLibre **muss** die Attribution
sichtbar in der Karte erscheinen. Der `ⓘ`-Button daneben öffnet
das vollständige Copyright-Modal.

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│                    [Karte]                           │
│                                                      │
│              © OpenStreetMap | © Leaflet | © basemap.at  ⓘ │
└──────────────────────────────────────────────────────┘
```

```html
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

**Pflicht:** OSM, Leaflet und basemap.at müssen immer sichtbar sein.
Das `ⓘ`-Icon ist zusätzlich — es ersetzt nicht die Pflicht-Attribution.

---

## 3. Das Copyright-Modal

Öffnet sich über beide Auslöser (© und ⓘ).
Enthält alle Lizenzinformationen kompakt und verlinkt.

**Inhalt des Modals — immer aktuell halten:**

```
Copyright & Lizenzen
────────────────────
Kartendaten
  • OpenStreetMap contributors — ODbL 1.0
  • basemap.at — CC BY 4.0

Karten-Bibliothek
  • Leaflet — BSD 2-Clause
  • MapLibre GL JS — BSD 3-Clause

Icons & Schriften
  • Font Awesome Free — Icons CC BY 4.0, Code MIT
  • JetBrains Mono — OFL 1.1
```

Vollständige HTML-Struktur und JS: siehe `docs/modal.md` → Abschnitt "Copyright-Modal".

---

## 4. Impressum / Datenschutz (empfohlen)

Zusätzlich zur In-App-Darstellung sollte das Impressum einen Abschnitt
"Verwendete Open-Source-Ressourcen" enthalten.
Vorlage: siehe `docs/copyright.md` → Abschnitt "Webseiten-Impressum Empfehlung".

---

## Zusammenfassung: Was muss wo stehen?

| Seitentyp | Sidebar © | Karten-Attribution | Modal |
|---|---|---|---|
| Landing (cloud.oe5ith.at) | — (kein Sidebar) | — | Optional im Footer |
| Internal / Dashboard | ✅ im Sidebar-Footer | — | Via © Button |
| Tiles / Fonts / Sprites | ✅ im Sidebar-Footer | — | Via © Button |
| Karte (Leaflet/MapLibre) | ✅ im Sidebar-Footer | ✅ Pflicht in Karte | Via © und ⓘ |
| Routing / NAH | ✅ im Sidebar-Footer | ✅ Pflicht in Karte | Via © und ⓘ |

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-24 | Initiale Definition. Sidebar © Button + Karten-Attribution ⓘ + Modal. |

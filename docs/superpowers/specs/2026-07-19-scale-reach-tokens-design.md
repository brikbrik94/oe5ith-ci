# Design: Erreichbarkeits-/Zonen-Skala (`--scale-reach-*`)

**Status:** approved · 2026-07-19

---

## Kontext

Für eine neue Kartenseite (Sicherheitsberechnung) sollen Zonen abhängig von
Dauer/Entfernung eingefärbt werden — 10 Stufen von Rot (schlecht erreichbar)
nach Grün (gut erreichbar). Im CI existieren bisher nur einzelne Zustands-Tokens
(`--danger`, `--warning`, `--success`) und die 4er Chart-Palette
(`--chart-1..4`), aber keine mehrstufige Farbskala. Die Zonenfärbung selbst
passiert per JS/TS in der konsumierenden Site (Leaflet/MapLibre-Polygon-Fill),
das CI liefert nur die Farbwerte als Tokens.

Die bestehende `.map-legend`-Komponente (`components/modal.html`,
`docs/map-legend.md`) akzeptiert bereits beliebige CSS-Farbwerte pro Eintrag
(`type: 'area'`) — für die Legendendarstellung ist daher keine CI-Änderung
nötig, nur die neuen Farbwerte werden dort eingespeist.

---

## Naming

`--scale-reach-1` … `--scale-reach-10`. Bewusst generisch (nicht
"Sicherheitsberechnung"-spezifisch), da Dauer-/Entfernungs-Zonierung ein
wiederkehrendes Muster für Notfallschutz-Webmapping-Seiten ist (mehrfache
Nutzung = Kriterium für neue Tokens laut `docs/for-coding-agents.md`).

Stufe 1 = Rot = schlechteste Erreichbarkeit (weit/lang).
Stufe 10 = Grün = beste Erreichbarkeit (nah/kurz).

---

## Token-Werte

Neue Sektion in `css/common.css`, direkt nach dem bestehenden
`--danger`/`--danger-subtle`/`--danger-border`-Block. Endpunkte sind bewusst
identisch zu den bestehenden Semantik-Tokens, damit Stufe 1/10 optisch mit
`--danger`/`--success` übereinstimmen. Die 8 Zwischenwerte sind eine lineare
HSL-Interpolation (H 0°→142°, S 84%→71%, L 60%→45%) zwischen diesen beiden
Endpunkten.

```css
--scale-reach-1:  #ef4444;  /* = --danger — schlechteste Erreichbarkeit */
--scale-reach-2:  #ec6b3d;
--scale-reach-3:  #ea9537;
--scale-reach-4:  #e8c131;
--scale-reach-5:  #dbe52b;
--scale-reach-6:  #a7e225;
--scale-reach-7:  #71e01f;
--scale-reach-8:  #3dd620;
--scale-reach-9:  #21cd33;
--scale-reach-10: #22c55e;  /* = --success — beste Erreichbarkeit */

--scale-reach-gradient: linear-gradient(
  to right,
  var(--scale-reach-1), var(--scale-reach-2), var(--scale-reach-3),
  var(--scale-reach-4), var(--scale-reach-5), var(--scale-reach-6),
  var(--scale-reach-7), var(--scale-reach-8), var(--scale-reach-9),
  var(--scale-reach-10)
);
```

---

## Utility-Klasse

Neue Klasse in `css/utils.css` (eigener Kommentar-Block, analog zu den
bestehenden Utility-Gruppen dort):

```css
.scale-reach-bar {
  height: 8px;
  border-radius: var(--badge-radius);
  background: var(--scale-reach-gradient);
}
```

Zweck: durchgehender Verlaufs-Balken (z.B. unter/neben der Karte als visuelle
Legende der vollen Skala). `common.css` hat keinen generischen "small radius"-
Token — `--badge-radius` (4px) ist der kleinste bestehende Radius-Token und
wird hier wiederverwendet statt einen neuen Token nur für diesen einen Fall
anzulegen.

---

## Verwendung (Referenz für die konsumierende Site, nicht Teil des CI-Commits)

```js
// Duration/Distance-Wert in Bucket 1-10 mappen (App-Logik)
const step = bucketize(zone.durationMinutes); // 1..10
polygon.setStyle({
  fillColor: getComputedStyle(document.documentElement)
    .getPropertyValue(`--scale-reach-${step}`).trim(),
});

// Legende (bestehende MapLegend-Klasse, keine CI-Änderung nötig)
for (let i = 1; i <= 10; i++) {
  legend.addEntry({
    type: 'area',
    color: getComputedStyle(document.documentElement)
      .getPropertyValue(`--scale-reach-${i}`).trim(),
    label: labelForStep(i),
  });
}
```

---

## Dokumentation

- Neuer Abschnitt „Erreichbarkeits-/Zonen-Skala" in `docs/tokens.md`:
  Tabelle aller 11 Tokens (10 Farben + Gradient) mit Verwendungszweck,
  plus Kurzbeispiel wie oben.
- Neue Swatch-Gruppe in `components/tokens.html` (analog zum bestehenden
  `.swatch-grid`-Muster), 10 Farbfelder + ein Balken mit
  `.scale-reach-bar` zur Live-Vorschau des Gradients.
- Kein neuer `docs/registry.json`-Eintrag — läuft unter dem bestehenden
  `tokens`-Eintrag (`category: infra`, referenziert bereits
  `common.css`/`tokens.md`/`tokens.html`).

---

## Versionierung

Rein additiv (neue Tokens + neue Utility-Klasse, keine bestehenden Werte
geändert) → **MINOR-Release**. Nächste Version: `v1.22.0`.
`CHANGELOG.md`-Eintrag unter `Added`:

> Added `--scale-reach-1..10` + `--scale-reach-gradient` tokens and
> `.scale-reach-bar` utility for duration/distance-based zone coloring
> (red → green, 10 steps).

---

## Out of Scope

- Die JS-Bucketing-Logik (Wert → Stufe 1-10) gehört zur konsumierenden Site,
  nicht zum CI-Repo.
- Keine neue Legend-Komponente — `.map-legend` deckt das bereits ab.
- Keine Anpassung an `--chart-1..4` oder anderen bestehenden Farb-Tokens.

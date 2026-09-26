# Progress-Bar

Linearer Einzelwert-Fortschrittsbalken für "N von M"-Anzeigen — z. B. sequenzielle
Verarbeitung mehrerer Gebiete/Dateien in einem Job (`{"done": N, "total": M}`).
Kein Kreis-/Ring-Progress, keine eingebaute JS-Logik: Fill-Breite und Label-Text
werden vom Aufrufer gesetzt und aktualisiert (Polling/Animation ist Konsumenten-Sache,
analog zu `disclosure.md`).

CSS: `css/progress.css`. Voraussetzung: `css/common.css`.

---

## G1 — Elemente

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.progress` | Wrapper, trägt `role="progressbar"` + `aria-value*`-Attribute | Pflicht | `.indeterminate` |
| `.progress-track` | Hintergrundschiene des Balkens | Pflicht | — |
| `.progress-fill` | Füllbalken; Breite per Inline-Style (`style="width: X%"`) vom Aufrufer gesetzt | Pflicht im bestimmten Zustand, entfällt im `.indeterminate`-Zustand | — |
| `.progress-label` | Kurzer Text direkt am Balken (z. B. "3 von 5 Gebieten") | Optional | — |

## G2 — Struktur

```text
.progress                      (Pflicht — role="progressbar")
├── .progress-track            (Pflicht)
│   └── .progress-fill         (Pflicht, nur bestimmter Zustand — entfällt bei .indeterminate)
└── .progress-label            (Optional)
```

`.progress-fill` ist ausschließlich Kind von `.progress-track`, nie direktes Kind
von `.progress`. `.progress-label` liegt als Geschwister-Element neben
`.progress-track`, nicht ineinander verschachtelt.

## G3 — Reihenfolge & Platzierung

- `.progress-track` steht immer vor `.progress-label` im Markup (Balken zuerst,
  Text darunter) — beide werden per `.progress { flex-direction: column }`
  automatisch gestapelt, keine zusätzliche Positionierung durch den Aufrufer nötig.
- `.progress` benötigt keinen eigenen Rahmen und fügt sich direkt in
  `.panel`/`.panel-body` ein (kein Wrapper-Panel erforderlich), analog zu
  `.disclosure`.
- Im `.indeterminate`-Zustand entfällt `.progress-fill` vollständig aus dem
  Markup — die Animation wird rein über `.progress-track::after` erzeugt.

## G4 — Zustände & Varianten

| Zustand / Variante | Klasse / Attribut | Wann verwenden |
|---|---|---|
| Bestimmt (0–100%) | `.progress-fill` mit `style="width: X%"` | `total` ist bekannt — Fortschritt lässt sich exakt in Prozent ausdrücken |
| Unbestimmt | `.progress.indeterminate` (kein `.progress-fill`, kein `aria-valuenow`) | `total` ist noch nicht bekannt (Job hat noch kein erstes Gebiet gemeldet) |
| Mit Label | `.progress-label` gesetzt | Kurzer Statustext soll direkt am Balken angezeigt werden |
| Ohne Label | `.progress-label` weggelassen | Balken steht für sich, Text wird außerhalb vom Aufrufer platziert |

---

## Barrierefreiheit

`.progress` trägt immer:

- `role="progressbar"`
- `aria-valuemin="0"`
- `aria-valuemax="100"`
- `aria-valuenow="<X>"` — **nur im bestimmten Zustand**, entspricht der
  Fill-Breite in Prozent. Im `.indeterminate`-Zustand wird `aria-valuenow`
  weggelassen (korrekt laut WAI-ARIA für Progressbars ohne bekannten Wert).

## Tokens

Keine neuen Tokens — ausschließlich bestehende:

| Verwendung | Token |
|---|---|
| Fill-Farbe | `--accent` |
| Track-Hintergrund | `--panel-deep` |
| Track-Kontur | `--border` |
| Label-Text | `--muted` |
| Fill-Übergang | `--transition-base` |

Der Eckenradius von Track/Fill ist mit `3px` fest an die Balkenhöhe (`6px`)
gekoppelt (Pillenform) — kein Token, analog zum ebenfalls hardcodierten
`border-radius: 3px` der globalen Scrollbar in `css/common.css`.

## Beispiel

```html
<div class="progress" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-track">
    <div class="progress-fill" style="width: 60%"></div>
  </div>
  <span class="progress-label">3 von 5 Gebieten</span>
</div>
```

Unbestimmter Zustand:

```html
<div class="progress indeterminate" role="progressbar" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-track"></div>
  <span class="progress-label">Wird ermittelt…</span>
</div>
```

Referenz-HTML: `components/progress.html`.

# Logo & Favicons

Diese Datei beschreibt die Verwendung von Logo, Favicons und markennahen Assets im `oe5ith-ci` Repository.

Ziel ist, dass alle OE5ITH-Webseiten dieselben Dateien und dieselben Einbinderegeln verwenden.

---

## Dateien

Die CI-relevanten Logo- und Favicon-Dateien liegen in:

```text
assets/
```

Aktuell vorgesehene Dateien:

| Datei | Zweck |
|---|---|
| `assets/logo.svg` | primäres OE5ITH Logo |
| `assets/favicon.svg` | modernes SVG-Favicon |
| `assets/favicon.ico` | ICO-Favicon für Browser-Kompatibilität |
| `assets/favicon-32.png` | PNG-Favicon 32×32 |
| `assets/favicon-16.png` | PNG-Favicon 16×16 |

---

## Grundregeln

Logo und Favicons sind Teil der OE5ITH Brand.

Nicht erlaubt:

- Logo verzerren
- Logo drehen
- Logo mit Schatten, Glow oder Effekten versehen
- Logo umfärben, außer eine Variante ist explizit vorgesehen
- Logo als wiederholtes Hintergrundmuster verwenden
- Logo in unlesbarer Größe anzeigen
- mehrere unterschiedliche Logo-Varianten ohne Dokumentation verwenden

Erlaubt:

- Logo proportional skalieren
- Logo in Topbar, Landing Page oder Footer verwenden
- Textmarke `OE5ITH` verwenden, wenn das Logo zu klein wäre
- Favicons nach Browser-Kompatibilität gestaffelt einbinden

---

## HTML-Einbindung Favicons

Empfohlene Einbindung:

```html
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.ico" sizes="any">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/favicon-16.png" sizes="16x16" type="image/png">
```

Die Pfade können je nach Deployment abweichen.

Beispiel bei zentral gehostetem CI:

```html
<link rel="icon" href="/assets/oe5ith-ci/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/oe5ith-ci/assets/favicon.ico" sizes="any">
```

Wichtig ist, dass die Dateien aus dem CI-Repository stammen und nicht lokal pro Webseite neu erstellt werden.

---

## Logo in der Topbar

Für Seiten mit Topbar kann entweder das Logo oder die Textmarke verwendet werden.

Beispiel mit Logo:

```html
<a class="topbar-brand" href="/">
  <img src="/assets/logo.svg" alt="OE5ITH" class="topbar-logo">
  <span class="topbar-title">OE5ITH Cloud Portal</span>
</a>
```

Beispiel nur mit Textmarke:

```html
<a class="topbar-brand" href="/">
  <span class="topbar-title">OE5ITH Cloud Portal</span>
</a>
```

Wenn das Logo in der Topbar zu klein oder unruhig wirkt, ist die Textmarke vorzuziehen.

---

## Logo auf Landing Pages

Auf Landing Pages darf das Logo größer und prominenter verwendet werden.

Empfehlung:

- Logo oberhalb des Seitentitels oder links neben dem Titel verwenden.
- Genug Abstand zu Cards und Navigation halten.
- Nicht mehrere Logos auf derselben Seite platzieren.
- Logo nicht als dekorativen Hintergrund verwenden.

Beispiel:

```html
<header class="landing-header">
  <img src="/assets/logo.svg" alt="OE5ITH" class="landing-logo">
  <h1>OE5ITH Cloud Portal</h1>
</header>
```

---

## Logo im Footer

Im Footer ist das Logo optional.

Für technische Seiten reicht oft die Textmarke oder Version/Copyright-Information.

Beispiel:

```html
<footer class="site-footer">
  <span>OE5ITH</span>
  <span>©</span>
</footer>
```

Footer-Logo nur verwenden, wenn es die Seite nicht überlädt.

---

## Alt-Texte

Für das Logo soll ein kurzer, sinnvoller Alt-Text verwendet werden.

Empfohlen:

```html
<img src="/assets/logo.svg" alt="OE5ITH">
```

Wenn direkt daneben bereits `OE5ITH` als Text steht und das Logo rein dekorativ ist:

```html
<img src="/assets/logo.svg" alt="" aria-hidden="true">
```

---

## Größen

Empfohlene Richtwerte:

| Einsatz | Empfehlung |
|---|---|
| Topbar | ca. 24–36 px Höhe |
| Landing Page | ca. 64–120 px Höhe |
| Footer | ca. 20–32 px Höhe |
| Favicon SVG | Browser entscheidet |
| PNG-Favicon | 16×16 und 32×32 |

Logo immer proportional skalieren.

Nicht gleichzeitig Breite und Höhe erzwingen, wenn dadurch das Seitenverhältnis verloren geht.

Richtig:

```css
.logo {
  height: 32px;
  width: auto;
}
```

Falsch:

```css
.logo {
  width: 100px;
  height: 20px;
}
```

---

## Deployment-Pfade

Die konkrete URL hängt davon ab, wie das CI-Repository in eine Webseite eingebunden wird.

Mögliche Varianten:

```text
/assets/logo.svg
/assets/oe5ith-ci/assets/logo.svg
/css/...
```

oder bei relativer Einbindung:

```text
assets/logo.svg
```

Coding-Agenten dürfen Pfade nicht eigenmächtig ändern. Wenn ein Projekt bereits eine Pfadstruktur verwendet, ist diese beizubehalten.

---

## Wann Textmarke statt Logo?

Die Textmarke `OE5ITH` ist vorzuziehen, wenn:

- sehr wenig Platz vorhanden ist
- das Logo in der kleinen Darstellung unruhig wirkt
- die Seite sehr datenorientiert ist
- die Topbar bereits viele Bedienelemente enthält
- eine klare technische Darstellung wichtiger ist als visuelle Markenpräsenz

Beispiel:

```text
OE5ITH Tiles
OE5ITH Routing
OE5ITH SDR
```

---

## Zusammenhang mit Brand und Naming

Weitere Regeln:

```text
docs/brand.md
docs/naming.md
```

Kurzfassung:

- `OE5ITH` im sichtbaren Kontext immer groß schreiben.
- Domains und technische Pfade bleiben kleingeschrieben.
- Logo und Textmarke nicht uneinheitlich mischen.
- Service-Namen nach `docs/naming.md` verwenden.

---

## Prüfliste

Vor dem Veröffentlichen einer Seite prüfen:

- [ ] Favicon stammt aus `assets/`.
- [ ] Logo stammt aus `assets/`.
- [ ] Logo wurde nicht verzerrt.
- [ ] Logo wurde nicht lokal umfärbt.
- [ ] Alt-Text ist sinnvoll gesetzt.
- [ ] Pfade passen zum Deployment.
- [ ] Sichtbarer Dienstname folgt `docs/naming.md`.
- [ ] Keine zusätzliche lokale Logo-Variante wurde ohne Dokumentation eingeführt.

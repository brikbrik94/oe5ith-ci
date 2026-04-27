# Brand

Diese Datei beschreibt die markennahe Ebene der OE5ITH-Webseiten.

Sie ergänzt das technische Design System um Regeln zur Wiedererkennbarkeit, Schreibweise, Tonalität und visuellen Grundhaltung.

---

## Zweck

Die Brand-Regeln beantworten die Frage:

> Woran erkennt man, dass eine Webseite oder ein Dienst zum OE5ITH-System gehört?

Dazu gehören nicht nur CSS und Farben, sondern auch:

- Name und Schreibweise
- Logo und Favicons
- Grundton der Texte
- visuelle Wiedererkennbarkeit
- Umgang mit Service-Namen
- Darstellung von Copyright und Quellen
- technische, aber klare UI-Sprache

---

## Verhältnis zu CI und Design System

| Ebene | Aufgabe |
|---|---|
| Brand | Identität, Name, Tonalität, Wiedererkennbarkeit |
| CI / Corporate Identity | übergeordnete visuelle und organisatorische Regeln |
| Design System | Tokens, Komponenten, Layouts und Seitentypen |
| CSS Library | produktive CSS-Dateien für Webseiten |

Brand-Regeln sind nicht immer technische Regeln. Sie betreffen auch Inhalte, Benennung und Darstellung.

---

## Name

Die bevorzugte Schreibweise lautet:

```text
OE5ITH
```

`OE5ITH` wird groß geschrieben, da es sich um ein Amateurfunk-Rufzeichen handelt.

Nicht verwenden:

```text
oe5ith
Oe5ith
OE5ith
oe5ITH
```

Ausnahme:

- Domainnamen
- technische Pfade
- Repository-Namen
- Dateinamen
- CSS-Klassen
- URLs

Beispiele:

```text
oe5ith.at
tiles.oe5ith.at
oe5ith-ci
```

---

## Grundcharakter

Die OE5ITH-Webseiten sollen technisch, ruhig und funktional wirken.

Zielbild:

- dunkel
- sachlich
- klar strukturiert
- wenig verspielt
- gute Lesbarkeit
- status- und datenorientiert
- geeignet für Karten, Dashboards, Monitoring und technische Werkzeuge

Nicht-Zielbild:

- marketinglastig
- bunt oder verspielt
- stark animiert
- unruhig
- überladen
- uneinheitlich

---

## Tonalität

Texte sollen kurz, klar und technisch verständlich sein.

Empfohlen:

```text
Service online
Letzter Refresh: 12:04
Karte laden
Routingprofil auswählen
Keine Daten verfügbar
```

Nicht empfohlen:

```text
Wow! Dein super Service ist jetzt bereit!
Hier klicken für magische Ergebnisse!
Oopsie, da ging was schief!
```

Die Sprache darf freundlich sein, soll aber nüchtern und zweckorientiert bleiben.

---

## Sprache

Die primäre Sprache der Dokumentation und UI-Texte ist Deutsch.

Technische Begriffe können auf Englisch bleiben, wenn sie im Web-/Admin-Kontext üblich sind.

Beispiele:

- Dashboard
- Token
- Sidebar
- Topbar
- Modal
- API
- Endpoint
- Routing
- Monitoring
- Status

Wichtig ist Konsistenz: Begriffe sollen innerhalb einer Webseite und über mehrere Webseiten hinweg gleich verwendet werden.

---

## Logo

Das Logo liegt in:

```text
assets/logo.svg
```

Grundregeln:

- Logo nicht verzerren.
- Logo nicht umfärben, außer eine Variante ist explizit vorgesehen.
- Logo nicht mit Effekten wie Schatten, Glow oder Rotation verändern.
- Logo nicht in zu kleinen Größen verwenden, wenn Details unlesbar werden.
- Logo nicht als dekoratives Muster im Hintergrund verwenden.

Wenn kein Logo sinnvoll ist, darf stattdessen die Textmarke `OE5ITH` verwendet werden.

---

## Favicons

Favicons liegen in:

```text
assets/favicon.svg
assets/favicon.ico
assets/favicon-32.png
assets/favicon-16.png
```

Empfohlene Einbindung:

```html
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.ico" sizes="any">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/favicon-16.png" sizes="16x16" type="image/png">
```

Die konkreten Pfade können je nach Deployment abweichen.

---

## Farben

Die zentrale Farbdefinition liegt in:

```text
css/common.css
docs/tokens.md
```

Farben werden nicht lokal hardcodiert.

Brand-relevante Farblogik:

- dunkler Hintergrund als Grundfläche
- Blau als primäre Akzentfarbe
- Grün/Gelb/Rot nur für semantische Zustände
- Violett für Auth/Security-Kontext
- dezente Hintergründe statt greller Flächen

Semantische Farben dürfen nicht rein dekorativ verwendet werden.

Beispiel:

- `--success` nur für OK, online, aktiv
- `--warning` nur für Warnung, Hinweis, eingeschränkten Zustand
- `--danger` nur für Fehler, offline, destruktive Aktionen
- `--auth` für Auth, Security, Login, SSO

---

## UI-Stil

Der UI-Stil ist komponentenbasiert.

Typische Elemente:

- Topbar
- Sidebar
- Cards
- Panels
- Badges
- Buttons
- Tabellen
- Modals
- Karten-Overlays

Die Oberflächen sollen eher wie ein technisches Kontrollzentrum als wie eine Marketing-Webseite wirken.

Wichtig:

- klare Hierarchie
- eindeutige Statusanzeigen
- wenig visuelle Ablenkung
- konsistente Abstände
- konsistente Bedienelemente
- keine lokalen Sonderstyles ohne Notwendigkeit

---

## Service-Namen

Service-Namen sollen einheitlich und nachvollziehbar sein.

Grundform:

```text
OE5ITH <Dienstname>
```

Beispiele:

```text
OE5ITH Cloud Portal
OE5ITH Tiles
OE5ITH Routing
OE5ITH SDR
OE5ITH Monitoring
```

Die genaue Namensliste wird in einer eigenen Datei gepflegt:

```text
docs/naming.md
```

---

## Domains und technische Namen

Domainnamen und technische Identifikatoren dürfen kleingeschrieben sein.

Beispiele:

```text
oe5ith.at
tiles.oe5ith.at
karte.oe5ith.at
netbird.oe5ith.at
oe5ith-ci
```

Im sichtbaren UI-Kontext sollte aber die saubere Markenschreibweise verwendet werden:

```text
OE5ITH Tiles
```

statt:

```text
tiles.oe5ith.at
```

Ausnahme: Wenn bewusst ein technischer Endpoint oder eine URL angezeigt wird.

---

## Copyright und Quellen

Copyright- und Lizenzinformationen sind Teil der Brand-Verlässlichkeit.

Regeln dazu stehen in:

```text
docs/copyright.md
docs/copyright-display.md
```

Grundsatz:

- Pflicht-Attributionen sichtbar darstellen, wo erforderlich.
- Vollständige Lizenzinformationen über Modal oder Footer erreichbar machen.
- Externe Ressourcen und deren Lizenzen dokumentieren.
- Karten-Attributionen nicht durch ein allgemeines Copyright-Modal ersetzen.

---

## Nicht tun

Nicht CI-konform:

- verschiedene Blautöne lokal hardcoden
- eigene Button-Stile pro Webseite bauen
- unterschiedliche Sidebar-Layouts ohne dokumentierten Grund verwenden
- Statusfarben dekorativ einsetzen
- Logo verzerren oder als Effektgrafik verwenden
- Demo-CSS produktiv einbinden
- Service-Namen wechselnd schreiben
- URLs als sichtbare Seitentitel verwenden, wenn ein klarer Dienstname existiert

---

## Kurzfassung

OE5ITH-Webseiten sollen:

- technisch
- dunkel
- ruhig
- konsistent
- datenorientiert
- gut lesbar
- wiedererkennbar
- wartbar

sein.

Die Brand gibt die Identität vor. Das Design System setzt sie technisch um.

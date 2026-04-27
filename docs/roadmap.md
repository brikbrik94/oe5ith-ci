# Roadmap

Diese Datei sammelt geplante Erweiterungen für das `oe5ith-ci` Repository.

Sie dient als Arbeitsplan für zukünftige Releases und als Orientierung für manuelle Änderungen oder Coding-Agenten.

---

## Aktueller Stand

Aktueller stabiler Stand:

```text
v1.1.0
```

Schwerpunkt von `v1.1.0`:

- Dokumentationsstruktur erweitert
- README überarbeitet
- Token-Dokumentation korrigiert
- Brand-, Naming-, Logo-, Usage-, Versionierungs- und Agenten-Regeln ergänzt

Details stehen in:

```text
CHANGELOG.md
```

---

## Nächster geplanter Release

```text
v1.2.0
```

Arbeitstitel:

```text
Technischer Design-System-Ausbau
```

Ziel:

Das bestehende CI-/Design-System soll technisch robuster werden. Vor allem Tokens, Accessibility und einfache Prüfskripte sollen ergänzt werden, ohne bestehende Webseiten zu brechen.

`v1.2.0` soll rückwärtskompatibel bleiben.

---

## Ziele für v1.2.0

### 1. Accessibility-Dokumentation ergänzen

Neue Datei:

```text
docs/accessibility.md
```

Inhalte:

- Fokuszustände
- Tastaturbedienung
- Farbkontrast
- Buttons vs. Links
- Modals
- Menüs
- Karten-Controls
- `prefers-reduced-motion`
- sinnvolle Verwendung von ARIA
- Hinweise für Coding-Agenten

Grundsatz:

Accessibility-Regeln sollen pragmatisch und technisch umsetzbar sein. Ziel ist keine vollständige WCAG-Zertifizierung, sondern ein sauberer Mindeststandard für OE5ITH-Webseiten.

---

### 2. Spacing-Tokens ergänzen

Aktuell gibt es einzelne Layoutwerte wie:

```css
--card-padding: 20px;
--card-gap: 20px;
```

Für bessere Wiederverwendung soll eine Spacing-Skala ergänzt werden.

Vorschlag:

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
```

Wichtig:

- Bestehende Tokens nicht entfernen.
- Bestehende Webseiten nicht brechen.
- Bestehende Tokens können später intern auf die neue Skala gemappt werden.

Beispiel:

```css
--card-padding: var(--space-5);
--card-gap: var(--space-5);
```

---

### 3. Radius-Tokens ergänzen

Aktuell gibt es komponentennahe Radius-Tokens:

```css
--card-radius: 12px;
--btn-radius: 6px;
--badge-radius: 4px;
```

Ergänzend soll eine allgemeinere Radius-Skala eingeführt werden.

Vorschlag:

```css
--radius-sm: 4px;
--radius-md: 6px;
--radius-lg: 12px;
--radius-xl: 16px;
```

Bestehende Tokens bleiben erhalten.

Mögliche spätere Zuordnung:

```css
--badge-radius: var(--radius-sm);
--btn-radius: var(--radius-md);
--card-radius: var(--radius-lg);
```

---

### 4. Typografie-Tokens erweitern

Aktuell sind vor allem Font-Families definiert:

```css
--font-sans: 'Segoe UI', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
```

Ergänzt werden sollen Font-Size- und Line-Height-Tokens.

Vorschlag:

```css
--font-size-xs: 12px;
--font-size-sm: 13px;
--font-size-base: 14px;
--font-size-md: 16px;
--font-size-lg: 20px;
--font-size-xl: 24px;

--line-height-tight: 1.2;
--line-height-base: 1.5;
--line-height-relaxed: 1.7;
```

Zu aktualisierende Dateien:

```text
css/common.css
docs/tokens.md
docs/typography.md
components/typography.html
components/typography-preview.html
```

---

### 5. Breakpoints dokumentieren

CSS Custom Properties können nicht zuverlässig direkt in normalen `@media`-Queries verwendet werden.

Trotzdem sollen die Breakpoints zentral dokumentiert werden.

Vorschlag:

```text
Mobile:  ≤ 768px
Tablet:  769px–1024px
Desktop: ≥ 1025px
Wide:    ≥ 1440px
```

Zu dokumentieren in:

```text
docs/tokens.md
docs/page.md
docs/usage.md
```

Optional können zusätzlich reine Referenz-Tokens in `css/common.css` ergänzt werden:

```css
--breakpoint-mobile: 768px;
--breakpoint-tablet: 1024px;
--breakpoint-wide: 1440px;
```

Wichtig: Dokumentieren, dass diese Tokens nicht direkt in allen `@media`-Queries nutzbar sind.

---

### 6. Einfache CI-Checks ergänzen

Neues Script:

```text
scripts/check-ci.sh
```

Ziel:

Häufige CI-Verstöße schnell finden.

Mögliche Checks:

```bash
grep -R "#[0-9a-fA-F]\{3,8\}" css docs components
grep -R "z-index: [0-9]" css components
grep -R "css/demo.css" --include="*.html" .
grep -R "shared/assets/common.css" .
```

Das Script soll zunächst Warnungen ausgeben und nicht zu aggressiv abbrechen.

Mögliche Kategorien:

- hardcodierte Farben
- direkte Z-Index-Werte
- versehentlich produktiv eingebundenes `css/demo.css`
- alte Pfade wie `shared/assets/common.css`
- veraltete Dateinamen wie `README_v1.md`, `tokens_final.md`

Zu dokumentieren in:

```text
README.md
docs/for-coding-agents.md
docs/usage.md
```

---

### 7. README und Changelog aktualisieren

Für `v1.2.0` müssen aktualisiert werden:

```text
README.md
CHANGELOG.md
```

README ergänzen um:

- `docs/accessibility.md`
- `scripts/check-ci.sh`
- neue Token-Gruppen

CHANGELOG ergänzen um:

```text
v1.2.0
```

mit Kategorien:

- Added
- Changed
- Fixed, falls nötig

---

## Empfohlene Umsetzungsreihenfolge für v1.2.0

1. `docs/accessibility.md` erstellen.
2. Spacing-Tokens in `css/common.css` ergänzen.
3. Radius-Tokens in `css/common.css` ergänzen.
4. `docs/tokens.md` aktualisieren.
5. Typografie-Tokens in `css/common.css` ergänzen.
6. `docs/typography.md` aktualisieren.
7. Typografie-Referenzen in `components/` prüfen.
8. Breakpoints dokumentieren.
9. `scripts/check-ci.sh` erstellen.
10. `docs/for-coding-agents.md` und `docs/usage.md` um Check-Hinweise ergänzen.
11. README aktualisieren.
12. CHANGELOG aktualisieren.
13. Checks lokal ausführen.
14. Commit erstellen.
15. Tag `v1.2.0` setzen.
16. Push auf GitHub.

---

## Release-Einschätzung

`v1.2.0` sollte ein Minor Release sein.

Begründung:

- neue Tokens werden ergänzt
- neue Dokumentation wird ergänzt
- Prüfskript wird ergänzt
- bestehende Tokens und Klassen bleiben erhalten
- bestehende Webseiten bleiben kompatibel

Kein Major Release nötig, solange keine Klassen oder Tokens entfernt oder umbenannt werden.

---

## Spätere mögliche Releases

### v1.3.0 — Komponenten-Review

Mögliche Themen:

- Buttons konsolidieren
- Card-Varianten prüfen
- Badge-Varianten prüfen
- Forms vereinheitlichen
- Modal-Varianten dokumentieren
- Context-Menu auf Accessibility prüfen

---

### v1.4.0 — Beispielseiten und Templates

Mögliche Themen:

- vollständige Beispielseite für Dashboard
- vollständige Beispielseite für Detail-Seite
- vollständige Beispielseite für Listen-Seite
- vollständige Beispielseite für Karten-Seite
- HTML-Templates für Coding-Agenten

Möglicher Ordner:

```text
examples/
```

---

### v1.5.0 — Theme-Optionen

Mögliche Themen:

- Vorbereitung für Light Theme
- Theme-Tokens
- semantische Surface-Tokens
- bessere Trennung von Basisfarben und semantischen Tokens

Beispiel:

```css
--color-neutral-900: #1a1a1a;
--surface-page: var(--color-neutral-900);
```

---

### v2.0.0 — Möglicher Breaking Cleanup

Nur falls nötig.

Mögliche Themen:

- alte Tokens entfernen
- Tokens umbenennen
- CSS-Klassen konsolidieren
- Struktur stärker in Brand / Design System / CSS Library trennen
- Altlasten entfernen

Ein `v2.0.0` darf erst erfolgen, wenn Migrationshinweise vorhanden sind.

---

## Offene Fragen

Diese Punkte sollen vor der Umsetzung von `v1.2.0` geklärt werden:

- Sollen Spacing- und Radius-Tokens nur ergänzt oder bestehende Tokens direkt darauf gemappt werden?
- Soll `scripts/check-ci.sh` nur warnen oder bei Fehlern mit Exit-Code abbrechen?
- Sollen Accessibility-Regeln rein dokumentiert oder auch in CSS ergänzt werden?
- Soll es einen eigenen Ordner `examples/` bereits in `v1.2.0` geben oder erst später?
- Sollen Breakpoint-Werte als CSS-Tokens ergänzt werden, obwohl sie in Media Queries nur eingeschränkt nutzbar sind?

---

## Kurzfassung

Nächster geplanter Schritt:

```text
v1.2.0
```

Fokus:

- Accessibility-Doku
- Spacing-Tokens
- Radius-Tokens
- Typografie-Tokens
- Breakpoint-Doku
- einfache CI-Checks
- README und CHANGELOG aktualisieren

Ziel:

Das Design System technisch robuster machen, ohne bestehende Webseiten zu brechen.

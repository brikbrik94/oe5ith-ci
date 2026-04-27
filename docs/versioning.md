# Versionierung

Diese Datei beschreibt, wie Versionen für das `oe5ith-ci` Repository vergeben und dokumentiert werden.

Ziel ist, dass Webseiten nachvollziehbar angeben können, welche CI-/Design-System-Version sie verwenden, und dass Änderungen kontrolliert veröffentlicht werden.

---

## Grundprinzip

`oe5ith-ci` verwendet semantische Versionierung nach dem Schema:

```text
vMAJOR.MINOR.PATCH
```

Beispiele:

```text
v1.0.0
v1.1.0
v1.1.1
v2.0.0
```

Die Versionierung erfolgt nicht über Dateinamen.

Richtig:

```text
README.md
docs/tokens.md
docs/usage.md
```

Falsch:

```text
README_v1.md
tokens_final.md
usage_neu.md
```

Versionen werden über Git-Tags, Releases und ein zentrales `CHANGELOG.md` nachvollziehbar gemacht.

---

## Bedeutung der Versionsnummern

### MAJOR

Die MAJOR-Version wird erhöht, wenn es Breaking Changes gibt.

Beispiel:

```text
v1.4.2 → v2.0.0
```

Ein Breaking Change ist eine Änderung, durch die bestehende Webseiten angepasst werden müssen.

Beispiele:

- CSS-Klassen werden entfernt oder umbenannt.
- Tokens werden entfernt oder umbenannt.
- bestehende Komponenten ändern ihre HTML-Struktur inkompatibel.
- `css/index.css` importiert zentrale Dateien nicht mehr wie zuvor.
- Seitentypen werden grundlegend umstrukturiert.
- Standardpfade für Assets ändern sich.
- bestehende Layoutannahmen werden gebrochen.

---

### MINOR

Die MINOR-Version wird erhöht, wenn neue Funktionen oder Komponenten rückwärtskompatibel ergänzt werden.

Beispiel:

```text
v1.4.2 → v1.5.0
```

Beispiele:

- neue Komponente wird ergänzt.
- neuer Seitentyp wird dokumentiert.
- neuer Sidebar-Typ wird ergänzt.
- neue Tokens werden ergänzt.
- neue Referenz-HTMLs werden hinzugefügt.
- neue Dokumentation wird ergänzt.
- bestehende Komponenten erhalten neue optionale Varianten.

Bestehende Webseiten müssen bei MINOR-Updates nicht angepasst werden.

---

### PATCH

Die PATCH-Version wird erhöht, wenn Fehler korrigiert werden, ohne Verhalten oder API zu ändern.

Beispiel:

```text
v1.4.2 → v1.4.3
```

Beispiele:

- Tippfehler in Dokumentation.
- falscher Pfad in README korrigiert.
- kleine CSS-Bugs behoben.
- Z-Index-Doku mit CSS synchronisiert.
- fehlende Token-Dokumentation ergänzt.
- Favicon-Datei ersetzt, ohne Pfade zu ändern.
- Kommentare oder Formatierung verbessert.

---

## Was ist ein Release?

Ein Release ist ein definierter stabiler Stand des CI-Repositories.

Ein Release sollte enthalten:

- Git-Tag, z. B. `v1.2.0`
- Eintrag in `CHANGELOG.md`
- kurze Zusammenfassung der Änderungen
- Hinweis auf Breaking Changes, falls vorhanden
- Migrationshinweise, falls bestehende Webseiten angepasst werden müssen

---

## CHANGELOG.md

Für zukünftige Änderungen soll ein zentrales `CHANGELOG.md` geführt werden.

Empfohlenes Format:

```markdown
# Changelog

## v1.1.0 - 2026-04-27

### Added

- `docs/usage.md` ergänzt.
- `docs/for-coding-agents.md` ergänzt.
- `docs/versioning.md` ergänzt.

### Changed

- README-Struktur überarbeitet.
- Token-Dokumentation mit `css/common.css` synchronisiert.

### Fixed

- falsche Z-Index-Werte in eingebetteter Token-Doku korrigiert.
```

Empfohlene Kategorien:

| Kategorie | Bedeutung |
|---|---|
| Added | neu hinzugefügt |
| Changed | bestehendes Verhalten oder bestehende Doku geändert |
| Fixed | Fehler korrigiert |
| Deprecated | noch vorhanden, aber künftig zu vermeiden |
| Removed | entfernt |
| Security | sicherheitsrelevante Änderung |
| Breaking | inkompatible Änderung |

---

## Git-Tags

Releases sollen mit Git-Tags markiert werden.

Beispiel:

```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

Tags sollen nur auf stabile Stände gesetzt werden.

---

## Keine Versionierung in Dateinamen

Dateinamen bleiben stabil.

Richtig:

```text
README.md
docs/tokens.md
docs/page-types.md
docs/usage.md
```

Falsch:

```text
README_v2.md
tokens_2026.md
page-types_final.md
usage_new.md
```

Begründung:

- Links bleiben stabil.
- Coding-Agenten finden Dateien zuverlässig.
- Git zeigt die Historie bereits.
- Releases und Tags übernehmen die Versionierung.

---

## Version in Webseiten

Webseiten können optional dokumentieren, welche CI-Version sie verwenden.

Beispiel im HTML-Kommentar:

```html
<!-- OE5ITH CI: v1.1.0 -->
```

Oder als sichtbare Meta-Information im Footer:

```text
OE5ITH CI v1.1.0
```

Das ist optional, aber hilfreich bei Fehlersuche und Migrationen.

---

## Wann wird die Version erhöht?

| Änderung | Version |
|---|---|
| Tippfehler in Doku | PATCH |
| Doku ergänzt | MINOR oder PATCH |
| neue Komponente | MINOR |
| neue optionale Button-Variante | MINOR |
| CSS-Bugfix ohne neue Klassen | PATCH |
| Token ergänzt | MINOR |
| Token umbenannt | MAJOR |
| CSS-Klasse entfernt | MAJOR |
| CSS-Klasse ergänzt | MINOR |
| bestehendes Layout inkompatibel geändert | MAJOR |
| README aktualisiert | PATCH |
| neue Nutzungsdoku | MINOR |
| Breaking Change dokumentiert | MAJOR |

---

## Pre-Releases

Für experimentelle Stände können Pre-Releases verwendet werden.

Beispiele:

```text
v1.2.0-alpha.1
v1.2.0-beta.1
v1.2.0-rc.1
```

Bedeutung:

| Typ | Bedeutung |
|---|---|
| alpha | frühe experimentelle Version |
| beta | weitgehend vollständig, aber noch nicht stabil |
| rc | Release Candidate, vermutlich final |

Produktive Webseiten sollten möglichst nur stabile Versionen verwenden.

---

## Deprecation-Regel

Wenn eine Klasse, ein Token oder ein Pattern künftig ersetzt werden soll, wird es zuerst als deprecated markiert.

Ablauf:

1. In Doku als deprecated kennzeichnen.
2. Ersatz nennen.
3. Im Changelog dokumentieren.
4. Mindestens eine MINOR-Version weiter verfügbar lassen.
5. Erst mit einer MAJOR-Version entfernen.

Beispiel:

```markdown
`--old-accent` ist deprecated. Bitte `--accent` verwenden.
```

---

## Migrationshinweise

Bei Breaking Changes müssen Migrationshinweise ergänzt werden.

Beispiel:

```markdown
## Migration v1 → v2

- `.old-card` wurde durch `.ci-card` ersetzt.
- `--panel-bg` wurde durch `--panel` ersetzt.
- Karten-Seiten müssen `css/page.css` entfernen.
```

Migrationshinweise können im `CHANGELOG.md` oder in einer eigenen Datei stehen, z. B.:

```text
docs/migration-v2.md
```

---

## Empfohlener Release-Ablauf

1. Änderungen lokal prüfen.
2. `git status --short` kontrollieren.
3. `git diff` prüfen.
4. `CHANGELOG.md` aktualisieren.
5. Version festlegen.
6. Commit erstellen.
7. Tag erstellen.
8. Tag pushen.
9. Optional GitHub Release erstellen.
10. Betroffene Webseiten aktualisieren.

---

## Beispiel

Für die aktuelle Dokumentationsrunde wäre eine passende Version:

```text
v1.1.0
```

Begründung:

- neue Dokumentationsdateien wurden ergänzt.
- README wurde strukturell verbessert.
- Token-Doku wurde korrigiert.
- keine bestehenden CSS-Klassen wurden entfernt.
- bestehende Webseiten bleiben kompatibel.

---

## Kurzfassung

- Versionierung erfolgt über Git-Tags und `CHANGELOG.md`.
- Dateinamen bleiben stabil.
- Breaking Changes erhöhen MAJOR.
- Rückwärtskompatible Ergänzungen erhöhen MINOR.
- Fehlerkorrekturen erhöhen PATCH.
- Jede stabile Veröffentlichung bekommt einen Git-Tag.

# Changelog

Alle relevanten Änderungen am `oe5ith-ci` Repository werden in dieser Datei dokumentiert.

Das Format orientiert sich an semantischer Versionierung:

```text
vMAJOR.MINOR.PATCH
```

Siehe auch:

```text
docs/versioning.md
```

---

## v1.1.0 - 2026-04-27

### Added

- `docs/concepts.md` ergänzt.
  - Begriffe und Ebenen wie CI, Brand, Design System, CSS Library und Komponenten-Referenz definiert.
- `docs/usage.md` ergänzt.
  - CSS-Einbindung, Reihenfolge, Demo-CSS-Regel und Beispiele für Seitentypen dokumentiert.
- `docs/for-coding-agents.md` ergänzt.
  - Regeln für automatisierte Änderungen, Coding-Agenten und CI-konforme Umsetzung dokumentiert.
- `docs/versioning.md` ergänzt.
  - Semantische Versionierung, Release-Regeln, Git-Tags und Deprecation-Regeln dokumentiert.

### Changed

- `README.md` überarbeitet.
  - Zweck des Repositories klarer beschrieben.
  - Repo-Struktur aktualisiert.
  - Bereiche `css/`, `components/`, `docs/` und `assets/` erklärt.
  - wichtige Einstiegsdokumente ergänzt.
  - Begriffsklärung zu CI, Design System, CSS Library und Komponenten-Referenz ergänzt.
- `docs/tokens.md` überarbeitet.
  - Master-Datei auf `css/common.css` vereinheitlicht.
  - Sidebar-Tab-Tokens in die Akzent-Tabelle aufgenommen.
  - eingebettete `common.css` mit den aktuellen Token-Werten synchronisiert.

### Fixed

- Widerspruch zwischen `shared/assets/common.css` und `css/common.css` in der Token-Dokumentation korrigiert.
- Veraltete Z-Index-Werte im eingebetteten `common.css`-Block von `docs/tokens.md` korrigiert.
- Beispiel für `.layout` in `docs/tokens.md` auf `var(--topbar-height)` korrigiert.

### Notes

- Diese Version enthält nur Dokumentations- und Strukturverbesserungen.
- Es wurden keine produktiven CSS-Klassen entfernt.
- Bestehende Webseiten sollten mit dieser Version kompatibel bleiben.

---

## v1.0.0 - 2026-04-22

### Added

- Initiale vollständige Token-Definition.
- Basisfarben, Akzentfarben und semantische Farben definiert.
- Typografie-, Spacing-, Z-Index-, Transition- und Shadow-Tokens ergänzt.
- Komponentenstruktur für Topbar, Sidebar, Cards, Buttons, Badges, Forms, Modal und Typografie aufgebaut.
- Referenz-HTMLs in `components/` ergänzt.
- Spezifikationen in `docs/` ergänzt.
- Logo und Favicons in `assets/` ergänzt.

### Notes

- Erste konsolidierte Version des OE5ITH CI / Design Systems.

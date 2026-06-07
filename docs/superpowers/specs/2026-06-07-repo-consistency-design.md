# Repo-Konsistenz & Doku-Sync — Design

**Datum:** 2026-06-07
**Status:** Genehmigt (Brainstorming abgeschlossen)

## Problem

Die Grundstruktur des Repos (`css/` · `components/` · `docs/` · `assets/` · `scripts/`)
ist sauber und tragfähig. Das eigentliche Problem ist **Dokumentations-Drift**:

- README pflegt den kompletten Datei-Baum und die Status-Tabelle **von Hand** →
  veraltet ständig. Konkret: README listet eine nicht existierende `tokens.css`
  (Karteileiche) und es fehlen `calendar.css`, `code-viewer.css`, `coords.css`,
  `service-dashboard.css`, `toast.css`, `utils.css` sowie diverse Docs.
- CLAUDE.md „CSS loading order" nennt nur einen veralteten Teilsatz der CSS-Dateien.
- Altlasten: `CI_FIXES_REPORT.md` (vollständig umgesetzt → obsolet), `.worktrees/`
  nicht in `.gitignore`, offene uncommittete Änderungen.

Die Beziehungen zwischen Dateien sind **many-to-many und teils bewusst lückenhaft**
(konzeptionelle Docs ohne CSS; Patterns wie `context-menu` dokumentiert, aber CSS in
anderen Dateien; ein Feature mit mehreren HTMLs). Naives Namens-Matching scheitert daran.

## Ziel

1. Eine deklarative **Single Source of Truth** für „welches Feature besitzt welche Dateien".
2. Ein **wiederverwendbares Check-Script**, das Drift in beide Richtungen erkennt.
3. README-Übersicht wird **generiert**, kann strukturell nicht mehr veralten.
4. Eine **verbindliche Doku-Konvention**, die den Dreiklang Spec→Referenz→CSS prüfbar macht.
5. Altlasten entfernt.

Kein Umbau der bestehenden Ordnerstruktur — der Aufbau bleibt wie er ist.

## Architektur

```
docs/registry.json   ──►  scripts/cli/check_consistency.py  ──►  - Exit-Code (0/1)
(Single Source of                    │                            - Bericht via utils.py
 Truth: Feature→Dateien)             │                            - Generiert README-Abschnitte
                                     ▼
                          Validierung gegen reale
                          Dateien in css/ components/ docs/
```

Das Manifest ist die einzige Wahrheit. Das Script vergleicht Manifest ↔ Platte und
rendert daraus die README. Die Doku-Konvention bindet beides an den Workflow.

## Bausteine

### 1. Manifest — `docs/registry.json`

Deklarative Liste aller Features mit ihren Dateien und einer Kategorie.

```json
{
  "components": [
    { "id": "topbar", "title": "Topbar", "category": "component",
      "css": ["topbar.css"], "doc": ["topbar.md"], "html": ["topbar.html"] },

    { "id": "service-dashboard", "title": "Service-Dashboard", "category": "component",
      "css": ["service-dashboard.css"], "doc": ["service-dashboard.md"],
      "html": ["service-dashboard-overview.html", "service-dashboard-detail.html",
               "service-dashboard-config.html"] },

    { "id": "context-menu", "title": "Context-Menu", "category": "component",
      "css": [], "doc": ["context-menu.md"], "html": ["context-menu.html"],
      "note": "CSS lebt in modal.css/page.css" },

    { "id": "brand", "title": "Brand", "category": "concept",
      "css": [], "doc": ["brand.md"], "html": [] },

    { "id": "common", "title": "Tokens / Reset / Layout", "category": "infra",
      "css": ["common.css"], "doc": ["tokens.md"], "html": ["tokens.html"] }
  ]
}
```

**Felder:** `id` (kebab-case, eindeutig), `title` (Anzeigename), `category`, `css`/`doc`/`html`
(Dateilisten relativ zum jeweiligen Ordner), `note` (optional, erklärt bewusste Lücken).

**Kategorien:**
- `component` — voller Dreiklang Spec→Referenz→CSS erwartet.
- `concept` — reine Doku (z. B. `brand`, `naming`, `concepts`, `versioning`, `usage`,
  `for-coding-agents`, `copyright`, `copyright-display`, `resources`, `logo`, `cli`, `roadmap`).
- `infra` — Sonderfälle (`common`, `index`, `demo`).

Leere Arrays + `note` machen bewusste Abweichungen explizit und dokumentiert — kein stilles
Sonderfall-Wissen mehr.

### 2. Check-Script — `scripts/cli/check_consistency.py`

Nutzt die bestehenden Logger aus `scripts/cli/utils.py` (`log_step`, `log_success`,
`log_warn`, `log_error`). Fünf Prüfungen:

1. **Dangling:** Manifest nennt eine Datei, die nicht existiert → Fehler.
2. **Orphan:** Datei in `css/` / `components/` / `docs/` gehört zu keinem Manifest-Eintrag →
   Fehler (zwingt zur Registrierung von Neuem). `docs/superpowers/**` ist ausgenommen.
3. **Import-Check:** Jede produktive `css/*.css` (außer `demo.css` und `index.css` selbst) ist
   in `css/index.css` per `@import` eingebunden.
4. **Kategorie-Regeln:** `category: component` ohne `doc` → Warnung (Dreiklang verletzt).
5. **Exit-Code:** 1 bei jedem Fehler, sonst 0 → Pre-Commit/CI-tauglich.

**CLI:**
- `python scripts/cli/check_consistency.py` — nur prüfen, read-only.
- `python scripts/cli/check_consistency.py --write` — zusätzlich README-Abschnitte generieren.

### 3. README-Generierung (Marker-Block)

In README kommen Marker um Datei-Baum und Status-Tabelle:

```html
<!-- AUTOGEN:structure START -->
... generierter Datei-Baum ...
<!-- AUTOGEN:structure END -->

<!-- AUTOGEN:status START -->
... generierte Status-Tabelle (Spec / Referenz-HTML / CSS: ✅ oder —) ...
<!-- AUTOGEN:status END -->
```

`--write` rendert beide Blöcke aus dem Manifest. Alles außerhalb der Marker bleibt
handgepflegt (Prosa, Grundregeln, Workflow). Damit kann die Übersicht strukturell nicht
mehr veralten; die `tokens.css`-Karteileiche verschwindet automatisch.

**CLAUDE.md:** Die „CSS loading order" wird **einmalig manuell** korrigiert (kurze,
konzeptionell geordnete Liste — nicht alphabetisch, daher nicht generiert). Plus ein
Verweis auf die Registrierungs-Konvention.

### 4. Doku-Konvention — `docs/for-coding-agents.md`

Neuer verbindlicher Abschnitt **„Neue Komponente registrieren"**:

> Jede neue Komponente/jedes Feature:
> 1. Eintrag in `docs/registry.json`
> 2. Spec in `docs/`
> 3. Referenz-HTML in `components/`
> 4. CSS in `css/` + Import in `css/index.css`
> 5. `python scripts/cli/check_consistency.py` muss grün sein

Kurzer Verweis darauf in CLAUDE.md.

### 5. Cleanup

- `CI_FIXES_REPORT.md` löschen (vollständig umgesetzt, verifiziert: z-index-Tokens und
  `--topbar-height-mobile` existieren in `common.css`, keine hartcodierten z-index in `css/`).
- `.worktrees/` in `.gitignore` aufnehmen.
- Offene Änderungen (`docs/topbar.md`, neues `CLAUDE.md`) am Ende sauber committen.

## Testing

- **Positiv:** Manifest gegen Ist-Stand vollständig erstellen → Script läuft grün.
- **Negativ:** testweise eine Datei umbenennen bzw. aus dem Manifest entfernen → Script läuft
  rot mit klarer Dangling-/Orphan-Meldung.
- **Generierung:** `--write` → README-Blöcke korrekt gerendert, Inhalt außerhalb der Marker
  unverändert (Diff prüfen).

## Bewusst nicht im Scope (YAGNI)

- Keine Umstrukturierung der Ordner.
- Keine Generierung der CLAUDE.md-Loading-Order (manuell, einmalig).
- Keine CI-Pipeline-Einrichtung — das Script ist nur CI-*tauglich*; Einbindung ist ein
  möglicher Folgeschritt.
- `version`/`status`-Felder im Manifest erst, wenn ein konkreter Bedarf entsteht.

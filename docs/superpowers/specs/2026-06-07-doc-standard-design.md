# Doku-Standard für Komponenten-Docs — Design

**Datum:** 2026-06-07
**Status:** Genehmigt (Brainstorming abgeschlossen)

## Problem

Die beschreibenden Docs in `docs/` sind für Coding-Agenten gedacht, aber nicht
durchgängig **interpretationsfrei**: Bei manchen Komponenten (z. B.
`service-dashboard.md`) muss ein Agent die Beispiel-HTML in `components/*.html`
lesen und interpretieren, um zu wissen, welche Elemente zu verwenden sind, in
welcher Reihenfolge/Platzierung (z. B. wo Speichern/Abbrechen-Buttons hinkommen),
wie die DOM-Verschachtelung aussieht und welche Zustände/Varianten existieren.

Ziel: Jede Komponenten-Doc soll so vollständig sein, dass ein Agent die Komponente
allein aus dem Text + den Element-Listen korrekt bauen kann — ohne die Beispielseite
zu interpretieren. Das HTML in `components/` ist dann **Verifikation, nicht Quelle**.

## Ziel & Umfang

Erster Schritt (dieser Spec):

1. Einen verbindlichen **Doku-Standard** als neue Datei `docs/doc-standard.md` definieren.
2. `service-dashboard.md` als **kanonisches Muster** vollständig auf den Standard heben.
3. Den Standard in `for-coding-agents.md` verankern und als Registry-Eintrag registrieren.

Der Rollout auf die übrigen Komponenten-Docs erfolgt später als eigene Pläne (nicht hier).

## Geltungsbereich

Der Standard gilt für Docs der Registry-Kategorie **`component`**. `concept`-Docs
(brand, naming, versioning, usage …) und `infra` sind ausgenommen — sie beschreiben
keine zusammensetzbaren UI-Elemente. Dies knüpft an die in v1.12.1 eingeführten
Registry-Kategorien an.

## Die vier Pflicht-Garantien

Jede `component`-Doc MUSS diese vier Informationen vollständig im Text enthalten,
jeweils im vorgegebenen Format:

### G1 — Vollständige Element-Tabelle

Jede verwendbare Klasse/jedes Element der Komponente steht in einer Tabelle mit den
Spalten:

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|

Keine Klasse darf nur in der Beispiel-HTML auftauchen, ohne in dieser Tabelle zu stehen.

### G2 — Struktur / Verschachtelung

Ein expliziter Baum (oder annotiertes HTML-Skelett) der Eltern-Kind-Hierarchie, sodass
die DOM-Verschachtelung ohne Lesen der `components/*.html` klar ist. Beispiel-Format:

```text
.svc-form-actions
├── button.btn.btn-primary      (Speichern — Pflicht)
├── a.btn.btn-ghost             (Abbrechen — Pflicht)
└── span.svc-form-hint          (Hinweis — Optional)
```

### G3 — Reihenfolge & Platzierung

Explizite Prosa-Regeln zur Anordnung/Position, nicht nur aus dem Beispiel ablesbar.
Verbindliche Button-Konvention (projektweit): **primärer Button zuerst/links,
sekundärer als `btn-ghost` daneben.** Weitere Platzierungsregeln je Komponente
(z. B. „Header: Titel links, Status/Aktionen rechts").

### G4 — Zustände & Varianten

Eine Tabelle aller Zustände/Varianten mit der Bedingung „wann verwenden":

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|

## `docs/doc-standard.md` — Inhalt

Die Datei enthält:

1. **Definition „interpretationsfrei"** — kurze Erklärung des Ziels und der Regel
   „Doc ist Quelle, `components/*.html` ist Verifikation".
2. **Geltungsbereich** — gilt für `category: component`; concept/infra ausgenommen.
3. **Die vier Garantien G1–G4** — jeweils mit Format-Vorlage (Tabellen-/Baum-Schema oben).
4. **Hinweis zur Flexibilität** — der Standard schreibt Pflicht-*Informationen* vor, keine
   starre identische Abschnittsreihenfolge. Bestehende vollständige Docs (z. B.
   `buttons.md`, `cards.md`) erfüllen ihn bereits und müssen nicht umgeschrieben werden;
   komponenten-spezifische Zusatzabschnitte bleiben erlaubt.

## Muster-Umbau `service-dashboard.md`

Die Datei wird auf den Standard gehoben. Konkrete, heute interpretationsbedürftige Lücken:

- **G1:** Element-Tabelle um fehlende Klassen ergänzen — insbesondere die vollständigen
  Toggle-Teile (`.svc-toggle-track`, `.svc-toggle-thumb`, `.svc-toggle-label`,
  `.svc-toggle-sublabel`) und alle `svc-*`-Klassen der drei Seiten.
- **G2:** Verschachtelungs-Baum für alle drei Seiten (Overview / Detail / Config).
- **G3:** Reihenfolge/Platzierung der **Speichern/Abbrechen-Buttons** als explizite Regel:
  Speichern = `btn btn-primary` (Disketten-Icon) zuerst, Abbrechen = `btn btn-ghost`
  daneben, optionaler `.svc-form-hint` rechts. Plus Header-Platzierung der Detailseite.
- **G4:** Zustände-Tabelle: online/offline/unknown (Status-Dots & Status-Line),
  Toggle on/warn, Read-only-Feld.

Die anderen Komponenten-Docs bleiben in diesem Schritt unberührt.

## Verankerung

- `docs/doc-standard.md` wird als **Registry-Eintrag** (`category: concept`,
  `doc: ["doc-standard.md"]`) in `docs/registry.json` ergänzt, damit
  `python3 scripts/cli/check_consistency.py` grün bleibt (kein Orphan).
- In `docs/for-coding-agents.md` ein Verweis-Abschnitt: „Komponenten-Docs folgen
  `docs/doc-standard.md` (interpretationsfrei, G1–G4)."
- Ein neuer Punkt in der Abschluss-Prüfliste von `for-coding-agents.md`.

## Versionierung

Reine Doku-Änderung → **PATCH** (`v1.12.2`). CHANGELOG unter `Added` (doc-standard) und
`Changed` (service-dashboard.md interpretationsfrei).

## Bewusst nicht im Scope (YAGNI)

- Kein maschineller Inhalts-Check (Heading-Prüfung in `check_consistency.py`) — ein Tool
  kann „Abschnitt existiert" prüfen, nicht „Inhalt ist interpretationsfrei". Möglicher
  späterer Zusatz.
- Kein Umbau der übrigen ~15 Komponenten-Docs in diesem Schritt (eigene Pläne).
- Keine Änderung an `components/*.html` — die Doc ist die Quelle, das HTML bleibt
  Verifikation.

## Testing / Verifikation

- `python3 scripts/cli/check_consistency.py` bleibt grün (neuer Registry-Eintrag, kein Orphan).
- Manuelle Prüfung am Muster: Kann `service-dashboard.md` die Config-Seite (Felder,
  Button-Platzierung, Verschachtelung, Zustände) allein aus dem Text beschreiben, ohne
  dass `service-dashboard-config.html` gelesen werden muss? Gegencheck: jede `svc-*`-Klasse
  im CSS tauct in der Element-Tabelle auf.

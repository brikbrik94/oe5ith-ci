# Doku-Standard für Komponenten-Docs

Dieser Standard legt fest, wie beschreibende Komponenten-Docs in `docs/` geschrieben
werden, damit ein Coding-Agent eine Komponente **allein aus der Doc** korrekt umsetzen
kann — ohne die Beispiel-HTML in `components/*.html` interpretieren zu müssen.

**Grundregel:** Die Doc ist die Quelle. Das HTML in `components/` ist nur **Verifikation**,
nicht die Spezifikation. Was nur im Beispiel-HTML steht, aber nicht in der Doc, gilt als
nicht spezifiziert.

---

## Geltungsbereich

Der Standard gilt für Docs der Registry-Kategorie **`component`** (siehe
`docs/registry.json`). Konzept-Docs (`concept`, z. B. brand, naming, versioning) und
Infrastruktur (`infra`) sind ausgenommen — sie beschreiben keine zusammensetzbaren
UI-Elemente.

Der Standard schreibt Pflicht-**Informationen** vor, keine starre identische
Abschnittsreihenfolge. Bestehende vollständige Docs erfüllen ihn ggf. bereits;
komponenten-spezifische Zusatzabschnitte bleiben erlaubt.

---

## Die vier Pflicht-Garantien

Jede `component`-Doc MUSS diese vier Informationen vollständig im Text enthalten.

### G1 — Vollständige Element-Tabelle

Jede verwendbare Klasse/jedes Element der Komponente steht in einer Tabelle. **Keine
Klasse darf nur im Beispiel-HTML auftauchen.** Format:

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.beispiel` | Was es tut | Pflicht | `.aktiv`, `.warn` |

### G2 — Struktur / Verschachtelung

Ein expliziter Baum der Eltern-Kind-Hierarchie, sodass die DOM-Verschachtelung ohne
Lesen der `components/*.html` klar ist. Format:

```text
.wrapper
├── .kind-a            (Pflicht)
└── .kind-b            (Optional)
```

### G3 — Reihenfolge & Platzierung

Explizite Prosa-Regeln zur Anordnung/Position — nicht nur aus dem Beispiel ablesbar.

**Projektweite Button-Konvention:** primärer Button zuerst/links, sekundärer als
`btn-ghost` daneben.

### G4 — Zustände & Varianten

Eine Tabelle aller Zustände/Varianten mit der Bedingung „wann verwenden". Format:

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Aktiv | `.aktiv` | Wenn der Dienst läuft |

---

## Prüffrage

Bevor eine Komponenten-Doc als fertig gilt: *Könnte ein Agent die Komponente bauen, ohne
die `components/*.html` zu öffnen?* Wenn nein, fehlt eine der Garantien G1–G4.

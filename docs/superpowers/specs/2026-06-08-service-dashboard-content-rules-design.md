# Service-Dashboard — Inhaltliche Spezifikation (Detail + Config)

**Datum:** 2026-06-08
**Status:** Design (genehmigt)
**Betroffene Datei:** `docs/service-dashboard.md` (reines Doku-Update, keine CSS-Änderung)

## Ziel

Die bestehende Service-Dashboard-Doku beschreibt die **Struktur** der drei Seiten
(G1–G4 nach `docs/doc-standard.md`), legt aber nicht fest, **welche Inhalte
semantisch wohin gehören**. Diese Spec ergänzt zwei inhaltliche Regelwerke:

1. **Detail-Seite:** Ein-Endpunkt-Regel + festes Set erlaubter Panel-Typen.
2. **Config-Seite:** Kategorien-Gruppierung (offenes Prinzip) + Pflicht-Überschrift je Panel.

Es werden **keine neuen CSS-Klassen** eingeführt und keine bestehende Struktur
geändert. Nur Text in `docs/service-dashboard.md`.

---

## Abschnitt A — Detail-Seite (Seite 2)

### A1. Grundregel: Ein Endpunkt pro Detailseite

Eine Detailseite zeigt **genau einen Dienst/Endpunkt**. Alle Panels der Seite
beziehen sich auf diesen einen Endpunkt. Mehrere Dienste werden **nie** auf
einer Detailseite gemischt — jeder Dienst hat seine eigene Detailseite, der
Wechsel erfolgt über die Sidebar-Navigation.

Hinweis: Die „Variante – Dienst offline" in `components/service-dashboard-detail.html`
ist eine **Zustands-Demo** (Offline-Darstellung), kein zweiter Dienst auf
derselben Seite.

### A2. Festes Set an Panel-Typen

Jede Kachel (`.panel`) auf der Detailseite muss **genau einem** der folgenden
Panel-Typen entsprechen. Andere Panel-Typen sind nicht zulässig.

| Panel-Typ | Inhalt | Pflicht/Optional |
|---|---|---|
| **Live-Status** | Echtzeit-Laufzeitwerte, per JS aktualisiert (z.B. GPS-Fix, Geschwindigkeit, nächste TX, Payload, Dienst aktiv) | Pflicht (mind. 1 pro Seite) |
| **Verbindung / Endpoint** | Statische Verbindungsdaten: Host, Port, Protokoll, URL, letzter Kontakt | Optional |
| **Konfiguration (read-only)** | Aktuell geladene Einstellungen nur zur Anzeige; Ändern erfolgt über die Config-Seite | Optional |
| **Diagnose / Fehler** | Letzte Fehler, Warnungen, Diagnosehinweise | Optional |

### A3. Zellen-Regel

Ein Wert = eine `.svc-data-cell` (Label / Wert / optional Subtext). Eine Zelle
enthält **keinen** zusammengesetzten oder mehrwertigen Inhalt — mehrere Werte
werden auf mehrere Zellen aufgeteilt.

---

## Abschnitt B — Config-Seite (Seite 3)

### B1. Gruppierung nach Kategorien (offenes Prinzip)

Einstellungen werden thematisch in Panels („Kategorien") gruppiert. Dienste
wählen die passenden Kategorien selbst — es gibt **keine** geschlossene Liste.

Empfohlene Beispiel-Kategorien: **Allgemein, Verbindung, Authentifizierung,
Erweitert**.

Reihenfolge: allgemeine/häufig genutzte Kategorien zuerst, „Erweitert" bzw.
riskante Einstellungen zuletzt.

### B2. Pflicht-Überschrift je Panel

**Jedes Config-Panel MUSS eine Überschrift** (`.panel-title` mit Icon +
Bezeichnung) enthalten — auch wenn das Panel nur ein einzelnes Feld hat. Damit
wird `.panel-title` auf der Config-Seite von „bestehende Klasse" zu **Pflicht**
hochgestuft.

---

## Platzierung im Doc

- **Seite 2 — Detail:** Neue Unterüberschrift `### Inhalt & Semantik` nach dem
  bestehenden `### Reihenfolge & Platzierung (G3)`. Enthält A1 (Ein-Endpunkt-Regel),
  A2 (Panel-Typen-Tabelle) und A3 (Zellen-Regel).
- **Seite 3 — Config:** Neue Unterüberschrift `### Inhalt & Semantik` nach dem
  bestehenden `### Reihenfolge & Platzierung (G3)`. Enthält B1 (Kategorien-Prinzip)
  und B2 (Pflicht-Überschrift). Zusätzlich: in der G1-Tabelle bzw. im
  G1-„Bestehende Klassen"-Hinweis der Config-Seite kenntlich machen, dass
  `.panel-title` dort Pflicht ist.
- **Änderungshistorie:** Neuer Eintrag mit Datum 2026-06-08.

## Nicht-Ziele (YAGNI)

- Keine neuen CSS-Klassen.
- Keine Änderung der bestehenden G2-Verschachtelungsbäume (Struktur bleibt gleich).
- Keine geschlossene Kategorienliste für die Config-Seite (bewusst offen).
- Keine Änderung an der Übersichts-Seite (Seite 1).

## Verifikation

- `python3 scripts/cli/check_consistency.py` läuft weiterhin grün (keine neuen
  Dateien, keine Registry-Änderung — `service-dashboard` ist bereits registriert).
- Doku bleibt interpretationsfrei im Sinne von `docs/doc-standard.md`.

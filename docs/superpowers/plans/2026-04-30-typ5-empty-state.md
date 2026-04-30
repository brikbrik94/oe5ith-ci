# Typ 5 Empty State Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `.result-empty` als neue CSS-Klasse für den leeren Zustand von Typ-5-Sidebars — optional mit Icon, kein Hover, kein Klick.

**Architecture:** Zwei CSS-Stellen (Produktions-CSS + Demo-Inline-Style), ein neues HTML-Beispiel in der Referenzseite, eine Doku-Erweiterung. Kein Build-Schritt erforderlich, reine CSS/HTML-Änderungen.

**Tech Stack:** CSS (Custom Properties), HTML, FontAwesome (optional für Icons)

---

## Dateiübersicht

| Datei | Änderung |
|---|---|
| `css/sidebar.css` | `.result-empty` + `.result-empty i` am Ende des Typen-Blocks ergänzen |
| `components/sidebar-types.html` | `.result-empty` zum `<style>`-Block hinzufügen + neues Demo-Panel für den Leerzustand |
| `docs/sidebar-types.md` | Typ-5-Abschnitt: `.result-empty` dokumentieren |

---

## Task 1: CSS in `sidebar.css` ergänzen

**Files:**
- Modify: `css/sidebar.css` — nach letzter Regel (Zeile 240, Ende der Datei)

- [ ] **Schritt 1: CSS-Regeln ans Ende von `sidebar.css` anfügen**

Direkt vor dem abschließenden `@media (max-width: 768px)`-Block (Zeile 229), nach dem Kommentar `/* ═══ PAGE CONTENT ═══ */`, diese Regeln einfügen:

```css
/* ═══ TYP 5 — LEERZUSTAND ═══ */
.result-empty {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px 4px;
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.5;
}
.result-empty i {
  flex-shrink: 0;
  margin-top: 2px;
  opacity: 0.5;
  font-size: 0.85rem;
}
```

- [ ] **Schritt 2: Visuell im Browser prüfen**

`components/sidebar-types.html` im Browser öffnen — es darf noch keine sichtbare Änderung geben, da die Klasse noch nicht genutzt wird. Kein Fehler in der Browser-Konsole.

- [ ] **Schritt 3: Commit**

```bash
git add css/sidebar.css
git commit -m "feat: add .result-empty empty state class for Typ 5 sidebar"
```

---

## Task 2: Demo-Styles in `components/sidebar-types.html` ergänzen

**Files:**
- Modify: `components/sidebar-types.html` — `<style>`-Block, nach Zeile 312 (nach `.result-simple-meta`)

Die Demo-HTML-Datei hat einen eigenen `<style>`-Block mit allen Typ-4/5-Klassen. `.result-empty` muss dort ebenfalls eingetragen werden, damit der Demo korrekt rendert.

- [ ] **Schritt 1: CSS in den `<style>`-Block einfügen**

Nach der Regel `.result-simple-meta { ... }` (Zeile 312) diese Regeln einfügen:

```css
/* Typ 5: Leerzustand */
.result-empty {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px 4px;
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.5;
}
.result-empty i {
  flex-shrink: 0;
  margin-top: 2px;
  opacity: 0.5;
  font-size: 0.85rem;
}
```

- [ ] **Schritt 2: Neues Demo-Panel für Leerzustand in Typ-5-Sektion einbauen**

Die Typ-5-Sektion beginnt bei Zeile 624 (`<!-- ═══ TYP 5: ERGEBNIS-LISTE EINFACH ═══ -->`). Nach dem bestehenden `.screen`-Block mit der Ergebnis-Liste (endet bei Zeile 682) ein zweites Screen-Panel für den Leerzustand ergänzen:

```html
<!-- Leerzustand -->
<div class="screen" style="margin-top:16px">
  <div class="m-tb">
    <div class="m-brand"><img src="assets/logo.svg"> OESITH</div>
    <div class="m-nav"><a>OSM Standard ▾</a><a>Zoom</a><a>Legende</a></div>
  </div>
  <div class="m-layout">
    <div class="sidebar" style="height:200px">
      <div class="sidebar-inner">
        <div style="font-size:0.88rem;font-weight:600;color:#fff;margin-bottom:12px">Nächste Stützpunkte</div>
        <div class="result-empty">
          <i class="fa-solid fa-arrow-pointer"></i>
          Klicke auf einen Punkt in der Karte, um die 5 nächsten NAH-Stützpunkte zu berechnen.
        </div>
      </div>
    </div>
    <div class="m-map-bg"><span class="m-map-label">Leaflet / MapLibre</span></div>
  </div>
</div>
```

- [ ] **Schritt 3: Im Browser prüfen**

`components/sidebar-types.html` im Browser öffnen → zur Typ-5-Sektion scrollen. Der leere Zustand soll sichtbar sein: gedämpfter Text mit Mauspfeil-Icon links. Kein Hover-Effekt beim Darüberfahren. Kein Fehler in der Konsole.

- [ ] **Schritt 4: Commit**

```bash
git add components/sidebar-types.html
git commit -m "feat: add result-empty demo to Typ 5 sidebar-types reference"
```

---

## Task 3: Dokumentation in `docs/sidebar-types.md` erweitern

**Files:**
- Modify: `docs/sidebar-types.md` — Typ-5-Abschnitt (aktuell Zeile 203–232)

- [ ] **Schritt 1: Leerzustand-Abschnitt im Typ-5-Kapitel ergänzen**

Nach der bestehenden **Regeln**-Liste in Typ 5 (nach "Klick auf ganzes Item → Zoom auf Karte, Item wird `.active`") diesen Block einfügen:

```markdown
**Leerzustand:**

Wenn noch keine Ergebnisse vorliegen, `.result-empty` anstelle der `.result-list` anzeigen:

```html
<div class="result-empty">
  <i class="fa-solid fa-arrow-pointer"></i>
  Klicke auf einen Punkt in der Karte, um die 5 nächsten NAH-Stützpunkte zu berechnen.
</div>
```

- Icon optional — FontAwesome, Auswahl site-spezifisch (z.B. `fa-arrow-pointer` für Desktop-Hinweis)
- Kein Hover, kein Klick — rein informativer Zustand
- Text frei wählbar je nach Anwendungsfall
```

- [ ] **Schritt 2: Änderungshistorie aktualisieren**

In der Tabelle am Ende von `docs/sidebar-types.md` eine Zeile hinzufügen:

```markdown
| 2026-04-30 | Typ 5: `.result-empty` Leerzustand ergänzt |
```

- [ ] **Schritt 3: Commit**

```bash
git add docs/sidebar-types.md
git commit -m "docs: document result-empty empty state for Typ 5 sidebar"
```

---

## Task 4: Abschlusskontrolle

- [ ] **Schritt 1: Spec-Abgleich**

Spec `docs/superpowers/specs/2026-04-30-typ5-empty-state-design.md` durchgehen:
- `.result-empty` + `.result-empty i` in `sidebar.css` ✓ (Task 1)
- HTML-Beispiel in `sidebar-types.html` ✓ (Task 2)
- Dokumentation in `sidebar-types.md` ✓ (Task 3)
- Keine hardcodierten Farben — nur `var(--muted)` und `opacity` ✓

- [ ] **Schritt 2: Pre-change Checklist aus CLAUDE.md**

```
☐ css/common.css bleibt Source of Truth (keine Tokens geändert)
☐ Keine hardcodierten Farben oder z-index Werte
☐ Keine Produktionsseite verwendet css/demo.css
☐ Bestehende Komponenten wiederverwendet
☐ Neue Komponente dokumentiert
☐ Kein Pfad unbeabsichtigt geändert
```

- [ ] **Schritt 3: Final-Check im Browser**

`components/sidebar-types.html` öffnen → Typ-5-Sektion:
1. Ergebnis-Liste rendert unverändert
2. Leerzustand-Panel zeigt Icon + Text, gedämpft, kein Hover-Effekt

# Attribution-Bereinigung + Landing Page Footer — Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Custom `.map-attribution`-CSS entfernen (native MapLibre/Leaflet-Attribution verwenden) und Typ-5-Landing-Page durch definierte `.page-footer`-Komponente vervollständigen.

**Architecture:** Reine CSS- und Doku-Änderungen in drei Dateien. `css/page.css` verliert den Attribution-Block und gewinnt den Footer-Block. `docs/page-types.md` und `components/page-types.html` werden synchron aktualisiert. CHANGELOG bekommt einen v2.0.0-Eintrag (Breaking Change: `.map-attribution*` entfernt).

**Tech Stack:** CSS Custom Properties, HTML

---

## Dateikarte

| Datei | Aktion | Inhalt |
|---|---|---|
| `css/page.css` | Modify | Attribution-Block (Zeilen 469–528) entfernen; `.page-footer`-Block nach Zeile 339 einfügen |
| `docs/page-types.md` | Modify | Typ-5-Abschnitt: Footer als Pflicht; Karten-Sonderfall: kein `.map-attribution` mehr; Regeltabelle ergänzen |
| `components/page-types.html` | Modify | Footer-CSS in `<style>`-Block; Footer-HTML im Typ-5-Demo |
| `CHANGELOG.md` | Modify | v2.0.0-Eintrag mit Breaking/Added |

---

## Task 1: Attribution-Block aus `css/page.css` entfernen

**Files:**
- Modify: `css/page.css:469–528`

- [ ] **Schritt 1: Lies `css/page.css` ab Zeile 465**

Stelle sicher dass du den richtigen Block siehst: er beginnt mit dem Kommentar `/* ═══ KARTEN-ATTRIBUTION` und endet mit `.maplibregl-ctrl-attrib { display: none !important; }` (die letzte Zeile der Datei).

- [ ] **Schritt 2: Den gesamten Attribution-Block entfernen**

Entferne exakt diesen Block (Zeilen 469–528 inklusive der Leerzeile davor):

```css
/* ═══════════════════════════════════════
   KARTEN-ATTRIBUTION
   Pflicht-Block auf allen Karten-Seiten.
   Position: unten rechts in der Karte.
   ⓘ-Button öffnet vollständiges Copyright-Modal.
   ═══════════════════════════════════════ */
.map-attribution {
  position: absolute;
  bottom: 0;
  right: 0;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(26,26,26,0.85);
  backdrop-filter: blur(4px);
  padding: 3px 8px;
  font-size: 0.68rem;
  color: var(--muted);
  z-index: var(--z-content);
  border-top-left-radius: 4px;
}
.map-attribution a {
  color: var(--muted);
  text-decoration: none;
  transition: color var(--transition-fast);
}
.map-attribution a:hover { color: var(--text); }

.map-attribution-sep {
  color: var(--subtle);
  user-select: none;
}

/* ⓘ Info-Button öffnet Copyright-Modal */
.map-attribution-info {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 1px solid var(--subtle);
  background: transparent;
  color: var(--subtle);
  font-size: 0.6rem;
  cursor: pointer;
  font-family: inherit;
  transition: color var(--transition-fast), border-color var(--transition-fast);
  flex-shrink: 0;
  line-height: 1;
}
.map-attribution-info:hover {
  color: var(--muted);
  border-color: var(--muted);
}

/* Leaflet/MapLibre eigene Attribution ausblenden wenn .map-attribution verwendet wird
   (verhindert doppelte Attribution) */
.leaflet-control-attribution { display: none !important; }
.maplibregl-ctrl-attrib       { display: none !important; }
```

Nach dem Entfernen endet `css/page.css` mit dem Status-Dot-Block:
```css
.status-dot.on    { background: var(--success); box-shadow: 0 0 4px var(--success); }
.status-dot.warn  { background: var(--warning); box-shadow: 0 0 4px rgba(234,179,8,0.5); }
.status-dot.off   { background: var(--danger);  box-shadow: 0 0 4px rgba(239,68,68,0.5); }
```

- [ ] **Schritt 3: Prüfen**

```bash
grep -n "map-attribution\|leaflet-control-attribution\|maplibregl-ctrl-attrib" /root/git/oe5ith-ci/css/page.css
```

Erwartetes Ergebnis: keine Ausgabe (alle drei Klassen vollständig entfernt).

- [ ] **Schritt 4: Commit**

```bash
git add css/page.css
git commit -m "feat!: remove .map-attribution CSS, use native MapLibre/Leaflet attribution"
```

---

## Task 2: `.page-footer`-Block in `css/page.css` ergänzen

**Files:**
- Modify: `css/page.css` — nach Zeile 339 (nach dem `@media (max-width: 768px)`-Block des Landing-Abschnitts)

- [ ] **Schritt 1: Lies `css/page.css` ab Zeile 336**

Du siehst:
```css
@media (max-width: 768px) {
  .landing-body { padding: 40px 16px 24px; }
  .landing-title { font-size: 1.5rem; }
}

/* ═══════════════════════════════════════
   ERGEBNIS-LISTE
```

- [ ] **Schritt 2: Footer-Block zwischen dem Landing-`@media`-Block und dem ERGEBNIS-LISTE-Kommentar einfügen**

Der vollständige einzufügende Block:

```css

/* ── PAGE FOOTER ── */
.page-footer {
  width: 100%;
  border-top: 1px solid var(--border);
  padding: 14px 0 0;
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  font-size: 0.72rem;
  color: var(--subtle);
}

.page-footer-version {
  font-family: var(--font-mono);
  color: var(--subtle);
}

.page-footer-copy {
  color: var(--subtle);
}

.page-footer-links {
  display: flex;
  gap: 12px;
}

.page-footer-links a {
  color: var(--muted);
  text-decoration: none;
  transition: color var(--transition-fast);
}
.page-footer-links a:hover { color: var(--text); }
```

- [ ] **Schritt 3: Prüfen**

```bash
grep -n "page-footer" /root/git/oe5ith-ci/css/page.css
```

Erwartetes Ergebnis: 6–7 Treffer für `.page-footer`, `.page-footer-version`, `.page-footer-copy`, `.page-footer-links`.

- [ ] **Schritt 4: Commit**

```bash
git add css/page.css
git commit -m "feat: add .page-footer component to page.css"
```

---

## Task 3: `docs/page-types.md` aktualisieren

**Files:**
- Modify: `docs/page-types.md`

Lies die Datei zuerst vollständig. Es gibt drei Stellen die geändert werden müssen.

- [ ] **Schritt 1: Typ-5-Abschnitt — Footer als Pflicht dokumentieren**

Den Abschnitt `## Typ 5 — Landing Page` suchen. Die **Struktur**-Box ersetzen:

Vorher:
```markdown
**Struktur:**
```
Topbar
└── landing-body (zentriert)
    ├── landing-title            ← "Willkommen im Cloud Portal"
    ├── card-grid                ← Navigation-Cards (Typ 1 aus cards.css)
    └── Footer (optional)        ← Versioninfo, Copyright
```
```

Nachher:
```markdown
**Struktur:**
```
Topbar
└── landing-body (zentriert)
    ├── landing-title            ← "Willkommen im Cloud Portal"
    ├── card-grid                ← Navigation-Cards (Typ 1 aus cards.css)
    └── page-footer              ← Version · Copyright · Links (Pflicht)
        ├── page-footer-version  ← CI-Version, z.B. "CI v2.0.0"
        ├── page-footer-copy     ← "© 2026 OE5ITH"
        └── page-footer-links    ← Impressum, Datenschutz
```
```

Die **Merkmale**-Liste um einen Punkt ergänzen (nach "Disabled-Cards für noch nicht verfügbare Bereiche"):
```markdown
- `.page-footer` mit Version, Copyright-Text und Links ist **Pflicht** — kein optionaler Baustein
```

- [ ] **Schritt 2: Karten-Sonderfall — `.map-attribution`-Verweis entfernen**

Im Abschnitt `## Karten-Seite (Sonderfall)` unter **Besonderheiten** diese Zeile entfernen:
```markdown
- Leaflet/MapLibre CSS-Overrides aus `modal.css` aktivieren
```

Und durch folgendes ersetzen:
```markdown
- Native MapLibre/Leaflet-Attribution bleibt aktiv (kein CSS-Override nötig)
- `.sidebar-footer-copyright`-Button für weiterführende Lizenzinfos nutzen
```

- [ ] **Schritt 3: Regeltabelle ergänzen**

Nach dem Karten-Sonderfall-Abschnitt und vor `## Schnellreferenz` eine neue Tabelle einfügen:

```markdown
## Footer- und Copyright-Regeln

| Seitentyp | Sidebar | Copyright-Anzeige |
|---|---|---|
| Typ 1–4 | Pflicht | Sidebar-Footer: Version + `.sidebar-footer-copyright`-Button |
| Typ 5 — Startseite | Nicht vorhanden | `.page-footer` mit Version, Copyright-Text, Links |
| Karten-Sonderfall | Pflicht (auch wenn leer) | Sidebar-Footer + native MapLibre/Leaflet-Attribution |

---
```

- [ ] **Schritt 4: Änderungshistorie ergänzen**

In der Tabelle am Ende eine neue Zeile oben einfügen:
```markdown
| 2026-05-07 | `.map-attribution`-Verweis entfernt (Breaking: v2.0.0). `.page-footer` als Pflichtbaustein für Typ 5 dokumentiert. Footer/Copyright-Regeltabelle ergänzt. |
```

- [ ] **Schritt 5: Commit**

```bash
git add docs/page-types.md
git commit -m "docs: update page-types for footer rules and native map attribution"
```

---

## Task 4: `components/page-types.html` — Footer-Demo ergänzen

**Files:**
- Modify: `components/page-types.html`

Lies die Datei zuerst. Der Typ-5-Abschnitt beginnt um Zeile 597 mit `<!-- ═══ TYP 5: LANDING ═══ -->`.

- [ ] **Schritt 1: Footer-CSS in den `<style>`-Block der HTML-Datei einfügen**

Im `<style>`-Block der Datei (im `<head>`) nach der `.m-landing`/`.m-landing-title`-Definition folgenden CSS-Block ergänzen:

```css
.m-footer {
  width: 100%;
  border-top: 1px solid var(--border);
  padding-top: 10px;
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
  font-size: 0.65rem;
  color: var(--subtle);
}
.m-footer-links { display: flex; gap: 10px; }
.m-footer-links a { color: var(--muted); text-decoration: none; }
.m-footer-links a:hover { color: var(--text); }
```

- [ ] **Schritt 2: Footer-HTML im Typ-5-Demo einfügen**

Im Typ-5-Demo-Block das schließende `</div>` der `.m-landing`-Card-Grid direkt vor dem schließenden `</div>` von `.m-landing` ergänzen. Die Stelle:

Vorher (ca. Zeile 633–634):
```html
      </div>
    </div>
  </div>
```

Nachher:
```html
      </div>
      <div class="m-footer">
        <span style="font-family:monospace;color:var(--subtle)">CI v2.0.0</span>
        <span>© 2026 OE5ITH</span>
        <div class="m-footer-links">
          <a href="#">Impressum</a>
          <a href="#">Datenschutz</a>
        </div>
      </div>
    </div>
  </div>
```

- [ ] **Schritt 3: Annotation aktualisieren**

Die Annotation unter dem Typ-5-Demo (ca. Zeile 636–639) anpassen:

Vorher:
```html
  <p class="annotation">
    Kein <code>.layout</code>, kein Sidebar. <code>.landing-body</code> mit <code>padding-top: 60px</code>.
    Nav-Cards (Typ 1 aus cards.css). Disabled-Cards für zukünftige Bereiche.
  </p>
```

Nachher:
```html
  <p class="annotation">
    Kein <code>.layout</code>, keine Sidebar. <code>.landing-body</code> mit <code>padding-top: 60px</code>.
    Nav-Cards (Typ 1 aus cards.css). Disabled-Cards für zukünftige Bereiche.
    <code>.page-footer</code> mit Version, Copyright und Links ist <strong>Pflicht</strong> auf jeder Startseite.
    <code>margin-top: auto</code> drückt den Footer ans Ende von <code>.landing-body</code>.
  </p>
```

- [ ] **Schritt 4: Visuell prüfen**

`components/page-types.html` im Browser öffnen. Zum Typ-5-Abschnitt scrollen. Der Demo-Block muss zeigen:
- Topbar + zentrierte Nav-Cards (3 Kacheln)
- Fußzeile mit `CI v2.0.0` links, `© 2026 OE5ITH` Mitte, `Impressum` und `Datenschutz` rechts
- `border-top` trennt Footer von Cards

- [ ] **Schritt 5: Commit**

```bash
git add components/page-types.html
git commit -m "feat: add page-footer demo to page-types.html Typ 5"
```

---

## Task 5: `CHANGELOG.md` — v2.0.0 anlegen

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Schritt 1: Aktuellen letzten Tag prüfen**

```bash
git tag --sort=-version:refname | head -5
```

Erwartetes Ergebnis: `v1.6.1` ist der letzte Tag → v2.0.0 ist korrekt.

- [ ] **Schritt 2: v2.0.0-Block ganz oben in die Versionsliste einfügen**

Direkt nach dem Datei-Header (vor dem ersten `## v`-Block) einfügen:

```markdown
## v2.0.0 - 2026-05-07

### Breaking

- `css/page.css`: `.map-attribution`, `.map-attribution-sep`, `.map-attribution-info`
  entfernt. Sites die diese Klassen verwenden müssen das `.map-attribution`-HTML-Element
  entfernen und native MapLibre/Leaflet-Attribution aktivieren.
- `css/page.css`: Hide-Regeln `.leaflet-control-attribution` und `.maplibregl-ctrl-attrib`
  entfernt. Native Attribution wird jetzt im Standard-Stil der jeweiligen Bibliothek
  angezeigt.

### Added

- `css/page.css`: `.page-footer`, `.page-footer-version`, `.page-footer-copy`,
  `.page-footer-links` — Fußzeilen-Komponente für Typ-5-Startseiten (ohne Sidebar).
  Enthält Version, Copyright-Text und Linkliste (Impressum, Datenschutz etc.).

---
```

- [ ] **Schritt 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "chore: update CHANGELOG.md for v2.0.0"
```

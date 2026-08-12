# Disclosure (Single-Panel) — Design / Spec

**Datum:** 2026-07-06
**Status:** Freigegeben · zur Umsetzung
**Angefragt von:** website-v3 (Routing-Sidebar, A→B-Turn-by-Turn-Anweisungen)
**Version:** additiv → MINOR `v1.19.0`

Quelle: `ci-routing-disclosure-request.md` (Anforderung, extern in
website-v3 gepflegt). Dieses Dokument ist die freigegebene, technisch
geklärte Design-Spec.

---

## 1. Zweck

Generische, wiederverwendbare CI-Komponente für ein **einzelnes
auf-/zuklappbares Panel** ohne Auswahlzustand: eine klickbare Kopfzeile mit
optionalem Zähler, die einen Inhaltsbereich auf-/zuklappt.

**Abgrenzung zu `.accordion`:** `.accordion` bleibt zuständig für
Layer-Toggle-**Gruppen** mit Dot, Status-Badge, Checkbox-Liste,
Gruppen-Controls und JS-gesteuerter `max-height`-Berechnung. `.disclosure`
hat keinen Auswahlzustand, keine Checkboxen, keine Gruppen-Controls und
**kein JS für Auf-/Zu** — das native `<details>`-Element übernimmt das.

Erster Einsatz: website-v3 Routing-Sidebar (Turn-by-Turn-Wegbeschreibung
nach A→B-Routenberechnung). Künftig auch für andere aufklappbare
Detail-Listen.

---

## 2. HTML-Struktur

Nativ auf `<details>`/`<summary>` aufgebaut (barrierefrei per Default,
kein eigenes JS nötig, entspricht dem ARIA-APG-Disclosure-Pattern):

```html
<details class="disclosure">
  <summary class="disclosure-header">
    <span class="disclosure-title">Wegbeschreibung</span>
    <span class="disclosure-count badge badge-gray">18 Schritte</span>
    <i class="fa-solid fa-chevron-down disclosure-chevron"></i>
  </summary>
  <div class="disclosure-body">
    <div class="disclosure-item">
      <span class="disclosure-item-text">Head northeast on Untere Donauländer, B129</span>
      <span class="disclosure-item-meta">280 m</span>
    </div>
    <!-- … -->
  </div>
</details>
```

---

## 3. Klassen-Spezifikation

| Klasse | Zweck / Regeln |
|---|---|
| `.disclosure` | Wrapper (`<details>`). Kein eigener Rahmen zwingend nötig — fügt sich in bestehende Panel-Kontexte (`.result-container` u.ä.) ein. |
| `.disclosure-header` | `<summary>`. Flex-Row: Titel · Zähler · Chevron, `gap`, `cursor:pointer`. Hover-BG `var(--surface-hover)`. `list-style:none` + `::-webkit-details-marker{display:none}` (nativer Marker entfernt, Chevron übernimmt die Optik). Fokus-Ring nativ über `<summary>`, sichtbar (kein `outline:none`). |
| `.disclosure-title` | Primärtext, `--text`. |
| `.disclosure-count` | Sekundärinfo — **reuse `.badge`** (keine neue Badge-Variante), z.B. `.badge` mit Default-Farbe. |
| `.disclosure-chevron` | Rotiert bei offenem `<details>`: `details[open] .disclosure-chevron{ transform:rotate(180deg) }`, Transition nur am Chevron (`--transition-base`), analog `.acc-chevron`-Optik. |
| `.disclosure-body` | Inhaltscontainer. **Kein JS-Höhen-Contract** — `<details>` blendet nativ ein/aus, keine `max-height`-Transition nötig (zentraler Unterschied zu `.accordion`). |
| `.disclosure-item` | Einzelner Eintrag. Flex-Row: Text · Meta (rechts). |
| `.disclosure-item-text` | Primärtext, `--text`, `flex:1`, `min-width:0`. |
| `.disclosure-item-meta` | Sekundärtext rechts, `--muted`, klein, `flex-shrink:0`; `.mono` optional zusätzlich bei Zahlen. |

---

## 4. Tokens

**Keine neuen Tokens.** Nur Reuse bestehender:

| Token | Verwendung |
|---|---|
| `--text` | Primärtext (Titel, Item-Text) |
| `--muted` | Sekundärtext (Item-Meta) |
| `--border` | Trennlinie Header/Body falls nötig |
| `--transition-base` | Chevron-Rotation |
| `--surface-hover` | Hover-BG `.disclosure-header` (rgba 0.05 — Entscheidung: bestehenden Token reusen statt den hardcodierten `.acc-header`-Wert 0.03 zu kopieren oder einen neuen Token einzuführen) |

`.disclosure-count` erbt Farbe/Radius/Padding vollständig von `.badge`
(`badges.css`) — keine eigene Deklaration.

---

## 5. Accessibility & Motion

- Tastaturbedienbar über native `<summary>`-Fokussierbarkeit — kein
  zusätzliches `tabindex` nötig.
- `@media (prefers-reduced-motion: reduce)`: Chevron-Transition
  deaktivieren.

---

## 6. Referenz-Komponente

`components/disclosure.html` (mit `css/demo.css` wie andere
Referenzseiten):

1. Zwei `<details class="disclosure">` nebeneinander — eines geschlossen,
   eines mit `open`-Attribut.
2. Mehrere `.disclosure-item` mit unterschiedlich langem Text
   (Ellipsis-Verhalten falls relevant).
3. `.disclosure` eingebettet in einen `.panel`/`.panel-body`-Kontext
   (`page.css`), damit sichtbar ist, wie es sich in bestehende
   Sidebar-Panels einfügt. (`.result-container` aus der website-v3-Anfrage
   existiert im `oe5ith-ci`-Repo nicht — `.panel` ist die reale,
   wiederverwendbare CI-Klasse für Panel-Kontexte.)

---

## 7. Doku-/Registry-/Versions-Updates

- `css/disclosure.css` — neue Datei.
- `css/index.css` — `@import "disclosure.css";` (nach `sidebar.css`, da
  fachlich zur Sidebar gehört).
- `docs/sidebar.md` — neuer Abschnitt „Disclosure (Single-Panel)" mit
  Abgrenzungstabelle „wann Accordion / wann Disclosure verwenden".
- `docs/registry.json` — **kein neuer Top-Level-Eintrag**: bestehenden
  `sidebar`-Eintrag erweitern (`css` um `disclosure.css`, `html` um
  `disclosure.html`), da die Komponente Teil der Sidebar-Doku ist, nicht
  einer eigenen Doku-Datei. `python3 scripts/cli/check_consistency.py`
  muss grün sein.
- `CHANGELOG.md` — `Added`-Eintrag (additiv, nicht breaking).
- Version: MINOR `v1.19.0`.

---

## 8. Akzeptanzkriterien

- [ ] `.disclosure` basiert auf nativem `<details>`/`<summary>` — kein JS für Auf-/Zuklappen.
- [ ] Chevron rotiert bei `details[open]`, analog `.acc-chevron`-Optik.
- [ ] Tastaturbedienbar (native Fokussierbarkeit reicht), Fokus-Ring sichtbar.
- [ ] `::marker`/`::-webkit-details-marker` entfernt, Chevron übernimmt die Optik.
- [ ] `.disclosure-count` nutzt `.badge`, keine neue Badge-Variante.
- [ ] Hover-BG nutzt `--surface-hover`, keine hardcodierte rgba.
- [ ] Keine hardcodierten Farben/Radien/Z-Index/Transitions — nur Tokens.
- [ ] Reduced-Motion respektiert.
- [ ] `css/demo.css` nur in `components/disclosure.html`, nicht produktiv.
- [ ] Referenz-HTML, `docs/sidebar.md`, `registry.json` (sidebar-Eintrag erweitert), `CHANGELOG.md` aktualisiert; `check_consistency.py` grün.

# Split View (Master-Detail)

**CSS:** `css/split.css`  
**Referenz:** `components/split-view.html`  
**Seitentyp:** Typ 6 — Master-Detail  
**Status:** definiert · v1.14

---

## Überblick

Pattern für Seiten, die eine scrollbare Auswahlliste (Master) und einen abhängigen
Detailbereich (Detail) nebeneinander darstellen. Beide Spalten scrollen unabhängig
voneinander — die Seite selbst scrollt nicht mehr.

Typische Anwendungsfälle: Log-Explorer, Ressourcenlisten mit Detailansicht, Alarm-/
Event-Listen, Geräteverwaltung.

**Wann verwenden:**
- Inhalt ist eine selektierbare Liste, deren Auswahl einen Detailbereich füllt.
- Master-Liste und Detailbereich haben inhärent unterschiedliche Scroll-Längen.
- Der Nutzer wechselt häufig zwischen Einträgen, ohne die Seite neu zu laden.

**Wann nicht verwenden:**
- Einfache Detail-Seite ohne Auswahlliste → Typ 1 (`.panel`-Stapel).
- Alle Inhalte sollen gemeinsam gescrollt werden → kein Split-View.
- Map-Seiten → eigenes Layout (kein `css/page.css`).

---

## Höhen- und Scroll-Modell

Split View aktiviert einen **Fixed-Height-Modus automatisch** — ohne zusätzliche
Klassen am Seiten-Wrapper. Sobald `.split-view` im DOM vorhanden ist, greift in
`css/split.css` ein `:has(.split-view)`-Selektor, der `.page-content` auf
`overflow: hidden` setzt und `.content-body` auf `flex: 1; min-height: 0;`.

Dadurch nehmen Master und Detail die verbleibende Viewport-Höhe vollständig ein
und scrollen jeweils intern. `css/common.css` und `css/page.css` bleiben unverändert.

---

## Element-Tabelle (G1)

| Element / Klasse | Zweck | Pflicht/Optional | Erlaubte Modifier |
|---|---|---|---|
| `.split-view` | Flex-Container für Master und Detail, nimmt volle Höhe ein | Pflicht | — |
| `.split-master` | Linke Spalte — schmale, scrollbare Auswahlliste | Pflicht | — |
| `.split-master-header` | Optionaler Header der Master-Spalte (Titel, Aktions-Buttons) | Optional | — |
| `.split-master-body` | Scrollbarer Listenbereich innerhalb von `.split-master` | Pflicht | — |
| `.split-item` | Einzelner Listeneintrag; als `<button>` oder `<a>` | Pflicht (1–n) | `.active` |
| `.split-item-label` | Primäres Beschriftungs-Element im Item; kürzt mit Ellipsis | Pflicht | — |
| `.split-item-meta` | Sekundäre Metadaten im Item (Zeit, Zähler u. ä.) | Optional | — |
| `.split-detail` | Rechte Spalte — scrollbarer Detailbereich | Pflicht | — |
| `.status-dot` | Status-Indikator (aus `css/page.css`); steht als erstes Kind im `.split-item` | Optional | `.on`, `.warn`, `.off` |

---

## Struktur / Verschachtelung (G2)

```text
.content-body
└── .split-view
    ├── .split-master                  (Pflicht — <aside> empfohlen)
    │   ├── .split-master-header       (Optional)
    │   │   ├── [Titel / .ci-label]
    │   │   └── [Aktions-Buttons]      (letztes Kind → margin-left: auto)
    │   └── .split-master-body         (Pflicht)
    │       └── .split-item            (Pflicht, 1–n — <button> oder <a>)
    │           ├── .status-dot [.on|.warn|.off]  (Optional — immer erstes Kind)
    │           ├── .split-item-label  (Pflicht)
    │           └── .split-item-meta   (Optional)
    └── .split-detail                  (Pflicht — <section> empfohlen)
        └── [beliebige .panel-Elemente, .ci-table, etc.]
```

---

## Reihenfolge & Platzierung (G3)

- `.split-view` ist das **einzige direkte Kind** von `.content-body`. Kein anderes
  Element darf auf gleicher Ebene stehen, da der Fixed-Height-Modus exklusiv wirkt.
- `.split-master` kommt **vor** `.split-detail` im DOM (links vor rechts).
- Innerhalb jedes `.split-item` steht `.status-dot` **zuerst**, gefolgt von
  `.split-item-label` und optional `.split-item-meta`.
- `.split-master-header` ist **optional**, aber wenn vorhanden, steht es **vor**
  `.split-master-body`.
- `.split-master-body` ist **immer erforderlich** — ohne ihn scrollen die Items nicht.
- Das letzte Kind in `.split-master-header` erhält automatisch `margin-left: auto`
  und wird rechtsbündig ausgerichtet.

---

## Zustände & Varianten (G4)

| Zustand / Variante | Klasse / Modifier | Wann verwenden |
|---|---|---|
| Aktiv / ausgewählt | `.split-item.active` | Aktuell ausgewählter Eintrag; linker Akzentstreifen + subtile Hintergrundfarbe |
| Hover | `:hover` (automatisch) | Mauszustand — kein zusätzliches Markup nötig |
| Tastaturfokus | `:focus-visible` (automatisch) | Sichtbarer Outline (`var(--accent-border)`) bei Tastaturnavigation |
| Status OK | `.status-dot.on` | Dienst läuft / kein Fehler |
| Status Warnung | `.status-dot.warn` | Degradierter Betrieb / Warnung |
| Status Offline | `.status-dot.off` | Dienst nicht erreichbar / ausgefallen |
| Mobile gestapelt | automatisch ab ≤ 768 px | Master wird auf volle Breite + `max-height` begrenzt, Detail darunter |
| Reduzierte Bewegung | automatisch (`prefers-reduced-motion`) | Hover-Transition auf `.split-item` wird deaktiviert |

---

## Tokens

| Token | Standardwert | Verwendung |
|---|---|---|
| `--split-master-width` | `300px` | Breite der Master-Spalte auf Desktop |
| `--split-master-max-h` | `320px` | Maximale Höhe der Master-Spalte im gestapelten Mobile-Layout |

Beide Tokens sind in `css/common.css` definiert und können dort oder per
CSS-Override in der Seite angepasst werden.

---

## Vollständiges HTML-Beispiel

```html
<div class="content-body">
  <div class="split-view">

    <!-- MASTER -->
    <aside class="split-master">
      <div class="split-master-header">
        <span class="ci-label">Quellen</span>
        <button class="btn btn-sm btn-ghost" title="Aktualisieren">
          <i class="fa-solid fa-rotate"></i>
        </button>
      </div>
      <div class="split-master-body">

        <button class="split-item active">
          <span class="status-dot on"></span>
          <span class="split-item-label">nginx error (default)</span>
          <span class="split-item-meta">2m</span>
        </button>

        <button class="split-item">
          <span class="status-dot warn"></span>
          <span class="split-item-label">PostgreSQL 17 (main)</span>
          <span class="split-item-meta">12s</span>
        </button>

        <button class="split-item">
          <span class="status-dot off"></span>
          <span class="split-item-label">systemd / sshd</span>
          <span class="split-item-meta">4h</span>
        </button>

      </div>
    </aside>

    <!-- DETAIL -->
    <section class="split-detail">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <i class="fa-solid fa-filter"></i> Filter
          </div>
        </div>
        <div class="panel-body">
          <div class="form-row">
            <div class="form-field">
              <label class="form-label">Suche</label>
              <input class="form-input" type="text" placeholder="Volltext…">
            </div>
            <div class="form-field">
              <label class="form-label">Level</label>
              <select class="form-select">
                <option>Alle</option>
                <option>ERROR</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</div>
```

---

## Regeln

1. **Nur Tokens verwenden** — keine hartcodierten Farben, Radien oder Z-Index-Werte.
2. **`.status-dot` wiederverwenden** — die drei Klassen `.on`, `.warn`, `.off` kommen
   aus `css/page.css`. Keine neue Dot-Variante erfinden.
3. **`.split-detail` braucht `min-width: 0`** — dies ist bereits in `css/split.css`
   gesetzt und verhindert, dass lange Tabellen- oder Log-Zeilen das Flex-Layout sprengen.
   Diese Eigenschaft nicht entfernen.
4. **`.split-item` als `<button>` oder `<a>`** — nie als `<div>`. Nur so sind
   Tastaturnavigation und Fokus-Styles korrekt.
5. **Kein `css/demo.css`** in Produktionsseiten — nur in `components/`.

---

## CSS einbinden

```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/page.css">
<link rel="stylesheet" href="css/split.css">
```

Oder alles auf einmal über `css/index.css`.

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-06-18 | Initiale Definition. Split View (Typ 6), G1–G4, Tokens, Fixed-Height-Modell. |

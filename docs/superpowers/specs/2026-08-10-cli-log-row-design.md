# CLI — Strukturierte Datenzeilen (`log_row`) — Design / Spec

**Datum:** 2026-08-10
**Status:** Freigegeben · zur Umsetzung
**Angefragt von:** pocsag-decoder (`hampager.sh`, externes Projekt außerhalb
dieses Repos), das POCSAG-Meldungen als fixbreite Spaltenzeilen im Terminal
ausgibt und dafür eine CI-konforme, wiederverwendbare Formatierung braucht.
**Version:** additiv → MINOR

Betroffene Dateien: `scripts/cli/utils.sh`, `scripts/cli/utils.py`,
`docs/cli.md`.

---

## 1. Zweck

`docs/cli.md` definiert bisher nur **Status-Zeilen** (`log_header`,
`log_step`, `log_info`, `log_success`, `log_warn`, `log_error`, `log_auth`,
`log_debug`, `log_sep`) — jede Funktion gibt genau eine semantisch gefärbte
Meldung aus.

Ein zweiter, bisher nicht abgedeckter Anwendungsfall ist die **strukturierte
Datenzeile**: mehrere Werte in festen, ausgerichteten Spalten mit einheitlichem
Trennzeichen, wie sie z. B. ein POCSAG-Decoder pro empfangener Nachricht
ausgibt:

```
POCSAG1200 | RIC     208 | F3 | Zeit lokal (Swissphone)          | 2026-08-10 10:58:00 Lokalzeit
POCSAG1200 | RIC    4520 | F3 | Rubrik 80 (APRS-WX) #1           | 0828z OE5XFR/Frauenmarkt: 26.7C w: 4m/s=228deg h: 35% hPa: 1020 r: 0mm/h
```

Ohne CI-Definition baut sich jedes Script seine eigene `printf`-Breitenlogik
— das ist genau die Art von lokaler Sonderlösung, die `for-coding-agents.md`
vermeiden will. `log_row` schließt diese Lücke als neue, generische Funktion
in `utils.sh`/`utils.py`, dokumentiert in `docs/cli.md`.

**Abgrenzung zu den Status-Funktionen:** `log_row` hat keine Farbe und kein
festes Symbol — sie liefert reine Struktur (Trennzeichen, Padding,
Ausrichtung). Statuslogik (Farbe je Ereignistyp) bleibt Aufgabe des Callers,
der einzelne Spaltenwerte bei Bedarf selbst mit den bestehenden `C_*`-Farben
umschließt, bevor er sie an `log_row` übergibt.

---

## 2. Spalten-Modell

`log_row` ist generisch: beliebig viele Spalten, Breite und Ausrichtung
werden bei jedem Aufruf mitgegeben — kein festes Schema wie "RIC, Func,
Label, Value". Damit ist die Funktion für jeden CLI-Anwendungsfall nutzbar,
nicht nur für POCSAG-artige Logs.

Jede Spalte außer der letzten wird als Compact-String übergeben:

```
"wert:align:breite"
```

- `align` ∈ `{l, r}` (linksbündig / rechtsbündig)
- `breite` = Zielbreite in Zeichen (Padding-Ziel, kein Hard-Limit)

Die **letzte Spalte ist immer ein roher String** ohne Spezifikation — kein
Padding, läuft bis Zeilenende. Grund: Freitext-Werte (z. B. POCSAG-Nachrichten)
enthalten selbst Doppelpunkte (`26.7C w: 4m/s=228deg h: 35%`), was das
`wert:align:breite`-Parsing brechen würde, wenn diese Spalte mitspezifiziert
werden müsste.

Trennzeichen zwischen allen Spalten ist fix `" | "` (Leerzeichen-Pipe-
Leerzeichen) — CI-weiter Standard, nicht pro Aufruf konfigurierbar.

### Beispiel

```bash
log_row "POCSAG1200:l:11" "RIC $ric:r:7" "$func:l:2" "$label:l:34" "$value"
```

```python
log_row("POCSAG1200:l:11", f"RIC {ric}:r:7", f"{func}:l:2", f"{label}:l:34", value)
```

Ergebnis:

```
POCSAG1200 |    RIC 208 | F3 | Zeit lokal (Swissphone)          | 2026-08-10 10:58:00 Lokalzeit
```

---

## 3. Padding, Ausrichtung, Overflow

- `l` → linksbündig, mit Leerzeichen auf `breite` aufgefüllt.
  Bash: `printf "%-${breite}s" "$wert"`. Python: `f"{wert:<{breite}}"`.
- `r` → rechtsbündig. Bash: `printf "%${breite}s" "$wert"`.
  Python: `f"{wert:>{breite}}"`.
- Ist `wert` länger als `breite`: **kein** Abschneiden. Die Spalte wächst über
  die Zielbreite hinaus, nachfolgende Spalten verschieben sich in dieser einen
  Zeile optisch. Vollständigkeit der Log-Daten hat Vorrang vor perfekter
  Spaltentreue.
- Ungültiges `align`-Token (nicht `l`/`r`): Funktion bricht die Zeile ab und
  meldet den Fehler über `log_error` (Bash: `return 1`, Python:
  `raise ValueError`), statt still einen Default anzunehmen.

### Bekannte Einschränkung — Mehrbyte-Zeichen

Labels mit Umlauten (`Niederöst.`, `Kärnten`, `Oberösterr.`) können je nach
Bash-/Terminal-Umgebung die Padding-Breite um 1–2 Spalten verfälschen, da
`printf` nicht in jeder Umgebung Terminal-Anzeigebreite statt Byte-/
Zeichenanzahl zählt. Das ist rein kosmetisch (kein Datenverlust) und wird
hier bewusst nicht technisch gelöst (keine `wcwidth`-Implementierung) — für
ein Logging-Utility wäre das überdimensioniert. Wird in `docs/cli.md` als
dokumentierte Einschränkung festgehalten.

---

## 4. Implementierung

### Bash (`scripts/cli/utils.sh`)

```bash
# Strukturierte Datenzeile mit festem Trennzeichen " | ".
# Jede Spalte außer der letzten: "wert:align:breite" (align = l|r).
# Letzte Spalte: roher String, kein Padding.
log_row() {
    local n=$#
    local out=""
    local i spec val align width
    for ((i = 1; i < n; i++)); do
        spec="${!i}"
        IFS=':' read -r val align width <<< "$spec"
        case "$align" in
            l) out+="$(printf "%-${width}s" "$val")" ;;
            r) out+="$(printf "%${width}s" "$val")" ;;
            *)
                log_error "log_row: ungültiges align '$align' in Spec '$spec'"
                return 1
                ;;
        esac
        out+=" | "
    done
    out+="${!n}"
    echo -e "$out"
}
```

### Python (`scripts/cli/utils.py`)

```python
def log_row(*cols: str) -> None:
    """Strukturierte Datenzeile mit festem Trennzeichen ' | '.
    Jede Spalte außer der letzten: 'wert:align:breite' (align = l|r).
    Letzte Spalte: roher String, kein Padding."""
    parts = []
    for spec in cols[:-1]:
        val, align, width = spec.rsplit(":", 2)
        width = int(width)
        if align == "l":
            parts.append(f"{val:<{width}}")
        elif align == "r":
            parts.append(f"{val:>{width}}")
        else:
            raise ValueError(f"log_row: ungültiges align '{align}' in Spec '{spec}'")
    parts.append(cols[-1])
    print(" | ".join(parts))
```

Kein Farbparameter, keine Symbol-Konstante — bewusst minimal, analog zur
Entscheidung in Abschnitt 1.

---

## 5. Dokumentation

`docs/cli.md` bekommt einen neuen Abschnitt „Strukturierte Datenzeilen"
(nach dem bestehenden „Funktionen"-Abschnitt, vor „Verwendung — Bash"):

- Syntax-Erklärung (`wert:align:breite`, letzte Spalte roh)
- Das POCSAG-Beispiel aus Abschnitt 1 dieser Spec als Referenzbeispiel
- Regeln: Trennzeichen fix, kein Truncation, Unicode-Einschränkung,
  Fehlerverhalten bei ungültigem `align`
- Neuer Eintrag in der Änderungshistorie-Tabelle:
  `2026-08-10 | log_row ergänzt (Bash + Python) — strukturierte
  Datenzeilen mit festem Trennzeichen " | ", generisches Spalten-Modell.`

`docs/tokens.md` ist nicht betroffen — `log_row` führt keine neuen Farb-Tokens
ein.

---

## 6. Tests

Keine neue Testinfrastruktur. `utils.sh`/`utils.py` haben aktuell keine
Testsuite (nur `check_consistency.py` hat eine, über
`test_check_consistency.py`). `log_row` wird manuell anhand des realen
POCSAG-Beispiels verifiziert: Ausgabe von `log_row` mit den Beispielwerten
aus Abschnitt 1 wird visuell mit dem tatsächlichen Terminal-Log aus
`hampager.sh` verglichen.

---

## 7. Versionierung

Additive Ergänzung (neue Funktion, keine Breaking Changes an bestehenden
`log_*`-Funktionen) → **MINOR**-Release. `CHANGELOG.md` bekommt einen
`Added`-Eintrag; Tag folgt gemäß `CLAUDE.md`-Versionierungsregeln nach
Umsetzung.

---

## 8. Registry

`docs/registry.json`-Eintrag `"cli"` (Kategorie `concept`) bleibt unverändert
— `log_row` ist eine Ergänzung der bestehenden Dateien `utils.sh`/`utils.py`/
`cli.md`, keine neue Komponente, kein neuer Registry-Eintrag nötig.

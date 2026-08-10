# CLI log_row Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a generic `log_row` function to `scripts/cli/utils.sh` and `scripts/cli/utils.py` for structured, column-aligned CLI data rows (e.g. POCSAG decoder logs), and document it in `docs/cli.md`.

**Architecture:** `log_row` is a variadic function. Every argument except the last is a compact spec string `"wert:align:breite"` (`align` = `l`/`r`); the last argument is always a raw, unpadded string. All columns are joined with the fixed separator `" | "`. No color, no truncation — pure structural formatting, consistent between the Bash and Python implementations.

**Tech Stack:** Bash (builtin `printf`/`read`), Python 3 stdlib only.

## Global Constraints

- Separator between all columns is fixed `" | "` — never configurable per call. (Spec §2)
- The last argument passed to `log_row` is always a raw string with no `:align:width` spec and no padding. (Spec §2)
- `align` accepts only `l` (left) or `r` (right); any other value is an error — the row is aborted, not silently defaulted. (Spec §3)
- If a value is longer than its target width, it is never truncated — the column grows and later columns visually shift in that one row. (Spec §3)
- `log_row` has no color parameter and no symbol — callers wrap individual values with existing `C_*` variables themselves if color is needed. (Spec §1, §4)
- No new test infrastructure (no pytest/bats suite) — verify manually against the real POCSAG example from the spec. (Spec §6)
- No new CI tokens, no new `docs/registry.json` entry — this extends existing files (`utils.sh`, `utils.py`, `cli.md`), it is not a new component. (Spec §5, §8)
- This is an additive MINOR change — no breaking changes to existing `log_*` functions. (Spec §7)

---

### Task 1: Add `log_row` to `scripts/cli/utils.sh`

**Files:**
- Modify: `scripts/cli/utils.sh` (add function after `log_sep`, i.e. after line 107)
- Verify with: `/tmp/claude-0/-root-git-oe5ith-ci/89ae54c4-5529-41db-a1cf-1b42182f89f4/scratchpad/verify_log_row.sh` (scratch verification script, not committed)

**Interfaces:**
- Produces: `log_row` (Bash function) — variadic, last arg raw string, all prior args `"wert:align:breite"`. Prints the joined row to stdout via `printf '%b%s\n'`. Returns 1 and calls `log_error` if any non-last spec has an invalid `align` token.

- [ ] **Step 1: Add the `log_row` function to `scripts/cli/utils.sh`**

Append after the existing `log_sep` function (currently ends at line 107):

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
    printf '%b%s\n' "$out" "${!n}"
}
```

**Note (post-Task-1-review fix):** the original plan draft used `out+="${!n}"; echo -e "$out"`. Task 1's review caught that `echo -e` interprets backslash escapes (`\n`, `\t`, `\c`) in the raw last column too — which can silently truncate free-text values (e.g. POCSAG messages) containing a stray backslash, violating the "never truncate" rule in Global Constraints. `printf '%b%s\n' "$out" "${!n}"` keeps escape interpretation (for optional `C_*` coloring) scoped to the structural columns in `$out` only; the raw last column via `%s` is never escape-interpreted. This is the corrected, authoritative version of Step 1 — implement this, not the version any earlier commit message may reference.

- [ ] **Step 2: Write a scratch verification script**

Create `/tmp/claude-0/-root-git-oe5ith-ci/89ae54c4-5529-41db-a1cf-1b42182f89f4/scratchpad/verify_log_row.sh`:

```bash
#!/bin/bash
source "/root/git/oe5ith-ci/scripts/cli/utils.sh"

echo "--- Zeile 1 (Zeit lokal) ---"
log_row "POCSAG1200:l:11" "RIC 208:r:12" "F3:l:2" "Zeit lokal (Swissphone):l:34" "2026-08-10 10:58:00 Lokalzeit"

echo "--- Zeile 2 (Freitext mit Doppelpunkten) ---"
log_row "POCSAG1200:l:11" "RIC 4520:r:12" "F3:l:2" "Rubrik 80 (APRS-WX) #1:l:34" "0828z OE5XFR/Frauenmarkt: 26.7C w: 4m/s=228deg h: 35% hPa: 1020 r: 0mm/h"

echo "--- Zeile 3 (überlanger Wert, kein Truncation) ---"
log_row "POCSAG1200:l:11" "RIC 2023023:r:7" "F3:l:2" "Alpha:l:34" "Host UNREACHABLE alert for oe3xsa.esx1"

echo "--- Zeile 4 (ungültiges align -> Fehler) ---"
log_row "X:c:5" "letzte Spalte"
echo "Exit-Code: $?"
```

- [ ] **Step 3: Run the verification script**

Run: `bash /tmp/claude-0/-root-git-oe5ith-ci/89ae54c4-5529-41db-a1cf-1b42182f89f4/scratchpad/verify_log_row.sh`

Expected:
- Zeile 1 output: `POCSAG1200` padded left to 11 chars (1 trailing space) + ` | ` + `RIC 208` padded right to 12 chars (5 leading spaces) + ` | ` + `F3` (already exactly 2 chars, no padding) + ` | ` + the 23-char label padded left to 34 chars (11 trailing spaces) + ` | ` + the raw local-time string, unpadded.
- Zeile 2 output: the full free-text value (including its internal colons) appears intact and unmangled as the last column.
- Zeile 3 output: `RIC 2023023` (11 chars) exceeds its width-7 spec but prints in full, not truncated; the row still terminates correctly with the `Alpha`/message columns after it.
- Zeile 4 output: a `log_error`-formatted red `✖` message about invalid align `'c'`, and `Exit-Code: 1`.

**Copy the literal Zeile 1 output line from this run** — you'll paste it into `docs/cli.md` in Task 3 (do not hand-type it there; use exactly what this script prints, so the doc matches shipped behavior).

If any of these don't match, fix `log_row` in `utils.sh` before proceeding.

- [ ] **Step 4: Commit**

```bash
git add scripts/cli/utils.sh
git commit -m "$(cat <<'EOF'
feat(cli): add log_row for structured Bash log rows

Generic column formatter with fixed " | " separator, per-column
left/right alignment, and a raw last column for free-text values
that may contain colons (e.g. POCSAG decoder message logs).

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Add `log_row` to `scripts/cli/utils.py`

**Files:**
- Modify: `scripts/cli/utils.py` (add function after `get_rel_path`, i.e. after line 90)
- Verify with: `/tmp/claude-0/-root-git-oe5ith-ci/89ae54c4-5529-41db-a1cf-1b42182f89f4/scratchpad/verify_log_row.py` (scratch verification script, not committed)

**Interfaces:**
- Consumes: nothing from Task 1 (parallel, independent implementation of the same spec).
- Produces: `log_row(*cols: str) -> None` (Python function) — variadic, last arg raw string, all prior args `"wert:align:breite"`. Prints the joined row via `print()`. Raises `ValueError` if any non-last spec has an invalid `align` token.

- [ ] **Step 1: Add the `log_row` function to `scripts/cli/utils.py`**

Append after the existing `get_rel_path` function (currently ends at line 90):

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

- [ ] **Step 2: Write a scratch verification script**

Create `/tmp/claude-0/-root-git-oe5ith-ci/89ae54c4-5529-41db-a1cf-1b42182f89f4/scratchpad/verify_log_row.py`:

```python
import sys
sys.path.insert(0, "/root/git/oe5ith-ci/scripts/cli")
from utils import log_row

print("--- Zeile 1 (Zeit lokal) ---")
log_row("POCSAG1200:l:11", "RIC 208:r:12", "F3:l:2", "Zeit lokal (Swissphone):l:34", "2026-08-10 10:58:00 Lokalzeit")

print("--- Zeile 2 (Freitext mit Doppelpunkten) ---")
log_row("POCSAG1200:l:11", "RIC 4520:r:12", "F3:l:2", "Rubrik 80 (APRS-WX) #1:l:34", "0828z OE5XFR/Frauenmarkt: 26.7C w: 4m/s=228deg h: 35% hPa: 1020 r: 0mm/h")

print("--- Zeile 3 (überlanger Wert, kein Truncation) ---")
log_row("POCSAG1200:l:11", "RIC 2023023:r:7", "F3:l:2", "Alpha:l:34", "Host UNREACHABLE alert for oe3xsa.esx1")

print("--- Zeile 4 (ungültiges align -> ValueError) ---")
try:
    log_row("X:c:5", "letzte Spalte")
    print("FEHLER: keine Exception ausgelöst")
except ValueError as e:
    print(f"OK, ValueError: {e}")
```

- [ ] **Step 3: Run the verification script**

Run: `python3 /tmp/claude-0/-root-git-oe5ith-ci/89ae54c4-5529-41db-a1cf-1b42182f89f4/scratchpad/verify_log_row.py`

Expected:
- Zeile 1 output: byte-for-byte identical to Task 1's Bash `log_row` output for the same inputs — same padding rules (left-pad `POCSAG1200` to 11, right-pad `RIC 208` to 12, `F3` unpadded at width 2, left-pad the 23-char label to 34), both implementations must agree.
- Zeile 2 output: free-text value with internal colons intact.
- Zeile 3 output: `RIC 2023023` not truncated.
- Zeile 4 output: `OK, ValueError: log_row: ungültiges align 'c' in Spec 'X:c:5'`.

**Compare this run's Zeile 1 output character-by-character against the line you copied from Task 1 Step 3.** If they differ, one of the two implementations has a padding bug — fix it before proceeding (both must match; this is the cross-implementation consistency check for this task).

If any of these don't match, fix `log_row` in `utils.py` before proceeding.

- [ ] **Step 4: Commit**

```bash
git add scripts/cli/utils.py
git commit -m "$(cat <<'EOF'
feat(cli): add log_row for structured Python log rows

Same contract as the Bash log_row added in scripts/cli/utils.sh:
fixed " | " separator, per-column left/right alignment via
"wert:align:breite", raw unpadded last column for free-text values.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Document `log_row` and update the changelog

**Files:**
- Modify: `docs/cli.md` (new section + Funktionen table row + Änderungshistorie row)
- Modify: `CHANGELOG.md` (repo root) — entry under `## [Unreleased]`

**Interfaces:**
- Consumes: the finalized `log_row` behavior from Task 1 and Task 2 (must document the actual shipped signature and rules, not the spec draft).
- Produces: nothing consumed by later tasks — this is the last task in the plan.

- [ ] **Step 1: Add `log_row` to the Funktionen table in `docs/cli.md`**

In `docs/cli.md`, the `## Funktionen` table currently ends with the `log_sep` row (line 44):

```markdown
| `log_sep` | Dim | `  ───` | Trennlinie |
```

Add a new row directly after it:

```markdown
| `log_sep` | Dim | `  ───` | Trennlinie |
| `log_row` | keine (farblos) | keine | Strukturierte Datenzeile, siehe eigener Abschnitt unten |
```

- [ ] **Step 2: Add a new "Strukturierte Datenzeilen" section to `docs/cli.md`**

Insert this new section directly after the `## Funktionen` table and before `## Verwendung — Bash`:

```markdown
---

## Strukturierte Datenzeilen

`log_row` deckt einen zweiten Anwendungsfall ab: mehrere Werte in festen,
ausgerichteten Spalten mit einheitlichem Trennzeichen — z. B. für
Decoder-Logs, die pro Ereignis eine Zeile mit mehreren Feldern ausgeben
(Beispiel: POCSAG-Pager-Decoder).

**Trennzeichen** zwischen allen Spalten ist immer fix `" | "` — nicht pro
Aufruf konfigurierbar.

**Syntax:** Jede Spalte außer der letzten wird als Compact-String
`"wert:align:breite"` übergeben (`align` = `l` linksbündig oder `r`
rechtsbündig, `breite` = Padding-Zielbreite in Zeichen). Die **letzte
Spalte ist immer ein roher String** ohne Spezifikation, ohne Padding —
das erlaubt Freitext-Werte, die selbst Doppelpunkte enthalten.

```bash
log_row "POCSAG1200:l:11" "RIC 208:r:12" "F3:l:2" "Zeit lokal (Swissphone):l:34" "2026-08-10 10:58:00 Lokalzeit"
```

```python
log_row("POCSAG1200:l:11", "RIC 208:r:12", "F3:l:2", "Zeit lokal (Swissphone):l:34", "2026-08-10 10:58:00 Lokalzeit")
```

**Ausgabe:**

Paste the exact "Zeile 1" line captured in Task 1 Step 3 (and cross-checked against Task 2 Step 3) into a fenced code block here — do not hand-type it. The separator's own leading/trailing space combines with column padding, so the real spacing around each `|` is wider than it looks at a glance; only the actual script output is authoritative.

**Regeln:**

1. Ist ein Wert länger als seine `breite`: **kein Abschneiden** — die
   Spalte wächst über die Zielbreite hinaus, nachfolgende Spalten
   verschieben sich in dieser einen Zeile optisch. Vollständigkeit der
   Log-Daten hat Vorrang vor perfekter Spaltentreue.
2. Ungültiges `align`-Token (nicht `l`/`r`): Die Zeile wird abgebrochen
   und der Fehler über `log_error` gemeldet (Bash: `return 1`, Python:
   `ValueError`) — kein stiller Default.
3. `log_row` hat keine Farbe und kein Symbol. Wenn eine Zeile farblich
   hervorgehoben werden soll, umschließt der Aufrufer den jeweiligen
   Spaltenwert selbst mit den bestehenden `C_*`-Variablen, bevor er ihn
   an `log_row` übergibt.
4. **Bekannte Einschränkung:** Labels mit Umlauten (`Niederöst.`,
   `Kärnten`, `Oberösterr.`) können je nach Bash-/Terminal-Umgebung die
   Padding-Breite um 1–2 Spalten verfälschen, da `printf` nicht überall
   Terminal-Anzeigebreite statt Byte-/Zeichenanzahl zählt. Rein
   kosmetisch, kein Datenverlust.
5. **Einschränkung:** `wert` in Spalten außer der letzten darf keinen
   Doppelpunkt enthalten. Die Bash- und Python-Implementierung parsen
   `"wert:align:breite"` aus unterschiedlichen Richtungen (Bash von
   links, Python von rechts) — ein Doppelpunkt im Wert einer
   Nicht-letzten Spalte führt zu unterschiedlichem Verhalten zwischen
   beiden Implementierungen. In der letzten Spalte (roher String) sind
   Doppelpunkte dagegen unproblematisch.

---
```

- [ ] **Step 3: Add an Änderungshistorie row in `docs/cli.md`**

The `## Änderungshistorie` table currently has one row (line 109):

```markdown
| 2026-04-22 | Initiale Definition. Farben auf CI-Tokens gemappt. `log_auth` und `log_sep` neu. `require_cmd` in Bash ergänzt. |
```

Add a new row after it (newest last, matching the existing oldest-first order used elsewhere in this repo's changelogs):

```markdown
| 2026-04-22 | Initiale Definition. Farben auf CI-Tokens gemappt. `log_auth` und `log_sep` neu. `require_cmd` in Bash ergänzt. |
| 2026-08-10 | `log_row` ergänzt (Bash + Python) — strukturierte Datenzeilen mit festem Trennzeichen `" | "`, generisches Spalten-Modell, letzte Spalte roh für Freitext-Werte. |
```

- [ ] **Step 4: Add a CHANGELOG.md entry**

In `CHANGELOG.md` (repo root), the `## [Unreleased]` section is currently empty (lines 7-9):

```markdown
## [Unreleased]

---
```

Replace with:

```markdown
## [Unreleased]

### Added
- **`log_row`** (`scripts/cli/utils.sh`, `scripts/cli/utils.py`) — strukturierte, spaltenausgerichtete CLI-Log-Zeilen mit festem Trennzeichen `" | "`. Generisches Spalten-Modell (`"wert:align:breite"`), letzte Spalte immer roher String für Freitext-Werte mit Doppelpunkten. Dokumentiert in `docs/cli.md`.

---
```

- [ ] **Step 5: Run the consistency check**

Run: `python3 /root/git/oe5ith-ci/scripts/cli/check_consistency.py`

Expected: exits without errors (this task doesn't touch `docs/registry.json`, so the existing `cli` entry stays valid — this just confirms nothing else was broken).

- [ ] **Step 6: Commit**

```bash
git add docs/cli.md CHANGELOG.md
git commit -m "$(cat <<'EOF'
docs(cli): document log_row structured data rows

Adds the "Strukturierte Datenzeilen" section to docs/cli.md and a
CHANGELOG.md entry for the log_row function added in the prior two
commits.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## After This Plan

Versioning per `CLAUDE.md`: this is an additive MINOR change. Tagging
(`git tag -a v1.24.0 -m "Release v1.24.0"` + `git push origin v1.24.0`) is
a separate, deliberate release action — not part of this plan. Decide
with the user whether to tag now or bundle with other pending
`[Unreleased]` work first.

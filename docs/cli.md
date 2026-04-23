# CLI — Terminal Erscheinungsbild

**Dateien:** `scripts/cli/utils.sh` · `scripts/cli/utils.py`  
**Status:** definiert · v1.0

---

## Überblick

Alle Shell- und Python-Scripts verwenden dieselben Logging-Funktionen
für ein einheitliches Terminal-Erscheinungsbild.
Die Farben sind direkt auf die CI Design Tokens gemappt.

---

## Farb-Mapping

| CI Token | Hex | ANSI | Verwendung |
|---|---|---|---|
| `--accent` | `#3b82f6` | `\033[1;34m` Blau | Header, Info |
| `--success` | `#22c55e` | `\033[1;32m` Grün | Erfolg, OK |
| `--warning` | `#eab308` | `\033[1;33m` Gelb | Warnung |
| `--danger` | `#ef4444` | `\033[1;31m` Rot | Fehler, kritisch |
| `--auth` | `#a78bfa` | `\033[1;35m` Lila | Auth/Security |
| `--muted` | `#888888` | `\033[2m` Dim | Debug, sekundär |

> ANSI-Farben sind Näherungen — Terminals rendern sie unterschiedlich.
> Die Semantik (Blau = Info, Grün = OK, etc.) bleibt konsistent.

---

## Funktionen

| Funktion | Farbe | Symbol | Verwendung |
|---|---|---|---|
| `log_header` | Blau + Bold | `▶▶▶` | Beginn eines neuen Abschnitts |
| `log_step` | Bold | `[n/m]` | Nummerierter Schritt |
| `log_info` | Blau | `  ℹ` | Allgemeine Information |
| `log_success` | Grün | `  ✔` | Aktion erfolgreich |
| `log_warn` | Gelb | `  ⚠` | Warnung, nicht kritisch |
| `log_error` | Rot | `  ✖` | Fehler, Script ggf. abbrechen |
| `log_auth` | Lila | `  ℹ` | Auth/Security-Ereignis |
| `log_debug` | Dim | `  ·` | Debug — nur wenn `DEBUG=1` |
| `log_sep` | Dim | `  ───` | Trennlinie |

---

## Verwendung — Bash

```bash
source "$(dirname "$0")/utils.sh"

log_header  "Deploy starten"
log_step    1 3 "common.css kopieren..."
log_success "common.css → /var/www/karte/assets/"
log_step    2 3 "Nginx reload..."
log_warn    "Nginx: reload dauert länger als erwartet"
log_step    3 3 "Health-Check..."
log_error   "Health-Check fehlgeschlagen — Port 8080 nicht erreichbar"
log_sep
log_debug   "Response: HTTP 503"
```

**Ausgabe:**

```
▶▶▶ Deploy starten
[1/3] common.css kopieren...
  ✔ common.css → /var/www/karte/assets/
[2/3] Nginx reload...
  ⚠ Nginx: reload dauert länger als erwartet
[3/3] Health-Check...
  ✖ Health-Check fehlgeschlagen — Port 8080 nicht erreichbar
  ─────────────────────────────────
```

---

## Verwendung — Python

```python
from utils import log_header, log_step, log_info, log_success, log_warn, log_error, log_sep

log_header("Overpass Import")
log_step(1, 4, "OSM-Datei prüfen...")
log_info("Dateigröße: 1.2 GB")
log_success("Datei OK")
log_step(2, 4, "Import starten...")
log_warn("Importzeit kann > 30 min betragen")
log_sep()
```

---

## Regeln

1. `log_header` nur einmal pro Script-Abschnitt — nicht für jeden Schritt
2. `log_error` bei kritischen Fehlern, danach `exit 1` (Bash) oder `sys.exit(1)` (Python)
3. `log_warn` nur wenn eine Aktion trotzdem weiterläuft
4. `log_auth` für alle Authentik/SSO/Token-Ereignisse — nie `log_info`
5. `log_debug` für Diagnose-Output — immer hinter `DEBUG=1` Guard

---

## Änderungshistorie

| Datum | Änderung |
|---|---|
| 2026-04-22 | Initiale Definition. Farben auf CI-Tokens gemappt. `log_auth` und `log_sep` neu. `require_cmd` in Bash ergänzt. |

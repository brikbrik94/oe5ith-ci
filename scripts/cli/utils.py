# ═══════════════════════════════════════════════════════════
#  OE5ITH CI — CLI Utils (Python)
#  Einheitliches Terminal-Erscheinungsbild für alle Scripts.
#
#  Farb-Mapping → CI Design Tokens:
#    Accent  (#3b82f6)  → C_BLUE    (Infos, Header)
#    Success (#22c55e)  → C_GREEN   (Erfolg, OK)
#    Warning (#eab308)  → C_YELLOW  (Warnungen)
#    Danger  (#ef4444)  → C_RED     (Fehler, kritisch)
#    Auth    (#a78bfa)  → C_PURPLE  (Auth/Security)
#    Muted   (#888888)  → C_DIM     (sekundäre Infos, Debug)
#
#  Verwendung:
#    from scripts.cli.utils import log_info, log_success, ...
#    # oder direkt:
#    import sys; sys.path.insert(0, "scripts/cli"); from utils import *
# ═══════════════════════════════════════════════════════════

import os

# ── FARBEN ──────────────────────────────────────────────────
C_RESET  = "\033[0m"
C_BOLD   = "\033[1m"
C_DIM    = "\033[2m"

# CI-Token-Mapping (ANSI-Näherung)
C_BLUE   = "\033[1;34m"    # --accent       #3b82f6
C_GREEN  = "\033[1;32m"    # --success      #22c55e
C_YELLOW = "\033[1;33m"    # --warning      #eab308
C_RED    = "\033[1;31m"    # --danger       #ef4444
C_PURPLE = "\033[1;35m"    # --auth         #a78bfa
C_CYAN   = "\033[0;36m"    # --code-text    #4ade80 (Näherung)

# ── SYMBOLE ─────────────────────────────────────────────────
S_HEADER  = "▶▶▶"
S_STEP    = "  ▶"
S_INFO    = "  ℹ"
S_SUCCESS = "  ✔"
S_WARN    = "  ⚠"
S_ERROR   = "  ✖"
S_DEBUG   = "  ·"

# ── LOGGING ─────────────────────────────────────────────────

def log_header(msg: str) -> None:
    """Großer Abschnitts-Header (--accent blau)."""
    print(f"\n{C_BLUE}{C_BOLD}{S_HEADER} {msg}{C_RESET}")

def log_step(current: int, total: int, msg: str) -> None:
    """Nummerierter Schritt innerhalb einer Gruppe."""
    print(f"{C_BOLD}[{current}/{total}]{C_RESET} {msg}")

def log_info(msg: str) -> None:
    """Allgemeine Info (--accent blau)."""
    print(f"{C_BLUE}{S_INFO}{C_RESET} {msg}")

def log_success(msg: str) -> None:
    """Erfolgreich abgeschlossen (--success grün)."""
    print(f"{C_GREEN}{S_SUCCESS}{C_RESET} {msg}")

def log_warn(msg: str) -> None:
    """Warnung, nicht kritisch (--warning gelb)."""
    print(f"{C_YELLOW}{S_WARN}{C_RESET} {msg}")

def log_error(msg: str) -> None:
    """Fehler, kritisch (--danger rot)."""
    print(f"{C_RED}{S_ERROR}{C_RESET} {msg}")

def log_auth(msg: str) -> None:
    """Auth/Security-Ereignis (--auth lila)."""
    print(f"{C_PURPLE}{S_INFO}{C_RESET} {msg}")

def log_debug(msg: str) -> None:
    """Debug-Ausgabe — nur wenn DEBUG=1 gesetzt (--muted gedimmt)."""
    if os.environ.get("DEBUG", "0") == "1":
        print(f"{C_DIM}{S_DEBUG} [debug] {msg}{C_RESET}")

# ── HELPER ──────────────────────────────────────────────────

def log_sep() -> None:
    """Trennlinie (--border, gedimmt)."""
    print(f"{C_DIM}  ─────────────────────────────────{C_RESET}")

def get_rel_path(full_path: str, root_path: str) -> str:
    """Relativen Pfad zurückgeben (relativ zu root_path)."""
    full_path = full_path.rstrip("/")
    root_path = root_path.rstrip("/")
    if full_path.startswith(root_path + "/"):
        return full_path[len(root_path) + 1:]
    return full_path

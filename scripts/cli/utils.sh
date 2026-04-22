#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  OE5ITH CI — CLI Utils (Bash)
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
#    source "$(dirname "$0")/utils.sh"
# ═══════════════════════════════════════════════════════════

# ── FARBEN ──────────────────────────────────────────────────
C_RESET="\033[0m"
C_BOLD="\033[1m"
C_DIM="\033[2m"

# CI-Token-Mapping (ANSI-Näherung)
C_BLUE="\033[1;34m"     # --accent       #3b82f6
C_GREEN="\033[1;32m"    # --success      #22c55e
C_YELLOW="\033[1;33m"   # --warning      #eab308
C_RED="\033[1;31m"      # --danger       #ef4444
C_PURPLE="\033[1;35m"   # --auth         #a78bfa
C_CYAN="\033[0;36m"     # --code-text    #4ade80 (Näherung)

# ── SYMBOLE ─────────────────────────────────────────────────
S_HEADER="▶▶▶"
S_STEP="  ▶"
S_INFO="  ℹ"
S_SUCCESS="  ✔"
S_WARN="  ⚠"
S_ERROR="  ✖"
S_DEBUG="  ·"

# ── LOGGING ─────────────────────────────────────────────────

# Großer Abschnitts-Header (--accent blau)
log_header() {
    echo -e "\n${C_BLUE}${C_BOLD}${S_HEADER} $1${C_RESET}"
}

# Schritt innerhalb einer Gruppe
log_step() {
    local current=$1
    local total=$2
    local msg=$3
    echo -e "${C_BOLD}[${current}/${total}]${C_RESET} ${msg}"
}

# Allgemeine Info (--accent blau)
log_info() {
    echo -e "${C_BLUE}${S_INFO}${C_RESET} $1"
}

# Erfolgreich abgeschlossen (--success grün)
log_success() {
    echo -e "${C_GREEN}${S_SUCCESS}${C_RESET} $1"
}

# Warnung, nicht kritisch (--warning gelb)
log_warn() {
    echo -e "${C_YELLOW}${S_WARN}${C_RESET} $1"
}

# Fehler, kritisch (--danger rot)
log_error() {
    echo -e "${C_RED}${S_ERROR}${C_RESET} $1"
}

# Auth/Security-Ereignis (--auth lila)
log_auth() {
    echo -e "${C_PURPLE}${S_INFO}${C_RESET} $1"
}

# Debug — nur wenn DEBUG=1 (--muted gedimmt)
log_debug() {
    if [[ "${DEBUG:-0}" == "1" ]]; then
        echo -e "${C_DIM}${S_DEBUG} [debug] $1${C_RESET}"
    fi
}

# ── HELPER ──────────────────────────────────────────────────

# Relativen Pfad ausgeben (relativ zu einem Root-Verzeichnis)
get_rel_path() {
    local full_path="$1"
    local root_path="$2"
    echo "${full_path#$root_path/}"
}

# Prüfen ob Befehl verfügbar ist
require_cmd() {
    if ! command -v "$1" &>/dev/null; then
        log_error "Befehl nicht gefunden: $1"
        exit 1
    fi
}

# Trennlinie (--border #333, gedimmt)
log_sep() {
    echo -e "${C_DIM}  ─────────────────────────────────${C_RESET}"
}

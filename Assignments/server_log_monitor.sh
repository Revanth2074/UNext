#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${LOG_DIR:-$SCRIPT_DIR/logs}"
REPORT_DIR="${REPORT_DIR:-$SCRIPT_DIR/reports}"
SCRIPT_LOG="${SCRIPT_LOG:-$SCRIPT_DIR/script_logs/script_execution.log}"
DATE="$(date +%Y-%m-%d)"
REPORT_FILE="$REPORT_DIR/daily_report_$DATE.txt"

mkdir -p "$LOG_DIR" "$REPORT_DIR" "$(dirname "$SCRIPT_LOG")"

write_log() {
  local level="$1"
  local msg="$2"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $msg" >> "$SCRIPT_LOG"
}

clean_line() {
  local line="$1"
  line="$(echo "$line" | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')"
  line="$(echo "$line" | tr '\t' ' ' )"
  echo "$line"
}

check_directory() {
  if [ ! -d "$LOG_DIR" ]; then
    write_log "ERROR" "Log directory not found: $LOG_DIR"
    echo "Log directory not found: $LOG_DIR"
    exit 1
  fi

  local log_files=("$LOG_DIR"/*.log)
  if [ ! -e "${log_files[0]}" ]; then
    write_log "ERROR" "No .log files found in $LOG_DIR"
    echo "No .log files found in $LOG_DIR"
    exit 1
  fi

  for log_file in "$LOG_DIR"/*.log; do
    [ -e "$log_file" ] || continue
    if [ ! -r "$log_file" ]; then
      write_log "ERROR" "Unreadable log file: $log_file"
      echo "Unreadable log file: $log_file"
      exit 1
    fi
  done
}

process_log_file() {
  local log_file="$1"
  local server_name
  server_name=$(basename "$log_file" .log)

  local info_count warn_count error_count
  info_count=$(awk '$3=="INFO" {count++} END {print count+0}' "$log_file")
  warn_count=$(awk '$3=="WARNING" {count++} END {print count+0}' "$log_file")
  error_count=$(awk '$3=="ERROR" {count++} END {print count+0}' "$log_file")

  local status
  if [ "$error_count" -gt 10 ]; then
    status="CRITICAL"
  elif [ "$warn_count" -gt 20 ]; then
    status="WARNING"
  else
    status="NORMAL"
  fi

  echo "$server_name $info_count $warn_count $error_count $status"
}

generate_report() {
  : > "$REPORT_FILE"
  echo "Daily Server Health Report" >> "$REPORT_FILE"
  echo "Generated: $(date)" >> "$REPORT_FILE"
  echo "Server INFO WARNING ERROR STATUS" >> "$REPORT_FILE"

  for log_file in "$LOG_DIR"/*.log; do
    [ -e "$log_file" ] || continue
    local result
    result=$(process_log_file "$log_file")
    local server_name info_count warn_count error_count status
    read -r server_name info_count warn_count error_count status <<< "$result"
    echo "$server_name $info_count $warn_count $error_count $status" >> "$REPORT_FILE"
  done

  echo "Report written to $REPORT_FILE"
}

show_menu() {
  while true; do
    echo "1. Analyze logs"
    echo "2. Generate report"
    echo "3. View report"
    echo "4. Exit"
    read -p "Select [1-4]: " choice

    case "$choice" in
      1)
        write_log "INFO" "Manual log analysis requested"
        check_directory
        for log_file in "$LOG_DIR"/*.log; do
          [ -e "$log_file" ] || continue
          while IFS= read -r line; do
            cleaned=$(clean_line "$line")
            echo "$cleaned"
          done < "$log_file"
        done
        ;;
      2)
        write_log "INFO" "Report generation requested"
        check_directory
        generate_report
        ;;
      3)
        if [ -f "$REPORT_FILE" ]; then
          cat "$REPORT_FILE"
        else
          echo "No report generated yet"
        fi
        ;;
      4)
        exit 0
        ;;
      *)
        echo "Invalid selection"
        ;;
    esac
  done
}

main() {
  write_log "INFO" "Script started"
  check_directory

  if [ "${1:-}" = "--menu" ]; then
    show_menu
  else
    generate_report
  fi

  write_log "INFO" "Script completed"
}

main "$@"

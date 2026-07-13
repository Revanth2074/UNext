#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORDER_DIR="${ORDER_DIR:-$SCRIPT_DIR/orders}"
REPORT_DIR="${REPORT_DIR:-$SCRIPT_DIR/reports}"
ALERT_LOG="${ALERT_LOG:-$SCRIPT_DIR/alert_logs/alert_log.txt}"
DATE="$(date +%Y-%m-%d)"
REPORT_FILE="$REPORT_DIR/sales_$DATE.csv"

mkdir -p "$ORDER_DIR" "$REPORT_DIR" "$(dirname "$ALERT_LOG")"

write_alert() {
  local level="$1"
  local message="$2"
  echo "$(date '+%Y-%m-%d %H:%M:%S') [$level] $message" >> "$ALERT_LOG"
}

format_currency() {
  local value="$1"
  local whole="${value%.*}"
  local cents="00"

  if [[ "$value" == *.* ]]; then
    cents="${value##*.}"
    if [ ${#cents} -lt 2 ]; then
      cents="${cents}0"
    fi
  fi

  whole="${whole//,/}"
  if [[ "$whole" =~ ^[0-9]+$ ]]; then
    whole=$(printf "%'d" "$whole")
  fi

  echo "₹$whole.$cents"
}

validate_files() {
  if [ ! -d "$ORDER_DIR" ]; then
    write_alert "ERROR" "Order directory not found: $ORDER_DIR"
    echo "Order directory not found: $ORDER_DIR"
    exit 1
  fi

  local csv_files=("$ORDER_DIR"/*.csv)
  if [ ! -e "${csv_files[0]}" ]; then
    write_alert "ERROR" "No CSV files found in $ORDER_DIR"
    echo "No CSV files found in $ORDER_DIR"
    exit 1
  fi

  for csv_file in "$ORDER_DIR"/*.csv; do
    [ -e "$csv_file" ] || continue
    if [ ! -s "$csv_file" ]; then
      write_alert "ERROR" "Empty CSV file detected: $csv_file"
      echo "Empty CSV file detected: $csv_file"
      exit 1
    fi
  done
}

process_store() {
  local csv_file="$1"
  local store_name
  store_name=$(basename "$csv_file" .csv)

  local failed_count pending_count refund_count
  failed_count=$(grep -E '^[^,]+,[^,]+,FAILED,' "$csv_file" | wc -l | tr -d ' ')
  pending_count=$(grep -E '^[^,]+,[^,]+,PENDING,' "$csv_file" | wc -l | tr -d ' ')
  refund_count=$(grep -E '^[^,]+,[^,]+,REFUNDED,' "$csv_file" | wc -l | tr -d ' ')

  local completed_rows
  completed_rows=$(grep -E '^[^,]+,[^,]+,COMPLETED,' "$csv_file" || true)

  local revenue total avg
  revenue=$(echo "$completed_rows" | awk -F',' '{sum += $5} END {printf "%.2f", sum+0}')
  total=$(awk -F',' 'NR>1 {count++} END {print count+0}' "$csv_file")
  avg=$(awk -F',' 'NR>1 {sum += $5; count++} END {if (count>0) printf "%.2f", sum/count; else print "0.00"}' "$csv_file")

  local amounts top_orders
  amounts=$(echo "$completed_rows" | cut -d',' -f5 | sort -nr)
  top_orders=$(echo "$completed_rows" | sort -t',' -k5,5nr | head -n 5)

  local status
  if [ "$failed_count" -gt 30 ]; then
    status="CRITICAL"
    write_alert "ALERT" "$store_name has $failed_count failed orders"
  elif [ "$refund_count" -gt 20 ]; then
    status="WARNING"
    write_alert "WARNING" "$store_name has $refund_count refunded orders"
  else
    status="OK"
    write_alert "INFO" "$store_name status is OK"
  fi

  echo "Store: $store_name"
  echo "Failed: $failed_count | Pending: $pending_count | Refunded: $refund_count"
  echo "Revenue: $(format_currency "$revenue") | Orders: $total | Avg: $(format_currency "$avg")"
  echo "Top completed orders:"
  echo "$top_orders"

  echo "$store_name,$(format_currency "$revenue"),$total,$failed_count,$status"
}

generate_csv() {
  echo "Store/Category,Revenue,Orders,Failed,STATUS" > "$REPORT_FILE"

  for csv_file in "$ORDER_DIR"/*.csv; do
    [ -e "$csv_file" ] || continue

    local row
    row=$(process_store "$csv_file")
    local store_name revenue orders failed status
    IFS=',' read -r store_name revenue orders failed status <<< "$(echo "$row" | tail -n 1)"

    echo "$store_name,$revenue,$orders,$failed,$status" >> "$REPORT_FILE"
  done

  echo "CSV report generated at $REPORT_FILE"
}

show_menu() {
  while true; do
    echo "1. Process today's orders"
    echo "2. Generate CSV report"
    echo "3. View alert log"
    echo "4. Exit"
    read -p "Select [1-4]: " choice

    case "$choice" in
      1)
        validate_files
        for csv_file in "$ORDER_DIR"/*.csv; do
          [ -e "$csv_file" ] || continue
          while IFS=',' read -r order_id date status category amount; do
            [ -z "$order_id" ] && continue
            [ "$order_id" = "order_id" ] && continue
            echo "Processing row: $order_id $date $status $category $amount"
          done < "$csv_file"
        done
        ;;
      2)
        validate_files
        generate_csv
        ;;
      3)
        cat "$ALERT_LOG"
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
  if [ "${1:-}" = "--menu" ]; then
    show_menu
  else
    validate_files
    generate_csv
  fi
}

main "$@"

info_count = 0 
error_count = 0
warn_count = 0
#function to analyze log file
analyze_log_file() {
    file="$1"
    while IFS= read -r line; do
        if echo "$line" | grep -q "INFO"; then
            info_count=$((info_count + 1))
        elif echo "$line" | grep -q "WARNING"; then
            ((warn_count++))
        else
            ((error_count++))
        fi
    done < "$file"

}

#function to determine the system status
check_status(){
    if[[ $error_count -gt 0 ]]; then
        echo "System Status: ERROR"
    elif [[ $warn_count -gt 0 ]]; then
        echo "System Status: WARNING"
    else
        echo "System Status: OK"
    fi
}


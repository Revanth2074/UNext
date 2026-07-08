# A simple script to reverse a string
reverse_string() {
    input_string="$1"
    reversed_string=""
    
    # Loop through the string in reverse order
    for (( i=${#input_string}-1; i>=0; i-- )); do
        reversed_string+="${input_string:$i:1}"
    done
    
    echo "Reversed string: $reversed_string"
}

# Call the function with a string
reverse_string "Hello, World!"
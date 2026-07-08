#!/bin/bash

echo "=========================================="
echo "      Greatest of Two Numbers Checker     "
echo "=========================================="

# Prompt user for the first number
echo -n "Enter first number: "
read num1

# Prompt user for the second number
echo -n "Enter second number: "
read num2

echo "=========================================="

# Compare the numbers
if [ "$num1" -gt "$num2" ]; then
    echo "The greatest number is: $num1"
elif [ "$num2" -gt "$num1" ]; then
    echo "The greatest number is: $num2"
else
    echo "Both numbers are equal ($num1)."
fi

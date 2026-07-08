#!/bin/bash

echo "=========================================="
echo "         Multiplication Table Generator   "
echo "=========================================="

# Prompt user for the number
echo -n "Enter a number: "
read num

echo "=========================================="
echo "Multiplication Table for $num:"
echo "=========================================="

# Loop from 1 to 10
for i in {1..10}
do
    # Calculate the product
    result=$((num * i))
    
    # Print the row (e.g., 5 x 1 = 5)
    echo "$num x $i = $result"
done

echo "=========================================="

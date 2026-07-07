#!/bin/bash

echo "Enter marks for 5 subjects:"

read -p "Subject 1: " s1
read -p "Subject 2: " s2
read -p "Subject 3: " s3
read -p "Subject 4: " s4
read -p "Subject 5: " s5

total=$((s1 + s2 + s3 + s4 + s5))
percentage=$((total / 5))

echo "Total Marks = $total"
echo "Percentage = $percentage%"

if [ $percentage -ge 90 ]; then
    grade="A+"
elif [ $percentage -ge 80 ]; then
    grade="A"
elif [ $percentage -ge 70 ]; then
    grade="B"
elif [ $percentage -ge 60 ]; then
    grade="C"
elif [ $percentage -ge 50 ]; then
    grade="D"
else
    grade="F"
fi

echo "Grade = $grade"

#!/bin/bash

employees_file="employees.txt"
report_file="payroll_report.txt"

if [ ! -f "$employees_file" ]; then
    echo "Input file '$employees_file' not found. Create it with employee data like: 101 John 45000"
    exit 1
fi

printf "%s\t%s\t%s\t%s\t%s\t%s\n" "EmployeeID" "Name" "Salary" "Tax" "Bonus" "NetSalary" > "$report_file"
printf "%s\n" "-------------------------------------------------------------" >> "$report_file"

while read -r emp_id emp_name emp_salary; do
    if [ -z "$emp_id" ] || [ -z "$emp_name" ] || [ -z "$emp_salary" ]; then
        continue
    fi

    if [ "$emp_salary" -le 30000 ]; then
        tax=$(( emp_salary * 5 / 100 ))
    elif [ "$emp_salary" -le 60000 ]; then
        tax=$(( emp_salary * 10 / 100 ))
    else
        tax=$(( emp_salary * 15 / 100 ))
    fi

    if [ "$emp_salary" -le 50000 ]; then
        bonus=2000
    else
        bonus=5000
    fi

    net_salary=$(( emp_salary - tax + bonus ))
    printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$emp_id" "$emp_name" "$emp_salary" "$tax" "$bonus" "$net_salary" >> "$report_file"
done < "$employees_file"

echo "Payroll report generated: $report_file"

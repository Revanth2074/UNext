employees = [("Asha", 85), ("Bala", 92), ("Chitra", 78)]

sorted_employees = sorted(employees, key=lambda x: x[1], reverse=True)

print("Sorted Employees:")
print(sorted_employees)
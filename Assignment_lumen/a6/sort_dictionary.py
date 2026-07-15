students = {
    "Asha": 78,
    "Bala": 90,
    "Chitra": 65
}

rank_list = sorted(students.items(), key=lambda x: x[1], reverse=True)

print("Rank List:")
for name, marks in rank_list:
    print(name, "-", marks)
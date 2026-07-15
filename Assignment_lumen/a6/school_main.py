from school import students, teachers, results

students.add_student("Asha")
students.add_student("Bala")

teachers.assign_subject("Mr. Ravi", "Mathematics")

print("Students:", students.view_students())
print("Teachers:", teachers.view_teachers())

marks = 82
print("Marks =", marks)
print("Grade =", results.calculate_grade(marks))
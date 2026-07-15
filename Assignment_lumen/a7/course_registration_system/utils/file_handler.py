import csv
import os


COURSES_FILE = "data/courses.csv"
STUDENTS_FILE = "data/students.csv"


# ---------------- COURSE FILE ----------------

def read_courses():

    courses = []

    if not os.path.exists(COURSES_FILE):

        raise FileNotFoundError(
            "Course data file not found"
        )


    with open(
        COURSES_FILE,
        "r"
    ) as file:

        reader = csv.reader(file)

        next(reader)  # Skip header


        for row in reader:

            courses.append(row)


    return courses



def write_courses(courses):

    with open(
        COURSES_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)


        writer.writerow(
            [
                "course_id",
                "course_name",
                "instructor",
                "seats_available"
            ]
        )


        writer.writerows(courses)



# ---------------- STUDENT FILE ----------------


def read_students():

    students = []


    if not os.path.exists(STUDENTS_FILE):

        raise FileNotFoundError(
            "Student data file not found"
        )


    with open(
        STUDENTS_FILE,
        "r"
    ) as file:

        reader = csv.reader(file)

        next(reader)


        for row in reader:

            students.append(row)


    return students




def write_students(students):

    with open(
        STUDENTS_FILE,
        "w",
        newline=""
    ) as file:


        writer = csv.writer(file)


        writer.writerow(
            [
                "student_id",
                "name",
                "email",
                "enrolled_courses"
            ]
        )


        writer.writerows(students)
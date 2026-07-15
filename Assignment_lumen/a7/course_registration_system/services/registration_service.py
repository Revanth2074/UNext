from models.course import Course
from models.student import Student

from utils.file_handler import (
    read_courses,
    write_courses,
    read_students,
    write_students
)

from exceptions.custom_exceptions import (
    CourseNotFoundError,
    StudentNotFoundError,
    CourseFullError
)


# ---------------------------------
# View All Courses
# ---------------------------------

def view_courses():

    courses = read_courses()


    print("\n====== Available Courses ======\n")


    for course in courses:

        print(
            f"Course ID : {course[0]}"
        )

        print(
            f"Course Name : {course[1]}"
        )

        print(
            f"Instructor : {course[2]}"
        )

        print(
            f"Seats Available : {course[3]}"
        )

        print(
            "-" * 30
        )



# ---------------------------------
# Add New Course
# ---------------------------------

def add_course(
        course_id,
        course_name,
        instructor,
        seats
):

    courses = read_courses()


    new_course = Course(
        course_id,
        course_name,
        instructor,
        seats
    )


    courses.append(
        new_course.to_list()
    )


    write_courses(
        courses
    )


    print(
        "Course added successfully"
    )



# ---------------------------------
# Register Student
# ---------------------------------

def register_student(
        student_id,
        name,
        email
):

    students = read_students()


    new_student = Student(
        student_id,
        name,
        email,
        ""
    )


    students.append(
        new_student.to_list()
    )


    write_students(
        students
    )


    print(
        "Student registered successfully"
    )



# ---------------------------------
# Enroll Course
# ---------------------------------

def enroll_course(
        student_id,
        course_id
):

    courses = read_courses()

    students = read_students()


    student_found = False
    course_found = False



    # Find Student

    for student in students:

        if student[0] == student_id:

            student_found = True

            student_record = student

            break



    if not student_found:

        raise StudentNotFoundError(
            "Error: Student not found"
        )



    # Find Course

    for course in courses:


        if course[0] == course_id:


            course_found = True


            if int(course[3]) <= 0:

                raise CourseFullError(
                    "Error: No seats available for this course"
                )



            course[3] = str(
                int(course[3]) - 1
            )



            if student_record[3] == "":

                student_record[3] = course_id

            else:

                student_record[3] += "," + course_id



            break



    if not course_found:

        raise CourseNotFoundError(
            "Error: Course not found"
        )



    write_courses(
        courses
    )


    write_students(
        students
    )


    print(
        "Course enrollment successful"
    )



# ---------------------------------
# Drop Course
# ---------------------------------

def drop_course(
        student_id,
        course_id
):

    courses = read_courses()

    students = read_students()



    student_found = False
    course_found = False



    # Find student

    for student in students:


        if student[0] == student_id:


            student_found = True


            student_record = student


            break



    if not student_found:


        raise StudentNotFoundError(
            "Error: Student not found"
        )



    # Remove course from student


    enrolled = (
        student_record[3].split(",")
        if student_record[3]
        else []
    )


    if course_id in enrolled:

        enrolled.remove(
            course_id
        )


        student_record[3] = ",".join(
            enrolled
        )

    else:

        print(
            "Student is not enrolled in this course"
        )



    # Increase course seats


    for course in courses:


        if course[0] == course_id:


            course_found = True


            course[3] = str(
                int(course[3]) + 1
            )


            break



    if not course_found:


        raise CourseNotFoundError(
            "Error: Course not found"
        )



    write_courses(
        courses
    )


    write_students(
        students
    )


    print(
        "Course dropped successfully"
    )
from services.registration_service import (
    view_courses,
    add_course,
    register_student,
    enroll_course,
    drop_course
)

from exceptions.custom_exceptions import (
    CourseNotFoundError,
    StudentNotFoundError,
    CourseFullError
)


def menu():

    while True:

        print("\n===== Student Course Registration System =====")
        print("1. View Courses")
        print("2. Add Course")
        print("3. Register Student")
        print("4. Enroll Course")
        print("5. Drop Course")
        print("6. Exit")


        choice = input("Enter your choice: ")


        try:

            if choice == "1":

                view_courses()


            elif choice == "2":

                course_id = input("Enter Course ID: ")
                name = input("Enter Course Name: ")
                instructor = input("Enter Instructor Name: ")
                seats = input("Enter Available Seats: ")


                add_course(
                    course_id,
                    name,
                    instructor,
                    seats
                )


            elif choice == "3":

                student_id = input("Enter Student ID: ")
                name = input("Enter Student Name: ")
                email = input("Enter Email: ")


                register_student(
                    student_id,
                    name,
                    email
                )


            elif choice == "4":

                student_id = input(
                    "Enter Student ID: "
                )

                course_id = input(
                    "Enter Course ID: "
                )


                enroll_course(
                    student_id,
                    course_id
                )


            elif choice == "5":

                student_id = input(
                    "Enter Student ID: "
                )

                course_id = input(
                    "Enter Course ID: "
                )


                drop_course(
                    student_id,
                    course_id
                )


            elif choice == "6":

                print(
                    "Thank you for using Student Course Registration System."
                )

                break


            else:

                print(
                    "Invalid choice."
                )


        except CourseNotFoundError as e:

            print(e)


        except StudentNotFoundError as e:

            print(e)


        except CourseFullError as e:

            print(e)


        except FileNotFoundError:

            print(
                "Error: Course/Student data file not found"
            )


        except Exception as e:

            print(
                "Unexpected Error:",
                e
            )



if __name__ == "__main__":

    menu()
import unittest


from services.registration_service import (
    register_student,
    enroll_course,
    drop_course,
    add_course
)


from utils.file_handler import (
    read_courses,
    read_students,
    write_courses,
    write_students
)


from exceptions.custom_exceptions import (
    CourseNotFoundError,
    StudentNotFoundError,
    CourseFullError
)



class TestCourseRegistration(unittest.TestCase):


    def setUp(self):

        # Reset data before every test

        write_courses(
            [
                [
                    "C101",
                    "Python Programming",
                    "Dr.Kumar",
                    "2"
                ],
                [
                    "C102",
                    "Data Science",
                    "Dr.Smith",
                    "0"
                ]
            ]
        )


        write_students(
            [
                [
                    "S001",
                    "Ravi Kumar",
                    "ravi@gmail.com",
                    ""
                ]
            ]
        )



    # TC01 View Courses

    def test_view_courses(self):

        courses = read_courses()

        self.assertEqual(
            len(courses),
            2
        )



    # TC02 Register Student

    def test_register_student(self):

        register_student(
            "S002",
            "Meena",
            "meena@gmail.com"
        )


        students = read_students()


        self.assertEqual(
            len(students),
            2
        )



    # TC03 Enroll Course

    def test_enroll_course(self):

        enroll_course(
            "S001",
            "C101"
        )


        courses = read_courses()


        self.assertEqual(
            courses[0][3],
            "1"
        )



    # TC04 Full Course

    def test_full_course(self):

        with self.assertRaises(
            CourseFullError
        ):

            enroll_course(
                "S001",
                "C102"
            )



    # TC05 Course Not Found

    def test_course_not_found(self):

        with self.assertRaises(
            CourseNotFoundError
        ):

            enroll_course(
                "S001",
                "C999"
            )



    # TC06 Student Not Found

    def test_student_not_found(self):

        with self.assertRaises(
            StudentNotFoundError
        ):

            enroll_course(
                "S999",
                "C101"
            )



    # TC07 Drop Course

    def test_drop_course(self):

        enroll_course(
            "S001",
            "C101"
        )


        drop_course(
            "S001",
            "C101"
        )


        students = read_students()


        self.assertEqual(
            students[0][3],
            ""
        )



if __name__ == "__main__":

    unittest.main()
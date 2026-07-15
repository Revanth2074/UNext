class Student:

    def __init__(
        self,
        student_id,
        name,
        email,
        enrolled_courses=""
    ):

        self.student_id = student_id
        self.name = name
        self.email = email
        self.enrolled_courses = enrolled_courses


    def add_course(
        self,
        course_id
    ):

        if self.enrolled_courses == "":
            self.enrolled_courses = course_id

        else:
            self.enrolled_courses += "," + course_id



    def remove_course(
        self,
        course_id
    ):

        courses = self.enrolled_courses.split(",")

        if course_id in courses:
            courses.remove(course_id)

        self.enrolled_courses = ",".join(courses)



    def to_list(self):

        return [
            self.student_id,
            self.name,
            self.email,
            self.enrolled_courses
        ]



    def __str__(self):

        return (
            f"Student ID : {self.student_id}\n"
            f"Name : {self.name}\n"
            f"Email : {self.email}\n"
            f"Enrolled Courses : {self.enrolled_courses}"
        )
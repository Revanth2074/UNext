class Course:

    def __init__(
        self,
        course_id,
        course_name,
        instructor,
        seats_available
    ):

        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.seats_available = int(seats_available)


    def reduce_seat(self):

        if self.seats_available > 0:
            self.seats_available -= 1


    def increase_seat(self):

        self.seats_available += 1


    def to_list(self):

        return [
            self.course_id,
            self.course_name,
            self.instructor,
            self.seats_available
        ]


    def __str__(self):

        return (
            f"Course ID : {self.course_id}\n"
            f"Course Name : {self.course_name}\n"
            f"Instructor : {self.instructor}\n"
            f"Seats Available : {self.seats_available}"
        )
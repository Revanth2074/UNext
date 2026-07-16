from models.person import Person


class Member(Person):

    def __init__(self, member_id, name, age, membership_type):
        super().__init__(member_id, name, age)
        self.membership_type = membership_type

    def __str__(self):
        return f"{super().__str__()}, Membership:{self.membership_type}"
from typing import Union


MemberID = Union[int, str]


def display_member(member_id: MemberID, name: str):
    print("Member Details")
    print("--------------")
    print(f"Member ID : {member_id}")
    print(f"Name      : {name}")
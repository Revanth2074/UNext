from models.member import Member
from services.member_service import MemberService


service = MemberService()

member = Member(1, "Tony", 24, "Premium")

service.add_member(member)

assert service.get_member(1).name == "Tony"

service.update_membership(1, "Regular")

assert service.get_member(1).membership_type == "Regular"

service.delete_member(1)

assert service.get_member(1) is None

print("Member Test Passed")
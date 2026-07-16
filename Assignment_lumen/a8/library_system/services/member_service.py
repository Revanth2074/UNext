from data.datastore import datastore


class MemberService:

    def add_member(self, member):
        datastore["members"][member.id] = member

    def get_member(self, member_id):
        return datastore["members"].get(member_id)

    def update_membership(self, member_id, membership):
        member = self.get_member(member_id)
        if member:
            member.membership_type = membership

    def delete_member(self, member_id):
        datastore["members"].pop(member_id, None)

    def list_members(self):
        return datastore["members"].values()
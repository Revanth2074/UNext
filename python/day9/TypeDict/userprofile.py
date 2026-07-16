from typing import TypedDict

class UserProfile(TypedDict):
    id: int
    name: str
    email: str
    bio: Optional[str]

def format_user_profile(users: List[UserProfile]) -> List:
    return [f" {u['name']} ({u['email']}) - {u.get('bio', 'No bio available')}" for u in users]

users = [
    {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "bio": "Software engineer"
    },
    {
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com",
        "bio": "Data scientist"
    }
]
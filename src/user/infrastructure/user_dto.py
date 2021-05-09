from typing import TypedDict


class UserDTO(TypedDict):
    user_id: str
    email: str
    username: str
    avatar: str

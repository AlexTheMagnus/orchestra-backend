from typing import TypedDict, List


class UserDTO(TypedDict):
    user_id: str
    favorites: List[str]
    likes: List[str]

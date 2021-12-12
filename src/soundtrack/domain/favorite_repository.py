from abc import ABC, abstractmethod

from .soundtrack_id import SoundtrackId
from .user_id import UserId


class FavoriteRepository(ABC):
    @abstractmethod
    def delete_all_with_soundtrack(self, soundtrack_id: SoundtrackId):
        pass
from src.soundtrack.domain.favorite_repository import FavoriteRepository
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.user_id import UserId

class FavoriteInMemoryRepository(FavoriteRepository):
    def delete_all_with_soundtrack(self, soundtrack_id: SoundtrackId):
        pass
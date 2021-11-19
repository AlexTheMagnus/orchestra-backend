import os
import sqlalchemy as db

from ..domain.favorite_repository import FavoriteRepository
from ..domain.soundtrack_id import SoundtrackId

class FavoriteMysqlRepository(FavoriteRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__favorites = db.Table(
            "favorite", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)


    def delete_all_with_soundtrack(self, soundtrack_id: SoundtrackId):
        query = db.delete(self.__favorites
        ).where(self.__favorites.columns.soundtrack_id == soundtrack_id.value)
        self.__db_connection.execute(query)

    def clean(self):
        query = db.delete(self.__favorites)
        self.__db_connection.execute(query)
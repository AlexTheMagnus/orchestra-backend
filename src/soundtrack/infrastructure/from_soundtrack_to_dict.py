from typing import List

from ..domain.soundtrack import Soundtrack


class FromSoundtrackToDict:

    def __init__(self):
        pass

    @staticmethod
    def with_soundtrack(soundtrack: Soundtrack):    
        soundtrack_dict = {
            "soundtrack_id": soundtrack.soundtrack_id.value,
            "book": soundtrack.book.value,
            "soundtrack_title": soundtrack.soundtrack_title.value,
            "author": soundtrack.author.value
        }

        return soundtrack_dict

    @staticmethod
    def with_soundtracks_list(soundtracks_list: List[Soundtrack]):
        soundtracks_list_dict = { "soundtracks_list": [] }
        
        for soundtrack in soundtracks_list:
            soundtrack_dict = FromSoundtrackToDict.with_soundtrack(soundtrack)
            soundtracks_list_dict["soundtracks_list"].append(soundtrack_dict)

        return soundtracks_list_dict
from spotipy import client

class AccessTokenValidator:
    @staticmethod
    def validate(access_token: str):
        try:
            spotify_user = client.Spotify(auth=access_token).me()
        except Exception as error:
            return None
        
        return spotify_user
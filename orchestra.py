import os
from flask import Flask
from flask_cors import CORS

from src.soundtrack.infrastructure.chapter.chapters_controller import chapters
from src.soundtrack.infrastructure.soundtracks_controller import soundtracks
from src.user.infrastructure.users_controller import users

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Orchestra, conduct your books\' soundtracks'

app.register_blueprint(soundtracks)
app.register_blueprint(chapters)
app.register_blueprint(users)

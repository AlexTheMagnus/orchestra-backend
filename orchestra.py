import os
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from src.soundtrack.infrastructure.chapter.chapters_controller import chapters
from src.soundtrack.infrastructure.soundtracks_controller import soundtracks
from src.user.infrastructure.users_controller import users

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Orchestra, conduct your books\' soundtracks'

# Swagger
SWAGGER_URL = ''
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Orchestra REST API"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.register_blueprint(soundtracks)
app.register_blueprint(chapters)
app.register_blueprint(users)

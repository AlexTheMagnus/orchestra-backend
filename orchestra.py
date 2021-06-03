from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from src.soundtrack.infrastructure.soundtrack_controller import soundtracks

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

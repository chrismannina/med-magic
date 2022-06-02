from os import environ, path
from dotenv import load_dotenv
import requests

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask configuaration from .env file"""

    # general config
    try:
        FLASK_APP = environ.get('FLASK_APP')
        FLASK_ENV = environ.get('FLASK_ENV')    
        r = requests.get('https://uuid-genie.herokuapp.com/api/uuid')
        uuid = r.json()
        SECRET_KEY = uuid['uuid']
    except:
        pass
    
    # static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = True
    
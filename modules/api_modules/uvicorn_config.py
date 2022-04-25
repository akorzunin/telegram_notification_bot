#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()

from modules.api_modules.fast_api_app import app

CONFIG = dict(
    app=app, 
    host=os.getenv('HOST', '0.0.0.0'),
    port=int(os.getenv('PORT', 8000)),
    log_level='info',
)
import enum

class TreshholdType(enum.Enum):
    higher = 'higher'
    lower= 'lower'

from modules.api_modules.db_api.database import SessionLocal
class DBContextManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
from src.controller.database.database import SessionLocal

class BaseQuery:
    def __init__(self):
        self.db = SessionLocal()
    
    def commit(self):
        self.db.commit()
    
    def close(self):
        self.db.close()

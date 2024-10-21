from fastapi import FastAPI
from src.controller import controller_auth, controller_user
from src.controller.database.database import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Authentication System"} 

# Register routers
app.include_router(controller_auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(controller_user.router, prefix="/user", tags=["User"])

# To run: uvicorn main:app --reload



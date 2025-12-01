from fastapi import FastAPI

from .db.database import engine, Base
from .api.v1.api import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(api_router, prefix="/api/v1")

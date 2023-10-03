from dotenv import load_dotenv
from fastapi import FastAPI

from routes.api import router
from src.demo_data.insert_data import insert_all_data
from src.models import all_models
from src.models.database import engine

load_dotenv()

# Drop all existing tables
all_models.Base.metadata.drop_all(engine)
# delete all tables and recreate here
all_models.Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(router)
insert_all_data()

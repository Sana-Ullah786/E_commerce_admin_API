from dotenv import load_dotenv
from fastapi import FastAPI
from src.models.database import engine
from src.models import all_models
from routes.api import router



load_dotenv()

# Drop all existing tables
all_models.Base.metadata.drop_all(engine)
# delete all tables and recreate here
all_models.Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(router)

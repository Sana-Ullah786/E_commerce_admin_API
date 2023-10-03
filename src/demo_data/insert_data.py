import requests
CATEGORIES = [
    'Desktops',
    'Chairs',
    'LED'
]
from src.dependencies import get_db
from src.models import all_models
def insert_categories():
    # use db to insert data into category
    db = next(get_db())
    for category in CATEGORIES:
        new_category = all_models.Category(name=category)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    print("Categories inserted successfully")


    

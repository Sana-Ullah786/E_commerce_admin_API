from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.models import all_models
from faker import Faker
import random

MERCHANTS = [
    "Amazon",
    "Walmart"
]


CATEGORIES = [
    'Desktops',
    'Chairs',
    'LED'
]

# Helper function to insert categies into DB
def insert_categories():
    db = next(get_db())
    for category in CATEGORIES:
        new_category = all_models.Category(name=category)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    print("Categories inserted successfully")


# Helper function to insert Merchants into DB
def insert_merchants():
    db = next(get_db())
    for merchant in MERCHANTS:
        new_merchant = all_models.Merchant(name=merchant)
        db.add(new_merchant)
        db.commit()
        db.refresh(new_merchant)
    print("Merchants inserted successfully")

fake = Faker()





# Helper function to create random products for a given category
def create_random_product(category_id: int) -> all_models.Product:
    product_name = fake.word()
    description = fake.sentence()
    price = fake.random_number(digits=4, fix_len=True)  # This will give you a price between 1000 and 9999

    return all_models.Product(
        name=product_name,
        description=description,
        category_id=category_id,
        price=price
    )

# Main function to insert random products for each category
def insert_random_products():
    db: Session = next(get_db())
    # select all merchants id from Merchant and chose random id
    merchant_id = db.query(all_models.Merchant.merchant_id).order_by(all_models.Merchant.merchant_id).all()
    merchant_ids = [merchant[0] for merchant in merchant_id]
    for category in db.query(all_models.Category):
        for _ in range(10):  # insert 10 products for each category
            new_product = create_random_product(category.category_id)
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            # select random merchant id from merchant_ids
            random_merchant_id = random.choice(merchant_ids)
            # create product_merchant object
            product_merchant = all_models.ProductMerchant(product_id=new_product.product_id, merchant_id=random_merchant_id)
            db.add(product_merchant)
            db.commit()

            

    print("Random products inserted successfully!")


def insert_all_data():
    insert_categories()
    insert_merchants()
    insert_random_products()
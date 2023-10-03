import random

from faker import Faker
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import all_models

MERCHANTS = ["Amazon", "Walmart"]


CATEGORIES = ["Desktops", "Chairs", "LED"]


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


# Helper function to insert username, password into db
def insert_user():
    db = next(get_db())
    # unhashed Password is = Password123!
    new_user = all_models.User(
        username="admin", password="$2a$12$55.zn7lW0z594G45Sqj7FOKALV1NIFZKvtMB55BjdIJbxdk65O8m6", is_admin=True, is_deleted=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("User inserted successfully")

fake = Faker()


# Helper function to create random products for a given category
def create_random_product(category_id: int) -> all_models.Product:
    product_name = fake.word()
    description = fake.sentence()
    price = fake.random_number(
        digits=4, fix_len=True
    )  # This will give you a price between 1000 and 9999

    return all_models.Product(
        name=product_name, description=description, category_id=category_id, price=price
    )


# Main function to insert random products for each category
def insert_random_products():
    db: Session = next(get_db())
    # select all merchants id from Merchant and chose random id
    merchant_id = (
        db.query(all_models.Merchant.merchant_id)
        .order_by(all_models.Merchant.merchant_id)
        .all()
    )
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
            product_merchant = all_models.ProductMerchant(
                product_id=new_product.product_id, merchant_id=random_merchant_id
            )
            db.add(product_merchant)
            db.commit()

    print("Random products inserted successfully!")


# helper function to insert inventory
def insert_inventory():
    """
    product_id: int = Field(description="ID of the related product")
    current_stock: int = Field(ge=0, description="Current stock of the product")
    low_stock_threshold: int = Field(ge=0, description="Threshold below which stock is considered low")

    """
    # for all product ids in db, add current stock between 40 and 50 ramdom using faker and add threshold between 5 and 10 random
    db = next(get_db())
    for product in db.query(all_models.Product):
        new_inventory = all_models.Inventory (
            product_id = product.product_id,
            current_stock = fake.random_int(min=40, max=50),
            low_stock_threshold = fake.random_int(min=5, max=10)
        )
        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)
        # insert inventory log
        new_inventory_log = all_models.InventoryLog (
            inventory_id = new_inventory.inventory_id,
            product_id = product.product_id,
            previous_stock = 0,
            new_stock = new_inventory.current_stock,
            total_stock = new_inventory.current_stock
        )
        db.add(new_inventory_log)
        db.commit()
        db.refresh(new_inventory_log)
    print("Inventory inserted successfully")

# helper function to update inventories
def update_all_inventories():
    db = next(get_db())
    for inventory in db.query(all_models.Inventory):
        _previous_stock = inventory.current_stock
        new_stock = fake.random_int(min=4, max=8)
        inventory.current_stock += new_stock
        db.commit()
        db.refresh(inventory)
        # insert inventory log
        new_inventory_log = all_models.InventoryLog (
            inventory_id = inventory.inventory_id,
            product_id = inventory.product_id,
            previous_stock = _previous_stock,
            new_stock = new_stock,
            total_stock = new_stock + _previous_stock,
            # get random date between past 10 days and next 15 days
            created_at = fake.date_time_between(start_date="-10d", end_date="+15d")
        )
        db.add(new_inventory_log)
        db.commit()
        db.refresh(new_inventory_log)
    print("Inventory updated successfully")



def insert_all_data():
    insert_user()
    insert_categories()
    insert_merchants()
    insert_random_products()
    insert_inventory()
    update_all_inventories()

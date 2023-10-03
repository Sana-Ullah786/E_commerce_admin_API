# ADMIN CREDENTIALS: (To get access token as each endpoint is accessible by ADMIN only and access demo data populated in Database)
## username = admin
## password = Password123!
# NOTE: Demo data is also will be populated when you run the server

# E_commerce_admin_API

A brief description of your project and its functionality.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.8**: If not installed, download it from [here](https://www.python.org/downloads/release/python-380/).
- **MySQL**: If not installed, download it from [here](https://dev.mysql.com/downloads/installer/). Ensure the MySQL server is running after installation.

## Dependencies

This project uses several libraries and dependencies, which are listed in the `requirements.txt` file.

## Setup & Installation

1. **Clone the Repository**:
    ```
    git clone https://github.com/Sana-Ullah786/E_commerce_admin_API.git
    cd E_commerce_admin_API
    ```

2. **Set Up a Virtual Environment** (recommended):
    ```
    python3.8 -m venv venv
    source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
    ```

3. **Install Required Packages**:
    ```
    pip install -r requirements.txt
    ```

4. **Setup MySQL Database**:
    - Create a new database in MySQL.
    - Remember the database name for the next step.

5. **Configure `.env` File**:
    An `.env` file is provided in the root directory. Open this file and modify the `DATABASE_URL` with your actual MySQL credentials and database name:
    ```
    DATABASE_URL=mysql+mysqlconnector://YOUR_MYSQL_USERNAME:YOUR_MYSQL_PASSWORD@localhost:3306/YOUR_DATABASE_NAME
    ```

6. **Run the Application**:
    ```
    uvicorn main:app --reload
    ```

    Navigate to `http://127.0.0.1:8000/` in your browser. You should see the FastAPI application running.

## Documentation

Visit `http://127.0.0.1:8000/docs` to view the FastAPI autogenerated API documentation for the endpoints.


# ENDPOINTS
### 1. /token (POST)
**Purpose**:
This endpoint is designed for user authentication. It allows users to log in using their username and password and returns an access token along with additional information.

**Usage**:

- Users must provide their credentials (username and password) in the request form.
- The system will validate the credentials against the database.
- If the credentials are valid, an access token will be generated and returned in the response.
- To make authorized requests to protected endpoints, include the access token in the request headers with the Authorization header field set to Bearer your_access_token_here.

### 2. /category (POST)
**Purpose:**
This endpoint is used to create a new category.

**Usage:**
- Send a POST request with a JSON body containing the category name.
- The system will create a new category with the provided name.
- If successful, it will return a status code `201 Created` along with a message and the newly created category's ID.
  
### 3. /category/{category_name} (GET)

**Purpose:**
This endpoint is used to retrieve a category by its name.

**Usage:**
- Send a GET request with the category name as a path parameter.
- The system will search for a category with a name that matches the provided name (case-insensitive).
- If the category is found, it will return a status code `200 OK` along with a message and the category's ID.
- If no category with the given name is found, it will return a status code `404 Not Found` with an error message.

### 4. /category/id/{category_id} (GET)
**Purpose:**
This endpoint is used to retrieve a category by its ID.

**Usage:**
- Send a GET request with the category ID as a path parameter.
- The system will search for a category with the provided ID.
- If the category is found, it will return a status code `200 OK` along with a message and the category's name.
- If no category with the given ID is found, it will return a status code `404 Not Found` with an error message.

### 5. /inventory (POST)

**Purpose:**
This endpoint is used to create a new inventory entry for a product.

**Usage:**
- Send a POST request with a JSON body containing the product ID, current stock, and low stock threshold.
- The system will create a new inventory entry with the provided information.
- It will also insert an inventory log entry with initial stock details.
- If successful, it will return a status code `201 Created` along with a message and the newly created inventory's ID.

### 6. /inventory/{product_id} (PUT)

**Purpose:**
This endpoint is used to update the inventory of a specific product by its ID.

**Usage:**
- Send a PUT request with the `product_id` as a path parameter and the new stock quantity in the request body.
- The system will update the inventory for the specified product by adding the new stock quantity.
- It will also insert an inventory log entry to record the stock change.
- If successful, it will return a status code `201 Created` along with a message and the updated inventory's ID.


### 7. /inventory/track/{product_id} (GET)
**Purpose**:
This endpoint is used to retrieve the inventory tracking history for a specific product by its ID.

**Usage**:

- Send a GET request with the product_id as a path parameter to retrieve the inventory tracking history for the specified product.
- The system will return a response with a list of inventory log entries that track changes in stock quantity for the product.
- If no inventory logs are found for the product, it will return a status code 404 Not Found.

### 8. /inventory (GET)
**Purpose**:
This endpoint is used to retrieve all inventory items in the system.

**Usage:**

- Send a GET request to retrieve a list of all inventory items.
- The system will return a response with the inventory data, including product IDs, current stock quantities, and low stock thresholds.
- If no inventory items are found, it will return a status code 404 Not Found.
### 9. /inventory/{product_id} (GET)
**Purpose**:
This endpoint is used to retrieve the status of inventory for a specific product by its ID.

**Usage:**

- Send a GET request with the product_id as a path parameter to retrieve the inventory status for the specified product.
- The system will return a response with the inventory data, including the product's current stock quantity.
- If the current stock is below the low stock threshold, it will include an "alert" in the response indicating low inventory.
- If no inventory item is found for the product, it will return a status code 404 Not Found.
### 9. /inventory/category/{category_id} (GET)
**Purpose**:
This endpoint is used to retrieve the status of inventory items within a specific category by category ID.

**Usage:**

- Send a GET request with the category_id as a path parameter to retrieve the inventory status for all products within the specified category.
- The system will return a response with two lists: "low_inventory_items" and "good_inventory_items."
- "low_inventory_items" contain inventory items with stock quantities below their respective low stock thresholds.
- "good_inventory_items" contain inventory items with stock quantities above their respective low stock thresholds.
- If no inventory items are found for the category, it will return a status code 404 Not Found.
### 10. /inventory/merchant/{merchant_id} (GET)
**Purpose**:
This endpoint is used to retrieve the status of inventory items associated with a specific merchant by merchant ID.

**Usage:**

- Send a GET request with the merchant_id as a path parameter to retrieve the inventory status for all products associated with the specified merchant.
- The system will return a response with two lists: "low_inventory_items" and "good_inventory_items."
- "low_inventory_items" contain inventory items with stock quantities below their respective low stock thresholds.
- "good_inventory_items" contain inventory items with stock quantities above their respective low stock thresholds.
- If no inventory items are found for the merchant, it will return a status code 404 Not Found.

### 11. /merchant (POST)
**Purpose**:
This endpoint is used to create a new merchant.

**Usage:**

- Send a POST request with a JSON body containing the merchant's name.
- The system will create a new merchant with the provided name.
- If successful, it will return a status code 201 Created along with a message and the newly created merchant's ID.

### 12. /merchant/id/{merchant_id} (GET)
**Purpose**:
This endpoint is used to retrieve a merchant by its ID.

**Usage:**

- Send a GET request with the merchant_id as a path parameter.
- The system will search for the merchant with the specified ID.
- If found, it will return a status code 200 OK along with a message and the merchant's name.

### 13. /merchant/{merchant_name} (GET)
**Purpose**:
This endpoint is used to retrieve a merchant by its name (case-insensitive).

**Usage:**

- Send a GET request with the merchant_name as a path parameter.
- The system will search for the merchant with the specified name (case-insensitive).
- If found, it will return a status code 200 OK along with a message and the merchant's ID.

### 14. /product (POST)
**Purpose**:
This endpoint is used to create a new product.

**Usage:**

- Send a POST request with a JSON body containing the product details, including the name, description, category ID, and price.
- The system will create a new product with the provided information.
- If successful, it will return a status code 201 Created along with a message and the newly created product's ID.

### 15. /sales (POST)
**Purpose**:
This endpoint is used to create a new sale transaction and update the product inventory.

**Usage:**

- Send a POST request with a JSON body containing the sale details, including the product ID, quantity sold, region, and revenue.
- The system will:
  - Check if the product exists.
  - Check if there is sufficient stock in the inventory.
  - Create a new sale transaction.
  - Update the product's inventory by reducing the stock.
- If successful, it will return a status code 201 Created along with a message and the newly created sale's ID.

### 16. /sales/analysis (GET)
**Purpose**:
This endpoint is used to analyze sales data within a specified time period and with optional filters, such as product, category, merchant, date range, and region.

**Usage:**

- Send a GET request to this endpoint with the following query parameters:
- period (string): Specifies the time period for analysis (daily, weekly, monthly, or annual).
- product_id (optional int): Filters results by a specific product ID.
- category_id (optional int): Filters results by a specific category ID.
- merchant_id (optional int): Filters results by a specific merchant ID.
- start_date (optional date): Specifies the start date for the analysis period.
- end_date (optional date): Specifies the end date for the analysis period.
- region (optional string): Filters results by a specific region.

### 17. /sales/compare_revenue (GET)
**Purpose**:
This endpoint is used to compare revenue for different categories of products over a specified time period.

**Usage:**

- Send a GET request to this endpoint with the following query parameter:
- period (string): Specifies the time period for revenue comparison (daily, weekly, monthly, or annual).
- The system will calculate and return revenue comparisons for each product category within the specified time period. The response will include the category name, category ID, total sales, and total 
- revenue for each category.

### 18. /sales/by_product (GET)
**Purpose**:
This endpoint is used to fetch sales data for a specific product.

**Usage:**

- Send a GET request to this endpoint with the following parameters:
- product_id (int): ID of the product to fetch sales data for.
- Optional Parameters:
- skip (int, default: 0): Number of records to skip.
- limit (int, default: 100): Maximum number of records to retrieve.
- start_date (date, optional): Start date for filtering sales data.
- end_date (date, optional): End date for filtering sales data.
- region (str, optional): Region for filtering sales data by region.
- The system will retrieve and return sales data for the specified product based on the provided parameters.

### 19. /sales/by_category (GET)
**Purpose**:
This endpoint is used to fetch sales data for a specific category of products.

**Usage:**

- Send a GET request to this endpoint with the following parameters:
- category_id (int): ID of the category to fetch sales data for.
- Optional Parameters:
- skip (int, default: 0): Number of records to skip.
- limit (int, default: 100): Maximum number of records to retrieve.
- start_date (date, optional): Start date for filtering sales data.
- end_date (date, optional): End date for filtering sales data.
- region (str, optional): Region for filtering sales data by region.
- The system will retrieve and return sales data for products within the specified category based on the provided parameters.

### 20. /sales/by_merchant (GET)
**Purpose**:
This endpoint is used to fetch sales data for a specific merchant.

**Usage:**

- Send a GET request to this endpoint with the following parameters:
- merchant_id (int): ID of the merchant to fetch sales data for.
- Optional Parameters:
- skip (int, default: 0): Number of records to skip.
- limit (int, default: 100): Maximum number of records to retrieve.
- start_date (date, optional): Start date for filtering sales data.
- end_date (date, optional): End date for filtering sales data.
- region (str, optional): Region for filtering sales data by region.
- The system will retrieve and return sales data for products associated with the specified merchant based on the provided parameters


### 21. /sales (GET)
**Purpose**:
This endpoint is used to fetch all sales data.

**Usage:**

- Send a GET request to this endpoint.
- Optional Parameters:
- skip (int, default: 0): Number of records to skip.
- limit (int, default: 100): Maximum number of records to retrieve.
- The system will retrieve and return sales data based on the provided parameters.

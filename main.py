from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from datetime import date
from logger import logger

app = FastAPI()
security = HTTPBasic()

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",        
        user="admin",            
        password="",
        database="data_study"    
    )
    return conn


### create admin account
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "admin":
        logger.error("Invalid login attempt: %s", credentials.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


### show campaign summary metrics
@app.get("/campaign_summary")
def campaign_summary(user: str = Depends(verify_credentials)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    select count(distinct order_id) as total_orders, 
           count(distinct uid) as total_customers,
           sum(gmv) as total_gmv, 
           sum(case when rebate > 0 then 1 else 0 end) as total_rebate_vouchers,
           sum(rebate) as total_rebate_values 
    from transaction_data
    """
    cursor.execute(query)
    rows = cursor.fetchall()   # return all results

    cursor.close()
    conn.close()
    return rows

### show customer ranking and their category
@app.get("/cutomers_category_ranking/{customer_id}")
def read_customers_ranking(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM customer_pending_rank WHERE customerID = %s"
    cursor.execute(query, (customer_id,))
    rows = cursor.fetchall()   # return all results

    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Customer is not found")
    return rows


### show shop ranking and their category
@app.get("/shops_category_ranking/{shop_id}")
def read_shops_ranking(shop_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM shop_selling_rank WHERE shop_id = %s"
    cursor.execute(query, (shop_id,))
    rows = cursor.fetchall()   # return all results

    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Shop is not found")
    return rows


### determine if the customer has fraudulent behavior
@app.get("/customers/{customer_id}")
def read_fraud_customer(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM suspected_fraud_customers WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    rows = cursor.fetchall()   # return all results

    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Customer is not found in suspected fraud list")
    return rows   


### determine if the shop has fraudulent behavior
@app.get("/shop_id/{shop_id}")
def read_fraud_shop(shop_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM suspected_fraud_shop WHERE shop_id = %s"
    cursor.execute(query, (shop_id,))
    rows = cursor.fetchall()   # return all results

    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Shop is not found in suspected fraud list")
    
    return rows


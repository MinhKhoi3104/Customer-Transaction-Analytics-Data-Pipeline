from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from datetime import date
from logger import logger

app = FastAPI()

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",        
        user="admin",            
        password="",
        database="data_study"    
    )
    return conn

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
        raise HTTPException(status_code=404, detail="Customer not found in suspected fraud list")
    
    return rows   

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
        raise HTTPException(status_code=404, detail="Shop not found in suspected fraud list")
    
    return rows
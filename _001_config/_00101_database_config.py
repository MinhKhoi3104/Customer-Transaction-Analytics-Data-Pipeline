import mysql.connector

URL_MYSQL = {
    "url": "jdbc:mysql://localhost:3307/ecom_transaction",
    "properties": {
        "host": "localhost",
        "port": 3307,
        "user": "root",
        "password": "123", 
        "database": "ecom_transaction"
    }
}
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",        
        port=3307,
        user="root",            
        password="123",
        database="ecom_transaction"    
    )
    return conn

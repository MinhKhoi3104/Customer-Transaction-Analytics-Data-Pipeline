# Customer Transaction Analytics Platform
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python) 
![DBT](https://img.shields.io/badge/DBT-1.7-orange?logo=dbt) 
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql) 
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi) 
![Postman](https://img.shields.io/badge/Postman-Tool-orange?logo=postman) 
![Docker](https://img.shields.io/badge/Docker-28-blue?logo=docker) 

A data analytics platform for e-commerce transactions, built with **DBT**, **MySQL**, and **FastAPI** to transform raw campaign data into business insights and fraud detection reports, and containerized with **Docker** for consistent deployment across environments.
## Introduction of the Project and Overview of the Implementation Steps
### 📌 Introduction:
This project is a Customer Transaction Analytics Platform designed to process and analyze e-commerce campaign data. The system transforms raw transaction logs into structured insights, such as customer spending, shop performance, and fraud detection. It also provides APIs for different stakeholders (customers, shop owners, and the marketing team) to access business metrics in real time.

![overview](./image/overview.png)

### 📝 Context:
The dataset was collected from a discount campaign on an e-commerce platform, containing detailed transaction records during the event. The campaign ran for **4 days (2019-10-30 to 2019-11-02)**, where each user received **one voucher per day** (30% off per order, capped at 20,000 VND).  
After gathering the campaign transaction data, the following steps were implemented:

### ⚙️ Overview of the Implementation Steps:
- Used **DBT (Data Build Tool)** to process and transform data from the raw transaction table (tbl transaction_data):
    - Transformed into a table storing shop and shop owner information (**tbl dim_shop_owner**).
    - Transformed into a table storing customer information such as total spending, ranking, and classification (Gold, Silver, Bronze) (**tbl customer_pending_rank**).
    - Transformed into a table storing shop information such as total orders, GMV, shop ranking by orders and revenue, and classification (Gold, Silver, Bronze) (**tbl shop_selling_rank**).
    - Defined, detected, and stored customers and shops with potentially fraudulent transactions into two separate tables:
        - **tbl suspected_fraud_customers** (customer info and reasons for fraud suspicion).
        - **tbl suspected_fraud_shop** (shop info and reasons for fraud suspicion).
- Built an **API** to allow different users to access analytics:
    - For customers and shop owners: 
        - View total GMV, ranking, classification, and check whether they are flagged as suspicious (with reasons).
    - For Marcom staff: 
        - Log in with authorized credentials (username: admin, password: admin) to view campaign-level metrics such as total orders, GMV, number of vouchers used, as well as detailed customer/shop information similar to other users.
- Used **Docker** to containerize the API, ensuring stable and consistent deployment across environments while simplifying setup and scalability.
  
## Detailed Project Demo Guide
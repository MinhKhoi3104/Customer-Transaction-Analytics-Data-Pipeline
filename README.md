# Customer Transaction Analytics Data Pipeline
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python) 
![DBT](https://img.shields.io/badge/DBT-1.7-orange?logo=dbt) 
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql) 
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi) 
![Postman](https://img.shields.io/badge/Postman-Tool-orange?logo=postman) 
![Docker](https://img.shields.io/badge/Docker-28-blue?logo=docker) 

A data pipeline for e-commerce transactions, built with **Python**, **DBT**, **MySQL**, **FastAPI**, and **Docker** to transform raw campaign data into business insights and fraud detection reports.
## Introduction of the Project and Overview of the Implementation Steps
### 📌 Introduction:
This project is a Customer Transaction Analytics Data Pipeline designed to process and analyze e-commerce campaign data. The system transforms raw transaction logs into structured insights, such as customer spending, shop performance, and fraud detection. It also provides APIs for different stakeholders (customers, shop owners, and the marketing team) to access business metrics in real time.

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

1. First, clone this repository from GitHub to your local machine. Then, set up a MySQL database (version 8.0) running on localhost:3306. Next, create a database named data_study and import the transaction_data.csv file from the data_sample folder into it.

![importdata](./image/importdata.png)

2. Next, create a new virtual environment to prepare for the demo. Note that the demo will be conducted on an ***Ubuntu environment using Anaconda***. If you are working on a different operating system or environment, please adapt the commands accordingly.

```bash
conda create --name demo-01 python=3.10 -y
conda activate demo-01
```
3. Then, import the required libraries.
```bash
pip install -r requirements.txt
```
4. Open a new terminal, update the dbt profile configuration, and then run the following commands:
```bash
cd ~/.dbt/ && code .
```
- Modify the file as follows:

![update-dbt-profile](./image/update-dbt-profile.png)

5. Return to the original terminal and run the following commands:
```bash
cd customer_online_transactions_analytics ### Navigate to the folder where dbt is running.
dbt run
```
- If the output matches the example image, the execution was successful and you will see the newly created tables in MySQL.

![dbt-success](./image/dbt-success.png)

![new-tbl](./image/new-tbl.png)

6. Continue by running the commands to open the DBT docs, where you can review the logic used to create the tables.
```bash
dbt docs generate;
dbt docs serve;
```
![dbt-docs](./image/dbt-docs.png)

![lineage-graph](./image/lineage-graph.png)

7. Next, run the commands to start FastAPI. You can open a separate terminal to enter the command or click "Ctrl + C" to continue this terminal. However, If you countinue to use this terminal, you must enter the command "cd .." before entering the below command
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
![api-success](./image/api-success.png)

- Copy the URL and paste it into your browser, then append /docs (e.g., http://0.0.0.0:8000/docs).

![api-docs](./image/api-docs.png)

- Click 'Try it out' and fill in the input to perform the search (for cases requiring login, use username = admin and password = admin).

![api-demo-01](./image/api-demo-01.png)

![api-demo-02](./image/api-demo-02.png)

- Note: Viewing the campaign summary is restricted to internal use (Marcom department), so a username and password are required. Any unauthorized login attempts with incorrect credentials will be logged in the file o_transaction_analytics_api.log

![api_authen](./image/api_authen.png)

![log_user_notpass](./image/log_user_notpass.png)

- All accesses to the API will be notified and logged.

![api-log-access](./image/api-log-access.png)

- Additionally, we can use Postman as an alternative to accessing the link http://0.0.0.0:8000/docs

![postman](./image/postman.png)

## ***Author: Nguyen Minh Khoi***
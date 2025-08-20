{{ config(materialized='view') }}

-- raw data add updated_date
select
    txn_time,
    txn_date,
    order_id,
    uid,
    shop_id,
    shop_owner_uid,
    gmv,
    rebate,
-- add updated_date
    NOW() as updated_date
from {{ source('main', 'transaction_data') }}
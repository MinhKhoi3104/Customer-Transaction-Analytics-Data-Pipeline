{{ config(materialized='table') }}

-- suspected fraud shop is defined: having under-1000 orders (fake orders hay order boosting)
select 
    txn_date,
    shop_owner_uid,
    shop_id
    'order_boosting' as 'fraud_note'
from {{ ref('stg_transaction_data') }}
where gmv < 1000
group by txn_date, shop_owner_uid,shop_id
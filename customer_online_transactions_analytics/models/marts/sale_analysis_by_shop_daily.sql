{{ config(materialized='table') }}

-- transform data, keep customer transaction data, eliminate other cases such as: adjust bad debt, customerID is blank
select
    txn_date as 'transaction_date',
    shop_id,
    shop_owner_uid,
    count(order_id) as 'order_total',
    sum(gmv) as 'gmv_total',
    sum(case when rebate > 0 then 1 else 0 end) as 'rebate_count',
    sum(rebate) as 'rebate_total'
from {{ ref('stg_transaction_data')}}
group by txn_date, shop_id, shop_owner_uid

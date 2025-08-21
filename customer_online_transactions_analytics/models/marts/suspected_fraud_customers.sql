{{ config(materialized='table') }}

-- suspected fraud customers is defined: buying under-1000 orders, use more than 1 voucher per day
with define_under_1000_fraud as (
select 
    txn_date,
    uid as 'customer_id',
    'have_orders_under_1000' as 'fraud_note'
from {{ ref('stg_transaction_data') }}
where gmv < 1000
group by txn_date, uid
)
, define_more_than_1_voucher_fraud as (
select
    txn_date,
    uid as 'customer_id',
    'use_more_than_1_voucher_per_day' as 'fraud_note'
from {{ ref('stg_transaction_data') }}
where rebate > 0
group by txn_date, uid
having count(rebate) > 1
)
-- main (sum up fraud)
(select * from define_under_1000_fraud)
union all
(select * from define_more_than_1_voucher_fraud)
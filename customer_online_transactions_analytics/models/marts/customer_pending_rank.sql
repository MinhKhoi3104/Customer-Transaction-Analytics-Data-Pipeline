{{ config(materialized='table') }}

-- customer pending rank 
with customer_total_pending as (
select
    uid as 'customerID',
    sum(gmv) as 'total_pending',
    dense_rank() over (order by sum(gmv) desc) as 'pending_rank'
from {{ ref('stg_transaction_data') }}
group by customerID )
-- customer category
select 
    customerID,
    total_pending,
    pending_rank,
    {{ rank_category('pending_rank') }} as 'customer_category'
from customer_total_pending
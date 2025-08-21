{{ config(materialized='table') }}

-- dim table about shop and shop_owner
select
    shop_id,
    shop_owner_uid
from {{ ref('stg_transaction_data')}}
group by shop_id, shop_owner_uid
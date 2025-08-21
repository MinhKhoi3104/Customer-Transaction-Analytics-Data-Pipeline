{{ config(materialized='table') }}

-- rank shop according the number of sold quantity, the gmv total
with shop_rank as (
select
    shop_id,
    shop_owner_uid,
    sum(total_order) as 'total_order',
    dense_rank() over (order by sum(total_order) DESC) as 'orders_rank',
    sum(total_gmv) as 'total_gmv',
    dense_rank() over (order by sum(total_gmv) DESC) as 'gmv_rank'

from {{ ref('sale_analysis_by_shop_daily') }}
group by shop_id, shop_owner_uid)

-- shop catogory
select *,
    {{ rank_category('gmv_rank') }} as 'shop_category'
from shop_rank
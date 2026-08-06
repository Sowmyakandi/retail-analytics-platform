with products as (

    select * from {{ ref('stg_products') }}

),

inventory as (

    select
        product_id,
        sum(stock_quantity) as total_stock_on_hand,
        max(case when needs_reorder then 1 else 0 end) = 1 as any_warehouse_needs_reorder

    from {{ ref('stg_inventory') }}
    group by product_id

)

select
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    p.list_price,
    coalesce(i.total_stock_on_hand, 0) as total_stock_on_hand,
    coalesce(i.any_warehouse_needs_reorder, false) as any_warehouse_needs_reorder

from products p
left join inventory i on p.product_id = i.product_id

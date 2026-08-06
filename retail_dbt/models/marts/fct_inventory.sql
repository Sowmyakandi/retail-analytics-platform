select
    inventory_id,
    product_id,
    warehouse,
    stock_quantity,
    reorder_level,
    last_restock_date,
    needs_reorder

from {{ ref('stg_inventory') }}

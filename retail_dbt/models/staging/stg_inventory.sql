with source as (

    select * from {{ source('raw', 'inventory') }}

),

renamed as (

    select
        inventory_id,
        product_id,
        trim(warehouse) as warehouse,
        cast(stock_quantity as integer) as stock_quantity,
        cast(reorder_level as integer) as reorder_level,
        cast(last_restock_date as date) as last_restock_date,
        cast(stock_quantity as integer) <= cast(reorder_level as integer) as needs_reorder

    from source
    where inventory_id is not null
      and product_id is not null

)

select * from renamed

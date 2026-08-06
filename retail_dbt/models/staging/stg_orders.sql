with source as (

    select * from {{ source('raw', 'orders') }}

),

renamed as (

    select
        order_id,
        customer_id,
        product_id,
        cast(quantity as integer) as quantity,
        cast(unit_price as decimal(12, 2)) as unit_price,
        cast(total_amount as decimal(14, 2)) as total_amount,
        cast(order_date as date) as order_date,
        trim(order_status) as order_status,
        trim(shipping_city) as shipping_city,
        trim(shipping_state) as shipping_state,
        round(cast(quantity as decimal(12, 2)) * cast(unit_price as decimal(12, 2)), 2)
            as calculated_total_amount

    from source
    where order_id is not null
      and customer_id is not null
      and product_id is not null

),

flagged as (

    select
        *,
        round(total_amount - calculated_total_amount, 2) as revenue_difference,
        abs(total_amount - calculated_total_amount) > 0.01 as has_revenue_mismatch

    from renamed

)

select * from flagged

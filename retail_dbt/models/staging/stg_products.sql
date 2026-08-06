with source as (

    select * from {{ source('raw', 'products') }}

),

renamed as (

    select
        product_id,
        trim(product_name) as product_name,
        trim(category) as category,
        trim(brand) as brand,
        cast(price as decimal(12, 2)) as list_price

    from source
    where product_id is not null

)

select * from renamed

with source as (

    select * from {{ source('raw', 'payments') }}

),

renamed as (

    select
        payment_id,
        order_id,
        cast(payment_date as date) as payment_date,
        trim(payment_method) as payment_method,
        cast(payment_amount as decimal(14, 2)) as payment_amount,
        trim(payment_status) as payment_status,
        transaction_reference,
        cast(payment_attempt as integer) as payment_attempt,
        parent_payment_id

    from source
    where payment_id is not null
      and order_id is not null

)

select * from renamed

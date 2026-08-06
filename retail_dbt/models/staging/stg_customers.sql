with source as (

    select * from {{ source('raw', 'customers') }}

),

renamed as (

    select
        customer_id,
        trim(first_name) as first_name,
        trim(last_name) as last_name,
        trim(first_name) || ' ' || trim(last_name) as full_name,
        lower(trim(email)) as email,
        phone,
        trim(city) as city,
        trim(state) as state,
        cast(signup_date as date) as signup_date

    from source
    where customer_id is not null

)

select * from renamed

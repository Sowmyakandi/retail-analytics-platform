with orders as (

    select * from {{ ref('stg_orders') }}

),

payments as (

    select
        order_id,
        sum(case when payment_status = 'Successful' then payment_amount else 0 end)
            as amount_paid,
        count(*) as payment_attempts,
        max(payment_date) as last_payment_date

    from {{ ref('stg_payments') }}
    group by order_id

)

select
    o.order_id,
    o.customer_id,
    o.product_id,
    o.quantity,
    o.unit_price,
    o.total_amount,
    o.calculated_total_amount,
    o.revenue_difference,
    o.has_revenue_mismatch,
    o.order_date,
    o.order_status,
    o.shipping_city,
    o.shipping_state,
    coalesce(p.amount_paid, 0) as amount_paid,
    coalesce(p.payment_attempts, 0) as payment_attempts,
    p.last_payment_date,
    (o.total_amount - coalesce(p.amount_paid, 0)) as amount_outstanding

from orders o
left join payments p on o.order_id = p.order_id

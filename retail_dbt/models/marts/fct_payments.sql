select
    payment_id,
    order_id,
    payment_date,
    payment_method,
    payment_amount,
    payment_status,
    transaction_reference,
    payment_attempt,
    parent_payment_id

from {{ ref('stg_payments') }}

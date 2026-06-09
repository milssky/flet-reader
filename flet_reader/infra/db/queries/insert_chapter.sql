INSERT INTO chapters (
    book_id,
    parent_id,
    title,
    order_index,
    level
)
VALUES (
    :book_id,
    :parent_id,
    :title,
    :order_index,
    :level
);

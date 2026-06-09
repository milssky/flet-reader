INSERT INTO blocks (
    book_id,
    chapter_id,
    order_index,
    type,
    content,
    payload
)
VALUES (
    :book_id,
    :chapter_id,
    :order_index,
    :type,
    :content,
    :payload
);

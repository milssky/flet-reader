SELECT
    books.id,
    books.title,
    book_authors.name
FROM books
INNER JOIN book_authors ON books.id = book_authors.book_id;

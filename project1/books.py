from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book

    return {"no book found!!"}

@app.get("/books/")
async def read_book_by_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author:str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold() and book.get('author').casefold() == book_author.casefold():
            books_to_return.append(book)

    return books_to_return

# post call

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

# put request

@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    is_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            is_updated = True
            return {"book updated"}

    if not is_updated:
        BOOKS.append(updated_book)
        return {"book added"}

    return {"no action performed!"}

# delete request

@app.delete("/books/delete_book")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"book deleted"}
    return {"no book found"}

# get books based on author

@app.get("/books/books_by_author/{author_name}")
async def all_books_by_author(author_name: str):
    required_books = []
    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold():
            required_books.append(book)

    return required_books

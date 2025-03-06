from fastapi import FastAPI, HTTPException, Path, Query, Body
from pydantic import BaseModel, Field
from typing import Optional
import main2


app = FastAPI()
app.include_router(main2.router)

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create.', default=None)
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=5, max_length=200)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "not required while adding new book. Required for updating",
                "title": "A new Book",
                "author": "Author name",
                "description": "desc about book",
                "rating": 5,
                "published_date": 2029
            }
        }
    }

def find_book_id(book: Book):
    if len(BOOKS)> 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.get("/books")
async def get_all_books():
    return BOOKS

# 1. path parameter
@app.get("/book/{book_id}")
async def get_book_by_id(book_id: int = Path(lt=10)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# 2. Query parameter
@app.get("/book_author/")
async def get_book_by_author(author_name: str = Query(min_length=5)):
    for book in BOOKS:
        if book.author == author_name:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    BOOKS.append(find_book_id(Book(**book_request.model_dump())))

@app.put("/upadte-book")
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/delete-book/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail="Item not found")

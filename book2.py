from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

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

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2027
            }
        }
    }


books = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(3, 'Computer Science Pro', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book description', 3, 2028),
    Book(5, 'HP2', 'Author 2', 'Book description', 2, 2027),
    Book(6, 'HP3', 'Author 3', 'Book description', 1, 2026)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return books

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

@app.get('/books/', status_code=status.HTTP_200_OK) 
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    return_by_book_rating = []
    for book in books:
        if book.rating == book_rating:
            return_by_book_rating.append(book)
    return return_by_book_rating

@app.get('/books/publish/', status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    return_by_published_date = []
    for book in books:
        if book.published_date == published_date:
            return_by_published_date.append(book)
    return return_by_published_date

@app.post('/create-book/', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_book_id(new_book))

def find_book_id(book: Book):
    # if len(books) > 0:
    #     book.id = books[-1].id + 1
    # else:
    #     book.id = 1
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book

@app.put('/books/update-book/', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(books)):
        if books[i].id == book.id:
            books[i] = book
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not found')

@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(books)):
        if books[i].id == book_id:
            books.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found')
    
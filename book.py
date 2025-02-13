from fastapi import FastAPI, Body, Depends
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import Session

# DATABASE_URL = "postgresql://postgres:ulugbek007@localhost/postgres"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# class Book(Base):
#     __tablename__ = "books"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, unique=True, index=True)
#     author = Column(String)
#     category = Column(String)

# Base.metadata.create_all(bind=engine)

books = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Six', 'category': 'math'}
]

app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/books")
# async def read_all_books(db: Session = Depends(get_db)):
#     return db.query(Book).all()

# @app.get("/books/{book_title}/")
# async def book_title(book_title: str, db: Session = Depends(get_db)):
#     return db.query(Book).filter(Book.title.ilike(book_title)).first()

# @app.get("/books/")
# async def read_category_by_query(category: str, db: Session = Depends(get_db)):
#     return db.query(Book).filter(Book.category.ilike(category)).all()

# @app.get("/books/byauthor/")
# async def read_all_books_by_author(author: str, db: Session = Depends(get_db)):
#     return db.query(Book).filter(Book.author.ilike(author)).all()

# @app.get("/books/{book_author}")
# async def read_author_category_by_query(book_author: str, category: str, db: Session = Depends(get_db)):
#     return db.query(Book).filter(Book.author.ilike(book_author), Book.category.ilike(category)).all()

# @app.post("/books/book_create")
# async def create_book(new_book: dict = Body(...), db: Session = Depends(get_db)):
#     db_book = Book(title=new_book["title"], author=new_book["author"], category=new_book["category"])
#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#     return db_book

# @app.put("/books/update_book")
# async def update_book(updated_book: dict = Body(...), db: Session = Depends(get_db)):
#     db_book = db.query(Book).filter(Book.title.ilike(updated_book["title"])).first()
#     if db_book:
#         db_book.title = updated_book["title"]
#         db_book.author = updated_book["author"]
#         db_book.category = updated_book["category"]
#         db.commit()
#         db.refresh(db_book)
#         return db_book
#     return {"error": "Book not found"}

# @app.delete("/books/delete_book/{book_title}")
# async def delete_book(book_title: str, db: Session = Depends(get_db)):
#     db_book = db.query(Book).filter(Book.title.ilike(book_title)).first()
#     if db_book:
#         db.delete(db_book)
#         db.commit()
#         return {"message": "Book deleted"}
#     return {"error": "Book not found"}


@app.get("/books")
async def read_all_books():
    return books

@app.get("/books/{book_title}/")
async def book_title(book_title: str):
    for book in books:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in books:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in books:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/byauthor/")
async def read_all_books_by_author(author: str):
    books_to_return = []
    for book in books:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}")    
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in books:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/book_create")
async def create_book(new_book=Body()):
    books.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(books)):
        if books[i].get("title").casefold() == updated_book.get("title").casefold():
            books[i] = updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(books)):
        if books[i].get("title").casefold() == book_title.casefold():
            books.pop(i)
            break



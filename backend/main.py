from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text

engine = create_engine('postgresql+psycopg2://danylo:6432@localhost/book_tracker')

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

class Book(BaseModel):
    title: str
    author: str   
    year: int
    genre: str   
    rating: int
    date_read: str
    comment: str

app = FastAPI()

@app.post('/books')
async def add_book(book: Book):

    return book
from fastapi import FastAPI
from pydantic import BaseModel

class Book(BaseModel):
    test: str

app = FastAPI()

@app.post('/books')
async def add_book(book: Book):
    return book
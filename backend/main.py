from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.pool import SimpleConnectionPool
import time

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn='dbname=book_tracker user=danylo')

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
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute("select 'hello world'")
    print(cur.fetchone())
    conn.commit()
    cur.close()
    pool.putconn(conn)
    return book
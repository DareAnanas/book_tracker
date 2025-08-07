from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.sql import SQL, Identifier
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
    fields = list(book.dict().keys())
    identifiers = map(Identifier, fields)
    snip = SQL(', ').join(identifiers)
    values = tuple(book.dict().values())
    cur.execute(SQL("""
                insert into books ({})
                values (%s, %s, %s, %s, %s, %s, %s);
                """).format(snip),
                values
                )
    conn.commit()
    cur.close()
    pool.putconn(conn)
    return book
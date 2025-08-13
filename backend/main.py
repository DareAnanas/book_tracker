from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.sql import SQL, Identifier
import time
from datetime import datetime

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn='dbname=book_tracker user=danylo')

def is_valid_iso8601_date(date_str: str) -> bool:
    """
    Check if a string is a valid ISO 8601 date in YYYY-MM-DD format.
    Returns True if valid, False otherwise.
    """
    try:
        # Strictly parse as YYYY-MM-DD
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

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
    if not (book.year >= 1 and book.year <= 9999):
        return {"Error": "Year must be from 1 to 9999"}
    if not (book.rating >= 1 and book.rating <= 5):
        return {"Error": "Rating must be from 1 to 5"}
    if not is_valid_iso8601_date(book.date_read):
        return {"Error": "Date must be in ISO 8601 format"}
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

@app.get('/books')
async def get_books():
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute('select * from books')
    print(cur.fetchall())
    conn.commit()
    cur.close()
    pool.putconn(conn)
    return {'a': 'bababui'}
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

class BookWithId(BaseModel):
    id: int
    title: str
    author: str   
    year: int
    genre: str   
    rating: int
    date_read: str
    comment: str

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    genre: str | None = None
    rating: int | None = None
    date_read: str | None = None
    comment: str | None = None

def convertToBaseModel(book: tuple) -> BookWithId:
    field_names = list(BookWithId.__fields__.keys())
    book_dict = {}
    for i in range(len(book)):
        if field_names[i] == 'date_read':
            book_dict[field_names[i]] = book[i].strftime('%Y-%m-%d')
            continue
        book_dict[field_names[i]] = book[i]
    book = BookWithId(**book_dict)
    return book

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
    cur.execute('select * from books;')
    books = cur.fetchall()
    conn.commit()
    cur.close()
    pool.putconn(conn)
    books = list(map(convertToBaseModel, books))
    return books

@app.put('/books/{id}')
async def update_book(id: int, book: BookUpdate):
    sql_list = []
    values = []
    for field, value in book.dict().items():
        if value != None:
            sql_list.append(SQL('{} = %s').format(Identifier(field)))
            values.append(value)
    if len(values) == 0:
        return {'Update status': 'Nothing updated'}
    snip = SQL(', ').join(sql_list)
    values.append(id)
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute(SQL('update books set {} where id = %s').format(snip), values)
    conn.commit()
    cur.close()
    pool.putconn(conn)
    return {'Update status': f'{len(values) - 1} fields updated'}
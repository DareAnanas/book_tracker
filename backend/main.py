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
    cur.execute("""
                insert into books (title, author, year, genre, rating, date_read, comment) 
                values (%(title)s, %(author)s, %(year)s, %(genre)s, %(rating)s, %(date_read)s, %(comment)s);
                """,
                {
                    'title': book.title,
                    'author': book.author,
                    'year': book.year,
                    'genre': book.genre,
                    'rating': book.rating,
                    'date_read': book.date_read,
                    'comment': book.comment
                }
                )
    conn.commit()
    cur.close()
    pool.putconn(conn)
    return book
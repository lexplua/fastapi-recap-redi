from typing import List, Union, Literal

from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.models.base_models import BookModel
from app.repositories.repository import BookRepository
from app.database import get_db
from app.classwork_functions import add, greet, tell_me_future

application = FastAPI()


@application.get("/books/")
def list_books(field: Literal['title', 'author'] = 'title', order: str = None, db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    return book_repo.list_books(field, order)


@application.post("/books/add")
def create_books(books: Union[BookModel, List[BookModel]], db: Session = Depends(get_db)):
    book_repo = BookRepository(db)

    if isinstance(books, list):
        return book_repo.create_multiple_books(books)
    else:
        return book_repo.create_book(books.title, books.author)


@application.delete("/books/delete")
def delete_book(book: BookModel, db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    return book_repo.delete_book(book)


# classwork
@application.get("/hello/{name}")
def main(name: str):
    return {
        'message': greet(name)
    }


class TwoNumbers(BaseModel):
    a: float
    b: float


@application.post("/sum")
def main(numbers: TwoNumbers):
    return {"result": add(numbers.a, numbers.b)}


@application.get('/add')
def add_two(a: int, b: int):
    return {
        'result': add(a, b)
    }


class QuestionModel(BaseModel):
    question: str


@application.post('/question')
def question(body: QuestionModel):
    return {
        'result': tell_me_future(body.question)
    }

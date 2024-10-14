from typing import List

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.base_models import BookModel
from app.models.db_models import Book


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_book_by_id(self, book_id: int):
        return self.session.query(Book).filter(Book.id == book_id).first()

    def create_book(self, title: str, author: str):
        new_book = Book(title=title, author=author)
        self.session.add(new_book)
        self.session.commit()
        self.session.refresh(new_book)
        return new_book

    def create_multiple_books(self, books: List[BookModel]):
        new_books = [Book(title=book.title, author=book.author) for book in books]
        self.session.add_all(new_books)
        self.session.commit()
        return books

    def list_books(self, field: str, order: str):
        if order == "asc":
            return self.session.query(Book).order_by(asc(getattr(Book, field))).all()
        elif order == "desc":
            return self.session.query(Book).order_by(desc(getattr(Book, field))).all()
        return self.session.query(Book).all()

    def delete_book_by_id(self, book_id: int):
        book = self.session.query(Book).filter(Book.id == book_id).first()
        if book:
            self.session.delete(book)
            self.session.commit()
        return book

    def delete_book(self, book: BookModel):
        book = self.session.query(Book).filter(Book.title == book.title and Book.author == book.author).first()
        if book:
            self.session.delete(book)
            self.session.commit()
        return book

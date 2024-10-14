import math
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from app.classwork import application
from app.database import get_db


@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    return db


@pytest.fixture(autouse=True)
def override_dependency(mock_db):
    application.dependency_overrides[get_db] = lambda: mock_db


client = TestClient(application)


@pytest.mark.parametrize(
    'book_data, status_code, result_data',
    [
        ({"title": "Test Book", "author": "Test Author"}, 200, {"title": "Test Book", "author": "Test Author"}),
        ({"title": "Test Book", "authorr": "Test Author"}, 422, {"title": "Test Book", "author": "Test Author"}),
    ]
)
def test_add_single_book(mock_db, book_data: dict[str, str], status_code, result_data: dict[str, str]):

    response = client.post("/books/add", json=book_data)

    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()["title"] == result_data["title"]
        assert response.json()["author"] == result_data["author"]
        mock_db.add.assert_called_once()


@pytest.mark.parametrize(
    'books_data, status_code, result_data',
    [
        ([{"title": "Book 1", "author": "Author 1"}, {"title": "Book 2", "author": "Author 2"}],
         200, [{"title": "Book 1", "author": "Author 1"}, {"title": "Book 2", "author": "Author 2"}]),
        ([{"titler": "Book 1", "author": "Author 1"}, {"title": "Book 2", "author": "Author 2"}],
         422, [{"title": "Book 1", "author": "Author 1"}, {"title": "Book 2", "author": "Author 2"}])
    ]
)
def test_add_multiple_books(mock_db, books_data, status_code, result_data):

    response = client.post("/books/add", json=books_data)

    assert response.status_code == status_code

    response_json = response.json()
    if status_code == 200:
        assert len(response_json) == len(result_data)
        assert response_json[0]["title"] == result_data[0]["title"]
        assert response_json[1]["title"] == result_data[1]["title"]
        assert response_json[0]["author"] == result_data[0]["author"]
        assert response_json[1]["author"] == result_data[1]["author"]
        mock_db.add_all.assert_called_once()


@pytest.mark.parametrize(
    'field, order, status_code, result_data',
    [
        ('title', 'asc', 200, [{"title": "Book A", "author": "Author X"}, {"title": "Book B", "author": "Author Y"}]),
        ('author', 'desc', 200, [{"title": "Book B", "author": "Author Y"}, {"title": "Book A", "author": "Author X"}]),
        ('unknown_field', None, 422, None)
    ]
)
def test_list_books(mock_db, mocker, field, order, status_code, result_data):
    mock_book_repo = mocker.patch('app.classwork.BookRepository')
    mock_book_repo.return_value.list_books.return_value = result_data if result_data else []

    url = f"/books/?field={field}"
    if order:
        url += f"&order={order}"

    response = client.get(url)

    assert response.status_code == status_code

    if status_code == 200:
        response_json = response.json()
        assert len(response_json) == len(result_data)
        for i, book in enumerate(result_data):
            assert response_json[i]["title"] == book["title"]
            assert response_json[i]["author"] == book["author"]

        mock_book_repo.return_value.list_books.assert_called_once_with(field, order)


def test_main():
    response = client.get('/hello/Kostia')
    assert response.status_code == 200
    body = response.json()
    assert 'message' in body
    assert body['message'] == 'Hello, Kostia'


@pytest.mark.parametrize(
    'a, b, status_code, result',
    [
        (2, 6, 200, 8),
        (2.1, 2, 422, None)

    ]
)
def test_addition(a, b, status_code, result):
    response = client.get('/add', params={'a': a, 'b': b})
    assert response.status_code == status_code
    if status_code == 200:
        body = response.json()
        assert body['result'] == result


@pytest.mark.parametrize(
    'a, b, status_code, result',
    [
        (2.4, 6.4, 200, 8.8),
        (2, 6, 200, 8),
        ('2.1', 6, 200, 8.1),
        ("ff", 2, 422, None)
    ]
)
def test_sum(a, b, status_code, result):
    response = client.post('/sum', json={"a": a, "b": b})
    assert response.status_code == status_code
    if status_code == 200:
        body = response.json()
        assert math.isclose( body['result'], result)

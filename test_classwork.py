from fastapi.testclient import TestClient
import pytest

from classwork import application

client = TestClient(application)


def test_main():
    response = client.get('/hello/Kostia')
    assert response.status_code == 200
    body = response.json()
    assert 'message' in body
    assert body['message'] == 'Hello, Kostia'


# @pytest.mark.parametrize(
#     'a, b, status_code, result',
#     [
#         (2, 6, 200, 8),
#         (2.1, 2, 422, None)
#
#     ]
# )
# def test_addition(a, b, status_code, result):
#     response = client.get('/add', params={'a': a, 'b': b})
#     assert response.status_code == status_code
#     if status_code == 200:
#         body = response.json()
#         assert body['result'] == result


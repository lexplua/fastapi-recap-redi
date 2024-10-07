from fastapi import FastAPI
from pydantic import BaseModel

from classwork_functions import add, greet, tell_me_future

application = FastAPI()


@application.get("/hello/{name}")
def main(name: str):
    return {
        'message': greet(name)
    }


# @application.get('/add')
# def add_two(a: int, b: int):
#     return {
#      'result': add(a, b)
#     }
#
#
# class QuestionModel(BaseModel):
#     question: str
#
#
# @application.post('/question')
# def question(body: QuestionModel):
#     return {
#         'result': tell_me_future(body.question)
#     }

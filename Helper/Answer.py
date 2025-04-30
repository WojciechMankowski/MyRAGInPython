from pydantic import BaseModel

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    question: Question
    answer: str


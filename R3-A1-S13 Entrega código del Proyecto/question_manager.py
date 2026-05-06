import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class QuestionType(Enum):
    TEXT = "texto"
    IMAGE_SEQUENCE = "secuencia_imagenes"


@dataclass
class Question:
    id: str
    question: str
    question_type: QuestionType
    answers: List[str]
    correct_answer: str
    sequence: Optional[List[str]] = None

    def get_shuffled_answers(self):
        answers = self.answers.copy()
        random.shuffle(answers)
        return answers


class QuestionPool:
    def __init__(self, questions):
        self.all_questions = questions
        self.unused_questions = questions.copy()
        random.shuffle(self.unused_questions)

    def get_next_question(self):
        if not self.unused_questions:
            self.unused_questions = self.all_questions.copy()
            random.shuffle(self.unused_questions)
        return self.unused_questions.pop(0)


LABERINTO_QUESTIONS = [
    Question(
        id="q1",
        question="¿Cuánto es 2 + 2?",
        question_type=QuestionType.TEXT,
        answers=["1", "3", "4", "5"],
        correct_answer="4",
    ),
    Question(
        id="q2",
        question="Cuenta de dos en dos: 2, 4, 6, ___",
        question_type=QuestionType.TEXT,
        answers=["7", "8", "9", "10"],
        correct_answer="8",
    ),
    Question(
        id="q3",
        question="Completa la secuencia:",
        question_type=QuestionType.IMAGE_SEQUENCE,
        sequence=[
            "assets/imagenes/Mate-Reto/circulo_azul.png",
            "assets/imagenes/Mate-Reto/circulo_verde.png",
            "assets/imagenes/Mate-Reto/circulo_azul.png",
            "___",
        ],
        answers=[
            "assets/imagenes/Mate-Reto/circulo_amarillo.png",
            "assets/imagenes/Mate-Reto/circulo_verde.png",
            "assets/imagenes/Mate-Reto/circulo_azul.png",
            "assets/imagenes/Mate-Reto/circulo_laberinto.png",
        ],
        correct_answer="assets/imagenes/Mate-Reto/circulo_verde.png",
    ),
]
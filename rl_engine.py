import random

class AdaptiveQuiz:

    def __init__(self):

        # QUESTION BANK (more + structured)
        self.questions = [
            {"question": "What is 2 + 2?", "answer": "4", "difficulty": 1},
            {"question": "What is 5 + 7?", "answer": "12", "difficulty": 1},
            {"question": "What is 10 - 3?", "answer": "7", "difficulty": 1},

            {"question": "What is 6 * 7?", "answer": "42", "difficulty": 2},
            {"question": "What is 15 / 3?", "answer": "5", "difficulty": 2},
            {"question": "What is 9 * 8?", "answer": "72", "difficulty": 2},

            {"question": "Square of 12?", "answer": "144", "difficulty": 3},
            {"question": "Cube of 3?", "answer": "27", "difficulty": 3},
            {"question": "What is 25 * 16?", "answer": "400", "difficulty": 3},
        ]

        self.score = 0
        self.difficulty = 1
        self.used_questions = []

    def get_question(self):

        # filter questions by difficulty
        pool = [
            q for q in self.questions
            if q["difficulty"] == self.difficulty
            and q not in self.used_questions
        ]

        # if no questions left in that difficulty → reset pool
        if not pool:
            self.used_questions = []
            pool = [
                q for q in self.questions
                if q["difficulty"] == self.difficulty
            ]

        question = random.choice(pool)
        self.used_questions.append(question)

        return question

    def update(self, correct):

        if correct:
            self.score += 1
            self.difficulty = min(self.difficulty + 1, 3)
        else:
            self.difficulty = max(self.difficulty - 1, 1)
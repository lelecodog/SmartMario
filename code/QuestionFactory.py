import random


class QuestionFactory:
    def __init__(self, min_val=1, max_val=10):
        self.min_val = min_val
        self.max_val = max_val

    def generate_question(self):
        a = random.randint(self.min_val, self.max_val)
        b = random.randint(self.min_val, self.max_val)
        correct = a + b
        question_text = f"{a} + {b} = "

        # Gera duas respostas erradas diferentes
        wrong1 = correct + random.choice([-3, -2, -1, 1, 2, 3])
        wrong2 = correct + random.choice([-3, -2, -1, 1, 2, 3])
        while wrong1 == correct or wrong2 == correct or wrong1 == wrong2:
            wrong1 = correct + random.randint(-5, 5)
            wrong2 = correct + random.randint(-5, 5)

        # Embaralha as respostas
        options = [correct, wrong1, wrong2]
        random.shuffle(options)

        return {
            "question": question_text,
            "correct": correct,
            "options": options
        }


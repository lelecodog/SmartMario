import random


class QuestionFactory:
    @staticmethod
    def generate_question(min_val, max_val, operations):
        op = random.choice(operations)
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)

        if op == "/":
            b = random.randint(1, max_val)
            correct = random.randint(min_val, max_val)
            a = b * correct
            question_text = f"{a} ÷ {b} = "

        elif op == "+":
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            correct = a + b
            question_text = f"{a} + {b} = "

        elif op == "-":
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, a)
            correct = a - b
            question_text = f"{a} - {b} = "

        elif op == "*":
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            correct = a * b
            question_text = f"{a} × {b} = "

        # Generate wrong answers
        wrong1 = correct + random.choice([-3, -2, -1, 1, 2, 3])
        wrong2 = correct + random.choice([-3, -2, -1, 1, 2, 3])
        while wrong1 == correct or wrong2 == correct or wrong1 == wrong2:
            wrong1 = correct + random.randint(-5, 5)
            wrong2 = correct + random.randint(-5, 5)

        options = [correct, wrong1, wrong2]
        random.shuffle(options)

        return {
            "question": question_text,
            "correct": correct,
            "options": options
        }

from typing import List

class InterviewEngine:
    def __init__(self, questions: List[str]):
        self.questions = questions
        self.answers = []
        self.current = 0

    def start(self):
        print("\n--- AI Interview Simulation ---\n")
        while self.current < len(self.questions):
            print(f"Q{self.current+1}: {self.questions[self.current]}")
            answer = input("Your answer: ")
            self.answers.append({'question': self.questions[self.current], 'answer': answer})
            self.current += 1
        print("\nInterview complete! Thank you for participating.\n")

    def get_results(self):
        return self.answers

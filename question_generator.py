import random
from typing import List, Dict
import nltk

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

class QuestionGenerator:
    def __init__(self, parsed_resume: Dict[str, List[str]]):
        self.skills = parsed_resume.get('skills', [])
        self.experience = parsed_resume.get('experience', [])
        self.projects = parsed_resume.get('projects', [])
        self.technologies = parsed_resume.get('technologies', [])
        self.roles = parsed_resume.get('roles', [])

    def generate_technical_questions(self, difficulty: str) -> List[str]:
        questions = []
        for skill in self.skills:
            if difficulty == 'Easy':
                questions.append(f"What is {skill}?")
            elif difficulty == 'Medium':
                questions.append(f"How have you applied {skill} in your work?")
            elif difficulty == 'Hard':
                questions.append(f"Describe a challenging problem you solved using {skill}.")
        for tech in self.technologies:
            if difficulty == 'Easy':
                questions.append(f"Explain the basics of {tech}.")
            elif difficulty == 'Medium':
                questions.append(f"How would you compare {tech} to other technologies?")
            elif difficulty == 'Hard':
                questions.append(f"Describe an advanced use case for {tech}.")
        return questions

    def generate_behavioral_questions(self, difficulty: str) -> List[str]:
        templates = {
            'Easy': [
                "Tell me about yourself.",
                "What motivates you at work?"
            ],
            'Medium': [
                "Describe a time you worked in a team.",
                "How do you handle feedback?"
            ],
            'Hard': [
                "Tell me about a time you failed and what you learned.",
                "Describe a situation where you had to lead under pressure."
            ]
        }
        return templates.get(difficulty, [])

    def generate_project_questions(self, difficulty: str) -> List[str]:
        questions = []
        for project in self.projects:
            if difficulty == 'Easy':
                questions.append(f"What was the goal of the project: '{project[:60]}...'? ")
            elif difficulty == 'Medium':
                questions.append(f"What challenges did you face in the project: '{project[:60]}...'? ")
            elif difficulty == 'Hard':
                questions.append(f"How did you ensure the success of the project: '{project[:60]}...'? ")
        return questions

    def generate_all_questions(self, difficulty: str) -> List[str]:
        questions = []
        questions.extend(self.generate_technical_questions(difficulty))
        questions.extend(self.generate_behavioral_questions(difficulty))
        questions.extend(self.generate_project_questions(difficulty))
        random.shuffle(questions)
        return questions

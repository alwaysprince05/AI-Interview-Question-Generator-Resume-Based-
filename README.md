# 🤖 AI Interview Question Generator — Resume Based

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/NLP-spaCy%20%7C%20NLTK-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Made%20by-alwaysprince05-purple?style=for-the-badge" />
</p>

---

## 📌 About

**AI Interview Question Generator** is a Python-based terminal application that intelligently analyzes a candidate's resume (PDF or TXT) and auto-generates personalized interview questions. It uses **NLP (spaCy + NLTK)** and rule-based logic to extract skills, experience, projects, and technologies — then creates **technical**, **behavioral**, and **project-based** questions tailored to the resume content.

No paid APIs. No internet required at runtime. Just pure Python intelligence.

---

## ✨ Features

- 📄 **Resume Parsing** — Supports both PDF and plain-text `.txt` resumes
- 🧠 **Smart Extraction** — Extracts skills, technologies, experience, roles, and projects using NLP
- ❓ **Question Generation** — Generates technical, behavioral, and project-based questions
- 🎯 **Difficulty Levels** — Choose from Easy, Medium, or Hard questions
- 🎤 **Interview Simulation** — Simulates a real interview: questions are asked one by one, you type your answers
- 🐍 **100% Python** — No paid APIs, no external services needed

---

## 📁 Project Structure

```
AI-Interview-Question-Generator-Resume-Based-/
│
├── main.py                  # Entry point — runs the interview flow
├── resume_parser.py         # Parses resume and extracts key data using spaCy + regex
├── question_generator.py    # Generates questions based on extracted resume data
├── interview_engine.py      # Simulates the interview session
├── utils.py                 # Utility functions (file checks, keyword loading)
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/alwaysprince05/AI-Interview-Question-Generator-Resume-Based-.git
cd AI-Interview-Question-Generator-Resume-Based-
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download NLTK data *(first run only)*

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### 4. Download spaCy model *(first run only)*

```bash
python -m spacy download en_core_web_sm
```

---

## 🚀 How to Run

```bash
python main.py
```

You'll be prompted to:
1. Enter the path to your resume (PDF or TXT)
2. Select question difficulty: **Easy / Medium / Hard**
3. The interview begins — answer questions one by one in the terminal

---

## 🔧 How to Extend

| File | What to Modify |
|---|---|
| `question_generator.py` | Add new question templates or categories |
| `resume_parser.py` | Improve NLP extraction or add new fields |
| `interview_engine.py` | Add scoring, timer, or feedback features |
| `utils.py` | Add new keyword lists or utility helpers |

---

## 📦 Requirements

```
pdfminer.six
spacy
nltk
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**alwaysprince05**
- GitHub: [@alwaysprince05](https://github.com/alwaysprince05)

---

> *Built with ❤️ using Python, spaCy, and NLTK*

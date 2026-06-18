import os
import sys
import json
import uuid
import random
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def try_parse_resume(path):
    """Try to parse resume using spaCy, fallback to simple text parsing."""
    try:
        from resume_parser import ResumeParser
        parser = ResumeParser(path)
        return parser.parse()
    except Exception:
        return simple_parse(path)

def simple_parse(path):
    """Simple fallback parser when spaCy/pdfminer not available."""
    text = ""
    if path.lower().endswith('.pdf'):
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(path)
        except Exception:
            text = ""
    else:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception:
            text = ""

    import re
    skill_kw = ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL', 'HTML', 'CSS',
                'React', 'Node.js', 'Django', 'Flask', 'Machine Learning', 'Deep Learning',
                'TensorFlow', 'PyTorch', 'NLP', 'Data Science', 'AWS', 'Docker', 'Git',
                'MongoDB', 'PostgreSQL', 'REST API', 'TypeScript', 'Kotlin', 'Swift']
    found_skills = [s for s in skill_kw if re.search(r'\b' + re.escape(s) + r'\b', text, re.IGNORECASE)]

    tech_kw = ['React', 'Node.js', 'Django', 'Flask', 'TensorFlow', 'PyTorch',
               'Docker', 'Kubernetes', 'AWS', 'Azure', 'MongoDB', 'PostgreSQL', 'MySQL']
    found_tech = [t for t in tech_kw if re.search(r'\b' + re.escape(t) + r'\b', text, re.IGNORECASE)]

    return {
        'skills': found_skills if found_skills else ['Problem Solving', 'Communication', 'Teamwork'],
        'experience': [],
        'projects': [],
        'technologies': found_tech if found_tech else [],
        'roles': []
    }

def generate_questions(parsed, difficulty):
    """Generate interview questions from parsed resume data."""
    questions = []

    # Technical questions from skills
    for skill in parsed.get('skills', []):
        if difficulty == 'Easy':
            questions.append({'text': f"What is {skill} and what are its main use cases?", 'type': 'Technical', 'category': 'Skills'})
        elif difficulty == 'Medium':
            questions.append({'text': f"How have you applied {skill} in your work or projects?", 'type': 'Technical', 'category': 'Skills'})
        elif difficulty == 'Hard':
            questions.append({'text': f"Describe a complex, challenging problem you solved using {skill}.", 'type': 'Technical', 'category': 'Skills'})

    # Tech questions
    for tech in parsed.get('technologies', []):
        if difficulty == 'Easy':
            questions.append({'text': f"Explain the basics of {tech}.", 'type': 'Technical', 'category': 'Technology'})
        elif difficulty == 'Medium':
            questions.append({'text': f"How would you compare {tech} to alternative technologies?", 'type': 'Technical', 'category': 'Technology'})
        elif difficulty == 'Hard':
            questions.append({'text': f"Describe an advanced, production-level use case for {tech}.", 'type': 'Technical', 'category': 'Technology'})

    # Behavioral questions
    behavioral = {
        'Easy': [
            {'text': "Tell me about yourself and your background.", 'type': 'Behavioral', 'category': 'Personal'},
            {'text': "What are your greatest strengths?", 'type': 'Behavioral', 'category': 'Personal'},
            {'text': "Why are you interested in this role?", 'type': 'Behavioral', 'category': 'Motivation'},
        ],
        'Medium': [
            {'text': "Describe a time you worked effectively in a team to achieve a goal.", 'type': 'Behavioral', 'category': 'Teamwork'},
            {'text': "How do you handle constructive feedback from peers or managers?", 'type': 'Behavioral', 'category': 'Growth'},
            {'text': "Tell me about a time you managed multiple priorities simultaneously.", 'type': 'Behavioral', 'category': 'Time Management'},
        ],
        'Hard': [
            {'text': "Tell me about a significant failure you experienced and what you learned from it.", 'type': 'Behavioral', 'category': 'Resilience'},
            {'text': "Describe a situation where you had to lead a team under high pressure with tight deadlines.", 'type': 'Behavioral', 'category': 'Leadership'},
            {'text': "How have you influenced a team or organization to adopt a new process or technology?", 'type': 'Behavioral', 'category': 'Leadership'},
        ]
    }
    questions.extend(behavioral.get(difficulty, []))

    # Project questions
    for proj in parsed.get('projects', []):
        snippet = proj[:80] + '...' if len(proj) > 80 else proj
        if difficulty == 'Easy':
            questions.append({'text': f"What was the goal of this project: \"{snippet}\"?", 'type': 'Project', 'category': 'Projects'})
        elif difficulty == 'Medium':
            questions.append({'text': f"What challenges did you face in: \"{snippet}\"?", 'type': 'Project', 'category': 'Projects'})
        elif difficulty == 'Hard':
            questions.append({'text': f"How did you measure success and handle trade-offs in: \"{snippet}\"?", 'type': 'Project', 'category': 'Projects'})

    random.shuffle(questions)
    return questions[:15]  # Cap at 15 questions


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resume']
    difficulty = request.form.get('difficulty', 'Easy')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF and TXT files are supported'}), 400

    filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    parsed = try_parse_resume(filepath)
    questions = generate_questions(parsed, difficulty)

    if not questions:
        return jsonify({'error': 'Could not generate questions from this resume. Try a different file.'}), 400

    session['questions'] = questions
    session['current'] = 0
    session['answers'] = []
    session['difficulty'] = difficulty
    session['parsed'] = {k: v[:5] for k, v in parsed.items() if isinstance(v, list)}
    session['filename'] = file.filename

    # Clean up uploaded file
    try:
        os.remove(filepath)
    except Exception:
        pass

    return jsonify({'redirect': url_for('interview')})


@app.route('/interview')
def interview():
    if 'questions' not in session or not session['questions']:
        return redirect(url_for('index'))
    return render_template('interview.html',
                           total=len(session['questions']),
                           difficulty=session.get('difficulty', 'Easy'),
                           parsed=session.get('parsed', {}),
                           filename=session.get('filename', 'Your Resume'))


@app.route('/question', methods=['GET'])
def get_question():
    questions = session.get('questions', [])
    idx = session.get('current', 0)
    if idx >= len(questions):
        return jsonify({'done': True, 'answers': session.get('answers', [])})
    q = questions[idx]
    return jsonify({
        'done': False,
        'index': idx,
        'total': len(questions),
        'question': q['text'],
        'type': q['type'],
        'category': q['category']
    })


@app.route('/answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    answer = data.get('answer', '').strip()
    questions = session.get('questions', [])
    idx = session.get('current', 0)

    if idx < len(questions):
        answers = session.get('answers', [])
        answers.append({
            'question': questions[idx]['text'],
            'type': questions[idx]['type'],
            'category': questions[idx]['category'],
            'answer': answer
        })
        session['answers'] = answers
        session['current'] = idx + 1

    next_idx = session.get('current', 0)
    if next_idx >= len(questions):
        return jsonify({'done': True})
    
    next_q = questions[next_idx]
    return jsonify({
        'done': False,
        'index': next_idx,
        'total': len(questions),
        'question': next_q['text'],
        'type': next_q['type'],
        'category': next_q['category']
    })


@app.route('/results')
def results():
    answers = session.get('answers', [])
    difficulty = session.get('difficulty', 'Easy')
    if not answers:
        return redirect(url_for('index'))
    return render_template('results.html', answers=answers, difficulty=difficulty, total=len(answers))


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

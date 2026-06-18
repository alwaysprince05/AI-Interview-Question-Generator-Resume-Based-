import os

def load_skill_keywords():
    # A basic list of common skills (expand as needed)
    return [
        'python', 'java', 'c++', 'machine learning', 'deep learning', 'nlp', 'data analysis',
        'project management', 'sql', 'excel', 'communication', 'leadership', 'teamwork',
        'problem solving', 'cloud', 'aws', 'azure', 'docker', 'kubernetes', 'git', 'linux',
        'javascript', 'react', 'node.js', 'html', 'css', 'tensorflow', 'pytorch', 'scikit-learn',
        'pandas', 'numpy', 'matplotlib', 'flask', 'django', 'fastapi', 'agile', 'scrum', 'jira'
    ]

def load_technology_keywords():
    return [
        'python', 'java', 'c++', 'aws', 'azure', 'docker', 'kubernetes', 'git', 'linux',
        'javascript', 'react', 'node.js', 'html', 'css', 'tensorflow', 'pytorch', 'scikit-learn',
        'pandas', 'numpy', 'matplotlib', 'flask', 'django', 'fastapi', 'sql', 'mongodb', 'mysql',
        'postgresql', 'redis', 'jira', 'agile', 'scrum'
    ]

def load_role_keywords():
    return [
        'software engineer', 'data scientist', 'project manager', 'developer', 'analyst',
        'consultant', 'intern', 'team lead', 'researcher', 'architect', 'qa engineer',
        'product manager', 'business analyst', 'devops engineer', 'frontend developer',
        'backend developer', 'full stack developer', 'ai engineer', 'ml engineer', 'nlp engineer'
    ]

def file_exists(filepath):
    return os.path.isfile(filepath)

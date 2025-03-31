import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import json
import requests
import ast
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)

# OpenRouter API Configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("API key not found! Set OPENROUTER_API_KEY in environment variables.")

# Knowledge files
KNOWLEDGE_FILES = {
    "fluent": "fluent.json",
    "altius": "altius.json"
}

# Maximum number of questions to generate
MAX_QUESTIONS = 10

def load_knowledge(file_path):
    """Load and return the knowledge base from a JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def parse_ai_response(response_text):
    """
    Attempt to parse the AI response into a list of quiz questions.
    Uses multiple parsing strategies to handle different response formats.
    """
    try:
        return json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        pass
    try:
        return ast.literal_eval(response_text)
    except (SyntaxError, ValueError):
        pass
    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    try:
        question_blocks = re.split(r'\d+\.', response_text)[1:]
        parsed_questions = []
        
        for block in question_blocks:
            lines = block.strip().split('\n')
            question = lines[0].strip()
            options = [line.strip() for line in lines[1:5] if line.strip()]
            correct_answer = next((opt for opt in options if '*' in opt), options[0])
            correct_answer = correct_answer.replace('*', '').strip()
            parsed_questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_answer
            })
        return parsed_questions
    except Exception as e:
        print(f"Failed to parse response: {e}")
        return None

def generate_questions(concept):
    """Generate quiz questions using OpenRouter API"""
    prompt = (
        f"Generate 2-3 multiple choice questions about the blockchain concept: {concept['title']}\n"
        f"Description: {concept['description']}\n"
        f"Details: {concept['details']}\n\n"
        "Please provide the response in a strict JSON format with the following structure:\n"
        "[{\n"
        "  'question': 'Question text here',\n"
        "  'options': ['Option A', 'Option B', 'Option C', 'Option D'],\n"
        "  'correct_answer': 'Correct option text'\n"
        "}]\n"
        "Ensure the JSON is properly formatted and valid."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://your-site-url.com",
        "X-Title": "Blockchain Quiz App",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "system", "content": "You are an AI generating structured quiz questions. Always respond in valid JSON format."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        ai_response = response.json()['choices'][0]['message']['content']
        return parse_ai_response(ai_response)
    except Exception as e:
        print(f"OpenRouter API Error: {e}")
        return None

@app.route("/")
def index():
    """Serve the HTML frontend"""
    return render_template("index.html")

@app.route("/generate", methods=["GET"])
def generate():
    """Fetch quiz questions dynamically"""
    source = request.args.get("source")
    if source not in KNOWLEDGE_FILES:
        return jsonify({"error": "Invalid source"}), 400
    
    knowledge_base = load_knowledge(KNOWLEDGE_FILES[source])
    if not knowledge_base:
        return jsonify({"error": "Could not load knowledge base"}), 500
    
    questions = []
    for concept in knowledge_base:
        q = generate_questions(concept)
        if q:
            questions.extend(q)
            if len(questions) >= MAX_QUESTIONS:
                questions = questions[:MAX_QUESTIONS]
                break
    
    return jsonify(questions)

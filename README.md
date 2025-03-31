# Flask Quiz App

A web-based quiz application that generates dynamic multiple-choice questions using OpenRouter AI. The app fetches questions from a knowledge base and serves them through a simple Flask web interface.

## Features
- 🧠 AI-generated multiple-choice questions
- 📚 Supports multiple knowledge sources
- ⚡ Fast and lightweight Flask backend
- 🌍 Easy deployment on Render

---

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- Git

### Clone the Repository
```bash
git clone https://github.com/mystic0137/flask-quiz-app.git
cd flask-quiz-app
```

### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your-api-key-here
```

---

## Running Locally
```bash
flask run --host=0.0.0.0 --port=5000
```
Then, visit `http://127.0.0.1:5000` in your browser.

---

## Deployment on Render
1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Deploy-ready Flask quiz app"
   git push origin master
   ```
2. Go to [Render](https://dashboard.render.com/) and create a **New Web Service**.
3. Connect your GitHub repository.
4. Use the following configurations:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
5. Click **Deploy** and wait for your app to go live!

---

## API Endpoints

| Method | Endpoint      | Description                         |
|--------|--------------|-------------------------------------|
| GET    | `/`          | Renders the homepage               |
| GET    | `/generate`  | Returns AI-generated quiz questions |

---

## License
This project is licensed under the MIT License.

---

## Author
👤 **mystic0137**

Enjoy the app! 🚀


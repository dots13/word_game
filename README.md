# Dutch Word Game 🎮🇳🇱

A small word game for practicing Dutch vocabulary, developed as part of a language course and deployed using Render.

## 🚀 Live Demo
[Play the game](https://word-game-3raq.onrender.com/)

## 📌 Features

- Fetches words from an Airtable database.

- Provides different game modes:
  - Quiz Mode: Randomly tests vocabulary knowledge.
  - Matching Mode: Players match Dutch words with their English translations.
  - De/Hat Mode: Helps practice the correct use of Dutch articles (de and het).

- Caches word data for efficiency.
## 🛠️ Technologies Used

- Python (Flask)
- Airtable API
- Pandas
- HTML, CSS (Jinja templates for rendering)
- JavaScript (for interactivity)
- Render (for deployment)

## ⚙️ Installation
1. Clone this repository:
```py sh
git clone https://github.com/yourusername/word-game.git
cd word-game
```
2. Create a virtual environment and install dependencies:
sh
```py sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. Create a .env file with your Airtable credentials:
```py sh
AIRTABLE_API_KEY=your_api_key
BASE_ID=your_base_id
TABLE_NAME=your_table_name
```
4. Run the Flask app:
```py sh
python app.py
```

## 📡 API Endpoints
- /get_lessons - Fetch available lessons
- /get_word_list - Get the full word list
- /get_words?lesson=X&mode=Y - Get words for a specific lesson and mode

## 🚀 Deployment
This app is deployed on Render. To deploy yourself:
1. Push your repository to GitHub.
2. Create a new Render Web Service with:
  - Start Command: gunicorn app:app
  - Environment Variables: Add AIRTABLE_API_KEY, BASE_ID, and TABLE_NAME.
# 📜 License
MIT License.

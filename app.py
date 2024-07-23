from flask import Flask, render_template, jsonify, request
import pandas as pd
import requests
import random
import os
from dotenv import load_dotenv
from threading import Lock

# Load environment variables from .env file
load_dotenv()

# Flask application setup
app = Flask(__name__)

# Airtable configuration
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
AIRTABLE_URL = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}'

HEADERS = {
    'Authorization': f'Bearer {AIRTABLE_API_KEY}',
    'Content-Type': 'application/json'
}

# Data caching
data_cache = None
cache_lock = Lock()

def fetch_from_airtable():
    url = AIRTABLE_URL
    all_records = []
    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        all_records.extend(data['records'])
        url = data.get('offset')
        if url:
            url = f'{AIRTABLE_URL}?offset={url}'
    return all_records

def load_words():
    global data_cache
    with cache_lock:
        if data_cache is None:
            records = fetch_from_airtable()
            df = [
                {
                    'Lesson': record['fields'].get('Lesson', ''),
                    'Dutch': record['fields'].get('Dutch', ''),
                    'English': record['fields'].get('English', '')
                }
                for record in records
            ]
            data_cache = pd.DataFrame(df)
    sorted_df = data_cache.sort_values(by='Dutch')
    return sorted_df

def get_random_subset(de_words, het_words):
    random.shuffle(de_words)
    needed_count = len(het_words)
    random_subset = de_words[:needed_count]
    return random_subset


@app.route('/')
def index():
    lessons = load_words()['Lesson'].unique().tolist()
    return render_template('index.html', lessons=lessons)


@app.route('/get_lessons', methods=['GET'])
def get_lessons():
    df = load_words()
    lessons = df['Lesson'].unique().tolist()
    lessons = sorted(map(int, lessons))
    return jsonify({'lessons': lessons})


@app.route('/get_word_list', methods=['GET'])
def get_word_list():
    df = load_words()
    word_list = df.to_dict(orient='records')
    return jsonify(word_list)


@app.route('/get_words', methods=['GET'])
def get_words():
    lesson = request.args.get('lesson')
    mode = request.args.get('mode')
    df = load_words()
    words = df[df['Lesson'] == int(lesson)].to_dict(orient='records')
    if mode == 'quiz':
        return jsonify(random.sample(words, len(words)))
    elif mode == 'match':
        selected_words = random.sample(words, min(8, len(words)))
        pairs = [{'word': word['Dutch'], 'lang': 'Dutch', 'translation': word['English']} for word in selected_words] + [
            {'word': word['English'], 'lang': 'English', 'translation': word['Dutch']} for word in selected_words]
        random.shuffle(pairs)
        return jsonify(pairs)
    elif mode == 'de_het':
        de_words = [entry['Dutch'] for entry in words if '(de)' in entry['Dutch']]
        het_words = [entry['Dutch'] for entry in words if '(het)' in entry['Dutch']]
        de_subset = get_random_subset(de_words, het_words)
        all_words = de_subset + het_words
        questions = [{'word': word.split('(')[0].strip(), 'article': 'de' if word in de_words else 'het'} for word in all_words]
        return jsonify(questions)
    return jsonify(words)

if __name__ == '__main__':
    app.run(debug=True)


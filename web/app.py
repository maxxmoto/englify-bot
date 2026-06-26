import random
import sys
import os
from grammar import GRAMMAR_LEVELS
from flask import Flask, render_template, jsonify, request

# Подтягиваем модули из папки бота
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from content import get_daily_word, generate_tasks
from irregular_verbs import IRREGULAR_VERBS

app = Flask(__name__)

@app.after_request
def add_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response

@app.route('/')
def index():
    from test_data import TEST_QUESTIONS
    today = 0  # или реальный день года
    word = get_daily_word(today)
    return render_template('index.html', word=word, test_questions=TEST_QUESTIONS)

@app.route('/tasks')
def tasks_page():
    return render_template('tasks.html')

@app.route('/verbs')
def verbs_page():
    verbs = random.sample(IRREGULAR_VERBS, min(10, len(IRREGULAR_VERBS)))
    return render_template('verbs.html', verbs=verbs)

@app.route('/words')
def words_page():
    return render_template('words.html')

# API: генерация заданий на лету (по уровню и дню)
@app.route('/api/tasks')
def api_tasks():
    level = request.args.get('level', 'novice')
    day = request.args.get('day', 0, type=int)
    tasks = generate_tasks(day, level)
    return jsonify(tasks)

# API: проверка ответа
@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    correct_idx = data.get('correct')
    chosen = data.get('chosen')
    return jsonify({'result': correct_idx == chosen})

# API: отдать MP3 голосового сообщения (на сервере)
@app.route('/voice/<word>')
def voice(word):
    from gtts import gTTS
    import io
    tts = gTTS(text=word, lang='en')
    audio = io.BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)
    return audio.read(), 200, {'Content-Type': 'audio/mpeg'}

# страница теста
@app.route('/test')
def test_page():
    from test_data import TEST_QUESTIONS
    return render_template('test.html', questions=TEST_QUESTIONS)

@app.route('/pro')
def pro_page():
    return render_template('pro.html')

@app.route('/grammar')
def grammar_levels():
    return render_template('grammar_levels.html', levels=GRAMMAR_LEVELS)

@app.route('/grammar/<level>')
def grammar_topic_list(level):
    if level not in GRAMMAR_LEVELS:
        return redirect(url_for('grammar_levels'))
    topics = GRAMMAR_LEVELS[level]['topics']
    return render_template('grammar_topics.html', level=level, topics=topics, level_title=GRAMMAR_LEVELS[level]['title'])

@app.route('/grammar/<level>/<int:topic_id>')
def grammar_topic(level, topic_id):
    if level not in GRAMMAR_LEVELS:
        return redirect(url_for('grammar_levels'))
    topic = None
    for t in GRAMMAR_LEVELS[level]['topics']:
        if t['id'] == topic_id:
            topic = t
            break
    if not topic:
        return redirect(url_for('grammar_topic_list', level=level))
    return render_template('grammar_topic.html', level=level, topic=topic)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
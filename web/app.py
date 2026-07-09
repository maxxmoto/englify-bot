import sys
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from db_data import get_word, get_verbs, get_test_questions, get_grammar_levels, init_tables, populate_if_empty
from ege import get_all_ege_tasks, get_ege_task, check_ege_answer
from reading import get_all_articles, get_article

# Подтягиваем модули из папки бота
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from content import generate_tasks

app = Flask(__name__)

@app.after_request
def add_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/')
def index():
    today = 0
    word = get_word(today)
    return render_template('index.html', word=word, test_questions=get_test_questions())

@app.route('/tasks')
def tasks_page():
    return render_template('tasks.html')

@app.route('/verbs')
def verbs_page():
    verbs = get_verbs(10)
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
    return render_template('test.html', questions=get_test_questions())

@app.route('/reading')
def reading_page():
    return render_template('reading.html', articles=get_all_articles())

@app.route('/reading/<int:article_id>')
def reading_article(article_id):
    article = get_article(article_id)
    if not article:
        return redirect(url_for('reading_page'))
    return render_template('reading_article.html', article=article)

@app.route('/pro')
def pro_page():
    return render_template('pro.html')

@app.route('/ege')
def ege_page():
    tasks = get_all_ege_tasks()
    return render_template('ege.html', tasks=tasks)

@app.route('/ege/<int:task_id>')
def ege_task_page(task_id):
    task = get_ege_task(task_id)
    if not task:
        return redirect(url_for('ege_page'))
    return render_template('ege_task.html', task=task)

@app.route('/api/ege_check', methods=['POST'])
def ege_check():
    data = request.get_json()
    task = get_ege_task(data.get('task_id'))
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    answers = data.get('answers', [])
    correct, total, results = check_ege_answer(task, answers)
    return jsonify({'correct': correct, 'total': total, 'results': results})

@app.route('/grammar')
def grammar_levels():
    gl = get_grammar_levels()
    return render_template('grammar_levels.html', levels=gl)

@app.route('/grammar/<level>')
def grammar_topic_list(level):
    gl = get_grammar_levels()
    if level not in gl:
        return redirect(url_for('grammar_levels'))
    return render_template('grammar_topics.html', level=level, topics=gl[level]['topics'], level_title=gl[level]['title'])

@app.route('/grammar/<level>/<int:topic_id>')
def grammar_topic(level, topic_id):
    gl = get_grammar_levels()
    if level not in gl:
        return redirect(url_for('grammar_levels'))
    topic = None
    for t in gl[level]['topics']:
        if t['id'] == topic_id:
            topic = t
            break
    if not topic:
        return redirect(url_for('grammar_topic_list', level=level))
    return render_template('grammar_topic.html', level=level, topic=topic)


if __name__ == '__main__':
    init_tables()
    populate_if_empty()
    app.run(debug=True, port=5000)
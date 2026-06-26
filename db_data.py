import sqlite3
import json
import random
import sys, os
from content import WORDS_OF_DAY
from irregular_verbs import IRREGULAR_VERBS
from test_data import TEST_QUESTIONS

DB_PATH = "englify.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_tables():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY,
        word TEXT NOT NULL,
        translation TEXT NOT NULL,
        example TEXT NOT NULL,
        example_translation TEXT NOT NULL,
        day_index INTEGER UNIQUE
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS irregular_verbs (
        id INTEGER PRIMARY KEY,
        v1 TEXT NOT NULL,
        v2 TEXT NOT NULL,
        v3 TEXT NOT NULL,
        translation TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS test_questions (
        id INTEGER PRIMARY KEY,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        correct INTEGER NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS grammar_levels (
        id INTEGER PRIMARY KEY,
        level TEXT NOT NULL,
        title TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS grammar_topics (
        id INTEGER PRIMARY KEY,
        level_id INTEGER,
        title TEXT NOT NULL,
        questions TEXT NOT NULL,
        FOREIGN KEY(level_id) REFERENCES grammar_levels(id)
    )''')
    conn.commit()
    conn.close()

def populate_if_empty():
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM words")
    if c.fetchone()[0] == 0:
        for i, w in enumerate(WORDS_OF_DAY):
            c.execute(
                "INSERT INTO words (word, translation, example, example_translation, day_index) VALUES (?,?,?,?,?)",
                (w["word"], w["translation"], w["example"], w["example_translation"], i)
            )

    c.execute("SELECT COUNT(*) FROM irregular_verbs")
    if c.fetchone()[0] == 0:
        for v in IRREGULAR_VERBS:
            c.execute(
                "INSERT INTO irregular_verbs (v1, v2, v3, translation) VALUES (?,?,?,?)",
                (v["v1"], v["v2"], v["v3"], v["translation"])
            )

    c.execute("SELECT COUNT(*) FROM test_questions")
    if c.fetchone()[0] == 0:
        for q in TEST_QUESTIONS:
            c.execute(
                "INSERT INTO test_questions (question, options, correct) VALUES (?,?,?)",
                (q["question"], json.dumps(q["options"]), q["correct"])
            )

    c.execute("SELECT COUNT(*) FROM grammar_levels")
    if c.fetchone()[0] == 0:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'web'))
        from grammar import GRAMMAR_LEVELS
        for level_key, level_data in GRAMMAR_LEVELS.items():
            c.execute("INSERT INTO grammar_levels (level, title) VALUES (?,?)",
                      (level_key, level_data["title"]))
            level_id = c.lastrowid
            for topic in level_data["topics"]:
                c.execute("INSERT INTO grammar_topics (level_id, title, questions) VALUES (?,?,?)",
                          (level_id, topic["title"], json.dumps(topic.get("questions", []))))

    conn.commit()
    conn.close()

    # EGE tables
    from ege import init_ege_table, populate_ege
    init_ege_table()
    populate_ege()

def get_word(day_index):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT word, translation, example, example_translation FROM words WHERE day_index = ?",
              (day_index % len(WORDS_OF_DAY),))
    row = c.fetchone()
    conn.close()
    if row:
        return {"word": row[0], "translation": row[1], "example": row[2], "example_translation": row[3]}
    return WORDS_OF_DAY[day_index % len(WORDS_OF_DAY)]

def get_verbs(count=10):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT v1, v2, v3, translation FROM irregular_verbs ORDER BY RANDOM() LIMIT ?", (count,))
    rows = c.fetchall()
    conn.close()
    if rows:
        return [{"v1": r[0], "v2": r[1], "v3": r[2], "translation": r[3]} for r in rows]
    return random.sample(IRREGULAR_VERBS, min(count, len(IRREGULAR_VERBS)))

def get_all_verbs():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT v1, v2, v3, translation FROM irregular_verbs")
    rows = c.fetchall()
    conn.close()
    if rows:
        return [{"v1": r[0], "v2": r[1], "v3": r[2], "translation": r[3]} for r in rows]
    return IRREGULAR_VERBS

def get_test_questions():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT question, options, correct FROM test_questions ORDER BY id")
    rows = c.fetchall()
    conn.close()
    if rows:
        return [{"question": r[0], "options": json.loads(r[1]), "correct": r[2]} for r in rows]
    return TEST_QUESTIONS

def get_grammar_levels():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, level, title FROM grammar_levels ORDER BY id")
    levels = c.fetchall()
    result = {}
    for lid, lkey, ltitle in levels:
        c.execute("SELECT id, title, questions FROM grammar_topics WHERE level_id = ? ORDER BY id", (lid,))
        topics = []
        for tid, ttitle, tquestions in c.fetchall():
            topics.append({"id": tid, "title": ttitle, "questions": json.loads(tquestions) if tquestions else []})
        result[lkey] = {"title": ltitle, "topics": topics}
    conn.close()
    if result:
        return result
    return GRAMMAR_LEVELS

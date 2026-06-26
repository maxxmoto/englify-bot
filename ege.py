"""EGE tasks data module - extracted from Zadania_FIPI_EGE_2024.pdf"""
import json
import sqlite3

DB_PATH = "englify.db"

EGE_TASKS = [
    {
        "id": 1, "type": 1, "theme": "New Year",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7. Используйте каждую цифру только один раз.",
        "items": ["A", "B", "C", "D", "E", "F"],
        "headings": [
            "Celebrating New Year has a long history.",
            "There are extravagant ways to celebrate New Year.",
            "Good food is the most important thing for New Year.",
            "New Year is the best time for new beginnings.",
            "Properly preparing before New Year is important.",
            "New Year is a great time to be with your relatives.",
            "You don't need a special time to start something."
        ],
        "correct": [4, 7, 1, 6, 2, 5, 3]
    },
    {
        "id": 2, "type": 2, "theme": "Drawing school",
        "format": "true_false",
        "instruction": "Определите, какие из утверждений соответствуют содержанию текста (1 — True), какие не соответствуют (2 — False) и о чём в тексте не сказано (3 — Not stated).",
        "statements": [
            "The park is full of children playing.",
            "Lily often reads books on psychology.",
            "The book contains some facts from the past.",
            "Miles finds the book useless.",
            "Miles rarely trusts strangers.",
            "Lily is going to finish reading the book soon.",
            "Miles has invited Lily to the cinema at the weekend."
        ],
        "correct": [2, 1, 3, 1, 2, 1, 3]
    },
    {
        "id": 3, "type": 2, "theme": "A book about living without money",
        "format": "true_false",
        "instruction": "Определите, какие из утверждений соответствуют содержанию текста (1 — True), какие не соответствуют (2 — False) и о чём в тексте не сказано (3 — Not stated).",
        "statements": [
            "Ben is surprised by the number of people who don't earn money.",
            "Ben spent a huge amount of money on food before.",
            "Ben doesn't have a mobile phone.",
            "Ben's friends have a positive attitude to his lifestyle.",
            "Ben spends his free time in libraries.",
            "Ben's parents taught him to make things himself.",
            "Ben's dream is to build his own house."
        ],
        "correct": [1, 3, 2, 1, 3, 2, 1]
    },
    {
        "id": 4, "type": 2, "theme": "Volunteering in Kenya",
        "format": "true_false",
        "instruction": "Определите, какие из утверждений соответствуют содержанию текста (1 — True), какие не соответствуют (2 — False) и о чём в тексте не сказано (3 — Not stated).",
        "statements": [
            "The author went to Kenya with her classmates.",
            "The plane was delayed by several hours.",
            "The author's host family met her at the airport.",
            "The author had her own room in the host family's house.",
            "The author learned some Swahili phrases.",
            "The author liked the local food.",
            "The author regrets going to Kenya."
        ],
        "correct": [2, 1, 3, 1, 1, 3, 2]
    },
    {
        "id": 5, "type": 2, "theme": "Jogging tour in London",
        "format": "true_false",
        "instruction": "Определите, какие из утверждений соответствуют содержанию текста (1 — True), какие не соответствуют (2 — False) и о чём в тексте не сказано (3 — Not stated).",
        "statements": [
            "The jogging tour starts early in the morning.",
            "The tour is only for professional runners.",
            "You can see famous London landmarks during the tour.",
            "The tour guide tells stories about London.",
            "All participants get a complimentary T-shirt.",
            "The tour ends at a café with refreshments.",
            "The tour is available all year round."
        ],
        "correct": [1, 2, 1, 1, 3, 2, 1]
    },
    {
        "id": 6, "type": 1, "theme": "Scotland",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7. Используйте каждую цифру только один раз.",
        "items": ["A", "B", "C", "D", "E", "F"],
        "headings": [
            "Scotland offers many options for travelling.",
            "The city of Edinburgh is a must-see destination.",
            "Scottish mountains attract extreme sports fans.",
            "Scottish cuisine is unique and diverse.",
            "The locals in Scotland are very friendly.",
            "Scottish music festivals are world-famous.",
            "Scotland has a rich historical heritage."
        ],
        "correct": [1, 5, 3, 7, 2, 4, 6]
    },
    {
        "id": 7, "type": "3-9", "theme": "Psychologist Lisa",
        "format": "multiple_choice",
        "instruction": "Прочитайте текст и выполните задания 3-9. В каждом задании запишите номер выбранного ответа.",
        "questions": [
            {"num": 3, "text": "What do we learn about Lisa Black at the beginning of the interview?", "options": ["All of her books are bestsellers.", "She has an undergraduate degree in psychology.", "She has two world-famous books."], "correct": 2},
            {"num": 4, "text": "Lisa compares weightlifting and studying to show that...", "options": ["to develop, one needs to work hard.", "sport is necessary for brain work.", "these processes are not very hard."], "correct": 0},
            {"num": 5, "text": "Lisa considers a stress-free life to be...", "options": ["the best choice.", "impossible.", "a must."], "correct": 1},
            {"num": 6, "text": "Lisa thinks stress is good if it is...", "options": ["manageable.", "chronic.", "short-term."], "correct": 2},
            {"num": 7, "text": "Lisa explains to her clients that anxiety in fact is...", "options": ["a way to make you work more.", "a protective mechanism.", "a thing one needs to get rid of."], "correct": 1},
            {"num": 8, "text": "According to Lisa, while discussing the worst-case scenarios with their children, parents should concentrate on the...", "options": ["things they say.", "way they sound.", "solution to the problem."], "correct": 2},
            {"num": 9, "text": "Lisa advises parents to... the fact that their children are sometimes stressed.", "options": ["accept", "dread", "reject"], "correct": 0}
        ]
    },
    {
        "id": 8, "type": "3-9", "theme": "Football player Carl",
        "format": "multiple_choice",
        "instruction": "Прочитайте текст и выполните задания 3-9. В каждом задании запишите номер выбранного ответа.",
        "questions": [
            {"num": 3, "text": "What do we learn about Carl at the beginning of the interview?", "options": ["He started playing football at age 10.", "His father was also a footballer.", "He comes from a wealthy family."], "correct": 1},
            {"num": 4, "text": "Carl says the most important quality for a footballer is...", "options": ["natural talent.", "hard work.", "good luck."], "correct": 1},
            {"num": 5, "text": "According to Carl, his coach helped him to...", "options": ["improve his technique.", "believe in himself.", "earn more money."], "correct": 1},
            {"num": 6, "text": "Carl thinks the best moment of his career was...", "options": ["his first professional match.", "scoring the winning goal.", "signing his first contract."], "correct": 1},
            {"num": 7, "text": "Carl believes that teamwork is...", "options": ["more important than individual skill.", "less important than training.", "the same as following orders."], "correct": 0},
            {"num": 8, "text": "What does Carl say about injuries?", "options": ["They are part of the game.", "They can be easily avoided.", "They end most careers."], "correct": 0},
            {"num": 9, "text": "Carl's advice to young footballers is to...", "options": ["focus only on football.", "enjoy the game and study.", "change clubs often."], "correct": 1}
        ]
    },
    {
        "id": 9, "type": "3-9", "theme": "Actress Kelly",
        "format": "multiple_choice",
        "instruction": "Прочитайте текст и выполните задания 3-9. В каждом задании запишите номер выбранного ответа.",
        "questions": [
            {"num": 3, "text": "What do we learn about Kelly's childhood?", "options": ["She grew up in a small town.", "She started acting at age 5.", "Her parents were actors."], "correct": 0},
            {"num": 4, "text": "Kelly got her first role...", "options": ["after graduating from drama school.", "by sending photos to a casting agency.", "through a family connection."], "correct": 1},
            {"num": 5, "text": "Kelly describes her most challenging role as...", "options": ["physically demanding.", "emotionally draining.", "technically complex."], "correct": 1},
            {"num": 6, "text": "What does Kelly say about fame?", "options": ["She enjoys being recognized.", "She tries to keep her private life private.", "She thinks fame is the best part of acting."], "correct": 1},
            {"num": 7, "text": "Kelly thinks the key to a good performance is...", "options": ["memorizing lines perfectly.", "understanding the character.", "having good co-stars."], "correct": 1},
            {"num": 8, "text": "Kelly is currently working on...", "options": ["a new film.", "a theatre play.", "a TV series."], "correct": 2},
            {"num": 9, "text": "Kelly advises young actors to...", "options": ["move to Hollywood.", "be persistent and patient.", "only accept leading roles."], "correct": 1}
        ]
    },
    {
        "id": 10, "type": "3-9", "theme": "Writer Kelly",
        "format": "multiple_choice",
        "instruction": "Прочитайте текст и выполните задания 3-9. В каждом задании запишите номер выбранного ответа.",
        "questions": [
            {"num": 3, "text": "What kind of books does the writer create?", "options": ["Detective stories.", "Science fiction novels.", "Children's books."], "correct": 2},
            {"num": 4, "text": "The writer gets inspiration for her stories from...", "options": ["her own childhood memories.", "other popular books.", "her children's questions."], "correct": 0},
            {"num": 5, "text": "How long does it take the writer to finish a book?", "options": ["A few weeks.", "Several months.", "Over a year."], "correct": 1},
            {"num": 6, "text": "The writer's favourite part of the process is...", "options": ["illustrating the book.", "creating the characters.", "editing the text."], "correct": 1},
            {"num": 7, "text": "The writer thinks the most difficult part is...", "options": ["finding a publisher.", "meeting deadlines.", "writing the first draft."], "correct": 2},
            {"num": 8, "text": "What does the writer say about feedback from readers?", "options": ["She reads every message.", "It helps her improve.", "She ignores criticism."], "correct": 1},
            {"num": 9, "text": "The writer's next book will be about...", "options": ["animals.", "space travel.", "friendship."], "correct": 2}
        ]
    },
    {
        "id": 11, "type": 1, "theme": "Presents",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7. Используйте каждую цифру только один раз.",
        "items": ["A", "B", "C", "D", "E", "F"],
        "headings": [
            "Choosing presents is not always easy.",
            "Homemade presents are the most valuable.",
            "The best presents are experiences, not things.",
            "Some people prefer practical gifts.",
            "Present wrapping is an art.",
            "Gift cards are a safe option.",
            "Surprise presents are the most memorable."
        ],
        "correct": [2, 6, 1, 4, 3, 5, 7]
    },
    {
        "id": 12, "type": 1, "theme": "Consumerism",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7. Используйте каждую цифру только один раз.",
        "items": ["A", "B", "C", "D", "E", "F"],
        "headings": [
            "Advertising influences our choices.",
            "Buying less can make us happier.",
            "The problem of overconsumption.",
            "Second-hand shopping is becoming popular.",
            "Brands don't always mean quality.",
            "How to resist impulse buying.",
            "Minimalism as a lifestyle."
        ],
        "correct": [3, 5, 1, 7, 2, 4, 6]
    },
    {
        "id": 13, "type": 1, "theme": "Fresh fruit",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7. Используйте каждую цифру только один раз.",
        "items": ["A", "B", "C", "D", "E", "F"],
        "headings": [
            "Fruit is essential for a healthy diet.",
            "Exotic fruit from around the world.",
            "How to choose ripe fruit.",
            "Seasonal fruit tastes the best.",
            "Growing your own fruit is rewarding.",
            "Fruit can be used in savoury dishes.",
            "Dried fruit makes a healthy snack."
        ],
        "correct": [4, 1, 6, 2, 5, 3, 7]
    },
    {
        "id": 14, "type": 2, "theme": "Art as a hobby",
        "format": "true_false",
        "instruction": "Определите, какие из утверждений соответствуют содержанию текста (1 — True), какие не соответствуют (2 — False) и о чём в тексте не сказано (3 — Not stated).",
        "statements": [
            "Jacob is very busy this summer.",
            "Jacob has had a summer job before.",
            "Rosie loves drawing.",
            "Jacob is a student of an art school.",
            "Rosie thinks doodling is quite easy.",
            "Rosie has never done doodling.",
            "Jacob lives next door to Rosie."
        ],
        "correct": [2, 1, 1, 2, 3, 2, 1]
    },
    {
        "id": 15, "type": 2, "theme": "Ordering a cake",
        "format": "true_false",
        "instruction": "Определите, какие из утверждений соответствуют содержанию текста (1 — True), какие не соответствуют (2 — False) и о чём в тексте не сказано (3 — Not stated).",
        "statements": [
            "The cake was ordered for a birthday party.",
            "The customer wanted a chocolate cake.",
            "The bakery delivered the cake on time.",
            "The cake had a personalised message on it.",
            "The customer was satisfied with the result.",
            "The bakery offered a discount for regular customers.",
            "The customer paid in cash."
        ],
        "correct": [1, 2, 1, 1, 1, 3, 2]
    },
    {
        "id": 16, "type": 2, "theme": "Mushrooms",
        "format": "true_false",
        "instruction": "Определите, какие из утверждений соответствуют содержанию текста (1 — True), какие не соответствуют (2 — False) и о чём в тексте не сказано (3 — Not stated).",
        "statements": [
            "Mushrooms grow only in forests.",
            "Some mushrooms are poisonous.",
            "Mushroom picking is a popular hobby in Russia.",
            "All mushrooms are edible after cooking.",
            "Mushrooms contain many vitamins.",
            "You should never eat raw mushrooms.",
            "Mushrooms can be used in medicine."
        ],
        "correct": [2, 1, 1, 2, 1, 1, 3]
    },
    {
        "id": 17, "type": "1", "theme": "Yoga",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7. Используйте каждую цифру только один раз.",
        "items": ["A", "B", "C", "D", "E", "F"],
        "headings": [
            "Yoga improves physical health.",
            "Yoga helps to reduce stress.",
            "Different types of yoga exist.",
            "You can practise yoga anywhere.",
            "Yoga is for all ages.",
            "Yoga requires special equipment.",
            "Yoga originated in ancient India."
        ],
        "correct": [2, 5, 7, 1, 4, 6, 3]
    }
]


def init_ege_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ege_tasks (
        id INTEGER PRIMARY KEY,
        task_type TEXT NOT NULL,
        theme TEXT NOT NULL,
        format TEXT NOT NULL,
        instruction TEXT,
        data TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def populate_ege():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM ege_tasks")
    if c.fetchone()[0] == 0:
        for task in EGE_TASKS:
            data = {k: v for k, v in task.items() if k not in ('id', 'type', 'theme', 'format', 'instruction')}
            c.execute(
                "INSERT INTO ege_tasks (id, task_type, theme, format, instruction, data) VALUES (?,?,?,?,?,?)",
                (task['id'], str(task['type']), task['theme'], task['format'],
                 task.get('instruction', ''), json.dumps(data, ensure_ascii=False))
            )
        conn.commit()
        print(f"Populated {len(EGE_TASKS)} EGE tasks")
    conn.close()

def get_all_ege_tasks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, task_type, theme, format, instruction, data FROM ege_tasks ORDER BY id")
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        task = {'id': r[0], 'type': r[1], 'theme': r[2], 'format': r[3], 'instruction': r[4]}
        task.update(json.loads(r[5]))
        result.append(task)
    return result

def get_ege_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, task_type, theme, format, instruction, data FROM ege_tasks WHERE id = ?", (task_id,))
    r = c.fetchone()
    conn.close()
    if r:
        task = {'id': r[0], 'type': r[1], 'theme': r[2], 'format': r[3], 'instruction': r[4]}
        task.update(json.loads(r[5]))
        return task
    return None

def check_ege_answer(task, answers):
    """Check user answers against correct answers.
    Returns (correct_count, total_count, results_list)"""
    fmt = task['format']
    
    if fmt == 'matching':
        correct = task.get('correct', [])
        results = []
        for i, ans in enumerate(answers):
            if i < len(correct):
                try:
                    results.append(int(ans) == correct[i])
                except ValueError:
                    results.append(False)
            else:
                results.append(False)
        return sum(results), len(correct), results
    
    elif fmt == 'true_false':
        correct = task.get('correct', [])
        results = []
        for i, ans in enumerate(answers):
            if i < len(correct):
                try:
                    results.append(int(ans) == correct[i])
                except ValueError:
                    results.append(False)
            else:
                results.append(False)
        return sum(results), len(correct), results
    
    elif fmt == 'multiple_choice':
        questions = task.get('questions', [])
        results = []
        for i, q in enumerate(questions):
            if i < len(answers):
                try:
                    results.append(int(answers[i]) == q['correct'])
                except (ValueError, IndexError):
                    results.append(False)
            else:
                results.append(False)
        return sum(results), len(questions), results
    
    return 0, 0, []

"""EGE tasks data module - extracted from Zadania_FIPI_EGE_2024.pdf"""
import json
import sqlite3

DB_PATH = "englify.db"

EGE_TASKS = [
    ####### TASK 1: NEW YEAR (matching with texts) #######
    {
        "id": 1, "type": 1, "theme": "New Year",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7.",
        "headings": [
            "Celebrating New Year has a long history.",
            "There are extravagant ways to celebrate New Year.",
            "Good food is the most important thing for New Year.",
            "New Year is the best time for new beginnings.",
            "Properly preparing before New Year is important.",
            "New Year is a great time to be with your relatives.",
            "You don't need a special time to start something."
        ],
        "texts": [
            "A. People have been celebrating the start of a new year for thousands of years. The first celebrations of New Year that we know about were in ancient Babylon about 4000 years ago.",
            "B. In many countries, people make special preparations for the New Year. They clean their houses from top to bottom, pay off debts, and buy new clothes to bring good luck.",
            "C. Some people celebrate New Year by going to extravagant parties, watching spectacular fireworks displays, or travelling to exotic destinations.",
            "D. Too much food is an essential part of New Year celebrations. In Spain, people eat 12 grapes at midnight. In Japan, they eat soba noodles for longevity.",
            "E. Many people see the New Year as a perfect opportunity to make positive changes. They set resolutions such as exercising more or learning a new skill.",
            "F. The New Year period is associated with family reunions. People travel to be with loved ones, share meals, exchange gifts, and reflect on the past year."
        ],
        "correct": [2, 5, 4, 3, 1, 6]
    },
    ####### TASK 2: DRAWING SCHOOL (true/false) #######
    {
        "id": 2, "type": 2, "theme": "Drawing school",
        "format": "true_false",
        "instruction": "True (1), False (2), Not stated (3).",
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
    ####### TASK 3: BOOK ABOUT LIVING WITHOUT MONEY (true/false) #######
    {
        "id": 3, "type": 2, "theme": "A book about living without money",
        "format": "true_false",
        "instruction": "True (1), False (2), Not stated (3).",
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
    ####### TASK 4: VOLUNTEERING IN KENYA (true/false) #######
    {
        "id": 4, "type": 2, "theme": "Volunteering in Kenya",
        "format": "true_false",
        "instruction": "True (1), False (2), Not stated (3).",
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
    ####### TASK 5: JOGGING TOUR IN LONDON (true/false) #######
    {
        "id": 5, "type": 2, "theme": "Jogging tour in London",
        "format": "true_false",
        "instruction": "True (1), False (2), Not stated (3).",
        "statements": [
            "The jogging tour starts early in the morning.",
            "The tour is only for professional runners.",
            "You can see famous London landmarks during the tour.",
            "The tour guide tells stories about London.",
            "All participants get a complimentary T-shirt.",
            "The tour ends at a cafe with refreshments.",
            "The tour is available all year round."
        ],
        "correct": [1, 2, 1, 1, 3, 2, 1]
    },
    ####### TASK 6: SCOTLAND (matching with texts) #######
    {
        "id": 6, "type": 1, "theme": "Scotland",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7.",
        "headings": [
            "Scotland is a land full of legends.",
            "There are no reasons to go to Scotland.",
            "Scotland attracts visitors with its culture.",
            "One can love Scotland for its beautiful nature.",
            "Kilts are the best souvenirs from Scotland.",
            "Scotland is a great place to learn history.",
            "Scotland offers its visitors delicious food."
        ],
        "texts": [
            "A. Scotland has stunning landscapes from the rugged Highlands with ancient mountains to the peaceful lochs and green valleys. The natural beauty of Scotland takes your breath away.",
            "B. Scottish culture is rich and unique. The sound of bagpipes, traditional ceilidh dances, and famous Scottish hospitality make every visitor feel welcome.",
            "C. Historical castles and monuments can be found all over Scotland. From Edinburgh Castle to Culloden, every stone tells a story of Scotland's dramatic past.",
            "D. Traditional Scottish food includes famous dishes like haggis, neeps and tatties. Seafood is also excellent, with fresh salmon being particularly popular.",
            "E. Scottish folklore is full of mysterious creatures. The story of the Loch Ness Monster continues to attract curious visitors from around the world.",
            "F. The traditional Scottish kilt made of tartan fabric is recognized worldwide. Each clan has its own unique tartan pattern and wearing a kilt is a symbol of pride."
        ],
        "correct": [5, 3, 6, 7, 1, 4]
    },
    ####### TASK 7: PSYCHOLOGIST LISA (multiple choice) #######
    {
        "id": 7, "type": "3-9", "theme": "Psychologist Lisa",
        "format": "multiple_choice",
        "instruction": "Выберите правильный ответ.",
        "questions": [
            {"num": 3, "text": "What do we learn about Lisa Black at the beginning of the interview?", "options": ["All of her books are bestsellers.", "She has an undergraduate degree in psychology.", "She has two world-famous books."], "correct": 2},
            {"num": 4, "text": "Lisa compares weightlifting and studying to show that...", "options": ["to develop, one needs to work hard.", "sport is necessary for brain work.", "these processes are not very hard."], "correct": 0},
            {"num": 5, "text": "Lisa considers a stress-free life to be...", "options": ["the best choice.", "impossible.", "a must."], "correct": 1},
            {"num": 6, "text": "Lisa thinks stress is good if it is...", "options": ["manageable.", "chronic.", "short-term."], "correct": 2},
            {"num": 7, "text": "Lisa explains to her clients that anxiety in fact is...", "options": ["a way to make you work more.", "a protective mechanism.", "a thing one needs to get rid of."], "correct": 1},
            {"num": 8, "text": "According to Lisa, while discussing worst-case scenarios with children, parents should concentrate on the...", "options": ["things they say.", "way they sound.", "solution to the problem."], "correct": 2},
            {"num": 9, "text": "Lisa advises parents to... the fact that their children are sometimes stressed.", "options": ["accept", "dread", "reject"], "correct": 0}
        ]
    },
    ####### TASK 8: FOOTBALL PLAYER CARL (multiple choice) #######
    {
        "id": 8, "type": "3-9", "theme": "Football player Carl",
        "format": "multiple_choice",
        "instruction": "Выберите правильный ответ.",
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
    ####### TASK 9: ACTRESS KELLY (multiple choice) #######
    {
        "id": 9, "type": "3-9", "theme": "Actress Kelly",
        "format": "multiple_choice",
        "instruction": "Выберите правильный ответ.",
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
    ####### TASK 10: WRITER KELLY (multiple choice) #######
    {
        "id": 10, "type": "3-9", "theme": "Writer Kelly",
        "format": "multiple_choice",
        "instruction": "Выберите правильный ответ.",
        "questions": [
            {"num": 3, "text": "What kind of books does the writer create?", "options": ["Detective stories.", "Science fiction novels.", "Children's books."], "correct": 2},
            {"num": 4, "text": "The writer gets inspiration from...", "options": ["her own childhood memories.", "other popular books.", "her children's questions."], "correct": 0},
            {"num": 5, "text": "How long does it take the writer to finish a book?", "options": ["A few weeks.", "Several months.", "Over a year."], "correct": 1},
            {"num": 6, "text": "The writer's favourite part of the process is...", "options": ["illustrating the book.", "creating the characters.", "editing the text."], "correct": 1},
            {"num": 7, "text": "The writer thinks the most difficult part is...", "options": ["finding a publisher.", "meeting deadlines.", "writing the first draft."], "correct": 2},
            {"num": 8, "text": "What does the writer say about feedback?", "options": ["She reads every message.", "It helps her improve.", "She ignores criticism."], "correct": 1},
            {"num": 9, "text": "The writer's next book will be about...", "options": ["animals.", "space travel.", "friendship."], "correct": 2}
        ]
    },
    ####### TASK 11: PRESENTS (matching with texts) #######
    {
        "id": 11, "type": 1, "theme": "Presents",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7.",
        "headings": [
            "Money is the worst present ever.",
            "It's very convenient to shop for gifts online.",
            "Homemade gifts demonstrate your care.",
            "It's not worth buying presents for special occasions.",
            "A good present doesn't have to be useful.",
            "A good present can be shared with friends.",
            "A chance to get new impressions is a great present."
        ],
        "texts": [
            "A. When you create a gift with your own hands, you put your time and love into it. A hand-knitted scarf or a batch of homemade cookies can mean much more than an expensive store-bought item.",
            "B. Some of the best gifts are those that let you do something together. Tickets to a concert or a weekend trip create memories that last much longer than any material object.",
            "C. The most exciting presents are often the ones you never expected. A surprise gift shows that someone really knows you and cares about your happiness.",
            "D. Many people think the cost of a gift shows how much you care. However, a thoughtfully chosen small item can be more meaningful than an expensive one.",
            "E. Before buying anything, take time to think about what the person would truly appreciate. Consider their hobbies and interests rather than picking the first thing you see.",
            "F. While a new gadget might seem like a great present, sometimes the best gift is an experience. A hot air balloon ride or a cooking workshop gives unforgettable memories."
        ],
        "correct": [3, 6, 7, 5, 1, 4]
    },
    ####### TASK 12: CONSUMERISM (matching with texts) #######
    {
        "id": 12, "type": 1, "theme": "Consumerism",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7.",
        "headings": [
            "Worthless things may still be needed by someone.",
            "A possible way out is to put your clutter out of sight.",
            "You don't have to devote much time to house cleaning.",
            "One should devote a certain place to certain things.",
            "Making a shopping list helps to have fewer things.",
            "You should sort out your clothes first.",
            "Your relatives and friends may solve your litter problem."
        ],
        "texts": [
            "A. Many people buy things they don't really need. Homes get filled with clothes we never wear and gadgets we never use. This overconsumption is bad for the environment.",
            "B. Before throwing things away, think if someone else might need them. Old books can go to libraries, clothes can be donated, and furniture can be given to friends.",
            "C. A simple way to control spending is to plan purchases. Before going shopping, make a list of what you actually need and stick to it.",
            "D. If your room is full of unused things, try organizing them. Put similar items together, use boxes and shelves, and keep only what you need on display.",
            "E. The first step to decluttering your wardrobe is to sort everything into piles: keep, donate, repair, and throw away.",
            "F. One of the easiest ways to reduce clutter is to give unwanted items to people you know. Your old books might be perfect for a friend."
        ],
        "correct": [3, 1, 5, 4, 6, 7]
    },
    ####### TASK 13: FRESH FRUIT (matching with texts) #######
    {
        "id": 13, "type": 1, "theme": "Fresh fruit",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7.",
        "headings": [
            "Fresh fruit can put you in a good mood.",
            "Eating fresh fruit is the best way to improve health.",
            "Eating fresh fruit keeps your energy levels high.",
            "Fresh fruit is too expensive for many people.",
            "Eating fresh fruit helps you study better.",
            "Fresh fruit may make your eating habits better.",
            "Fresh fruit can make you look good."
        ],
        "texts": [
            "A. Fruit is packed with vitamins, minerals and antioxidants that strengthen your immune system and reduce the risk of many diseases.",
            "B. The natural sugars in fruit provide a quick energy boost. Instead of chocolate, try an apple or a banana for sustained energy.",
            "C. People who eat fruit regularly tend to have clearer skin. The antioxidants help fight ageing and keep you looking youthful.",
            "D. If you replace unhealthy snacks with fruit, you will consume fewer calories. Fruit is low in calories but high in fibre.",
            "E. The natural sugars and vitamins in fruit give your brain a boost. Students who eat fruit before exams often perform better.",
            "F. There is evidence that eating fruit can improve your mental wellbeing. The nutrients help regulate mood and reduce anxiety."
        ],
        "correct": [2, 3, 7, 6, 5, 1]
    },
    ####### TASK 14: ART AS A HOBBY (true/false) #######
    {
        "id": 14, "type": 2, "theme": "Art as a hobby",
        "format": "true_false",
        "instruction": "True (1), False (2), Not stated (3).",
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
    ####### TASK 15: ORDERING A CAKE (true/false) #######
    {
        "id": 15, "type": 2, "theme": "Ordering a cake",
        "format": "true_false",
        "instruction": "True (1), False (2), Not stated (3).",
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
    ####### TASK 16: MUSHROOMS (true/false) #######
    {
        "id": 16, "type": 2, "theme": "Mushrooms",
        "format": "true_false",
        "instruction": "True (1), False (2), Not stated (3).",
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
    ####### TASK 17: YOGA (matching with texts) #######
    {
        "id": 17, "type": 1, "theme": "Yoga",
        "format": "matching",
        "instruction": "Установите соответствие между текстами A-F и заголовками 1-7.",
        "headings": [
            "Yoga should be done with a certain purpose.",
            "One should create a special atmosphere for doing yoga.",
            "One needs high quality equipment for doing yoga.",
            "There is a big variety of yoga styles available.",
            "When you do yoga, you shouldn't have any ambitions.",
            "Online yoga lessons have many advantages.",
            "Yoga is the best way to lose a lot of weight."
        ],
        "texts": [
            "A. There are many approaches to yoga, from gentle Hatha to dynamic Vinyasa and Ashtanga. Each style has its own focus on flexibility, strength or meditation.",
            "B. You don't need to touch your toes or stand on your head to start yoga. The key is to practise without comparing yourself to others.",
            "C. Many people find online yoga very convenient. You can choose from thousands of videos and practise at any time without expensive studio memberships.",
            "D. To make home yoga enjoyable, create a calm environment. Light a candle, use soft lighting, play relaxing music and avoid being disturbed.",
            "E. Before practising, take a moment to set an intention. It could be to feel more energetic, to relax, or simply to be present in the moment.",
            "F. You don't need expensive equipment for yoga. All you need is a comfortable mat and clothes that allow you to move freely."
        ],
        "correct": [4, 5, 6, 2, 1, 3]
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
    count = c.fetchone()[0]
    if count != len(EGE_TASKS):
        if count > 0:
            c.execute("DELETE FROM ege_tasks")
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
    fmt = task['format']
    if fmt == 'matching':
        correct = task.get('correct', [])
        results = [int(a) == correct[i] if i < len(correct) else False for i, a in enumerate(answers)]
        return sum(results), len(correct), results
    elif fmt == 'true_false':
        correct = task.get('correct', [])
        results = [int(a) == correct[i] if i < len(correct) else False for i, a in enumerate(answers)]
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

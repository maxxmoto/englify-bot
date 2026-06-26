# web/grammar.py

GRAMMAR_LEVELS = {
    "beginner": {
        "title": "Beginner (Основы грамматики и лёгкая лексика)",
        "topics": [
            {
                "id": 1,
                "title": "Глагол to be (am / is / are)",
                "theory": "I – am, he / she / it – is, we / you / they – are. Отрицание: am not / is not (isn’t) / are not (aren’t). Вопрос: Am I…? Is he…? Are they…?",
                "tasks": [
                    {"question": "I ___ a teacher.", "answer": "am"},
                    {"question": "She ___ from London.", "answer": "is"},
                    {"question": "They ___ happy.", "answer": "are"},
                    {"question": "We ___ not tired.", "answer": "are"},
                    {"question": "___ you a student?", "answer": "Are"},
                    {"question": "My brother ___ 20 years old.", "answer": "is"},
                    {"question": "The cat ___ black.", "answer": "is"},
                    {"question": "I ___ not hungry.", "answer": "am"},
                    {"question": "___ he your friend?", "answer": "Is"},
                    {"question": "The books ___ on the table.", "answer": "are"}
                ]
            },
            {
                "id": 2,
                "title": "Местоимения и притяжательные прилагательные",
                "theory": "Личные (I, you, he, she, it, we, they) → притяжательные (my, your, his, her, its, our, their). Указательные: this (этот), that (тот), these (эти), those (те).",
                "tasks": [
                    {"question": "This is ___ book. (I)", "answer": "my"},
                    {"question": "___ name is Anna. (She)", "answer": "Her"},
                    {"question": "___ are my friends. (this → мн.ч.)", "answer": "These"},
                    {"question": "Look at ___ dog over there.", "answer": "that"},
                    {"question": "___ house is very big. (They)", "answer": "Their"},
                    {"question": "Is this ___ pen? (you)", "answer": "your"},
                    {"question": "___ am from Russia.", "answer": "I"},
                    {"question": "We love ___ cat. (we)", "answer": "our"},
                    {"question": "___ apples are red. (These / That)", "answer": "These"},
                    {"question": "He is my brother. ___ name is Tom.", "answer": "His"}
                ]
            },
            {
                "id": 3,
                "title": "Множественное число существительных",
                "theory": "Обычно +s (cat → cats). После -s, -sh, -ch, -x, -o → +es (bus → buses, tomato → tomatoes). Согласная + y → -ies (city → cities). Исключения: man → men, woman → women, child → children, tooth → teeth, foot → feet.",
                "tasks": [
                    {"question": "one apple → two ___", "answer": "apples"},
                    {"question": "one box → three ___", "answer": "boxes"},
                    {"question": "one baby → four ___", "answer": "babies"},
                    {"question": "one child → two ___", "answer": "children"},
                    {"question": "one knife → five ___", "answer": "knives"},
                    {"question": "one mouse → three ___", "answer": "mice"},
                    {"question": "one woman → two ___", "answer": "women"},
                    {"question": "one tomato → six ___", "answer": "tomatoes"},
                    {"question": "one leaf → many ___", "answer": "leaves"},
                    {"question": "one tooth → two ___", "answer": "teeth"}
                ]
            },
            {
                "id": 4,
                "title": "Артикли a / an и the",
                "theory": "a + согласный звук (a book), an + гласный звук (an apple). Неопределённый артикль – предмет впервые. The – когда предмет известен, уникален или уже упоминался.",
                "tasks": [
                    {"question": "I have ___ dog.", "answer": "a"},
                    {"question": "She is ___ honest person.", "answer": "an"},
                    {"question": "___ sun is shining.", "answer": "The"},
                    {"question": "Give me ___ orange, please.", "answer": "an"},
                    {"question": "He is ___ best student.", "answer": "the"},
                    {"question": "I saw ___ elephant at the zoo.", "answer": "an"},
                    {"question": "___ moon is beautiful tonight.", "answer": "The"},
                    {"question": "Can I have ___ glass of water?", "answer": "a"},
                    {"question": "This is ___ interesting idea.", "answer": "an"},
                    {"question": "___ children are playing outside.", "answer": "The"}
                ]
            },
            {
                "id": 5,
                "title": "Have got / has got",
                "theory": "I / you / we / they have got, he / she / it has got. Вопрос: Have you got…? Has she got…? Отрицание: haven’t got, hasn’t got.",
                "tasks": [
                    {"question": "I ___ got a new bike.", "answer": "have"},
                    {"question": "She ___ got blue eyes.", "answer": "has"},
                    {"question": "___ they got a car?", "answer": "Have"},
                    {"question": "We ___ got any money.", "answer": "haven’t"},
                    {"question": "He ___ got a sister.", "answer": "has"},
                    {"question": "___ your house got a garden?", "answer": "Has"},
                    {"question": "My parents ___ got a big flat.", "answer": "have"},
                    {"question": "I ___ got a headache.", "answer": "have"},
                    {"question": "She ___ got any pets.", "answer": "hasn’t"},
                    {"question": "___ you got a pen?", "answer": "Have"}
                ]
            },
            {
                "id": 6,
                "title": "Present Simple (настоящее простое)",
                "theory": "Утверждение: I / you / we / they work; he / she / it works. Отрицание: don’t / doesn’t + V1. Вопрос: Do / Does + подлежащее + V1? Употребляется для регулярных действий и фактов.",
                "tasks": [
                    {"question": "He ___ (play) football every Sunday.", "answer": "plays"},
                    {"question": "They ___ (not / like) coffee.", "answer": "don’t like"},
                    {"question": "___ she ___ (speak) English?", "answer": "Does / speak"},
                    {"question": "My sister ___ (study) at university.", "answer": "studies"},
                    {"question": "We ___ (go) to school by bus.", "answer": "go"},
                    {"question": "He ___ (not / watch) TV in the morning.", "answer": "doesn’t watch"},
                    {"question": "___ you ___ (live) in Moscow?", "answer": "Do / live"},
                    {"question": "The train ___ (arrive) at 7 o’clock.", "answer": "arrives"},
                    {"question": "I ___ (have) breakfast at 8 a.m.", "answer": "have"},
                    {"question": "___ it ___ (rain) a lot here?", "answer": "Does / rain"}
                ]
            },
            {
                "id": 7,
                "title": "There is / There are",
                "theory": "There is + ед.ч. / неисчисл. (There is a chair). There are + мн.ч. (There are three chairs). Вопрос: Is there…? Are there…?",
                "tasks": [
                    {"question": "___ a table in the room.", "answer": "There is"},
                    {"question": "___ two windows.", "answer": "There are"},
                    {"question": "___ any milk in the fridge?", "answer": "Is there"},
                    {"question": "___ many people in the park.", "answer": "There are"},
                    {"question": "___ a cat on the sofa.", "answer": "There isn’t"},
                    {"question": "___ any books on the shelf?", "answer": "Are there"},
                    {"question": "___ an apple and two bananas.", "answer": "There is"},
                    {"question": "___ some sugar in the bowl.", "answer": "There is"},
                    {"question": "___ three children in the pool.", "answer": "There are"},
                    {"question": "___ any cheese?", "answer": "Is there"}
                ]
            },
            {
                "id": 8,
                "title": "Простые предлоги места и времени",
                "theory": "Место: in (внутри), on (на поверхности), under (под), next to (рядом), between (между), behind (позади), in front of (перед). Время: at (время: at 5, at night), on (дни: on Monday), in (месяцы/годы: in June, in 2025).",
                "tasks": [
                    {"question": "The cat is ___ the table.", "answer": "under"},
                    {"question": "The book is ___ the bag.", "answer": "in"},
                    {"question": "The picture is ___ the wall.", "answer": "on"},
                    {"question": "She sits ___ me. (рядом)", "answer": "next to"},
                    {"question": "I get up ___ 7 o’clock.", "answer": "at"},
                    {"question": "We go to the park ___ Sunday.", "answer": "on"},
                    {"question": "Her birthday is ___ May.", "answer": "in"},
                    {"question": "The bank is ___ the post office and the café.", "answer": "between"},
                    {"question": "Don’t stand ___ front of the TV.", "answer": "in"},
                    {"question": "He is ___ home now.", "answer": "at"}
                ]
            }
        ]
    },
    "intermediate": {
        "title": "Intermediate (Средний уровень)",
        "topics": [
            {
                "id": 9,
                "title": "Present Continuous vs Present Simple",
                "theory": "Present Continuous (am / is / are + Ving) — действие прямо сейчас, временное, запланированное будущее. Present Simple — регулярное, факты. Маркеры Continuous: now, at the moment, Look!, Listen!",
                "tasks": [
                    {"question": "Listen! She ___ (sing).", "answer": "is singing"},
                    {"question": "I usually ___ (drink) tea, but today I ___ (have) coffee.", "answer": "drink / am having"},
                    {"question": "We ___ (go) to Italy every summer.", "answer": "go"},
                    {"question": "___ you ___ (watch) TV right now?", "answer": "Are / watching"},
                    {"question": "He ___ (not / work) on Sundays.", "answer": "doesn’t work"},
                    {"question": "My brother ___ (play) football at the moment.", "answer": "is playing"},
                    {"question": "Water ___ (boil) at 100°C.", "answer": "boils"},
                    {"question": "They ___ (stay) at a hotel this week.", "answer": "are staying"},
                    {"question": "She ___ (study) French twice a week.", "answer": "studies"},
                    {"question": "I ___ (look) for my keys now.", "answer": "am looking"}
                ]
            },
            {
                "id": 10,
                "title": "Past Simple (прошедшее простое)",
                "theory": "Правильные глаголы +ed (work → worked). Неправильные — по таблице (go → went, have → had). Отрицание: didn’t + V1. Вопрос: Did + подлежащее + V1? Указатели: yesterday, last week, ago.",
                "tasks": [
                    {"question": "I ___ (visit) my grandma yesterday.", "answer": "visited"},
                    {"question": "She ___ (go) to the cinema last night.", "answer": "went"},
                    {"question": "We ___ (not / see) that film.", "answer": "didn’t see"},
                    {"question": "___ he ___ (buy) a new car?", "answer": "Did / buy"},
                    {"question": "They ___ (eat) pizza for dinner.", "answer": "ate"},
                    {"question": "My parents ___ (get) married 20 years ago.", "answer": "got"},
                    {"question": "He ___ (stop) working at 6 p.m.", "answer": "stopped"},
                    {"question": "I ___ (read) three books last month.", "answer": "read (произносится [red])"},
                    {"question": "She ___ (not / call) me.", "answer": "didn’t call"},
                    {"question": "___ you ___ (sleep) well?", "answer": "Did / sleep"}
                ]
            },
            {
                "id": 11,
                "title": "Future Simple и to be going to",
                "theory": "Future Simple (will + V1) — спонтанные решения, обещания, предсказания. To be going to — планы, намерения, прогноз на основе очевидного.",
                "tasks": [
                    {"question": "I think it ___ (rain) tomorrow.", "answer": "will rain"},
                    {"question": "Look at the clouds! It ___ (rain).", "answer": "is going to rain"},
                    {"question": "She ___ (travel) to Paris next month. (план)", "answer": "is going to travel"},
                    {"question": "I ___ (help) you with the bags. (предложение)", "answer": "will help"},
                    {"question": "They ___ (not / come) to the party.", "answer": "won’t come"},
                    {"question": "___ you ___ (be) at home this evening?", "answer": "Will / be"},
                    {"question": "We ___ (visit) our grandparents this weekend. (план)", "answer": "are going to visit"},
                    {"question": "He ___ (probably / call) later.", "answer": "will probably call"},
                    {"question": "I promise I ___ (be) careful.", "answer": "will be"},
                    {"question": "What ___ you ___ (do) after the lesson?", "answer": "are / going to do"}
                ]
            },
            {
                "id": 12,
                "title": "Present Perfect (настоящее совершённое)",
                "theory": "Have / has + V3. Связь прошлого с настоящим: результат сейчас, жизненный опыт, неистёкший период. Маркеры: ever, never, just, already, yet, since, for.",
                "tasks": [
                    {"question": "I ___ (finish) my homework.", "answer": "have finished"},
                    {"question": "She ___ (never / be) to China.", "answer": "has never been"},
                    {"question": "They ___ (not / arrive) yet.", "answer": "haven’t arrived"},
                    {"question": "___ you ___ (ever / eat) sushi?", "answer": "Have / ever eaten"},
                    {"question": "He ___ (live) here since 2010.", "answer": "has lived"},
                    {"question": "We ___ (already / see) this movie.", "answer": "have already seen"},
                    {"question": "She ___ (just / leave).", "answer": "has just left"},
                    {"question": "I ___ (know) him for five years.", "answer": "have known"},
                    {"question": "My parents ___ (buy) a new house.", "answer": "have bought"},
                    {"question": "___ he ___ (do) his homework yet?", "answer": "Has / done"}
                ]
            },
            {
                "id": 13,
                "title": "Модальные глаголы (can, must, should, have to, may)",
                "theory": "can — возможность / умение; must — должен (сильное требование); have to — вынужден (внешняя необходимость); should — совет; may — разрешение / вероятность.",
                "tasks": [
                    {"question": "You ___ (should / must) see a doctor. You look very sick.", "answer": "must"},
                    {"question": "Drivers ___ stop at red lights.", "answer": "must"},
                    {"question": "I ___ swim very well.", "answer": "can"},
                    {"question": "You ___ eat more vegetables. (совет)", "answer": "should"},
                    {"question": "___ I open the window?", "answer": "May / Can"},
                    {"question": "He ___ get up early because the bus leaves at 6.", "answer": "has to"},
                    {"question": "You ___ (can’t / shouldn’t) park here. It’s forbidden.", "answer": "can’t"},
                    {"question": "She ___ sing beautifully when she was a child.", "answer": "could"},
                    {"question": "We ___ wear a uniform at our school.", "answer": "have to"},
                    {"question": "You ___ worry. Everything will be fine.", "answer": "shouldn’t"}
                ]
            },
            {
                "id": 14,
                "title": "Степени сравнения прилагательных",
                "theory": "Односложные: -er / -est (big → bigger → the biggest). Двусложные на -y: -ier / -iest (happy → happier). Многосложные: more / the most (interesting → more interesting → the most interesting). Исключения: good → better → best; bad → worse → worst.",
                "tasks": [
                    {"question": "My sister is ___ (tall) than me.", "answer": "taller"},
                    {"question": "This is ___ (good) restaurant in town.", "answer": "the best"},
                    {"question": "Today is ___ (hot) than yesterday.", "answer": "hotter"},
                    {"question": "She is ___ (intelligent) person I know.", "answer": "the most intelligent"},
                    {"question": "This exam was ___ (difficult) than the last one.", "answer": "more difficult"},
                    {"question": "He runs ___ (fast) than his brother.", "answer": "faster"},
                    {"question": "That was the ___ (bad) day of my life.", "answer": "worst"},
                    {"question": "This book is ___ (interesting) than the film.", "answer": "more interesting"},
                    {"question": "February is the ___ (short) month.", "answer": "shortest"},
                    {"question": "She is the ___ (friendly) girl in class.", "answer": "friendliest"}
                ]
            },
            {
                "id": 15,
                "title": "Условные предложения 0 и 1 типа",
                "theory": "Type 0 (реальность, всегда правда): If + Present Simple, Present Simple. Type 1 (реальное будущее): If + Present Simple, will + V1.",
                "tasks": [
                    {"question": "If you heat ice, it ___ (melt).", "answer": "melts"},
                    {"question": "If it ___ (rain), I will take an umbrella.", "answer": "rains"},
                    {"question": "She will miss the bus if she ___ (not / hurry).", "answer": "doesn’t hurry"},
                    {"question": "If I ___ (be) late, my boss will be angry.", "answer": "am"},
                    {"question": "If you mix red and blue, you ___ (get) purple.", "answer": "get"},
                    {"question": "We ___ (go) to the beach if the weather is nice.", "answer": "will go"},
                    {"question": "If he ___ (not / come), we won’t start.", "answer": "doesn’t come"},
                    {"question": "Babies cry if they ___ (be) hungry.", "answer": "are"},
                    {"question": "If you study hard, you ___ (pass) the exam.", "answer": "will pass"},
                    {"question": "I’ll call you if I ___ (have) time.", "answer": "have"}
                ]
            },
            {
                "id": 16,
                "title": "Фразовые глаголы (введение)",
                "theory": "Фразовые глаголы меняют смысл с предлогом: look after (заботиться), give up (бросать), turn on / off (вкл/выкл), look forward to (ждать с нетерпением).",
                "tasks": [
                    {"question": "Can you ___ (look after / look for) my cat while I’m away?", "answer": "look after"},
                    {"question": "He ___ (gave up / gave away) smoking last year.", "answer": "gave up"},
                    {"question": "Please ___ (turn on / turn off) the light before you leave.", "answer": "turn off"},
                    {"question": "I’m really ___ (looking forward to / looking for) the holidays.", "answer": "looking forward to"},
                    {"question": "She ___ (put on / take off) her coat and went out.", "answer": "put on"},
                    {"question": "I’m ___ (looking for / looking after) my keys. Have you seen them?", "answer": "looking for"},
                    {"question": "We need to ___ (find out / give up) the truth.", "answer": "find out"},
                    {"question": "Can you ___ (pick up / turn down) that pen for me?", "answer": "pick up"},
                    {"question": "He ___ (turned down / looked after) the job offer.", "answer": "turned down"},
                    {"question": "I’ll ___ (come back / go on) in five minutes.", "answer": "come back"}
                ]
            }
        ]
    },
    "advanced": {
        "title": "Advanced (Продвинутые конструкции, идиомы)",
        "topics": [
            {
                "id": 17,
                "title": "Сложные времена: Past Perfect и Future Perfect",
                "theory": "Past Perfect (had + V3) — действие, завершённое до другого момента в прошлом. Future Perfect (will have + V3) — действие завершится к моменту в будущем.",
                "tasks": [
                    {"question": "When we arrived, the film ___ (already / start).", "answer": "had already started"},
                    {"question": "By next June, she ___ (finish) the course.", "answer": "will have finished"},
                    {"question": "He ___ (never / see) snow before he moved to Norway.", "answer": "had never seen"},
                    {"question": "I’m sure they ___ (arrive) by 5 p.m.", "answer": "will have arrived"},
                    {"question": "After she ___ (eat) dinner, she went for a walk.", "answer": "had eaten"},
                    {"question": "By the time you read this, I ___ (leave).", "answer": "will have left"},
                    {"question": "We ___ (live) there for ten years before we decided to move.", "answer": "had lived"},
                    {"question": "Don’t call at 8; I ___ (not / finish) work yet.", "answer": "won’t have finished"}
                ]
            },
            {
                "id": 18,
                "title": "Условные предложения 2 и 3 типа, смешанный тип",
                "theory": "Type 2 (нереальное в настоящем): If + Past Simple, would + V1. Type 3 (нереальное в прошлом): If + Past Perfect, would have + V3. Mixed: If + Past Perfect, would + V1 (прошлое условие → настоящий результат).",
                "tasks": [
                    {"question": "If I ___ (be) you, I would accept the offer.", "answer": "were"},
                    {"question": "If she had studied, she ___ (pass) the exam.", "answer": "would have passed"},
                    {"question": "I ___ (buy) that car if I had enough money.", "answer": "would buy"},
                    {"question": "If we hadn’t missed the train, we ___ (be) on time.", "answer": "would have been"},
                    {"question": "If I were taller, I ___ (play) basketball professionally.", "answer": "would play"},
                    {"question": "He ___ (not / lose) his job if he had been more careful.", "answer": "wouldn’t have lost"},
                    {"question": "If I had known you were ill, I ___ (visit) you.", "answer": "would have visited"},
                    {"question": "If it weren’t raining, we ___ (go) for a walk.", "answer": "would go"},
                    {"question": "If you had invited me, I ___ (come).", "answer": "would have come"},
                    {"question": "She would be rich now if she ___ (buy) those shares then.", "answer": "had bought"}
                ]
            },
            {
                "id": 19,
                "title": "Пассивный залог (все времена)",
                "theory": "be + V3. Present Passive: am/is/are + V3; Past Passive: was/were + V3; Perfect Passive: have/has been + V3. Исполнитель через by.",
                "tasks": [
                    {"question": "English ___ (speak) all over the world.", "answer": "is spoken"},
                    {"question": "The cake ___ (make) by my mother yesterday.", "answer": "was made"},
                    {"question": "The results ___ (announce) next Monday.", "answer": "will be announced"},
                    {"question": "This road ___ (repair) at the moment.", "answer": "is being repaired"},
                    {"question": "He ___ (just / promote).", "answer": "has just been promoted"},
                    {"question": "The letters ___ (send) by 5 p.m. yesterday.", "answer": "had been sent"},
                    {"question": "This book ___ (write) by George Orwell.", "answer": "was written"},
                    {"question": "Our flight ___ (delay) because of fog.", "answer": "was delayed"},
                    {"question": "The problem ___ (discuss) now.", "answer": "is being discussed"},
                    {"question": "A new hospital ___ (build) in my town.", "answer": "has been built"}
                ]
            },
            {
                "id": 20,
                "title": "Косвенная речь (Reported Speech)",
                "theory": "Сдвиг времён назад. Present → Past, Past → Past Perfect. Изменение местоимений и наречий (now → then, today → that day). Вопросы без вспомогательного do/does: “What do you want?” → He asked what I wanted.",
                "tasks": [
                    {"question": "“I am tired,” she said. → She said that she ___ tired.", "answer": "was"},
                    {"question": "“We will call you,” they told me. → They told me they ___ me.", "answer": "would call"},
                    {"question": "“I have finished my work,” he said. → He said he ___ his work.", "answer": "had finished"},
                    {"question": "“Where do you live?” she asked me. → She asked me where ___.", "answer": "I lived"},
                    {"question": "“Don’t touch that!” he told us. → He told us ___ touch that.", "answer": "not to"},
                    {"question": "“I can swim,” she said. → She said she ___ swim.", "answer": "could"},
                    {"question": "“I saw the film last week,” he said. → He said he ___ the film the week before.", "answer": "had seen"},
                    {"question": "“Are you coming?” she asked. → She asked if I ___ coming.", "answer": "was"}
                ]
            },
            {
                "id": 21,
                "title": "Инверсия (Inversion)",
                "theory": "После отрицательных наречий в начале предложения — обратный порядок слов. Never have I seen, Rarely does he complain, Not only did they win, No sooner had he left than…, Only then did I realise.",
                "tasks": [
                    {"question": "Never ___ (I / see) such a beautiful sunset.", "answer": "have I seen"},
                    {"question": "Hardly ___ (we / arrive) when it started to rain.", "answer": "had we arrived"},
                    {"question": "Not only ___ (she / finish) the report, but she also presented it.", "answer": "did she finish"},
                    {"question": "Under no circumstances ___ (you / open) this door.", "answer": "should you open"},
                    {"question": "Little ___ (he / know) about the problem.", "answer": "does he know"},
                    {"question": "Only after the meeting ___ (I / understand) the situation.", "answer": "did I understand"},
                    {"question": "Rarely ___ (she / speak) in public.", "answer": "does she speak"},
                    {"question": "So beautiful ___ (the music / be) that everyone stopped talking.", "answer": "was the music"}
                ]
            },
            {
                "id": 22,
                "title": "Сложные конструкции с инфинитивом и герундием",
                "theory": "Complex Object: I want you to come. Complex Subject: He is said to be rich. Герундий после предлогов и некоторых глаголов (enjoy, avoid, suggest). Инфинитив для цели (to do). Изменение смысла: stop to do / stop doing.",
                "tasks": [
                    {"question": "I heard her ___ (sing) a song.", "answer": "sing"},
                    {"question": "He is said ___ (be) a millionaire.", "answer": "to be"},
                    {"question": "She suggested ___ (go) to the park.", "answer": "going"},
                    {"question": "I want you ___ (help) me.", "answer": "to help"},
                    {"question": "They made him ___ (apologize).", "answer": "apologize"},
                    {"question": "I avoided ___ (talk) about it.", "answer": "talking"},
                    {"question": "He stopped ___ (smoke) a year ago.", "answer": "smoking"},
                    {"question": "She stopped ___ (buy) some water on the way home.", "answer": "to buy"},
                    {"question": "It’s worth ___ (visit) that museum.", "answer": "visiting"},
                    {"question": "I saw him ___ (cross) the street.", "answer": "cross"}
                ]
            },
            {
                "id": 23,
                "title": "Cleft sentences (Расщеплённые предложения)",
                "theory": "It is/was … that/who … для выделения смысла. What … is/was … . Вопросы с it: It was John who broke the vase. What I need is a good rest.",
                "tasks": [
                    {"question": "John broke the vase. (Выдели John) → It ___ John who broke the vase.", "answer": "was"},
                    {"question": "I need a good rest. → What I need ___ a good rest.", "answer": "is"},
                    {"question": "She doesn’t like the noise. → It ___ the noise that she doesn’t like.", "answer": "is"},
                    {"question": "We met at that café. → It was at that café that we ___.", "answer": "met"},
                    {"question": "He bought a car, not a bike. → What he bought ___ a car.", "answer": "was"}
                ]
            },
            {
                "id": 24,
                "title": "Идиомы и продвинутая лексика",
                "theory": "Идиомы – устойчивые выражения, смысл которых не вытекает из отдельных слов (break the ice, piece of cake, hit the nail on the head). Продвинутая лексика: выбрать точное слово по контексту.",
                "tasks": [
                    {"question": "To start a conversation and make people feel more comfortable: ___ (break the ice / hit the sack)", "answer": "break the ice"},
                    {"question": "The exam was very easy. It was a ___ (tough cookie / piece of cake).", "answer": "piece of cake"},
                    {"question": "She’s very practical and sensible. She’s ___ (down-to-earth / over the moon).", "answer": "down-to-earth"},
                    {"question": "I’m feeling ___ (under the weather / on cloud nine) today; I might be getting sick.", "answer": "under the weather"},
                    {"question": "Don’t worry, the problem is just ___ (a storm in a teacup / a red herring).", "answer": "a storm in a teacup"},
                    {"question": "His comment really ___ (hit the nail on the head / cost an arm and a leg).", "answer": "hit the nail on the head"},
                    {"question": "That car costs ___ (an arm and a leg / a penny).", "answer": "an arm and a leg"},
                    {"question": "Please, ___ (cut to the chase / bite the bullet) and tell me what happened.", "answer": "cut to the chase"},
                    {"question": "He’s very generous, he has ___ (a heart of gold / a chip on his shoulder).", "answer": "a heart of gold"},
                    {"question": "We decided to ___ (call it a day / kick the bucket) after working for 12 hours.", "answer": "call it a day"},
                    {"question": "She was ___ (over the moon / in hot water) when she got the promotion.", "answer": "over the moon"}
                ]
            }
        ]
    }
}
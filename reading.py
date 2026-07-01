"""Reading section - easy English articles with vocabulary"""
import json

ARTICLES = [
    {
        "id": 1,
        "title": "My Morning Routine",
        "level": "A2",
        "text": "Every morning I wake up at seven o'clock. First, I brush my teeth and wash my face. Then I have breakfast. I usually eat cereal with milk and drink a glass of orange juice. After breakfast, I get dressed and go to school. I live near my school, so I walk there. It takes me fifteen minutes. I like to listen to music on the way. When I arrive at school, I meet my friends and we go to class together.",
        "words": [
            {"word": "routine", "translation": "режим, распорядок"},
            {"word": "wake up", "translation": "просыпаться"},
            {"word": "brush", "translation": "чистить (щёткой)"},
            {"word": "breakfast", "translation": "завтрак"},
            {"word": "cereal", "translation": "хлопья"},
            {"word": "glass", "translation": "стакан"},
            {"word": "get dressed", "translation": "одеваться"},
            {"word": "arrive", "translation": "прибывать"},
            {"word": "meet", "translation": "встречать(ся)"},
            {"word": "together", "translation": "вместе"}
        ]
    },
    {
        "id": 2,
        "title": "A Day at the Park",
        "level": "A2",
        "text": "Last Sunday, my family and I went to the park. The weather was beautiful and sunny. My mother packed a picnic basket with sandwiches, fruit, and lemonade. My father played football with my brother. I read a book under a big tree. My little sister fed the ducks in the pond. We stayed at the park for four hours. In the evening, we went home tired but happy. I love spending time with my family outdoors.",
        "words": [
            {"word": "weather", "translation": "погода"},
            {"word": "sunny", "translation": "солнечный"},
            {"word": "pack", "translation": "упаковывать, собирать"},
            {"word": "picnic", "translation": "пикник"},
            {"word": "basket", "translation": "корзина"},
            {"word": "sandwich", "translation": "бутерброд"},
            {"word": "pond", "translation": "пруд"},
            {"word": "feed", "translation": "кормить"},
            {"word": "tired", "translation": "уставший"},
            {"word": "outdoors", "translation": "на улице, на природе"}
        ]
    },
    {
        "id": 3,
        "title": "My Favourite Hobby",
        "level": "A2",
        "text": "My favourite hobby is photography. I started taking pictures two years ago when my grandfather gave me his old camera. At first, I only took photos of my cat and my garden. Then I joined a photography club at school. Now I take photos of everything: interesting buildings, beautiful sunsets, and people in the street. I learned how to use light and shadows. Last month, I won a prize in a school photography competition. My dream is to become a professional photographer one day.",
        "words": [
            {"word": "photography", "translation": "фотография"},
            {"word": "camera", "translation": "камера, фотоаппарат"},
            {"word": "join", "translation": "присоединяться"},
            {"word": "club", "translation": "клуб, кружок"},
            {"word": "sunset", "translation": "закат"},
            {"word": "shadow", "translation": "тень"},
            {"word": "prize", "translation": "приз, награда"},
            {"word": "competition", "translation": "соревнование, конкурс"},
            {"word": "professional", "translation": "профессиональный"},
            {"word": "become", "translation": "становиться"}
        ]
    },
    {
        "id": 4,
        "title": "How Pizza Became Popular",
        "level": "B1",
        "text": "Pizza is one of the most popular foods in the world today, but it originally came from Italy. In the 18th century, people in Naples began adding tomatoes to flat bread. This was the beginning of modern pizza. In 1889, a chef named Raffaele Esposito created a special pizza for the Italian king. He used tomatoes, mozzarella cheese, and basil to represent the colours of the Italian flag. Italian immigrants brought pizza to America in the early 20th century. After World War Two, American soldiers returned home and wanted to eat the pizza they had tried in Italy. This made pizza popular all over the world.",
        "words": [
            {"word": "popular", "translation": "популярный"},
            {"word": "originally", "translation": "изначально"},
            {"word": "century", "translation": "век"},
            {"word": "flat bread", "translation": "лепёшка"},
            {"word": "chef", "translation": "шеф-повар"},
            {"word": "create", "translation": "создавать"},
            {"word": "represent", "translation": "представлять, символизировать"},
            {"word": "flag", "translation": "флаг"},
            {"word": "immigrant", "translation": "иммигрант"},
            {"word": "soldier", "translation": "солдат"}
        ]
    },
    {
        "id": 5,
        "title": "The Story of the Internet",
        "level": "B1",
        "text": "The Internet changed our lives completely, but it started as a small project. In the 1960s, scientists in the United States created a network called ARPANET. It connected four computers at different universities. The goal was to share information quickly. In 1991, a British scientist named Tim Berners-Lee invented the World Wide Web. He wanted to make it easy for people to share documents. The first website was created in 1991 and it explained what the Web was. Today, more than five billion people use the Internet. We use it for work, study, entertainment, and talking with friends. Nobody could have imagined how big it would become.",
        "words": [
            {"word": "network", "translation": "сеть"},
            {"word": "connect", "translation": "соединять"},
            {"word": "university", "translation": "университет"},
            {"word": "goal", "translation": "цель"},
            {"word": "invent", "translation": "изобретать"},
            {"word": "documents", "translation": "документы"},
            {"word": "billion", "translation": "миллиард"},
            {"word": "entertainment", "translation": "развлечение"},
            {"word": "imagine", "translation": "представлять, воображать"},
            {"word": "completely", "translation": "полностью"}
        ]
    },
    {
        "id": 6,
        "title": "Why Cats Make Great Pets",
        "level": "A2",
        "text": "Cats are wonderful pets for many reasons. They are clean animals and spend a lot of time washing themselves. You do not need to take them for walks like dogs. Cats are also very independent, so they can stay home alone during the day. However, they still enjoy playing with their owners. Many cats love to chase toys and sleep in sunny places. Studies show that spending time with a cat can reduce stress and make you feel happier. Cats communicate by meowing, purring, and moving their tails. Each cat has its own personality. Some are shy, some are brave, and some are very funny!",
        "words": [
            {"word": "wonderful", "translation": "замечательный"},
            {"word": "reason", "translation": "причина"},
            {"word": "independent", "translation": "независимый"},
            {"word": "owner", "translation": "владелец"},
            {"word": "chase", "translation": "гоняться, преследовать"},
            {"word": "reduce", "translation": "уменьшать, снижать"},
            {"word": "stress", "translation": "стресс"},
            {"word": "communicate", "translation": "общаться"},
            {"word": "purr", "translation": "мурлыкать"},
            {"word": "personality", "translation": "личность, характер"}
        ]
    },
    {
        "id": 7,
        "title": "The Great Wall of China",
        "level": "B1",
        "text": "The Great Wall of China is one of the most famous structures in the world. It is about 21,000 kilometres long. People often say that you can see it from space, but this is not true. The wall was built over many centuries, starting in the 7th century BC. Different Chinese emperors added new sections to protect their land from enemies. Millions of workers helped build the wall. Many of them worked in very difficult conditions. Today, the Great Wall is a UNESCO World Heritage site. Millions of tourists visit it every year. The most popular part near Beijing is visited by thousands of people every day.",
        "words": [
            {"word": "structure", "translation": "строение, сооружение"},
            {"word": "kilometre", "translation": "километр"},
            {"word": "space", "translation": "космос"},
            {"word": "century", "translation": "век"},
            {"word": "emperor", "translation": "император"},
            {"word": "section", "translation": "секция, участок"},
            {"word": "protect", "translation": "защищать"},
            {"word": "enemy", "translation": "враг"},
            {"word": "conditions", "translation": "условия"},
            {"word": "tourist", "translation": "турист"}
        ]
    },
    {
        "id": 8,
        "title": "How to Learn a Language",
        "level": "B1",
        "text": "Learning a new language takes time and practice, but it can be very enjoyable. The most important thing is to be consistent. Try to study a little every day rather than many hours once a week. Listening to music and watching films in the language helps your ear get used to the sounds. Speaking with native speakers is also very useful, even if you make mistakes. Reading books and articles helps you learn new words in context. Using a flashcard app can help you remember vocabulary. Finally, do not be afraid to make mistakes. Everyone makes them when learning, and they help you improve.",
        "words": [
            {"word": "practice", "translation": "практика"},
            {"word": "enjoyable", "translation": "приятный, доставляющий удовольствие"},
            {"word": "consistent", "translation": "последовательный, постоянный"},
            {"word": "rather than", "translation": "а не, вместо того чтобы"},
            {"word": "native speaker", "translation": "носитель языка"},
            {"word": "useful", "translation": "полезный"},
            {"word": "mistake", "translation": "ошибка"},
            {"word": "context", "translation": "контекст"},
            {"word": "vocabulary", "translation": "словарный запас"},
            {"word": "improve", "translation": "улучшать(ся)"}
        ]
    },
    {
        "id": 9,
        "title": "A Letter from London",
        "level": "A2",
        "text": "Dear Emma, I am having a wonderful time in London! The city is amazing. Yesterday I visited the Tower of London and saw the Crown Jewels. They were beautiful. Then I walked across Tower Bridge and took many photos. Today I went to the British Museum. I saw the Rosetta Stone and Egyptian mummies. In the evening, I went to a musical in the West End. The singers were very talented. The food here is good but expensive. The weather is rainy, but I do not mind. English people are very polite and helpful. I will come back home next Saturday. See you soon! Love, Anna",
        "words": [
            {"word": "dear", "translation": "дорогой (в письме)"},
            {"word": "amazing", "translation": "потрясающий, удивительный"},
            {"word": "visit", "translation": "посещать"},
            {"word": "jewels", "translation": "драгоценности"},
            {"word": "museum", "translation": "музей"},
            {"word": "mummy", "translation": "мумия"},
            {"word": "talented", "translation": "талантливый"},
            {"word": "expensive", "translation": "дорогой"},
            {"word": "rainy", "translation": "дождливый"},
            {"word": "polite", "translation": "вежливый"}
        ]
    },
    {
        "id": 10,
        "title": "Robots in Our Life",
        "level": "B1",
        "text": "Robots are becoming a bigger part of our everyday life. In factories, robots build cars and electronic devices very quickly and without mistakes. In hospitals, robots help doctors perform difficult surgeries. Some robots can clean our homes, like robot vacuum cleaners. In the future, robots may deliver our food and packages. However, many people worry that robots will take their jobs. Experts say that robots will create new types of jobs too. For example, someone needs to program and repair the robots. It is important to learn new skills to work with technology. Robots are tools, not enemies. They can make our lives easier if we use them well.",
        "words": [
            {"word": "robot", "translation": "робот"},
            {"word": "factory", "translation": "фабрика, завод"},
            {"word": "device", "translation": "устройство, прибор"},
            {"word": "hospital", "translation": "больница"},
            {"word": "surgery", "translation": "хирургическая операция"},
            {"word": "vacuum cleaner", "translation": "пылесос"},
            {"word": "deliver", "translation": "доставлять"},
            {"word": "worry", "translation": "беспокоиться"},
            {"word": "expert", "translation": "эксперт"},
            {"word": "skill", "translation": "навык"}
        ]
    }
]


def get_all_articles():
    return ARTICLES

def get_article(article_id):
    for a in ARTICLES:
        if a["id"] == article_id:
            return a
    return None

def get_word_translation(word, articles=None):
    """Look up a word translation across all articles"""
    if articles is None:
        articles = ARTICLES
    word_lower = word.lower().strip(".,!?;:'\"()[]")
    for a in articles:
        for w in a["words"]:
            if w["word"].lower() == word_lower:
                return w["translation"]
    return None

import sqlite3
import asyncio
import os
import platform
import random
from datetime import datetime, date
import pytz
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, filters, ContextTypes
from content import generate_tasks
from db_data import get_word, get_verbs, get_all_verbs, get_test_questions, init_tables, populate_if_empty
from ege import get_all_ege_tasks, get_ege_task, check_ege_answer
from gtts import gTTS
import io

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

MOSCOW_TZ = pytz.timezone("Europe/Moscow")
DB_PATH = "englify.db"

# ---------- БАЗА ДАННЫХ ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    level TEXT DEFAULT 'novice',
                    language TEXT DEFAULT 'ru',
                    is_pro INTEGER DEFAULT 0,
                    daily_tasks_done INTEGER DEFAULT 0,
                    last_task_date TEXT DEFAULT ''
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS learned_words (
                    user_id INTEGER,
                    word TEXT,
                    learned_date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS completed_tasks (
                    user_id INTEGER,
                    task_id TEXT,
                    date TEXT,
                    correct INTEGER
                )''')
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT level, language, is_pro, daily_tasks_done, last_task_date FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"level": row[0], "language": row[1], "is_pro": bool(row[2]),
                "daily_tasks_done": row[3], "last_task_date": row[4]}
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        conn.close()
        return {"level": "novice", "language": "ru", "is_pro": False,
                "daily_tasks_done": 0, "last_task_date": ""}

def update_user(user_id, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for key, value in kwargs.items():
        c.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

def add_learned_word(user_id, word):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute("INSERT OR IGNORE INTO learned_words (user_id, word, learned_date) VALUES (?, ?, ?)",
              (user_id, word, today))
    conn.commit()
    conn.close()

def get_learned_words(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT word, learned_date FROM learned_words WHERE user_id = ? ORDER BY learned_date DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def record_task(user_id, task_id, correct):
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO completed_tasks (user_id, task_id, date, correct) VALUES (?, ?, ?, ?)",
              (user_id, task_id, today, int(correct)))
    conn.commit()
    conn.close()

def get_stats(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(correct) FROM completed_tasks WHERE user_id = ?", (user_id,))
    total, correct = c.fetchone()
    conn.close()
    return total or 0, correct or 0

def get_all_users_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE is_pro = 1")
    pro_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM learned_words")
    total_words = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM completed_tasks")
    total_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT user_id) FROM completed_tasks")
    active_users = c.fetchone()[0]
    c.execute("SELECT user_id, language FROM users ORDER BY user_id DESC LIMIT 10")
    recent = c.fetchall()
    conn.close()
    return {"total_users": total_users, "pro_users": pro_users,
            "total_words": total_words, "total_tasks": total_tasks,
            "active_users": active_users, "recent_users": recent}

# ---------- ПЕРЕВОДЫ ----------
def _(text_ru, text_en, lang):
    return text_en if lang == 'en' else text_ru

def main_menu_keyboard(lang):
    labels = {
        'ru': {"tasks": "📝 Задания", "verbs": "🐾 Глаголы", "words": "📚 Мои слова",
               "level": "🎚 Уровень", "mode": "🌐 Режим", "pro": "⭐ Pro", "ege": "🎯 ЕГЭ"},
        'en': {"tasks": "📝 Tasks", "verbs": "🐾 Verbs", "words": "📚 My words",
               "level": "🎚 Level", "mode": "🌐 Mode", "pro": "⭐ Pro", "ege": "🎯 USE"}
    }
    l = labels[lang]
    keyboard = [
        [InlineKeyboardButton(l["tasks"], callback_data="menu_tasks")],
        [InlineKeyboardButton(l["verbs"], callback_data="menu_verbs")],
        [InlineKeyboardButton(l["ege"], callback_data="menu_ege")],
        [InlineKeyboardButton(l["words"], callback_data="menu_words")],
        [InlineKeyboardButton(l["level"], callback_data="menu_level"),
         InlineKeyboardButton(l["mode"], callback_data="menu_mode")],
        [InlineKeyboardButton(l["pro"], callback_data="menu_pro")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- ЕЖЕДНЕВНАЯ РАССЫЛКА ----------
async def daily_job(app):
    now = datetime.now(MOSCOW_TZ)
    day_of_year = now.timetuple().tm_yday - 1
    word_data = get_word(day_of_year)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, language FROM users")
    users = c.fetchall()
    conn.close()
    for uid, lang in users:
        greeting = _("Доброе утро! ☀️", "Good morning! ☀️", lang)
        word_line = _(
            f"Слово дня: **{word_data['word']}** — {word_data['translation']}\nПример: {word_data['example']}",
            f"Word of the day: **{word_data['word']}** — {word_data['translation']}\nExample: {word_data['example']}",
            lang
        )
        keyboard = [
            [InlineKeyboardButton(_("✅ Выучил", "✅ Learned", lang), callback_data=f"learned_{word_data['word']}")],
            [InlineKeyboardButton(_("🔊 Озвучить", "🔊 Listen", lang), callback_data=f"voice_{word_data['word']}")],
            [InlineKeyboardButton(_("📋 Мои слова", "📋 My words", lang), callback_data="menu_words")]
        ]
        try:
            await app.bot.send_message(uid, f"{greeting}\n\n{word_line}",
                                       reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            pass

# ---------- ПЛАНИРОВЩИК ----------
async def scheduler(app):
    sent_today = False
    now = datetime.now(MOSCOW_TZ)
    if now.hour >= 9 and not sent_today:
        await daily_job(app)
        sent_today = True
    while True:
        now = datetime.now(MOSCOW_TZ)
        if now.hour == 9 and now.minute == 0 and not sent_today:
            await daily_job(app)
            sent_today = True
        if now.hour > 9:
            sent_today = False
        await asyncio.sleep(30)

# ---------- ОБРАБОТЧИКИ ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    lang = user["language"]
    text = _(
        "Привет! Я Englify — твой ежедневный помощник в изучении английского. Выбери действие:",
        "Hey! I'm Englify — your daily English learning buddy. Choose an option:",
        lang
    )
    keyboard = [
        [InlineKeyboardButton(_("📝 Тест на уровень", "📝 Level test", lang), callback_data="start_test")],
        [InlineKeyboardButton(_("⚡ Выбрать уровень самому", "⚡ Choose level", lang), callback_data="choose_level")],
        [InlineKeyboardButton(_("🌐 Переключить язык", "🌐 Switch language", lang), callback_data="toggle_lang")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = query.from_user.id
    user = get_user(uid)
    lang = user["language"]

    if data == "start_test":
        context.user_data["test_index"] = 0
        context.user_data["test_score"] = 0
        context.user_data["test_questions"] = get_test_questions()
        await send_test_question(query, context, uid, lang)
    elif data.startswith("test_"):
        questions = context.user_data.get("test_questions", get_test_questions())
        idx = context.user_data.get("test_index", 0)
        if idx >= len(questions):
            return
        chosen = int(data.split("_")[1])
        correct = questions[idx]["correct"]
        if chosen == correct:
            context.user_data["test_score"] += 1
        context.user_data["test_index"] += 1
        if context.user_data["test_index"] < len(questions):
            await send_test_question(query, context, uid, lang)
        else:
            score = context.user_data["test_score"]
            if score >= 12: level = "pro"
            elif score >= 7: level = "middle"
            else: level = "novice"
            update_user(uid, level=level)
            level_names = {"novice": _("Новичок", "Novice", lang),
                           "middle": _("Мидл", "Middle", lang),
                           "pro": _("Профи", "Pro", lang)}
            await query.edit_message_text(
                _("Тест завершён! Твой уровень: ", "Test finished! Your level: ", lang) + level_names[level],
                reply_markup=main_menu_keyboard(lang)
            )

    elif data == "choose_level":
        keyboard = [
            [InlineKeyboardButton(_("🟢 Новичок", "🟢 Novice", lang), callback_data="set_novice"),
             InlineKeyboardButton(_("🟡 Мидл", "🟡 Middle", lang), callback_data="set_middle"),
             InlineKeyboardButton(_("🔴 Профи", "🔴 Pro", lang), callback_data="set_pro")]
        ]
        await query.edit_message_text(_("Выбери уровень:", "Choose your level:", lang),
                                      reply_markup=InlineKeyboardMarkup(keyboard))
    elif data.startswith("set_"):
        level = data[4:]
        update_user(uid, level=level)
        await query.edit_message_text(_("Уровень сохранён!", "Level saved!", lang),
                                      reply_markup=main_menu_keyboard(lang))
    elif data == "toggle_lang":
        new_lang = "en" if lang == "ru" else "ru"
        update_user(uid, language=new_lang)
        await query.edit_message_text(_("Язык интерфейса изменён.", "Interface language changed.", new_lang),
                                      reply_markup=main_menu_keyboard(new_lang))
    elif data == "menu_tasks":
        if not user["is_pro"]:
            today = date.today().isoformat()
            if user["last_task_date"] != today:
                update_user(uid, daily_tasks_done=0, last_task_date=today)
                user["daily_tasks_done"] = 0
            if user["daily_tasks_done"] >= 3:
                await query.edit_message_text(
                    _("Сегодня ты уже выполнил 3 задания. Pro-версия снимает лимит!",
                      "You've completed 3 tasks today. Pro removes the limit!", lang),
                    reply_markup=main_menu_keyboard(lang))
                return
        now = datetime.now(MOSCOW_TZ)
        day_index = now.timetuple().tm_yday - 1
        level = user["level"]
        tasks = generate_tasks(day_index, level)
        context.user_data["current_tasks"] = tasks
        context.user_data["task_index"] = 0
        await show_task(query, tasks[0], lang, uid)
    elif data.startswith("answer_"):
        parts = data.split("_")
        chosen = int(parts[1])
        tasks = context.user_data.get("current_tasks")
        idx = context.user_data.get("task_index", 0)
        if not tasks or idx >= len(tasks):
            return
        task = tasks[idx]
        correct = chosen == task["correct"]
        now = datetime.now(MOSCOW_TZ)
        day_index = now.timetuple().tm_yday - 1
        record_task(uid, f"{user['level']}_{day_index}_{idx}", correct)
        today = date.today().isoformat()
        if user["last_task_date"] != today:
            update_user(uid, daily_tasks_done=1, last_task_date=today)
        else:
            update_user(uid, daily_tasks_done=user["daily_tasks_done"] + 1)
        feedback = _("✅ Верно!", "✅ Correct!", lang) if correct else _("❌ Неверно.", "❌ Wrong.", lang)
        context.user_data["task_index"] = idx + 1
        next_idx = idx + 1
        if next_idx < len(tasks):
            await show_task(query, tasks[next_idx], lang, uid, prefix=feedback + "\n\n")
        else:
            await query.edit_message_text(
                feedback + "\n\n" + _("🎉 Задания на сегодня закончены!", "🎉 All tasks done for today!", lang),
                reply_markup=main_menu_keyboard(lang)
            )
    elif data == "menu_words":
        words = get_learned_words(uid)
        if not words:
            text = _("Ты ещё не отметил ни одного слова.", "No words marked yet.", lang)
        else:
            text = _("📚 Выученные слова:\n", "📚 Learned words:\n", lang)
            for w, d in words:
                text += f"• {w} ({d})\n"
        await query.edit_message_text(text, reply_markup=main_menu_keyboard(lang))
    elif data == "menu_level":
        keyboard = [
            [InlineKeyboardButton(_("🟢 Новичок", "🟢 Novice", lang), callback_data="set_novice"),
             InlineKeyboardButton(_("🟡 Мидл", "🟡 Middle", lang), callback_data="set_middle"),
             InlineKeyboardButton(_("🔴 Профи", "🔴 Pro", lang), callback_data="set_pro")]
        ]
        await query.edit_message_text(_("Выбери уровень:", "Choose your level:", lang),
                                      reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "menu_mode":
        new_lang = "en" if lang == "ru" else "ru"
        update_user(uid, language=new_lang)
        await query.edit_message_text(_("Язык интерфейса изменён.", "Interface language changed.", new_lang),
                                      reply_markup=main_menu_keyboard(new_lang))
    elif data == "menu_pro":
        text = _(
            "⭐ Pro — всего 1 звезда Telegram навсегда!\nСнимает лимит заданий и включает перевод в English Mode.",
            "⭐ Pro — just 1 Telegram Star forever!\nRemoves daily task limit and enables translation in English Mode.",
            lang
        )
        keyboard = [
            [InlineKeyboardButton(_("💳 Купить Pro за ⭐1", "💳 Buy Pro for ⭐1", lang), callback_data="buy_pro")],
            [InlineKeyboardButton(_("⬅ Назад", "⬅ Back", lang), callback_data="back_main")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "buy_pro":
        await send_pro_invoice(query, uid, lang, context)
    elif data == "back_main":
        await query.edit_message_text(
            _("Выбери действие:", "Choose an option:", lang),
            reply_markup=main_menu_keyboard(lang)
        )

    elif data.startswith("learned_"):
        word = data[8:]
        add_learned_word(uid, word)
        await query.edit_message_text(
            _("Слово сохранено в изученные!", "Word saved as learned!", lang),
            reply_markup=main_menu_keyboard(lang)
        )
    elif data == "translate_task":
        if not user["is_pro"]:
            await query.answer(_("Доступно только в Pro", "Only available in Pro", lang), show_alert=True)
            return
        tasks = context.user_data.get("current_tasks")
        idx = context.user_data.get("task_index", 0)
        if tasks and idx < len(tasks):
            hint = f"Перевод: \"{tasks[idx].get('translation_hint', tasks[idx]['options'][tasks[idx]['correct']])}\""
        else:
            hint = "Нет задания"
        await query.answer(hint, show_alert=True)

    # ---------- ЕГЭ ----------
    elif data == "menu_ege":
        tasks = get_all_ege_tasks()
        buttons = []
        for t in tasks:
            label = f"Задание {t['type']}: {t['theme']}"
            buttons.append([InlineKeyboardButton(label, callback_data=f"ege_{t['id']}_0")])
        buttons.append([InlineKeyboardButton(_("⬅ Назад", "⬅ Back", lang), callback_data="back_main")])
        await query.edit_message_text(
            _("🎯 **ЕГЭ-тренажёр**\nВыбери задание:", "🎯 **USE Trainer**\nChoose a task:", lang),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif data.startswith("ege_ans_"):
        parts = data.split("_")
        task_id = int(parts[2])
        q_idx = int(parts[3])
        answer = int(parts[4])
        await handle_ege_answer(query, context, task_id, q_idx, answer, lang)
    elif data.startswith("ege_"):
        parts = data.split("_")
        if len(parts) >= 3:
            task_id = int(parts[1])
            q_idx = int(parts[2])
            task = get_ege_task(task_id)
            if not task:
                await query.edit_message_text("❌ Задание не найдено", reply_markup=main_menu_keyboard(lang))
                return
            await show_ege_question(query, context, task, q_idx, lang, uid)

    # ---------- ТРЕНАЖЁР ГЛАГОЛОВ ----------
    elif data == "menu_verbs":
        context.user_data["verb_score"] = 0
        context.user_data["verb_index"] = 0
        verbs = get_verbs(10)
        context.user_data["verbs"] = verbs
        await ask_verb_question(query, context, lang)
    elif data.startswith("verb_"):
        parts = data.split("_", 1)
        if len(parts) < 2:
            return
        answer_idx = int(parts[1])
        verbs = context.user_data.get("verbs")
        idx = context.user_data.get("verb_index", 0)
        if not verbs or idx >= len(verbs):
            return
        current_verb = verbs[idx]
        correct_idx = context.user_data.get("verb_correct_idx", 0)
        correct = (answer_idx == correct_idx)
        if correct:
            context.user_data["verb_score"] = context.user_data.get("verb_score", 0) + 1
        feedback = _("✅ Верно!", "✅ Correct!", lang) if correct else _("❌ Ошибка", "❌ Wrong", lang)
        context.user_data["verb_index"] = idx + 1
        if idx + 1 < len(verbs):
            await ask_verb_question(query, context, lang, prefix=feedback + "\n\n")
        else:
            total_score = context.user_data.get("verb_score", 0)
            await query.edit_message_text(
                feedback + "\n\n" +
                _("🎉 Тренировка завершена! Правильных: ", "🎉 Training finished! Correct: ", lang) +
                f"{total_score}/{len(verbs)}",
                reply_markup=main_menu_keyboard(lang)
            )

    elif data.startswith("voice_"):
        word = data[6:]
        await send_voice_word(uid, word, lang, context)
        await query.answer("🔊 Голосовое сообщение отправлено!")

async def ask_verb_question(query, context, lang, prefix=""):
    verbs = context.user_data.get("verbs")
    idx = context.user_data.get("verb_index", 0)
    if not verbs or idx >= len(verbs):
        return
    verb = verbs[idx]
    # Варианты: правильная форма V3, случайные другие V3
    correct_form = verb["v3"]
    other_forms = [v["v3"] for v in get_all_verbs() if v["v3"] != correct_form]
    random_forms = random.sample(other_forms, min(2, len(other_forms)))
    options = [correct_form] + random_forms
    random.shuffle(options)
    correct_idx = options.index(correct_form)
    context.user_data["verb_correct_idx"] = correct_idx
    question_text = _(
        f"🐱 Микки: Какая третья форма глагола **{verb['v1']}** ({verb['translation']})?\n( {verb['v1']} - {verb['v2']} - ??? )",
        f"🐱 Mickey: What's the V3 for **{verb['v1']}** ({verb['translation']})?\n( {verb['v1']} - {verb['v2']} - ??? )",
        lang
    )
    buttons = [[InlineKeyboardButton(opt, callback_data=f"verb_{i}")] for i, opt in enumerate(options)]
    await query.edit_message_text(prefix + question_text, reply_markup=InlineKeyboardMarkup(buttons))

async def show_ege_question(query, context, task, q_idx, lang, uid):
    fmt = task['format']
    total = len(task.get('headings', [])) if fmt == 'matching' else len(task.get('statements', [])) if fmt == 'true_false' else len(task.get('questions', []))

    if q_idx >= total:
        # Show results
        saved = context.user_data.get(f"ege_answers_{task['id']}", [])
        correct_count, total_count, results = check_ege_answer(task, saved)
        text = _(
            f"🎯 **{task['theme']}** — завершено!\n\n✅ Правильно: {correct_count}/{total_count}",
            f"🎯 **{task['theme']}** — finished!\n\n✅ Correct: {correct_count}/{total_count}", lang
        )
        if fmt == 'true_false':
            text += _("\n(1=True, 2=False, 3=Not stated)", "\n(1=True, 2=False, 3=Not stated)", lang)
        await query.edit_message_text(text, reply_markup=main_menu_keyboard(lang))
        return

    if fmt == 'matching':
        text = _(
            f"**{task['theme']}**\nЗадание 1. Установите соответствие\n\n"
            f"**Текст {task['texts'][q_idx]}**\n\n"
            f"Какой заголовок подходит?",
            f"**{task['theme']}**\nTask 1. Match the texts\n\n"
            f"**{task['texts'][q_idx]}**\n\n"
            f"Which heading fits?", lang
        )
        buttons = [[InlineKeyboardButton(f"{i}. {task['headings'][i-1][:50]}", callback_data=f"ege_ans_{task['id']}_{q_idx}_{i}")] for i in range(1, 8)]

    elif fmt == 'true_false':
        stmt = task['statements'][q_idx]
        text = _(
            f"**{task['theme']}**\nУтверждение {q_idx+1}/{total}\n\n{stmt}\n\n1 — True | 2 — False | 3 — Not stated",
            f"**{task['theme']}**\nStatement {q_idx+1}/{total}\n\n{stmt}\n\n1 — True | 2 — False | 3 — Not stated", lang
        )
        buttons = [
            [InlineKeyboardButton("1 ✅ True", callback_data=f"ege_ans_{task['id']}_{q_idx}_1"),
             InlineKeyboardButton("2 ❌ False", callback_data=f"ege_ans_{task['id']}_{q_idx}_2"),
             InlineKeyboardButton("3 ❓ Not stated", callback_data=f"ege_ans_{task['id']}_{q_idx}_3")]
        ]

    elif fmt == 'multiple_choice':
        q = task['questions'][q_idx]
        text = _(
            f"**{task['theme']}**\nВопрос {q['num']}\n\n{q['text']}",
            f"**{task['theme']}**\nQuestion {q['num']}\n\n{q['text']}", lang
        )
        buttons = [[InlineKeyboardButton(opt[:60], callback_data=f"ege_ans_{task['id']}_{q_idx}_{i}")] for i, opt in enumerate(q['options'])]

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def handle_ege_answer(query, context, task_id, q_idx, answer, lang):
    uid = query.from_user.id
    key = f"ege_answers_{task_id}"
    if key not in context.user_data:
        context.user_data[key] = []
    answers = context.user_data[key]
    while len(answers) <= q_idx:
        answers.append(None)
    answers[q_idx] = answer

    task = get_ege_task(task_id)
    if not task:
        return
    await show_ege_question(query, context, task, q_idx + 1, lang, uid)

async def send_test_question(query, context, uid, lang):
    questions = context.user_data.get("test_questions", get_test_questions())
    idx = context.user_data["test_index"]
    q = questions[idx]
    text = (f"Вопрос {idx+1}/{len(questions)}: {q['question']}" if lang == 'ru'
            else f"Question {idx+1}/{len(questions)}: {q['question']}")
    buttons = [[InlineKeyboardButton(opt, callback_data=f"test_{i}")] for i, opt in enumerate(q["options"])]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def show_task(query, task, lang, uid, prefix=""):
    text = prefix + task["question"]
    buttons = []
    for i, opt in enumerate(task["options"]):
        buttons.append([InlineKeyboardButton(opt, callback_data=f"answer_{i}")])
    if lang == 'en':
        buttons.append([InlineKeyboardButton("🔍 Translate", callback_data="translate_task")])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def send_pro_invoice(query, uid, lang, context):
    if query:
        await query.edit_message_text(
            _("🧾 Отправляю счёт…", "🧾 Sending invoice…", lang)
        )
    else:
        await context.bot.send_message(
            uid,
            _("🧾 Отправляю счёт…", "🧾 Sending invoice…", lang)
        )
    await context.bot.send_invoice(
        chat_id=uid,
        title=_("Englify Pro", "Englify Pro", lang),
        description=_(
            "Доступ к Pro-функциям навсегда:\n"
            "• Безлимитные задания\n"
            "• Перевод в English Mode\n"
            "• Эксклюзивные фичи",
            "Lifetime Pro access:\n"
            "• Unlimited tasks\n"
            "• Translation in English Mode\n"
            "• Exclusive features",
            lang
        ),
        payload="pro_subscription",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=_("Подписка Pro", "Pro Subscription", lang), amount=1)]
    )

async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    update_user(uid, is_pro=1)
    lang = get_user(uid)["language"]
    await update.message.reply_text(
        _(
            "🎉 Спасибо! Pro активирован навсегда!\n"
            "Теперь у тебя безлимитные задания и перевод в English Mode.",
            "🎉 Thank you! Pro activated forever!\n"
            "Now you have unlimited tasks and English Mode translation.",
            lang
        ),
        reply_markup=main_menu_keyboard(lang)
    )

def is_admin(update):
    return update.effective_user.id in ADMIN_IDS

async def add_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    try:
        target_id = int(context.args[0])
        update_user(target_id, is_pro=1)
        await update.message.reply_text(f"Пользователь {target_id} теперь Pro.")
    except:
        await update.message.reply_text("Использование: /addpro user_id")

async def remove_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    try:
        target_id = int(context.args[0])
        update_user(target_id, is_pro=0)
        await update.message.reply_text(f"У пользователя {target_id} отключён Pro.")
    except:
        await update.message.reply_text("Использование: /removepro user_id")

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    s = get_all_users_stats()
    text = (
        f"📊 **Статистика бота**\n\n"
        f"👤 Всего пользователей: {s['total_users']}\n"
        f"⭐ Pro пользователей: {s['pro_users']}\n"
        f"📝 Активных (задания): {s['active_users']}\n"
        f"📚 Выучено слов: {s['total_words']}\n"
        f"✅ Выполнено заданий: {s['total_tasks']}\n\n"
        f"**Последние 10 пользователей:**\n"
    )
    for uid, lang in s['recent_users']:
        text += f"• `{uid}` ({lang})\n"
    await update.message.reply_text(text)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    if not context.args:
        await update.message.reply_text("Использование: /broadcast <текст>")
        return
    message = " ".join(context.args)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users")
    users = c.fetchall()
    conn.close()
    sent = 0
    failed = 0
    for (uid,) in users:
        try:
            await context.bot.send_message(uid, f"📢 **Объявление:**\n\n{message}")
            sent += 1
        except:
            failed += 1
    await update.message.reply_text(f"Рассылка завершена.\n✅ Доставлено: {sent}\n❌ Ошибок: {failed}")



async def send_voice_word(chat_id, word, lang, context):
    """Озвучивает слово и отправляет голосовое сообщение"""
    try:
        # Создаём аудио в памяти
        tts = gTTS(text=word, lang='en', slow=False)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        # Отправляем как голосовое сообщение
        await context.bot.send_voice(
            chat_id=chat_id,
            voice=audio_bytes,
            caption=f"🔊 {word}"
        )
    except Exception as e:
        print(f"Ошибка озвучки: {e}")


# ---------- ЗАПУСК ----------
if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    init_db()
    init_tables()
    populate_if_empty()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addpro", add_pro))
    app.add_handler(CommandHandler("removepro", remove_pro))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("broadcast", broadcast))

    async def pay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        user = get_user(uid)
        await send_pro_invoice(None, uid, user["language"], context)

    app.add_handler(CommandHandler("pay", pay_command))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.add_handler(CallbackQueryHandler(button_handler))

    # /word без лишнего сообщения
    async def manual_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await daily_job(app)

    app.add_handler(CommandHandler("word", manual_word))

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(app))

    print("Бот запущен...")
    app.run_polling(close_loop=False)
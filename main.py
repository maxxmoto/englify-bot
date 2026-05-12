import sqlite3
import asyncio
import os
from datetime import datetime, date
import pytz
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from content import get_daily_word, generate_tasks
from test_data import TEST_QUESTIONS

# Загружаем секреты из .env файла
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

# ---------- ПЕРЕВОДЫ ----------
def _(text_ru, text_en, lang):
    return text_en if lang == 'en' else text_ru

def main_menu_keyboard(lang):
    labels = {
        'ru': {"tasks": "📝 Задания", "words": "📚 Мои слова", "level": "🎚 Уровень",
               "mode": "🌐 Режим", "pro": "⭐ Pro"},
        'en': {"tasks": "📝 Tasks", "words": "📚 My words", "level": "🎚 Level",
               "mode": "🌐 Mode", "pro": "⭐ Pro"}
    }
    l = labels[lang]
    keyboard = [
        [InlineKeyboardButton(l["tasks"], callback_data="menu_tasks")],
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
    word_data = get_daily_word(day_of_year)
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
            [InlineKeyboardButton(_("✅ Выучил", "✅ Learned"), callback_data=f"learned_{word_data['word']}")],
            [InlineKeyboardButton(_("📋 Мои слова", "📋 My words"), callback_data="menu_words")]
        ]
        try:
            await app.bot.send_message(uid, f"{greeting}\n\n{word_line}",
                                       reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            pass

# ---------- ПЛАНИРОВЩИК ----------
async def scheduler(app):
    sent_today = False
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
        [InlineKeyboardButton(_("📝 Тест на уровень", "📝 Level test"), callback_data="start_test")],
        [InlineKeyboardButton(_("⚡ Выбрать уровень самому", "⚡ Choose level"), callback_data="choose_level")],
        [InlineKeyboardButton(_("🌐 Переключить язык", "🌐 Switch language"), callback_data="toggle_lang")]
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
        await send_test_question(query, context, uid, lang)
    elif data.startswith("test_"):
        idx = context.user_data.get("test_index", 0)
        if idx >= len(TEST_QUESTIONS):
            return
        chosen = int(data.split("_")[1])
        correct = TEST_QUESTIONS[idx]["correct"]
        if chosen == correct:
            context.user_data["test_score"] += 1
        context.user_data["test_index"] += 1
        if context.user_data["test_index"] < len(TEST_QUESTIONS):
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
            [InlineKeyboardButton(_("🟢 Новичок", "🟢 Novice"), callback_data="set_novice"),
             InlineKeyboardButton(_("🟡 Мидл", "🟡 Middle"), callback_data="set_middle"),
             InlineKeyboardButton(_("🔴 Профи", "🔴 Pro"), callback_data="set_pro")]
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
            [InlineKeyboardButton(_("🟢 Новичок", "🟢 Novice"), callback_data="set_novice"),
             InlineKeyboardButton(_("🟡 Мидл", "🟡 Middle"), callback_data="set_middle"),
             InlineKeyboardButton(_("🔴 Профи", "🔴 Pro"), callback_data="set_pro")]
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
            "⭐ Pro-подписка снимает лимит заданий и включает перевод в English Mode.\nДля покупки напиши менеджеру @finpolq.",
            "⭐ Pro removes daily task limit and enables translation in English Mode.\nContact @finpolq to purchase.",
            lang
        )
        await query.edit_message_text(text, reply_markup=main_menu_keyboard(lang))
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

async def send_test_question(query, context, uid, lang):
    idx = context.user_data["test_index"]
    q = TEST_QUESTIONS[idx]
    text = (f"Вопрос {idx+1}/{len(TEST_QUESTIONS)}: {q['question']}" if lang == 'ru'
            else f"Question {idx+1}/{len(TEST_QUESTIONS)}: {q['question']}")
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

async def add_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    try:
        target_id = int(context.args[0])
        update_user(target_id, is_pro=1)
        await update.message.reply_text(f"Пользователь {target_id} теперь Pro.")
    except:
        await update.message.reply_text("Использование: /addpro user_id")

# ---------- ЗАПУСК ----------
if __name__ == "__main__":
    # Windows: переключаемся на SelectorEventLoop, чтобы избежать ошибок закрытия ProactorEventLoop
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    init_db()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addpro", add_pro))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем планировщик в текущем event loop
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(app))

    print("Бот запущен...")
    app.run_polling(close_loop=False)  # не закрываем цикл, чтобы планировщик продолжался
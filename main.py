import telebot
import schedule
import threading
import time
from bot_logic import parol, flip_coin, knb_game, play_knb_round
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

# Словарь для хранения игр пользователей
user_games = {}

# ---------- Обработчики команд ----------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """
                 
    🤖 Добро пожаловать в мой бот! 🤖

    Доступные команды:
    
    /start или /help - показать это сообщение
    /game - начать игру "Камень, Ножницы, Бумага"
    /pass - сгенерировать пароль
    /coin - подбросить монетку
    /set <секунды> - установить периодическое напоминание
    /unset - отменить все напоминания
    /vipolny - решить пример (только сложение, вычитание, умножение и деление)
    
    В игре "Камень, Ножницы, Бумага" просто напишите "камень", "ножницы" или "бумага" когда игра активна!
    """)

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_pass(message):
    bot.reply_to(message, f"Твой пароль: {parol(8)}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(commands=['game'])
def start_game(message):
    user_id = message.from_user.id
    # Начинаем новую игру
    user_games[user_id] = knb_game()
    
    response = "🎮 Игра 'Камень, Ножницы, Бумага' началась!\n"
    response += "Игра идет до 3 раундов.\n\n"
    response += "Напиши: камень, ножницы или бумага"
    bot.reply_to(message, response)

# ---------- Таймеры (из второго бота) ----------
def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beep!')

@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        # Планируем задачу с тегом, равным chat_id, чтобы можно было отменить позже
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
        bot.reply_to(message, f'Таймер установлен на каждые {sec} секунд.')
    else:
        bot.reply_to(message, 'Использование: /set <секунды>')

@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)
    bot.reply_to(message, 'Все таймеры для этого чата удалены.')

@bot.message_handler(commands=['vipolny'])
def calculate(message):
    expr = message.text.replace("/vipolny", "").strip()
    if not expr:
        bot.reply_to(message, "Пиши задачу правильно, например: 2+2")
        return
    try:
        # Просто вычисляем выражение
        result = eval(expr)
        bot.reply_to(message, f"Результат: {result}")
    except:
        bot.reply_to(message, "Пиши задачу правильно, например: 2+2")
        

# ---------- Обработка всех остальных сообщений ----------
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    text = message.text.lower()
    
    # Если у пользователя есть активная игра
    if user_id in user_games and user_games[user_id]['active']:
        # Игрок делает ход
        game_state, result = play_knb_round(user_games[user_id], text)
        user_games[user_id] = game_state
        bot.reply_to(message, result)
    else:
        # Если игрок пытается сделать ход без активной игры
        if text in ['камень', 'ножницы', 'бумага']:
            bot.reply_to(message, "У тебя нет активной игры. Начни игру с помощью /game")
        else:
            # Эхо-ответ для других сообщений
            bot.reply_to(message, f"Ты написал: {message.text}")

# ---------- Запуск бота с фоновым планировщиком ----------
if __name__ == '__main__':
    # Запускаем polling в отдельном потоке (daemon, чтобы он завершился при выходе)
    polling_thread = threading.Thread(target=bot.infinity_polling, name='bot_polling', daemon=True)
    polling_thread.start()

    # Основной поток занимается планировщиком
    while True:
        schedule.run_pending()
        time.sleep(1)

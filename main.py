import telebot
import settings
import keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(settings.Telegram.TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    msg = bot.send_message(message.chat.id, 'Давай познакомимся! Введи свои Фамилию, Имя, Отчество!')
    bot.register_next_step_handler(msg, fio_step)

def fio_step(message):
    user_info = message.text.split()
    msg = bot.send_message(
        message.chat.id,
        'Очень приятно! А теперь расскажи мне в каком классе ты учишься!',
        reply_markup=[keyboards.CLASS_CHOISE.keyboard]
    )
    bot.register_next_step_handler(msg, choise_class, user_info)

def choise_class(message, user_info):
    user_info.append(message.text)
    print(user_info)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
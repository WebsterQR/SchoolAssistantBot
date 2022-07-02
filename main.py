import telebot
import settings
import keyboards
import database
from aiogram.types import ReplyKeyboardRemove

bot = telebot.TeleBot(settings.Telegram.TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    msg = bot.send_message(
        message.chat.id,
        'Привет! Для начала мне нужно знать кто ты - учитель или ученик...',
        reply_markup=[keyboards.STUDENT_OR_TEACHER.keyboard]
    )
    bot.register_next_step_handler(msg, position_step)

def position_step(message):
    user_info = {
        'Фамилия': '',
        'Имя': '',
        'Отчество': '',
        'Класс': '',
        'Должность': ''
    }
    if message.text == "Ученик":
        user_info['Должность'] = 'Ученик'
    else:
        user_info['Должность'] = 'Учитель'
    msg = bot.send_message(
        message.chat.id,
        'А теперь давай познакомимся! Введи свои Фамилию, Имя, Отчество!',
        reply_markup=[ReplyKeyboardRemove()]
    )
    bot.register_next_step_handler(msg, fio_step, user_info)

def fio_step(message, user_info):
    FIO = message.text.split()
    user_info['Фамилия'] = FIO[0]
    user_info['Имя'] = FIO[1]
    user_info['Отчество'] = FIO[2]
    if user_info['Должность'] == 'Ученик':
        msg = bot.send_message(
            message.chat.id,
            f'Очень приятно, {user_info["Имя"]}! А теперь расскажи мне в каком классе ты учишься!',
            reply_markup=[keyboards.CLASS_CHOISE.keyboard]
        )
        bot.register_next_step_handler(msg, choise_class, user_info)
    else:
        msg = bot.send_message(
            message.chat.id,
            f'Очень приятно, {user_info["Имя"]}! Но мне нужно знать, действительно ли Вы учитель. '
            f'Пожалуйста, введите проверочный код',
        )
        bot.register_next_step_handler(msg, confirm_teacher, user_info)

def choise_class(message, user_info):
    user_info['Класс'] = message.text
    database.add_user(user_info)
    bot.send_message(
        message.chat.id,
        'Регистрация в боте прошла успешно!',
        reply_markup=[ReplyKeyboardRemove()]
    )
    print(user_info)

def confirm_teacher(message, user_info):
    if message.text == settings.auth.TEACHER_PASSWORD:
        database.add_user(user_info)
        bot.send_message(
            message.chat.id,
            'Регистрация в боте прошла успешно!',
            reply_markup=[ReplyKeyboardRemove()]
        )
    else:
        msg = bot.send_message(
            message.chat.id,
            'Неверный пароль, попробуйте еще раз!',
            reply_markup=[ReplyKeyboardRemove()]
        )
        bot.register_next_step_handler(msg, confirm_teacher, user_info)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
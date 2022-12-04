from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import common


class CLASS_CHOISE:
    keyboard = ReplyKeyboardMarkup()
    class_5a = KeyboardButton('5А')
    class_5b = KeyboardButton('5Б')
    class_5v = KeyboardButton('5В')
    class_5g = KeyboardButton('5Г')
    class_5d = KeyboardButton('5Д')

    class_6a = KeyboardButton('6A')
    class_6b = KeyboardButton('6Б')
    class_6v = KeyboardButton('6В')
    class_6g = KeyboardButton('6Г')
    class_6d = KeyboardButton('6Д')

    class_7a = KeyboardButton('7A')
    class_7b = KeyboardButton('7Б')
    class_7v = KeyboardButton('7В')
    class_7g = KeyboardButton('7Г')
    class_7d = KeyboardButton('7Д')

    class_8a = KeyboardButton('8A')
    class_8b = KeyboardButton('8Б')
    class_8v = KeyboardButton('8В')
    class_8g = KeyboardButton('8Г')

    class_9a = KeyboardButton('9А')
    class_9b = KeyboardButton('9Б')
    class_9v = KeyboardButton('9В')
    class_9g = KeyboardButton('9Г')

    class_10a = KeyboardButton('10A')
    class_10b = KeyboardButton('10Б')
    class_10v = KeyboardButton('10В')

    class_11a = KeyboardButton('11A')
    class_11b = KeyboardButton('11Б')
    class_11v = KeyboardButton('11В')

    keyboard.row(class_5a, class_5b, class_5v, class_5g, class_5d)
    keyboard.row(class_6a, class_6b, class_6v, class_6g, class_6d)
    keyboard.row(class_7a, class_7b, class_7v, class_7g, class_7d)
    keyboard.row(class_8a, class_8b, class_8v, class_8g)
    keyboard.row(class_9a, class_9b, class_9v, class_9g)
    keyboard.row(class_10a, class_10b, class_10v)
    keyboard.row(class_11a, class_11b, class_11v)


class STUDENT_OR_TEACHER:
    keyboard = ReplyKeyboardMarkup()
    student = KeyboardButton('Ученик')
    teacher = KeyboardButton('Учитель')
    keyboard.add(student, teacher)


class EMPTY_KEYBOARD:
    keyboard = ReplyKeyboardMarkup()


class MAIN_MENU:
    keyboard = ReplyKeyboardMarkup()
    homework = KeyboardButton('Домашнее задание')
    schedule = KeyboardButton('Расписание')
    find_teacher = KeyboardButton('Найти учителя')
    next_lesson = KeyboardButton('Следующий урок')
    keyboard.add(homework, schedule)
    keyboard.add(find_teacher, next_lesson)


class MAIN_MENU_FOR_TEACHERS:
    keyboard = ReplyKeyboardMarkup()
    schedule = KeyboardButton('Расписание (педагог)')
    add_homework = KeyboardButton('Добавить домашнее задание')
    notify_the_class = KeyboardButton('Оповестить класс')
    keyboard.add(schedule, add_homework)
    keyboard.add(notify_the_class)


class SCHEDULE:
    keyboard = ReplyKeyboardMarkup()
    today = KeyboardButton('Расписание на сегодня')
    tomorrow = KeyboardButton('Расписание на завтра')
    week = KeyboardButton('Расписание на всю неделю')
    keyboard.add(today, tomorrow)
    keyboard.add(week)


class FIND_TEACHER:
    keyboard = ReplyKeyboardMarkup()
    for teacher in common.teachers_list:
        button = KeyboardButton(teacher)
        keyboard.row(button)
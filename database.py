import datetime

import psycopg2

import common
import settings

def database_connect():
    try:
        conn = psycopg2.connect(dbname=settings.database.database,
                                user=settings.database.user,
                                password=settings.database.password,
                                host=settings.database.host)
    except:
        conn = False

    return conn

def add_user(user_info):
    conn = database_connect()
    if conn:
        cursor = conn.cursor()
        check_existence_user_and_delete_if_necessary(conn, cursor, user_info['telegram_chat_id'])
        if user_info['Должность'] == 'Ученик':
            class_id = get_class_id(cursor, user_info['Класс'])
        else:
            teacher_fio = user_info['Фамилия'] + ' ' + user_info['Имя'] + ' ' + user_info['Отчество']
            class_id = get_teachers_class_id(cursor, teacher_fio)
        cursor.execute("INSERT INTO users (name, surname, patronymic, position, class_id, user_id) "
                       "VALUES(%s, %s, %s, %s, %s, %s)",
                       (user_info['Имя'],
                        user_info['Фамилия'],
                        user_info['Отчество'],
                        user_info['Должность'],
                        class_id,
                        user_info['telegram_chat_id']))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        print("Error while connecting to database, user was not added")

def get_class_id(cursor, class_name):
    postgreSQL_select_Query = "SELECT class_id FROM classes WHERE class_name = %s"
    cursor.execute(postgreSQL_select_Query, (class_name,))
    data = cursor.fetchall()
    return data[0][0]


def get_teachers_class_id(cursor, teacher_fio):
    print(teacher_fio)
    postgreSQL_select_Query = "SELECT class_id FROM classroom_teachers WHERE teacher_fio = %s"
    cursor.execute(postgreSQL_select_Query, (teacher_fio,))
    data = cursor.fetchall()
    print(data)
    if data:
        return data[0][0]
    else:
        return 9999


def check_existence_user_and_delete_if_necessary(conn, cursor, chat_id):
    postgreSQL_select_Query = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(postgreSQL_select_Query, (chat_id,))
    data = cursor.fetchall()
    print(data)
    if len(data) > 0:
        postgreSQL_delete_Query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(postgreSQL_delete_Query, (chat_id,))
        conn.commit()

def get_class_id_by_chat_id(chat_id):
    conn = database_connect()
    if conn:
        cursor = conn.cursor()
        postgreSQL_select_Query = "SELECT class_id FROM users WHERE user_id = %s"
        cursor.execute(postgreSQL_select_Query, (chat_id,))
        data = cursor.fetchall()
        conn.close()
        return data

def get_shedule(day, chat_id):
    class_id = get_class_id_by_chat_id(chat_id)[0][0]
    print(class_id)
    today_date = datetime.date.today()
    week_day_num = today_date.isoweekday()
    conn = database_connect()
    if not conn:
        return 'error'
    cursor = conn.cursor()
    if day == 'today':
        week_day = common.week_day[week_day_num]
        if week_day_num == 7:
            str_ans = "Сегодня воскресенье, уроков нет!"
        else:
            data = common.students_schedule[common.class_name_id[class_id]][week_day]
            str_ans = 'Расписание на сегодня: \n'
            for el in data:
                str_ans += f'{el}) {data[el]} \n' if data[el] != None else ''
        return str_ans
    elif day == 'tomorrow':
        tomorrow_week_day_num = 1 if week_day_num == 7 else week_day_num + 1
        if tomorrow_week_day_num == 7:
            str_ans = "Завтра воскресенье, уроков нет!"
        else:
            week_day = common.week_day[tomorrow_week_day_num]
            data = common.students_schedule[common.class_name_id[class_id]][week_day]
            str_ans = 'Расписание на завтра: \n'
            for el in data:
                str_ans += f'{el}) {data[el]} \n' if data[el] != None else ''
            str_ans = 'Расписание на завтра: \n'
            for num, el in enumerate(data):
                str_ans += f'{num + 1}) {data[el]} \n' if data[el] != None else ''
        return str_ans
    elif day == 'all week':
        str_ans = 'Расписание на всю неделю: \n'
        for i in range(1, 7):
            if i == 6 and class_id < 80:
                continue
            data = common.students_schedule[common.class_name_id[class_id]]
            str_ans = 'Расписание на неделю: \n'
            for day in data:
                str_ans += f'{day}: \n'
                for lesson in data[day]:
                    str_ans += f'{lesson}) {data[day][lesson]} \n' if data[day][lesson] != None else ''
    return str_ans

def get_next_lesson(chat_id):
    current_hour = datetime.datetime.now().hour
    current_min = datetime.datetime.now().minute
    schedule = get_shedule('today', chat_id)
    lesson_num = get_lesson_num_by_time(current_hour, current_min)
    str_ans = f'Следующий урок {schedule[lesson_num]}'
    return str_ans

def get_lesson_num_by_time(hour, minute):
    all_mins = hour * 60 + minute
    return (all_mins - 540) // 60

def send_info_to_class(message, class_name, bot):
    class_id = common.class_name_to_class_id[class_name]
    conn = database_connect()
    teacher = message.chat.first_name + ' ' + message.chat.last_name
    if conn:
        cursor = conn.cursor()
        postgreSQL_select_Query = "SELECT * FROM users WHERE class_id = %s "
        cursor.execute(postgreSQL_select_Query, (class_id, ))
        data = cursor.fetchall()
        print(data)
        for student in data:
            bot.send_message(
                student[-1],
                f'Сообщение от учителя {teacher}: \n'
                f'{message.text}'
            )
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
        postgreSQL_delete_Query = "DELETE FROM users WHERE user_id = 176063054"
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
            postgreSQL_select_Query = "SELECT lesson, classroom_number FROM shedule WHERE week_day = %s AND class_id = %s"
            cursor.execute(postgreSQL_select_Query, (week_day, class_id))
            data = cursor.fetchall()
            str_ans = 'Расписание на сегодня: \n'
            for num, el in enumerate(data):
                str_ans += f'{num+1}) {el[0]} в кабинете {el[1]} \n'
        return str_ans
    elif day == 'tomorrow':
        tomorrow_week_day_num = 1 if week_day_num == 7 else week_day_num + 1
        if tomorrow_week_day_num == 7:
            str_ans = "Завтра воскресенье, уроков нет!"
        else:
            week_day = common.week_day[tomorrow_week_day_num]
            postgreSQL_select_Query = "SELECT lesson, classroom_number FROM shedule WHERE week_day = %s AND class_id = %s""
            cursor.execute(postgreSQL_select_Query, (week_day, class_id))
            data = cursor.fetchall()
            str_ans = 'Расписание на завтра: \n'
            for num, el in enumerate(data):
                str_ans += f'{num + 1}) {el[0]} в кабинете {el[1]} \n'
        return str_ans
    elif day == 'all week':
        pass

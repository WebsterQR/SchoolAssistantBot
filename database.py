import psycopg2
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

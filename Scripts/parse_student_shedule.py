import openpyxl as xl


classes_columns_mapping = {
    'C': '5А',
    'E': '5Б',
    'G': '5В',
    'I': '5Г',
    'K': '5Д',
    'M': '6А',
    'O': '6Б',
    'Q': '6В',
    'S': '6Г',
    'U': '6Д',
    'W': '7А',
    'Y': '7Б',
    'AA': '7В',
    'AC': '7Г',
    'AE': '7Д',
    'AG': '8А',
    'AI': '8Б',
    'AK': '8В',
    'AM': '8Г',
    'AO': '9А',
    'AQ': '9Б',
    'AS': '9В',
    'AU': '9Г',
    'AW': '10А',
    'AY': '10Б',
    'BA': '10В',
    'BC': '11А',
    'BE': '11Б',
    'BG': '11В',
}

def get_one_week_dict():
    one_week_dict = dict()
    for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        one_week_dict[day] = {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: ''
    }
    return one_week_dict
def create_base():
    classes = ['5А', '5Б', '5В', '5Г', '5Д',
               '6А', '6Б', '6В', '6Г', '6Д',
               '7А', '7Б', '7В', '7Г', '7Д',
               '8А', '8Б', '8В', '8Г',
               '9А', '9Б', '9В', '9Г',
               '10А', '10Б', '10В',
               '11А', '11Б', '11В']
    one_day_dict = {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: ''
    }
    one_week_dict = dict()

    # one_week_dict = {
    #     'Понедельник': one_day_dict,
    #     'Вторник': one_day_dict,
    #     'Среда': one_day_dict,
    #     'Четверг': one_day_dict,
    #     'Пятница': one_day_dict,
    #     'Суббота': one_day_dict
    # }
    base_schedule_dict = dict()
    for one_class in classes:
        base_schedule_dict[one_class] = get_one_week_dict()

    return base_schedule_dict

def get_week_day_and_lesson_number(num):
    week_day_num_mapping = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота'
    }
    week_day = week_day_num_mapping[(num - 5) // 7]
    lesson_num = (num - 5) % 7
    return week_day, lesson_num


if __name__ == '__main__':
    base_schedule_dict = create_base()
    wb = xl.load_workbook('./input_files/shedule_student_2022_2023.xlsx')
    #sheet_name =  wb.get_sheet_names()[0]
    sheet_name = wb.sheetnames
    sheet = wb[sheet_name[0]]
    # print(base_schedule_dict)
    for column_name in classes_columns_mapping:
        for row_num in range(5, 46):
            subject = sheet[f'{column_name}{row_num}'].value
            class_name = classes_columns_mapping[column_name]
            week_day, lesson_num = get_week_day_and_lesson_number(row_num)
            base_schedule_dict[class_name][week_day][int(lesson_num) + 1] = subject
    print(base_schedule_dict)

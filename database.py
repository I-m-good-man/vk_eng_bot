import psycopg2
import work_with_time


"""

-----------------------------------------------------

Здесь определены функции для работы с таблицами dates

-----------------------------------------------------

"""


def add_or_del_string_in_dates_table(date, del_date=False, add_date=False):
    """
    Эта функция либо доавбляет дату в таблицу с датами, либо удаляет дату.
    :param date: '26.10.2020' - пример входной даты.
    :param del_date:
    :param add_date:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    if del_date:
        cursor.execute(f"delete from dates where date = '{date}';")
    if add_date:
        cursor.execute(f"insert into dates values ('{date}');")

    conn.commit()
    conn.close()


def create_dates_table():
    """
    Эта функция создает таблицу dates, в которой хранятся только даты.
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute("""create table dates(date date);""")

    conn.commit()
    conn.close()


def get_dates_from_dates_table():
    """
    Функция возвращает все даты из таблицы dates.
    :return:
    """

    # конвертируем дату в валидный формат


    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute("""select date from dates""")

    res_l = []

    for date in cursor:
        date = date[0]
        date = f'{date.year}-{date.month}-{date.day}'
        res_l.append(date)
    conn.close()
    return res_l








"""

-----------------------------------------------------------------------------------------

Здесь определены функции для работы с таблицами-датами, в которых хранится инфа о юзерах.

-----------------------------------------------------------------------------------------

"""


def get_data_from_date_table(table_name):
    """
    Функция, которая возвращает все данные из таблицы-даты в виде списка словарей, в которых названия ключей совпадают
    с названиями полей в бд.
    :param table_name:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"select (user_id, number_of_learned_per_day, number_of_learned_words_before_this_day, number_of_repetitions, passed_the_words) from {table_name};")

    data_list = []

    cursor = cursor.fetchall()
    for string in cursor:
        temp_data_dict = {}

        temp_data_dict['user_id'] = int(string[0][1:-1].split(',')[0])
        temp_data_dict['number_of_learned_per_day'] = int(string[0][1:-1].split(',')[1])
        temp_data_dict['number_of_learned_words_before_this_day'] = int(string[0][1:-1].split(',')[2])
        temp_data_dict['number_of_repetitions'] = int(string[0][1:-1].split(',')[3])
        if string[0][1:-1].split(',')[4] == 'f':
            temp_data_dict['passed_the_words'] = False
        elif string[0][1:-1].split(',')[4] == 't':
            temp_data_dict['passed_the_words'] = True
        data_list.append(temp_data_dict)

    conn.close()
    return data_list


def create_date_table_for_new_day(date):
    """
    Эта функция создает новую таблицу для указанного дня.

    user_id - идент юзера
    number_of_learned_per_day - кол-во слов, которое он выучил за дату таблицы
    number_of_learned_words_before_this_day - кол-во слов, которое он выучил до этого дня
    number_of_repetitions - количество повторений слов. от 0 до 3
    number_of_reminders - количество напоминаний слов.

    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"""create table {date}(
    user_id integer primary key references user_data (user_id),
    number_of_learned_per_day integer,
    number_of_learned_words_before_this_day integer,
    number_of_repetitions integer,
    passed_the_words boolean,
    number_of_reminders integer
    );
    """)

    conn.commit()
    conn.close()


def get_number_of_reminders_from_date_table(table_name, user_id):
    """
    Функция, которая возвращает все данные из таблицы-даты в виде списка словарей, в которых названия ключей совпадают
    с названиями полей в бд.
    :param table_name:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()
    cursor.execute(f"select number_of_reminders from {table_name} where user_id={user_id};")
    number_of_reminders = cursor.fetchall()[0][0]
    conn.close()
    return number_of_reminders


def change_number_of_reminders_in_date_table(user_id, new_value, table_name):
    """
    Функция, которая меняет поле количества запоминаний.
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"update {table_name} set number_of_reminders={new_value} where user_id={user_id};")

    conn.commit()
    conn.close()


def add_strings_in_date_table(table_name, strings):
    """
    Функция, которая добавляет записи в табицу-дату. Также, функция может добавить в таблицу только одну запись.
    :param table_name:
    :param strings: -список со словарями, формат, в котором возвращает данные функция get_data_from_date_table
    :return:
    """

    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    # парсим список со словарями и делаем записи в таблицу
    for string in strings:
        user_id = string['user_id']
        number_of_learned_per_day = string['number_of_learned_per_day']
        number_of_learned_words_before_this_day = string['number_of_learned_words_before_this_day']
        number_of_repetitions = string['number_of_repetitions']
        passed_the_words = str(string['passed_the_words'])
        number_of_reminders = 0

        cursor.execute(f"""insert into {table_name} (user_id, 
                                                    number_of_learned_per_day,
                                                    number_of_learned_words_before_this_day, 
                                                    number_of_repetitions, passed_the_words, number_of_reminders) values ({user_id}, 
                                                    {number_of_learned_per_day},
                                                    {number_of_learned_words_before_this_day}, 
                                                    {number_of_repetitions}, '{passed_the_words}', {number_of_reminders});""")

    conn.commit()
    conn.close()


# add_strings_in_date_table('date_2020_12_17', [{'user_id':1, 'number_of_learned_per_day': 10, 'number_of_learned_words_before_this_day': 100, 'number_of_repetitions': 3, 'passed_the_words': True}, {'user_id':2, 'number_of_learned_per_day': 5, 'number_of_learned_words_before_this_day': 50, 'number_of_repetitions': 1, 'passed_the_words': False}])
# create_date_table_for_new_day('date_2020_12_13')
# print(get_data_from_date_table('date_2020_12_13'))


def change_number_of_repetitions_in_date_table(user_id, table_name, new_number_of_repetitions=1):
    """
    Функция, которая обновляет у юзера кол-во повторений слов за данный день.
    :param user_id: идент юзера
    :param table_name: название таблицы-даты
    :param new_number_of_repetitions: новое число повторений
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"select number_of_repetitions from {table_name} where user_id={user_id};")
    last_value = cursor.fetchall()[0][0]
    new_value = last_value + new_number_of_repetitions
    cursor.execute(f"update {table_name} set number_of_repetitions={new_value} where user_id={user_id};")

    conn.commit()
    conn.close()


def change_passed_the_words_in_date_table(user_id, table_name, flag):
    """
    Функция, которая меняет значение у поля passed_the_words - отправлены ли эти слова сегодня.
    :param user_id:
    :param flag:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"update {table_name} set passed_the_words={flag} where user_id={user_id};")

    conn.commit()
    conn.close()


def change_number_of_learned_per_day_in_date_table(user_id, table_name, words_number_in_dispatch):
    """
    Эта функция изменяет поле words_number_in_dispatch.
    :param user_id:
    :param label_date_table:
    :param words_number_in_dispatch:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"update {table_name} set number_of_learned_per_day={words_number_in_dispatch} where user_id={user_id};")

    conn.commit()
    conn.close()


def del_string_in_date_table(user_id, table_name):
    """
    Функция удаляет запись из таблицы-даты.
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"delete from {table_name} where user_id = '{user_id}';")

    conn.commit()
    conn.close()


"""

--------------------------------------------------------------------------------------------------------------

Здесь определены функции для работы с таблицой user_data - изменениями, проверками значений полей строк и т.д.

--------------------------------------------------------------------------------------------------------------

"""


def add_new_string_in_table_user_data(user_id, dispatch_time, words_number_in_dispatch=5,
                                  learned_words=0, number_of_day_admission=0, correct_learned_word_counter=0):
    """
    Добавляет новую строку в базовую таблицу users.
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()
    cursor.execute(f"""insert into user_data (user_id, 
                                        dispatch_time, 
                                        words_number_in_dispatch, 
                                        learned_words, 
                                        number_of_day_admission,
                                        correct_learned_word_counter) values ({user_id}, 
                                                                '{dispatch_time}', 
                                                                {words_number_in_dispatch}, 
                                                                {learned_words}, 
                                                                {number_of_day_admission},
                                                                {correct_learned_word_counter});""")
    conn.commit()
    conn.close()


def create_table_user_data():
    """
    Создает основную таблицу с данными о пользователях.


    user_id - идент юзера
    dispatch_time - время ежедневной рассылки слов
    words_number_in_dispatch - кол-во слов в ежеднвеной рассылке
    learned_words - сколько всего выучено слов
    number_of_day_admission - кол-во дней пропуска обучения
    correct_learned_word_counter - правильный счетчик выученных слов

    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute("""create table user_data(user_id integer primary key, 
                                            dispatch_time time, 
                                            words_number_in_dispatch integer, 
                                            learned_words integer, 
                                            number_of_day_admission integer,
                                            correct_learned_word_counter integer);""")

    conn.commit()
    conn.close()


def change_number_correct_learned_word_counter(user_id, learned_words):
    """
    Эта функция меняет в бд правильный счетчик выученных слов.
    :param user_id:
    :param learned_words:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"update user_data set correct_learned_word_counter={learned_words} where user_id={user_id};")

    conn.commit()
    conn.close()


def change_number_of_word_in_dispatch(user_id, words_number_in_dispatch):
    """
    Эта функция меняет в бд количество слов ежедневной рассыллки
    :param user_id:
    :param words_number_in_dispatch:
    :return:
    """

    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"update user_data set words_number_in_dispatch={words_number_in_dispatch} where user_id={user_id};")

    conn.commit()
    conn.close()


def change_number_learned_words(user_id, learned_words):
    """
    Эта функция меняет в бд количество выученных слов пользователем.
    :param user_id:
    :param learned_words:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"update user_data set learned_words={learned_words} where user_id={user_id};")

    conn.commit()
    conn.close()


def change_dispatch_time(user_id, dispatch_time):
    """
    Эта функция меняет в бд время отправки ежедневноой рассылки слов на английском языке.
    :param user_id:
    :param dispatch_time:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"update user_data set dispatch_time='{dispatch_time}' where user_id={user_id};")

    conn.commit()
    conn.close()


def check_user_in_user_data_table(user_id):
    """
    Проверяет, есть ли пользователь в базе данных, в таблице user_data
    :param user_id:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute("select user_id from user_data;")

    res = False

    for i in cursor:
        if user_id in i:
            res = True
            break

    conn.close()

    return res


def change_number_of_day_admission(user_id, new_number_of_day_admission):
    """
    Функция изменяет кол-во дней пропуска.
    :param user_id:
    :param new_number_of_day_admission: если равно 1, то увелич прежнее значение в таблице на 1, если 0, то обнуляет его.
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    if new_number_of_day_admission == 1:
        cursor.execute(f"select number_of_day_admission from user_data where user_id={user_id};")
        last_value = cursor.fetchall()[0][0]
        new_value = last_value + 1
        cursor.execute(f"update user_data set number_of_day_admission={new_value} where user_id={user_id};")

    elif new_number_of_day_admission == 0:
        new_value = 0
        cursor.execute(f"update user_data set number_of_day_admission={new_value} where user_id={user_id};")

    conn.commit()
    conn.close()


def get_data_about_user_from_user_data_table(user_id):
    """
    Функция, которое нужна, чтобы получить данные о пользователе из основной таблицы базы данных user_data
    :param user_id:
    :return:
    """

    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"select (dispatch_time, words_number_in_dispatch, number_of_day_admission, learned_words, correct_learned_word_counter) from user_data where user_id={user_id};")

    main_user_data = {}
    string = cursor.fetchall()[0]
    dispatch_time = string[0][1:-1].split(',')[0]
    # переводим время отправки в секунды
    hour, min = list(map(int, dispatch_time.split(':')[:-1]))
    dispatch_time_sec = hour * 3600 + min * 60

    main_user_data['dispatch_time'] = dispatch_time_sec
    main_user_data['words_number_in_dispatch'] = int(string[0][1:-1].split(',')[1])
    main_user_data['number_of_day_admission'] = int(string[0][1:-1].split(',')[2])
    main_user_data['learned_words'] = int(string[0][1:-1].split(',')[3])
    main_user_data['correct_learned_word_counter'] = int(string[0][1:-1].split(',')[4])

    conn.close()

    return main_user_data


def get_all_users_from_user_data_table():
    """
    Фукнция возвращает user_id всех пользователей бота
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"select user_id from user_data;")

    user_id_generator = [string[0] for string in list(cursor)]

    conn.close()

    return user_id_generator


def check_subscribe_status(user_id):
    """
    Эта функция проверяет, подписпан ли пользователь на сообшество.
    :param user_id:
    :return:
    """
    pass


def change_subscription_status(user_id, status):
    """
    Эта функция меняет в бд состояние подписки пользователя (True или False).
    :param user_id:
    :param status:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    # меняем

    conn.commit()
    conn.close()


def del_string_in_user_data_table(user_id):
    """
    Функция удаляет запись из таблицы user_data.
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"delete from user_data where user_id = '{user_id}';")

    conn.commit()
    conn.close()


"""

-----------------------------------------------------

Здесь определены функции для работы с таблицой words.

-----------------------------------------------------

"""


def get_words_string_from_table_words(number_of_learned_words_before_this_day, words_number_in_dispatch):
    """
    Функция, которая возвращает строку со словами, которые берет из бд, основываясь на кол-ве слов в рассылке кол-ве
    слов, которые юзер выучил до времени отправки (это номер последнего выученного слова).
    :param number_of_learned_words_before_this_day:
    :param words_number_in_dispatch:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"select (eng_word, transcription, rus_word) from words where number > {number_of_learned_words_before_this_day} "
                   f"and number <{number_of_learned_words_before_this_day + words_number_in_dispatch+1} ;")
    res_str = ''
    for string in cursor:
        string = string[0]
        string = string[1:-1]
        eng_word, transcription, rus_word = string.split(',')

        # изменяем формат данных

        if '"' in rus_word:
            rus_word = rus_word[1:-1]

        if '"' in eng_word:
            eng_word = eng_word[1:-1]

        if '"' in transcription:
            transcription = transcription[1:-1]

        if '/' in rus_word:
            rus_word = rus_word.replace(' /', ',')

        if ' ( брит. )' in rus_word:
            rus_word = rus_word.replace(' ( брит. )', '')

        res_str += f'{eng_word} [{transcription}] - {rus_word}\n'
    conn.close()
    return res_str



def search_bugs(number_of_learned_words_before_this_day, words_number_in_dispatch):
    """
    Функция, которая возвращает строку со словами, которые берет из бд, основываясь на кол-ве слов в рассылке кол-ве
    слов, которые юзер выучил до времени отправки (это номер последнего выученного слова).
    :param number_of_learned_words_before_this_day:
    :param words_number_in_dispatch:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(
        f"select (eng_word, transcription, rus_word) from words where number > {number_of_learned_words_before_this_day} and number <{number_of_learned_words_before_this_day + words_number_in_dispatch + 1} ;")

    res_str = ''
    c = 0
    for string in cursor:
        string = string[0]
        string = string[1:-1]
        try:
            eng_word, transcription, rus_word = string.split(',')
        except:
            print(string)
            c += 1
    print(c)


def change_number_of_learned_words_before_this_day_from_date_table(new_number, user_id, table_name):
    """
    Функция, которая меняет в таблице дате количество слов, выученных до этого дня
    в таблице дате.
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()
    cursor.execute(f"update {table_name} set number_of_learned_words_before_this_day={new_number} where user_id={user_id};")
    conn.commit()
    conn.close()



def get_words_list_from_table_words(number_of_learned_words_before_this_day, words_number_in_dispatch):
    """
    Функция, которая возвращает словарь со словами, которые берет из бд, основываясь на кол-ве слов в рассылке кол-ве
    слов, которые юзер выучил до времени отправки (это номер последнего выученного слова).

    Эта фцнкция возвращает список со словами с удобным форматом данных для функции проверки слов.
    :param number_of_learned_words_before_this_day:
    :param words_number_in_dispatch:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"select (eng_word, transcription, rus_word) from words where number > {number_of_learned_words_before_this_day} and number <{number_of_learned_words_before_this_day + words_number_in_dispatch+1} ;")

    res_list = []
    for string in cursor:
        string = string[0]
        string = string[1:-1]

        eng_word, transcription, rus_word = string.split(',')
        # изменяем формат данных

        if '"' in rus_word:
            rus_word = rus_word[1:-1]

        if '"' in eng_word:
            eng_word = eng_word[1:-1]

        if '"' in transcription:
            transcription = transcription[1:-1]

        if '/' in rus_word:
            rus_word = rus_word.replace(' /', ',')

        if ' ( брит. )' in rus_word:
            rus_word = rus_word.replace(' ( брит. )', '')
        # checked - поле, в котором отмечается, проверили ли это слово у юзера уже, или нет
        res_list.append({'eng_word': eng_word, 'transcription': transcription, 'rus_word': rus_word, 'checked': False})

    conn.close()

    return res_list

# print(get_words_list_from_table_words(1038, 5))


"""

-------------------------------

Здесь определены общие функции.

-------------------------------

"""


def commit_decorator(commit_needed=True):
    """
    Декоратор для того, чтобы можно было настроить внутренний декоратор, нужно ли коммитить в бд или нет.
    :param commit_needed:
    :return:
    """

    def decorator_for_works_with_db(func):
        """
        Декоратор для проделывания рутинных задач - подключение к бд, создание курсора и тд
        :param func:
        :return:
        """

        def wrapper():
            conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
            cursor = conn.cursor()

            res = func(cursor)

            if commit_needed:
                print('commit')
                conn.commit()
            conn.close()

            return res

        return wrapper

    return decorator_for_works_with_db


def show_all_tables():
    """
    Функция, которая возвращает все доступные таблицы из базы данных.
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute("select table_name from information_schema.tables where table_schema='public' order by table_name;")
    table_names = cursor.fetchall()

    conn.commit()
    conn.close()

    return [i[0] for i in table_names]


def del_table(*table_names):
    """
    Эта функция удаляет из базы данных указанную в аргументе таблицу.
    :param table_name:
    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    for table_name in table_names:
        cursor.execute(f"drop table {table_name};")

    conn.commit()
    conn.close()


def delete_user_from_bot(*user_id):
    """
    Функция удаляет юзера из всей базы данных
    :param user_id:
    :return:
    """
    user_id = user_id[0]
    # сначала удаляем юзера из таблицы user_data
    del_string_in_user_data_table(user_id)

    # удаляем юзеров из таблиц - дат
    dates = get_dates_from_dates_table()
    for date in dates:
        date = date.replace('-', '_')
        table_name = f'date_{date}'
        table_data = get_data_from_date_table(table_name)
        if table_data:
            for user_data in table_data:
                if user_id == user_data['user_id']:
                    del_string_in_date_table(user_id, table_name)
                    break

def get_data_about_users():
    """
    Функция возвращает общую информацию о всех пользователях.
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute(f"select (dispatch_time, words_number_in_dispatch, number_of_day_admission, learned_words, correct_learned_word_counter) from user_data;")

    counter_for_0_day_admission = 0
    counter_for_less_5_day_admission = 0
    counter_for_more_10_day_admission = 0
    counter_for_more_100_learned_words = 0

    for string in cursor.fetchall():
        main_user_data = {}
        main_user_data['number_of_day_admission'] = int(string[0][1:-1].split(',')[2])
        main_user_data['correct_learned_word_counter'] = int(string[0][1:-1].split(',')[4])

        if main_user_data['number_of_day_admission'] == 0:
            counter_for_0_day_admission += 1
        elif main_user_data['number_of_day_admission'] < 5:
            counter_for_less_5_day_admission += 1
        elif main_user_data['number_of_day_admission'] > 10:
            counter_for_more_10_day_admission += 1

        if main_user_data['correct_learned_word_counter'] >= 100:
            counter_for_more_100_learned_words += 1

    conn.close()

    res_string = f'Люди, у которых 0 дней пропуска: {counter_for_0_day_admission}.\n' \
                 f'Люди, у которых меньше 5 дней пропуска: {counter_for_less_5_day_admission}.\n' \
                 f'Люди, у которых больше 10 дней пропуска: {counter_for_more_10_day_admission}.\n' \
                 f'Люди, которые выучили больше 100 слов: {counter_for_more_100_learned_words}.\n'

    return res_string


import psycopg2


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


def create_table_user_data():
    """
    Создает основную таблицу с данными о пользователях.


    user_id - идент юзера
    dispatch_time - время ежедневной рассылки слов
    words_number_in_dispatch - кол-во слов в ежеднвеной рассылке
    learned_words - сколько всего выучено слов
    number_of_day_admission - кол-во дней пропуска обучения


    :return:
    """
    conn = psycopg2.connect(dbname='mydb', user='postgres', password='marat242003', host='localhost')
    cursor = conn.cursor()

    cursor.execute("""create table user_data(user_id integer primary key, 
                                            dispatch_time time, 
                                            words_number_in_dispatch integer, 
                                            learned_words integer, 
                                            number_of_day_admission integer);""")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_dates_table()
    create_table_user_data()
    input()







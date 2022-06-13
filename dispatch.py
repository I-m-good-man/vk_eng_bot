import work_with_time
import database
from work_with_vk_pkg import vk
from work_with_vk_pkg import messages
from work_with_vk_pkg import keyboards
import random
import time
import multiprocessing


"""
Вся работа с датами в коде идет в формату год-месяц-день. Формат, в котором хранятся даты в таблице dates
Также в бд используюются таблицы-даты, их имена существую в формате date_год_месяц_день - формат аналогиче вышеописанному.

В бд есть таблица дат, в которой хранится самое большое 60 дат. Для каждой даты из таблицы существуют своя отдельная
таблица, в которой хранятся данные именно об этом дне для каждого юзера:
1) user_id - идент пользователя.
2) number_of_learned_per_day - кол-во слов, которое юзер выучил за этот день
3) number_of_learned_words_before_this_day - кол-во слов, которое юзер выучил до этого дня
4) number_of_repetitions - кол-во повторений слов, выученных в эту дату
5) passed_the_words - маркер, который нужен чтобы определить, отправили ли слова в эту дату.

Бот использует метод интервального повторения, поэтому он отправляет юзеру слова из каждой даты всего 4 раза, используя
между отправками разные временные промежутки. 
После запоминания:
1) Первое повторение спустя 2 дня.
2) Второе повторение спустя 10 дней.
3) Третье повторение спустя 30 дней.
4) Четвертое повторение спустя 60 дней.

"""


def gen_table_name_for_date_table(date):
    """
    Функция для преобразования даты в название таблицы, пример:
    дата - 2020-12-13
    название таблицы - date_2020_12_13
    :param date:
    :return:
    """
    date = date.replace('-', '_')
    table_name = f'date_{date}'
    return table_name


def old_early_dispatch(user_id):
    """
    Функция отправляет юзеру слова, чтобы он не дожидался ежедневной расслыки.
    :param user_id:
    :return:
    """
    current_server_time = work_with_time.get_current_server_handy_time()

    current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'

    data_list = database.get_data_from_date_table(gen_table_name_for_date_table(current_server_date))

    for string in data_list:
        if string['user_id'] == user_id:
            number_of_learned_words_before_this_day = string['number_of_learned_words_before_this_day']

            main_user_data = database.get_data_about_user_from_user_data_table(user_id)
            words_number_in_dispatch = main_user_data['words_number_in_dispatch']

            words_string = database.get_words_string_from_table_words(number_of_learned_words_before_this_day,
                                                                      words_number_in_dispatch)

            msg_dispatch = messages.gen_early_dispatch_msg(words_string, words_number_in_dispatch)
            vk.send_message(user_id, msg_dispatch, keyboard=keyboards.base_user_keyboard.get_keyboard())

            database.change_passed_the_words_in_date_table(user_id, gen_table_name_for_date_table(current_server_date), True)
            break


def early_dispatch(*user_id_for_early_dispatch):
    """
    Новая функция ранней рассылки, которая присылает пользователю слова для повторения.
    :param user_id:
    :return:
    """

    user_id_for_early_dispatch = user_id_for_early_dispatch[0]

    # отправляем юзеру сообщение о том, чтобы он немного подождал
    wait_a_little_msg = messages.wait_a_little_msg
    vk.send_message(user_id_for_early_dispatch, wait_a_little_msg)

    current_server_time = work_with_time.get_current_server_handy_time()

    current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'
    current_server_date_sec = work_with_time.get_date_to_sec(current_server_date)

    # серверное время, которое прошло с начала дня в секундах
    current_server_time_per_day_sec = current_server_time.tm_hour * 3600 + current_server_time.tm_min * 60

    # получаем список со всеми датами и упорядочиваем его в порядке возрастания дат
    dates = database.get_dates_from_dates_table()
    dates.sort(key=lambda date: work_with_time.get_date_to_sec(date))

    # в цикле перебираем даты из упорядоченного в порядке возрастания списка с датами, которые есть в бд
    # для каждой даты получаем данные с записями о пользователях на эту дату
    for date in dates:
        label_date_table = gen_table_name_for_date_table(date)
        data_list = database.get_data_from_date_table(label_date_table)

        # переводим дату в секунды
        date_sec = work_with_time.get_date_to_sec(date)

        # разница между текущей серверной датой и датой из списка в днях
        dif_between_dates = int((current_server_date_sec - date_sec) // 86400)

        # если разница между датами равна 60 дней, то для юзеров из этой даты пришло время для четвертого повторения
        if dif_between_dates == 60:
            # перебираем список с табличными данными о пользователях на эту дату
            for user_data in data_list:
                user_id = user_data['user_id']
                number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                number_of_repetitions = user_data['number_of_repetitions']

                # если пользователь еще ни разу не повторял слова
                if user_id == user_id_for_early_dispatch and number_of_repetitions == 3:
                    # получаем данные о пользователе из основной таблицы user_data
                    main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                    dispatch_time_sec = main_user_data['dispatch_time']
                    words_number_in_dispatch = main_user_data['words_number_in_dispatch']

                    # генерируем строку со словами для отправки
                    words_string = database.get_words_string_from_table_words(
                        number_of_learned_words_before_this_day,
                        words_number_in_dispatch)

                    msg_dispatch = messages.gen_repeat_words_4_msg(words_string)

                    # отправляем юзеру сообщение
                    vk.send_message(user_id, msg_dispatch)

                    # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                    database.change_number_of_repetitions_in_date_table(user_id,
                                                                        gen_table_name_for_date_table(date), 1)

        # если разница между датами равна 30 дней, то для юзеров из этой даты пришло время для третьего повторения
        elif dif_between_dates == 30:
            # перебираем список с табличными данными о пользователях на эту дату
            for user_data in data_list:
                user_id = user_data['user_id']
                number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                number_of_repetitions = user_data['number_of_repetitions']

                # если пользователь еще ни разу не повторял слова
                if user_id == user_id_for_early_dispatch and number_of_repetitions == 2:
                    # получаем данные о пользователе из основной таблицы user_data
                    main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                    dispatch_time_sec = main_user_data['dispatch_time']
                    words_number_in_dispatch = main_user_data['words_number_in_dispatch']

                    # генерируем строку со словами для отправки
                    words_string = database.get_words_string_from_table_words(
                        number_of_learned_words_before_this_day,
                        words_number_in_dispatch)

                    msg_dispatch = messages.gen_repeat_words_3_msg(words_string)

                    # отправляем юзеру сообщение
                    vk.send_message(user_id, msg_dispatch)

                    # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                    database.change_number_of_repetitions_in_date_table(user_id,
                                                                        gen_table_name_for_date_table(date), 1)
        # если разница между датами равна 10 дней, то для юзеров из этой даты пришло время для второго повторения
        elif dif_between_dates == 10:
            # перебираем список с табличными данными о пользователях на эту дату
            for user_data in data_list:
                user_id = user_data['user_id']
                number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                number_of_repetitions = user_data['number_of_repetitions']

                # если пользователь еще ни разу не повторял слова
                if user_id == user_id_for_early_dispatch and number_of_repetitions == 1:
                    # получаем данные о пользователе из основной таблицы user_data
                    main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                    dispatch_time_sec = main_user_data['dispatch_time']
                    words_number_in_dispatch = main_user_data['words_number_in_dispatch']

                    # генерируем строку со словами для отправки
                    words_string = database.get_words_string_from_table_words(
                        number_of_learned_words_before_this_day,
                        words_number_in_dispatch)

                    msg_dispatch = messages.gen_repeat_words_2_msg(words_string)

                    # отправляем юзеру сообщение
                    vk.send_message(user_id, msg_dispatch)

                    # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                    database.change_number_of_repetitions_in_date_table(user_id,
                                                                        gen_table_name_for_date_table(date), 1)

        # если разница между датами равна 2 дня, то для юзеров из этой даты пришло время для первого повторения
        elif dif_between_dates == 2:
            # перебираем список с табличными данными о пользователях на эту дату
            for user_data in data_list:
                user_id = user_data['user_id']
                number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                number_of_repetitions = user_data['number_of_repetitions']

                # если пользователь еще ни разу не повторял слова и если user_id пользователя из теблицы совпадает
                if user_id == user_id_for_early_dispatch and number_of_repetitions == 0:
                    # получаем данные о пользователе из основной таблицы user_data
                    main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                    dispatch_time_sec = main_user_data['dispatch_time']
                    words_number_in_dispatch = main_user_data['words_number_in_dispatch']

                    # генерируем строку со словами для отправки
                    words_string = database.get_words_string_from_table_words(
                        number_of_learned_words_before_this_day,
                        words_number_in_dispatch)

                    msg_dispatch = messages.gen_repeat_words_1_msg(words_string)

                    # отправляем юзеру сообщение
                    vk.send_message(user_id, msg_dispatch)

                    # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                    database.change_number_of_repetitions_in_date_table(user_id,
                                                                        gen_table_name_for_date_table(date), 1)

        # если разница между датами равна 0 дней, то значит, дата совпадает с серверной датой
        elif dif_between_dates == 0:
            # перебираем список с табличными данными о пользователях на эту дату
            for user_data in data_list:
                user_id = user_data['user_id']
                number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                passed_the_words = user_data['passed_the_words']
                number_of_learned_per_day = user_data['number_of_learned_per_day']

                # если id пользователя из таблицы совпадает с айди пользователя которому должны отправить раннюю рассылку
                if user_id == user_id_for_early_dispatch:
                    # получаем данные о пользователе из основной таблицы user_data
                    main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                    dispatch_time_sec = main_user_data['dispatch_time']
                    words_number_in_dispatch = main_user_data['words_number_in_dispatch']
                    learned_words = main_user_data['learned_words']

                    # если пользователь уже выучил слова за сегодняшний день, то мы не должны отправлять ему слова
                    # за завтрашний день
                    if number_of_learned_per_day:
                        learned_words -= number_of_learned_per_day

                    # сразу отправляем слова за сегодняшний день

                    # генерируем строку со словами для отправки
                    words_string = database.get_words_string_from_table_words(
                        learned_words,
                        words_number_in_dispatch)

                    msg_dispatch = messages.gen_everyday_dispatch_msg(words_string, words_number_in_dispatch)

                    # обновляем поле passed_the_words, ставим True, т.к. рассылка сейчас придет
                    database.change_passed_the_words_in_date_table(user_id, label_date_table, True)

                    # отправляем юзеру сообщение
                    vk.send_message(user_id, msg_dispatch, None)


# переменная, которая нужна, чтобы отслеживать, морозится поток, или нет.
flag = True


def main():
    while True:
        if flag:
            try:

                current_server_time = work_with_time.get_current_server_handy_time()

                current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'
                current_server_date_sec = work_with_time.get_date_to_sec(current_server_date)

                # серверное время, которое прошло с начала дня в секундах
                current_server_time_per_day_sec = current_server_time.tm_hour * 3600 + current_server_time.tm_min * 60

                # получаем список со всеми датами и упорядочиваем его в порядке возрастания дат
                dates = database.get_dates_from_dates_table()
                dates.sort(key=lambda date: work_with_time.get_date_to_sec(date))

                # кол-во дат в таблице дат, их кол-во должно быть меньше 61
                number_of_dates = len(dates)

                # если в бд нет таблиц дат, то добавляем сегодняшнюю и в dates добавляем дату
                if number_of_dates == 0:
                    database.add_or_del_string_in_dates_table(current_server_date, add_date=True)
                    database.create_date_table_for_new_day(gen_table_name_for_date_table(current_server_date))
                    number_of_dates += 1
                    dates.append(current_server_date)

                # если текущей серверной даты нет в таблице, то нужно ее туда добавить и создать новую таблицу этой даты и заполнить
                # ее, основываясь на данных таблицы последнего дня
                if not (current_server_date in dates):
                    number_of_dates += 1

                    database.add_or_del_string_in_dates_table(current_server_date, add_date=True)

                    last_label_date_table = gen_table_name_for_date_table(dates[-1])
                    data_list_from_last_date = database.get_data_from_date_table(last_label_date_table)

                    # генерируем на основе таблицы прошлого дня записи для таблицы нового дня и кладем их в пустой список
                    data_list_for_new_day = []
                    for string in data_list_from_last_date:
                        user_id = string['user_id']
                        number_of_learned_per_day = string['number_of_learned_per_day']
                        number_of_learned_words_before_this_day = string['number_of_learned_words_before_this_day']

                        # если юзер в прошлый день ничего не выучил, то удаляем из таблицы предыдущего дня (таблицы-дня) запись
                        # об этом пользователе и в новую таблицу добавляем новую особую запись
                        # также нужно добавить в таблицу user_data в поле number_of_day_admission увеличение на один день пропуска
                        if number_of_learned_per_day == 0:
                            temp_dict = {'user_id': user_id, 'number_of_learned_per_day': 0,
                                         'number_of_learned_words_before_this_day': number_of_learned_words_before_this_day,
                                         'number_of_repetitions': 0, 'passed_the_words': False}
                            data_list_for_new_day.append(temp_dict)

                            database.change_number_of_day_admission(user_id, 1)

                            database.del_string_in_date_table(user_id, last_label_date_table)

                        # иначе на новый день делаем новую запись для юзера
                        else:
                            new_number_of_learned_words_before_this_day = number_of_learned_words_before_this_day + number_of_learned_per_day

                            temp_dict = {'user_id': user_id, 'number_of_learned_per_day': 0,
                                         'number_of_learned_words_before_this_day': new_number_of_learned_words_before_this_day,
                                         'number_of_repetitions': 0, 'passed_the_words': False}
                            data_list_for_new_day.append(temp_dict)

                    # создаем таблицу на новый день и добаляем туда записи для всех юзеров
                    database.create_date_table_for_new_day(gen_table_name_for_date_table(current_server_date))
                    database.add_strings_in_date_table(gen_table_name_for_date_table(current_server_date), data_list_for_new_day)

                    # если дат в бд больше 92, то нужно удалить самую раннюю дату
                    if number_of_dates > 92:
                        del_date = dates.pop(0)
                        database.add_or_del_string_in_dates_table(del_date, del_date=True)
                        database.del_table(gen_table_name_for_date_table(del_date))

                # в цикле перебираем даты из упорядоченного в порядке возрастания списка с датами, которые есть в бд
                # для каждой даты получаем данные с записями о пользователях на эту дату
                for date in dates:
                    label_date_table = gen_table_name_for_date_table(date)
                    data_list = database.get_data_from_date_table(label_date_table)

                    # переводим дату в секунды
                    date_sec = work_with_time.get_date_to_sec(date)

                    # разница между текущей серверной датой и датой из списка в днях
                    dif_between_dates = int((current_server_date_sec - date_sec) // 86400)

                    # если разница между датами равна 0 дней, то значит, дата совпадает с серверной датой
                    if dif_between_dates == 0:
                        # перебираем список с табличными данными о пользователях на эту дату
                        for user_data in data_list:
                            user_id = user_data['user_id']
                            number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                            passed_the_words = user_data['passed_the_words']
                            number_of_learned_per_day = user_data['number_of_learned_per_day']


                            # получаем данные о пользователе из основной таблицы user_data
                            main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                            dispatch_time_sec = main_user_data['dispatch_time']
                            words_number_in_dispatch = main_user_data['words_number_in_dispatch']

                            # получаем еще больше данных о пользователе
                            more_user_data = database.get_data_about_user_from_user_data_table(user_id)
                            number_of_day_admission = more_user_data['number_of_day_admission']
                            learned_words = more_user_data['learned_words']
                            correct_learned_words = more_user_data['correct_learned_word_counter']

                            # если этому пользователю слова сегодня еще не отправлены
                            if not passed_the_words:

                                # Если разница между сервеным временем и временем отправки меньше 10 минут, то отправляем
                                if abs(current_server_time_per_day_sec - dispatch_time_sec) <= 600:

                                    # генерируем строку со словами для отправки
                                    words_string = database.get_words_string_from_table_words(learned_words,
                                                                                               words_number_in_dispatch)
                                    msg_dispatch = messages.gen_everyday_dispatch_msg(words_string, words_number_in_dispatch)

                                    # обновляем поле passed_the_words, ставим True, т.к. рассылка сейчас придет
                                    database.change_passed_the_words_in_date_table(user_id, label_date_table, True)

                                    # отправляем юзеру сообщение
                                    # если пользователь заблокировал бота, то сразу удаляем его из бд
                                    try:
                                        vk.send_message(user_id, msg_dispatch, None)
                                    except:
                                        process = multiprocessing.Process(target=database.delete_user_from_bot,
                                                                          args=(user_id,))
                                        process.start()

                                    if number_of_day_admission == 0:
                                        if (correct_learned_words + words_number_in_dispatch) > correct_learned_words > 50:
                                            msg = messages.congratulate_on_learned_words_msg(correct_learned_words)
                                        elif (correct_learned_words + words_number_in_dispatch) > correct_learned_words > 200:
                                            msg = messages.congratulate_on_learned_words_msg(correct_learned_words)
                                        elif (correct_learned_words + words_number_in_dispatch) > correct_learned_words > 500:
                                            msg = messages.congratulate_on_learned_words_msg(correct_learned_words)
                                        elif (correct_learned_words + words_number_in_dispatch) > correct_learned_words > 900:
                                            msg = messages.congratulate_on_learned_words_msg(correct_learned_words)
                                        else:
                                            random_int_for_msg = random.randrange(1, 24)
                                            switch_case_msg = {1: messages.every_day_learn_msg_1,
                                                               2: messages.every_day_learn_msg_2,
                                                               3: messages.every_day_learn_msg_3,
                                                               4: messages.every_day_learn_msg_4,
                                                               5: messages.every_day_learn_msg_5,
                                                               6: messages.every_day_learn_msg_6,
                                                               7: messages.every_day_learn_msg_7,
                                                               8: messages.every_day_learn_msg_8,
                                                               9: messages.every_day_learn_msg_9,
                                                               11: messages.every_day_learn_msg_11,
                                                               12: messages.every_day_learn_msg_12,
                                                               13: messages.every_day_learn_msg_13,
                                                               14: messages.every_day_learn_msg_14,
                                                               15: messages.every_day_learn_msg_15,
                                                               16: messages.every_day_learn_msg_16,
                                                               17: messages.every_day_learn_msg_17,
                                                               18: messages.every_day_learn_msg_18,
                                                               19: messages.every_day_learn_msg_19,
                                                               20: messages.every_day_learn_msg_20,
                                                               21: messages.every_day_learn_msg_21,
                                                               22: messages.every_day_learn_msg_22,
                                                               23: messages.every_day_learn_msg_23
                                                               }
                                            msg = switch_case_msg[random_int_for_msg]()

                                    else:
                                        msg = messages.admission_msg(number_of_day_admission)

                                    # последним сообщением из рассылки повышаем мотивацию юзера к изучению
                                    vk.send_message(user_id, msg, None)
                                    break
                            # если слова отправлены, но пользователь их не выучил, то ему нужно напомнить о них
                            else:
                                if number_of_learned_per_day == 0:
                                    # каждые 4 часа напоминаем о словах
                                    number_of_reminders = database.get_number_of_reminders_from_date_table(gen_table_name_for_date_table(current_server_date), user_id)
                                    if number_of_reminders == 0:
                                        if (current_server_time_per_day_sec - dispatch_time_sec) > 3600:
                                            database.change_number_of_reminders_in_date_table(user_id, 1, gen_table_name_for_date_table(current_server_date))
                                            vk.send_message(user_id, messages.reminder_message, None)
                                    elif number_of_reminders == 1:
                                        if (current_server_time_per_day_sec - dispatch_time_sec) > 14400:
                                            database.change_number_of_reminders_in_date_table(user_id, 2, gen_table_name_for_date_table(current_server_date))
                                            vk.send_message(user_id, messages.reminder_message, None)
                                    elif number_of_reminders == 2:
                                        if (current_server_time_per_day_sec - dispatch_time_sec) > 28800:
                                            database.change_number_of_reminders_in_date_table(user_id, 3, gen_table_name_for_date_table(current_server_date))
                                            vk.send_message(user_id, messages.reminder_message, None)
                                    elif number_of_reminders == 3:
                                        if (current_server_time_per_day_sec - dispatch_time_sec) > 57600:
                                            database.change_number_of_reminders_in_date_table(user_id, 4, gen_table_name_for_date_table(current_server_date))
                                            vk.send_message(user_id, messages.reminder_message, None)
                                    elif number_of_reminders == 4:
                                        if (current_server_time_per_day_sec - dispatch_time_sec) > 72000:
                                            database.change_number_of_reminders_in_date_table(user_id, 5, gen_table_name_for_date_table(current_server_date))
                                            vk.send_message(user_id, messages.reminder_message, None)


                    # если разница между датами равна 1 день, то для юзеров из этой даты пришло время для третьего повторения
                    elif dif_between_dates == 1:
                        # перебираем список с табличными данными о пользователях на эту дату
                        for user_data in data_list:
                            user_id = user_data['user_id']
                            number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                            number_of_repetitions = user_data['number_of_repetitions']

                            # если пользователь еще ни разу не повторял слова
                            if number_of_repetitions == 1:
                                # получаем данные о пользователе из основной таблицы user_data
                                main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                                dispatch_time_sec = main_user_data['dispatch_time']
                                words_number_in_dispatch = main_user_data['words_number_in_dispatch']

                                # Если разница между сервеным временем и временем отправки меньше 10 минут, то отправляем
                                if abs(current_server_time_per_day_sec - dispatch_time_sec) <= 600:
                                    # генерируем строку со словами для отправки
                                    words_string = database.get_words_string_from_table_words(
                                        number_of_learned_words_before_this_day,
                                        words_number_in_dispatch)

                                    msg_dispatch = messages.gen_repeat_words_3_msg(words_string)

                                    # отправляем юзеру сообщение
                                    # если пользователь заблокировал бота, то сразу удаляем его из бд
                                    try:
                                        vk.send_message(user_id, msg_dispatch)
                                    except:
                                        process = multiprocessing.Process(target=database.delete_user_from_bot,
                                                                          args=(user_id,))
                                        process.start()

                                    # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                                    database.change_number_of_repetitions_in_date_table(user_id, gen_table_name_for_date_table(date), 1)

                    # если разница между датами равна 17 дней, то для юзеров из этой даты пришло время для четвертого повторения
                    elif dif_between_dates == 17:
                        # перебираем список с табличными данными о пользователях на эту дату
                        for user_data in data_list:
                            user_id = user_data['user_id']
                            number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                            number_of_repetitions = user_data['number_of_repetitions']

                            # если пользователь еще ни разу не повторял слова
                            if number_of_repetitions == 2:
                                # получаем данные о пользователе из основной таблицы user_data
                                main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                                dispatch_time_sec = main_user_data['dispatch_time']
                                words_number_in_dispatch = main_user_data['words_number_in_dispatch']

                                # Если разница между сервеным временем и временем отправки меньше 10 минут, то отправляем
                                if abs(current_server_time_per_day_sec - dispatch_time_sec) <= 600:
                                    # генерируем строку со словами для отправки
                                    words_string = database.get_words_string_from_table_words(
                                        number_of_learned_words_before_this_day,
                                        words_number_in_dispatch)

                                    msg_dispatch = messages.gen_repeat_words_4_msg(words_string)

                                    # отправляем юзеру сообщение
                                    # если пользователь заблокировал бота, то сразу удаляем его из бд
                                    try:
                                        vk.send_message(user_id, msg_dispatch)
                                    except:
                                        process = multiprocessing.Process(target=database.delete_user_from_bot,
                                                                          args=(user_id,))
                                        process.start()

                                    # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                                    database.change_number_of_repetitions_in_date_table(user_id,
                                                                                        gen_table_name_for_date_table(date), 1)

                    # если разница между датами равна 92 дней, то для юзеров из этой даты пришло время для пятого повторения
                    elif dif_between_dates == 92:
                        # перебираем список с табличными данными о пользователях на эту дату
                        for user_data in data_list:
                            user_id = user_data['user_id']
                            number_of_learned_words_before_this_day = user_data['number_of_learned_words_before_this_day']
                            number_of_repetitions = user_data['number_of_repetitions']

                            # если пользователь еще ни разу не повторял слова
                            if number_of_repetitions == 3:
                                # получаем данные о пользователе из основной таблицы user_data
                                main_user_data = database.get_data_about_user_from_user_data_table(user_id)
                                dispatch_time_sec = main_user_data['dispatch_time']
                                words_number_in_dispatch = main_user_data['words_number_in_dispatch']

                                # Если разница между сервеным временем и временем отправки меньше 10 минут, то отправляем
                                if abs(current_server_time_per_day_sec - dispatch_time_sec) <= 600:
                                    # генерируем строку со словами для отправки
                                    words_string = database.get_words_string_from_table_words(
                                        number_of_learned_words_before_this_day,
                                        words_number_in_dispatch)

                                    msg_dispatch = messages.gen_repeat_words_5_msg(words_string)

                                    # отправляем юзеру сообщение
                                    # если пользователь заблокировал бота, то сразу удаляем его из бд
                                    try:
                                        vk.send_message(user_id, msg_dispatch)
                                    except:
                                        process = multiprocessing.Process(target=database.delete_user_from_bot,
                                                                          args=(user_id,))
                                        process.start()

                                    # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                                    database.change_number_of_repetitions_in_date_table(user_id,
                                                                                        gen_table_name_for_date_table(date), 1)

            except:
                continue


def async_dispatch_30_sec(user_id, msg):
    """
    Функция, которая отправляет сообщение пользователю по прошествии 30 секунд.
    """
    time_1 = time.time()
    while True:
        time_2 = time.time()
        if abs(time_2 - time_1) > 30:
            vk.send_message(user_id, msg)
            break


def async_dispatch_25_min(user_id, msg):
    """
    Функция, которая отправляет сообщение пользователю по прошествии 25 минут.
    """
    time_1 = time.time()
    while True:
        time_2 = time.time()
        if abs(time_2 - time_1) > 1500:
            vk.send_message(user_id, msg)
            break


if __name__ == '__main__':
        main()






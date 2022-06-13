"""

Тут живут обработчики сообщений юзера. Обработчики учитывают состояние юзера, передаваемое в user - экземпляре класса
User.
"""


from work_with_vk_pkg import messages, validators, keyboards, config
import database
import work_with_time
import dispatch
import word_check
from vk_api.bot_longpoll import VkBotEventType
from work_with_vk_pkg import vk
import multiprocessing


def handlers(event, user):
    if event.type == VkBotEventType.MESSAGE_NEW:
        msg = event.object.message['text']
        msg = msg.strip().lower()
    elif event.type == event.type == VkBotEventType.MESSAGE_EVENT:
        msg = event.object.payload['message']
        msg = msg.strip().lower()

    # при базовой настройке, если пользователь отвечает на вопрос о соглашении на ежедневную рассылку
    if user.enters_answer_on_bot_license_agreement:
        if validators.enters_answer_on_bot_license_agreement_validator(msg):
            user.switch_enters_answer_on_bot_license_agreement(False)
            if msg == 'да':
                user.switch_enters_local_time(True)

                # отправляем клавиатуру с временами
                times_list = work_with_time.gen_times_of_all_russian_time_zone()
                time_keyboard = keyboards.create_keyboard_with_current_time(times_list, first_time=True)
                return messages.user_agree_with_bot_license_agreement_msg, time_keyboard.get_keyboard()

            elif msg == 'нет':
                return messages.user_disagree_with_bot_license_agreement_msg, keyboards.start_keyboard.get_keyboard()
        else:
            return messages.invalid_answer_on_bot_license_agreement_msg, None

    # при базовой настройке, если пользователь вводит свое локальное время
    elif user.enters_local_time:
        if validators.enters_local_time_and_dispatch_time_validator(msg):
            user.switch_enters_local_time(False)
            user.switch_enters_dispatch_time(True)

            user.local_time = msg
            user.server_time = work_with_time.get_current_server_time()

            dispatch_times_list = work_with_time.gen_dispatch_time()
            time_keyboard = keyboards.create_keyboard_with_current_time(dispatch_times_list, first_time=True)
            return messages.valid_local_time_msg, time_keyboard.get_keyboard()
        else:
            return messages.invalid_local_time_msg, None

    # при базовой настройке, если пользователь вводит время отправки слов
    elif user.enters_dispatch_time:
        if validators.enters_local_time_and_dispatch_time_validator(msg):
            user.switch_enters_dispatch_time(False)

            # добавляем в бд новую запись с новым юзером
            server_dispatch_time = work_with_time.difference_in_time(user.local_time, msg, user.server_time)
            database.add_new_string_in_table_user_data(user.user_id, server_dispatch_time)

            # добавляем в таблицу-дату новую запись

            # текущая серверная дата
            current_server_time = work_with_time.get_current_server_handy_time()
            current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'

            # формируем запись
            string = [{
                'user_id': user.user_id,
                'number_of_learned_per_day': 0,
                'number_of_learned_words_before_this_day': 0,
                'number_of_repetitions': 0,
                'passed_the_words': False
            }]

            # добавляем запись
            database.add_strings_in_date_table(dispatch.gen_table_name_for_date_table(current_server_date), string)

            # уведомляем админа о новом юзере
            vk.send_message(config.admin_user_id, messages.msg_for_admin_about_new_user(user.user_id))

            return messages.valid_dispatch_time_msg, keyboards.base_user_keyboard.get_keyboard()
        else:
            return messages.invalid_dispatch_time_msg, None

    # если пользователь меняет настройки бота или использует расширенный настройки
    elif user.setup_bot:
        # если пользователь меняет время рассылки, то в алгоритме используется запрос локального времени юзера
        if user.setup_bot_enters_local_time:
            # обработка кнопки отмена
            if msg == '/отмена':
                user.switch_setup_bot_enters_local_time(False)
                return messages.cancel_change_settings_msg, keyboards.setup_bot_keyboard.get_keyboard()

            else:
                if validators.enters_local_time_and_dispatch_time_validator(msg):
                    user.switch_setup_bot_enters_local_time(False)
                    user.switch_setup_bot_enters_dispatch_time(True)

                    user.local_time = msg
                    user.server_time = work_with_time.get_current_server_time()

                    dispatch_times_list = work_with_time.gen_dispatch_time()
                    time_keyboard = keyboards.create_keyboard_with_current_time(dispatch_times_list)
                    return messages.valid_setup_bot_change_local_time_msg, time_keyboard.get_keyboard()
                else:
                    return messages.invalid_setup_bot_change_local_time_msg, None

        # если юзер меняет время рассылки
        elif user.setup_bot_enters_dispatch_time:
            # обработка кнопки отмена
            if msg == '/отмена':
                user.switch_setup_bot_enters_dispatch_time(False)
                return messages.cancel_change_settings_msg, keyboards.setup_bot_keyboard.get_keyboard()
            else:
                if validators.enters_local_time_and_dispatch_time_validator(msg):
                    user.switch_setup_bot_enters_dispatch_time(False)
                    user.switch_setup_bot(False)

                    server_dispatch_time = work_with_time.difference_in_time(user.local_time, msg, user.server_time)
                    database.change_dispatch_time(user.user_id, server_dispatch_time)
                    return messages.valid_setup_bot_change_dispatch_time_msg, keyboards.base_user_keyboard.get_keyboard()
                else:
                    return messages.invalid_setup_bot_change_dispatch_time_msg, None

        # если юзер меняет число слов в рассылке
        elif user.setup_bot_change_number_of_word_in_dispatch:
            # обработка кнопки отмена
            if msg == '/отмена':
                user.switch_setup_bot_change_number_of_word_in_dispatch(False)
                return messages.cancel_change_settings_msg, keyboards.setup_bot_keyboard.get_keyboard()
            else:
                if validators.change_number_of_word_in_dispatch_validator(msg):
                    user.switch_setup_bot_change_number_of_word_in_dispatch(False)
                    user.switch_setup_bot(False)

                    database.change_number_of_word_in_dispatch(user.user_id, int(msg))
                    return messages.valid_change_number_of_word_in_dispatch_msg, keyboards.base_user_keyboard.get_keyboard()
                else:
                    return messages.invalid_change_number_of_word_in_dispatch_msg, None

        # если юзер отключает рассылку
        elif user.setup_bot_disable_dispatch:
            if validators.disable_dispatch_validator(msg):
                if msg == 'да':
                    # останавливаем рассылку, чтобы при удалении юзера из бд, не возникло ошибок
                    database.flag = False
                    # в отдельном процессе запускаем удаление юзера из бота, чтобы не тормозить работу всего бота
                    process = multiprocessing.Process(target=database.delete_user_from_bot, args=(user.user_id,))
                    process.start()
                    # database.delete_user_from_bot(user.user_id)
                    database.flag = True

                    user.switch_setup_bot(False)
                    user.switch_setup_bot_disable_dispatch(False)

                    return messages.allow_disable_dispatch_msg, keyboards.start_keyboard.get_keyboard()

                elif msg == 'нет':
                    user.switch_setup_bot_disable_dispatch(False)
                    return messages.cancel_disable_dispatch_msg, keyboards.setup_bot_keyboard.get_keyboard()
            else:
                return messages.invalid_answer_disable_dispatch_msg, None

        # если юзер меняет уровень сложности слов
        elif user.setup_bot_change_lvl_of_words:
            if msg == '/отмена':
                user.switch_setup_bot_change_lvl_of_words(False)
                del user.words_mode
                return messages.cancel_change_lvl_of_words_msg, keyboards.setup_bot_keyboard.get_keyboard()
            else:
                if user.words_mode == 'base' and msg == '/продвинутый уровень':
                    database.change_number_learned_words(user.user_id, 1000)

                    current_server_time = work_with_time.get_current_server_handy_time()
                    current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'
                    table_name = dispatch.gen_table_name_for_date_table(current_server_date)

                    database.change_number_of_learned_words_before_this_day_from_date_table(1000, user.user_id,
                                                                                            table_name)
                    database.change_number_of_learned_per_day_in_date_table(user.user_id, table_name, 0)

                    user.switch_setup_bot_change_lvl_of_words(False)
                    user.switch_setup_bot(False)

                    del user.words_mode
                    return messages.setup_bot_exit_msg, keyboards.base_user_keyboard.get_keyboard()
                elif user.words_mode == 'pro' and msg == '/базовый уровень':
                    database.change_number_learned_words(user.user_id, 0)

                    current_server_time = work_with_time.get_current_server_handy_time()
                    current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'
                    table_name = dispatch.gen_table_name_for_date_table(current_server_date)

                    database.change_number_of_learned_words_before_this_day_from_date_table(0, user.user_id,
                                                                                            table_name)
                    database.change_number_of_learned_per_day_in_date_table(user.user_id, table_name, 0)

                    user.switch_setup_bot_change_lvl_of_words(False)
                    user.switch_setup_bot(False)

                    del user.words_mode
                    return messages.allow_change_lvl_of_words_msg, keyboards.base_user_keyboard.get_keyboard()
                else:
                    return messages.invalid_change_lvl_of_words_msg, None


        # иначе, бот ожидает от юзера одну из команд настроек
        else:
            if msg == '/время рассылки':
                user.switch_setup_bot_enters_local_time(True)

                # отправляем клавиатуру с временами
                times_list = work_with_time.gen_times_of_all_russian_time_zone()
                time_keyboard = keyboards.create_keyboard_with_current_time(times_list)
                return messages.setup_bot_change_local_time_msg, time_keyboard.get_keyboard()

            elif msg == '/количество слов':
                user.switch_setup_bot_change_number_of_word_in_dispatch(True)
                return messages.change_number_of_word_in_dispatch_msg, keyboards.cancel_keyboard.get_keyboard()

            elif msg == '/отключить рассылку':
                user.switch_setup_bot_disable_dispatch(True)
                return messages.disable_dispatch_msg, keyboards.setup_bot_disable_dispatch_keyboard.get_keyboard()

            elif msg == '/сложность слов':
                user.switch_setup_bot_change_lvl_of_words(True)
                learned_words = database.get_data_about_user_from_user_data_table(user.user_id)['learned_words']

                if learned_words >= 1000:
                    mode = 'pro'
                else:
                    mode = 'base'

                msg = messages.change_lvl_of_words_msg(mode)
                keyboard = keyboards.setup_bot_change_lvl_of_words_keyboard(mode)

                user.words_mode = mode

                return msg, keyboard.get_keyboard()

            elif msg == '/выйти':
                user.switch_setup_bot(False)
                user.switch_setup_bot_change_number_of_word_in_dispatch(False)
                user.switch_setup_bot_enters_dispatch_time(False)
                user.switch_setup_bot_enters_local_time(False)

                return messages.setup_bot_exit_msg, keyboards.base_user_keyboard.get_keyboard()

            else:
                return messages.invalid_setup_bot_info_msg, None

    # если идет проверка слов пользователя
    elif user.words_check:
        if msg == '/выйти':
            # меняем все состояния пользователя
            user.switch_words_check(False)
            user.switch_words_check_1_lvl(False)
            user.switch_words_check_2_lvl(False)
            user.switch_words_check_3_lvl(False)
            return messages.words_check_exit_msg, keyboards.base_user_keyboard.get_keyboard()
        else:
            if user.words_check_1_lvl:
                # перебираем слова, если первое попавшееся слово не проверено, то на это слово отвечает сейчас юзер
                for count, word in enumerate(user.words_list):
                    if not word['checked']:
                        if msg == '/не знаю':
                            # отмечаем слово проверенным, т.к. отправляем ответ на него
                            word['checked'] = True

                            # отправляем перевод текущего слова и спрашиваем следующее, если текущее-не последнее, иначе
                            # спрашиваем текущее
                            if count != len(user.words_list) - 1:
                                next_word = user.words_list[count + 1]
                                next_keyboard = keyboards.create_keyboard_for_words_check_1_lvl(user.words_list, next_word)
                                return messages.gen_msg_for_words_check_1_lvl_dont_know(word, next_word), next_keyboard.get_keyboard()
                            else:
                                user.switch_words_check_1_lvl(False)
                                user.switch_words_check_3_lvl(True)

                                # добавляем к каждому слову в списке со словами слово с пропусками и упорядоченные попущенные буквы
                                for el in user.words_list:
                                    el['word_with_blanks'], el['missing_letters'] = word_check.make_the_prompt_in_word(
                                        el['eng_word'])
                                    el['checked'] = False

                                # отправляем сообщение и клаву с первым словом для проверки третьего уровня
                                last_msg_words_check_1_lvl = messages.gen_last_msg_for_words_check_2_lvl(
                                    user.words_list[0])
                                last_keyboard_words_check_2_lvl = keyboards.create_keyboard_for_words_check_3_lvl()

                                # последнее сообщение, которое бот отправил юзеру
                                user.last_msg = last_msg_words_check_1_lvl

                                return last_msg_words_check_1_lvl, last_keyboard_words_check_2_lvl.get_keyboard()

                        else:
                            # если правильно отгадал слово, изменяем статус проверки слова и отправляем новое слово с клавой
                            if msg == word['eng_word']:
                                word['checked'] = True

                                # если правильно отгаданное юзером слово - не последнее, то отправляем следущее, иначе
                                # переводим его на следующий уровень проверки
                                if count != len(user.words_list)-1:
                                    next_word = user.words_list[count+1]
                                    next_keyboard = keyboards.create_keyboard_for_words_check_1_lvl(user.words_list, next_word)
                                    return messages.gen_msg_for_words_check_1_lvl_correct(word, next_word), next_keyboard.get_keyboard()

                                else:
                                    user.switch_words_check_1_lvl(False)
                                    user.switch_words_check_3_lvl(True)

                                    # добавляем к каждому слову в списке со словами слово с пропусками и упорядоченные попущенные буквы
                                    for el in user.words_list:
                                        el['word_with_blanks'], el['missing_letters'] = word_check.make_the_prompt_in_word(el['eng_word'])
                                        el['checked'] = False

                                    # отправляем сообщение и клаву с первым словом для проверки третьего уровня
                                    last_msg_words_check_1_lvl = messages.gen_last_msg_for_words_check_2_lvl(
                                        user.words_list[0])
                                    last_keyboard_words_check_2_lvl = keyboards.create_keyboard_for_words_check_3_lvl()

                                    # последнее сообщение, которое бот отправил юзеру
                                    user.last_msg = last_msg_words_check_1_lvl

                                    return last_msg_words_check_1_lvl, last_keyboard_words_check_2_lvl.get_keyboard()

                            # если неправильно отгадал слово
                            else:
                                new_msg = messages.gen_msg_for_words_check_1_lvl_wrong(word)
                                return new_msg, None

            elif user.words_check_2_lvl:

                for count, word in enumerate(user.words_list):
                    if not word['checked']:

                        if msg == '/не знаю':
                            # отмечаем слово проверенным, т.к. отправляем ответ на него
                            word['checked'] = True

                            # изменяем сообщение с правильным переводом
                            edit_msg = messages.add_all_letters_words_check_2_lvl(user.last_msg, word)
                            # добавляем транскрипцию
                            edit_msg = messages.add_transcription_words_check_2_lvl(edit_msg, word)
                            # удаляем первую строку из сообщения и добавляем заголовок запомните  к сообщению
                            edit_msg = messages.del_first_string(edit_msg)
                            edit_msg = messages.add_title_remember_words_check_2_lvl(edit_msg)

                            vk.edit_message(user.user_id, edit_msg, vk.id_of_last_bot_msg(user.user_id))

                            # отправляем перевод текущего слова и спрашиваем следующее, если текущее-не последнее, иначе
                            # спрашиваем текущее
                            if count != len(user.words_list) - 1:

                                # отправляем сообщение c новым словом для проверки
                                next_msg = messages.gen_next_msg_for_words_check_2_lvl(user.words_list[count + 1])
                                next_keyboard = keyboards.create_keyboard_for_words_check_2_lvl(
                                    user.words_list[count + 1]['missing_letters'])

                                # последнее сообщение, которое бот отправил юзеру
                                user.last_msg = next_msg

                                # последняя клавиатура, который бот отправил юзеру
                                user.last_keyboard = next_keyboard

                                return next_msg, next_keyboard.get_keyboard()

                            # если слово - последнее
                            else:
                                user.switch_words_check_2_lvl(False)
                                user.switch_words_check_3_lvl(True)

                                # удаляем данные, которые использовались на втором уровне проверки слов
                                for el in user.words_list:
                                    del el['word_with_blanks'], el['missing_letters']
                                    el['checked'] = False

                                # отправляем сообщение и клаву с первым словом для проверки третьего уровня
                                last_msg_words_check_2_lvl = messages.gen_last_msg_for_words_check_2_lvl(
                                    user.words_list[0])
                                last_keyboard_words_check_2_lvl = keyboards.create_keyboard_for_words_check_3_lvl()

                                # последнее сообщение, которое бот отправил юзеру
                                user.last_msg = last_msg_words_check_2_lvl

                                return last_msg_words_check_2_lvl, last_keyboard_words_check_2_lvl.get_keyboard()

                        else:

                            # если правильно отгадал букву, то изменяем сообщение и отправляем новую клавиатуру
                            if msg == word['missing_letters'][0]:

                                # удаляем правильно отгаданную букву из списка оставшихся для отгадок букв
                                last_letter = word['missing_letters'].pop(0)

                                # удаляем первую строку в сообщении прошлом
                                edit_msg = messages.del_first_string(user.last_msg)
                                # добавляем букву на место пропуска в сообщение
                                edit_msg = messages.add_letter_words_check_2_lvl(last_letter, edit_msg)

                                # если отгаданная буква еще раз повторяется в слове, то не выделяем ее цветом
                                if not (last_letter in word['missing_letters']):
                                    # изменяем текущую клавиатуру, изменяем цвет кнопки с правильно отгаданной буквой
                                    edit_keyboard = keyboards.edit_right_button_words_check_2_lvl(last_letter, user.last_keyboard)
                                else:
                                    edit_keyboard = user.last_keyboard

                                # заменяем все красные кнопки на нейтральные(если до этого неправильно отгадывал буквы)
                                edit_keyboard = keyboards.remove_red_buttons_words_check_2_lvl(edit_keyboard)

                                # если юзеру нужно еще отгадать буквы, то отгадывает
                                if word['missing_letters']:

                                    # добавляем заголовок правильно
                                    edit_msg = messages.add_title_right_words_check_2_lvl(edit_msg)

                                    user.last_msg = edit_msg
                                    user.last_keyboard = edit_keyboard

                                    vk.edit_message(user.user_id, edit_msg, vk.id_of_last_bot_msg(user.user_id), edit_keyboard.get_keyboard())
                                    return None, None

                                # иначе отмечаем это слово проверенным и переходим к следующему
                                else:
                                    word['checked'] = True

                                    # добавляем заголовок окончательно правильно
                                    edit_msg = messages.add_title_all_right_words_check_2_lvl(edit_msg)

                                    # добавляем транскрипцию
                                    edit_msg = messages.add_transcription_words_check_2_lvl(edit_msg, word)

                                    vk.edit_message(user.user_id, edit_msg, vk.id_of_last_bot_msg(user.user_id), edit_keyboard.get_keyboard())

                                    # если текущее слово было не последним, то отправляем следующее
                                    if count != len(user.words_list)-1:
                                        # отправляем сообщение c новым словом для проверки
                                        next_msg = messages.gen_next_msg_for_words_check_2_lvl(user.words_list[count+1])
                                        next_keyboard = keyboards.create_keyboard_for_words_check_2_lvl(user.words_list[count+1]['missing_letters'])

                                        # последнее сообщение, которое бот отправил юзеру
                                        user.last_msg = next_msg

                                        # последняя клавиатура, который бот отправил юзеру
                                        user.last_keyboard = next_keyboard

                                        return next_msg, next_keyboard.get_keyboard()

                                    # если слов для проверки больше не осталось, то переходим к 3 уровню проверки
                                    else:

                                        user.switch_words_check_2_lvl(False)
                                        user.switch_words_check_3_lvl(True)

                                        # удаляем данные, которые использовались на втором уровне проверки слов
                                        for el in user.words_list:
                                            del el['word_with_blanks'], el['missing_letters']
                                            el['checked'] = False

                                        # отправляем сообщение и клаву с первым словом для проверки третьего уровня
                                        last_msg_words_check_2_lvl = messages.gen_last_msg_for_words_check_2_lvl(
                                            user.words_list[0])
                                        last_keyboard_words_check_2_lvl = keyboards.create_keyboard_for_words_check_3_lvl()

                                        # последнее сообщение, которое бот отправил юзеру
                                        user.last_msg = last_msg_words_check_2_lvl

                                        return last_msg_words_check_2_lvl, last_keyboard_words_check_2_lvl.get_keyboard()

                            # если неправильно отгадал букву
                            else:
                                # удаляем первую строку в сообщении прошлом
                                edit_msg = messages.del_first_string(user.last_msg)
                                # изменяем текущее сообщение
                                edit_msg = messages.add_title_wrong_words_check_2_lvl(edit_msg)
                                # изменяем цвет неправильно отгаданной буквы на кнопке
                                edit_keyboard = keyboards.edit_wrong_button_words_check_2_lvl(msg, user.last_keyboard)

                                # последнее сообщение, которое бот отправил юзеру
                                user.last_msg = edit_msg
                                # последняя клавиатура, которую бот отправил юзеру
                                user.last_keyboard = edit_keyboard

                                vk.edit_message(user.user_id, edit_msg, vk.id_of_last_bot_msg(user.user_id), edit_keyboard.get_keyboard())

                                return None, None

                return None, None

            elif user.words_check_3_lvl:

                if msg == '/выйти':
                    # меняем все состояния пользователя
                    user.switch_words_check(False)
                    user.switch_words_check_1_lvl(False)
                    user.switch_words_check_2_lvl(False)
                    user.switch_words_check_3_lvl(False)
                    return messages.words_check_exit_msg, keyboards.base_user_keyboard.get_keyboard()
                else:
                    for count, word in enumerate(user.words_list):
                        if not word['checked']:

                            if msg == '/не знаю':
                                # отмечаем слово проверенным, т.к. отправляем ответ на него
                                word['checked'] = True

                                # изменяем сообщение
                                edit_msg = messages.add_transcription_and_translate_words_check_3_lvl(user.last_msg, word)
                                edit_msg = messages.del_first_string(edit_msg)
                                edit_msg = messages.add_title_remember_words_check_2_lvl(edit_msg)
                                vk.edit_message(user.user_id, edit_msg, vk.id_of_last_bot_msg(user.user_id))

                                # отправляем перевод текущего слова и спрашиваем следующее, если текущее-не последнее, иначе
                                # спрашиваем текущее
                                if count != len(user.words_list) - 1:
                                    next_word = user.words_list[count + 1]

                                    next_msg = messages.gen_next_msg_for_words_check_3_lvl(next_word)
                                    # последнее сообщение, которое бот отправил юзеру
                                    user.last_msg = next_msg

                                    return next_msg, None
                                else:
                                    user.switch_words_check_3_lvl(False)
                                    user.switch_words_check(False)

                                    # отправляем сообщение и клаву с первым словом для проверки третьего уровня
                                    last_msg_words_check_3_lvl = messages.gen_last_msg_for_words_check_3_lvl()
                                    last_keyboard_words_check_3_lvl = keyboards.base_user_keyboard

                                    # меняем в базах данных значения
                                    database.change_number_of_day_admission(user.user_id, 0)
                                    database.change_number_of_learned_per_day_in_date_table(user.user_id,
                                                                                            user.table_name,
                                                                                            user.words_number_in_dispatch)
                                    new_number_of_learned_words = user.words_number_in_dispatch + user.number_of_learned_words_before_this_day
                                    database.change_number_learned_words(user.user_id, new_number_of_learned_words)

                                    new_correct_learned_word_counter = user.words_number_in_dispatch + user.correct_learned_word_counter_before_this_day
                                    database.change_number_correct_learned_word_counter(user.user_id,
                                                                                        new_correct_learned_word_counter)

                                    # создаем отдельный процесс, в котором асинхронно отправляем юзеру сообщение
                                    # о первом повторении, эти повторения не учитываются в бд, т.к. отправляются рано
                                    words_string = database.get_words_string_from_table_words(
                                        user.number_of_learned_words_before_this_day,
                                        user.words_number_in_dispatch)
                                    process = multiprocessing.Process(target=dispatch.async_dispatch_30_sec,
                                                                      args=(user.user_id,
                                                                            messages.gen_repeat_words_1_msg(
                                                                                words_string)))
                                    process.start()

                                    # создаем еще один процесс для второго повторения через 25 минут
                                    process = multiprocessing.Process(target=dispatch.async_dispatch_25_min,
                                                                      args=(user.user_id,
                                                                            messages.gen_repeat_words_2_msg(
                                                                                words_string)))
                                    process.start()

                                    # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                                    current_server_time = work_with_time.get_current_server_handy_time()
                                    current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'
                                    process = multiprocessing.Process(
                                        target=database.change_number_of_repetitions_in_date_table,
                                        args=(user.user_id,
                                              dispatch.gen_table_name_for_date_table(
                                                  current_server_date), 1))
                                    process.start()

                                    # удаляем данные, которые использовались на третьем уровне проверки слов
                                    del user.words_list
                                    del user.table_name
                                    del user.words_number_in_dispatch
                                    del user.number_of_learned_words_before_this_day

                                    return last_msg_words_check_3_lvl, last_keyboard_words_check_3_lvl.get_keyboard()

                            else:
                                # если правильно отгадал слово
                                if msg == word['eng_word']:

                                    word['checked'] = True

                                    # изменяем сообщение с правильно отгаднанным словом
                                    edit_msg = user.last_msg
                                    edit_msg = messages.del_first_string(edit_msg)
                                    edit_msg = messages.add_title_right_words_check_2_lvl(edit_msg)
                                    edit_msg = messages.add_transcription_and_translate_words_check_3_lvl(edit_msg, word)
                                    vk.edit_message(user.user_id, edit_msg,  vk.id_of_last_bot_msg(user.user_id))

                                    # если текущее слово было не последним, то отправляем следующее
                                    if count != len(user.words_list) - 1:
                                        # отправляем сообщение c новым словом для проверки
                                        next_msg = messages.gen_next_msg_for_words_check_3_lvl(user.words_list[count + 1])

                                        # последнее сообщение, которое бот отправил юзеру
                                        user.last_msg = next_msg

                                        return next_msg, keyboards.create_keyboard_for_words_check_3_lvl().get_keyboard()

                                    else:
                                        user.switch_words_check_3_lvl(False)
                                        user.switch_words_check(False)

                                        # отправляем сообщение и клаву с первым словом для проверки третьего уровня
                                        last_msg_words_check_3_lvl = messages.gen_last_msg_for_words_check_3_lvl()
                                        last_keyboard_words_check_3_lvl = keyboards.base_user_keyboard

                                        # меняем в базах данных значения
                                        database.change_number_of_day_admission(user.user_id, 0)
                                        database.change_number_of_learned_per_day_in_date_table(user.user_id,
                                                                                                user.table_name,
                                                                                                user.words_number_in_dispatch)
                                        new_number_of_learned_words = user.words_number_in_dispatch + user.number_of_learned_words_before_this_day
                                        database.change_number_learned_words(user.user_id, new_number_of_learned_words)

                                        new_correct_learned_word_counter = user.words_number_in_dispatch + user.correct_learned_word_counter_before_this_day
                                        database.change_number_correct_learned_word_counter(user.user_id, new_correct_learned_word_counter)


                                        # создаем отдельный процесс, в котором асинхронно отправляем юзеру сообщение
                                        # о первом повторении эти повторения не учитываются в бд, т.к. отправляются рано
                                        words_string = database.get_words_string_from_table_words(
                                        user.number_of_learned_words_before_this_day,
                                        user.words_number_in_dispatch)
                                        process = multiprocessing.Process(target=dispatch.async_dispatch_30_sec,
                                                                          args=(user.user_id,messages.gen_repeat_words_1_msg(words_string)))
                                        process.start()

                                        # создаем еще один процесс для второго повторения через 25 минут
                                        process = multiprocessing.Process(target=dispatch.async_dispatch_25_min,
                                                                          args=(user.user_id,
                                                                                messages.gen_repeat_words_2_msg(
                                                                                    words_string)))
                                        process.start()

                                        # в таблице-дате изменяем для этого юзера поле number_of_repetitions, увеличивая его на 1
                                        current_server_time = work_with_time.get_current_server_handy_time()
                                        current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'
                                        process = multiprocessing.Process(target=database.change_number_of_repetitions_in_date_table,
                                                                          args=(user.user_id,
                                                                                dispatch.gen_table_name_for_date_table(
                                                                                    current_server_date), 1))
                                        process.start()


                                        # удаляем данные, которые использовались на третьем уровне проверки слов
                                        del user.words_list
                                        del user.table_name
                                        del user.words_number_in_dispatch
                                        del user.number_of_learned_words_before_this_day


                                        return last_msg_words_check_3_lvl, last_keyboard_words_check_3_lvl.get_keyboard()

                                # если неправильно отгадал слово
                                else:
                                    # удаляем первую строку
                                    edit_msg = messages.del_first_string(user.last_msg)
                                    # изменяем текущее сообщение
                                    edit_msg = messages.add_title_wrong_words_check_2_lvl(edit_msg)

                                    vk.edit_message(user.user_id, edit_msg, vk.id_of_last_bot_msg(user.user_id))

                                    # последнее сообщение, которое бот отправил юзеру
                                    user.last_msg = edit_msg

                                    return None, None

    # если пользователь не находится ни в каком состоянии
    else:
        if msg == 'начать':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                return messages.dont_understand_msg, None
            else:
                return messages.start_msg, keyboards.start_keyboard.get_keyboard()

        elif msg == '/инфо':
            return messages.bot_capabilities_msg, None

        elif msg == '/начать использование' or msg == '/начать':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                return messages.dont_understand_msg, None
            else:
                user.switch_enters_answer_on_bot_license_agreement(True)
                return messages.bot_license_agreement_msg, keyboards.bot_license_agreement_keyboard.get_keyboard()

        elif msg == '/настройки':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                user.setup_bot = True
                return messages.setup_bot_info_msg, keyboards.setup_bot_keyboard.get_keyboard()
            else:
                return messages.start_msg, None

        elif msg == '/кнопки':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                return messages.base_keyboard_msg, keyboards.base_user_keyboard.get_keyboard()
            else:
                return messages.start_msg, None

        elif msg == '/команды':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                return messages.base_command_msg, None
            else:
                return messages.start_msg, None

        elif msg == '/статистика':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):

                num_word = database.get_data_about_user_from_user_data_table(user.user_id)['correct_learned_word_counter']

                return messages.msg_for_statistic(num_word), None
            else:
                return messages.start_msg, None

        elif msg == '/получить слова':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                # создаем отдельный процесс, в котором будеет выполнятся функция, чтобы не тормозить работу бота
                process = multiprocessing.Process(target=dispatch.early_dispatch, args=(user.user_id,))
                process.start()
                # dispatch.early_dispatch(user.user_id)
                return None, None
            else:
                return messages.start_msg, None

        elif msg == '/сдать слова':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                # проверяем, отправлены ли уже юзеру его слова
                current_server_time = work_with_time.get_current_server_handy_time()
                current_server_date = f'{current_server_time.tm_year}-{current_server_time.tm_mon}-{current_server_time.tm_mday}'
                table_name = dispatch.gen_table_name_for_date_table(current_server_date)

                userdata = database.get_data_about_user_from_user_data_table(user.user_id)
                words_number_in_dispatch = userdata['words_number_in_dispatch']
                correct_learned_word_counter_before_this_day = userdata['correct_learned_word_counter']

                data_list = database.get_data_from_date_table(table_name)
                for string in data_list:
                    if string['user_id'] == user.user_id:
                        if string['passed_the_words']:
                            # если юзеру были отправлены слова и юзер их еще не все сдал, то начинаем проверку.
                            if string['number_of_learned_per_day'] != words_number_in_dispatch:
                                # меняем состояния пользователя
                                user.switch_words_check(True)
                                user.switch_words_check_1_lvl(True)

                                # создаем свойство у юзера, в котором хранятся слова, которые он должен сдать
                                number_of_learned_words_before_this_day = string['number_of_learned_words_before_this_day']

                                words_list = database.get_words_list_from_table_words(
                                    number_of_learned_words_before_this_day,
                                    words_number_in_dispatch)
                                user.words_list = words_list

                                first_word = words_list[0]
                                first_msg = messages.gen_first_msg_for_words_check_1_lvl(first_word)
                                first_keyboard = keyboards.create_keyboard_for_words_check_1_lvl(words_list, first_word)

                                # к объекту пользователя добавляем данные для дальнейших ихменений в бд
                                user.words_number_in_dispatch = words_number_in_dispatch
                                user.table_name = table_name
                                user.number_of_learned_words_before_this_day = number_of_learned_words_before_this_day
                                user.correct_learned_word_counter_before_this_day = correct_learned_word_counter_before_this_day

                                return first_msg, first_keyboard.get_keyboard()
                                """
                                # меняем в базах данных значения
                                database.change_number_of_day_admission(user.user_id, 0)
                                database.change_number_of_learned_per_day_in_date_table(user.user_id, table_name, words_number_in_dispatch)
                                new_number_of_learned_words = words_number_in_dispatch + string['number_of_learned_words_before_this_day']
                                database.change_number_learned_words(user.user_id, new_number_of_learned_words)
                                return messages.you_learned_the_words_msg, None
                                """

                            else:
                                return messages.already_learned_words_msg, None

                        else:
                            return messages.invalid_pass_the_word_msg, None
            else:
                return messages.start_msg, None

        # для тестов
        elif msg == '/тест':
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                print(msg)
                return messages.dont_understand_msg, None
            else:
                return messages.start_msg, None

        # скрытая команда для получения общей статистики
        elif msg == '/get_stat':
            return database.get_data_about_users(), None

        else:
            # если юзер есть в бд, значит он уже прошел "начать" и базовую настройку
            if database.check_user_in_user_data_table(user.user_id):
                return messages.dont_understand_msg, None
            else:
                return messages.start_msg, None




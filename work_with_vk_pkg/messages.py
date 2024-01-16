hello_msg = 'привет'

start_msg = 'Доступные команды:\n/инфо - узнать о возможностях бота.\n/начать использование - активировать бота.'

# dont_understand_msg = 'Прости, но я тебя не понимаю.'

bot_capabilities_msg = 'Это бот для изучения анлийских слов. \n\nБот каждый день будет тебе отправлять слова, а ты будешь их учить и сдавать.\n(Подробнее: https://vk.com/wall-200876594_12)'


base_keyboard_msg = 'Базовые кнопки бота.'


subscription_msg = 'Пожалуйста, подпишитесь на группу. Этим вы поддержите разработчика, а также больше не будете видеть эту просьбу.'

# сообщения соглашения с рассылкой от бота
bot_license_agreement_msg = 'Вы согласны получать от бота ежедневные рассылки с новыми английскими словами?(Да/Нет)'
user_agree_with_bot_license_agreement_msg = 'Отлично! Чтобы начать пользоваться ботом, нужно ответить на два вопроса для его настройки.\n\n Какое ваше текущее время?\n(Если нет кнопки с вашим временем, то введите его вручную)'
user_disagree_with_bot_license_agreement_msg = 'Очень жаль, что вы отказались. Вы всегда можете изменить свое решение.'
invalid_answer_on_bot_license_agreement_msg = f'Вы ввели некоректные данные!\n{bot_license_agreement_msg}'


# сообщения для укзания локального времени пользователя
request_for_enter_local_time_msg = 'local time'
valid_local_time_msg = 'Выберите время, в которое вы каждый день будете заниматься английским.\n(Если нет кнопки с вашим временем, то введите его вручную).'
invalid_local_time_msg = 'Вы ввели некоректные данные!\nКакое ваше текущее время? (например 14:25)'


# сообщения для укзания времени рассылки пользователям сообщений
request_for_enter_dispatch_time_msg = 'dispatch time'
valid_dispatch_time_msg = 'Настройка завершена.\nТеперь каждый день в указанное время вы будете учить английский с ботом!.\n Чтобы более детально настроить бота, нажмите /настройки'
invalid_dispatch_time_msg = 'Вы ввели некоректные данные!\nВ какое время вам удобно получать рассылку от бота? (например 14:25)'


# сообщение для базовых команд базовой клавиатуры
base_command_msg = 'Доступные команды:\n/настройки - изменить настройки бота.\n/команды - информация о командах.\n/функционал- узнать о возможностях бота.\n/кнопки - получить базовые кнопки бота.\n/статистика - ваша статистика.\n/получить слова - получить слова, не дожидаясь рассылки.\n/сдать слова - сдать слова.'
dont_understand_msg = base_command_msg

# сообщения для настройки бота
setup_bot_info_msg = '/время рассылки - чтобы сменить время рассылки.\n/количество слов - чтобы сменить количество слов, которое бот отправляет каждый день.\n/сложность слов - чтобы сменить уровень сложности слов.\n/отключить рассылку - чтобы деактивировать бота.\n/выйти - выйти в главное меню.'
invalid_setup_bot_info_msg = f'Команды в меню настроек:\n{setup_bot_info_msg}'

change_number_of_word_in_dispatch_msg = 'Введите число - количество слов, которое вы будете получать в ежедневной рассылке (от 5 до 20). По умолчанию - 5, больше 10 не рекомендуется.'
invalid_change_number_of_word_in_dispatch_msg = f'Вы ввели некоректные данные!\n{change_number_of_word_in_dispatch_msg}'
valid_change_number_of_word_in_dispatch_msg = 'Количество слов рассылки изменено.'

setup_bot_change_dispatch_time_msg = 'В какое время вам удобно получать рассылку от бота? (например 14:25)'
invalid_setup_bot_change_dispatch_time_msg = f'Вы ввели некоректные данные!\n{setup_bot_change_dispatch_time_msg}'
valid_setup_bot_change_dispatch_time_msg = 'Время рассылки успешно изменено.'

setup_bot_change_local_time_msg = 'Какое ваше текущее время? (например 14:25)'
valid_setup_bot_change_local_time_msg = setup_bot_change_dispatch_time_msg
invalid_setup_bot_change_local_time_msg = f'Вы ввели некоректные данные!\n{setup_bot_change_local_time_msg}'
cancel_change_settings_msg = 'Изменения отменены.'

disable_dispatch_msg = 'Отключив рассылку, вы потеряете абсолютно все свои данные, и бот будет возвращен в первоначальное состояние.\nОтключить рассылку? (Да/Нет)'
cancel_disable_dispatch_msg = 'Отключение рассылки отменено.'
allow_disable_dispatch_msg = 'Рассылка отключена, бот возвращен в первоначальное состояние.'
invalid_answer_disable_dispatch_msg = f'Вы ввели некоректные данные!\n{disable_dispatch_msg}'


def change_lvl_of_words_msg(mode):
    """
    Функция для отправки сообщения при смене уровня сложности слов.
    В зависимости от текущего уровня сложности (mode), функция вернет сообщение.
    """
    if mode == 'pro':
        msg = 'Вы находитесь на продвинутом уровне сложности слов. Чтобы перейти в базовый режим и начать учить простые слова из списка 1000 основных слов, нажмите /базовый уровень.\nВажно! При переходе на другой уровень сложности, вы не сможете вернуться к тому месту, на котором вы сейчас находитесь и учите слова.'
    elif mode == 'base':
        msg = 'Вы находитесь на базовом уровне сложности слов. Чтобы перейти в продвинутый режим и начать учить более сложные слова из списка 7000 слов, нажмите /продвинутый уровень.\nВажно! При переходе на другой уровень сложности, вы не сможете вернуться к тому месту, на котором вы сейчас находитесь и учите слова.'
    return msg

cancel_change_lvl_of_words_msg = 'Смена уровня сложности обучения отменена.'
invalid_change_lvl_of_words_msg = 'Вы ввели некоректные данные!'
allow_change_lvl_of_words_msg = 'Уровень сложности успешно изменен!'

setup_bot_exit_msg = 'Все ваши изменения успешно сохранены.'

wait_a_little_msg = 'Подождите, это может занять некоторое время.'



# сообщения для проверки слов. первый уровень
def gen_msg_for_words_check_1_lvl_correct(current_word, next_word):
    """
    Функция генерирует и возвращает строку для первого уровня проверки слов.
    """
    msg = f'Правильно! {current_word["eng_word"]} [{current_word["transcription"]}] - {current_word["rus_word"]}\nСледующее слово:\n{next_word["rus_word"]}'
    return msg


def gen_msg_for_words_check_1_lvl_wrong(word):
    """
    Функция генерирует и возвращает строку для первого уровня проверки слов.
    :param word:
    """
    msg = f'Неправильно! Переведите это слово:\n{word["rus_word"]}'
    return msg


def gen_msg_for_words_check_1_lvl_dont_know(current_word, next_word):
    msg = f'Запомните! {current_word["eng_word"]} [{current_word["transcription"]}] - {current_word["rus_word"]}\nСледующее слово: {next_word["rus_word"]}'
    return msg


def gen_first_msg_for_words_check_1_lvl(word):
    """
    Эта функция генерирует первое сообщение для проверки первого уровня.
    :param word:
    :return:
    """
    msg = f'Переведите это слово:\n{word["rus_word"]}'
    return msg

words_check_exit_msg = 'Проверка слов остановлена.'
end_of_words_check_1_lvl_msg = 'Вы прошли первый уровень проверки слов!'


def del_first_string(msg):
    """
    Функция удаляет первую строку из сообщения.
    :param msg:
    :return:
    """
    msg = ''.join(msg.split('\n', 1)[1:])
    return msg


def gen_last_msg_for_words_check_1_lvl(word):
    """
    Эта функция генерирует первое сообщение для проверки второго уровня.
    :param word:
    :return:
    """
    msg = f'Вы прошли первый уровень проверки слов!\nЗаполните пропуски в этом слове:\n{word["rus_word"]} - {word["word_with_blanks"]}'
    return msg


def gen_dont_know_last_msg_for_words_check_1_lvl(word, dont_know_word):
    """
    Эта функция генерирует первое сообщение для проверки второго уровня.
    :param word:
    :return:
    """
    msg = f'Запомните! {dont_know_word["eng_word"]} [{dont_know_word["transcription"]}] - {dont_know_word["rus_word"]}.\n\nВы прошли первый уровень проверки слов!\nЗаполните пропуски в этом слове:\n{word["rus_word"]} - {word["word_with_blanks"]}'
    return msg


def gen_next_msg_for_words_check_2_lvl(word):
    """
    Эта функция генерирует следующее сообщение для проверки 2 уровня
    :param word:
    :return:
    """
    msg = f'Следующее слово:\n{word["rus_word"]} - {word["word_with_blanks"]}'
    return msg


def add_letter_words_check_2_lvl(letter, msg):
    """
    Функция генерирует новое сообщение с уже подставленной буквой
    :param letter:
    :param msg:
    :return:
    """
    if letter == 'пробел':
        letter = ' '
    for count, el in enumerate(msg):
        if el == '_':
            new_msg = f'{msg[:count]}{letter}{msg[count+1:]}'
            return new_msg


def add_all_letters_words_check_2_lvl(msg, word):
    """
    Функция заменяет все пропуски на перевод слова.
    :param word:
    :return:
    """
    # учитываем то, чтоо некоторые буквы уже могут быть отгаданы
    count_prompts = msg.count('_')
    num_letters = len(word['eng_word'])
    msg = msg.replace('_'*count_prompts, word['eng_word'][num_letters-count_prompts:])
    return msg


def add_title_remember_words_check_2_lvl(msg):
    """
    Функция добавляет надпись Запомните! к сообщению
    :param msg:
    :return:
    """
    msg = f'Запомните!\n{msg}'
    return msg


def add_title_right_words_check_2_lvl(msg):
    """
    Функция добавляет надпись правильно к сообщению
    :param msg:
    :return:
    """
    msg = f'Правильно!\n{msg}'
    return msg


def add_title_wrong_words_check_2_lvl(msg):
    """
    Функция добавляет надпись неправильно к сообщению
    :param msg:
    :return:
    """
    msg = f'Неправильно!\n{msg}'
    return msg


def add_title_all_right_words_check_2_lvl(msg):
    """
    Функция генерирует сообщение, что все правильно.
    :param msg:
    :return:
    """
    msg = f'Все правильно!\n{msg}'
    return msg


def add_transcription_words_check_2_lvl(msg, word):
    new_msg = f"{msg} [{word['transcription']}]"
    return new_msg


def gen_last_msg_for_words_check_2_lvl(word):
    """
    Эта функция генерирует первое сообщение для проверки второго уровня.
    :param word:
    :return:
    """
    msg = f'Вы прошли первый уровень проверки слов! Напишите перевод этого слова:\n{word["rus_word"]}'
    return msg


def gen_last_msg_for_words_check_3_lvl():
    """
    Функция генерирует последнее завершающее сообщение третьего этапа проверки слов.
    :return:
    """
    msg = 'Поздравляем, вы сдали все слова на сегодня!'
    return msg


def gen_next_msg_for_words_check_3_lvl(next_word):
    """
    Функция возвращает сообщение со следующим словом для проверки.
    :param word:
    :return:
    """
    msg = f'Следующее слово:\n{next_word["rus_word"]}'
    return msg


def gen_wrong_msg_for_words_check_3_lvl():
    msg = 'Неправильно!'
    return msg


def add_transcription_and_translate_words_check_3_lvl(msg, word):
    """
    Функция добавляет к вопрошаемому слову транскрипцию и перевод.
    :param msg:
    :param word:
    :return:
    """
    msg = f'{msg} - {word["eng_word"]} [{word["transcription"]}]'
    return msg


def gen_last_dont_know_msg_for_words_check_3_lvl(last_word):
    """
    Функция генерирует последнее завершающее сообщение третьего этапа проверки слов с условием того, что юзер не знает
    последнего слова
    :return:
    """
    msg = 'Запомните! Поздравляем, вы сдали все слова на сегодня!'
    return msg


def gen_early_dispatch_msg(words_string, words_number_in_dispatch):
    res_msg = f"Ваши {words_number_in_dispatch} слов на сегодня:\n\n{words_string}\nСначала выучите слова, а затем нажмите /сдать слова, чтобы сдать их."
    return res_msg


# сообщения для команды /сдать слова
valid_pass_the_word_msg = 'Вы успешно сдали слова за сегодняшний день!'
invalid_pass_the_word_msg = 'Вы не можете сдать слова, т.к. бот не отправлял их вам. Введите /получить слова, чтобы бот отправил их вам.'
already_learned_words_msg = 'Вы уже выучили слова за сегодняшний день.'
you_learned_the_words_msg = 'Выученные вами слова сданы!'


def gen_everyday_dispatch_msg(words_string, words_number_in_dispatch):
    res_msg = f"Ваши {words_number_in_dispatch} слов на сегодня:\n\n{words_string}\nСначала выучите слова, а затем нажмите /сдать слова, чтобы сдать их."
    return res_msg


def gen_repeat_words_1_msg(words_string):
    """
    Функция для генерации сообщения для первого повторения слов
    :param words_string: 
    :param words_number_in_dispatch: 
    :return: 
    """

    res_msg = f"Первое повторение выученных слов:\n\n{words_string}"

    return res_msg


def gen_repeat_words_2_msg(words_string):
    """
    Функция для генерации сообщения для первого повторения слов
    :param words_string:
    :param words_number_in_dispatch:
    :return:
    """

    res_msg = f"Второе повторение выученных слов:\n\n{words_string}"

    return res_msg


def gen_repeat_words_3_msg(words_string):
    """
    Функция для генерации сообщения для первого повторения слов
    :param words_string:
    :param words_number_in_dispatch:
    :return:
    """

    res_msg = f"Третье повторение выученных слов:\n\n{words_string}"

    return res_msg


def gen_repeat_words_4_msg(words_string):
    """
    Функция для генерации сообщения для первого повторения слов
    :param words_string:
    :param words_number_in_dispatch:
    :return:
    """

    res_msg = f"Предпоследнее четвертое повторение выученных слов!\n\n{words_string}"

    return res_msg


def gen_repeat_words_5_msg(words_string):
    """
    Функция для генерации сообщения для первого повторения слов
    :param words_string:
    :param words_number_in_dispatch:
    :return:
    """

    res_msg = f"Последнее пятое повторение выученных слов!\n\n{words_string}"

    return res_msg


# мотивационные сообщения, которые бот отправляет юзеру в зависимости от того сколько дней юзер пропустил, или наоборот
# сколько дней подряд изучает английский


def every_day_learn_msg_1():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Стабильность и систематичность - путь к достижению успеха! Примени это знание в изучении английского языка и не забрасывай его.'
    return msg


def every_day_learn_msg_2():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Прошлое изменить невозможно, но будущее в вашей власти. А будущее, в котором вы знаете английский язык, смотрится гораздо выгоднее чем то, в котором вы его не знаете)'
    return msg


def every_day_learn_msg_3():
    """
    Мотивирующие сообщение на каждый день, версия 7.
    :return:
    """
    msg = 'Половина пользователей бота сдалась уже после первого дня, не стань одним из них...'
    return msg


def every_day_learn_msg_4():
    """
    Мотивирующие сообщение на каждый день, версия 4.
    :return:
    """
    msg = 'Помни, путь к большой мечте можно преодолеть только маленькими шажками.'
    return msg


def every_day_learn_msg_5():
    """
    Мотивирующие сообщение на каждый день, версия 5.
    :return:
    """
    msg = 'Регулярность и стабильность составляют успех. Будь успешен в изучении английского, не забрасывай его.'
    return msg


def every_day_learn_msg_6():
    """
    Мотивирующие сообщение на каждый день, версия 6.
    :return:
    """
    msg = 'Удели своему образованию всего 5 минут из своего 24-х часового дня и через время результат тебя удивит.'
    return msg


def every_day_learn_msg_7():
    """
    Мотивирующие сообщение на каждый день, версия 3.
    :return:
    """
    msg = 'Чем бы ты сейчас не был занят, попробуй уделить немного времени на самообразование.'
    return msg


def every_day_learn_msg_8():
    """
    Мотивирующие сообщение на каждый день, версия 8.
    :return:
    """
    msg = 'Выдели из своего длинного дня всего пару минут на английский язык и выучи его!'
    return msg


def every_day_learn_msg_9():
    """
    Мотивирующие сообщение на каждый день, версия 9.
    :return:
    """
    msg = 'За тебя английский никто не выучит, вся надежда на тебя)'
    return msg


def every_day_learn_msg_10():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Как же было бы классно слушать музыку, смотреть фильмы и читать книги в оригинале на английском...'
    return msg


def every_day_learn_msg_11():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Владеть другим языком – значит обладать второй душой.'
    return msg


def every_day_learn_msg_12():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Если миллионы людей по всему миру смогли выучить английский, то ты тоже сможешь!'
    return msg


def every_day_learn_msg_13():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Если вы знаете языки, вы везде будете как дома.'
    return msg


def every_day_learn_msg_14():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'C каждым новым языком вы проживаете новую жизнь. Если вы знаете только один язык, вы живете всего один раз.'
    return msg


def every_day_learn_msg_15():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Учить язык, значит открыть новое окно в мир.'
    return msg


def every_day_learn_msg_16():
    """
    Мотивирующие сообщение на каждый день, версия 2.
    :return:
    """
    msg = 'Давай, потрать чуточку времени на английский язык)'
    return msg


def every_day_learn_msg_17():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Настоящее - это результат ваших действий в прошлом, а будущее зависит от того, что вы делаете сейчас. Подумай над этим.'
    return msg


def every_day_learn_msg_18():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Сделай себя лучше, продолжи учить английский!'
    return msg


def every_day_learn_msg_19():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Удели 5 минут на английский!'
    return msg


def every_day_learn_msg_20():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Многие, кто начинал учить английский язык, бросали это дело. Не будь как они, будь лучше)'
    return msg


def every_day_learn_msg_21():
    """
    Мотивирующие сообщение на каждый день, версия 1.
    :return:
    """
    msg = 'Учи английский! Без него сейчас никуда)'
    return msg


def every_day_learn_msg_22():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'Только упорством и настойчивостью можно достичь своей цели. Учи английский)'
    return msg


def every_day_learn_msg_23():
    """
    Мотивирующие сообщение на каждый день, версия 10.
    :return:
    """
    msg = 'С вероятностью 100%, английский язык пригодится тебе в жизни, поэтому было бы неплохо его выучить.'
    return msg


def admission_msg(num_of_day_admission):
    """
    Если юзер пропускает обучение.
    :return:
    """

    if num_of_day_admission == 1:
        msg = 'Вы пропустили один день обучения. Такое бывает, главное осознать свою ошибку и исправиться.'
    elif 1 < num_of_day_admission < 5:
        msg = 'Снова бросили английский язык? Вы пропустили уже несколько дней обучения. Не стоит бросать...'
    elif 4 < num_of_day_admission < 10:
        msg = 'Вы пропустили уже достаточно много дней обучения. Еще не поздно вернуться.'
    else:
        msg = 'Забросили английский... Похоже, что вам бот не нужен. Чтобы отключить рассылку, нажмите /настройки -> /отключить рассылку.'

    return msg


def congratulate_on_learned_words_msg(num_of_learned_words):

    if len(str(num_of_learned_words)) >= 2:
        if int(str(num_of_learned_words)[-2:]) in [11, 12, 13, 14, 15, 16, 17, 18, 19]:
            word = 'слов'
        elif int(str(num_of_learned_words)[-1]) in [2, 3, 4]:
            word = 'слова'
        elif int(str(num_of_learned_words)[-1]) in [0, 5, 6, 7, 8, 9]:
            word = 'слов'
        elif int(str(num_of_learned_words)[-1]) in [1]:
            word = 'слово'
    else:
        if int(str(num_of_learned_words)[-1]) in [2, 3, 4]:
            word = 'слова'
        elif int(str(num_of_learned_words)[-1]) in [0, 5, 6, 7, 8, 9]:
            word = 'слов'
        elif int(str(num_of_learned_words)[-1]) in [1]:
            word = 'слово'

    msg = f'Поздравляем! Вы уже выучили {num_of_learned_words} {word}! Продолжайте в том же духе!'
    return msg


def msg_for_admin_about_new_user(new_user_id):
    """
    Эта функция информирует админа о том, что у бота появился новый юзер
    """
    msg = rf'У бота появился новый юзер: https://vk.com/id{new_user_id}'
    return msg


def msg_for_statistic(num_of_learned_words):
    """
    Функция для генерации сообщения о статистики.
    """

    if len(str(num_of_learned_words)) >= 2:
        if int(str(num_of_learned_words)[-2:]) in [11, 12, 13, 14, 15, 16, 17, 18, 19]:
            word = 'слов'
        elif int(str(num_of_learned_words)[-1]) in [2, 3, 4]:
            word = 'слова'
        elif int(str(num_of_learned_words)[-1]) in [0, 5, 6, 7, 8, 9]:
            word = 'слов'
        elif int(str(num_of_learned_words)[-1]) in [1]:
            word = 'слово'
    else:
        if int(str(num_of_learned_words)[-1]) in [2, 3, 4]:
            word = 'слова'
        elif int(str(num_of_learned_words)[-1]) in [0, 5, 6, 7, 8, 9]:
            word = 'слов'
        elif int(str(num_of_learned_words)[-1]) in [1]:
            word = 'слово'

    msg = f'Вы выучили {num_of_learned_words} {word}.'
    return msg


reminder_message = 'Не забудьте про английский!'

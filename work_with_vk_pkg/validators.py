def enters_local_time_and_dispatch_time_validator(msg):
    """
    Функция для проверки на валидность сообщения, в котором указано локальное время юзера local_time или время рассылки
    юзера dispatch_time.
    :param msg: сообщение со временем
    :return: True or False
    """

    msg = msg.strip()

    if msg.count(':') != 1:
        return False
    else:
        hours = msg.split(':')[0].strip()
        minutes = msg.split(':')[1].strip()

        if (not hours.isdigit()) or (not minutes.isdigit()):
            return False
        else:
            hours = int(hours)
            minutes = int(minutes)

            if 0 <= hours <= 23 and 0 <= minutes <= 59:
                return True
            else:
                return False


def enters_answer_on_bot_license_agreement_validator(msg):
    """
    Функция для проверки сообщения с ответом на вопрос messages.bot_license_agreement_msg. Варианты да/нет.
    :param msg:
    :return:
    """
    msg = msg.strip().lower()
    if msg == 'да' or msg == 'нет':
        return True
    else:
        return False


disable_dispatch_validator = enters_answer_on_bot_license_agreement_validator


def change_number_of_word_in_dispatch_validator(msg):
    """
    Проверяет, является ли сообщение числом. Число должно быть от 5 до 20.
    :param msg:
    :return:
    """
    msg = msg.lower().strip()
    if msg.isdigit():
        n = int(msg)
        if 5 <= n <= 20:
            return True
        else:
            return False
    else:
        return False

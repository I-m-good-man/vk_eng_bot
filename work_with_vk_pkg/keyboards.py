from vk_api import keyboard
import random


def create_keyboard_with_current_time(times_list, first_time=False):
    """
    Функция, которая получает на вход список с временами и генерирует клавиатуру с временами.
    :param times_list:
    :return:
    """
    time_keyboard = keyboard.VkKeyboard()
    for count, t in enumerate(times_list):
        if count % 3 == 0 and count:
            time_keyboard.add_line()
        time_keyboard.add_button(label=t, color=keyboard.VkKeyboardColor.SECONDARY)

    if not first_time:
        time_keyboard.add_line()
        time_keyboard.add_button(label='/отмена', color=keyboard.VkKeyboardColor.NEGATIVE)

    return time_keyboard


def create_keyboard_for_words_check_1_lvl(words_list, right_answer):
    """
    Функция, которая генерирует клавиатуру для проверки первого уровня слов.
    :param right_answer:
    :param words_list:
    :return:
    """
    word_keyboard = keyboard.VkKeyboard()
    words_list = words_list[:]
    words_list.remove(right_answer)
    # список, в который будем добавлять последовательность индексов слов из words_list в произвольном порядке
    nums_list = []

    index_words_list = [i for i in range(len(words_list))]
    for i in range(3):
        random_index = random.randint(0, len(index_words_list) - 1)
        nums_list.append(index_words_list[random_index])
        index_words_list.pop(random_index)

    words_list.append(right_answer)
    nums_list.insert(random.randint(0, 3), len(words_list)-1)

    word_keyboard.add_button(label=words_list[nums_list[0]]['eng_word'], color=keyboard.VkKeyboardColor.SECONDARY)
    word_keyboard.add_button(label=words_list[nums_list[1]]['eng_word'], color=keyboard.VkKeyboardColor.SECONDARY)
    word_keyboard.add_line()
    word_keyboard.add_button(label=words_list[nums_list[2]]['eng_word'], color=keyboard.VkKeyboardColor.SECONDARY)
    word_keyboard.add_button(label=words_list[nums_list[3]]['eng_word'], color=keyboard.VkKeyboardColor.SECONDARY)
    word_keyboard.add_line()
    word_keyboard.add_button(label='/выйти', color=keyboard.VkKeyboardColor.NEGATIVE)
    word_keyboard.add_button(label='/не знаю', color=keyboard.VkKeyboardColor.NEGATIVE)
    return word_keyboard


def create_keyboard_for_words_check_2_lvl(letter_list):
    """
    Эта функция генерирует клавиатуру для проверки слов второго уровня на основе букв.
    :param letter_list:
    :return:
    """

    # запутываем символы в списке букв в произвольном порядке
    new_letter_list = []

    index_list = [i for i in range(len(letter_list))]

    for i in range(len(letter_list)):
        index = random.randint(0, len(index_list)-1)
        # если в слове буква повторяется несколько раз, то делаем только одну букву на клаве
        new_letter_list.append(letter_list[index_list[index]]) if not (letter_list[index_list[index]] in new_letter_list) else None

        index_list.pop(index)

    letter_list = new_letter_list

    # создаем и заполняем клавиатуру
    letter_keyboard = keyboard.VkKeyboard()

    for count, letter in enumerate(letter_list, start=1):
        if count % 4 == 0:
            letter_keyboard.add_line()
        letter_keyboard.add_button(label=letter, color=keyboard.VkKeyboardColor.SECONDARY)

    letter_keyboard.add_line()
    letter_keyboard.add_button(label='/выйти', color=keyboard.VkKeyboardColor.NEGATIVE)
    letter_keyboard.add_button(label='/не знаю', color=keyboard.VkKeyboardColor.NEGATIVE)

    return letter_keyboard


def CALLBACK_create_keyboard_for_words_check_2_lvl(letter_list):
    """
    Эта функция генерирует клавиатуру для проверки слов второго уровня на основе букв.
    :param letter_list:
    :return:
    """

    # запутываем символы в списке букв в произвольном порядке
    new_letter_list = []

    index_list = [i for i in range(len(letter_list))]

    for i in range(len(letter_list)):
        index = random.randint(0, len(index_list)-1)
        # если в слове буква повторяется несколько раз, то делаем только одну букву на клаве
        new_letter_list.append(letter_list[index_list[index]]) if not (letter_list[index_list[index]] in new_letter_list) else None

        index_list.pop(index)

    letter_list = new_letter_list

    # создаем и заполняем клавиатуру
    letter_keyboard = keyboard.VkKeyboard()

    for count, letter in enumerate(letter_list, start=1):
        if count % 4 == 0:
            letter_keyboard.add_line()
        letter_keyboard.add_callback_button(label=letter, color=keyboard.VkKeyboardColor.SECONDARY, payload={'message': letter})

    letter_keyboard.add_line()
    letter_keyboard.add_callback_button(label='/выйти', color=keyboard.VkKeyboardColor.NEGATIVE, payload={'message': '/выйти'})
    letter_keyboard.add_callback_button(label='/не знаю', color=keyboard.VkKeyboardColor.NEGATIVE, payload={'message': '/не знаю'})

    return letter_keyboard


def edit_right_button_words_check_2_lvl(right_letter, last_keyboard):
    """
    Функция изменяет кнопку с правильно отгаданной буквой.
    :param right_letter:
    :param last_keyboard:
    :return:
    """
    for line in last_keyboard.keyboard['buttons']:
        for button in line:
            if button['action']['label'] == right_letter:
                button['color'] = 'positive'

    return last_keyboard


def edit_wrong_button_words_check_2_lvl(wrong_letter, last_keyboard):
    """
    Функция изменяет кнопку с неправильно отгаданной буквой.
    :param right_letter:
    :param last_keyboard:
    :return:
    """
    for line in last_keyboard.keyboard['buttons']:
        for button in line:
            if button['action']['label'] == wrong_letter:
                button['color'] = 'negative'

    return last_keyboard


def remove_red_buttons_words_check_2_lvl(last_keyboard):
    """
    Функция заменяет цвет всех красных кнопок на нейтральный.
    :param last_keyboard:
    :return:
    """
    for line in last_keyboard.keyboard['buttons']:
        for button in line:
            if button['color'] == 'negative':
                if (button['action']['label'] != '/выйти') and (button['action']['label'] != '/не знаю'):
                    button['color'] = 'secondary'

    return last_keyboard


def CALLBACK_create_keyboard_for_words_check_3_lvl():
    """
    Функция, которая делает клавиатуру для проверки слов 3 уровня.
    :return:
    """
    keyboard_3_lvl = keyboard.VkKeyboard()
    keyboard_3_lvl.add_callback_button(label='/выйти', color=keyboard.VkKeyboardColor.NEGATIVE,
                                        payload={'message': '/выйти'})
    keyboard_3_lvl.add_callback_button(label='/не знаю', color=keyboard.VkKeyboardColor.NEGATIVE,
                                        payload={'message': '/не знаю'})
    return keyboard_3_lvl


def create_keyboard_for_words_check_3_lvl():
    """
    Функция, которая делает клавиатуру для проверки слов 3 уровня.
    :return:
    """
    keyboard_3_lvl = keyboard.VkKeyboard()
    keyboard_3_lvl.add_button(label='/выйти', color=keyboard.VkKeyboardColor.NEGATIVE)
    keyboard_3_lvl.add_button(label='/не знаю', color=keyboard.VkKeyboardColor.NEGATIVE)
    return keyboard_3_lvl


# стартовая клавиатура, которая отправляется пользователю при самом первом сообщении "начать"
start_keyboard =keyboard.VkKeyboard()
start_keyboard.add_button(label='/инфо', color=keyboard.VkKeyboardColor.SECONDARY)
start_keyboard.add_line()
start_keyboard.add_button(label='/начать использование', color=keyboard.VkKeyboardColor.SECONDARY)


# клавиатура для отввета на вопрос о ежедневной рассылки от бота
bot_license_agreement_keyboard = keyboard.VkKeyboard()
bot_license_agreement_keyboard.add_button(label='Да', color=keyboard.VkKeyboardColor.POSITIVE)
bot_license_agreement_keyboard.add_button(label='Нет', color=keyboard.VkKeyboardColor.NEGATIVE)


# основная клавиатура до рассылки
base_user_keyboard = keyboard.VkKeyboard()
base_user_keyboard.add_button(label='/настройки', color=keyboard.VkKeyboardColor.SECONDARY)
base_user_keyboard.add_button(label='/команды', color=keyboard.VkKeyboardColor.SECONDARY)
base_user_keyboard.add_line()
base_user_keyboard.add_button(label='/инфо', color=keyboard.VkKeyboardColor.SECONDARY)
base_user_keyboard.add_button(label='/статистика', color=keyboard.VkKeyboardColor.SECONDARY)
base_user_keyboard.add_line()
base_user_keyboard.add_button(label='/получить слова', color=keyboard.VkKeyboardColor.SECONDARY)
base_user_keyboard.add_button(label='/сдать слова', color=keyboard.VkKeyboardColor.SECONDARY)


# клавиатура для настройки бота
setup_bot_keyboard = keyboard.VkKeyboard()
setup_bot_keyboard.add_button(label='/время рассылки', color=keyboard.VkKeyboardColor.SECONDARY)
setup_bot_keyboard.add_line()
setup_bot_keyboard.add_button(label='/количество слов', color=keyboard.VkKeyboardColor.SECONDARY)
setup_bot_keyboard.add_line()
setup_bot_keyboard.add_button(label='/отключить рассылку', color=keyboard.VkKeyboardColor.SECONDARY)
setup_bot_keyboard.add_line()
setup_bot_keyboard.add_button(label='/сложность слов', color=keyboard.VkKeyboardColor.SECONDARY)
setup_bot_keyboard.add_line()
setup_bot_keyboard.add_button(label='/выйти', color=keyboard.VkKeyboardColor.NEGATIVE)

# клавиатура для ответа на вопрос в настройке по поводу согласия на отключение рассылки, кнопки такие же как и в
# согласии на рассылку
setup_bot_disable_dispatch_keyboard = bot_license_agreement_keyboard


# клавиатура для смены уровня сложности слов при настройки
def setup_bot_change_lvl_of_words_keyboard(mode):
    """
    Клавиатура для смены уровня сложности слов при настройкию. В зависимости от текущего уровня сложности
    слов, бот будет отправлять разную клавиатуру.
    """
    setup_bot_change_lvl_of_words_keyboard = keyboard.VkKeyboard()
    if mode == 'pro':
        setup_bot_change_lvl_of_words_keyboard.add_button(label='/базовый уровень', color=keyboard.VkKeyboardColor.SECONDARY)
    elif mode == 'base':
        setup_bot_change_lvl_of_words_keyboard.add_button(label='/продвинутый уровень', color=keyboard.VkKeyboardColor.SECONDARY)
    setup_bot_change_lvl_of_words_keyboard.add_line()
    setup_bot_change_lvl_of_words_keyboard.add_button(label='/отмена', color=keyboard.VkKeyboardColor.NEGATIVE)

    return setup_bot_change_lvl_of_words_keyboard


# клавиатура с сообщением "отмена"
cancel_keyboard = keyboard.VkKeyboard()
cancel_keyboard.add_button(label='/отмена', color=keyboard.VkKeyboardColor.NEGATIVE)

# print(setup_bot_keyboard.keyboard)

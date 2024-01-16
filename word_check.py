import random


"""

В этом модуле определены функции  для проверки сдачи слов боту.

"""


def make_the_prompt_in_word(word):
    """
    Эта функция делает пропуски в словах, например word => ____
    :return:
    """
    new_word = len(word) * '_'
    missing_letters_list = list(word)
    for index, letter in enumerate(missing_letters_list):
        if letter == ' ':
            missing_letters_list.pop(index)
            missing_letters_list.insert(index, 'пробел')
    return new_word, missing_letters_list


def __make_the_prompt_in_word__(word):
    """
    Эта функция делает пропуски в словах, например word => w_r_


    ПОКА ЗАМЕНЕНА НА ДУРГУЮ ФУНКЦИЮ!!!



    :return:
    """


    # список, в котром хранятся списки - [индекс замененной буквы, сама замененная буква]
    missing_letters_list = []

    # index - это индекс символа, который заменяем на _
    if len(word) == 1:
        missing_letters_list.append([0, word[0]])
        word = '_'

    elif len(word) == 2:
        index = random.randint(0, 1)
        missing_letters_list.append([index, word[index]])
        word = f'_{word[1]}' if index == 0 else f'{word[0]}_'

    elif len(word) == 3:
        index = random.randint(0, 2)
        missing_letters_list.append([index, word[index]])
        if index == 0:
            word = f'_{word[1:]}'
        elif index == 1:
            word = f'{word[0]}_{word[2]}'
        else:
            word = f'{word[:2]}_'

    else:
        l = len(word)

        index_list = []

        num_index = int(l // 2)

        word_index_list = [i for i in range(len(word))]

        for i in range(num_index):
            index = random.randint(0, len(word_index_list)-1)
            index_list.append(word_index_list[index])
            missing_letters_list.append([word_index_list[index], word[word_index_list[index]]])
            word_index_list.pop(index)

        for index in index_list:
            if index == len(word)-1:
                word = f'{word[:index]}_'
            else:
                word = f'{word[:index]}_{word[index+1:]}'

    missing_letters_list.sort(key=lambda x: x[0])
    missing_letters_list = [el[1] for el in missing_letters_list]

    return word, missing_letters_list

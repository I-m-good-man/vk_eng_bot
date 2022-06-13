import work_with_time


class User:
    """
    Это конечный автомат для пользователя, он фиксирует состояния юзеров.
    """

    def __init__(self, user_id):

        """
        Состояния:
        enters_answer_on_bot_license_agreement - при базовой настройке юзер отвечает на вопрос о соглашении с рассылкой.
        enters_local_time - при базовой настройке юзер вводит его локальное время.
        enters_dispatch_time - при базовой настройке юзер вводит время рассылки.

        setup_bot - юзер меняет настройки бота
        setup_bot_change_number_of_word_in_dispatch - в настройке юзер меняет кол-во слов в рассылке.
        setup_bot_enters_local_time - в настройке юзер меняет меняет время расслыки, вводит локальное время
        setup_bot_enters_dispatch_time - в настройке юзер меняет время рассылки, вводит время рассылки.
        setup_bot_disable_dispatch - в настройке юзер отключает рассылку.
        setup_bot_change_lvl_of_words - в настрйоке меняет уровень сложности слов.

        words_check - состояние для проверки слов(сдача слов).
        switch_words_check_1_lvl - первый уровень сдачи слов.
        switch_words_check_2_lvl - второй уровень сдачи слов.
        switch_words_check_3_lvl - третий уровень сдачи слов.

        :param user_id:
        """

        self.user_id = user_id

        # сосотояния для базовой настройки
        self.enters_answer_on_bot_license_agreement = False
        self.enters_local_time = False
        self.enters_dispatch_time = False

        # состояния для расширенной настройки и изменений в боте
        self.setup_bot = False
        self.setup_bot_change_number_of_word_in_dispatch = False
        self.setup_bot_enters_dispatch_time = False
        self.setup_bot_enters_local_time = False
        self.setup_bot_disable_dispatch = False
        self.setup_bot_change_lvl_of_words = False

        # состояния для проверки слов
        self.words_check = False
        self.words_check_1_lvl = False
        self.words_check_2_lvl = False
        self.words_check_3_lvl = False


    def __setattr__(self, key, value):
        """
        Перегружаем метод присвоения атрибута для того чтобы при каждом обращении к объекту, указывать время этого
        обращения. Это нужно чтобы мы могли написать в дальнейшем алгоритм для удаления слишком старых юзеров
        :param key:
        :param value:
        :return:
        """
        self.__dict__[key] = value
        self.__dict__['last_time_contact'] = int(work_with_time.get_current_server_time())

    def switch_enters_answer_on_bot_license_agreement(self, value):
        self.enters_answer_on_bot_license_agreement = value

    def switch_enters_local_time(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера enters_local_time (ввода локального времени, когда юзер
        указывает время рассылки, нужно узнать локальное время юзера) на True или False.
        :param value:
        :return:
        """
        self.enters_local_time = value

    def switch_enters_dispatch_time(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера enters_dispatch_time (ввода времени рассылки сообщения со
         словами, на True или False.
        :param value:
        :return:
        """
        self.enters_dispatch_time = value

    def switch_setup_bot(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера setup_bot (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.setup_bot = value

    def switch_setup_bot_enters_dispatch_time(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера setup_bot_enters_dispatch_time (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.setup_bot_enters_dispatch_time = value

    def switch_setup_bot_change_number_of_word_in_dispatch(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера setup_bot_change_number_of_word_in_dispatch (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.setup_bot_change_number_of_word_in_dispatch = value

    def switch_setup_bot_enters_local_time(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера setup_bot_enters_local_time (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.setup_bot_enters_local_time = value

    def switch_setup_bot_disable_dispatch(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера setup_bot_disable_dispatch (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.setup_bot_disable_dispatch = value

    def switch_setup_bot_change_lvl_of_words(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера setup_bot_change_lvl_of_words (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.setup_bot_change_lvl_of_words = value

    def switch_words_check(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера words_check (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.words_check = value

    def switch_words_check_1_lvl(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера words_check_1_lvl (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.words_check_1_lvl = value

    def switch_words_check_2_lvl(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера words_check_2_lvl (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.words_check_2_lvl = value

    def switch_words_check_3_lvl(self, value):
        """
        Функция, которая при ее вызове меняет состояние юзера words_check_3_lvl (Настройки бота, при которой.
         Меняет значение на True или False.
        :param value:
        :return:
        """
        self.words_check_3_lvl = value






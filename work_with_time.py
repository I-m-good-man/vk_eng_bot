import time
import datetime


def get_current_server_time():
    """
    Функция, которая возвращает текущее серверное время в секундах.
    :return:
    """
    return int(time.time())


def get_current_server_handy_time():
    """
    Функция, возвращающая серверное время в мощном и удобном формате
    :return:
    """
    server_time = time.time()
    server_time = time.ctime(server_time)
    server_time = time.strptime(server_time, '%a %b  %d %H:%M:%S %Y')
    return server_time


def get_date_to_sec(date):
    """
    Функция, которая возвращает дату в секундах
    :return:
    """
    date_sec = datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()

    return date_sec


def get_db_valid_format_of_date(date):
    date = [date.split('.')[-1], date.split('.')[1], date.split('.')[0]]
    date = '-'.join(date)
    return date


def difference_in_time(user_time, dispatch_time, server_time):
    """
    Функция, которая находит разницу между локальным временем юзера и сервверным временем, т.о. создавая зависимость
    локального времени относительно серверного - dif.
    :param user_time: локальное время юзера
    :param dispatch_time: время рассылки
    :param server_time: время сервера в момент отправки пользователем своего времени.
    :return: server_dispatch_time: время отправки для сервера
    """

    # преобразуем серверное время в секунды
    server_time = time.ctime(server_time)
    server_time = time.strptime(server_time, '%a %b  %d %H:%M:%S %Y')
    sec_server_time = server_time.tm_hour * 3600 + server_time.tm_min * 60

    # преобразуем время пользователя в секунды
    user_time = user_time.strip()
    sec_user_time = int(user_time.split(':')[0].strip()) * 3600 + int(user_time.split(':')[1].strip()) * 60

    # преобразуем время рассылки в секунды
    dispatch_time = dispatch_time.strip()
    sec_dispatch_time = int(dispatch_time.split(':')[0].strip()) * 3600 + int(dispatch_time.split(':')[1].strip()) * 60

    # dif - это разница между серверным временем и локальным временем юзера относительно серверного времени, т.е.
    # например dif=-7 значит, что если от серверного времени отнять 7, то получится локальное время юзера, а если
    # dif=7 - это значит, что если к серверном времени прибавить 7, то получится локальное время пользователя
    if sec_user_time > sec_server_time:
        dif = sec_user_time - sec_server_time
        if (24/2)*3600 < dif:
            dif = 24 * 3600 - dif
            # присваеваем отрицательное значение, т.к. идет переход через день
            dif = -dif
    elif sec_user_time < sec_server_time:
        dif = sec_server_time - sec_user_time
        if (24 / 2) * 3600 < dif:
            dif = 24 * 3600 - dif
        dif = -dif
    else:
        dif = 0

    # находим серверное время отправки сообщения
    server_dispatch_time = sec_dispatch_time - dif
    if server_dispatch_time >= 24 * 3600:
        server_dispatch_time = server_dispatch_time - (24 * 3600)
    elif server_dispatch_time < 0:
        server_dispatch_time = 24 * 3600 + server_dispatch_time

    server_dispatch_time = str(datetime.timedelta(seconds=int(server_dispatch_time)))[:-3]

    return server_dispatch_time


def gen_times_of_all_russian_time_zone(dif_w_moscow=-2):
    """
    Функция, которая генерирует строки со временем в зависимости от текущего времени, чтобы задать таким образом все
    возможные часовые пояса.
    Разница во времен относительно Москвы с крупными городами - -1 до 9 часов. Поэтому относительно московского времени
    генерим строки с почасовой разницей

    dif_w_moscow - это часовая разница с московским временем, нужна для координации с серверным временем.
    Для Уфы dif_w_moscow = -2.
    :return:
    """
    # находим серверное время
    server_time = time.time()
    server_time = time.ctime(server_time)
    server_time = time.strptime(server_time, '%a %b  %d %H:%M:%S %Y')
    server_hour, server_minute = server_time.tm_hour, server_time.tm_min

    # определяем московское время
    moscow_hour, moscow_minute = server_hour + dif_w_moscow, server_minute
    if moscow_hour < 0:
        moscow_hour = 24 + moscow_hour
    if moscow_hour >= 24:
        moscow_hour = moscow_hour - 24

    # список, в который будут добавляться сгенерированные строки с временами
    list_with_times = []

    # добавляем московское время в список
    str_moscow_hour = str(moscow_hour)
    str_moscow_minute = str(moscow_minute)
    if len(str_moscow_hour) == 1:
        str_moscow_hour = f'0{str_moscow_hour}'
    if len(str_moscow_minute) == 1:
        str_moscow_minute = f'0{str_moscow_minute}'
    res_moscow_time = f'{str_moscow_hour}:{str_moscow_minute}'
    list_with_times.append(res_moscow_time)

    # генерируем времена для остальных городов
    for dif_w_cities in range(-1, 10):
        city_hour = moscow_hour + dif_w_cities
        city_minute = moscow_minute

        if city_hour < 0:
            city_hour = 24 + city_hour
        if city_hour >= 24:
            city_hour = city_hour - 24

        city_hour = str(city_hour)
        city_minute = str(city_minute)

        if len(city_hour) == 1:
            city_hour = f'0{city_hour}'
        if len(city_minute) == 1:
            city_minute = f'0{city_minute}'

        res_time = f'{city_hour}:{city_minute}'

        list_with_times.append(res_time)

    # передвигаем уфимсков время в начало списка
    ufa_time = list_with_times.pop(4)
    list_with_times.insert(0, ufa_time)

    return list_with_times


def gen_dispatch_time():
    """
    Функция генерирует возможные времена рассылки.
    :return:
    """
    list_with_times = []

    for h in range(7, 24, 2):
        res_t = f'{f"0{h}" if len(str(h)) == 1 else h}:00'
        list_with_times.append(res_t)

    return list_with_times

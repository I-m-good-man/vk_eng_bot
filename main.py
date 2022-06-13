from work_with_vk_pkg import vk
from vk_api.bot_longpoll import VkBotEventType
import fsm
import vk_api
import message_handler
import requests
import dispatch
import multiprocessing
import database



def main():
    # словарь с пользователями для работы FSM. user_id: user - юзер айди соответствует экземпляру класса User из FSM
    users_dict = {}

    while True:
        try:
            # первое время для отсчета проверки людей на активность
            time_1 = fsm.work_with_time.time.time()
            for event in vk.bot_longpoll.listen():

                if event.type == VkBotEventType.MESSAGE_NEW or event.type == VkBotEventType.MESSAGE_EVENT:
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        user_id = event.object.message['from_id']
                    elif event.type == VkBotEventType.MESSAGE_EVENT:
                        user_id = event.object['user_id']
                    if user_id not in users_dict:
                        users_dict[user_id] = fsm.User(user_id)

                    # удаляем старых юзеров из фсм для оптимизации работы
                    if len(users_dict) > 100:
                        for user in list(users_dict.keys()):
                            if (dispatch.work_with_time.get_current_server_time() - users_dict[user].last_time_contact) > 7200:
                                users_dict.pop(user)

                    res = message_handler.handlers(event, users_dict[user_id])

                    response_msg, keyboard = res

                    # если сообщение есть, то тогда отправляем его
                    if response_msg:
                        vk.send_message(user_id, response_msg, keyboard)

                    # каждые два часа просматриваем состояния пользователей
                    current_time = fsm.work_with_time.time.time()
                    if (current_time - time_1) > 7200:
                        time_1 = current_time
                        for user in list(users_dict.keys()):
                            if (dispatch.work_with_time.get_current_server_time() - users_dict[user].last_time_contact) > 7200:
                                if database.check_user_in_user_data_table(users_dict[user].user_id):
                                    if users_dict[user].setup_bot or users_dict[user].words_check:
                                        vk.send_message(users_dict[user].user_id, message_handler.messages.base_keyboard_msg,
                                                        message_handler.keyboards.base_user_keyboard.get_keyboard())

                                        users_dict.pop(user)
                                    else:
                                        if len(users_dict) > 50:
                                            users_dict.pop(user)
                                            del users_dict[user]

                    """
                    try:
                        vk.send_message(user_id, response_msg, keyboard)
                    except vk_api.exceptions.ApiError:
                        print('юзер запретил сообщения боту')
                    """


        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        except vk_api.exceptions.ApiError:
            pass
        # если пользователь заблокировал бота, то сразу удаляем его из бд
        except vk_api.exceptions.AccessDenied:
            process = multiprocessing.Process(target=database.delete_user_from_bot, args=(user_id,))
            process.start()
        except:
            pass



"""
if __name__ == '__main__':
    thread_1 = threading.Thread(target=main)
    thread_2 = threading.Thread(target=dispatch.main)

    thread_1.start()
    thread_2.start()
"""


if __name__ == '__main__':

    process_1 = multiprocessing.Process(target=main)
    process_2 = multiprocessing.Process(target=dispatch.main)

    process_1.start()
    process_2.start()




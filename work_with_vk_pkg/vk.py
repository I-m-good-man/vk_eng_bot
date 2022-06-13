from vk_api.bot_longpoll import VkBotLongPoll
import vk_api
from work_with_vk_pkg import config
import random


# токен и id группы
token = config.token
group_id = config.group_id
# авторизуемся в вк апи
vk_session = vk_api.vk_api.VkApiGroup(token=token)
# vk_session = vk_api.VkApi(token=token)
# подключаем бота к longpoll серверу
bot_longpoll = VkBotLongPoll(vk_session, group_id=group_id)


# функция для отправки сообщения пользователю
def send_message(user_id, msg=None, keyboard=None, att=None):
    try:
        vk_session.method('messages.send', {
            'random_id': random.randrange(-10000000, 10000000),
            'user_id': user_id,
            'message': msg,
            'attachment': att,
            'keyboard': keyboard})
        return 'good'
    except:
        return


# функция для изменения сообщения
def edit_message(user_id, msg, msg_id, keyboard=None):

    vk_session.method('messages.edit', {
        'peer_id': user_id,
        'message': msg,
        'message_id': msg_id,
        'keyboard': keyboard
    })


# функция для получения msg_id последнего сообщения
def id_of_last_msg(user_id):
    last_msg = vk_session.method('messages.getHistory', {
        'user_id': user_id,
        'count': 1
    })
    msg_id = last_msg['items'][0]['id']
    return msg_id


# функция для получения msg_id последнего сообщения
def id_of_last_bot_msg(user_id):
    messages = vk_session.method('messages.getHistory', {
        'user_id': user_id,
        'count': 20
    })

    for msg in messages['items']:
        if msg['from_id'] == (group_id * (-1)):
            msg_id = msg['id']
            return msg_id





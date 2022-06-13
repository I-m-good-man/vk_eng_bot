from work_with_vk_pkg import vk, config
from database import get_all_users_from_user_data_table


msg = 'Тестовое сообщение'
admin_user_id = config.admin_user_id


if not msg:
    print('Сообщение не введено.')
    input('press enter...')
else:
    print(f'Так выглядит сообщение для рассылки:\n{msg}\n')

    reply = ''
    while reply not in ['1', '2']:
        reply = input('Chose the mod of work:\n1 - Test\n2 - Main\nYour answer: ')

        if reply in ['1', '2']:
            check_reply = input(r'Точно отправляем?(y\n)'+'\nВаш ответ: ')

            if check_reply == 'y':

                if reply == '1':
                    vk.send_message(admin_user_id, msg)
                    print('Сообщение доставлено админу.')
                    break
                elif reply == '2':
                    counter = 0
                    all_users = get_all_users_from_user_data_table()
                    for user_id in all_users:
                        try:
                            rep = vk.send_message(user_id, msg)
                            if rep == 'good':
                                counter += 1
                        except:
                            pass
                    print(f'Сообщение получили: {counter}')

                    break
            else:
                print('Отправка отменена.')
                break

input('press enter...')








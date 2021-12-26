import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='c45b8a3ca1b40d4eba082ebf68b694871b67702dafa5fb264424e42c1a87b9721b1b39ccc796711a60697')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text == 'Первый вариант фразы' or event.text == 'Второй вариант фразы':  # Если написали заданную фразу
            if event.from_user:  # Если написали в ЛС
                vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    message='Ваш текст',
                    random_id=0
                )
            elif event.from_chat:  # Если написали в Беседе
                vk.messages.send(  # Отправляем собщение
                    chat_id=event.chat_id,
                    message='Ваш текст',
                    random_id=0
                )
    elif event.type == VkEventType.MESSAGE_EDIT:
        vk.messages.send(  # Отправляем сообщение
            user_id=event.user_id,
            message='Изменил сообщение',
            random_id=0
        )
    elif event.type == VkEventType.USER_TYPING:
        vk.messages.send(  # Отправляем сообщение
            user_id=event.user_id,
            message='Че печатаешь?',
            random_id=0
        )

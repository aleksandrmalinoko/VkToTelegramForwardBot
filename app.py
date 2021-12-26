import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import telebot
from telebot import types
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
vk_api_token = config['vk']['vk_api_token']
telegram_api_token = config['telegram']['telegram_api_token']
telegram_chat_id = config['telegram']['telegram_chat_id']

class VkServer:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.telegram_bot = telebot.TeleBot(token=telegram_api_token)

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.WALL_POST_NEW:
                try:
                    post_text = event.obj.text
                except:
                    continue
                try:
                    attachments = event.obj.attachments
                    medias = []
                    for attachment in attachments:
                        photo_url = attachment['photo']['sizes'][-1]['url']
                        medias.append(types.InputMediaPhoto(photo_url, post_text))
                        post_text = ''
                    self.telegram_bot.send_media_group(telegram_chat_id, medias)
                except:
                    self.telegram_bot.send_message(telegram_chat_id, post_text)


if __name__ == '__main__':
    vk_server = VkServer(vk_api_token, 179778319, "server1")
    vk_server.start()
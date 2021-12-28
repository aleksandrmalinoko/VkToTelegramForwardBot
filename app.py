import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import telebot
from telebot import types
import configparser
from time import sleep

config = configparser.ConfigParser()
config.read('config.ini')
vk_api_token = config['vk']['vk_api_token']
vk_group_id = config['vk']['group_id']
telegram_api_token = config['telegram']['telegram_api_token']
telegram_chat_id = config['telegram']['telegram_chat_id']


class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('LongPoll Error (VK):', e)
                print('Trying again', e)


class VkServer:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk_api_token = api_token
        self.group_id = group_id
        self.telegram_bot = telebot.TeleBot(token=telegram_api_token)
        self.vk = vk_api.VkApi(token=self.vk_api_token)
        self.long_poll = MyVkBotLongPoll(self.vk, self.group_id)
        self.vk_api = self.vk.get_api()

    def send_message(self, text):
        try:
            self.telegram_bot.send_message(telegram_chat_id, text)
        except Exception as e:
            print("Error while posting media: ", e)

    def send_media(self, medias):
        try:
            self.telegram_bot.send_media_group(telegram_chat_id, medias)
        except Exception as e:
            print("Error while posting media: ", e)

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.WALL_POST_NEW:
                try:
                    post_text = event.obj.text
                except:
                    continue
                if 'attachments' in event.obj:
                    attachments = event.obj.attachments
                    medias = []
                    for attachment in attachments:
                        if attachment['type'] == 'photo':
                            photo_url = attachment['photo']['sizes'][-1]['url']
                            medias.append(types.InputMediaPhoto(photo_url, post_text))
                            post_text = ''
                    if len(medias) != 0:
                        self.send_media(medias)
                    else:
                        self.send_message(event.obj.text)
                else:
                    self.send_message(event.obj.text)


if __name__ == '__main__':
    vk_server = VkServer(vk_api_token, vk_group_id, "server1")
    vk_server.start()

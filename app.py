import time
import datetime

import vk_api.utils
import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import telebot
from telebot import types
import configparser
import logging

logging.basicConfig(filename="logs/vk_forwarding.log", level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')
vk_api_token = config['vk']['vk_api_token']
vk_group_id = config['vk']['group_id']
telegram_api_token = config['telegram']['telegram_api_token']
telegram_chat_id = config['telegram']['telegram_chat_id']
sign_text = config['sign']['text']
sign_url = config['sign']['url']

class MyVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        try:
            for event in self.check():
                yield event
        except Exception as e:
            logging.error(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}. Error while getting event from VK: {e}")


class VkServer:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk_api_token = api_token
        self.group_id = group_id
        self.telegram_bot = telebot.TeleBot(token=telegram_api_token)
        self.vk = vk_api.VkApi(token=self.vk_api_token)
        self.long_poll = MyVkBotLongPoll(self.vk, self.group_id)
        self.vk_api = self.vk.get_api()
        self.telegram_update_id = -1

    def send_message(self, text):
        try:
            self.telegram_bot.send_message(telegram_chat_id, text, parse_mode='MarkdownV2', disable_web_page_preview=True)
            logging.info(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}. Add post without media.\nText: {text}")
        except Exception as e:
            logging.error(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}. Error while posting: {e}\nText: {text}")

    def send_media(self, medias):
        try:
            self.telegram_bot.send_media_group(telegram_chat_id, medias)
            logging.info(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}. Add post. Count medias: {len(medias)}")
        except Exception as e:
            logging.error(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}. Error while posting media: {e}")

    def get_updates_from_vk(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.WALL_POST_NEW:
                if int((datetime.datetime.utcfromtimestamp(event.object.date).strftime('%M'))) % 10 == 9:
                    continue
                try:
                    post_text = f"{event.obj.text}\n*{sign_text}{sign_url}*"
                except Exception as e:
                    logging.info(
                        f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}. Skipped post without text")
                    continue
                if 'attachments' in event.obj:
                    attachments = event.obj.attachments
                    medias = []
                    for attachment in attachments:
                        if attachment['type'] == 'photo':
                            photo_url = attachment['photo']['sizes'][-1]['url']
                            medias.append(types.InputMediaPhoto(photo_url, post_text, parse_mode='MarkdownV2'))
                            post_text = ''
                    if len(medias) != 0:
                        self.send_media(medias)
                    else:
                        self.send_message(post_text)
                else:
                    self.send_message(post_text)

    # def get_updates_from_telegram(self):
    #     for event in self.telegram_bot.get_updates(offset=self.telegram_update_id + 1):
    #         print(event)
    #         self.telegram_update_id = event.update_id


if __name__ == '__main__':
    vk_server = VkServer(vk_api_token, vk_group_id, "vk_telegram_server")
    while True:
        vk_server.get_updates_from_vk()
        # vk_server.get_updates_from_telegram()

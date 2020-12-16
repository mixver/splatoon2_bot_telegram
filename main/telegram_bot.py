import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import time

import os
import shutil
import requests
import json
import random
import urllib.parse

from reply import replySalmonRun,replyBattle,replyRandom

import sys
sys.path.append('../splatoon2_bot_core/')
from config import BOT_TOKEN
from base_config import API_RANKED, API_REGULAR, API_LEAGUE,TMP_IMG,TMP_DIR
from translation import STAGES, TIME, BATTLE_TYPES,CN_LEAGUE, CN_RANKED, CN_REGULAR
MODES = {API_LEAGUE: CN_LEAGUE, API_RANKED: CN_RANKED, API_REGULAR: CN_REGULAR}



def main():
    global update_id
    bot = telegram.Bot(BOT_TOKEN)

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1



t=time.time()
def echo(bot):
    global update_id
    def anyIn(keywords: [str]) -> bool:
        return any(keyword in update.message.text for keyword in keywords)
    # 在最后一个update_id之后请求更新
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  
            if update.message.text:
                if update.message.text.startswith('/start'):
                    customKeyboard=[
                        ['/查询单排','/查询组排','/查询打工'],
                        ['/查询下个单排','/查询下个组排'],
                        ['/查询随机']
                    ]
                    replyCustomKeyboard = telegram.ReplyKeyboardMarkup(customKeyboard)
                    bot.send_message(update.message.chat_id, "Splatoon2Bot start!", reply_markup=replyCustomKeyboard)
                if update.message.text.startswith('/查询打工'):
                    replySalmonRun(update,int(t))
                if update.message.text.startswith('/查询单排'):
                    mode = API_RANKED
                    replyBattle(update,mode,int(t),update.message.text)
                if update.message.text.startswith('/查询组排'):
                    mode = API_LEAGUE
                    replyBattle(update,mode,int(t),update.message.text)
                if update.message.text.startswith('/查询随机'):
                    replyRandom(update,update.message.text)
                if update.message.text.startswith('/查询下个单排'):
                    mode = API_RANKED
                    replyBattle(update,mode,int(t),update.message.text)
                # if update.message.text.startswith('/查询下个组排'):
                if anyIn("组排"):
                    mode = API_LEAGUE
                    replyBattle(update,mode,int(t),update.message.text)
        
if __name__ == '__main__':
    main()